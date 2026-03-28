import os
import re

# data-nav = ID yang di-EXCLUDE (halaman sembunyikan link dirinya sendiri)
# Halaman yg tidak ada di NAV_LINKS = data-nav kosong (tampilkan semua 4)
pages_public = {
    'contact.html':       {'i18n': 'navHeaderContact',   'label': 'CONTACT',     'nav': ''},
    'discussions.html':   {'i18n': 'navHeaderDiscuss',   'label': 'DISCUSSIONS', 'nav': ''},
    'documentation.html': {'i18n': 'navHeaderDocs',      'label': 'DOCS',        'nav': ''},
    'downloads.html':     {'i18n': 'navHeaderDownload',  'label': 'DOWNLOAD',    'nav': 'navDownloads'},
    'issues.html':        {'i18n': 'navHeaderIssues',    'label': 'ISSUES',      'nav': ''},
    'license.html':       {'i18n': 'navHeaderLicense',   'label': 'LICENSE',     'nav': ''},
    'support.html':       {'i18n': 'footerDonateLink',   'label': 'SUPPORT',     'nav': ''},
    'changelog.html':     {'i18n': 'navHeaderChangelog', 'label': 'CHANGELOG',   'nav': ''},
}

base = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'public'))

for filename, cfg in pages_public.items():
    fpath = os.path.join(base, filename)
    if not os.path.exists(fpath):
        print(f'SKIP: {filename}')
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Build replacement script tag
    nav_attr = f' data-nav="{cfg["nav"]}"' if cfg['nav'] else ''
    new_script = (
        f'<script defer src="/components/header.js"'
        f' data-page-label="{cfg["label"]}"'
        f' data-page-i18n="{cfg["i18n"]}"'
        f'{nav_attr}>'
        '</script>'
    )

    original = content
    # Replace only the script tag attributes (keep the empty header tag intact)
    content = re.sub(
        r'<script defer src="/components/header\.js"[^>]*></script>',
        new_script,
        content
    )

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        nav_display = cfg['nav'] if cfg['nav'] else '(tampilkan semua)'
        print(f'FIXED: {filename}  ->  data-nav="{cfg["nav"]}" {nav_display}')
    else:
        print(f'NO CHANGE: {filename}')

print('\nDone.')
