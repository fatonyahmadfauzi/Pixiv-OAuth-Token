"""
patch_notfound_v2.py - Patch ALL occurrences with proper translations
Handles duplicate language blocks (e.g., JP appearing twice for different pages)
"""
import os, re

TRANSLATIONS = {
    'en': {
        'notFoundDesc': 'The page you are looking for does not exist or has been moved.',
        'notFoundBackHome': 'Back to Homepage',
    },
    'pl': {
        'notFoundDesc': 'Strona, kt\u00f3rej szukasz, nie istnieje lub zosta\u0142a przeniesiona.',
        'notFoundBackHome': 'Powr\u00f3t do strony g\u0142\u00f3wnej',
    },
    'zh': {
        'notFoundDesc': '\u60a8\u8bbf\u95ee\u7684\u9875\u9762\u4e0d\u5b58\u5728\u6216\u5df2\u88ab\u79fb\u52a8\u5230\u5176\u4ed6\u4f4d\u7f6e\u3002',
        'notFoundBackHome': '\u8fd4\u56de\u9996\u9875',
    },
    'jp': {
        'notFoundDesc': '\u304a\u63a2\u3057\u306e\u30da\u30fc\u30b8\u306f\u5b58\u5728\u3057\u306a\u3044\u304b\u3001\u5225\u306e\u5834\u6240\u306b\u79fb\u52d5\u3055\u308c\u3066\u3044\u307e\u3059\u3002',
        'notFoundBackHome': '\u30db\u30fc\u30e0\u30da\u30fc\u30b8\u306b\u623b\u308b',
    },
    'de': {
        'notFoundDesc': 'Die gesuchte Seite existiert nicht oder wurde verschoben.',
        'notFoundBackHome': 'Zur\u00fcck zur Startseite',
    },
    'fr': {
        'notFoundDesc': 'La page que vous recherchez n\u2019existe pas ou a \u00e9t\u00e9 d\u00e9plac\u00e9e.',
        'notFoundBackHome': 'Retour \u00e0 l\u2019accueil',
    },
    'es': {
        'notFoundDesc': 'La p\u00e1gina que buscas no existe o ha sido movida.',
        'notFoundBackHome': 'Volver al inicio',
    },
    'ru': {
        'notFoundDesc': '\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430, \u043a\u043e\u0442\u043e\u0440\u0443\u044e \u0432\u044b \u0438\u0449\u0435\u0442\u0435, \u043d\u0435 \u0441\u0443\u0449\u0435\u0441\u0442\u0432\u0443\u0435\u0442 \u0438\u043b\u0438 \u0431\u044b\u043b\u0430 \u043f\u0435\u0440\u0435\u043c\u0435\u0449\u0435\u043d\u0430.',
        'notFoundBackHome': '\u041d\u0430 \u0433\u043b\u0430\u0432\u043d\u0443\u044e',
    },
    'pt': {
        'notFoundDesc': 'A p\u00e1gina que voc\u00ea est\u00e1 procurando n\u00e3o existe ou foi movida.',
        'notFoundBackHome': 'Voltar \u00e0 p\u00e1gina inicial',
    },
    'id': {
        'notFoundDesc': 'Halaman yang Anda cari tidak ada atau telah dipindahkan.',
        'notFoundBackHome': 'Kembali ke Beranda',
    },
    'kr': {
        'notFoundDesc': '\uc9c0\uae08 \ucc3e\uc73c\uc2dc\ub294 \ud398\uc774\uc9c0\ub294 \uc874\uc7ac\ud558\uc9c0 \uc54a\uac70\ub098 \ub2e4\ub978 \uacf3\uc73c\ub85c \uc774\ub3d9\ub418\uc5c8\uc2b5\ub2c8\ub2e4.',
        'notFoundBackHome': '\ud648\ud398\uc774\uc9c0\ub85c \ub3cc\uc544\uac00\uae30',
    },
}

