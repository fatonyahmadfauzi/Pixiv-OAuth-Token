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

const LANG_ORDER = ["en", "pl", "zh", "jp", "de", "fr", "es", "ru", "pt", "id", "kr"];
const I18N = {
  en: {
    kicker: "Pixiv OAuth Toolkit",
    title: "Pixiv OAuth Web",
    subtitle: "Toolkit to generate Pixiv OAuth tokens via CLI, GUI, and Web with secure PKCE flow and Vercel-ready deployment.",
    badgePkce: "PKCE Flow", badgeDeploy: "Vercel Ready", badgeRelease: "Release Download",
    overviewTitle: "Project Overview",
    overviewDesc: "This project helps exchange/refresh Pixiv OAuth tokens and ships Windows build scripts for Portable/Setup artifacts.",
    docs: "Read the docs",
    modesTitle: "Available Modes", modeCli: "CLI: pixiv_login.py", modeGui: "GUI: pixiv_login_gui.py", modeWeb: "Web: static UI + serverless /api/token",
    requirementsTitle: "Requirements", reqPy: "Python 3.11+", reqDeps: "Dependencies: requests, pyinstaller", reqBuild: "Windows build toolchain for setup installer",
    oauthTitle: "OAuth Token Console",
    lang: "Language", open: "1) Open Login Page", placeholder: "2) Paste pixiv:// callback URL or code here",
    exchange: "Exchange Token", refresh: "Refresh Token", result: "Result",
    copyAccess: "Copy access_token", copyRefresh: "Copy refresh_token", ready: "Ready.",
    opened: "Login page opened. After login, paste pixiv:// callback URL or code.",
    codeEmpty: "Code is empty.", clickOpen: "Click 'Open Login Page' first.", noRefresh: "No refresh_token available.",
    copiedAccess: "access_token copied.", copiedRefresh: "refresh_token copied.",
    nothingAccess: "No access_token available.", nothingRefresh: "No refresh_token available.",
    resource: "Resources", contact: "Contact", dev: "Developer",
    downloadsTitle: "Downloads", downloadsDesc: "Download latest build directly from GitHub Releases.",
    quickCmdTitle: "Quick Command", quickCmdDesc: "Copy command for PowerShell/CMD download and pip install.",
    copyPs: "Copy PowerShell", copyCmd: "Copy CMD", copyPip: "Copy pip command",
    navConsole: "Console", navDownloads: "Downloads", navQuickCmd: "Quick Cmd", navTutorial: "Tutorial",
    tutorialTitle: "Tutorial", tutorialDesc: "Fill this section with ordered screenshots to guide users from login to token exchange.",
    tutorialCtaText: "Need visual step-by-step guide?", tutorialCtaBtnLabel: "Open Tutorial Page",
    windowsPreviewBadge: "Windows App Preview", windowsPreviewTitle: "See Pixiv OAuth Windows App in Action",
    windowsPreviewDesc: "Short preview of the Windows app flow from login to successful token generation.",
    windowsVideoFallback: "Your browser does not support HTML5 video.",
    cliPreviewBadge: "CLI Preview", cliPreviewTitle: "Preview Pixiv OAuth CLI Output",
    cliPreviewDesc: "CLI output simulation to quickly understand login, code parsing, and token results.",
    cliFigureLabel: "Fig. CLI — Pixiv OAuth Token Preview", cliToggleMore: "See More", cliToggleLess: "Show Less",
    downloadsCtaText: "Downloads & quick commands are now on a dedicated page.", downloadsCtaBtnLabel: "Open Downloads Page",
    downloadsBrandTag: "DOWNLOAD", downloadsHomeLink: "Homepage", downloadsTutorialLink: "Tutorial", downloadsConsoleLink: "Console",
    downloadsTabDownloads: "Downloads", downloadsTabQuickCmd: "Quick Command", downloadsFooterTag: "DOWNLOAD",
    tutorialBrandTag: "TUTORIAL", tutorialHomeLink: "Homepage", tutorialConsoleLink: "Console", tutorialDownloadsLink: "Downloads",
    tutorialTabStart: "Get Started", tutorialTabSteps: "Tutorial Steps", tutorialTabTips: "Tips",
    tutorialIntroTitle: "Get Started with Pixiv OAuth Tutorial", tutorialIntroDesc: "Follow each step from login to token exchange so the process is easier on desktop and mobile.",
    tutorialStep1Title: "Open Login Page", tutorialStep1Desc: "Open the Pixiv login page from the web console tool.",
    tutorialStep2Title: "Continue Login", tutorialStep2Desc: "Continue login until Pixiv redirects you to the callback page.",
    tutorialStep3Title: "Open Console", tutorialStep3Desc: "Open DevTools/Console to capture the pixiv callback URL.",
    tutorialStep4Title: "Copy pixiv URL", tutorialStep4Desc: "Copy the callback URL that contains Pixiv authorization code.",
    tutorialStep5Title: "Paste URL / Code", tutorialStep5Desc: "Paste callback URL or code into the OAuth console input.",
    tutorialStep6Title: "Exchange Token", tutorialStep6Desc: "Click Exchange Token, then copy access_token and refresh_token.",
    tutorialBackToConsole: "Back to OAuth Console", tutorialFooterTag: "TUTORIAL",
    footerGithub: "GitHub Repository", footerOAuthEndpoint: "Pixiv OAuth Endpoint", footerPython: "Python 3.11+", footerPyInstaller: "PyInstaller", footerVercel: "Vercel", footerTikTok: "TikTok", footerTwitter: "Twitter", footerDeveloperName: "Fatony Ahmad Fauzi",
    errApiNotFound: "API endpoint not found (404). Deploy /api/token on Vercel first.",
    errApiHtml: "Server returned HTML instead of JSON. Check deployment routes/config.",
    copiedPs: "PowerShell command copied.", copiedCmd: "CMD command copied.", copiedPip: "pip command copied."
  },
  id: {
    subtitle: "Toolkit untuk mendapatkan token Pixiv OAuth melalui CLI, GUI, dan Web dengan alur PKCE aman serta siap deploy di Vercel.",
    overviewTitle: "Ringkasan Project", overviewDesc: "Project ini membantu exchange/refresh token Pixiv OAuth dan menyediakan script build Windows untuk artifact Portable/Setup.",
    docs: "Baca dokumentasi",
    modesTitle: "Mode Tersedia", requirementsTitle: "Kebutuhan", oauthTitle: "Konsol Token OAuth",
    lang: "Bahasa", open: "1) Buka Halaman Login", placeholder: "2) Tempel URL callback pixiv:// atau code di sini",
    exchange: "Ambil Token", refresh: "Refresh Token", result: "Hasil",
    copyAccess: "Salin access_token", copyRefresh: "Salin refresh_token", ready: "Siap.",
    opened: "Halaman login dibuka. Setelah login, tempel URL pixiv:// atau code.",
    codeEmpty: "Code kosong.", clickOpen: "Klik 'Buka Halaman Login' dulu.", noRefresh: "Belum ada refresh_token.",
    copiedAccess: "access_token tersalin.", copiedRefresh: "refresh_token tersalin.",
    nothingAccess: "Belum ada access_token.", nothingRefresh: "Belum ada refresh_token.",
    resource: "Resource", contact: "Kontak", dev: "Developer",
    downloadsTitle: "Unduhan", downloadsDesc: "Unduh build terbaru langsung dari GitHub Releases.",
    quickCmdTitle: "Perintah Cepat", quickCmdDesc: "Salin command download PowerShell/CMD dan install pip.",
    copyPs: "Salin PowerShell", copyCmd: "Salin CMD", copyPip: "Salin perintah pip",
    navConsole: "Konsol", navDownloads: "Unduhan", navQuickCmd: "Perintah Cepat", navTutorial: "Tutorial",
    tutorialTitle: "Tutorial", tutorialDesc: "Isi bagian ini dengan screenshot berurutan untuk panduan login sampai tukar token.",
    tutorialCtaText: "Butuh panduan visual langkah demi langkah?", tutorialCtaBtnLabel: "Buka Halaman Tutorial",
    windowsPreviewBadge: "Preview Aplikasi Windows", windowsPreviewTitle: "Lihat Aplikasi Pixiv OAuth Windows Beraksi",
    windowsPreviewDesc: "Preview singkat alur aplikasi Windows dari login sampai token berhasil dibuat.",
    windowsVideoFallback: "Browser Anda tidak mendukung video HTML5.",
    cliPreviewBadge: "Preview CLI", cliPreviewTitle: "Preview Output CLI Pixiv OAuth",
    cliPreviewDesc: "Simulasi output CLI untuk melihat proses login, pembacaan code, dan hasil token secara ringkas.",
    cliFigureLabel: "Gambar CLI — Preview Token Pixiv OAuth", cliToggleMore: "Lihat Lebih Banyak", cliToggleLess: "Lihat Lebih Sedikit",
    downloadsCtaText: "Unduhan & perintah cepat sekarang ada di halaman khusus.", downloadsCtaBtnLabel: "Buka Halaman Unduhan",
    downloadsBrandTag: "UNDUH", downloadsHomeLink: "Beranda", downloadsTutorialLink: "Tutorial", downloadsConsoleLink: "Konsol",
    downloadsTabDownloads: "Unduhan", downloadsTabQuickCmd: "Perintah Cepat", downloadsFooterTag: "UNDUH",
    tutorialBrandTag: "TUTORIAL", tutorialHomeLink: "Beranda", tutorialConsoleLink: "Konsol", tutorialDownloadsLink: "Unduhan",
    tutorialTabStart: "Mulai", tutorialTabSteps: "Langkah Tutorial", tutorialTabTips: "Tips",
    tutorialIntroTitle: "Mulai Tutorial Pixiv OAuth", tutorialIntroDesc: "Ikuti langkah berurutan dari login sampai exchange token agar proses lebih mudah di desktop maupun mobile.",
    tutorialStep1Title: "Buka Halaman Login", tutorialStep1Desc: "Buka halaman login Pixiv dari konsol web tool.",
    tutorialStep2Title: "Lanjutkan Login", tutorialStep2Desc: "Lanjutkan login sampai Pixiv mengarahkan ke halaman callback.",
    tutorialStep3Title: "Buka Console", tutorialStep3Desc: "Buka DevTools/Console untuk mengambil URL callback pixiv.",
    tutorialStep4Title: "Salin URL pixiv", tutorialStep4Desc: "Salin URL callback yang berisi authorization code dari Pixiv.",
    tutorialStep5Title: "Tempel URL / Code", tutorialStep5Desc: "Tempel URL callback atau code ke input OAuth console.",
    tutorialStep6Title: "Tukar Token", tutorialStep6Desc: "Klik Exchange Token, lalu salin access_token dan refresh_token.",
    tutorialBackToConsole: "Kembali ke OAuth Console", tutorialFooterTag: "TUTORIAL",
    footerGithub: "Repository GitHub", footerOAuthEndpoint: "Endpoint OAuth Pixiv", footerPython: "Python 3.11+", footerPyInstaller: "PyInstaller", footerVercel: "Vercel", footerTikTok: "TikTok", footerTwitter: "Twitter/X", footerDeveloperName: "Fatony Ahmad Fauzi",
    errApiNotFound: "Endpoint API tidak ditemukan (404). Deploy /api/token di Vercel dulu.",
    errApiHtml: "Server mengembalikan HTML, bukan JSON. Cek konfigurasi route/deploy.",
    copiedPs: "Command PowerShell tersalin.", copiedCmd: "Command CMD tersalin.", copiedPip: "Command pip tersalin."
  },
  jp: {
    subtitle: "CLI・GUI・Web向け Pixiv OAuth（PKCE）ツールキット。Vercel にデプロイ可能。",
    overviewTitle: "プロジェクト概要", modesTitle: "利用モード", requirementsTitle: "要件", oauthTitle: "OAuth トークンコンソール",
    overviewDesc: "このプロジェクトは Pixiv OAuth トークンの取得/更新を支援し、Windows の Portable/Setup ビルドを提供します。",
    docs: "ドキュメントを読む",
    lang: "言語", open: "1) ログインページを開く", placeholder: "2) pixiv:// コールバックURLまたはコードを貼り付け",
    exchange: "トークン取得", refresh: "トークン更新", result: "結果",
    copyAccess: "access_tokenをコピー", copyRefresh: "refresh_tokenをコピー", ready: "準備完了。",
    opened: "ログインページを開きました。ログイン後にpixiv:// URLかコードを貼り付けてください。",
    codeEmpty: "コードが空です。", clickOpen: "先に「ログインページを開く」を押してください。", noRefresh: "refresh_tokenがありません。",
    copiedAccess: "access_tokenをコピーしました。", copiedRefresh: "refresh_tokenをコピーしました。",
    nothingAccess: "access_tokenがありません。", nothingRefresh: "refresh_tokenがありません。",
    resource: "リソース", contact: "連絡先", dev: "開発者",
    downloadsTitle: "ダウンロード", downloadsDesc: "GitHub Releases から最新ビルドをダウンロード。",
    quickCmdTitle: "クイックコマンド", quickCmdDesc: "PowerShell/CMD ダウンロードと pip インストール用コマンド。",
    copyPs: "PowerShellをコピー", copyCmd: "CMDをコピー", copyPip: "pipコマンドをコピー"
  },
  pl: {
    lang: "Język", overviewTitle: "Przegląd projektu", modesTitle: "Dostępne tryby", requirementsTitle: "Wymagania", oauthTitle: "Konsola tokenów OAuth",
    overviewDesc: "Projekt pomaga uzyskiwać/odświeżać tokeny Pixiv OAuth i zawiera skrypty build dla Windows.", docs: "Czytaj dokumentację",
    open: "1) Otwórz stronę logowania", placeholder: "2) Wklej URL zwrotny pixiv:// lub kod tutaj", exchange: "Wymień token", refresh: "Odśwież token", result: "Wynik",
    copyAccess: "Kopiuj access_token", copyRefresh: "Kopiuj refresh_token", ready: "Gotowe.",
    resource: "Zasoby", contact: "Kontakt", dev: "Deweloper", downloadsTitle: "Pobieranie", downloadsDesc: "Pobierz najnowszą wersję z GitHub Releases.",
    quickCmdTitle: "Szybkie polecenie", quickCmdDesc: "Skopiuj polecenie PowerShell/CMD oraz instalację pip.",
    copyPs: "Kopiuj PowerShell", copyCmd: "Kopiuj CMD", copyPip: "Kopiuj polecenie pip"
  },
  zh: {
    lang: "语言", overviewTitle: "项目概览", modesTitle: "可用模式", requirementsTitle: "环境要求", oauthTitle: "OAuth 令牌控制台",
    overviewDesc: "该项目可帮助获取/刷新 Pixiv OAuth 令牌，并提供 Windows 打包脚本。", docs: "阅读文档",
    open: "1) 打开登录页面", placeholder: "2) 在此粘贴 pixiv:// 回调URL或代码", exchange: "交换令牌", refresh: "刷新令牌", result: "结果",
    copyAccess: "复制 access_token", copyRefresh: "复制 refresh_token", ready: "就绪。",
    resource: "资源", contact: "联系", dev: "开发者", downloadsTitle: "下载", downloadsDesc: "从 GitHub Releases 下载最新版本。",
    quickCmdTitle: "快速命令", quickCmdDesc: "复制 PowerShell/CMD 下载命令和 pip 安装命令。",
    copyPs: "复制 PowerShell", copyCmd: "复制 CMD", copyPip: "复制 pip 命令"
  },
  de: {
    lang: "Sprache", overviewTitle: "Projektübersicht", modesTitle: "Verfügbare Modi", requirementsTitle: "Anforderungen", oauthTitle: "OAuth-Token-Konsole",
    overviewDesc: "Dieses Projekt hilft beim Abrufen/Aktualisieren von Pixiv OAuth-Token und enthält Build-Skripte für Windows.", docs: "Dokumentation lesen",
    open: "1) Login-Seite öffnen", placeholder: "2) pixiv:// Callback-URL oder Code hier einfügen", exchange: "Token abrufen", refresh: "Token aktualisieren", result: "Ergebnis",
    copyAccess: "access_token kopieren", copyRefresh: "refresh_token kopieren", ready: "Bereit.",
    resource: "Ressourcen", contact: "Kontakt", dev: "Entwickler", downloadsTitle: "Downloads", downloadsDesc: "Lade den neuesten Build von GitHub Releases herunter.",
    quickCmdTitle: "Schnellbefehl", quickCmdDesc: "Kopiere PowerShell/CMD-Download- und pip-Installationsbefehle.",
    copyPs: "PowerShell kopieren", copyCmd: "CMD kopieren", copyPip: "pip-Befehl kopieren"
  },
  fr: {
    lang: "Langue", overviewTitle: "Aperçu du projet", modesTitle: "Modes disponibles", requirementsTitle: "Prérequis", oauthTitle: "Console de jetons OAuth",
    overviewDesc: "Ce projet aide à échanger/rafraîchir les jetons Pixiv OAuth et fournit des scripts de build Windows.", docs: "Lire la documentation",
    open: "1) Ouvrir la page de connexion", placeholder: "2) Collez l'URL callback pixiv:// ou le code ici", exchange: "Échanger le jeton", refresh: "Rafraîchir le jeton", result: "Résultat",
    copyAccess: "Copier access_token", copyRefresh: "Copier refresh_token", ready: "Prêt.",
    resource: "Ressources", contact: "Contact", dev: "Développeur", downloadsTitle: "Téléchargements", downloadsDesc: "Téléchargez la dernière version depuis GitHub Releases.",
    quickCmdTitle: "Commande rapide", quickCmdDesc: "Copiez les commandes PowerShell/CMD et l'installation pip.",
    copyPs: "Copier PowerShell", copyCmd: "Copier CMD", copyPip: "Copier la commande pip"
  },
  es: {
    lang: "Idioma", overviewTitle: "Resumen del proyecto", modesTitle: "Modos disponibles", requirementsTitle: "Requisitos", oauthTitle: "Consola de token OAuth",
    overviewDesc: "Este proyecto ayuda a intercambiar/actualizar tokens Pixiv OAuth e incluye scripts de build para Windows.", docs: "Leer la documentación",
    open: "1) Abrir página de inicio de sesión", placeholder: "2) Pega aquí la URL callback pixiv:// o el código", exchange: "Intercambiar token", refresh: "Actualizar token", result: "Resultado",
    copyAccess: "Copiar access_token", copyRefresh: "Copiar refresh_token", ready: "Listo.",
    resource: "Recursos", contact: "Contacto", dev: "Desarrollador", downloadsTitle: "Descargas", downloadsDesc: "Descarga la última versión desde GitHub Releases.",
    quickCmdTitle: "Comando rápido", quickCmdDesc: "Copia comandos de PowerShell/CMD e instalación por pip.",
    copyPs: "Copiar PowerShell", copyCmd: "Copiar CMD", copyPip: "Copiar comando pip"
  },
  ru: {
    lang: "Язык", overviewTitle: "Обзор проекта", modesTitle: "Доступные режимы", requirementsTitle: "Требования", oauthTitle: "Консоль OAuth-токена",
    overviewDesc: "Проект помогает получать/обновлять токены Pixiv OAuth и включает скрипты сборки для Windows.", docs: "Читать документацию",
    open: "1) Открыть страницу входа", placeholder: "2) Вставьте pixiv:// callback URL или код", exchange: "Получить токен", refresh: "Обновить токен", result: "Результат",
    copyAccess: "Копировать access_token", copyRefresh: "Копировать refresh_token", ready: "Готово.",
    resource: "Ресурсы", contact: "Контакты", dev: "Разработчик", downloadsTitle: "Загрузки", downloadsDesc: "Скачать последнюю сборку с GitHub Releases.",
    quickCmdTitle: "Быстрая команда", quickCmdDesc: "Скопируйте команды PowerShell/CMD и установку pip.",
    copyPs: "Копировать PowerShell", copyCmd: "Копировать CMD", copyPip: "Копировать команду pip"
  },
  pt: {
    lang: "Idioma", overviewTitle: "Visão geral do projeto", modesTitle: "Modos disponíveis", requirementsTitle: "Requisitos", oauthTitle: "Console de token OAuth",
    overviewDesc: "Este projeto ajuda a trocar/atualizar tokens Pixiv OAuth e inclui scripts de build para Windows.", docs: "Ler a documentação",
    open: "1) Abrir página de login", placeholder: "2) Cole a URL de callback pixiv:// ou código aqui", exchange: "Trocar token", refresh: "Atualizar token", result: "Resultado",
    copyAccess: "Copiar access_token", copyRefresh: "Copiar refresh_token", ready: "Pronto.",
    resource: "Recursos", contact: "Contato", dev: "Desenvolvedor", downloadsTitle: "Downloads", downloadsDesc: "Baixe a versão mais recente no GitHub Releases.",
    quickCmdTitle: "Comando rápido", quickCmdDesc: "Copie comandos de download PowerShell/CMD e instalação via pip.",
    copyPs: "Copiar PowerShell", copyCmd: "Copiar CMD", copyPip: "Copiar comando pip"
  },
  kr: {
    lang: "언어", overviewTitle: "프로젝트 개요", modesTitle: "사용 가능한 모드", requirementsTitle: "요구 사항", oauthTitle: "OAuth 토큰 콘솔",
    overviewDesc: "이 프로젝트는 Pixiv OAuth 토큰 발급/갱신을 돕고 Windows 빌드 스크립트를 제공합니다.", docs: "문서 읽기",
    open: "1) 로그인 페이지 열기", placeholder: "2) pixiv:// 콜백 URL 또는 코드를 붙여넣으세요", exchange: "토큰 교환", refresh: "토큰 갱신", result: "결과",
    copyAccess: "access_token 복사", copyRefresh: "refresh_token 복사", ready: "준비 완료.",
    resource: "리소스", contact: "연락처", dev: "개발자", downloadsTitle: "다운로드", downloadsDesc: "GitHub Releases에서 최신 빌드를 다운로드하세요.",
    quickCmdTitle: "빠른 명령", quickCmdDesc: "PowerShell/CMD 다운로드 명령과 pip 설치 명령을 복사하세요.",
    copyPs: "PowerShell 복사", copyCmd: "CMD 복사", copyPip: "pip 명령 복사"
  }
};

