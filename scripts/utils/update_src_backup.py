import re
import os

base_dir = r"C:\Users\faton\Downloads\Pixiv-OAuth-Token\web"
pub_index = os.path.join(base_dir, "public", "index.html")
pub_style = os.path.join(base_dir, "public", "assets", "style.css")

bak_index = os.path.join(base_dir, "src_backup", "public__index.html")
bak_style = os.path.join(base_dir, "src_backup", "public__assets__style.css")

# Read the minified public files
with open(pub_index, "r", encoding="utf-8") as f:
    pub_html = f.read()

with open(pub_style, "r", encoding="utf-8") as f:
    pub_css = f.read()

# EXTRACT HTML
m_html = re.search(r'<div class="cli-code-shell">.*?</svg></div>', pub_html, re.DOTALL)
if not m_html:
    print("Could not find cli-code-shell in HTML")
    exit(1)
new_cli_html = m_html.group(0)

# EXTRACT SCRIPT
m_script = re.search(r'<script>\(function\(\)\{const e=document\.querySelector.*?</script>', pub_html, re.DOTALL)
if not m_script:
    print("Could not find the SVG script")
    exit(1)
new_cli_script = m_script.group(0)

# EXTRACT CSS
# The styles we want to add start from @keyframes cliDotPulse
m_css = re.search(r'@keyframes cliDotPulse.*', pub_css, re.DOTALL)
if not m_css:
    print("Could not find animation CSS")
    exit(1)
new_anim_css = m_css.group(0)

# READ BACKUP
with open(bak_index, "r", encoding="utf-8") as f:
    orig_bak_html = f.read()

with open(bak_style, "r", encoding="utf-8") as f:
    orig_bak_css = f.read()

# PATCH HTML
# replace the old <div class="cli-code-shell"> ... </div>
patched_html = re.sub(r'<div class="cli-code-shell">.*?</div>\s*</section>', new_cli_html + '\n    </section>', orig_bak_html, flags=re.DOTALL)

# replace the old loop script: <script>\n    (function () {\n      const flowEl = document.getElementById("cliFlowAnim"); ... </script>
patched_html = re.sub(r'<script>\s*\(function \(\) \{\s*const flowEl = document\.getElementById\("cliFlowAnim"\);.*?</script>', new_cli_script, patched_html, flags=re.DOTALL)

# PATCH CSS
# Just append the CSS to the end of the backup file (replacing the old cli split if present)
new_media_override = "@media (max-width:980px){.cli-preview,.cli-flow-console{min-height:220px}.cli-console-split{grid-template-columns:1fr;gap:20px}.cli-login-target{padding:0 13ch 0 0!important;margin-left:0!important}.cli-login-target-dot{left:100%!important}}"
patched_css = re.sub(r'/\*\s*CLI split panel.*', f"/* CLI split panel and flow animations */\n{new_media_override}\n\n{new_anim_css}\n", orig_bak_css, flags=re.DOTALL)


with open(bak_index, "w", encoding="utf-8") as f:
    f.write(patched_html)

with open(bak_style, "w", encoding="utf-8") as f:
    f.write(patched_css)

print("Synchronized correctly!")
