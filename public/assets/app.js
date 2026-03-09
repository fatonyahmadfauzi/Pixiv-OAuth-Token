const CLIENT_ID = "MOBrBDS8blbauoSck0ZfDbtuzpyT";
const REDIRECT_URI = "https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback";
const LOGIN_URL = "https://app-api.pixiv.net/web/v1/login";
const REPO_BASE = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token";
const RELEASE_BASE = `${REPO_BASE}/releases/latest/download`;
const RELEASE_API = "https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest";
const DOWNLOADS_BASE = `${REPO_BASE}/raw/HEAD/downloads`;

let codeVerifier = "";
let tokenState = { access_token: "", refresh_token: "" };

const q = (id) => document.getElementById(id);
const output = q("output");

// ---------------------- DISPLAY LANGUAGE SETTINGS ----------------------

const LANG_ORDER = ["en", "pl", "zh", "jp", "de", "fr", "es", "ru", "pt", "id", "kr"];

const DISPLAY_LANGUAGES = {
  en: {
    kicker: "Pixiv OAuth Toolkit",
    title: "Pixiv OAuth Web",
    subtitle: "Toolkit to generate Pixiv OAuth tokens via CLI, GUI, and Web with secure PKCE flow and Vercel-ready deployment.",
    badgePkce: "PKCE Flow",
    badgeDeploy: "Vercel Ready",
    badgeRelease: "Release Download",
    overviewTitle: "Project Overview",
    overviewDesc: "This project helps exchange/refresh Pixiv OAuth tokens and ships Windows build scripts for Portable/Setup artifacts.",
    docs: "Read the docs",
    modesTitle: "Available Modes",
    modeCli: "CLI: pixiv_login.py",
    modeGui: "GUI: pixiv_login_gui.py",
    modeWeb: "Web: static UI + serverless /api/token",
    requirementsTitle: "Requirements",
    reqPy: "Python 3.11+",
    reqDeps: "Dependencies: requests, pyinstaller",
    reqBuild: "Windows build toolchain for setup installer",
    oauthTitle: "OAuth Token Console",
    lang: "Language",
    open: "1) Open Login Page",
    placeholder: "2) Paste pixiv:// callback URL or code here",
    exchange: "Exchange Token",
    refresh: "Refresh Token",
    result: "Result",
    copyAccess: "Copy access_token",
    copyRefresh: "Copy refresh_token",
    ready: "Ready.",
    opened: "Login page opened. After login, paste pixiv:// callback URL or code.",
    codeEmpty: "Code is empty.",
    clickOpen: "Click 'Open Login Page' first.",
    noRefresh: "No refresh_token available.",
    copiedAccess: "access_token copied.",
    copiedRefresh: "refresh_token copied.",
    nothingAccess: "No access_token available.",
    nothingRefresh: "No refresh_token available.",
    resource: "Resources",
    contact: "Contact",
    dev: "Developer",
    downloadsTitle: "Downloads",
    downloadsDesc: "Download latest build directly from GitHub Releases.",
    quickCmdTitle: "Quick Command",
    quickCmdDesc: "Copy command for PowerShell/CMD download and pip install.",
    copyPs: "Copy PowerShell",
    copyCmd: "Copy CMD",
    copyPip: "Copy pip command",
    navHomepage: "Homepage",
    navConsole: "Console",
    navDownloads: "Downloads",
    navQuickCmd: "Quick Cmd",
    navTutorial: "Tutorial",
    tutorialTitle: "Tutorial",
    tutorialDesc: "Fill this section with ordered screenshots to guide users from login to token exchange.",
    tutorialTabStart: "Get Started",
    tutorialTabSteps: "Tutorial Steps",
    tutorialTabTips: "Tips",
    tutorialPageTitle: "Get Started with Pixiv OAuth Tutorial",
    tutorialPageDesc: "Follow each step from login to token exchange so the process is easier on desktop and mobile.",
    tutorialStepsTitle: "Tutorial Steps",
    tutorialBackBtn: "Back to OAuth Console",
    needVisualGuide: "Need visual step-by-step guide?",
    openTutorialPage: "Open Tutorial Page",
    windowsPreviewBadge: "Windows App Preview",
    windowsPreviewTitle: "See Pixiv OAuth Windows App in Action",
    windowsPreviewDesc: "This short preview shows the Windows app flow from login to successful token generation.",
    cliPreviewBadge: "CLI Preview",
    cliPreviewTitle: "Preview Pixiv OAuth CLI Output",
    cliPreviewDesc: "CLI output simulation to show login flow, code parsing, and token result in a concise way.",
    openDownloadsPage: "Open Downloads Page",
    errApiNotFound: "API endpoint not found (404). Deploy /api/token on Vercel first.",
    errApiHtml: "Server returned HTML instead of JSON. Check deployment routes/config.",
    copiedPs: "PowerShell command copied.",
    copiedCmd: "CMD command copied.",
    copiedPip: "pip command copied.",
    showMore: "See More",
    showLess: "Show Less"
  },
  pl: {
    kicker: "Zestaw narzędzi Pixiv OAuth",
    title: "Sieć Pixiv OAuth",
    subtitle: "Zestaw narzędzi do generowania tokenów Pixiv OAuth przez CLI, GUI i WWW z bezpiecznym przepływem PKCE oraz wdrożeniem gotowym dla Vercel.",
    badgePkce: "Przepływ PKCE",
    badgeDeploy: "Gotowe dla Vercel",
    badgeRelease: "Pobierz wydanie",
    overviewTitle: "Przegląd projektu",
    overviewDesc: "Projekt pomaga wymieniać i odświeżać tokeny Pixiv OAuth oraz zawiera skrypty budowania Windows dla wersji Portable/Setup.",
    docs: "Czytaj dokumentację",
    modesTitle: "Dostępne tryby",
    modeCli: "CLI: pixiv_login.py",
    modeGui: "GUI: pixiv_login_gui.py",
    modeWeb: "Web: statyczny interfejs + serverless /api/token",
    requirementsTitle: "Wymagania",
    reqPy: "Python 3.11+",
    reqDeps: "Zależności: requests, pyinstaller",
    reqBuild: "Narzędzia budowania Windows dla instalatora setup",
    oauthTitle: "Konsola tokenów OAuth",
    lang: "Język",
    open: "1) Otwórz stronę logowania",
    placeholder: "2) Wklej URL zwrotny pixiv:// lub kod tutaj",
    exchange: "Wymień token",
    refresh: "Odśwież token",
    result: "Wynik",
    copyAccess: "Kopiuj access_token",
    copyRefresh: "Kopiuj refresh_token",
    ready: "Gotowe.",
    opened: "Strona logowania została otwarta. Po zalogowaniu wklej URL zwrotny pixiv:// lub kod.",
    codeEmpty: "Kod jest pusty.",
    clickOpen: "Najpierw kliknij „Otwórz stronę logowania”.",
    noRefresh: "Brak dostępnego refresh_token.",
    copiedAccess: "Skopiowano access_token.",
    copiedRefresh: "Skopiowano refresh_token.",
    nothingAccess: "Brak dostępnego access_token.",
    nothingRefresh: "Brak dostępnego refresh_token.",
    resource: "Zasoby",
    contact: "Kontakt",
    dev: "Deweloper",
    downloadsTitle: "Pobieranie",
    downloadsDesc: "Pobierz najnowszą wersję bezpośrednio z GitHub Releases.",
    quickCmdTitle: "Szybka komenda",
    quickCmdDesc: "Skopiuj polecenie pobierania PowerShell/CMD oraz instalacji pip.",
    copyPs: "Kopiuj PowerShell",
    copyCmd: "Kopiuj CMD",
    copyPip: "Kopiuj polecenie pip",
    navHomepage: "Strona główna",
    navConsole: "Konsola",
    navDownloads: "Pobieranie",
    navQuickCmd: "Szybka komenda",
    navTutorial: "Tutorial",
    tutorialTitle: "Tutorial",
    tutorialDesc: "Wypełnij tę sekcję uporządkowanymi zrzutami ekranu, aby poprowadzić użytkowników od logowania do wymiany tokenu.",
    errApiNotFound: "Nie znaleziono endpointu API (404). Najpierw wdroż /api/token na Vercel.",
    errApiHtml: "Serwer zwrócił HTML zamiast JSON. Sprawdź trasy wdrożenia/konfigurację.",
    copiedPs: "Polecenie PowerShell skopiowane.",
    copiedCmd: "Polecenie CMD skopiowane.",
    copiedPip: "Polecenie pip skopiowane.",
    showMore: "Pokaż więcej",
    showLess: "Pokaż mniej"
  },
  zh: {
    kicker: "Pixiv OAuth 工具包",
    title: "Pixiv OAuth 网页",
    subtitle: "通过 CLI、GUI 和 Web 生成 Pixiv OAuth 令牌的工具包，采用安全 PKCE 流程，并可直接部署到 Vercel。",
    badgePkce: "PKCE 流程",
    badgeDeploy: "Vercel 就绪",
    badgeRelease: "发布下载",
    overviewTitle: "项目概览",
    overviewDesc: "该项目可帮助交换/刷新 Pixiv OAuth 令牌，并提供 Windows Portable/Setup 构建脚本。",
    docs: "阅读文档",
    modesTitle: "可用模式",
    modeCli: "CLI: pixiv_login.py",
    modeGui: "GUI: pixiv_login_gui.py",
    modeWeb: "Web: 静态 UI + 无服务器 /api/token",
    requirementsTitle: "环境要求",
    reqPy: "Python 3.11+",
    reqDeps: "依赖：requests, pyinstaller",
    reqBuild: "用于 setup 安装程序的 Windows 构建工具链",
    oauthTitle: "OAuth 令牌控制台",
    lang: "语言",
    open: "1) 打开登录页面",
    placeholder: "2) 在此粘贴 pixiv:// 回调 URL 或代码",
    exchange: "交换令牌",
    refresh: "刷新令牌",
    result: "结果",
    copyAccess: "复制 access_token",
    copyRefresh: "复制 refresh_token",
    ready: "就绪。",
    opened: "登录页面已打开。登录后，请粘贴 pixiv:// 回调 URL 或代码。",
    codeEmpty: "代码为空。",
    clickOpen: "请先点击“打开登录页面”。",
    noRefresh: "没有可用的 refresh_token。",
    copiedAccess: "access_token 已复制。",
    copiedRefresh: "refresh_token 已复制。",
    nothingAccess: "没有可用的 access_token。",
    nothingRefresh: "没有可用的 refresh_token。",
    resource: "资源",
    contact: "联系",
    dev: "开发者",
    downloadsTitle: "下载",
    downloadsDesc: "直接从 GitHub Releases 下载最新版本。",
    quickCmdTitle: "快速命令",
    quickCmdDesc: "复制 PowerShell/CMD 下载命令和 pip 安装命令。",
    copyPs: "复制 PowerShell",
    copyCmd: "复制 CMD",
    copyPip: "复制 pip 命令",
    navHomepage: "首页",
    navConsole: "控制台",
    navDownloads: "下载",
    navQuickCmd: "快速命令",
    navTutorial: "教程",
    tutorialTitle: "教程",
    tutorialDesc: "请在此部分加入按顺序排列的截图，引导用户从登录到交换令牌。",
    errApiNotFound: "未找到 API 端点（404）。请先将 /api/token 部署到 Vercel。",
    errApiHtml: "服务器返回的是 HTML 而不是 JSON。请检查部署路由/配置。",
    copiedPs: "PowerShell 命令已复制。",
    copiedCmd: "CMD 命令已复制。",
    copiedPip: "pip 命令已复制。",
    showMore: "查看更多",
    showLess: "收起"
  },
  jp: {
    kicker: "Pixiv OAuth ツールキット",
    title: "Pixiv OAuth Web",
    subtitle: "安全な PKCE フローと Vercel 対応デプロイを備えた、CLI・GUI・Web 向け Pixiv OAuth トークン生成ツールキットです。",
    badgePkce: "PKCE フロー",
    badgeDeploy: "Vercel 対応",
    badgeRelease: "リリースをダウンロード",
    overviewTitle: "プロジェクト概要",
    overviewDesc: "このプロジェクトは Pixiv OAuth トークンの交換・更新を支援し、Windows Portable/Setup 用ビルドスクリプトを提供します。",
    docs: "ドキュメントを読む",
    modesTitle: "利用可能なモード",
    modeCli: "CLI: pixiv_login.py",
    modeGui: "GUI: pixiv_login_gui.py",
    modeWeb: "Web: 静的 UI + サーバーレス /api/token",
    requirementsTitle: "要件",
    reqPy: "Python 3.11+",
    reqDeps: "依存関係: requests, pyinstaller",
    reqBuild: "セットアップインストーラー用 Windows ビルドツールチェーン",
    oauthTitle: "OAuth トークンコンソール",
    lang: "言語",
    open: "1) ログインページを開く",
    placeholder: "2) pixiv:// コールバック URL またはコードをここに貼り付け",
    exchange: "トークンを取得",
    refresh: "トークンを更新",
    result: "結果",
    copyAccess: "access_token をコピー",
    copyRefresh: "refresh_token をコピー",
    ready: "準備完了。",
    opened: "ログインページを開きました。ログイン後、pixiv:// コールバック URL またはコードを貼り付けてください。",
    codeEmpty: "コードが空です。",
    clickOpen: "先に「ログインページを開く」をクリックしてください。",
    noRefresh: "利用可能な refresh_token がありません。",
    copiedAccess: "access_token をコピーしました。",
    copiedRefresh: "refresh_token をコピーしました。",
    nothingAccess: "利用可能な access_token がありません。",
    nothingRefresh: "利用可能な refresh_token がありません。",
    resource: "リソース",
    contact: "連絡先",
    dev: "開発者",
    downloadsTitle: "ダウンロード",
    downloadsDesc: "GitHub Releases から最新ビルドを直接ダウンロードします。",
    quickCmdTitle: "クイックコマンド",
    quickCmdDesc: "PowerShell/CMD ダウンロード用コマンドと pip インストール用コマンドをコピーします。",
    copyPs: "PowerShell をコピー",
    copyCmd: "CMD をコピー",
    copyPip: "pip コマンドをコピー",
    navHomepage: "ホームページ",
    navConsole: "コンソール",
    navDownloads: "ダウンロード",
    navQuickCmd: "クイックコマンド",
    navTutorial: "チュートリアル",
    tutorialTitle: "チュートリアル",
    tutorialDesc: "このセクションに順番付きスクリーンショットを追加して、ログインからトークン交換まで案内してください。",
    errApiNotFound: "API エンドポイントが見つかりません（404）。まず /api/token を Vercel にデプロイしてください。",
    errApiHtml: "サーバーが JSON ではなく HTML を返しました。デプロイルート/設定を確認してください。",
    copiedPs: "PowerShell コマンドをコピーしました。",
    copiedCmd: "CMD コマンドをコピーしました。",
    copiedPip: "pip コマンドをコピーしました。",
    showMore: "もっと見る",
    showLess: "閉じる"
  },
  de: {
    kicker: "Pixiv OAuth-Toolkit",
    title: "Pixiv OAuth-Web",
    subtitle: "Toolkit zum Erzeugen von Pixiv-OAuth-Tokens per CLI, GUI und Web mit sicherem PKCE-Flow und Vercel-fähigem Deployment.",
    badgePkce: "PKCE-Flow",
    badgeDeploy: "Vercel bereit",
    badgeRelease: "Release-Download",
    overviewTitle: "Projektübersicht",
    overviewDesc: "Dieses Projekt hilft beim Austauschen/Aktualisieren von Pixiv OAuth-Tokens und liefert Windows-Buildskripte für Portable/Setup-Artefakte.",
    docs: "Dokumentation lesen",
    modesTitle: "Verfügbare Modi",
    modeCli: "CLI: pixiv_login.py",
    modeGui: "GUI: pixiv_login_gui.py",
    modeWeb: "Web: statische UI + serverloses /api/token",
    requirementsTitle: "Anforderungen",
    reqPy: "Python 3.11+",
    reqDeps: "Abhängigkeiten: requests, pyinstaller",
    reqBuild: "Windows-Build-Toolchain für das Setup-Installationsprogramm",
    oauthTitle: "OAuth-Token-Konsole",
    lang: "Sprache",
    open: "1) Login-Seite öffnen",
    placeholder: "2) pixiv:// Callback-URL oder Code hier einfügen",
    exchange: "Token austauschen",
    refresh: "Token aktualisieren",
    result: "Ergebnis",
    copyAccess: "access_token kopieren",
    copyRefresh: "refresh_token kopieren",
    ready: "Bereit.",
    opened: "Login-Seite geöffnet. Nach dem Login pixiv:// Callback-URL oder Code einfügen.",
    codeEmpty: "Code ist leer.",
    clickOpen: "Klicken Sie zuerst auf „Login-Seite öffnen“.",
    noRefresh: "Kein refresh_token verfügbar.",
    copiedAccess: "access_token kopiert.",
    copiedRefresh: "refresh_token kopiert.",
    nothingAccess: "Kein access_token verfügbar.",
    nothingRefresh: "Kein refresh_token verfügbar.",
    resource: "Ressourcen",
    contact: "Kontakt",
    dev: "Entwickler",
    downloadsTitle: "Downloads",
    downloadsDesc: "Laden Sie den neuesten Build direkt von GitHub Releases herunter.",
    quickCmdTitle: "Schnellbefehl",
    quickCmdDesc: "Kopieren Sie PowerShell/CMD-Downloadbefehle und pip-Installationsbefehl.",
    copyPs: "PowerShell kopieren",
    copyCmd: "CMD kopieren",
    copyPip: "pip-Befehl kopieren",
    navHomepage: "Startseite",
    navConsole: "Konsole",
    navDownloads: "Downloads",
    navQuickCmd: "Schnellbefehl",
    navTutorial: "Tutorial",
    tutorialTitle: "Tutorial",
    tutorialDesc: "Füllen Sie diesen Abschnitt mit geordneten Screenshots, um Nutzer vom Login bis zum Token-Austausch zu führen.",
    errApiNotFound: "API-Endpunkt nicht gefunden (404). Deployen Sie zuerst /api/token auf Vercel.",
    errApiHtml: "Server hat HTML statt JSON zurückgegeben. Prüfen Sie Deployment-Routen/Konfiguration.",
    copiedPs: "PowerShell-Befehl kopiert.",
    copiedCmd: "CMD-Befehl kopiert.",
    copiedPip: "pip-Befehl kopiert.",
    showMore: "Mehr anzeigen",
    showLess: "Weniger anzeigen"
  },
  fr: {
    kicker: "Boîte à outils Pixiv OAuth",
    title: "Web OAuth Pixiv",
    subtitle: "Boîte à outils pour générer des jetons Pixiv OAuth via CLI, GUI et Web avec un flux PKCE sécurisé et un déploiement prêt pour Vercel.",
    badgePkce: "Flux PKCE",
    badgeDeploy: "Prêt pour Vercel",
    badgeRelease: "Télécharger la release",
    overviewTitle: "Aperçu du projet",
    overviewDesc: "Ce projet aide à échanger/rafraîchir les jetons Pixiv OAuth et fournit des scripts de build Windows pour les artefacts Portable/Setup.",
    docs: "Lire la documentation",
    modesTitle: "Modes disponibles",
    modeCli: "CLI: pixiv_login.py",
    modeGui: "GUI: pixiv_login_gui.py",
    modeWeb: "Web: interface statique + serverless /api/token",
    requirementsTitle: "Prérequis",
    reqPy: "Python 3.11+",
    reqDeps: "Dépendances : requests, pyinstaller",
    reqBuild: "Chaîne d’outils Windows pour l’installateur setup",
    oauthTitle: "Console de jetons OAuth",
    lang: "Langue",
    open: "1) Ouvrir la page de connexion",
    placeholder: "2) Collez ici l’URL callback pixiv:// ou le code",
    exchange: "Échanger le jeton",
    refresh: "Rafraîchir le jeton",
    result: "Résultat",
    copyAccess: "Copier access_token",
    copyRefresh: "Copier refresh_token",
    ready: "Prêt.",
    opened: "Page de connexion ouverte. Après connexion, collez l’URL callback pixiv:// ou le code.",
    codeEmpty: "Le code est vide.",
    clickOpen: "Cliquez d’abord sur « Ouvrir la page de connexion ».",
    noRefresh: "Aucun refresh_token disponible.",
    copiedAccess: "access_token copié.",
    copiedRefresh: "refresh_token copié.",
    nothingAccess: "Aucun access_token disponible.",
    nothingRefresh: "Aucun refresh_token disponible.",
    resource: "Ressources",
    contact: "Contact",
    dev: "Développeur",
    downloadsTitle: "Téléchargements",
    downloadsDesc: "Téléchargez la dernière build directement depuis GitHub Releases.",
    quickCmdTitle: "Commande rapide",
    quickCmdDesc: "Copiez la commande de téléchargement PowerShell/CMD et la commande d’installation pip.",
    copyPs: "Copier PowerShell",
    copyCmd: "Copier CMD",
    copyPip: "Copier la commande pip",
    navHomepage: "Accueil",
    navConsole: "Console",
    navDownloads: "Téléchargements",
    navQuickCmd: "Commande rapide",
    navTutorial: "Tutoriel",
    tutorialTitle: "Tutoriel",
    tutorialDesc: "Remplissez cette section avec des captures d’écran ordonnées pour guider les utilisateurs de la connexion jusqu’à l’échange de jetons.",
    errApiNotFound: "Point d’API introuvable (404). Déployez d’abord /api/token sur Vercel.",
    errApiHtml: "Le serveur a renvoyé du HTML au lieu de JSON. Vérifiez les routes/configurations de déploiement.",
    copiedPs: "Commande PowerShell copiée.",
    copiedCmd: "Commande CMD copiée.",
    copiedPip: "Commande pip copiée.",
    showMore: "Voir plus",
    showLess: "Voir moins"
  },
  es: {
    kicker: "Kit de herramientas Pixiv OAuth",
    title: "Web de Pixiv OAuth",
    subtitle: "Kit para generar tokens Pixiv OAuth mediante CLI, GUI y Web con flujo PKCE seguro y despliegue listo para Vercel.",
    badgePkce: "Flujo PKCE",
    badgeDeploy: "Listo para Vercel",
    badgeRelease: "Descargar release",
    overviewTitle: "Resumen del proyecto",
    overviewDesc: "Este proyecto ayuda a intercambiar/actualizar tokens Pixiv OAuth y ofrece scripts de compilación de Windows para artefactos Portable/Setup.",
    docs: "Leer la documentación",
    modesTitle: "Modos disponibles",
    modeCli: "CLI: pixiv_login.py",
    modeGui: "GUI: pixiv_login_gui.py",
    modeWeb: "Web: UI estática + serverless /api/token",
    requirementsTitle: "Requisitos",
    reqPy: "Python 3.11+",
    reqDeps: "Dependencias: requests, pyinstaller",
    reqBuild: "Cadena de herramientas de compilación de Windows para el instalador setup",
    oauthTitle: "Consola de token OAuth",
    lang: "Idioma",
    open: "1) Abrir página de inicio de sesión",
    placeholder: "2) Pega aquí la URL callback pixiv:// o el código",
    exchange: "Intercambiar token",
    refresh: "Actualizar token",
    result: "Resultado",
    copyAccess: "Copiar access_token",
    copyRefresh: "Copiar refresh_token",
    ready: "Listo.",
    opened: "Página de inicio de sesión abierta. Después de iniciar sesión, pega la URL callback pixiv:// o el código.",
    codeEmpty: "El código está vacío.",
    clickOpen: "Haz clic primero en “Abrir página de inicio de sesión”.",
    noRefresh: "No hay refresh_token disponible.",
    copiedAccess: "access_token copiado.",
    copiedRefresh: "refresh_token copiado.",
    nothingAccess: "No hay access_token disponible.",
    nothingRefresh: "No hay refresh_token disponible.",
    resource: "Recursos",
    contact: "Contacto",
    dev: "Desarrollador",
    downloadsTitle: "Descargas",
    downloadsDesc: "Descarga la última build directamente desde GitHub Releases.",
    quickCmdTitle: "Comando rápido",
    quickCmdDesc: "Copia el comando de descarga PowerShell/CMD y el comando de instalación pip.",
    copyPs: "Copiar PowerShell",
    copyCmd: "Copiar CMD",
    copyPip: "Copiar comando pip",
    navHomepage: "Inicio",
    navConsole: "Consola",
    navDownloads: "Descargas",
    navQuickCmd: "Comando rápido",
    navTutorial: "Tutorial",
    tutorialTitle: "Tutorial",
    tutorialDesc: "Completa esta sección con capturas ordenadas para guiar a los usuarios desde el inicio de sesión hasta el intercambio del token.",
    errApiNotFound: "No se encontró el endpoint de API (404). Despliega primero /api/token en Vercel.",
    errApiHtml: "El servidor devolvió HTML en lugar de JSON. Revisa las rutas/configuración del despliegue.",
    copiedPs: "Comando de PowerShell copiado.",
    copiedCmd: "Comando CMD copiado.",
    copiedPip: "Comando pip copiado.",
    showMore: "Ver más",
    showLess: "Ver menos"
  },
  ru: {
    kicker: "Набор инструментов Pixiv OAuth",
    title: "Веб-сайт Pixiv OAuth",
    subtitle: "Инструмент для генерации токенов Pixiv OAuth через CLI, GUI и Web с безопасным PKCE-потоком и развёртыванием, готовым для Vercel.",
    badgePkce: "PKCE-поток",
    badgeDeploy: "Готово для Vercel",
    badgeRelease: "Скачать релиз",
    overviewTitle: "Обзор проекта",
    overviewDesc: "Проект помогает обменивать/обновлять токены Pixiv OAuth и включает Windows-скрипты сборки для Portable/Setup.",
    docs: "Читать документацию",
    modesTitle: "Доступные режимы",
    modeCli: "CLI: pixiv_login.py",
    modeGui: "GUI: pixiv_login_gui.py",
    modeWeb: "Web: статический интерфейс + serverless /api/token",
    requirementsTitle: "Требования",
    reqPy: "Python 3.11+",
    reqDeps: "Зависимости: requests, pyinstaller",
    reqBuild: "Инструменты сборки Windows для setup-установщика",
    oauthTitle: "Консоль OAuth-токена",
    lang: "Язык",
    open: "1) Открыть страницу входа",
    placeholder: "2) Вставьте pixiv:// callback URL или код сюда",
    exchange: "Обменять токен",
    refresh: "Обновить токен",
    result: "Результат",
    copyAccess: "Копировать access_token",
    copyRefresh: "Копировать refresh_token",
    ready: "Готово.",
    opened: "Страница входа открыта. После входа вставьте pixiv:// callback URL или код.",
    codeEmpty: "Код пуст.",
    clickOpen: "Сначала нажмите «Открыть страницу входа».",
    noRefresh: "Нет доступного refresh_token.",
    copiedAccess: "access_token скопирован.",
    copiedRefresh: "refresh_token скопирован.",
    nothingAccess: "Нет доступного access_token.",
    nothingRefresh: "Нет доступного refresh_token.",
    resource: "Ресурсы",
    contact: "Контакты",
    dev: "Разработчик",
    downloadsTitle: "Загрузки",
    downloadsDesc: "Скачайте последнюю сборку напрямую из GitHub Releases.",
    quickCmdTitle: "Быстрая команда",
    quickCmdDesc: "Скопируйте команды загрузки PowerShell/CMD и команду установки pip.",
    copyPs: "Копировать PowerShell",
    copyCmd: "Копировать CMD",
    copyPip: "Копировать команду pip",
    navHomepage: "Главная",
    navConsole: "Консоль",
    navDownloads: "Загрузки",
    navQuickCmd: "Быстрая команда",
    navTutorial: "Учебник",
    tutorialTitle: "Учебник",
    tutorialDesc: "Заполните этот раздел упорядоченными скриншотами, чтобы провести пользователей от входа до обмена токена.",
    errApiNotFound: "API endpoint не найден (404). Сначала разверните /api/token в Vercel.",
    errApiHtml: "Сервер вернул HTML вместо JSON. Проверьте маршруты/конфигурацию развёртывания.",
    copiedPs: "Команда PowerShell скопирована.",
    copiedCmd: "Команда CMD скопирована.",
    copiedPip: "Команда pip скопирована.",
    showMore: "Показать больше",
    showLess: "Показать меньше"
  },
  pt: {
    kicker: "Kit de ferramentas Pixiv OAuth",
    title: "Pixiv OAuth Web",
    subtitle: "Kit para gerar tokens Pixiv OAuth via CLI, GUI e Web com fluxo PKCE seguro e implantação pronta para Vercel.",
    badgePkce: "Fluxo PKCE",
    badgeDeploy: "Pronto para Vercel",
    badgeRelease: "Baixar release",
    overviewTitle: "Visão geral do projeto",
    overviewDesc: "Este projeto ajuda a trocar/atualizar tokens Pixiv OAuth e fornece scripts de build do Windows para artefatos Portable/Setup.",
    docs: "Ler a documentação",
    modesTitle: "Modos disponíveis",
    modeCli: "CLI: pixiv_login.py",
    modeGui: "GUI: pixiv_login_gui.py",
    modeWeb: "Web: UI estática + serverless /api/token",
    requirementsTitle: "Requisitos",
    reqPy: "Python 3.11+",
    reqDeps: "Dependências: requests, pyinstaller",
    reqBuild: "Toolchain de build do Windows para o instalador setup",
    oauthTitle: "Console de token OAuth",
    lang: "Idioma",
    open: "1) Abrir página de login",
    placeholder: "2) Cole aqui a URL de callback pixiv:// ou o código",
    exchange: "Trocar token",
    refresh: "Atualizar token",
    result: "Resultado",
    copyAccess: "Copiar access_token",
    copyRefresh: "Copiar refresh_token",
    ready: "Pronto.",
    opened: "Página de login aberta. Após o login, cole a URL de callback pixiv:// ou o código.",
    codeEmpty: "O código está vazio.",
    clickOpen: "Clique primeiro em “Abrir página de login”.",
    noRefresh: "Nenhum refresh_token disponível.",
    copiedAccess: "access_token copiado.",
    copiedRefresh: "refresh_token copiado.",
    nothingAccess: "Nenhum access_token disponível.",
    nothingRefresh: "Nenhum refresh_token disponível.",
    resource: "Recursos",
    contact: "Contato",
    dev: "Desenvolvedor",
    downloadsTitle: "Downloads",
    downloadsDesc: "Baixe a build mais recente diretamente do GitHub Releases.",
    quickCmdTitle: "Comando rápido",
    quickCmdDesc: "Copie o comando de download PowerShell/CMD e o comando de instalação pip.",
    copyPs: "Copiar PowerShell",
    copyCmd: "Copiar CMD",
    copyPip: "Copiar comando pip",
    navHomepage: "Início",
    navConsole: "Console",
    navDownloads: "Downloads",
    navQuickCmd: "Comando rápido",
    navTutorial: "Tutorial",
    tutorialTitle: "Tutorial",
    tutorialDesc: "Preencha esta seção com capturas de tela em ordem para guiar os usuários do login até a troca do token.",
    errApiNotFound: "Endpoint da API não encontrado (404). Implante /api/token na Vercel primeiro.",
    errApiHtml: "O servidor retornou HTML em vez de JSON. Verifique as rotas/configuração de implantação.",
    copiedPs: "Comando do PowerShell copiado.",
    copiedCmd: "Comando CMD copiado.",
    copiedPip: "Comando pip copiado.",
    showMore: "Ver mais",
    showLess: "Ver menos"
  },
  id: {
    kicker: "Toolkit Pixiv OAuth",
    title: "Web OAuth Pixiv",
    subtitle: "Toolkit untuk mendapatkan token Pixiv OAuth melalui CLI, GUI, dan Web dengan alur PKCE aman serta siap deploy di Vercel.",
    badgePkce: "Alur PKCE",
    badgeDeploy: "Siap Vercel",
    badgeRelease: "Unduh Rilis",
    overviewTitle: "Ringkasan Proyek",
    overviewDesc: "Proyek ini membantu exchange/refresh token Pixiv OAuth dan menyediakan script build Windows untuk artifact Portable/Setup.",
    docs: "Baca dokumentasi",
    modesTitle: "Mode Tersedia",
    modeCli: "CLI: pixiv_login.py",
    modeGui: "GUI: pixiv_login_gui.py",
    modeWeb: "Web: UI statis + serverless /api/token",
    requirementsTitle: "Kebutuhan",
    reqPy: "Python 3.11+",
    reqDeps: "Dependensi: requests, pyinstaller",
    reqBuild: "Toolchain build Windows untuk installer setup",
    oauthTitle: "Konsol Token OAuth",
    lang: "Bahasa",
    open: "1) Buka Halaman Login",
    placeholder: "2) Tempel URL callback pixiv:// atau kode di sini",
    exchange: "Ambil Token",
    refresh: "Refresh Token",
    result: "Hasil",
    copyAccess: "Salin access_token",
    copyRefresh: "Salin refresh_token",
    ready: "Siap.",
    opened: "Halaman login dibuka. Setelah login, tempel URL callback pixiv:// atau kode.",
    codeEmpty: "Kode kosong.",
    clickOpen: "Klik 'Buka Halaman Login' terlebih dahulu.",
    noRefresh: "Belum ada refresh_token.",
    copiedAccess: "access_token tersalin.",
    copiedRefresh: "refresh_token tersalin.",
    nothingAccess: "Belum ada access_token.",
    nothingRefresh: "Belum ada refresh_token.",
    resource: "Sumber",
    contact: "Kontak",
    dev: "Developer",
    downloadsTitle: "Unduhan",
    downloadsDesc: "Unduh build terbaru langsung dari GitHub Releases.",
    quickCmdTitle: "Perintah Cepat",
    quickCmdDesc: "Salin perintah download PowerShell/CMD dan install pip.",
    copyPs: "Salin PowerShell",
    copyCmd: "Salin CMD",
    copyPip: "Salin perintah pip",
    navHomepage: "Beranda",
    navConsole: "Konsol",
    navDownloads: "Unduhan",
    navQuickCmd: "Perintah Cepat",
    navTutorial: "Tutorial",
    tutorialTitle: "Tutorial",
    tutorialDesc: "Isi bagian ini dengan screenshot berurutan untuk memandu pengguna dari login sampai tukar token.",
    tutorialTabStart: "Mulai",
    tutorialTabSteps: "Langkah Tutorial",
    tutorialTabTips: "Tips",
    tutorialPageTitle: "Mulai Tutorial Pixiv OAuth",
    tutorialPageDesc: "Ikuti langkah berurutan dari login sampai exchange token agar proses lebih mudah diikuti di desktop maupun mobile.",
    tutorialStepsTitle: "Langkah Tutorial",
    tutorialBackBtn: "Kembali ke OAuth Console",
    needVisualGuide: "Butuh panduan visual langkah demi langkah?",
    openTutorialPage: "Buka Halaman Tutorial",
    windowsPreviewBadge: "Preview Aplikasi Windows",
    windowsPreviewTitle: "Lihat Pixiv OAuth Windows App Beraksi",
    windowsPreviewDesc: "Preview singkat ini memperlihatkan alur aplikasi Windows dari tahap login hingga token berhasil dibuat.",
    cliPreviewBadge: "Preview CLI",
    cliPreviewTitle: "Preview Output Pixiv OAuth CLI",
    cliPreviewDesc: "Simulasi output CLI untuk membantu melihat proses login, pembacaan code, dan hasil token secara ringkas.",
    openDownloadsPage: "Buka Halaman Unduhan",
    errApiNotFound: "Endpoint API tidak ditemukan (404). Deploy /api/token ke Vercel terlebih dahulu.",
    errApiHtml: "Server mengembalikan HTML, bukan JSON. Periksa route atau konfigurasi deploy.",
    copiedPs: "Perintah PowerShell tersalin.",
    copiedCmd: "Perintah CMD tersalin.",
    copiedPip: "Perintah pip tersalin.",
    showMore: "Lihat Selengkapnya",
    showLess: "Tampilkan Sedikit"
  },
  kr: {
    kicker: "Pixiv OAuth 툴킷",
    title: "Pixiv OAuth 웹",
    subtitle: "안전한 PKCE 흐름과 Vercel 배포 지원을 갖춘 CLI, GUI, Web용 Pixiv OAuth 토큰 생성 툴킷입니다.",
    badgePkce: "PKCE 흐름",
    badgeDeploy: "Vercel 준비",
    badgeRelease: "릴리스 다운로드",
    overviewTitle: "프로젝트 개요",
    overviewDesc: "이 프로젝트는 Pixiv OAuth 토큰 교환/갱신을 돕고 Windows Portable/Setup용 빌드 스크립트를 제공합니다.",
    docs: "문서 읽기",
    modesTitle: "사용 가능한 모드",
    modeCli: "CLI: pixiv_login.py",
    modeGui: "GUI: pixiv_login_gui.py",
    modeWeb: "Web: 정적 UI + 서버리스 /api/token",
    requirementsTitle: "요구 사항",
    reqPy: "Python 3.11+",
    reqDeps: "의존성: requests, pyinstaller",
    reqBuild: "setup 설치 프로그램용 Windows 빌드 도구 체인",
    oauthTitle: "OAuth 토큰 콘솔",
    lang: "언어",
    open: "1) 로그인 페이지 열기",
    placeholder: "2) pixiv:// 콜백 URL 또는 코드를 여기에 붙여넣으세요",
    exchange: "토큰 교환",
    refresh: "토큰 갱신",
    result: "결과",
    copyAccess: "access_token 복사",
    copyRefresh: "refresh_token 복사",
    ready: "준비 완료.",
    opened: "로그인 페이지가 열렸습니다. 로그인 후 pixiv:// 콜백 URL 또는 코드를 붙여넣으세요.",
    codeEmpty: "코드가 비어 있습니다.",
    clickOpen: "먼저 '로그인 페이지 열기'를 클릭하세요.",
    noRefresh: "사용 가능한 refresh_token이 없습니다.",
    copiedAccess: "access_token이 복사되었습니다.",
    copiedRefresh: "refresh_token이 복사되었습니다.",
    nothingAccess: "사용 가능한 access_token이 없습니다.",
    nothingRefresh: "사용 가능한 refresh_token이 없습니다.",
    resource: "리소스",
    contact: "연락처",
    dev: "개발자",
    downloadsTitle: "다운로드",
    downloadsDesc: "GitHub Releases에서 최신 빌드를 직접 다운로드하세요.",
    quickCmdTitle: "빠른 명령",
    quickCmdDesc: "PowerShell/CMD 다운로드 명령과 pip 설치 명령을 복사하세요.",
    copyPs: "PowerShell 복사",
    copyCmd: "CMD 복사",
    copyPip: "pip 명령 복사",
    navHomepage: "홈페이지",
    navConsole: "콘솔",
    navDownloads: "다운로드",
    navQuickCmd: "빠른 명령",
    navTutorial: "튜토리얼",
    tutorialTitle: "튜토리얼",
    tutorialDesc: "이 섹션에 순서가 있는 스크린샷을 넣어 로그인부터 토큰 교환까지 안내하세요.",
    errApiNotFound: "API 엔드포인트를 찾을 수 없습니다(404). 먼저 Vercel에 /api/token을 배포하세요.",
    errApiHtml: "서버가 JSON 대신 HTML을 반환했습니다. 배포 경로/구성을 확인하세요.",
    copiedPs: "PowerShell 명령이 복사되었습니다.",
    copiedCmd: "CMD 명령이 복사되었습니다.",
    copiedPip: "pip 명령이 복사되었습니다.",
    showMore: "더 보기",
    showLess: "접기"
  }
};

