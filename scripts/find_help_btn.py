content = open('web/src_backup/public__assets__app.js', encoding='utf-8').read()

# Search for help-related terms
keywords = ['helpBtn', 'help-btn', 'floatingHelp', 'helpFloat', 'helpWidget',
            'support-btn', 'supportBtn', 'help-bubble', 'helpBubble',
            'fab', 'floating', 'bubble', 'fixed.*bottom', 'position:fixed']

print('Searching for help button...')
for kw in keywords:
    idx = content.find(kw)
    if idx >= 0:
        print(f'\nFound: {kw} at {idx}')
        print(repr(content[max(0,idx-30):idx+200]))
