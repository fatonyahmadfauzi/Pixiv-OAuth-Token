const CLIENT_ID = "MOBrBDS8blbauoSck0ZfDbtuzpyT";
const REDIRECT_URI = "https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback";
const LOGIN_URL = "https://app-api.pixiv.net/web/v1/login";
const REPO_BASE = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token";
const RELEASE_BASE = `${REPO_BASE}/releases/latest/download`;
const RELEASE_API = "/api/github?path=repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest";
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
    subtitle: "Toolkit to generate and refresh Pixiv OAuth tokens via CLI, GUI, and Web with a secure PKCE flow.",
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
    contact: "Social",
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
    navDownloads: "Download",
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
    cliPreviewFigure: "Fig. CLI — Pixiv OAuth Token Preview",
    downloadsDedicatedDesc: "Downloads & quick commands setup instructions.",
    tutorialStep1Title: "Open Login Page",
    tutorialStep1Desc: "Open the Pixiv login page from the web console tool.",
    tutorialStep2Title: "Continue Login",
    tutorialStep2Desc: "Continue Pixiv account login until redirected to callback.",
    tutorialStep3Title: "Open Console",
    tutorialStep3Desc: "Open devtools/console to capture the Pixiv callback URL.",
    tutorialStep4Title: "Copy pixiv URL",
    tutorialStep4Desc: "Copy the callback URL containing the Pixiv authorization code.",
    tutorialStep5Title: "Paste URL / Code",
    tutorialStep5Desc: "Paste the callback URL or code into the OAuth console input.",
    tutorialStep6Title: "Exchange Token",
    tutorialStep6Desc: "Click Exchange Token, then copy access_token / refresh_token.",
    errApiNotFound: "API endpoint not found (404). Deploy /api/token on Vercel first.",
    errApiHtml: "Server returned HTML instead of JSON. Check deployment routes/config.",
    copiedPs: "PowerShell command copied.",
    copiedCmd: "CMD command copied.",
    copiedPip: "pip command copied.",
    showMore: "See More",
    showLess: "Show Less",
    footerProductTitle: "Product",
    footerHomeLink: "Homepage",
    footerDownloadLink: "Downloads",
    footerTutorialLink: "Tutorial",
    footerSourceLink: "Source Code",
    footerResourceTitle: "Resources & Docs",
    footerDocsLink: "Documentation",
    footerPixivLink: "Pixiv OAuth Endpoint",
    footerPythonLink: "Python 3.11+",
    footerVercelLink: "Deployed on Vercel",
    footerSupportTitle: "Support",
    footerIssueLink: "Report an Issue",
    footerDiscussLink: "Discussions",
    footerDevLink: "Fatony Ahmad Fauzi",
    dlCatAgent: "AGENTS",
    dlSidebarWin: "Windows",
    dlCatSdk: "SDKS",
    dlSidebarPy: "Python",
    dlBadgeWin: "Agent",
    dlTitleWin: "Windows",
    dlInstallWin: "Installation",
    dlTabDl: "Download",
    dlTabPs: "PowerShell",
    dlTabCmd: "CMD",
    dlDescWin1: "Download a standalone executable with zero run time dependencies. Don’t know your architecture? ",
    dlDescWinHelp: "Help me find it.",
    dlDescPs: "Install via PowerShell with the following command:",
    dlDescCmd: "Install via CMD with the following command:",
    dlBadgePy: "SDK",
    dlTitlePy: "Python",
    dlInstallPy: "Installation",
    dlPyClone: "Clone repository",
    dlPyOpen: "Open project folder",
    dlPyVenv: "Optional: Create virtual environment",
    dlPyReqs: "Install requirements.txt",
    dlPyRun: "Run CLI app",
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
    contact: "Social",
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
    tutorialTabStart: "Start",
    tutorialTabSteps: "Kroki samouczka",
    tutorialTabTips: "Wskazówki",
    tutorialPageTitle: "Rozpocznij samouczek Pixiv OAuth",
    tutorialPageDesc: "Wykonaj kolejne kroki od logowania do wymiany tokena, aby proces był łatwiejszy na komputerze i telefonie.",
    tutorialStepsTitle: "Kroki samouczka",
    tutorialBackBtn: "Wróć do konsoli OAuth",
    needVisualGuide: "Potrzebujesz wizualnego przewodnika krok po kroku?",
    openTutorialPage: "Otwórz stronę samouczka",
    windowsPreviewBadge: "Podgląd aplikacji Windows",
    windowsPreviewTitle: "Zobacz Pixiv OAuth Windows App w akcji",
    windowsPreviewDesc: "Ten krótki podgląd pokazuje przepływ aplikacji Windows od logowania do pomyślnego wygenerowania tokena.",
    cliPreviewBadge: "Podgląd CLI",
    cliPreviewTitle: "Podgląd danych wyjściowych Pixiv OAuth CLI",
    cliPreviewDesc: "Symulacja outputu CLI, która pokazuje logowanie, odczyt kodu i wynik tokena w skrócie.",
    openDownloadsPage: "Otwórz stronę pobierania",
    cliPreviewFigure: "Rys. CLI — Podgląd tokena Pixiv OAuth",
    downloadsDedicatedDesc: "Pobieranie i szybkie komendy są teraz na osobnej stronie.",
    tutorialStep1Title: "Otwórz stronę logowania",
    tutorialStep1Desc: "Otwórz stronę logowania Pixiv z webowego narzędzia konsoli.",
    tutorialStep2Title: "Kontynuuj logowanie",
    tutorialStep2Desc: "Kontynuuj logowanie do konta Pixiv, aż nastąpi przekierowanie do callback.",
    tutorialStep3Title: "Otwórz konsolę",
    tutorialStep3Desc: "Otwórz devtools/console, aby pobrać URL callback Pixiv.",
    tutorialStep4Title: "Skopiuj URL pixiv",
    tutorialStep4Desc: "Skopiuj URL callback zawierający kod autoryzacji Pixiv.",
    tutorialStep5Title: "Wklej URL / kod",
    tutorialStep5Desc: "Wklej URL callback lub kod do pola wejściowego konsoli OAuth.",
    tutorialStep6Title: "Wymień token",
    tutorialStep6Desc: "Kliknij Wymień token, a następnie skopiuj access_token / refresh_token.",
    errApiNotFound: "Nie znaleziono endpointu API (404). Najpierw wdroż /api/token na Vercel.",
    errApiHtml: "Serwer zwrócił HTML zamiast JSON. Sprawdź trasy wdrożenia/konfigurację.",
    copiedPs: "Polecenie PowerShell skopiowane.",
    copiedCmd: "Polecenie CMD skopiowane.",
    copiedPip: "Polecenie pip skopiowane.",
    showMore: "Pokaż więcej",
    showLess: "Pokaż mniej",
    footerProductTitle: "Produkt",
    footerHomeLink: "Strona główna",
    footerDownloadLink: "Pobieranie",
    footerTutorialLink: "Samouczek",
    footerSourceLink: "Kod źródłowy",
    footerResourceTitle: "Zasoby i dokumentacja",
    footerDocsLink: "Dokumentacja",
    footerPixivLink: "Punkt końcowy Pixiv",
    footerPythonLink: "Python 3.11+",
    footerVercelLink: "Wdrożono na Vercel",
    footerSupportTitle: "Wsparcie",
    footerIssueLink: "Zgłoś problem",
    footerDiscussLink: "Dyskusje",
    footerDevLink: "Fatony Ahmad Fauzi",
    dlCatAgent: "AGENCI",
    dlSidebarWin: "Windows",
    dlCatSdk: "SDK",
    dlSidebarPy: "Python",
    dlBadgeWin: "Agent",
    dlTitleWin: "Windows",
    dlInstallWin: "Instalacja",
    dlTabDl: "Pobierz",
    dlTabPs: "PowerShell",
    dlTabCmd: "CMD",
    dlDescWin1: "Pobierz samodzielny plik wykonywalny bez zależności. Nie znasz swojej architektury? ",
    dlDescWinHelp: "Pomóż mi ją znaleźć.",
    dlDescPs: "Zainstaluj przez PowerShell:",
    dlDescCmd: "Zainstaluj przez CMD:",
    dlBadgePy: "SDK",
    dlTitlePy: "Python",
    dlInstallPy: "Instalacja",
    dlPyClone: "Sklonuj repozytorium",
    dlPyOpen: "Otwórz folder projektu",
    dlPyVenv: "Opcjonalnie: Utwórz środowisko wirtualne",
    dlPyReqs: "Zainstaluj requirements.txt",
    dlPyRun: "Uruchom aplikację CLI",
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
    contact: "Social",
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
    tutorialTabStart: "开始",
    tutorialTabSteps: "教程步骤",
    tutorialTabTips: "提示",
    tutorialPageTitle: "开始使用 Pixiv OAuth 教程",
    tutorialPageDesc: "按顺序完成从登录到交换令牌的步骤，让桌面和移动端都更容易操作。",
    tutorialStepsTitle: "教程步骤",
    tutorialBackBtn: "返回 OAuth 控制台",
    needVisualGuide: "需要可视化的分步指南吗？",
    openTutorialPage: "打开教程页面",
    windowsPreviewBadge: "Windows 应用预览",
    windowsPreviewTitle: "查看 Pixiv OAuth Windows 应用实际效果",
    windowsPreviewDesc: "这个简短预览展示了 Windows 应用从登录到成功生成令牌的流程。",
    cliPreviewBadge: "CLI 预览",
    cliPreviewTitle: "预览 Pixiv OAuth CLI 输出",
    cliPreviewDesc: "通过 CLI 输出模拟，快速查看登录流程、代码解析和令牌结果。",
    openDownloadsPage: "打开下载页面",
    cliPreviewFigure: "图：CLI — Pixiv OAuth 令牌预览",
    downloadsDedicatedDesc: "下载与快速命令现已移动到独立页面。",
    tutorialStep1Title: "打开登录页面",
    tutorialStep1Desc: "从 Web 控制台工具打开 Pixiv 登录页面。",
    tutorialStep2Title: "继续登录",
    tutorialStep2Desc: "继续 Pixiv 账号登录，直到跳转到回调页面。",
    tutorialStep3Title: "打开控制台",
    tutorialStep3Desc: "打开开发者工具/控制台以获取 Pixiv 回调 URL。",
    tutorialStep4Title: "复制 pixiv URL",
    tutorialStep4Desc: "复制包含 Pixiv 授权码的回调 URL。",
    tutorialStep5Title: "粘贴 URL / 代码",
    tutorialStep5Desc: "将回调 URL 或代码粘贴到 OAuth 控制台输入框中。",
    tutorialStep6Title: "交换令牌",
    tutorialStep6Desc: "点击交换令牌，然后复制 access_token / refresh_token。",
    errApiNotFound: "未找到 API 端点（404）。请先将 /api/token 部署到 Vercel。",
    errApiHtml: "服务器返回的是 HTML 而不是 JSON。请检查部署路由/配置。",
    copiedPs: "PowerShell 命令已复制。",
    copiedCmd: "CMD 命令已复制。",
    copiedPip: "pip 命令已复制。",
    showMore: "查看更多",
    showLess: "收起",
    footerProductTitle: "产品",
    footerHomeLink: "主页",
    footerDownloadLink: "下载",
    footerTutorialLink: "教程",
    footerSourceLink: "源代码",
    footerResourceTitle: "资源与文档",
    footerDocsLink: "文档",
    footerPixivLink: "Pixiv OAuth",
    footerPythonLink: "Python 3.11+",
    footerVercelLink: "部署在 Vercel 上",
    footerSupportTitle: "支持",
    footerIssueLink: "报告问题",
    footerDiscussLink: "讨论区",
    footerDevLink: "Fatony Ahmad Fauzi",
    dlCatAgent: "代理",
    dlSidebarWin: "Windows",
    dlCatSdk: "SDK",
    dlSidebarPy: "Python",
    dlBadgeWin: "代理",
    dlTitleWin: "Windows",
    dlInstallWin: "安装",
    dlTabDl: "下载",
    dlTabPs: "PowerShell",
    dlTabCmd: "CMD",
    dlDescWin1: "下载零运行时依赖的独立可执行文件。不知道您的系统架构？ ",
    dlDescWinHelp: "帮我查找。",
    dlDescPs: "通过 PowerShell 使用以下命令安装：",
    dlDescCmd: "通过 CMD 使用以下命令安装：",
    dlBadgePy: "SDK",
    dlTitlePy: "Python",
    dlInstallPy: "安装",
    dlPyClone: "克隆代码库",
    dlPyOpen: "打开项目文件夹",
    dlPyVenv: "可选：创建虚拟环境",
    dlPyReqs: "安装 requirements.txt",
    dlPyRun: "运行 CLI 应用",
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
    contact: "Social",
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
    tutorialTabStart: "はじめに",
    tutorialTabSteps: "チュートリアル手順",
    tutorialTabTips: "ヒント",
    tutorialPageTitle: "Pixiv OAuth チュートリアルを始める",
    tutorialPageDesc: "ログインからトークン交換まで順番に進めることで、PC・モバイルの両方で分かりやすく操作できます。",
    tutorialStepsTitle: "チュートリアル手順",
    tutorialBackBtn: "OAuth コンソールに戻る",
    needVisualGuide: "ステップごとのビジュアルガイドが必要ですか？",
    openTutorialPage: "チュートリアルページを開く",
    windowsPreviewBadge: "Windows アプリ プレビュー",
    windowsPreviewTitle: "Pixiv OAuth Windows アプリの動作を見る",
    windowsPreviewDesc: "この短いプレビューでは、Windows アプリでログインからトークン生成成功までの流れを確認できます。",
    cliPreviewBadge: "CLI プレビュー",
    cliPreviewTitle: "Pixiv OAuth CLI 出力プレビュー",
    cliPreviewDesc: "CLI 出力のシミュレーションで、ログインフロー、コード解析、トークン結果を簡潔に確認できます。",
    openDownloadsPage: "ダウンロードページを開く",
    cliPreviewFigure: "図: CLI — Pixiv OAuth トークンプレビュー",
    downloadsDedicatedDesc: "ダウンロードとクイックコマンドは専用ページに移動しました。",
    tutorialStep1Title: "ログインページを開く",
    tutorialStep1Desc: "Web コンソールツールから Pixiv のログインページを開きます。",
    tutorialStep2Title: "ログインを続行",
    tutorialStep2Desc: "Pixiv アカウントのログインを続け、コールバックにリダイレクトされるまで進めます。",
    tutorialStep3Title: "コンソールを開く",
    tutorialStep3Desc: "Pixiv のコールバック URL を取得するために devtools/console を開きます。",
    tutorialStep4Title: "pixiv URL をコピー",
    tutorialStep4Desc: "Pixiv の認可コードを含むコールバック URL をコピーします。",
    tutorialStep5Title: "URL / コードを貼り付け",
    tutorialStep5Desc: "コールバック URL またはコードを OAuth コンソール入力欄に貼り付けます。",
    tutorialStep6Title: "トークンを取得",
    tutorialStep6Desc: "トークン取得をクリックし、access_token / refresh_token をコピーします。",
    errApiNotFound: "API エンドポイントが見つかりません（404）。まず /api/token を Vercel にデプロイしてください。",
    errApiHtml: "サーバーが JSON ではなく HTML を返しました。デプロイルート/設定を確認してください。",
    copiedPs: "PowerShell コマンドをコピーしました。",
    copiedCmd: "CMD コマンドをコピーしました。",
    copiedPip: "pip コマンドをコピーしました。",
    showMore: "もっと見る",
    showLess: "閉じる",
    footerProductTitle: "製品",
    footerHomeLink: "ホームページ",
    footerDownloadLink: "ダウンロード",
    footerTutorialLink: "チュートリアル",
    footerSourceLink: "ソースコード",
    footerResourceTitle: "リソースとドキュメント",
    footerDocsLink: "ドキュメント",
    footerPixivLink: "Pixiv OAuth",
    footerPythonLink: "Python 3.11+",
    footerVercelLink: "Vercel でデプロイ",
    footerSupportTitle: "サポート",
    footerIssueLink: "問題を報告",
    footerDiscussLink: "ディスカッション",
    footerDevLink: "Fatony Ahmad Fauzi",
    dlCatAgent: "エージェント",
    dlSidebarWin: "Windows",
    dlCatSdk: "SDK",
    dlSidebarPy: "Python",
    dlBadgeWin: "エージェント",
    dlTitleWin: "Windows",
    dlInstallWin: "インストール",
    dlTabDl: "ダウンロード",
    dlTabPs: "PowerShell",
    dlTabCmd: "CMD",
    dlDescWin1: "ランタイム依存関係ゼロのスタンドアロン実行可能ファイルをダウンロードします。アーキテクチャが不明ですか？ ",
    dlDescWinHelp: "見つけるのを手伝ってください。",
    dlDescPs: "PowerShell 経由でインストールします：",
    dlDescCmd: "CMD 経由でインストールします：",
    dlBadgePy: "SDK",
    dlTitlePy: "Python",
    dlInstallPy: "インストール",
    dlPyClone: "リポジトリのクローン",
    dlPyOpen: "プロジェクトフォルダを開く",
    dlPyVenv: "オプション：仮想環境の作成",
    dlPyReqs: "requirements.txt のインストール",
    dlPyRun: "CLI アプリを実行",
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
    contact: "Social",
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
    navDownloads: "Download",
    navQuickCmd: "Schnellbefehl",
    navTutorial: "Tutorial",
    tutorialTitle: "Tutorial",
    tutorialDesc: "Füllen Sie diesen Abschnitt mit geordneten Screenshots, um Nutzer vom Login bis zum Token-Austausch zu führen.",
    tutorialTabStart: "Erste Schritte",
    tutorialTabSteps: "Tutorial-Schritte",
    tutorialTabTips: "Tipps",
    tutorialPageTitle: "Mit dem Pixiv OAuth Tutorial starten",
    tutorialPageDesc: "Folge den Schritten vom Login bis zum Token-Austausch, damit der Ablauf auf Desktop und Mobile leichter ist.",
    tutorialStepsTitle: "Tutorial-Schritte",
    tutorialBackBtn: "Zurück zur OAuth-Konsole",
    needVisualGuide: "Brauchst du eine visuelle Schritt-für-Schritt-Anleitung?",
    openTutorialPage: "Tutorial-Seite öffnen",
    windowsPreviewBadge: "Windows-App-Vorschau",
    windowsPreviewTitle: "Pixiv OAuth Windows App in Aktion ansehen",
    windowsPreviewDesc: "Diese kurze Vorschau zeigt den Ablauf der Windows-App vom Login bis zur erfolgreichen Token-Generierung.",
    cliPreviewBadge: "CLI-Vorschau",
    cliPreviewTitle: "Pixiv OAuth CLI-Ausgabe ansehen",
    cliPreviewDesc: "CLI-Ausgabe-Simulation, um Login-Flow, Code-Auslese und Token-Ergebnis kompakt zu zeigen.",
    openDownloadsPage: "Download-Seite öffnen",
    cliPreviewFigure: "Abb. CLI — Pixiv OAuth Token-Vorschau",
    downloadsDedicatedDesc: "Downloads und schnelle Befehle sind jetzt auf einer eigenen Seite.",
    tutorialStep1Title: "Login-Seite öffnen",
    tutorialStep1Desc: "Öffne die Pixiv-Login-Seite aus dem Web-Tool der Konsole.",
    tutorialStep2Title: "Login fortsetzen",
    tutorialStep2Desc: "Setze den Pixiv-Login fort, bis zur Callback-Seite weitergeleitet wird.",
    tutorialStep3Title: "Konsole öffnen",
    tutorialStep3Desc: "Öffne DevTools/Konsole, um die Pixiv-Callback-URL zu erfassen.",
    tutorialStep4Title: "pixiv-URL kopieren",
    tutorialStep4Desc: "Kopiere die Callback-URL mit dem Pixiv-Autorisierungscode.",
    tutorialStep5Title: "URL / Code einfügen",
    tutorialStep5Desc: "Füge Callback-URL oder Code in das Eingabefeld der OAuth-Konsole ein.",
    tutorialStep6Title: "Token austauschen",
    tutorialStep6Desc: "Klicke auf Token austauschen und kopiere danach access_token / refresh_token.",
    errApiNotFound: "API-Endpunkt nicht gefunden (404). Deployen Sie zuerst /api/token auf Vercel.",
    errApiHtml: "Server hat HTML statt JSON zurückgegeben. Prüfen Sie Deployment-Routen/Konfiguration.",
    copiedPs: "PowerShell-Befehl kopiert.",
    copiedCmd: "CMD-Befehl kopiert.",
    copiedPip: "pip-Befehl kopiert.",
    showMore: "Mehr anzeigen",
    showLess: "Weniger anzeigen",
    footerProductTitle: "Produkt",
    footerHomeLink: "Startseite",
    footerDownloadLink: "Downloads",
    footerTutorialLink: "Tutorial",
    footerSourceLink: "Quellcode",
    footerResourceTitle: "Ressourcen & Dokumente",
    footerDocsLink: "Dokumentation",
    footerPixivLink: "Pixiv OAuth",
    footerPythonLink: "Python 3.11+",
    footerVercelLink: "Bereitgestellt auf Vercel",
    footerSupportTitle: "Unterstützung",
    footerIssueLink: "Problem melden",
    footerDiscussLink: "Diskussionen",
    footerDevLink: "Fatony Ahmad Fauzi",
    dlCatAgent: "AGENTEN",
    dlSidebarWin: "Windows",
    dlCatSdk: "SDKS",
    dlSidebarPy: "Python",
    dlBadgeWin: "Agent",
    dlTitleWin: "Windows",
    dlInstallWin: "Installation",
    dlTabDl: "Herunterladen",
    dlTabPs: "PowerShell",
    dlTabCmd: "CMD",
    dlDescWin1: "Laden Sie eine eigenständige ausführbare Datei ohne Laufzeitabhängigkeiten herunter. Sie kennen Ihre Architektur nicht? ",
    dlDescWinHelp: "Hilf mir, es zu finden.",
    dlDescPs: "Installieren Sie über PowerShell:",
    dlDescCmd: "Installieren Sie über CMD:",
    dlBadgePy: "SDK",
    dlTitlePy: "Python",
    dlInstallPy: "Installation",
    dlPyClone: "Repository klonen",
    dlPyOpen: "Projektordner öffnen",
    dlPyVenv: "Optional: Virtuelle Umgebung erstellen",
    dlPyReqs: "Installiere requirements.txt",
    dlPyRun: "Führe CLI-App aus",
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
    contact: "Social",
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
    tutorialTabStart: "Commencer",
    tutorialTabSteps: "Étapes du tutoriel",
    tutorialTabTips: "Astuces",
    tutorialPageTitle: "Commencer le tutoriel Pixiv OAuth",
    tutorialPageDesc: "Suivez les étapes du login à l’échange du token pour faciliter le processus sur desktop et mobile.",
    tutorialStepsTitle: "Étapes du tutoriel",
    tutorialBackBtn: "Retour à la console OAuth",
    needVisualGuide: "Besoin d’un guide visuel étape par étape ?",
    openTutorialPage: "Ouvrir la page tutoriel",
    windowsPreviewBadge: "Aperçu application Windows",
    windowsPreviewTitle: "Voir Pixiv OAuth Windows App en action",
    windowsPreviewDesc: "Cet aperçu rapide montre le flux de l’application Windows, du login à la génération réussie du token.",
    cliPreviewBadge: "Aperçu CLI",
    cliPreviewTitle: "Aperçu de la sortie Pixiv OAuth CLI",
    cliPreviewDesc: "Simulation de sortie CLI pour voir rapidement le flux de connexion, la lecture du code et le résultat du token.",
    openDownloadsPage: "Ouvrir la page téléchargements",
    cliPreviewFigure: "Fig. CLI — Aperçu du token Pixiv OAuth",
    downloadsDedicatedDesc: "Les téléchargements et commandes rapides sont maintenant sur une page dédiée.",
    tutorialStep1Title: "Ouvrir la page de connexion",
    tutorialStep1Desc: "Ouvrez la page de connexion Pixiv depuis l’outil console web.",
    tutorialStep2Title: "Continuer la connexion",
    tutorialStep2Desc: "Continuez la connexion du compte Pixiv jusqu’à la redirection callback.",
    tutorialStep3Title: "Ouvrir la console",
    tutorialStep3Desc: "Ouvrez les devtools/la console pour récupérer l’URL callback Pixiv.",
    tutorialStep4Title: "Copier l’URL pixiv",
    tutorialStep4Desc: "Copiez l’URL callback contenant le code d’autorisation Pixiv.",
    tutorialStep5Title: "Coller URL / code",
    tutorialStep5Desc: "Collez l’URL callback ou le code dans l’input de la console OAuth.",
    tutorialStep6Title: "Échanger le token",
    tutorialStep6Desc: "Cliquez sur Échanger le token puis copiez access_token / refresh_token.",
    errApiNotFound: "Point d’API introuvable (404). Déployez d’abord /api/token sur Vercel.",
    errApiHtml: "Le serveur a renvoyé du HTML au lieu de JSON. Vérifiez les routes/configurations de déploiement.",
    copiedPs: "Commande PowerShell copiée.",
    copiedCmd: "Commande CMD copiée.",
    copiedPip: "Commande pip copiée.",
    showMore: "Voir plus",
    showLess: "Voir moins",
    footerProductTitle: "Produit",
    footerHomeLink: "Page d'accueil",
    footerDownloadLink: "Téléchargements",
    footerTutorialLink: "Tutoriel",
    footerSourceLink: "Code source",
    footerResourceTitle: "Ressources & Docs",
    footerDocsLink: "Documentation",
    footerPixivLink: "Point OAuth",
    footerPythonLink: "Python 3.11+",
    footerVercelLink: "Déployé sur Vercel",
    footerSupportTitle: "Support",
    footerIssueLink: "Signaler un problème",
    footerDiscussLink: "Discussions",
    footerDevLink: "Fatony Ahmad Fauzi",
    dlCatAgent: "AGENTS",
    dlSidebarWin: "Windows",
    dlCatSdk: "SDKS",
    dlSidebarPy: "Python",
    dlBadgeWin: "Agent",
    dlTitleWin: "Windows",
    dlInstallWin: "Installation",
    dlTabDl: "Télécharger",
    dlTabPs: "PowerShell",
    dlTabCmd: "CMD",
    dlDescWin1: "Exécutable sans dépendance d'exécution. Vous ne connaissez pas votre architecture ? ",
    dlDescWinHelp: "Aidez-moi.",
    dlDescPs: "Installez via PowerShell :",
    dlDescCmd: "Installez via CMD :",
    dlBadgePy: "SDK",
    dlTitlePy: "Python",
    dlInstallPy: "Installation",
    dlPyClone: "Cloner le dépôt",
    dlPyOpen: "Ouvrir le dossier",
    dlPyVenv: "Option: Créer environnement virtuel",
    dlPyReqs: "Installer requirements.txt",
    dlPyRun: "Exécuter l'application CLI",
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
    contact: "Social",
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
    tutorialTabStart: "Comenzar",
    tutorialTabSteps: "Pasos del tutorial",
    tutorialTabTips: "Consejos",
    tutorialPageTitle: "Comienza con el tutorial de Pixiv OAuth",
    tutorialPageDesc: "Sigue los pasos desde el inicio de sesión hasta el intercambio de token para que el proceso sea más fácil en desktop y móvil.",
    tutorialStepsTitle: "Pasos del tutorial",
    tutorialBackBtn: "Volver a la consola OAuth",
    needVisualGuide: "¿Necesitas una guía visual paso a paso?",
    openTutorialPage: "Abrir página de tutorial",
    windowsPreviewBadge: "Vista previa de la app de Windows",
    windowsPreviewTitle: "Mira Pixiv OAuth Windows App en acción",
    windowsPreviewDesc: "Esta vista previa corta muestra el flujo de la app de Windows desde el login hasta la generación exitosa del token.",
    cliPreviewBadge: "Vista previa CLI",
    cliPreviewTitle: "Vista previa de la salida de Pixiv OAuth CLI",
    cliPreviewDesc: "Simulación de salida CLI para mostrar de forma breve el flujo de login, lectura de código y resultado de token.",
    openDownloadsPage: "Abrir página de descargas",
    cliPreviewFigure: "Fig. CLI — Vista previa del token Pixiv OAuth",
    downloadsDedicatedDesc: "Las descargas y comandos rápidos ahora están en una página dedicada.",
    tutorialStep1Title: "Abrir página de inicio de sesión",
    tutorialStep1Desc: "Abre la página de inicio de sesión de Pixiv desde la herramienta de consola web.",
    tutorialStep2Title: "Continuar inicio de sesión",
    tutorialStep2Desc: "Continúa el inicio de sesión de la cuenta Pixiv hasta que se redirija al callback.",
    tutorialStep3Title: "Abrir consola",
    tutorialStep3Desc: "Abre devtools/consola para obtener la URL callback de Pixiv.",
    tutorialStep4Title: "Copiar URL de pixiv",
    tutorialStep4Desc: "Copia la URL callback que contiene el código de autorización de Pixiv.",
    tutorialStep5Title: "Pegar URL / código",
    tutorialStep5Desc: "Pega la URL callback o el código en el input de la consola OAuth.",
    tutorialStep6Title: "Intercambiar token",
    tutorialStep6Desc: "Haz clic en Intercambiar token y luego copia access_token / refresh_token.",
    errApiNotFound: "No se encontró el endpoint de API (404). Despliega primero /api/token en Vercel.",
    errApiHtml: "El servidor devolvió HTML en lugar de JSON. Revisa las rutas/configuración del despliegue.",
    copiedPs: "Comando de PowerShell copiado.",
    copiedCmd: "Comando CMD copiado.",
    copiedPip: "Comando pip copiado.",
    showMore: "Ver más",
    showLess: "Ver menos",
    footerProductTitle: "Producto",
    footerHomeLink: "Inicio",
    footerDownloadLink: "Descargas",
    footerTutorialLink: "Tutorial",
    footerSourceLink: "Código fuente",
    footerResourceTitle: "Recursos",
    footerDocsLink: "Documentación",
    footerPixivLink: "Pixiv OAuth",
    footerPythonLink: "Python 3.11+",
    footerVercelLink: "Desplegado en Vercel",
    footerSupportTitle: "Soporte",
    footerIssueLink: "Reportar problema",
    footerDiscussLink: "Discusiones",
    footerDevLink: "Fatony Ahmad Fauzi",
    dlCatAgent: "AGENTES",
    dlSidebarWin: "Windows",
    dlCatSdk: "SDKS",
    dlSidebarPy: "Python",
    dlBadgeWin: "Agente",
    dlTitleWin: "Windows",
    dlInstallWin: "Instalación",
    dlTabDl: "Descargar",
    dlTabPs: "PowerShell",
    dlTabCmd: "CMD",
    dlDescWin1: "Descargue un ejecutable sin dependencias. ¿No conoce su arquitectura? ",
    dlDescWinHelp: "Ayúdame a encontrarla.",
    dlDescPs: "Instale a través de PowerShell:",
    dlDescCmd: "Instale a través de CMD:",
    dlBadgePy: "SDK",
    dlTitlePy: "Python",
    dlInstallPy: "Instalación",
    dlPyClone: "Clonar repositorio",
    dlPyOpen: "Abrir carpeta",
    dlPyVenv: "Opcional: Crear entorno virtual",
    dlPyReqs: "Instalar requirements.txt",
    dlPyRun: "Ejecutar la app CLI",
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
    contact: "Social",
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
    tutorialTabStart: "Начало",
    tutorialTabSteps: "Шаги руководства",
    tutorialTabTips: "Советы",
    tutorialPageTitle: "Начните работу с руководством Pixiv OAuth",
    tutorialPageDesc: "Следуйте шагам от входа до обмена токена, чтобы процесс был проще на ПК и мобильных устройствах.",
    tutorialStepsTitle: "Шаги руководства",
    tutorialBackBtn: "Вернуться в OAuth-консоль",
    needVisualGuide: "Нужна визуальная пошаговая инструкция?",
    openTutorialPage: "Открыть страницу руководства",
    windowsPreviewBadge: "Превью Windows-приложения",
    windowsPreviewTitle: "Посмотрите Pixiv OAuth Windows App в действии",
    windowsPreviewDesc: "Это короткое превью показывает поток Windows-приложения от входа до успешной генерации токена.",
    cliPreviewBadge: "Превью CLI",
    cliPreviewTitle: "Превью вывода Pixiv OAuth CLI",
    cliPreviewDesc: "Симуляция вывода CLI, чтобы кратко показать вход, чтение кода и результат токена.",
    openDownloadsPage: "Открыть страницу загрузок",
    cliPreviewFigure: "Рис. CLI — Превью токена Pixiv OAuth",
    downloadsDedicatedDesc: "Загрузки и быстрые команды теперь находятся на отдельной странице.",
    tutorialStep1Title: "Открыть страницу входа",
    tutorialStep1Desc: "Откройте страницу входа Pixiv из веб-инструмента консоли.",
    tutorialStep2Title: "Продолжить вход",
    tutorialStep2Desc: "Продолжайте вход в аккаунт Pixiv, пока не произойдёт перенаправление на callback.",
    tutorialStep3Title: "Открыть консоль",
    tutorialStep3Desc: "Откройте devtools/консоль, чтобы получить callback URL Pixiv.",
    tutorialStep4Title: "Скопировать URL pixiv",
    tutorialStep4Desc: "Скопируйте callback URL, содержащий код авторизации Pixiv.",
    tutorialStep5Title: "Вставить URL / код",
    tutorialStep5Desc: "Вставьте callback URL или код в поле ввода OAuth-консоли.",
    tutorialStep6Title: "Обменять токен",
    tutorialStep6Desc: "Нажмите Обменять токен, затем скопируйте access_token / refresh_token.",
    errApiNotFound: "API endpoint не найден (404). Сначала разверните /api/token в Vercel.",
    errApiHtml: "Сервер вернул HTML вместо JSON. Проверьте маршруты/конфигурацию развёртывания.",
    copiedPs: "Команда PowerShell скопирована.",
    copiedCmd: "Команда CMD скопирована.",
    copiedPip: "Команда pip скопирована.",
    showMore: "Показать больше",
    showLess: "Показать меньше",
    footerProductTitle: "Продукт",
    footerHomeLink: "Главная",
    footerDownloadLink: "Загрузки",
    footerTutorialLink: "Учебник",
    footerSourceLink: "Исходный код",
    footerResourceTitle: "Ресурсы",
    footerDocsLink: "Документация",
    footerPixivLink: "Pixiv OAuth",
    footerPythonLink: "Python 3.11+",
    footerVercelLink: "На Vercel",
    footerSupportTitle: "Поддержка",
    footerIssueLink: "Сообщить о проблеме",
    footerDiscussLink: "Обсуждения",
    footerDevLink: "Fatony Ahmad Fauzi",
    dlCatAgent: "АГЕНТЫ",
    dlSidebarWin: "Windows",
    dlCatSdk: "SDK",
    dlSidebarPy: "Python",
    dlBadgeWin: "Агент",
    dlTitleWin: "Windows",
    dlInstallWin: "Установка",
    dlTabDl: "Скачать",
    dlTabPs: "PowerShell",
    dlTabCmd: "CMD",
    dlDescWin1: "Скачайте автономный файл. Не знаете свою архитектуру? ",
    dlDescWinHelp: "Помогите найти.",
    dlDescPs: "Установите через PowerShell:",
    dlDescCmd: "Установите через CMD:",
    dlBadgePy: "SDK",
    dlTitlePy: "Python",
    dlInstallPy: "Установка",
    dlPyClone: "Клонировать репозиторий",
    dlPyOpen: "Открыть папку",
    dlPyVenv: "Необязательно: Создать вирт. среду",
    dlPyReqs: "Установить requirements",
    dlPyRun: "Запустить приложение",
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
    contact: "Social",
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
    navDownloads: "Download",
    navQuickCmd: "Comando rápido",
    navTutorial: "Tutorial",
    tutorialTitle: "Tutorial",
    tutorialDesc: "Preencha esta seção com capturas de tela em ordem para guiar os usuários do login até a troca do token.",
    tutorialTabStart: "Começar",
    tutorialTabSteps: "Etapas do tutorial",
    tutorialTabTips: "Dicas",
    tutorialPageTitle: "Comece com o tutorial Pixiv OAuth",
    tutorialPageDesc: "Siga cada etapa do login até a troca de token para facilitar o processo no desktop e no mobile.",
    tutorialStepsTitle: "Etapas do tutorial",
    tutorialBackBtn: "Voltar para o Console OAuth",
    needVisualGuide: "Precisa de um guia visual passo a passo?",
    openTutorialPage: "Abrir página do tutorial",
    windowsPreviewBadge: "Prévia do app Windows",
    windowsPreviewTitle: "Veja o Pixiv OAuth Windows App em ação",
    windowsPreviewDesc: "Esta prévia curta mostra o fluxo do app Windows desde o login até a geração bem-sucedida do token.",
    cliPreviewBadge: "Prévia CLI",
    cliPreviewTitle: "Prévia da saída do Pixiv OAuth CLI",
    cliPreviewDesc: "Simulação de saída CLI para mostrar de forma concisa o fluxo de login, leitura de código e resultado do token.",
    openDownloadsPage: "Abrir página de downloads",
    cliPreviewFigure: "Fig. CLI — Prévia do token Pixiv OAuth",
    downloadsDedicatedDesc: "Downloads e comandos rápidos agora estão em uma página dedicada.",
    tutorialStep1Title: "Abrir página de login",
    tutorialStep1Desc: "Abra a página de login do Pixiv pelo console web tool.",
    tutorialStep2Title: "Continuar login",
    tutorialStep2Desc: "Continue o login da conta Pixiv até ser redirecionado para o callback.",
    tutorialStep3Title: "Abrir console",
    tutorialStep3Desc: "Abra devtools/console para pegar a URL de callback do Pixiv.",
    tutorialStep4Title: "Copiar URL do pixiv",
    tutorialStep4Desc: "Copie a URL de callback que contém o código de autorização do Pixiv.",
    tutorialStep5Title: "Colar URL / código",
    tutorialStep5Desc: "Cole a URL de callback ou o código no input do console OAuth.",
    tutorialStep6Title: "Trocar token",
    tutorialStep6Desc: "Clique em Trocar token e depois copie access_token / refresh_token.",
    errApiNotFound: "Endpoint da API não encontrado (404). Implante /api/token na Vercel primeiro.",
    errApiHtml: "O servidor retornou HTML em vez de JSON. Verifique as rotas/configuração de implantação.",
    copiedPs: "Comando do PowerShell copiado.",
    copiedCmd: "Comando CMD copiado.",
    copiedPip: "Comando pip copiado.",
    showMore: "Ver mais",
    showLess: "Ver menos",
    footerProductTitle: "Produto",
    footerHomeLink: "Página Inicial",
    footerDownloadLink: "Downloads",
    footerTutorialLink: "Tutorial",
    footerSourceLink: "Código Fonte",
    footerResourceTitle: "Recursos",
    footerDocsLink: "Documentação",
    footerPixivLink: "Pixiv OAuth",
    footerPythonLink: "Python 3.11+",
    footerVercelLink: "Implementado no Vercel",
    footerSupportTitle: "Suporte",
    footerIssueLink: "Relatar Problema",
    footerDiscussLink: "Discussões",
    footerDevLink: "Fatony Ahmad Fauzi",
    dlCatAgent: "AGENTES",
    dlSidebarWin: "Windows",
    dlCatSdk: "SDKS",
    dlSidebarPy: "Python",
    dlBadgeWin: "Agente",
    dlTitleWin: "Windows",
    dlInstallWin: "Instalação",
    dlTabDl: "Baixar",
    dlTabPs: "PowerShell",
    dlTabCmd: "CMD",
    dlDescWin1: "Baixe um executável independente. Não sabe sua arquitetura? ",
    dlDescWinHelp: "Ajude-me a encontrá-la.",
    dlDescPs: "Instale via PowerShell:",
    dlDescCmd: "Instale via CMD:",
    dlBadgePy: "SDK",
    dlTitlePy: "Python",
    dlInstallPy: "Instalação",
    dlPyClone: "Clonar repositório",
    dlPyOpen: "Abrir pasta",
    dlPyVenv: "Opcional: Criar ambiente virtual",
    dlPyReqs: "Instalar requirements.txt",
    dlPyRun: "Executar aplicativo CLI",
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
    contact: "Social",
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
    cliPreviewFigure: "Fig. CLI — Preview Token Pixiv OAuth",
    downloadsDedicatedDesc: "Unduhan & perintah cepat kini ada di halaman khusus.",
    tutorialStep1Title: "Buka Halaman Login",
    tutorialStep1Desc: "Buka halaman login Pixiv dari web tool console.",
    tutorialStep2Title: "Lanjutkan Login",
    tutorialStep2Desc: "Lanjutkan proses login akun Pixiv sampai diarahkan ke callback.",
    tutorialStep3Title: "Buka Console",
    tutorialStep3Desc: "Buka devtools/console untuk mengambil URL callback Pixiv.",
    tutorialStep4Title: "Salin URL pixiv",
    tutorialStep4Desc: "Salin URL callback yang berisi kode otorisasi Pixiv.",
    tutorialStep5Title: "Tempel URL / Kode",
    tutorialStep5Desc: "Tempel URL callback atau kode ke input OAuth console.",
    tutorialStep6Title: "Tukar Token",
    tutorialStep6Desc: "Klik Exchange Token lalu salin access_token / refresh_token.",
    errApiNotFound: "Endpoint API tidak ditemukan (404). Deploy /api/token ke Vercel terlebih dahulu.",
    errApiHtml: "Server mengembalikan HTML, bukan JSON. Periksa route atau konfigurasi deploy.",
    copiedPs: "Perintah PowerShell tersalin.",
    copiedCmd: "Perintah CMD tersalin.",
    copiedPip: "Perintah pip tersalin.",
    showMore: "Lihat Selengkapnya",
    showLess: "Tampilkan Sedikit",
    footerProductTitle: "Produk",
    footerHomeLink: "Beranda",
    footerDownloadLink: "Unduhan",
    footerTutorialLink: "Tutorial",
    footerSourceLink: "Kode Sumber",
    footerResourceTitle: "Sumber",
    footerDocsLink: "Dokumentasi",
    footerPixivLink: "Pixiv OAuth",
    footerPythonLink: "Python 3.11+",
    footerVercelLink: "Dideploy di Vercel",
    footerSupportTitle: "Dukungan",
    footerIssueLink: "Laporkan Masalah",
    footerDiscussLink: "Diskusi",
    footerDevLink: "Fatony Ahmad Fauzi",
    dlCatAgent: "AGEN",
    dlSidebarWin: "Windows",
    dlCatSdk: "SDK",
    dlSidebarPy: "Python",
    dlBadgeWin: "Agen",
    dlTitleWin: "Windows",
    dlInstallWin: "Instalasi",
    dlTabDl: "Unduh",
    dlTabPs: "PowerShell",
    dlTabCmd: "CMD",
    dlDescWin1: "Unduh aplikasi standalone executable tanpa runtime dependency. Tidak tahu arsitektur Anda? ",
    dlDescWinHelp: "Bantu saya menemukannya.",
    dlDescPs: "Instal menggunakan PowerShell dengan perintah berikut:",
    dlDescCmd: "Instal menggunakan CMD dengan perintah berikut:",
    dlBadgePy: "SDK",
    dlTitlePy: "Python",
    dlInstallPy: "Instalasi",
    dlPyClone: "Kloning repositori",
    dlPyOpen: "Buka folder proyek",
    dlPyVenv: "Opsional: Buat virtual environment",
    dlPyReqs: "Instal requirements.txt",
    dlPyRun: "Jalankan aplikasi CLI",
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
    contact: "Social",
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
    tutorialTabStart: "시작하기",
    tutorialTabSteps: "튜토리얼 단계",
    tutorialTabTips: "팁",
    tutorialPageTitle: "Pixiv OAuth 튜토리얼 시작하기",
    tutorialPageDesc: "로그인부터 토큰 교환까지 순서대로 따라하면 데스크톱과 모바일에서 더 쉽게 진행할 수 있습니다.",
    tutorialStepsTitle: "튜토리얼 단계",
    tutorialBackBtn: "OAuth 콘솔로 돌아가기",
    needVisualGuide: "시각적인 단계별 가이드가 필요하신가요?",
    openTutorialPage: "튜토리얼 페이지 열기",
    windowsPreviewBadge: "Windows 앱 미리보기",
    windowsPreviewTitle: "Pixiv OAuth Windows App 실행 화면 보기",
    windowsPreviewDesc: "이 짧은 미리보기는 로그인부터 토큰 생성 성공까지 Windows 앱 흐름을 보여줍니다.",
    cliPreviewBadge: "CLI 미리보기",
    cliPreviewTitle: "Pixiv OAuth CLI 출력 미리보기",
    cliPreviewDesc: "CLI 출력 시뮬레이션으로 로그인 흐름, 코드 읽기, 토큰 결과를 간단히 확인할 수 있습니다.",
    openDownloadsPage: "다운로드 페이지 열기",
    cliPreviewFigure: "그림. CLI — Pixiv OAuth 토큰 미리보기",
    downloadsDedicatedDesc: "다운로드 및 빠른 명령은 이제 전용 페이지로 이동했습니다.",
    tutorialStep1Title: "로그인 페이지 열기",
    tutorialStep1Desc: "웹 콘솔 도구에서 Pixiv 로그인 페이지를 엽니다.",
    tutorialStep2Title: "로그인 계속하기",
    tutorialStep2Desc: "Pixiv 계정 로그인을 계속 진행해 callback으로 이동합니다.",
    tutorialStep3Title: "콘솔 열기",
    tutorialStep3Desc: "Pixiv callback URL을 가져오기 위해 devtools/console을 엽니다.",
    tutorialStep4Title: "pixiv URL 복사",
    tutorialStep4Desc: "Pixiv 인증 코드가 포함된 callback URL을 복사합니다.",
    tutorialStep5Title: "URL / 코드 붙여넣기",
    tutorialStep5Desc: "callback URL 또는 코드를 OAuth 콘솔 입력 칸에 붙여넣습니다.",
    tutorialStep6Title: "토큰 교환",
    tutorialStep6Desc: "토큰 교환을 클릭한 뒤 access_token / refresh_token을 복사하세요.",
    errApiNotFound: "API 엔드포인트를 찾을 수 없습니다(404). 먼저 Vercel에 /api/token을 배포하세요.",
    errApiHtml: "서버가 JSON 대신 HTML을 반환했습니다. 배포 경로/구성을 확인하세요.",
    copiedPs: "PowerShell 명령이 복사되었습니다.",
    copiedCmd: "CMD 명령이 복사되었습니다.",
    copiedPip: "pip 명령이 복사되었습니다.",
    showMore: "더 보기",
    showLess: "접기",
    footerProductTitle: "제품",
    footerHomeLink: "홈",
    footerDownloadLink: "다운로드",
    footerTutorialLink: "튜토리얼",
    footerSourceLink: "소스 코드",
    footerResourceTitle: "리소스",
    footerDocsLink: "문서",
    footerPixivLink: "OAuth 엔드포인트",
    footerPythonLink: "Python 3.11+",
    footerVercelLink: "Vercel 배포됨",
    footerSupportTitle: "지원",
    footerIssueLink: "문제 신고",
    footerDiscussLink: "토론",
    footerDevLink: "Fatony Ahmad Fauzi",
    dlCatAgent: "에이전트",
    dlSidebarWin: "Windows",
    dlCatSdk: "SDK",
    dlSidebarPy: "Python",
    dlBadgeWin: "에이전트",
    dlTitleWin: "Windows",
    dlInstallWin: "설치",
    dlTabDl: "다운로드",
    dlTabPs: "PowerShell",
    dlTabCmd: "CMD",
    dlDescWin1: "종속성 없이 독립 실행형 파일을 다운로드합니다. 아키텍처를 모르시나요? ",
    dlDescWinHelp: "도움말.",
    dlDescPs: "PowerShell 실행:",
    dlDescCmd: "CMD 실행:",
    dlBadgePy: "SDK",
    dlTitlePy: "Python",
    dlInstallPy: "설치",
    dlPyClone: "저장소 복제",
    dlPyOpen: "프로젝트 폴더 열기",
    dlPyVenv: "선택: 가상 환경 만들기",
    dlPyReqs: "requirements.txt 설치",
    dlPyRun: "CLI 앱 실행",
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