// Fill missing keys with English fallback
for (const code of LANG_ORDER) {
  DISPLAY_LANGUAGES[code] = { ...DISPLAY_LANGUAGES.en, ...(DISPLAY_LANGUAGES[code] || {}) };
}

let DISPLAY_LANG = "en";

const FLAG_CLASS = {
  en: "fi-gb",
  pl: "fi-pl",
  zh: "fi-cn",
  jp: "fi-jp",
  de: "fi-de",
  fr: "fi-fr",
  es: "fi-es",
  ru: "fi-ru",
  pt: "fi-pt",
  id: "fi-id",
  kr: "fi-kr"
};

const LANG_NAME = {
  en: "English",
  pl: "Polski",
  zh: "中文",
  jp: "日本語",
  de: "Deutsch",
  fr: "Français",
  es: "Español",
  ru: "Русский",
  pt: "Português",
  id: "Indonesia",
  kr: "한국어"
};

function setDisplayLanguage(langCode) {
  DISPLAY_LANG = LANG_ORDER.includes(langCode) ? langCode : "en";
}

function t(key, vars = {}) {
  const text =
    DISPLAY_LANGUAGES[DISPLAY_LANG]?.[key] ??
    DISPLAY_LANGUAGES.en?.[key] ??
    key;

  return text.replace(/\{(\w+)\}/g, (_, name) => vars[name] ?? `{${name}}`);
}