const EXTRA_I18N = {
  pl: {
    downloadsBrandTag: "POBIERZ", downloadsHomeLink: "Strona główna", downloadsTutorialLink: "Poradnik", downloadsConsoleLink: "Konsola",
    downloadsTabDownloads: "Pobieranie", downloadsTabQuickCmd: "Szybkie polecenie", downloadsFooterTag: "POBIERZ",
    tutorialBrandTag: "PORADNIK", tutorialHomeLink: "Strona główna", tutorialConsoleLink: "Konsola", tutorialDownloadsLink: "Pobieranie",
    tutorialTabStart: "Start", tutorialTabSteps: "Kroki poradnika", tutorialTabTips: "Wskazówki",
    tutorialIntroTitle: "Rozpocznij poradnik Pixiv OAuth", tutorialIntroDesc: "Postępuj krok po kroku od logowania do wymiany tokena na komputerze i telefonie.",
    tutorialStep1Title: "Otwórz stronę logowania", tutorialStep1Desc: "Otwórz stronę logowania Pixiv z konsoli web.",
    tutorialStep2Title: "Kontynuuj logowanie", tutorialStep2Desc: "Kontynuuj logowanie aż Pixiv przekieruje do callback.",
    tutorialStep3Title: "Otwórz konsolę", tutorialStep3Desc: "Otwórz DevTools/Console, aby pobrać URL callback pixiv.",
    tutorialStep4Title: "Skopiuj URL pixiv", tutorialStep4Desc: "Skopiuj URL callback zawierający kod autoryzacyjny Pixiv.",
    tutorialStep5Title: "Wklej URL / kod", tutorialStep5Desc: "Wklej URL callback lub kod do pola OAuth console.",
    tutorialStep6Title: "Wymień token", tutorialStep6Desc: "Kliknij Wymień token, potem skopiuj access_token i refresh_token.",
    tutorialBackToConsole: "Wróć do OAuth Console", tutorialFooterTag: "PORADNIK",
    footerGithub: "Repozytorium GitHub", footerOAuthEndpoint: "Endpoint OAuth Pixiv", footerTwitter: "Twitter/X"
  },
  zh: {
    downloadsBrandTag: "下载", downloadsHomeLink: "主页", downloadsTutorialLink: "教程", downloadsConsoleLink: "控制台",
    downloadsTabDownloads: "下载", downloadsTabQuickCmd: "快速命令", downloadsFooterTag: "下载",
    tutorialBrandTag: "教程", tutorialHomeLink: "主页", tutorialConsoleLink: "控制台", tutorialDownloadsLink: "下载",
    tutorialTabStart: "开始", tutorialTabSteps: "教程步骤", tutorialTabTips: "提示",
    tutorialIntroTitle: "开始使用 Pixiv OAuth 教程", tutorialIntroDesc: "按顺序完成登录到交换令牌步骤，桌面和手机都更容易操作。",
    tutorialStep1Title: "打开登录页面", tutorialStep1Desc: "从网页控制台工具打开 Pixiv 登录页面。",
    tutorialStep2Title: "继续登录", tutorialStep2Desc: "继续登录直到 Pixiv 跳转到回调页面。",
    tutorialStep3Title: "打开控制台", tutorialStep3Desc: "打开 DevTools/Console 获取 pixiv 回调 URL。",
    tutorialStep4Title: "复制 pixiv URL", tutorialStep4Desc: "复制包含 Pixiv 授权码的回调 URL。",
    tutorialStep5Title: "粘贴 URL / 代码", tutorialStep5Desc: "将回调 URL 或代码粘贴到 OAuth 控制台输入框。",
    tutorialStep6Title: "交换令牌", tutorialStep6Desc: "点击交换令牌，然后复制 access_token 和 refresh_token。",
    tutorialBackToConsole: "返回 OAuth 控制台", tutorialFooterTag: "教程",
    footerGithub: "GitHub 仓库", footerOAuthEndpoint: "Pixiv OAuth 端点", footerTwitter: "Twitter/X"
  },
  jp: {
    downloadsBrandTag: "ダウンロード", downloadsHomeLink: "ホーム", downloadsTutorialLink: "チュートリアル", downloadsConsoleLink: "コンソール",
    downloadsTabDownloads: "ダウンロード", downloadsTabQuickCmd: "クイックコマンド", downloadsFooterTag: "ダウンロード",
    tutorialBrandTag: "チュートリアル", tutorialHomeLink: "ホーム", tutorialConsoleLink: "コンソール", tutorialDownloadsLink: "ダウンロード",
    tutorialTabStart: "はじめに", tutorialTabSteps: "手順", tutorialTabTips: "ヒント",
    tutorialIntroTitle: "Pixiv OAuth チュートリアルを始める", tutorialIntroDesc: "ログインからトークン交換まで順番に進めるとPC/モバイルでも簡単です。",
    tutorialStep1Title: "ログインページを開く", tutorialStep1Desc: "WebコンソールからPixivログインページを開きます。",
    tutorialStep2Title: "ログインを続行", tutorialStep2Desc: "Pixivがコールバックへリダイレクトするまで進めます。",
    tutorialStep3Title: "コンソールを開く", tutorialStep3Desc: "DevTools/ConsoleでpixivコールバックURLを取得します。",
    tutorialStep4Title: "pixiv URLをコピー", tutorialStep4Desc: "Pixiv認証コードを含むコールバックURLをコピーします。",
    tutorialStep5Title: "URL / コードを貼り付け", tutorialStep5Desc: "OAuthコンソール入力欄へURLまたはコードを貼り付けます。",
    tutorialStep6Title: "トークン交換", tutorialStep6Desc: "トークン交換を押して、access_token / refresh_token をコピーします。",
    tutorialBackToConsole: "OAuthコンソールに戻る", tutorialFooterTag: "チュートリアル",
    footerGithub: "GitHub リポジトリ", footerOAuthEndpoint: "Pixiv OAuth エンドポイント", footerTwitter: "Twitter/X"
  },
  de: {
    downloadsBrandTag: "DOWNLOAD", downloadsHomeLink: "Startseite", downloadsTutorialLink: "Tutorial", downloadsConsoleLink: "Konsole",
    downloadsTabDownloads: "Downloads", downloadsTabQuickCmd: "Schnellbefehl", downloadsFooterTag: "DOWNLOAD",
    tutorialBrandTag: "TUTORIAL", tutorialHomeLink: "Startseite", tutorialConsoleLink: "Konsole", tutorialDownloadsLink: "Downloads",
    tutorialTabStart: "Start", tutorialTabSteps: "Tutorial-Schritte", tutorialTabTips: "Tipps",
    tutorialIntroTitle: "Mit dem Pixiv OAuth Tutorial starten", tutorialIntroDesc: "Folge den Schritten von Login bis Token-Austausch für Desktop und Mobile.",
    tutorialStep1Title: "Login-Seite öffnen", tutorialStep1Desc: "Öffne die Pixiv-Login-Seite aus der Web-Konsole.",
    tutorialStep2Title: "Login fortsetzen", tutorialStep2Desc: "Fahre fort, bis Pixiv zur Callback-Seite weiterleitet.",
    tutorialStep3Title: "Konsole öffnen", tutorialStep3Desc: "Öffne DevTools/Console, um die pixiv Callback-URL zu holen.",
    tutorialStep4Title: "pixiv URL kopieren", tutorialStep4Desc: "Kopiere die Callback-URL mit dem Pixiv-Autorisierungscode.",
    tutorialStep5Title: "URL / Code einfügen", tutorialStep5Desc: "Füge URL oder Code in das OAuth-Konsolenfeld ein.",
    tutorialStep6Title: "Token austauschen", tutorialStep6Desc: "Klicke auf Token austauschen und kopiere access_token / refresh_token.",
    tutorialBackToConsole: "Zurück zur OAuth-Konsole", tutorialFooterTag: "TUTORIAL",
    footerGithub: "GitHub-Repository", footerOAuthEndpoint: "Pixiv OAuth-Endpunkt", footerTwitter: "Twitter/X"
  },
  fr: {
    downloadsBrandTag: "TÉLÉCHARGER", downloadsHomeLink: "Accueil", downloadsTutorialLink: "Tutoriel", downloadsConsoleLink: "Console",
    downloadsTabDownloads: "Téléchargements", downloadsTabQuickCmd: "Commande rapide", downloadsFooterTag: "TÉLÉCHARGER",
    tutorialBrandTag: "TUTORIEL", tutorialHomeLink: "Accueil", tutorialConsoleLink: "Console", tutorialDownloadsLink: "Téléchargements",
    tutorialTabStart: "Commencer", tutorialTabSteps: "Étapes du tutoriel", tutorialTabTips: "Astuces",
    tutorialIntroTitle: "Commencer le tutoriel Pixiv OAuth", tutorialIntroDesc: "Suivez les étapes du login à l'échange de token sur desktop et mobile.",
    tutorialStep1Title: "Ouvrir la page de connexion", tutorialStep1Desc: "Ouvrez la page de connexion Pixiv depuis la console web.",
    tutorialStep2Title: "Continuer la connexion", tutorialStep2Desc: "Continuez jusqu'à la redirection Pixiv vers la page callback.",
    tutorialStep3Title: "Ouvrir la console", tutorialStep3Desc: "Ouvrez DevTools/Console pour récupérer l'URL callback pixiv.",
    tutorialStep4Title: "Copier l'URL pixiv", tutorialStep4Desc: "Copiez l'URL callback contenant le code d'autorisation Pixiv.",
    tutorialStep5Title: "Coller URL / code", tutorialStep5Desc: "Collez l'URL callback ou le code dans l'entrée OAuth console.",
    tutorialStep6Title: "Échanger le token", tutorialStep6Desc: "Cliquez sur Échanger le token puis copiez access_token / refresh_token.",
    tutorialBackToConsole: "Retour à la console OAuth", tutorialFooterTag: "TUTORIEL",
    footerGithub: "Dépôt GitHub", footerOAuthEndpoint: "Endpoint OAuth Pixiv", footerTwitter: "Twitter/X"
  },
  es: {
    downloadsBrandTag: "DESCARGAR", downloadsHomeLink: "Inicio", downloadsTutorialLink: "Tutorial", downloadsConsoleLink: "Consola",
    downloadsTabDownloads: "Descargas", downloadsTabQuickCmd: "Comando rápido", downloadsFooterTag: "DESCARGAR",
    tutorialBrandTag: "TUTORIAL", tutorialHomeLink: "Inicio", tutorialConsoleLink: "Consola", tutorialDownloadsLink: "Descargas",
    tutorialTabStart: "Empezar", tutorialTabSteps: "Pasos del tutorial", tutorialTabTips: "Consejos",
    tutorialIntroTitle: "Empieza con el tutorial de Pixiv OAuth", tutorialIntroDesc: "Sigue los pasos desde login hasta intercambio de token en desktop y móvil.",
    tutorialStep1Title: "Abrir página de login", tutorialStep1Desc: "Abre la página de login de Pixiv desde la consola web.",
    tutorialStep2Title: "Continuar login", tutorialStep2Desc: "Continúa hasta que Pixiv redirija a la página callback.",
    tutorialStep3Title: "Abrir consola", tutorialStep3Desc: "Abre DevTools/Console para obtener la URL callback de pixiv.",
    tutorialStep4Title: "Copiar URL pixiv", tutorialStep4Desc: "Copia la URL callback que contiene el código de autorización de Pixiv.",
    tutorialStep5Title: "Pegar URL / código", tutorialStep5Desc: "Pega la URL callback o el código en el input de OAuth console.",
    tutorialStep6Title: "Intercambiar token", tutorialStep6Desc: "Haz clic en Intercambiar token y copia access_token / refresh_token.",
    tutorialBackToConsole: "Volver a OAuth Console", tutorialFooterTag: "TUTORIAL",
    footerGithub: "Repositorio GitHub", footerOAuthEndpoint: "Endpoint OAuth de Pixiv", footerTwitter: "Twitter/X"
  },
  ru: {
    downloadsBrandTag: "СКАЧАТЬ", downloadsHomeLink: "Главная", downloadsTutorialLink: "Туториал", downloadsConsoleLink: "Консоль",
    downloadsTabDownloads: "Загрузки", downloadsTabQuickCmd: "Быстрая команда", downloadsFooterTag: "СКАЧАТЬ",
    tutorialBrandTag: "ТУТОРИАЛ", tutorialHomeLink: "Главная", tutorialConsoleLink: "Консоль", tutorialDownloadsLink: "Загрузки",
    tutorialTabStart: "Начало", tutorialTabSteps: "Шаги", tutorialTabTips: "Советы",
    tutorialIntroTitle: "Начните с туториала Pixiv OAuth", tutorialIntroDesc: "Следуйте шагам от входа до обмена токена на ПК и мобильных.",
    tutorialStep1Title: "Открыть страницу входа", tutorialStep1Desc: "Откройте страницу входа Pixiv из веб-консоли.",
    tutorialStep2Title: "Продолжить вход", tutorialStep2Desc: "Продолжайте, пока Pixiv не перенаправит на callback.",
    tutorialStep3Title: "Открыть консоль", tutorialStep3Desc: "Откройте DevTools/Console, чтобы получить callback URL pixiv.",
    tutorialStep4Title: "Скопировать URL pixiv", tutorialStep4Desc: "Скопируйте callback URL с кодом авторизации Pixiv.",
    tutorialStep5Title: "Вставить URL / код", tutorialStep5Desc: "Вставьте callback URL или код в поле OAuth console.",
    tutorialStep6Title: "Обменять токен", tutorialStep6Desc: "Нажмите Обменять токен и скопируйте access_token / refresh_token.",
    tutorialBackToConsole: "Назад в OAuth Console", tutorialFooterTag: "ТУТОРИАЛ",
    footerGithub: "Репозиторий GitHub", footerOAuthEndpoint: "Pixiv OAuth Endpoint", footerTwitter: "Twitter/X"
  },
  pt: {
    downloadsBrandTag: "DOWNLOAD", downloadsHomeLink: "Início", downloadsTutorialLink: "Tutorial", downloadsConsoleLink: "Console",
    downloadsTabDownloads: "Downloads", downloadsTabQuickCmd: "Comando rápido", downloadsFooterTag: "DOWNLOAD",
    tutorialBrandTag: "TUTORIAL", tutorialHomeLink: "Início", tutorialConsoleLink: "Console", tutorialDownloadsLink: "Downloads",
    tutorialTabStart: "Começar", tutorialTabSteps: "Passos do tutorial", tutorialTabTips: "Dicas",
    tutorialIntroTitle: "Comece com o tutorial Pixiv OAuth", tutorialIntroDesc: "Siga os passos do login à troca de token no desktop e no mobile.",
    tutorialStep1Title: "Abrir página de login", tutorialStep1Desc: "Abra a página de login do Pixiv pelo console web.",
    tutorialStep2Title: "Continuar login", tutorialStep2Desc: "Continue até o Pixiv redirecionar para a página callback.",
    tutorialStep3Title: "Abrir console", tutorialStep3Desc: "Abra o DevTools/Console para capturar a URL callback pixiv.",
    tutorialStep4Title: "Copiar URL pixiv", tutorialStep4Desc: "Copie a URL callback com o código de autorização do Pixiv.",
    tutorialStep5Title: "Colar URL / código", tutorialStep5Desc: "Cole a URL callback ou código no campo do OAuth console.",
    tutorialStep6Title: "Trocar token", tutorialStep6Desc: "Clique em Trocar token e copie access_token / refresh_token.",
    tutorialBackToConsole: "Voltar para OAuth Console", tutorialFooterTag: "TUTORIAL",
    footerGithub: "Repositório GitHub", footerOAuthEndpoint: "Endpoint OAuth Pixiv", footerTwitter: "Twitter/X"
  },
  kr: {
    downloadsBrandTag: "다운로드", downloadsHomeLink: "홈", downloadsTutorialLink: "튜토리얼", downloadsConsoleLink: "콘솔",
    downloadsTabDownloads: "다운로드", downloadsTabQuickCmd: "빠른 명령", downloadsFooterTag: "다운로드",
    tutorialBrandTag: "튜토리얼", tutorialHomeLink: "홈", tutorialConsoleLink: "콘솔", tutorialDownloadsLink: "다운로드",
    tutorialTabStart: "시작", tutorialTabSteps: "튜토리얼 단계", tutorialTabTips: "팁",
    tutorialIntroTitle: "Pixiv OAuth 튜토리얼 시작하기", tutorialIntroDesc: "로그인부터 토큰 교환까지 순서대로 따라 하면 PC/모바일에서 더 쉽습니다.",
    tutorialStep1Title: "로그인 페이지 열기", tutorialStep1Desc: "웹 콘솔에서 Pixiv 로그인 페이지를 엽니다.",
    tutorialStep2Title: "로그인 계속", tutorialStep2Desc: "Pixiv가 콜백 페이지로 이동할 때까지 진행합니다.",
    tutorialStep3Title: "콘솔 열기", tutorialStep3Desc: "DevTools/Console에서 pixiv 콜백 URL을 가져옵니다.",
    tutorialStep4Title: "pixiv URL 복사", tutorialStep4Desc: "Pixiv 인증 코드가 포함된 콜백 URL을 복사합니다.",
    tutorialStep5Title: "URL / 코드 붙여넣기", tutorialStep5Desc: "OAuth 콘솔 입력칸에 콜백 URL 또는 코드를 붙여넣습니다.",
    tutorialStep6Title: "토큰 교환", tutorialStep6Desc: "토큰 교환을 누른 뒤 access_token / refresh_token을 복사합니다.",
    tutorialBackToConsole: "OAuth 콘솔로 돌아가기", tutorialFooterTag: "튜토리얼",
    footerGithub: "GitHub 저장소", footerOAuthEndpoint: "Pixiv OAuth 엔드포인트", footerTwitter: "Twitter/X"
  }
};

