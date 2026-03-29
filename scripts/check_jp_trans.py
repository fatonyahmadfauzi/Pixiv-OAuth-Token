"""
check_jp_translations.py
Check the JP translation values for notFound* keys in app.js
"""
content = open('web/public/assets/app.js', encoding='utf-8').read()

keys_to_check = ['notFoundSubtitle', 'notFoundDesc', 'notFoundBackHome']

for key in keys_to_check:
    idx = 0
    print(f'\n--- {key} occurrences ---')
    while True:
        idx = content.find(key + ':', idx)
        if idx < 0:
            break
        chunk = content[idx:idx+120]
        print(repr(chunk[:100]))
        idx += 1
