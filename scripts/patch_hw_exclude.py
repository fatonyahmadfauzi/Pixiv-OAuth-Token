"""
patch_hw_exclude.py
Adds a pathname check so the hw-widget is NOT rendered on:
  - /404  (or any URL that contains '404')
  - /enable-javascript

Strategy: wrap the document.body.insertAdjacentHTML(hwHTML) call with an
if (!EXCLUDED_PATHS.includes(window.location.pathname)) { ... } guard.
"""
import os, re

# Pages where hw-widget should NOT appear
EXCLUDE_CHECK = (
    "window.location.pathname==='/404'"
    "||window.location.pathname==='/enable-javascript'"
    "||document.body.classList.contains('page-not-found')"
)

FILES = [
    'web/src_backup/public__assets__app.js',
    'web/public/assets/app.js',
]

# The exact string that inserts hwHTML into the body
TARGET = 'document.body.insertAdjacentHTML("beforeend",hwHTML)'
REPLACEMENT = f'if(!({EXCLUDE_CHECK})){{document.body.insertAdjacentHTML("beforeend",hwHTML)}}'

for path in FILES:
    if not os.path.exists(path):
        print(f'SKIP: {path}')
        continue
    content = open(path, encoding='utf-8').read()
    if TARGET not in content:
        print(f'ERROR: target not found in {path}')
        continue
    if REPLACEMENT in content:
        print(f'SKIP (already patched): {path}')
        continue
    result = content.replace(TARGET, REPLACEMENT, 1)
    open(path, 'w', encoding='utf-8').write(result)
    print(f'PATCHED: {path}')

print('Done.')