for (const [code, values] of Object.entries(EXTRA_I18N)) {
  I18N[code] = { ...(I18N[code] || {}), ...values };
}

const EXTRA_SHOWCASE_I18N = {
  pl: {
    tutorialCtaText: "Potrzebujesz wizualnego przewodnika krok po kroku?", tutorialCtaBtnLabel: "Otwórz stronę poradnika",
    windowsPreviewBadge: "Podgląd aplikacji Windows", windowsPreviewTitle: "Zobacz aplikację Pixiv OAuth na Windows w akcji",
    windowsPreviewDesc: "Krótki podgląd przepływu aplikacji Windows od logowania do wygenerowania tokena.",
    windowsVideoFallback: "Twoja przeglądarka nie obsługuje wideo HTML5.",
    cliPreviewBadge: "Podgląd CLI", cliPreviewTitle: "Podgląd wyjścia CLI Pixiv OAuth",
    cliPreviewDesc: "Symulacja wyjścia CLI, aby szybko zrozumieć logowanie, odczyt kodu i wynik tokena.",
    cliFigureLabel: "Rys. CLI — Podgląd tokena Pixiv OAuth", cliToggleMore: "Pokaż więcej", cliToggleLess: "Pokaż mniej",
    downloadsCtaText: "Pobieranie i szybkie komendy są teraz na osobnej stronie.", downloadsCtaBtnLabel: "Otwórz stronę pobierania"
  },
  zh: {
    tutorialCtaText: "需要可视化分步指南吗？", tutorialCtaBtnLabel: "打开教程页面",
    windowsPreviewBadge: "Windows 应用预览", windowsPreviewTitle: "查看 Pixiv OAuth Windows 应用演示",
    windowsPreviewDesc: "简短预览 Windows 应用从登录到成功生成令牌的流程。",
    windowsVideoFallback: "您的浏览器不支持 HTML5 视频。",
    cliPreviewBadge: "CLI 预览", cliPreviewTitle: "预览 Pixiv OAuth CLI 输出",
    cliPreviewDesc: "CLI 输出模拟，帮助快速理解登录、代码解析和令牌结果。",
    cliFigureLabel: "图：CLI — Pixiv OAuth 令牌预览", cliToggleMore: "查看更多", cliToggleLess: "收起",
    downloadsCtaText: "下载与快速命令已移动到专用页面。", downloadsCtaBtnLabel: "打开下载页面"
  },
  jp: {
    tutorialCtaText: "ステップごとのビジュアルガイドが必要ですか？", tutorialCtaBtnLabel: "チュートリアルページを開く",
    windowsPreviewBadge: "Windowsアプリプレビュー", windowsPreviewTitle: "Pixiv OAuth Windowsアプリの動作を見る",
    windowsPreviewDesc: "ログインからトークン生成までのWindowsアプリの流れを短く紹介します。",
    windowsVideoFallback: "お使いのブラウザはHTML5動画に対応していません。",
    cliPreviewBadge: "CLIプレビュー", cliPreviewTitle: "Pixiv OAuth CLI 出力プレビュー",
    cliPreviewDesc: "ログイン、コード解析、トークン結果を素早く確認できるCLI出力シミュレーション。",
    cliFigureLabel: "図: CLI — Pixiv OAuth トークンプレビュー", cliToggleMore: "もっと見る", cliToggleLess: "閉じる",
    downloadsCtaText: "ダウンロードとクイックコマンドは専用ページに移動しました。", downloadsCtaBtnLabel: "ダウンロードページを開く"
  },
  de: {
    tutorialCtaText: "Brauchst du eine visuelle Schritt-für-Schritt-Anleitung?", tutorialCtaBtnLabel: "Tutorial-Seite öffnen",
    windowsPreviewBadge: "Windows-App-Vorschau", windowsPreviewTitle: "Pixiv OAuth Windows-App in Aktion ansehen",
    windowsPreviewDesc: "Kurze Vorschau des Windows-App-Ablaufs vom Login bis zur erfolgreichen Token-Erstellung.",
    windowsVideoFallback: "Dein Browser unterstützt kein HTML5-Video.",
    cliPreviewBadge: "CLI-Vorschau", cliPreviewTitle: "Pixiv OAuth CLI-Ausgabe ansehen",
    cliPreviewDesc: "CLI-Ausgabe-Simulation, um Login, Code-Erkennung und Token-Ergebnis schnell zu verstehen.",
    cliFigureLabel: "Abb. CLI — Pixiv OAuth Token-Vorschau", cliToggleMore: "Mehr anzeigen", cliToggleLess: "Weniger anzeigen",
    downloadsCtaText: "Downloads und Schnellbefehle sind jetzt auf einer eigenen Seite.", downloadsCtaBtnLabel: "Download-Seite öffnen"
  },
  fr: {
    tutorialCtaText: "Besoin d'un guide visuel étape par étape ?", tutorialCtaBtnLabel: "Ouvrir la page tutoriel",
    windowsPreviewBadge: "Aperçu app Windows", windowsPreviewTitle: "Voir l'application Windows Pixiv OAuth en action",
    windowsPreviewDesc: "Aperçu rapide du flux Windows, de la connexion à la génération réussie du token.",
    windowsVideoFallback: "Votre navigateur ne prend pas en charge la vidéo HTML5.",
    cliPreviewBadge: "Aperçu CLI", cliPreviewTitle: "Aperçu de la sortie CLI Pixiv OAuth",
    cliPreviewDesc: "Simulation de sortie CLI pour comprendre rapidement connexion, lecture du code et résultat token.",
    cliFigureLabel: "Fig. CLI — Aperçu du token Pixiv OAuth", cliToggleMore: "Voir plus", cliToggleLess: "Voir moins",
    downloadsCtaText: "Téléchargements et commandes rapides sont maintenant sur une page dédiée.", downloadsCtaBtnLabel: "Ouvrir la page de téléchargement"
  },
  es: {
    tutorialCtaText: "¿Necesitas guía visual paso a paso?", tutorialCtaBtnLabel: "Abrir página de tutorial",
    windowsPreviewBadge: "Vista previa app Windows", windowsPreviewTitle: "Ver Pixiv OAuth Windows App en acción",
    windowsPreviewDesc: "Vista previa corta del flujo en Windows desde login hasta token generado.",
    windowsVideoFallback: "Tu navegador no soporta video HTML5.",
    cliPreviewBadge: "Vista previa CLI", cliPreviewTitle: "Vista previa de salida CLI Pixiv OAuth",
    cliPreviewDesc: "Simulación de salida CLI para entender login, lectura de código y resultado de token.",
    cliFigureLabel: "Fig. CLI — Vista previa del token Pixiv OAuth", cliToggleMore: "Ver más", cliToggleLess: "Ver menos",
    downloadsCtaText: "Descargas y comandos rápidos ahora están en una página dedicada.", downloadsCtaBtnLabel: "Abrir página de descargas"
  },
  ru: {
    tutorialCtaText: "Нужна пошаговая визуальная инструкция?", tutorialCtaBtnLabel: "Открыть страницу туториала",
    windowsPreviewBadge: "Превью Windows-приложения", windowsPreviewTitle: "Посмотрите Pixiv OAuth Windows App в действии",
    windowsPreviewDesc: "Короткий просмотр процесса в Windows от входа до успешного получения токена.",
    windowsVideoFallback: "Ваш браузер не поддерживает HTML5-видео.",
    cliPreviewBadge: "Превью CLI", cliPreviewTitle: "Превью вывода CLI Pixiv OAuth",
    cliPreviewDesc: "Симуляция вывода CLI для быстрого понимания логина, чтения кода и результата токена.",
    cliFigureLabel: "Рис. CLI — Превью токена Pixiv OAuth", cliToggleMore: "Показать больше", cliToggleLess: "Показать меньше",
    downloadsCtaText: "Загрузки и быстрые команды теперь на отдельной странице.", downloadsCtaBtnLabel: "Открыть страницу загрузок"
  },
  pt: {
    tutorialCtaText: "Precisa de um guia visual passo a passo?", tutorialCtaBtnLabel: "Abrir página do tutorial",
    windowsPreviewBadge: "Preview do app Windows", windowsPreviewTitle: "Veja o app Windows Pixiv OAuth em ação",
    windowsPreviewDesc: "Preview curto do fluxo no Windows, do login até a geração do token.",
    windowsVideoFallback: "Seu navegador não suporta vídeo HTML5.",
    cliPreviewBadge: "Preview CLI", cliPreviewTitle: "Preview da saída CLI Pixiv OAuth",
    cliPreviewDesc: "Simulação da saída CLI para entender login, leitura do código e resultado do token.",
    cliFigureLabel: "Fig. CLI — Preview do token Pixiv OAuth", cliToggleMore: "Ver mais", cliToggleLess: "Ver menos",
    downloadsCtaText: "Downloads e comandos rápidos agora estão em uma página dedicada.", downloadsCtaBtnLabel: "Abrir página de downloads"
  },
  kr: {
    tutorialCtaText: "단계별 시각 가이드가 필요하신가요?", tutorialCtaBtnLabel: "튜토리얼 페이지 열기",
    windowsPreviewBadge: "Windows 앱 미리보기", windowsPreviewTitle: "Pixiv OAuth Windows 앱 실행 보기",
    windowsPreviewDesc: "로그인부터 토큰 생성 완료까지 Windows 앱 흐름을 짧게 보여줍니다.",
    windowsVideoFallback: "브라우저가 HTML5 비디오를 지원하지 않습니다.",
    cliPreviewBadge: "CLI 미리보기", cliPreviewTitle: "Pixiv OAuth CLI 출력 미리보기",
    cliPreviewDesc: "로그인, 코드 읽기, 토큰 결과를 빠르게 이해할 수 있는 CLI 출력 시뮬레이션입니다.",
    cliFigureLabel: "그림 CLI — Pixiv OAuth 토큰 미리보기", cliToggleMore: "더 보기", cliToggleLess: "간단히 보기",
    downloadsCtaText: "다운로드와 빠른 명령은 이제 전용 페이지에 있습니다.", downloadsCtaBtnLabel: "다운로드 페이지 열기"
  }
};

