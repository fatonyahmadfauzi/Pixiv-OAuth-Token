content = open('web/public/assets/app.js', encoding='utf-8').read()
idx = content.find('hwBtn')

# Find the function/block that creates hwBtn
# Go back to find the start of this block
start = max(0, idx - 800)
chunk = content[start:idx+1200]
print(chunk)
