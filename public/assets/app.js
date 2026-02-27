const CLIENT_ID = "MOBrBDS8blbauoSck0ZfDbtuzpyT";
const REDIRECT_URI = "https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback";
const LOGIN_URL = "https://app-api.pixiv.net/web/v1/login";
const RELEASE_BASE = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest/download";
const RELEASE_API = "https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest";

let codeVerifier = "";
let tokenState = { access_token: "", refresh_token: "" };

const q = (id) => document.getElementById(id);
const output = q("output");

const LANG_ORDER = ["en", "pl", "zh", "jp", "de", "fr", "es", "ru", "pt", "id", "kr"];
const I18N = {
  en: {
    kicker: "Pixiv OAuth Toolkit",
    title: "Pixiv OAuth Web",
    subtitle: "Toolkit to generate Pixiv OAuth tokens via CLI, GUI, and Web with secure PKCE flow and Netlify/Vercel-ready deployment.",
    badgePkce: "PKCE Flow", badgeDeploy: "Netlify & Vercel Ready", badgeRelease: "Release Download",
    overviewTitle: "Project Overview",
    overviewDesc: "This project helps exchange/refresh Pixiv OAuth tokens and ships Windows build scripts for Portable/Setup artifacts plus Linux binary support.",
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
    errApiNotFound: "API endpoint not found (404). Deploy /api/token (Vercel) or Netlify function first.",
    errApiHtml: "Server returned HTML instead of JSON. Check deployment routes/config.",
    copiedPs: "PowerShell command copied.", copiedCmd: "CMD command copied.", copiedPip: "pip command copied."
  },
  id: {
    subtitle: "Toolkit untuk mendapatkan token Pixiv OAuth melalui CLI, GUI, dan Web dengan alur PKCE aman serta siap deploy di Netlify/Vercel.",
    overviewTitle: "Ringkasan Project", overviewDesc: "Project ini membantu exchange/refresh token Pixiv OAuth dan menyediakan script build Windows untuk artifact Portable/Setup serta dukungan binary Linux.",
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
    errApiNotFound: "Endpoint API tidak ditemukan (404). Deploy /api/token (Vercel) atau function Netlify dulu.",
    errApiHtml: "Server mengembalikan HTML, bukan JSON. Cek konfigurasi route/deploy.",
    copiedPs: "Command PowerShell tersalin.", copiedCmd: "Command CMD tersalin.", copiedPip: "Command pip tersalin."
  },
  jp: {
    subtitle: "CLI・GUI・Web向け Pixiv OAuth（PKCE）ツールキット。Netlify/Vercel にデプロイ可能。",
    overviewTitle: "プロジェクト概要", modesTitle: "利用モード", requirementsTitle: "要件", oauthTitle: "OAuth トークンコンソール",
    overviewDesc: "このプロジェクトは Pixiv OAuth トークンの取得/更新を支援し、Windows の Portable/Setup ビルドと Linux バイナリを提供します。",
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
    overviewDesc: "Projekt pomaga uzyskiwać/odświeżać tokeny Pixiv OAuth i zawiera skrypty build dla Windows oraz binarkę Linux.", docs: "Czytaj dokumentację",
    open: "1) Otwórz stronę logowania", placeholder: "2) Wklej URL zwrotny pixiv:// lub kod tutaj", exchange: "Wymień token", refresh: "Odśwież token", result: "Wynik",
    copyAccess: "Kopiuj access_token", copyRefresh: "Kopiuj refresh_token", ready: "Gotowe.",
    resource: "Zasoby", contact: "Kontakt", dev: "Deweloper", downloadsTitle: "Pobieranie", downloadsDesc: "Pobierz najnowszą wersję z GitHub Releases.",
    quickCmdTitle: "Szybkie polecenie", quickCmdDesc: "Skopiuj polecenie PowerShell/CMD oraz instalację pip.",
    copyPs: "Kopiuj PowerShell", copyCmd: "Kopiuj CMD", copyPip: "Kopiuj polecenie pip"
  },
  zh: {
    lang: "语言", overviewTitle: "项目概览", modesTitle: "可用模式", requirementsTitle: "环境要求", oauthTitle: "OAuth 令牌控制台",
    overviewDesc: "该项目可帮助获取/刷新 Pixiv OAuth 令牌，并提供 Windows 打包脚本和 Linux 二进制。", docs: "阅读文档",
    open: "1) 打开登录页面", placeholder: "2) 在此粘贴 pixiv:// 回调URL或代码", exchange: "交换令牌", refresh: "刷新令牌", result: "结果",
    copyAccess: "复制 access_token", copyRefresh: "复制 refresh_token", ready: "就绪。",
    resource: "资源", contact: "联系", dev: "开发者", downloadsTitle: "下载", downloadsDesc: "从 GitHub Releases 下载最新版本。",
    quickCmdTitle: "快速命令", quickCmdDesc: "复制 PowerShell/CMD 下载命令和 pip 安装命令。",
    copyPs: "复制 PowerShell", copyCmd: "复制 CMD", copyPip: "复制 pip 命令"
  },
  de: {
    lang: "Sprache", overviewTitle: "Projektübersicht", modesTitle: "Verfügbare Modi", requirementsTitle: "Anforderungen", oauthTitle: "OAuth-Token-Konsole",
    overviewDesc: "Dieses Projekt hilft beim Abrufen/Aktualisieren von Pixiv OAuth-Token und enthält Build-Skripte für Windows sowie Linux-Binärdatei.", docs: "Dokumentation lesen",
    open: "1) Login-Seite öffnen", placeholder: "2) pixiv:// Callback-URL oder Code hier einfügen", exchange: "Token abrufen", refresh: "Token aktualisieren", result: "Ergebnis",
    copyAccess: "access_token kopieren", copyRefresh: "refresh_token kopieren", ready: "Bereit.",
    resource: "Ressourcen", contact: "Kontakt", dev: "Entwickler", downloadsTitle: "Downloads", downloadsDesc: "Lade den neuesten Build von GitHub Releases herunter.",
    quickCmdTitle: "Schnellbefehl", quickCmdDesc: "Kopiere PowerShell/CMD-Download- und pip-Installationsbefehle.",
    copyPs: "PowerShell kopieren", copyCmd: "CMD kopieren", copyPip: "pip-Befehl kopieren"
  },
  fr: {
    lang: "Langue", overviewTitle: "Aperçu du projet", modesTitle: "Modes disponibles", requirementsTitle: "Prérequis", oauthTitle: "Console de jetons OAuth",
    overviewDesc: "Ce projet aide à échanger/rafraîchir les jetons Pixiv OAuth et fournit des scripts de build Windows ainsi qu'un binaire Linux.", docs: "Lire la documentation",
    open: "1) Ouvrir la page de connexion", placeholder: "2) Collez l'URL callback pixiv:// ou le code ici", exchange: "Échanger le jeton", refresh: "Rafraîchir le jeton", result: "Résultat",
    copyAccess: "Copier access_token", copyRefresh: "Copier refresh_token", ready: "Prêt.",
    resource: "Ressources", contact: "Contact", dev: "Développeur", downloadsTitle: "Téléchargements", downloadsDesc: "Téléchargez la dernière version depuis GitHub Releases.",
    quickCmdTitle: "Commande rapide", quickCmdDesc: "Copiez les commandes PowerShell/CMD et l'installation pip.",
    copyPs: "Copier PowerShell", copyCmd: "Copier CMD", copyPip: "Copier la commande pip"
  },
  es: {
    lang: "Idioma", overviewTitle: "Resumen del proyecto", modesTitle: "Modos disponibles", requirementsTitle: "Requisitos", oauthTitle: "Consola de token OAuth",
    overviewDesc: "Este proyecto ayuda a intercambiar/actualizar tokens Pixiv OAuth e incluye scripts de build para Windows y binario Linux.", docs: "Leer la documentación",
    open: "1) Abrir página de inicio de sesión", placeholder: "2) Pega aquí la URL callback pixiv:// o el código", exchange: "Intercambiar token", refresh: "Actualizar token", result: "Resultado",
    copyAccess: "Copiar access_token", copyRefresh: "Copiar refresh_token", ready: "Listo.",
    resource: "Recursos", contact: "Contacto", dev: "Desarrollador", downloadsTitle: "Descargas", downloadsDesc: "Descarga la última versión desde GitHub Releases.",
    quickCmdTitle: "Comando rápido", quickCmdDesc: "Copia comandos de PowerShell/CMD e instalación por pip.",
    copyPs: "Copiar PowerShell", copyCmd: "Copiar CMD", copyPip: "Copiar comando pip"
  },
  ru: {
    lang: "Язык", overviewTitle: "Обзор проекта", modesTitle: "Доступные режимы", requirementsTitle: "Требования", oauthTitle: "Консоль OAuth-токена",
    overviewDesc: "Проект помогает получать/обновлять токены Pixiv OAuth и включает скрипты сборки для Windows и Linux-бинарник.", docs: "Читать документацию",
    open: "1) Открыть страницу входа", placeholder: "2) Вставьте pixiv:// callback URL или код", exchange: "Получить токен", refresh: "Обновить токен", result: "Результат",
    copyAccess: "Копировать access_token", copyRefresh: "Копировать refresh_token", ready: "Готово.",
    resource: "Ресурсы", contact: "Контакты", dev: "Разработчик", downloadsTitle: "Загрузки", downloadsDesc: "Скачать последнюю сборку с GitHub Releases.",
    quickCmdTitle: "Быстрая команда", quickCmdDesc: "Скопируйте команды PowerShell/CMD и установку pip.",
    copyPs: "Копировать PowerShell", copyCmd: "Копировать CMD", copyPip: "Копировать команду pip"
  },
  pt: {
    lang: "Idioma", overviewTitle: "Visão geral do projeto", modesTitle: "Modos disponíveis", requirementsTitle: "Requisitos", oauthTitle: "Console de token OAuth",
    overviewDesc: "Este projeto ajuda a trocar/atualizar tokens Pixiv OAuth e inclui scripts de build para Windows e binário Linux.", docs: "Ler a documentação",
    open: "1) Abrir página de login", placeholder: "2) Cole a URL de callback pixiv:// ou código aqui", exchange: "Trocar token", refresh: "Atualizar token", result: "Resultado",
    copyAccess: "Copiar access_token", copyRefresh: "Copiar refresh_token", ready: "Pronto.",
    resource: "Recursos", contact: "Contato", dev: "Desenvolvedor", downloadsTitle: "Downloads", downloadsDesc: "Baixe a versão mais recente no GitHub Releases.",
    quickCmdTitle: "Comando rápido", quickCmdDesc: "Copie comandos de download PowerShell/CMD e instalação via pip.",
    copyPs: "Copiar PowerShell", copyCmd: "Copiar CMD", copyPip: "Copiar comando pip"
  },
  kr: {
    lang: "언어", overviewTitle: "프로젝트 개요", modesTitle: "사용 가능한 모드", requirementsTitle: "요구 사항", oauthTitle: "OAuth 토큰 콘솔",
    overviewDesc: "이 프로젝트는 Pixiv OAuth 토큰 발급/갱신을 돕고 Windows 빌드 스크립트와 Linux 바이너리를 제공합니다.", docs: "문서 읽기",
    open: "1) 로그인 페이지 열기", placeholder: "2) pixiv:// 콜백 URL 또는 코드를 붙여넣으세요", exchange: "토큰 교환", refresh: "토큰 갱신", result: "결과",
    copyAccess: "access_token 복사", copyRefresh: "refresh_token 복사", ready: "준비 완료.",
    resource: "리소스", contact: "연락처", dev: "개발자", downloadsTitle: "다운로드", downloadsDesc: "GitHub Releases에서 최신 빌드를 다운로드하세요.",
    quickCmdTitle: "빠른 명령", quickCmdDesc: "PowerShell/CMD 다운로드 명령과 pip 설치 명령을 복사하세요.",
    copyPs: "PowerShell 복사", copyCmd: "CMD 복사", copyPip: "pip 명령 복사"
  }
};

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