# English text to skip (already correct) and map as EN
EN_DESC     = 'The page you are looking for does not exist or has been moved.'
EN_BACKHOME = 'Back to Homepage'

# Deduce lang order by finding notFoundSubtitle which is already correctly translated
# This tells us the actual order of language blocks
SUBTITLE_TO_LANG = {
    'Page Not Found':               'en',
    'Nie znaleziono strony':        'pl',
    '\u9875\u9762\u672a\u627e\u5230': 'zh',
    '\u30da\u30fc\u30b8\u304c\u898b\u3064\u304b\u308a\u307e\u305b\u3093': 'jp',
    'Seite nicht gefunden':         'de',
    'Page introuvable':             'fr',
    'P\u00e1gina no encontrada':    'es',
    '\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430 \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u0430': 'ru',
    'P\u00e1gina n\u00e3o encontrada': 'pt',
    'Halaman Tidak Ditemukan':      'id',
    '\ud398\uc774\uc9c0\ub97c \ucc3e\uc744 \uc218 \uc5c6\uc2b5\ub2c8\ub2e4': 'kr',
}

def patch_file(path):
    if not os.path.exists(path):
        print(f'SKIP: {path}')
        return

    content = open(path, encoding='utf-8').read()

    # Determine language order from notFoundSubtitle values
    sub_key = 'notFoundSubtitle:"'
    lang_order = []
    idx = 0
    while True:
        idx = content.find(sub_key, idx)
        if idx < 0: break
        end = content.find('"', idx + len(sub_key))
        val = content[idx + len(sub_key):end]
        lang = SUBTITLE_TO_LANG.get(val)
        if lang:
            lang_order.append(lang)
        idx = end

    print(f'\n{path}')
    print(f'  Detected language order ({len(lang_order)}): {lang_order}')

    # Now replace notFoundDesc and notFoundBackHome for each position
    for key_name, en_val in [('notFoundDesc', EN_DESC), ('notFoundBackHome', EN_BACKHOME)]:
        search_key = key_name + ':"'
        positions = []
        idx = 0
        while True:
            idx = content.find(search_key, idx)
            if idx < 0: break
            end = content.find('"', idx + len(search_key))
            val = content[idx + len(search_key):end]
            if val not in (key_name,):  # skip map entries
                positions.append((idx + len(search_key), end, val))
            idx = end

        # Sort descending to replace from end without shifting
        positions.sort(key=lambda x: x[0], reverse=True)

        # Map positions to languages
        # We have len(lang_order) translation blocks, possibly repeated twice
        # Positions are in forward order; we need to reverse for replacement
        # First pass get forward order
        fwd_positions = sorted(positions, key=lambda x: x[0])

        total = len(fwd_positions)
        block_size = len(lang_order)
        changed = 0

        for i, (val_start, val_end, old_val) in enumerate(fwd_positions):
            lang_idx = i % block_size
            if lang_idx < len(lang_order):
                lang = lang_order[lang_idx]
                new_val = TRANSLATIONS[lang][key_name]
            else:
                new_val = old_val  # keep as is

            if old_val != new_val:
                # Mark for replacement
                fwd_positions[i] = (val_start, val_end, old_val, new_val)
                changed += 1
            else:
                fwd_positions[i] = (val_start, val_end, old_val, old_val)

        # Apply replacements from end to not shift
        for item in sorted(fwd_positions, key=lambda x: x[0], reverse=True):
            val_start, val_end, old_val, new_val = item
            if old_val != new_val:
                content = content[:val_start] + new_val + content[val_end:]

        print(f'  {key_name}: {changed}/{total} blocks updated')

    open(path, 'w', encoding='utf-8').write(content)
    print(f'  Saved.')

FILES = [
    'web/src_backup/public__assets__app.js',
    'web/public/assets/app.js',
]

for f in FILES:
    patch_file(f)

print('\nDone.')
