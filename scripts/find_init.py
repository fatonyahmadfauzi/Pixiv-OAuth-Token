content = open('web/public/assets/app.js', encoding='utf-8').read()

# Find 'setupCli' and DOMContentLoaded to understand call chain
# Find the main init block
for kw in ['DOMContentLoaded', 'setupCli', '!function()', '!async function']:
    idx = 0
    while True:
        idx = content.find(kw, idx)
        if idx < 0: break
        ctx = content[idx:idx+300]
        print(f'{kw} at {idx}:')
        print(ctx[:200])
        print()
        idx += len(kw)
        if idx > 200000:
            break
