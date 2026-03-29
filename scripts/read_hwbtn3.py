import re

content = open('web/public/assets/app.js', encoding='utf-8').read()
idx = content.find('hwBtn')

# find the enclosing function by looking for an if/condition check
# Go back 2000 chars from hwBtn
start = max(0, idx - 2000)
chunk = content[start:idx+2000]

# Find key patterns
patterns = ['pathname', 'location', 'page-not', '404', 'disabled', 'exclude', 'skip',
            'hw-btn', 'hwBtn', 'body.append', 'document.body', 'initHelp', 'helpWidget']

for p in patterns:
    pi = chunk.find(p)
    if pi >= 0:
        print(f'[{p}] -> {repr(chunk[max(0,pi-30):pi+100])}')
        print()
