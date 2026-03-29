content = open('web/public/assets/app.js', encoding='utf-8').read()

# The code is likely minified and uses arrow functions
# Let's find where document.body.insertAdjacentHTML is called with hwHTML
idx = content.find('document.body', 172000)
print(f'document.body at {idx}:')
print(repr(content[max(0,idx-200):idx+400]))
print()

# Also look at WHO calls this - find the function that contains this block
# by searching for the arrow function wrapping it
search = content[max(0, idx-500):idx]
print('Before insertion:')
print(search[-300:])
