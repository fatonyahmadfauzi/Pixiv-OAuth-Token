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