function setupDownloadTabs() {
  const tabs = Array.from(document.querySelectorAll('.download-inline-tabs a[data-tab-target]'));
  if (!tabs.length) return;

  const panels = Array.from(document.querySelectorAll('.download-tab-panel'));

  const activate = (targetId) => {
    tabs.forEach((tab) => {
      const isActive = tab.dataset.tabTarget === targetId;
      tab.classList.toggle('active', isActive);
      tab.setAttribute('aria-current', isActive ? 'page' : 'false');
    });

    panels.forEach((panel) => {
      panel.classList.toggle('active', panel.id === targetId);
    });
  };

  tabs.forEach((tab) => {
    tab.addEventListener('click', (e) => {
      e.preventDefault();
      activate(tab.dataset.tabTarget);
    });

    tab.addEventListener('keydown', (e) => {
      const currentIndex = tabs.indexOf(tab);
      if (currentIndex < 0) return;

      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        e.preventDefault();
        const offset = e.key === 'ArrowRight' ? 1 : -1;
        const next = (currentIndex + offset + tabs.length) % tabs.length;
        activate(tabs[next].dataset.tabTarget);
        tabs[next].focus();
      }
    });
  });

  activate('downloadTabPanel');
}

function setupArchDownloadRows() {
  const ARCH_MAP = {
    x86: "x86",
    x64: "x64",
    arm64: "ARM64"
  };

  const rows = [
    { selectId: "archSelectGuiSetup", btnId: "btnGuiSetupArch", prefix: "Pixiv OAuth GUi Setup" },
    { selectId: "archSelectCliSetup", btnId: "btnCliSetupArch", prefix: "Pixiv OAuth CLi Setup" },
    { selectId: "archSelectGuiPortable", btnId: "btnGuiPortableArch", prefix: "Pixiv OAuth GUi (Portable)" },
    { selectId: "archSelectCliPortable", btnId: "btnCliPortableArch", prefix: "Pixiv OAuth CLi (Portable)" }
  ];

  const makeLink = (prefix, arch) => repoDownloadLink(`${prefix} ${ARCH_MAP[arch]}_latest.exe`);

  rows.forEach(({ selectId, btnId, prefix }) => {
    const select = q(selectId);
    const btn = q(btnId);
    if (!select || !btn) return;

    const apply = () => {
      const arch = select.value || "x64";
      btn.href = makeLink(prefix, arch);
    };

    select.addEventListener("change", apply);
    apply();
  });
}