function releaseLink(name) {
  return `${RELEASE_BASE}/${encodeURIComponent(name)}`;
}

function repoDownloadLink(name) {
  return `${DOWNLOADS_BASE}/${encodeURIComponent(name)}`;
}

function setDownloadLinks(assets = {}) {
  const cliSetup = q("dlCliSetup");
  const cliPortable = q("dlCliPortable");
  const guiSetup = q("dlGuiSetup");
  const guiPortable = q("dlGuiPortable");

  if (cliSetup) cliSetup.href = assets.cliSetup || repoDownloadLink("Pixiv OAuth CLi Setup_latest.exe");
  if (cliPortable) cliPortable.href = assets.cliPortable || repoDownloadLink("Pixiv OAuth CLi (Portable)_latest.exe");
  if (guiSetup) guiSetup.href = assets.guiSetup || repoDownloadLink("Pixiv OAuth GUi Setup_latest.exe");
  if (guiPortable) guiPortable.href = assets.guiPortable || repoDownloadLink("Pixiv OAuth GUi (Portable)_latest.exe");
}

async function hydrateReleaseAssets() {
  try {
    const res = await fetch(RELEASE_API, {
      headers: { Accept: "application/vnd.github+json" }
    });
    if (!res.ok) throw new Error("release api unavailable");

    const release = await res.json();
    const assets = release.assets || [];
    if (!assets.length) throw new Error("no release assets");

    const pick = (matcher) => assets.find((a) => matcher(a.name || ""))?.browser_download_url;

    const resolved = {
      cliSetup: pick((n) => /Pixiv OAuth CLi Setup/i.test(n)),
      cliPortable: pick((n) => /Pixiv OAuth CLi \(Portable\)/i.test(n)),
      guiSetup: pick((n) => /Pixiv OAuth GUi Setup/i.test(n)),
      guiPortable: pick((n) => /Pixiv OAuth GUi \(Portable\)/i.test(n))
    };

    setDownloadLinks(resolved);
    setCommandBlocks(resolved);
  } catch {
    setDownloadLinks();
    setCommandBlocks();
  }
}