function setDownloadLinks(assets = {}) {
  q("dlCliSetup").href = assets.cliSetup || "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest";
  q("dlCliPortable").href = assets.cliPortable || releaseLink("Pixiv OAuth CLi (Portable).exe");
  q("dlGuiSetup").href = assets.guiSetup || "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest";
  q("dlGuiPortable").href = assets.guiPortable || releaseLink("Pixiv OAuth GUi (Portable).exe");
  q("dlLinux").href = assets.linux || releaseLink("pixiv_login_plus_linux");
}

async function hydrateReleaseAssets() {
  try {
    const res = await fetch(RELEASE_API, { headers: { Accept: "application/vnd.github+json" } });
    if (!res.ok) throw new Error("release api unavailable");

    const release = await res.json();
    const assets = release.assets || [];
    const pick = (matcher) => assets.find((a) => matcher(a.name || ""))?.browser_download_url;

    setDownloadLinks({
      cliSetup: pick((n) => /Pixiv OAuth CLi Setup/i.test(n)),
      cliPortable: pick((n) => /Pixiv OAuth CLi \(Portable\)/i.test(n)),
      guiSetup: pick((n) => /Pixiv OAuth GUi Setup/i.test(n)),
      guiPortable: pick((n) => /Pixiv OAuth GUi \(Portable\)/i.test(n)),
      linux: pick((n) => /pixiv_login_plus_linux/i.test(n))
    });
  } catch {
    setDownloadLinks();
  }
}

