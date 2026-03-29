"""
show_notfound_all_langs.py - Show notFoundDesc and notFoundBackHome values for all languages
"""
import re

content = open('web/public/assets/app.js', encoding='utf-8').read()

for key in ['notFoundDesc', 'notFoundBackHome']:
    print(f'\n=== {key} ===')
    idx = 0
    count = 0
    while True:
        pattern = key + ':"'
        idx = content.find(pattern, idx)
        if idx < 0:
            break
        end = content.find('"', idx + len(pattern))
        value = content[idx + len(pattern):end]
        print(f'  [{count+1}] {repr(value)}')
        idx = end
        count += 1
