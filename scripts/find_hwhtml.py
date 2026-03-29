content = open('web/public/assets/app.js', encoding='utf-8').read()

# Find hw-container and look for the init condition
idx_hw = content.find('hw-container')
print('hw-container at:', idx_hw)
print()

# Find what wraps hwHTML and when it's appended to DOM
# Search for hwHTML creation and the function that calls it
idx_hwhtml = content.find('hwHTML')
print('hwHTML defined at:', idx_hwhtml)
# Get bigger context
chunk = content[max(0, idx_hwhtml-200):idx_hwhtml+500]
print(chunk)
print()

# Find where hwHTML is appended
idx_append = content.find('hwHTML', idx_hwhtml+1)
while idx_append >= 0:
    ctx = content[max(0, idx_append-100):idx_append+200]
    print(f'hwHTML usage at {idx_append}:')
    print(ctx[:200])
    print()
    idx_append = content.find('hwHTML', idx_append+1)
    if idx_append > idx_hwhtml + 5000:
        break
