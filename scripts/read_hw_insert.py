content = open('web/public/assets/app.js', encoding='utf-8').read()

# Find where hwHTML is inserted into DOM (around 172567)
idx = 172567
chunk = content[max(0, idx-500):idx+800]
print(chunk)
