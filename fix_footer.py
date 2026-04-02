with open('install.sh', 'r', encoding='utf-8') as f:
    content = f.read()

old = "echo -e \"  ${DIM}[i] Language '$RESOLVED_LANG' was auto-detected from your OS.${RESET}\"\necho -e \"  ${DIM}    To override: PIXIV_LANG=jp bash <(curl -sL ..../install.sh)${RESET}\""
new = "echo -e \"  ${DIM}[i] Language detected: $RESOLVED_LANG${RESET}\"\necho -e \"  ${DIM}    To use a different language: $PYTHON_CMD pixiv_login.py --lang jp${RESET}\"\necho -e \"  ${DIM}    To save permanently:         $PYTHON_CMD pixiv_login.py config set-lang jp${RESET}\""

if old in content:
    content = content.replace(old, new, 1)
    with open('install.sh', 'w', encoding='utf-8') as f:
        f.write(content)
    print('OK: footer updated')
else:
    # try to find the line
    idx = content.find("was auto-detected")
    print('MISS, context:', repr(content[idx-20:idx+80]) if idx >= 0 else 'not found')