async function hydrateReleaseAssets() {
  // Always render fallback links/commands first so tabs are never empty.
  // The fetch(RELEASE_API) code has been disabled to prevent 404 errors 
  // since the repository does not have any GitHub Releases yet. 
  // Just use the fallback download URLs instead.
  setDownloadLinks();
  setCommandBlocks();

  /*
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    const res = await fetch(RELEASE_API, {
      headers: { Accept: "application/vnd.github+json" },
      signal: controller.signal
    });

    clearTimeout(timeoutId);
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
    // Fallback already rendered above.
  }
  */
}

function setCommandBlocks(assets = {}) {
  const files = {
    guiPortable: {
      x64: assets.guiPortableX64 || repoDownloadLink("Pixiv OAuth GUi (Portable) x64_latest.exe"),
      x86: assets.guiPortableX86 || repoDownloadLink("Pixiv OAuth GUi (Portable) x86_latest.exe"),
      arm64: assets.guiPortableArm64 || repoDownloadLink("Pixiv OAuth GUi (Portable) ARM64_latest.exe")
    },
    cliPortable: {
      x64: assets.cliPortableX64 || repoDownloadLink("Pixiv OAuth CLi (Portable) x64_latest.exe"),
      x86: assets.cliPortableX86 || repoDownloadLink("Pixiv OAuth CLi (Portable) x86_latest.exe"),
      arm64: assets.cliPortableArm64 || repoDownloadLink("Pixiv OAuth CLi (Portable) ARM64_latest.exe")
    },
    guiSetup: {
      x64: assets.guiSetupX64 || repoDownloadLink("Pixiv OAuth GUi Setup x64_latest.exe"),
      x86: assets.guiSetupX86 || repoDownloadLink("Pixiv OAuth GUi Setup x86_latest.exe"),
      arm64: assets.guiSetupArm64 || repoDownloadLink("Pixiv OAuth GUi Setup ARM64_latest.exe")
    },
    cliSetup: {
      x64: assets.cliSetupX64 || repoDownloadLink("Pixiv OAuth CLi Setup x64_latest.exe"),
      x86: assets.cliSetupX86 || repoDownloadLink("Pixiv OAuth CLi Setup x86_latest.exe"),
      arm64: assets.cliSetupArm64 || repoDownloadLink("Pixiv OAuth CLi Setup ARM64_latest.exe")
    }
  };

  const labels = [
    ["guiPortable", "Portable GUI"],
    ["cliPortable", "Portable CLI"],
    ["guiSetup", "Setup GUI"],
    ["cliSetup", "Setup CLI"]
  ];

  const archOrder = [["x64", "64-Bit"], ["x86", "32-Bit"], ["arm64", "ARM 64-Bit"]];

  const psCommands = [];
  const cmdCommands = [];

  labels.forEach(([key, name]) => {
    archOrder.forEach(([arch, archLabel]) => {
      const url = files[key][arch];
      psCommands.push({
        title: `${name} ${archLabel}`,
        value: `Invoke-WebRequest "${url}" -OutFile "Pixiv OAuth ${name} (${archLabel}).exe"`
      });
      cmdCommands.push({
        title: `${name} ${archLabel}`,
        value: `curl -L "${url}" -o "Pixiv OAuth ${name} (${archLabel}).exe"`
      });
    });
  });

  const renderList = (containerId, commands) => {
    const root = q(containerId);
    if (!root) return;
    root.innerHTML = "";

    commands.forEach((item) => {
      const box = document.createElement("div");
      box.className = "cmd-command-item";

      const title = document.createElement("small");
      title.className = "cmd-command-label";
      title.textContent = item.title;

      const row = document.createElement("div");
      row.className = "cmd-command-row";

      const code = document.createElement("code");
      code.className = "cmd-command-code";
      code.textContent = item.value;

      const copyBtn = document.createElement("button");
      copyBtn.className = "cmd-copy-btn";
      copyBtn.type = "button";
      copyBtn.setAttribute("aria-label", `Copy ${item.title}`);
      copyBtn.innerHTML = '<i class="bi bi-copy" aria-hidden="true"></i>';
      copyBtn.addEventListener("click", async () => {
        await copyText(item.value, `Command copied: ${item.title}`);
      });

      row.appendChild(code);
      row.appendChild(copyBtn);
      box.appendChild(title);
      box.appendChild(row);
      root.appendChild(box);
    });
  };

  renderList("psCmdList", psCommands);
  renderList("cmdCmdList", cmdCommands);

  const ps = q("psCmd");
  const cmd = q("cmdCmd");
  if (ps) ps.textContent = psCommands.map((x) => x.value).join("\n");
  if (cmd) cmd.textContent = cmdCommands.map((x) => x.value).join("\n");
}



