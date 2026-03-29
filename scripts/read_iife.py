content = open('web/public/assets/app.js', encoding='utf-8').read()

# Read the !async function at 169527 onwards - this is the main IIFE
idx = 169527
chunk = content[idx:idx+3500]
print(chunk)
