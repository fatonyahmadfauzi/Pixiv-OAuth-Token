content = open('web/public/assets/app.js', encoding='utf-8').read()

# Read the full block around the insertAdjacentHTML at 172536
idx = 172536
# Go way back to find the enclosing function/condition
chunk = content[max(0, idx-2000):idx+500]
print(chunk)
