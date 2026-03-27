import re
import os

translations = {
    'en': {'download': 'DOWNLOAD', 'tutorial': 'TUTORIAL', 'changelog': 'CHANGELOG', 'web': 'WEB'},
    'id': {'download': 'UNDUH', 'tutorial': 'TUTORIAL', 'changelog': 'CHANGELOG', 'web': 'WEB'},
    'jp': {'download': 'ダウンロード', 'tutorial': 'チュートリアル', 'changelog': '変更履歴', 'web': 'ウェブ'},
    'zh': {'download': '下载', 'tutorial': '教程', 'changelog': '更新日志', 'web': '网页'},
    'kr': {'download': '다운로드', 'tutorial': '튜토리얼', 'changelog': '변경내역', 'web': '웹'},
    'es': {'download': 'DESCARGAR', 'tutorial': 'TUTORIAL', 'changelog': 'CAMBIOS', 'web': 'WEB'},
    'pt': {'download': 'BAIXAR', 'tutorial': 'TUTORIAL', 'changelog': 'CHANGELOG', 'web': 'WEB'},
    'fr': {'download': 'TÉLÉCHARGER', 'tutorial': 'TUTORIEL', 'changelog': 'CHANGELOG', 'web': 'WEB'},
    'de': {'download': 'HERUNTERLADEN', 'tutorial': 'TUTORIAL', 'changelog': 'CHANGELOG', 'web': 'WEB'},
    'ru': {'download': 'СКАЧАТЬ', 'tutorial': 'РУКОВОДСТВО', 'changelog': 'ИЗМЕНЕНИЯ', 'web': 'ВЕБ'},
    'pl': {'download': 'POBIERZ', 'tutorial': 'PORADNIK', 'changelog': 'ZMIANY', 'web': 'WEB'}
}

files = [
    r'c:\Users\faton\Downloads\Pixiv-OAuth-Token\web\public\assets\app.js',
    r'c:\Users\faton\Downloads\Pixiv-OAuth-Token\web\src_backup\public__assets__app.js'
]

for fp in files:
    if not os.path.exists(fp):
        continue
        
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We will search for EVERY language block and replace ALL "DOWNLOAD" instances within.
    for lang, trans in translations.items():
        # Match from `lang:{` up to `navHeaderWeb:"WEB"`
        # Because we already replaced SOME of them, the current text might be "DOWNLOAD" or the already-translated text.
        # But wait! The earlier script DID replace the first occurrence.
        # Let's just find `navHeaderDownload:"[ANYTHING]"` and replace it WITH the correct trans if we are in `lang:{...}`
        # The easiest way is to match `lang:{ ... }` by using a simple regex since we know there's no nested dictionaries for these values.
        
        # We will iterate and replace over the full string
        # Match `lang:{` up to `navHeaderLisensi` or `contactUsTitle`...
        
        # We'll regex substitute with a function that replaces globally inside this match
        pattern = r'(\b' + lang + r':\{.*?)(navHeaderDownload:)"[^"]+"(.*?navHeaderTutorial:)"[^"]+"(.*?navHeaderChangelog:)"[^"]+"(.*?navHeaderWeb:)"[^"]+"'
        
        def repl(m):
            return (
                m.group(1) + 
                m.group(2) + f'"{trans["download"]}"' + 
                m.group(3) + f'"{trans["tutorial"]}"' + 
                m.group(4) + f'"{trans["changelog"]}"' + 
                m.group(5) + f'"{trans["web"]}"'
            )
            
        content = re.sub(pattern, repl, content, count=0, flags=re.DOTALL)
        
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Fixed multiple translations in {fp}")
