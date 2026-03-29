content = open('web/public/assets/app.js', encoding='utf-8').read()

# Find initHelpWidget or the function that calls document.body.insertAdjacentHTML with hwHTML
# Search for the actual function name by looking for 'initH' or similar near position 172536
target = 172536

# Search for specific function that contains this code
search_start = max(0, target - 3000)
chunk = content[search_start:target+100]

# Find all function names in this chunk
import re
funcs = re.findall(r'function\s+(\w+)', chunk)
print('Functions in range:', funcs)
print()

# Also look for the call that triggers hw widget rendering
# Find 'initHelpWidget' or whatever calls document.body.insertAdjacentHTML
for name in ['initHelpWidget', 'initHwWidget', 'helpWidget', 'hwWidget', 'initContact', 'contactWidget']:
    idx = content.find(name)
    if idx >= 0:
        print(f'{name} at {idx}: {repr(content[max(0,idx-20):idx+150])}')
