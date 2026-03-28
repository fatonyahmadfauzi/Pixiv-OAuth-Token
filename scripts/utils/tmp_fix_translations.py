import re
import os
from pathlib import Path

# Resolve project root relative to this script's location (scripts/utils/ -> project root)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

def p(relative_path):
    """Convert project-relative path to absolute path."""
    return str(PROJECT_ROOT / relative_path)

def fix_app_js(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    replacements = [
        (r'(id:\{.*?footerPixivLink:\")Pixiv OAuth(\")', r'\1Endpoint Pixiv OAuth\2'),
        (r'(jp:\{.*?footerPixivLink:\")Pixiv OAuth(\")', r'\1Pixiv OAuth エンドポイント\2'),
        (r'(zh:\{.*?footerPixivLink:\")Pixiv OAuth(\")', r'\1Pixiv OAuth 端点\2'),
        (r'(de:\{.*?footerPixivLink:\")Pixiv OAuth(\")', r'\1Pixiv OAuth Endpunkt\2'),
        (r'(es:\{.*?footerPixivLink:\")Pixiv OAuth(\")', r'\1Endpoint de Pixiv OAuth\2'),
        (r'(fr:\{.*?footerPixivLink:\")Point OAuth(\")', r'\1Point de terminaison OAuth de Pixiv\2'),
        (r'(ru:\{.*?footerPixivLink:\")Pixiv OAuth(\")', r'\1Конечная точка Pixiv OAuth\2'),
        (r'(pt:\{.*?footerPixivLink:\")Pixiv OAuth(\")', r'\1Endpoint do Pixiv OAuth\2'),
        (r'(kr:\{.*?footerPixivLink:\")Pixiv OAuth(\")', r'\1Pixiv OAuth 엔드포인트\2'),
    ]

    original = content
    for pattern, repl in replacements:
        content = re.sub(pattern, repl, content)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated app.js: {filepath}")
    else:
        print(f"No changes for app.js: {filepath}")

def fix_html_js(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    keys = [
        "footerProductTitle", "footerHomeLink", "footerDownloadLink", "footerTutorialLink",
        "footerSourceLink", "footerResourceTitle", "footerDocsLink", "footerChangelogLink",
        "footerPixivLink", "footerPythonLink", "footerVercelLink", "footerSupportTitle",
        "footerIssueLink", "footerDiscussLink", "footerDevLink", "footerContactTitle"
    ]

    for key in keys:
        search1 = f'id="{key}"'
        repl1 = f'id="{key}" data-i18n="{key}"'
        search2 = f"id='{key}'"
        repl2 = f"id='{key}' data-i18n='{key}'"

        # Don't double replace
        if repl1 not in content:
            content = content.replace(search1, repl1)
        if repl2 not in content:
            content = content.replace(search2, repl2)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated HTML/JS: {filepath}")
    else:
        print(f"No changes for HTML/JS: {filepath}")

# Process app.js
fix_app_js(p("web/src_backup/public__assets__app.js"))
fix_app_js(p("web/public/assets/app.js"))

# Process HTML/footer files
fix_html_js(p("web/src_backup/public__components__footer.js"))
fix_html_js(p("web/src_backup/public__tutorial.html"))
fix_html_js(p("web/public/components/footer.js"))
fix_html_js(p("web/public/tutorial.html"))