function setCommandBlocks(assets = {}) {
  const guiPortable = assets.guiPortable || repoDownloadLink("Pixiv OAuth GUi (Portable)_latest.exe");
  const cliPortable = assets.cliPortable || repoDownloadLink("Pixiv OAuth CLi (Portable)_latest.exe");
  const guiSetup = assets.guiSetup || repoDownloadLink("Pixiv OAuth GUi Setup_latest.exe");
  const cliSetup = assets.cliSetup || repoDownloadLink("Pixiv OAuth CLi Setup_latest.exe");

  const ps = q("psCmd");
  const cmd = q("cmdCmd");
  const pip = q("pipCmd");

  if (ps) {
    ps.textContent = `$guiPortable = "${guiPortable}"
$cliPortable = "${cliPortable}"
$guiSetup = "${guiSetup}"
$cliSetup = "${cliSetup}"
Invoke-WebRequest $guiPortable -OutFile "Pixiv OAuth GUi (Portable).exe"
Invoke-WebRequest $cliPortable -OutFile "Pixiv OAuth CLi (Portable).exe"
Invoke-WebRequest $guiSetup -OutFile "Pixiv OAuth GUi Setup.exe"
Invoke-WebRequest $cliSetup -OutFile "Pixiv OAuth CLi Setup.exe"
`;
  }

  if (cmd) {
    cmd.textContent = `curl -L "${guiPortable}" -o "Pixiv OAuth GUi (Portable).exe"
curl -L "${cliPortable}" -o "Pixiv OAuth CLi (Portable).exe"
curl -L "${guiSetup}" -o "Pixiv OAuth GUi Setup.exe"
curl -L "${cliSetup}" -o "Pixiv OAuth CLi Setup.exe"
`;
  }

  if (pip) {
    pip.textContent = `python -m pip install -r requirements.txt
python -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"`;
  }
}

