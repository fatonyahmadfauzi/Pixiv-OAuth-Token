content = open('web/public/assets/app.js', encoding='utf-8').read()

# Find the initHelpWidget or similar function call
# Look for body.insertAdjacentHTML or body.appendChild near hwHTML
for kw in ['insertAdjacentHTML', 'appendChild', 'body.innerHTML', 'document.body']:
    idx = 0
    while True:
        idx = content.find(kw, idx)
        if idx < 0: break
        ctx = content[max(0, idx-100):idx+300]
        if 'hwHTML' in ctx or 'hw-container' in ctx or 'hwContainer' in ctx:
            print(f'[{kw}] at {idx}:')
            print(ctx)
            print()
        idx += len(kw)
