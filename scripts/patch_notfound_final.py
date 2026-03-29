"""
patch_notfound_final.py
Replaces remaining incorrect zh values in kr block positions.
Uses notFoundTitle as sequence anchor to count all 22 blocks precisely.
"""
import os

FILES = [
    'web/src_backup/public__assets__app.js',
    'web/public/assets/app.js',
]

# Korean translations
KR_DESC     = '\uc9c0\uae08 \ucc3e\uc73c\uc2dc\ub294 \ud398\uc774\uc9c0\ub294 \uc874\uc7ac\ud558\uc9c0 \uc54a\uac70\ub098 \ub2e4\ub978 \uacf3\uc73c\ub85c \uc774\ub3d9\ub418\uc5c8\uc2b5\ub2c8\ub2e4.'
KR_BACK     = '\ud648\ud398\uc774\uc9c0\ub85c \ub3cc\uc544\uac00\uae30'

# The wrong zh values currently in kr positions
ZH_DESC     = '\u60a8\u8bbf\u95ee\u7684\u9875\u9762\u4e0d\u5b58\u5728\u6216\u5df2\u88ab\u79fb\u52a8\u5230\u5176\u4ed6\u4f4d\u7f6e\u3002'
ZH_BACK     = '\u8fd4\u56de\u9996\u9875'

def patch_file(path):
    content = open(path, encoding='utf-8').read()

    # Collect positions of ALL notFoundDesc and notFoundBackHome values (non-map)
    def get_positions(key):
        search = key + ':"'
        positions = []
        idx = 0
        while True:
            idx = content.find(search, idx)
            if idx < 0: break
            vs = idx + len(search)
            ve = content.find('"', vs)
            val = content[vs:ve]
            if val != key:  # skip the map entry
                positions.append((vs, ve, val))
            idx = ve
        return positions

    desc_pos = get_positions('notFoundDesc')
    back_pos = get_positions('notFoundBackHome')

    print(f'{path}: {len(desc_pos)} desc, {len(back_pos)} back')

    # Show current values for positions 19-22
    for label, positions in [('notFoundDesc', desc_pos), ('notFoundBackHome', back_pos)]:
        for i, (vs, ve, val) in enumerate(positions):
            if i >= 18:
                print(f'  [{i+1}] {label}: {repr(val[:40])}')

    # The 21st and 22nd positions (index 20,21) should be Korean
    # Currently they have Chinese values - replace them
    replacements = []
    if len(desc_pos) >= 22:
        for i in [20, 21]:
            vs, ve, val = desc_pos[i]
            if val == ZH_DESC:
                replacements.append((vs, ve, KR_DESC, f'notFoundDesc[{i+1}]->kr'))
            elif val != KR_DESC:
                print(f'  WARN: desc[{i+1}] has unexpected value: {repr(val[:40])}')

    if len(back_pos) >= 22:
        for i in [20, 21]:
            vs, ve, val = back_pos[i]
            if val == ZH_BACK:
                replacements.append((vs, ve, KR_BACK, f'notFoundBackHome[{i+1}]->kr'))
            elif val != KR_BACK:
                print(f'  WARN: back[{i+1}] has unexpected value: {repr(val[:40])}')

    # Apply in reverse
    replacements.sort(key=lambda x: x[0], reverse=True)
    for vs, ve, new_val, label in replacements:
        content = content[:vs] + new_val + content[ve:]
        print(f'  FIXED {label}')

    open(path, 'w', encoding='utf-8').write(content)
    print(f'  Done ({len(replacements)} changes)')

for f in FILES:
    if os.path.exists(f):
        patch_file(f)
    else:
        print(f'SKIP: {f}')

print('\nAll done.')
