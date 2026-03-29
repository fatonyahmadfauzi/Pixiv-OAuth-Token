"""
patch_notfound_translations.py
Adds proper localized translations for notFoundDesc and notFoundBackHome
into every language block in app.js.

The current state: all languages have English fallback text.
This script replaces them with proper translations for all 11 supported languages.
"""
import os

# Translations for each language
# Format: lang_key -> {notFoundDesc, notFoundBackHome}
TRANSLATIONS = {
    # English (already correct, but we normalize anyway)
    'en': {
        'notFoundDesc': 'The page you are looking for does not exist or has been moved.',
        'notFoundBackHome': 'Back to Homepage',
    },
    # Polish
    'pl': {
        'notFoundDesc': 'Strona, kt\u00f3rej szukasz, nie istnieje lub zosta\u0142a przeniesiona.',
        'notFoundBackHome': 'Powr\u00f3t do strony g\u0142\u00f3wnej',
    },
    # Chinese Simplified
    'zh': {
        'notFoundDesc': '\u60a8\u8bbf\u95ee\u7684\u9875\u9762\u4e0d\u5b58\u5728\u6216\u5df2\u88ab\u79fb\u52a8\u5230\u5176\u4ed6\u4f4d\u7f6e\u3002',
        'notFoundBackHome': '\u8fd4\u56de\u9996\u9875',
    },
    # Japanese
    'jp': {
        'notFoundDesc': '\u304a\u63a2\u3057\u306e\u30da\u30fc\u30b8\u306f\u5b58\u5728\u3057\u306a\u3044\u304b\u3001\u5225\u306e\u5834\u6240\u306b\u79fb\u52d5\u3055\u308c\u3066\u3044\u307e\u3059\u3002',
        'notFoundBackHome': '\u30db\u30fc\u30e0\u30da\u30fc\u30b8\u306b\u623b\u308b',
    },
    # German
    'de': {
        'notFoundDesc': 'Die gesuchte Seite existiert nicht oder wurde verschoben.',
        'notFoundBackHome': 'Zur\u00fcck zur Startseite',
    },
    # French
    'fr': {
        'notFoundDesc': 'La page que vous recherchez n\u2019existe pas ou a \u00e9t\u00e9 d\u00e9plac\u00e9e.',
        'notFoundBackHome': 'Retour \u00e0 l\u2019accueil',
    },
    # Spanish
    'es': {
        'notFoundDesc': 'La p\u00e1gina que buscas no existe o ha sido movida.',
        'notFoundBackHome': 'Volver al inicio',
    },
    # Russian
    'ru': {
        'notFoundDesc': '\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430, \u043a\u043e\u0442\u043e\u0440\u0443\u044e \u0432\u044b \u0438\u0449\u0435\u0442\u0435, \u043d\u0435 \u0441\u0443\u0449\u0435\u0441\u0442\u0432\u0443\u0435\u0442 \u0438\u043b\u0438 \u0431\u044b\u043b\u0430 \u043f\u0435\u0440\u0435\u043c\u0435\u0449\u0435\u043d\u0430.',
        'notFoundBackHome': '\u041d\u0430 \u0433\u043b\u0430\u0432\u043d\u0443\u044e',
    },
    # Portuguese
    'pt': {
        'notFoundDesc': 'A p\u00e1gina que voc\u00ea est\u00e1 procurando n\u00e3o existe ou foi movida.',
        'notFoundBackHome': 'Voltar \u00e0 p\u00e1gina inicial',
    },
    # Indonesian
    'id': {
        'notFoundDesc': 'Halaman yang Anda cari tidak ada atau telah dipindahkan.',
        'notFoundBackHome': 'Kembali ke Beranda',
    },
    # Korean
    'kr': {
        'notFoundDesc': '\uc9c0\uae08 \ucc3e\uc73c\uc2dc\ub294 \ud398\uc774\uc9c0\ub294 \uc874\uc7ac\ud558\uc9c0 \uc54a\uac70\ub098 \ub2e4\ub978 \uacf3\uc73c\ub85c \uc774\ub3d9\ub418\uc5c8\uc2b5\ub2c8\ub2e4.',
        'notFoundBackHome': '\ud648\ud398\uc774\uc9c0\ub85c \ub3cc\uc544\uac00\uae30',
    },
}

