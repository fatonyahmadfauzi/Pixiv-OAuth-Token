content = open('web/public/assets/app.js', encoding='utf-8').read()

# Read 3000 chars before the document.body call at 172522
start = max(0, 172522 - 3000)
chunk = content[start:172522+200]
# Print in sections
sections = [chunk[i:i+300] for i in range(0, len(chunk), 300)]
for i, s in enumerate(sections):
    print(f'--- Section {i} (pos {start + i*300}) ---')
    print(s)
    print()
