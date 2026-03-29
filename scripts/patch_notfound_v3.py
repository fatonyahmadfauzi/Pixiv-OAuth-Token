"""
patch_notfound_v3.py
Uses notFoundSubtitle as anchor to find language blocks,
then replaces notFoundDesc and notFoundBackHome within each block.
"""
import os

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

SUBTITLE_TO_LANG = {
    'Page Not Found':                   'en',
    'Nie znaleziono strony':            'pl',
    '\u9875\u9762\u672a\u627e\u5230':   'zh',
    '\u30da\u30fc\u30b8\u304c\u898b\u3064\u304b\u308a\u307e\u305b\u3093': 'jp',
    'Seite nicht gefunden':             'de',
    'Page introuvable':                 'fr',
    'P\u00e1gina no encontrada':        'es',
    '\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430 \u043d\u0435 \u043d\u0430\u0439\u0434\u0435\u043d\u0430': 'ru',
    'P\u00e1gina n\u00e3o encontrada':  'pt',
    'Halaman Tidak Ditemukan':          'id',
    '\ud398\uc774\uc9c0\ub97c \ucc3e\uc744 \uc218 \uc5c6\uc2b5\ub2c8\ub2e4': 'kr',
}

def patch_file(path):
    if not os.path.exists(path):
        print(f'SKIP: {path}')
        return

    content = open(path, encoding='utf-8').read()

    # Find all notFoundSubtitle positions and their language
    sub_anchors = []  # [(position_after_value, lang)]
    idx = 0
    while True:
        idx = content.find('notFoundSubtitle:"', idx)
        if idx < 0: break
        end = content.find('"', idx + len('notFoundSubtitle:"'))
        val = content[idx + len('notFoundSubtitle:"'):end]
        lang = SUBTITLE_TO_LANG.get(val)
        if lang:
            sub_anchors.append((end, lang))
        idx = end

    print(f'\n{path}')
    print(f'  Found {len(sub_anchors)} language blocks')

    changes = []

    for i, (anchor_pos, lang) in enumerate(sub_anchors):
        # Next anchor or end of file
        next_anchor = sub_anchors[i+1][0] if i+1 < len(sub_anchors) else len(content)

        # Within [anchor_pos, next_anchor], replace notFoundDesc and notFoundBackHome
        block = content[anchor_pos:next_anchor]

        for key_name in ('notFoundDesc', 'notFoundBackHome'):
            search = key_name + ':"'
            ki = block.find(search)
            if ki < 0:
                continue
            val_start = ki + len(search)
            val_end = block.find('"', val_start)
            old_val = block[val_start:val_end]

            if old_val in (key_name,):
                continue  # skip map entries

            new_val = TRANSLATIONS[lang][key_name]
            if old_val != new_val:
                # Compute absolute positions
                abs_start = anchor_pos + val_start
                abs_end   = anchor_pos + val_end
                changes.append((abs_start, abs_end, old_val, new_val, lang, key_name))

    # Apply in reverse order
    changes.sort(key=lambda x: x[0], reverse=True)
    for abs_start, abs_end, old_val, new_val, lang, key_name in changes:
        content = content[:abs_start] + new_val + content[abs_end:]
        print(f'  [{lang}] {key_name}: {repr(old_val[:25])} -> {repr(new_val[:25])}')

    open(path, 'w', encoding='utf-8').write(content)
    print(f'  Total changes: {len(changes)}')

FILES = [
    'web/src_backup/public__assets__app.js',
    'web/public/assets/app.js',
]

for f in FILES:
    patch_file(f)

print('\nAll done.')