async function copyText(text, okMessage) {
  await navigator.clipboard.writeText(text);
  if (output) output.textContent = okMessage;
}

function updateLangFlag() {
  const el = q("langFlag");
  const current = q("langCurrent");

  if (el) el.className = `fi ${FLAG_CLASS[DISPLAY_LANG] || "fi-gb"}`;
  if (current) current.textContent = LANG_NAME[DISPLAY_LANG] || "English";

  document.querySelectorAll("#langMenu li").forEach((li) => {
    li.classList.toggle("active", li.dataset.lang === DISPLAY_LANG);
  });
}

function setupLanguageMenu() {
  const toggle = q("langToggle");
  const menu = q("langMenu");
  if (!toggle || !menu) return;

  const close = () => {
    menu.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
  };

  toggle.addEventListener("click", () => {
    const isOpen = menu.classList.toggle("open");
    toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });

  menu.querySelectorAll("li").forEach((item) => {
    item.tabIndex = 0;

    const selectLang = () => {
      setDisplayLanguage(item.dataset.lang);
      localStorage.setItem("pixiv_lang", DISPLAY_LANG);
      document.documentElement.lang = DISPLAY_LANG;
      applyLang();
      close();
    };

    item.addEventListener("click", selectLang);
    item.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        selectLang();
      }
    });
  });

  document.addEventListener("click", (e) => {
    if (!q("langControl")?.contains(e.target)) close();
  });
}