function setCommandBlocks() {
  q("psCmd").textContent = `$base = "${RELEASE_BASE}"\nInvoke-WebRequest "$base/Pixiv%20OAuth%20GUi%20(Portable).exe" -OutFile "Pixiv OAuth GUi (Portable).exe"\nInvoke-WebRequest "$base/Pixiv%20OAuth%20CLi%20(Portable).exe" -OutFile "Pixiv OAuth CLi (Portable).exe"`;
  q("cmdCmd").textContent = `curl -L "${RELEASE_BASE}/Pixiv%20OAuth%20GUi%20(Portable).exe" -o "Pixiv OAuth GUi (Portable).exe"\ncurl -L "${RELEASE_BASE}/Pixiv%20OAuth%20CLi%20(Portable).exe" -o "Pixiv OAuth CLi (Portable).exe"`;
  q("pipCmd").textContent = `python -m pip install -r requirements.txt\npython -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"`;
}

async function copyText(text, okMessage) {
  await navigator.clipboard.writeText(text);
  output.textContent = okMessage;
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
    langLabel: "lang",
    openLoginBtnLabel: "open",
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
    reqBuild: "reqBuild"
  };

  Object.entries(map).forEach(([id, key]) => {
    q(id).textContent = t(key);
  });

  q("inputCode").placeholder = t("placeholder");
  output.textContent = t("ready");
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
  return location.hostname.includes("netlify") ? "/.netlify/functions/token" : "/api/token";
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