function setupDownloadCategorySwitch() {
  const items = Array.from(document.querySelectorAll('[data-download-panel]'));
  const panels = Array.from(document.querySelectorAll('.download-category-panel'));
  if (!items.length || !panels.length) return;

  const activatePanel = (panelId) => {
    items.forEach((item) => {
      const active = item.dataset.downloadPanel === panelId;
      item.classList.toggle('active', active);
      item.setAttribute('aria-pressed', active ? 'true' : 'false');
    });

    panels.forEach((panel) => {
      const active = panel.id === panelId;
      panel.classList.toggle('active', active);
      panel.hidden = !active;
    });
  };

  items.forEach((item) => {
    item.addEventListener('click', () => activatePanel(item.dataset.downloadPanel));
    item.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        activatePanel(item.dataset.downloadPanel);
      }
    });
  });
}

function setupCommandCopyButtons() {
  document.querySelectorAll('[data-copy-text]').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const text = btn.getAttribute('data-copy-text') || '';
      if (!text) return;
      await copyText(text, 'Command copied.');
    });
  });
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


function setupHomeDownloadMenu() {
  const toggle = q("navDownloadToggle");
  const menu = q("navDownloadMenu");
  if (!toggle || !menu) return;

  const close = () => {
    menu.hidden = true;
    toggle.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
  };

  const open = () => {
    const container = toggle.closest(".topbar-inner");
    if (container) {
      const t = toggle.getBoundingClientRect();
      const c = container.getBoundingClientRect();
      const left = Math.max(8, Math.round(t.left - c.left - 10));
      menu.style.left = `${left}px`;
    }

    menu.hidden = false;
    toggle.classList.add("open");
    toggle.setAttribute("aria-expanded", "true");
  };

  toggle.addEventListener("click", (e) => {
    e.preventDefault();
    if (menu.hidden) open();
    else close();
  });

  document.addEventListener("click", (e) => {
    if (!toggle.contains(e.target) && !menu.contains(e.target)) close();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") close();
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

  toggle.addEventListener("click", (e) => {
    e.stopPropagation();
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
    docsBtnLabel: "docs",
    oauthTitle: "oauthTitle",
    openLoginBtnLabel: "open",
    openLoginBtnLabel2: "open",
    exchangeBtnLabel: "exchange",
    refreshBtnLabel: "refresh",
    resultTitle: "result",
    copyAccessBtnLabel: "copyAccess",
    copyRefreshBtnLabel: "copyRefresh",
    footerContactTitle: "contact",
    downloadsTitle: "downloadsTitle",
    downloadsDesc: "downloadsDesc",
    quickCmdTitle: "quickCmdTitle",
    quickCmdDesc: "quickCmdDesc",
    copyPsBtnLabel: "copyPs",
    copyCmdBtnLabel: "copyCmd",
    copyPipBtnLabel: "copyPip",
    navHomepageLabel: "navHomepage",
    navConsole: "navConsole",
    navDownloads: "navDownloads",
    navQuickCmd: "navQuickCmd",
    navTutorial: "navTutorial",
    downloadsTabLabel: "downloadsTitle",
    quickCmdTabLabel: "quickCmdTitle",
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
    tutorialBackBtnLabel: "tutorialBackBtn",
    cliPreviewFigure: "cliPreviewFigure",
    downloadsDedicatedDesc: "downloadsDedicatedDesc",
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
    footerProductTitle: "footerProductTitle",
    footerHomeLink: "footerHomeLink",
    footerDownloadLink: "footerDownloadLink",
    footerTutorialLink: "footerTutorialLink",
    footerSourceLink: "footerSourceLink",
    footerResourceTitle: "footerResourceTitle",
    footerDocsLink: "footerDocsLink",
    footerPixivLink: "footerPixivLink",
    footerPythonLink: "footerPythonLink",
    footerVercelLink: "footerVercelLink",
    footerSupportTitle: "footerSupportTitle",
    footerIssueLink: "footerIssueLink",
    footerDiscussLink: "footerDiscussLink",
    footerDevLink: "footerDevLink",
    dlCatAgent: "dlCatAgent",
    dlSidebarWin: "dlSidebarWin",
    dlCatSdk: "dlCatSdk",
    dlSidebarPy: "dlSidebarPy",
    dlBadgeWin: "dlBadgeWin",
    dlTitleWin: "dlTitleWin",
    dlInstallWin: "dlInstallWin",
    dlTabDl: "dlTabDl",
    dlTabPs: "dlTabPs",
    dlTabCmd: "dlTabCmd",
    dlDescWin1: "dlDescWin1",
    dlDescWinHelp: "dlDescWinHelp",
    dlDescPs: "dlDescPs",
    dlDescCmd: "dlDescCmd",
    dlBadgePy: "dlBadgePy",
    dlTitlePy: "dlTitlePy",
    dlInstallPy: "dlInstallPy",
    dlPyClone: "dlPyClone",
    dlPyOpen: "dlPyOpen",
    dlPyVenv: "dlPyVenv",
    dlPyReqs: "dlPyReqs",
    dlPyRun: "dlPyRun",
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

function setupMobileSidebar() {
  const menuToggle = document.getElementById("menuToggle");
  const sidebarOverlay = document.getElementById("sidebarOverlay");
  const navLinksContainer = document.querySelector(".nav-links") || document.querySelector(".tutorial-docs-actions");

  if (menuToggle && sidebarOverlay && navLinksContainer) {
    function toggleSidebar() {
      navLinksContainer.classList.toggle("open");
      sidebarOverlay.classList.toggle("active");
      document.body.style.overflow = sidebarOverlay.classList.contains("active") ? "hidden" : "";
    }

    menuToggle.addEventListener("click", toggleSidebar);
    sidebarOverlay.addEventListener("click", toggleSidebar);
    
    const closeBtns = navLinksContainer.querySelectorAll(".close-sidebar");
    closeBtns.forEach(btn => btn.addEventListener("click", toggleSidebar));

    const links = navLinksContainer.querySelectorAll("a:not(.sidebar-brand)");
    links.forEach(link => {
      link.addEventListener("click", () => {
        navLinksContainer.classList.remove("open");
        sidebarOverlay.classList.remove("active");
        document.body.style.overflow = "";
      });
    });
  }
}

function setupMobilePlatformDropdown() {
  const select = document.getElementById("mobilePlatformSelect");
  if (!select) return;

  select.addEventListener("change", () => {
    const targetId = select.value;
    const panels = document.querySelectorAll(".download-category-panel");
    const sidebarItems = document.querySelectorAll(".download-showcase-sidebar li");

    panels.forEach(p => {
      p.hidden = p.id !== targetId;
      p.classList.toggle("active", p.id === targetId);
    });
    sidebarItems.forEach(li => {
      li.classList.toggle("active", li.dataset.downloadPanel === targetId);
      li.setAttribute("aria-pressed", li.dataset.downloadPanel === targetId ? "true" : "false");
    });
  });
}

(async function init() {
  const saved = localStorage.getItem("pixiv_lang");
  if (saved && LANG_ORDER.includes(saved)) {
    setDisplayLanguage(saved);
  }

  document.documentElement.lang = DISPLAY_LANG;

  setupLanguageMenu();
  setupMobileSidebar();
  setupMobilePlatformDropdown();
  setupCliPreviewToggle();
  applyLang();
  setupDownloadCategorySwitch();
  setupDownloadTabs();
  setupArchDownloadRows();
  setupCommandCopyButtons();
  await hydrateReleaseAssets();
})();

// ---------------------- FLOATING BANTUAN WIDGET ----------------------
const hwHTML = `
<div class="hw-container">
  <button id="hwBtn" class="hw-btn"><i class="bi bi-question-circle-fill"></i> Bantuan</button>
  <div id="hwBox" class="hw-box">
    <div class="hw-header">
      Tinggalkan pesan untuk kami
      <button id="hwClose" class="hw-close" aria-label="Close widget"><i class="bi bi-dash"></i></button>
    </div>
    <form class="hw-form" action="https://formsubmit.co/fatonyahmadfauzi@gmail.com" method="POST" enctype="multipart/form-data">
      <input type="hidden" name="_subject" value="Pesan Bantuan dari Pixiv OAuth Web">
      <input type="hidden" name="_next" value="https://pixiv-o-auth-token.vercel.app/contact?success=true">
      <input type="hidden" name="_captcha" value="true">
      <input type="hidden" name="_template" value="box">

      <div class="hw-group">
        <label>Nama Anda</label>
        <input type="text" name="Nama_Anda" class="hw-input" required>
      </div>
      <div class="hw-group">
        <label>Alamat email</label>
        <input type="email" name="email" class="hw-input" required>
      </div>
      <div class="hw-group">
        <label>Ada yang bisa kami bantu?</label>
        <textarea name="Pesan" class="hw-input" required></textarea>
      </div>
      <div class="hw-group">
        <label class="hw-file-wrap" for="hwFile"><span>Lampiran</span> <div><i class="bi bi-paperclip"></i> Tambahkan hingga 5 file</div></label>
        <input type="file" id="hwFile" name="attachment" accept="image/*,.pdf,.zip,.log,.txt" multiple>
      </div>
      <button type="submit" class="hw-submit">Kirim</button>
    </form>
  </div>
</div>
`;

document.body.insertAdjacentHTML('beforeend', hwHTML);

const hwBtn = document.getElementById('hwBtn');
const hwBox = document.getElementById('hwBox');
const hwClose = document.getElementById('hwClose');

if (hwBtn && hwBox && hwClose) {
  hwBtn.addEventListener('click', () => {
    hwBox.classList.add('show');
    hwBtn.style.opacity = '0';
    hwBtn.style.pointerEvents = 'none';
  });

  hwClose.addEventListener('click', (e) => {
    e.preventDefault();
    hwBox.classList.remove('show');
    hwBtn.style.opacity = '1';
    hwBtn.style.pointerEvents = 'auto';
  });
}