for (const [code, values] of Object.entries(EXTRA_SHOWCASE_I18N)) {
  I18N[code] = { ...(I18N[code] || {}), ...values };
}

for (const code of LANG_ORDER) I18N[code] = { ...I18N.en, ...(I18N[code] || {}) };
let currentLang = "en";

const FLAG_CLASS = { en: "fi-gb", pl: "fi-pl", zh: "fi-cn", jp: "fi-jp", de: "fi-de", fr: "fi-fr", es: "fi-es", ru: "fi-ru", pt: "fi-pt", id: "fi-id", kr: "fi-kr" };
const LANG_NAME = { en: "English", pl: "Polski", zh: "中文", jp: "日本語", de: "Deutsch", fr: "Français", es: "Español", ru: "Русский", pt: "Português", id: "Indonesia", kr: "한국어" };

function t(key) {
  return (I18N[currentLang] && I18N[currentLang][key]) || I18N.en[key] || key;
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
    const res = await fetch(RELEASE_API, { headers: { Accept: "application/vnd.github+json" } });
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
  if (ps) ps.textContent = `$guiPortable = "${guiPortable}"
$cliPortable = "${cliPortable}"
$guiSetup = "${guiSetup}"
$cliSetup = "${cliSetup}"
Invoke-WebRequest $guiPortable -OutFile "Pixiv OAuth GUi (Portable).exe"
Invoke-WebRequest $cliPortable -OutFile "Pixiv OAuth CLi (Portable).exe"
Invoke-WebRequest $guiSetup -OutFile "Pixiv OAuth GUi Setup.exe"
Invoke-WebRequest $cliSetup -OutFile "Pixiv OAuth CLi Setup.exe"
`;

  if (cmd) cmd.textContent = `curl -L "${guiPortable}" -o "Pixiv OAuth GUi (Portable).exe"
curl -L "${cliPortable}" -o "Pixiv OAuth CLi (Portable).exe"
curl -L "${guiSetup}" -o "Pixiv OAuth GUi Setup.exe"
curl -L "${cliSetup}" -o "Pixiv OAuth CLi Setup.exe"
`;

  if (pip) pip.textContent = `python -m pip install -r requirements.txt
python -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"`;
}

