import os
import re

pages_backup = {
    'public__contact.html':       {'i18n': 'navHeaderContact',   'label': 'CONTACT',     'nav': ''},
    'public__discussions.html':   {'i18n': 'navHeaderDiscuss',   'label': 'DISCUSSIONS', 'nav': ''},
    'public__documentation.html': {'i18n': 'navHeaderDocs',      'label': 'DOCS',        'nav': ''},
    'public__downloads.html':     {'i18n': 'navHeaderDownload',  'label': 'DOWNLOAD',    'nav': 'navDownloads'},
    'public__issues.html':        {'i18n': 'navHeaderIssues',    'label': 'ISSUES',      'nav': ''},
    'public__license.html':       {'i18n': 'navHeaderLicense',   'label': 'LICENSE',     'nav': ''},
    'public__support.html':       {'i18n': 'footerDonateLink',   'label': 'SUPPORT',     'nav': ''},
    'public__changelog.html':     {'i18n': 'navHeaderChangelog', 'label': 'CHANGELOG',   'nav': ''},
}

base = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src_backup'))

for filename, cfg in pages_backup.items():
    fpath = os.path.join(base, filename)
    if not os.path.exists(fpath):
        print(f'SKIP: {filename}')
        continue

    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    nav_attr = f' data-nav="{cfg["nav"]}"' if cfg['nav'] else ''
    new_script = (
        f'<script defer src="/components/header.js"'
        f' data-page-label="{cfg["label"]}"'
        f' data-page-i18n="{cfg["i18n"]}"'
        f'{nav_attr}>'
        '</script>'
    )

    original = content
    content = re.sub(
        r'<script defer src="/components/header\.js"[^>]*></script>',
        new_script,
        content
    )

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'FIXED: {filename}')
    else:
        print(f'NO CHANGE: {filename}')

print('\nDone.')
