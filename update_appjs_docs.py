import re
import json

APP_JS_PATH = 'public/assets/app.js'

with open(APP_JS_PATH, 'r', encoding='utf-8') as f:
    app_js = f.read()

translations = {
    'en': {
        'docsTocLabel': 'On this page',
        'docsEditBtn': 'Edit on GitHub',
        'docsAutoFetchHtml': 'Auto-fetched from {file} on the <a href="https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token" target="_blank" rel="noopener">GitHub repository</a>.',
        'licenseErrorMsg': 'Failed to load License. Please check GitHub directly.',
        'licenseViewBtn': 'View on GitHub'
    },
    'pl': {
        'docsTocLabel': 'Na tej stronie',
        'docsEditBtn': 'Edytuj na GitHubie',
        'docsAutoFetchHtml': 'Automatycznie pobrane z pliku {file} w <a href="https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token" target="_blank" rel="noopener">repozytorium GitHub</a>.',
        'licenseErrorMsg': 'Nie udało się załadować licencji. Sprawdź bezpośrednio na GitHubie.',
        'licenseViewBtn': 'Zobacz na GitHubie'
    },
    'zh': {
        'docsTocLabel': '在这个页面上',
        'docsEditBtn': '在 GitHub 上编辑',
        'docsAutoFetchHtml': '从 <a href="https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token" target="_blank" rel="noopener">GitHub 存储库</a> 中的 {file} 自动获取。',
        'licenseErrorMsg': '无法加载许可证。请直接在 GitHub 上检查。',
        'licenseViewBtn': '在 GitHub 上查看'
    },
    'jp': {
        'docsTocLabel': 'このページの内容',
        'docsEditBtn': 'GitHubで編集する',
        'docsAutoFetchHtml': '<a href="https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token" target="_blank" rel="noopener">GitHub リポジトリ</a> の {file} から自動取得されました。',
        'licenseErrorMsg': 'ライセンスの読み込みに失敗しました。GitHubで直接確認してください。',
        'licenseViewBtn': 'GitHubで見る'
    },
    'de': {
        'docsTocLabel': 'Auf dieser Seite',
        'docsEditBtn': 'Auf GitHub bearbeiten',
        'docsAutoFetchHtml': 'Automatisch aus der {file} des <a href="https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token" target="_blank" rel="noopener">GitHub-Repositorys</a> geladen.',
        'licenseErrorMsg': 'Lizenz konnte nicht geladen werden. Bitte direkt auf GitHub überprüfen.',
        'licenseViewBtn': 'Auf GitHub ansehen'
    },
    'fr': {
        'docsTocLabel': 'Sur cette page',
        'docsEditBtn': 'Modifier sur GitHub',
        'docsAutoFetchHtml': 'Récupéré automatiquement depuis {file} sur le <a href="https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token" target="_blank" rel="noopener">dépôt GitHub</a>.',
        'licenseErrorMsg': 'Échec du chargement de la licence. Veuillez vérifier directement sur GitHub.',
        'licenseViewBtn': 'Voir sur GitHub'
    },
    'es': {
        'docsTocLabel': 'En esta página',
        'docsEditBtn': 'Editar en GitHub',
        'docsAutoFetchHtml': 'Obtenido automáticamente de {file} en el <a href="https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token" target="_blank" rel="noopener">repositorio de GitHub</a>.',
        'licenseErrorMsg': 'Error al cargar la licencia. Por favor, compruébelo directamente en GitHub.',
        'licenseViewBtn': 'Ver en GitHub'
    },
    'ru': {
        'docsTocLabel': 'На этой странице',
        'docsEditBtn': 'Редактировать на GitHub',
        'docsAutoFetchHtml': 'Автоматически загружено из {file} в <a href="https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token" target="_blank" rel="noopener">репозитории GitHub</a>.',
        'licenseErrorMsg': 'Не удалось загрузить лицензию. Пожалуйста, проверьте прямо на GitHub.',
        'licenseViewBtn': 'Посмотреть на GitHub'
    },
    'pt': {
        'docsTocLabel': 'Nesta página',
        'docsEditBtn': 'Editar no GitHub',
        'docsAutoFetchHtml': 'Obtido automaticamente de {file} no <a href="https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token" target="_blank" rel="noopener">repositório do GitHub</a>.',
        'licenseErrorMsg': 'Falha ao carregar a licença. Por favor, verifique diretamente no GitHub.',
        'licenseViewBtn': 'Ver no GitHub'
    },
    'id': {
        'docsTocLabel': 'Di halaman ini',
        'docsEditBtn': 'Edit di GitHub',
        'docsAutoFetchHtml': 'Diambil otomatis dari {file} pada <a href="https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token" target="_blank" rel="noopener">repositori GitHub</a>.',
        'licenseErrorMsg': 'Gagal memuat Lisensi. Silakan periksa langsung di GitHub.',
        'licenseViewBtn': 'Lihat di GitHub'
    },
    'kr': {
        'docsTocLabel': '이 페이지에서',
        'docsEditBtn': 'GitHub에서 편집하기',
        'docsAutoFetchHtml': '<a href="https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token" target="_blank" rel="noopener">GitHub 리포지토리</a>의 {file}에서 자동 가져옴.',
        'licenseErrorMsg': '라이선스를 로드하지 못했습니다. GitHub에서 직접 확인해 주세요.',
        'licenseViewBtn': 'GitHub에서 보기'
    }
}

for lang in translations:
    pattern = re.compile(rf'({lang}:\s*{{.*?)(notFoundBackPrev:\s*\".*?\",?\s*)(.*?}})', re.DOTALL)
    
    insert_str = ""
    for key, val in translations[lang].items():
        escaped_val = val.replace("\"", "\\\"")
        insert_str += f'{key}: "{escaped_val}",\n    '
    
    def rep_add(m):
        return m.group(1) + m.group(2) + "\n    " + insert_str + m.group(3)
    
    if pattern.search(app_js):
        app_js = pattern.sub(rep_add, app_js)
    else:
        print(f'Could not match insertion point for {lang}')

additions_dict = {
    "docsTocLabel": "docsTocLabel",
    "docsEditBtn": "docsEditBtn",
    "docsAutoFetchHtml": "docsAutoFetchHtml",
    "licenseErrorMsg": "licenseErrorMsg",
    "licenseViewBtn": "licenseViewBtn"
}

add_str = ""
for k, v in additions_dict.items():
    add_str += f'    {k}: "{v}",\n'

app_js = re.sub(r'(notFoundBackPrev:\s*"notFoundBackPrev",)', r'\1\n' + add_str, app_js)

with open(APP_JS_PATH, 'w', encoding='utf-8') as f:
    f.write(app_js)

print("SUCCESS")