q("openLoginBtn").onclick = async () => {
  const { codeChallenge } = await createPkce();
  const url = `${LOGIN_URL}?${new URLSearchParams({ code_challenge: codeChallenge, code_challenge_method: "S256", client: "pixiv-android" })}`;
  window.open(url, "_blank", "noopener");
  output.textContent = t("opened");
};

q("exchangeBtn").onclick = async () => {
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
    output.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    output.textContent = `Error: ${e.message}`;
  }
};

q("refreshBtn").onclick = async () => {
  try {
    if (!tokenState.refresh_token) throw new Error(t("noRefresh"));

    const data = await callApi({
      grant_type: "refresh_token",
      refresh_token: tokenState.refresh_token,
      client_id: CLIENT_ID,
      include_policy: true
    });

    tokenState = data;
    output.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    output.textContent = `Error: ${e.message}`;
  }
};

q("copyAccessBtn").onclick = async () => {
  if (!tokenState.access_token) {
    output.textContent = t("nothingAccess");
    return;
  }

  await copyText(tokenState.access_token, t("copiedAccess"));
};

q("copyRefreshBtn").onclick = async () => {
  if (!tokenState.refresh_token) {
    output.textContent = t("nothingRefresh");
    return;
  }

  await copyText(tokenState.refresh_token, t("copiedRefresh"));
};

q("copyPsBtn").onclick = async () => copyText(q("psCmd").textContent, t("copiedPs"));
q("copyCmdBtn").onclick = async () => copyText(q("cmdCmd").textContent, t("copiedCmd"));
q("copyPipBtn").onclick = async () => copyText(q("pipCmd").textContent, t("copiedPip"));

(async function init() {
  const saved = localStorage.getItem("pixiv_lang");
  if (saved && LANG_ORDER.includes(saved)) currentLang = saved;

  document.documentElement.lang = currentLang === "jp" ? "ja" : currentLang;

  setupLanguageMenu();
  setCommandBlocks();
  applyLang();
  await hydrateReleaseAssets();
})();
