"""
patch_applyLang.py
Adds notFound* keys to the applyLang() ID map in app.js so the
404 page elements get translated when the language is switched.
"""
import os

files_to_patch = [
    'web/src_backup/public__assets__app.js',
    'web/public/assets/app.js',
]

OLD = 'dlPyRun:"dlPyRun"'
NEW = ('dlPyRun:"dlPyRun"'
       ',notFoundTitle:"notFoundTitle"'
       ',notFoundSubtitle:"notFoundSubtitle"'
       ',notFoundDesc:"notFoundDesc"'
       ',notFoundBackHome:"notFoundBackHome"'
       ',footerCopyright404:"footerCopyright"')

for path in files_to_patch:
    if not os.path.exists(path):
        print(f'SKIP (not found): {path}')
        continue
    content = open(path, encoding='utf-8').read()
    if NEW.split(',')[1] in content:
        print(f'SKIP (already patched): {path}')
        continue
    if OLD not in content:
        print(f'ERROR (target not found in {path})')
        continue
    result = content.replace(OLD, NEW, 1)
    open(path, 'w', encoding='utf-8').write(result)
    print(f'PATCHED: {path}')

print('Done.')