async function copyText(text, okMessage) {
  await navigator.clipboard.writeText(text);
  if (output) output.textContent = okMessage;
}

function updateLangFlag() {
  const el = q("langFlag");
  const current = q("langCurrent");
  if (el) el.className = `fi ${FLAG_CLASS[currentLang] || "fi-gb"}`;
  if (current) current.textContent = LANG_NAME[currentLang] || "English";

  document.querySelectorAll("#langMenu li").forEach((li) => {
    li.classList.toggle("active", li.dataset.lang === currentLang);
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
    const open = menu.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  });

  menu.querySelectorAll("li").forEach((item) => {
    item.tabIndex = 0;
    const selectLang = () => {
      currentLang = item.dataset.lang;
      localStorage.setItem("pixiv_lang", currentLang);
      document.documentElement.lang = currentLang === "jp" ? "ja" : currentLang;
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
    toggle.textContent = expanded ? t("cliToggleLess") : t("cliToggleMore");
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
    navConsole: "navConsole",
    navDownloads: "navDownloads",
    navQuickCmd: "navQuickCmd",
    navTutorialLabel: "navTutorial",
    tutorialTitle: "tutorialTitle",
    tutorialDesc: "tutorialDesc",
    tutorialCtaText: "tutorialCtaText",
    tutorialCtaBtnLabel: "tutorialCtaBtnLabel",
    windowsPreviewBadge: "windowsPreviewBadge",
    windowsPreviewTitle: "windowsPreviewTitle",
    windowsPreviewDesc: "windowsPreviewDesc",
    windowsVideoFallback: "windowsVideoFallback",
    cliPreviewBadge: "cliPreviewBadge",
    cliPreviewTitle: "cliPreviewTitle",
    cliPreviewDesc: "cliPreviewDesc",
    cliFigureLabel: "cliFigureLabel",
    downloadsCtaText: "downloadsCtaText",
    downloadsCtaBtnLabel: "downloadsCtaBtnLabel",
    downloadsBrandTag: "downloadsBrandTag",
    downloadsHomeLink: "downloadsHomeLink",
    downloadsTutorialLink: "downloadsTutorialLink",
    downloadsConsoleLink: "downloadsConsoleLink",
    downloadsTabDownloads: "downloadsTabDownloads",
    downloadsTabQuickCmd: "downloadsTabQuickCmd",
    downloadsFooterTag: "downloadsFooterTag",
    tutorialBrandTag: "tutorialBrandTag",
    tutorialHomeLink: "tutorialHomeLink",
    tutorialConsoleLink: "tutorialConsoleLink",
    tutorialDownloadsLink: "tutorialDownloadsLink",
    tutorialTabStart: "tutorialTabStart",
    tutorialTabSteps: "tutorialTabSteps",
    tutorialTabTips: "tutorialTabTips",
    tutorialIntroTitle: "tutorialIntroTitle",
    tutorialIntroDesc: "tutorialIntroDesc",
    tutorialStepsTitle: "tutorialTabSteps",
    tutorialStep1Title: "tutorialStep1Title",
    tutorialStep1Desc: "tutorialStep1Desc",
    tutorialStep2Title: "tutorialStep2Title",
    tutorialStep2Desc: "tutorialStep2Desc",
    tutorialStep3Title: "tutorialStep3Title",
    tutorialStep3Desc: "tutorialStep3Desc",
    tutorialStep4Title: "tutorialStep4Title",
    tutorialStep4Desc: "tutorialStep4Desc",
    tutorialStep5Title: "tutorialStep5Title",
    tutorialStep5Desc: "tutorialStep5Desc",
    tutorialStep6Title: "tutorialStep6Title",
    tutorialStep6Desc: "tutorialStep6Desc",
    tutorialBackToConsole: "tutorialBackToConsole",
    tutorialFooterTag: "tutorialFooterTag",
    footerGithub: "footerGithub",
    footerOAuthEndpoint: "footerOAuthEndpoint",
    footerPython: "footerPython",
    footerPyInstaller: "footerPyInstaller",
    footerVercel: "footerVercel",
    footerTikTok: "footerTikTok",
    footerTwitter: "footerTwitter",
    footerDeveloperName: "footerDeveloperName"
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
    const isExpanded = q("cliPreviewBox")?.classList.contains("expanded");
    cliToggleBtn.textContent = isExpanded ? t("cliToggleLess") : t("cliToggleMore");
  }
  updateLangFlag();
}

function b64Url(bytes) {
  return btoa(String.fromCharCode(...bytes)).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

async function createPkce() {
  const arr = crypto.getRandomValues(new Uint8Array(32));
  codeVerifier = b64Url(arr);
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(codeVerifier));
  return { codeVerifier, codeChallenge: b64Url([...new Uint8Array(digest)]) };
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
    if ((raw && raw.toLowerCase().includes("<html")) || raw.startsWith("The page")) throw new Error(t("errApiHtml"));
    throw new Error(raw || "Unknown API response");
  }

  if (!res.ok) throw new Error(data.error || JSON.stringify(data));
  return data;
}

bindClick("openLoginBtn", async () => {
  const { codeChallenge } = await createPkce();
  const url = `${LOGIN_URL}?${new URLSearchParams({ code_challenge: codeChallenge, code_challenge_method: "S256", client: "pixiv-android" })}`;
  window.open(url, "_blank", "noopener");
  if (output) output.textContent = t("opened");
});

bindClick("exchangeBtn", async () => {
  try {
    const code = parseCode(q("inputCode").value);
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

bindClick("copyPsBtn", async () => { const el = q("psCmd"); if (el) await copyText(el.textContent, t("copiedPs")); });
bindClick("copyCmdBtn", async () => { const el = q("cmdCmd"); if (el) await copyText(el.textContent, t("copiedCmd")); });
bindClick("copyPipBtn", async () => { const el = q("pipCmd"); if (el) await copyText(el.textContent, t("copiedPip")); });

(async function init() {
  const saved = localStorage.getItem("pixiv_lang");
  if (saved && LANG_ORDER.includes(saved)) currentLang = saved;

  document.documentElement.lang = currentLang === "jp" ? "ja" : currentLang;

  setupLanguageMenu();
  setupCliPreviewToggle();
  applyLang();
  await hydrateReleaseAssets();
})();