# English fallback text (what's currently in ALL language blocks)
EN_DESC     = 'The page you are looking for does not exist or has been moved.'
EN_BACKHOME = 'Back to Homepage'

FILES = [
    'web/src_backup/public__assets__app.js',
    'web/public/assets/app.js',
]

# We need to find each language-specific block in app.js and replace the values.
# The structure in app.js is a minified object per language like:
#   { ..., notFoundDesc:"The page...", notFoundBackHome:"Back to Homepage", ... }
# repeating for each language in order: en, pl, zh, jp, de, fr, es, ru, pt, id, kr
# (order may vary, but all occurrences of notFoundDesc with EN value need replacement)

def patch_file(path):
    if not os.path.exists(path):
        print(f'SKIP (not found): {path}')
        return

    content = open(path, encoding='utf-8').read()

    # Collect positions of all notFoundDesc occurrences
    desc_key = 'notFoundDesc:"'
    back_key = 'notFoundBackHome:"'

    # Find all occurrences and their language order
    # Strategy: find all occurrences of notFoundSubtitle (which is already translated correctly)
    # and use those positions to determine which language block we're in,
    # then replace notFoundDesc and notFoundBackHome in the same block.

    # Simpler approach: replace each occurrence in order (en=1st, pl=2nd, ... kr=11th)
    lang_order = ['en', 'pl', 'zh', 'jp', 'de', 'fr', 'es', 'ru', 'pt', 'id', 'kr']

    # Count current occurrences
    desc_positions = []
    idx = 0
    while True:
        idx = content.find(desc_key, idx)
        if idx < 0: break
        # Skip the applyLang map entry (value is "notFoundDesc" not the EN text)
        end = content.find('"', idx + len(desc_key))
        val = content[idx + len(desc_key):end]
        if val not in ('notFoundDesc',):  # skip the map entries
            desc_positions.append((idx, end, val))
        idx = end

    back_positions = []
    idx = 0
    while True:
        idx = content.find(back_key, idx)
        if idx < 0: break
        end = content.find('"', idx + len(back_key))
        val = content[idx + len(back_key):end]
        if val not in ('notFoundBackHome',):
            back_positions.append((idx, end, val))
        idx = end

    print(f'\n{path}')
    print(f'  notFoundDesc occurrences (non-map): {len(desc_positions)}')
    print(f'  notFoundBackHome occurrences (non-map): {len(back_positions)}')

    if len(desc_positions) != len(lang_order):
        print(f'  WARNING: expected {len(lang_order)} desc occurrences, got {len(desc_positions)}')
        # Try to proceed anyway with available positions
    if len(back_positions) != len(lang_order):
        print(f'  WARNING: expected {len(lang_order)} back occurrences, got {len(back_positions)}')

    # Build replacement: work backwards so indices stay valid
    replacements = []

    for i, (start, end, old_val) in enumerate(desc_positions):
        lang = lang_order[i] if i < len(lang_order) else 'en'
        new_val = TRANSLATIONS[lang]['notFoundDesc']
        replacements.append((start + len(desc_key), end, old_val, new_val, f'notFoundDesc[{lang}]'))

    for i, (start, end, old_val) in enumerate(back_positions):
        lang = lang_order[i] if i < len(lang_order) else 'en'
        new_val = TRANSLATIONS[lang]['notFoundBackHome']
        replacements.append((start + len(back_key), end, old_val, new_val, f'notFoundBackHome[{lang}]'))

    # Sort by position descending (replace from end)
    replacements.sort(key=lambda x: x[0], reverse=True)

    changed = 0
    for val_start, val_end, old_val, new_val, label in replacements:
        if content[val_start:val_end] == old_val:
            if old_val != new_val:
                content = content[:val_start] + new_val + content[val_end:]
                changed += 1
                print(f'  REPLACED {label}: {repr(old_val[:30])} -> {repr(new_val[:30])}')
            # else: EN is already correct
        else:
            print(f'  MISMATCH {label}: expected {repr(old_val[:30])}, got {repr(content[val_start:val_end][:30])}')

    open(path, 'w', encoding='utf-8').write(content)
    print(f'  Total changes: {changed}')

for f in FILES:
    patch_file(f)

print('\nDone.')
