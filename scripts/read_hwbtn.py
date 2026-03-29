content = open('web/public/assets/app.js', encoding='utf-8').read()
idx = content.find('hwBtn')
# Print in chunks to avoid truncation
chunk = content[max(0, idx-600):idx+1000]
# Print 200 chars at a time
for i in range(0, len(chunk), 200):
    print(repr(chunk[i:i+200]))
    print()
