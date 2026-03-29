content = open('web/public/assets/app.js', encoding='utf-8').read()

# Find the function that initializes the hw widget
# Look backwards from 172536 to find the function definition
idx = 172536
# Find the last 'function' keyword before this point
func_search = content[:idx]
func_idx = func_search.rfind('function ')
print(f'Last function def before hw insert: at {func_idx}')
print('Context:')
print(content[func_idx:func_idx+300])
print()

# Also find the DOMContentLoaded or init call that triggers this
dcl = content[:idx].rfind('DOMContentLoaded')
if dcl >= 0:
    print(f'DOMContentLoaded at {dcl}')
    print(content[dcl:dcl+200])