function setupCliPreviewToggle() {
  const preview = q("cliPreviewBox");
  const toggle = q("cliToggleBtn");
  if (!preview || !toggle) return;

  let expanded = false;

  const render = () => {
    preview.classList.toggle("expanded", expanded);
    toggle.textContent = expanded ? t("showLess") : t("showMore");
  };

  toggle.addEventListener("click", () => {
    expanded = !expanded;
    render();
  });

  render();
}

function applyLang() {
  const map = {
    kickerText: "kicker",
    titleText: "title",
    subtitleText: "subtitle",
    badgePkce: "badgePkce",
    badgeDeploy: "badgeDeploy",
    badgeRelease: "badgeRelease",
    overviewTitle: "overviewTitle",
    overviewDesc: "overviewDesc",
    docsBtnLabel: "docs",
    modesTitle: "modesTitle",
    requirementsTitle: "requirementsTitle",
    oauthTitle: "oauthTitle",
    openLoginBtnLabel: "open",
    openLoginBtnLabel2: "open",
    exchangeBtnLabel: "exchange",
    refreshBtnLabel: "refresh",
    resultTitle: "result",
    copyAccessBtnLabel: "copyAccess",
    copyRefreshBtnLabel: "copyRefresh",
    footerResourceTitle: "resource",
    footerContactTitle: "contact",
    footerDevTitle: "dev",
    downloadsTitle: "downloadsTitle",
    downloadsDesc: "downloadsDesc",
    quickCmdTitle: "quickCmdTitle",
    quickCmdDesc: "quickCmdDesc",
    copyPsBtnLabel: "copyPs",
    copyCmdBtnLabel: "copyCmd",
    copyPipBtnLabel: "copyPip",
    modeCli: "modeCli",
    modeGui: "modeGui",
    modeWeb: "modeWeb",
    reqPy: "reqPy",
    reqDeps: "reqDeps",
    reqBuild: "reqBuild",
    navHomepageLabel: "navHomepage",
    navConsole: "navConsole",
    navDownloads: "navDownloads",
    navQuickCmd: "navQuickCmd",
    navTutorial: "navTutorial",
    downloadsTabLabel: "downloadsTitle",
    quickCmdTabLabel: "quickCmdTitle",
    tutorialTitle: "tutorialTitle",
    tutorialDesc: "tutorialDesc",
    needVisualGuideText: "needVisualGuide",
    tutorialCtaBtnLabel: "openTutorialPage",
    windowsPreviewBadge: "windowsPreviewBadge",
    windowsPreviewTitle: "windowsPreviewTitle",
    windowsPreviewDesc: "windowsPreviewDesc",
    cliPreviewBadge: "cliPreviewBadge",
    cliPreviewTitle: "cliPreviewTitle",
    cliPreviewDesc: "cliPreviewDesc",
    downloadsCtaBtnLabel: "openDownloadsPage",
    tutorialTabStart: "tutorialTabStart",
    tutorialTabSteps: "tutorialTabSteps",
    tutorialTabTips: "tutorialTabTips",
    tutorialPageTitle: "tutorialPageTitle",
    tutorialPageDesc: "tutorialPageDesc",
    tutorialStepsTitle: "tutorialStepsTitle",
    tutorialBackBtnLabel: "tutorialBackBtn"
  };

  Object.entries(map).forEach(([id, key]) => {
    const el = q(id);
    if (el) el.textContent = t(key);
  });

  const inputCode = q("inputCode");
  if (inputCode) inputCode.placeholder = t("placeholder");
  if (output) output.textContent = t("ready");

  const cliToggleBtn = q("cliToggleBtn");
  if (cliToggleBtn) {
    const expanded = q("cliPreviewBox")?.classList.contains("expanded");
    cliToggleBtn.textContent = expanded ? t("showLess") : t("showMore");
  }

  updateLangFlag();
}

