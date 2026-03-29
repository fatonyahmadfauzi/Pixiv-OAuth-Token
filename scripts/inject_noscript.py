"""
inject_noscript.py
Replaces <noscript> banners with a <meta refresh> redirect to /enable-javascript
in all public HTML pages (src_backup + public/).
Run from project root: python scripts/inject_noscript.py
"""

import os
import re
import glob

# Redirect to dedicated page — works without JS (meta refresh is HTML)
NOSCRIPT_REDIRECT = """\
  <noscript>
    <meta http-equiv="refresh" content="0; url=/enable-javascript">
  </noscript>"""

BODY_TAG_PATTERN = re.compile(r'(<body[^>]*>)', re.IGNORECASE)
OLD_NOSCRIPT_PATTERN = re.compile(
    r'\s*<noscript>.*?</noscript>',
    re.DOTALL | re.IGNORECASE
)

def process(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()

    # Remove any existing noscript block first
    new_content = OLD_NOSCRIPT_PATTERN.sub('', content)

    # Skip the enable-javascript page itself — no redirect there!
    if 'enable-javascript' in path.replace('\\', '/'):
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return 'cleaned'
        return 'skip'

    # Inject redirect noscript right after <body>
    result = BODY_TAG_PATTERN.sub(r'\1\n' + NOSCRIPT_REDIRECT, new_content, count=1)
    if result == new_content:
        return 'no-body'

    with open(path, 'w', encoding='utf-8') as f:
        f.write(result)
    return 'ok'

def main():
    src_files = sorted(glob.glob('web/src_backup/public__*.html'))
    pub_files = sorted(glob.glob('web/public/*.html'))
    all_files = src_files + pub_files

    results = {'ok': [], 'skip': [], 'no-body': [], 'cleaned': []}
    for path in all_files:
        r = process(path)
        results[r].append(path)

    print(f"\nUpdated with redirect ({len(results['ok'])}):")
    for p in results['ok']:
        print(f"  + {p}")

    if results['cleaned']:
        print(f"\nCleaned (enable-javascript page) ({len(results['cleaned'])}):")
        for p in results['cleaned']:
            print(f"  ~ {p}")

    if results['skip']:
        print(f"\nSkipped ({len(results['skip'])}):")
        for p in results['skip']:
            print(f"  - {p}")

    if results['no-body']:
        print(f"\nWarning — no <body> tag ({len(results['no-body'])}):")
        for p in results['no-body']:
            print(f"  ? {p}")

    print("\nDone.")

if __name__ == '__main__':
    main()