function b64Url(bytes) {
  return btoa(String.fromCharCode(...bytes))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
}

async function createPkce() {
  const arr = crypto.getRandomValues(new Uint8Array(32));
  codeVerifier = b64Url(arr);
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(codeVerifier));
  return {
    codeVerifier,
    codeChallenge: b64Url([...new Uint8Array(digest)])
  };
}

function parseCode(input) {
  const value = input.trim();
  if (!value) return "";
  if (value.startsWith("pixiv://")) return new URL(value).searchParams.get("code") || "";

  try {
    return new URL(value).searchParams.get("code") || value;
  } catch {
    return value;
  }
}

function apiBase() {
  return "/api/token";
}

function bindClick(id, handler) {
  const el = q(id);
  if (el) el.onclick = handler;
}

async function callApi(payload) {
  const res = await fetch(apiBase(), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const raw = await res.text();
  let data;

  try {
    data = JSON.parse(raw);
  } catch {
    if (res.status === 404) throw new Error(t("errApiNotFound"));
    if ((raw && raw.toLowerCase().includes("<html")) || raw.startsWith("The page")) {
      throw new Error(t("errApiHtml"));
    }
    throw new Error(raw || "Unknown API response");
  }

  if (!res.ok) throw new Error(data.error || JSON.stringify(data));
  return data;
}

bindClick("openLoginBtn", async () => {
  const { codeChallenge } = await createPkce();
  const url = `${LOGIN_URL}?${new URLSearchParams({
    code_challenge: codeChallenge,
    code_challenge_method: "S256",
    client: "pixiv-android"
  })}`;
  window.open(url, "_blank", "noopener");
  if (output) output.textContent = t("opened");
});

bindClick("exchangeBtn", async () => {
  try {
    const input = q("inputCode");
    const code = parseCode(input?.value || "");
    if (!code) throw new Error(t("codeEmpty"));
    if (!codeVerifier) throw new Error(t("clickOpen"));

    const data = await callApi({
      grant_type: "authorization_code",
      code,
      code_verifier: codeVerifier,
      redirect_uri: REDIRECT_URI,
      client_id: CLIENT_ID,
      include_policy: true
    });

    tokenState = data;
    if (output) output.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    if (output) output.textContent = `Error: ${e.message}`;
  }
});

bindClick("refreshBtn", async () => {
  try {
    if (!tokenState.refresh_token) throw new Error(t("noRefresh"));

    const data = await callApi({
      grant_type: "refresh_token",
      refresh_token: tokenState.refresh_token,
      client_id: CLIENT_ID,
      include_policy: true
    });

    tokenState = data;
    if (output) output.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    if (output) output.textContent = `Error: ${e.message}`;
  }
});

bindClick("copyAccessBtn", async () => {
  if (!tokenState.access_token) {
    if (output) output.textContent = t("nothingAccess");
    return;
  }
  await copyText(tokenState.access_token, t("copiedAccess"));
});

bindClick("copyRefreshBtn", async () => {
  if (!tokenState.refresh_token) {
    if (output) output.textContent = t("nothingRefresh");
    return;
  }
  await copyText(tokenState.refresh_token, t("copiedRefresh"));
});

bindClick("copyPsBtn", async () => {
  const el = q("psCmd");
  if (el) await copyText(el.textContent, t("copiedPs"));
});

bindClick("copyCmdBtn", async () => {
  const el = q("cmdCmd");
  if (el) await copyText(el.textContent, t("copiedCmd"));
});

bindClick("copyPipBtn", async () => {
  const el = q("pipCmd");
  if (el) await copyText(el.textContent, t("copiedPip"));
});

(async function init() {
  const saved = localStorage.getItem("pixiv_lang");
  if (saved && LANG_ORDER.includes(saved)) {
    setDisplayLanguage(saved);
  }

  document.documentElement.lang = DISPLAY_LANG;

  setupLanguageMenu();
  setupCliPreviewToggle();
  applyLang();
  await hydrateReleaseAssets();
})();
