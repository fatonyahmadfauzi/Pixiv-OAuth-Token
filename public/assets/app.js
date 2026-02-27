const CLIENT_ID = "MOBrBDS8blbauoSck0ZfDbtuzpyT";
const REDIRECT_URI = "https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback";
const LOGIN_URL = "https://app-api.pixiv.net/web/v1/login";
const RELEASE_BASE = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest/download";

let codeVerifier = "";
let tokenState = { access_token: "", refresh_token: "" };

const q = (id) => document.getElementById(id);
const output = q("output");

const LANG_ORDER = ["en", "pl", "zh", "jp", "de", "fr", "es", "ru", "pt", "id", "kr"];
const I18N = {
  en: {
    title: "Pixiv OAuth Web",
    subtitle: "Pixiv OAuth helper for CLI, GUI, and Web (PKCE) with Netlify/Vercel deployment support.",
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
    dev: "Dev",
    downloadsTitle: "Downloads",
    downloadsDesc: "Download latest build directly from GitHub Releases.",
    quickCmdTitle: "Quick Command",
    quickCmdDesc: "Copy command for PowerShell/CMD download and pip install.",
    copyPs: "Copy PowerShell",
    copyCmd: "Copy CMD",
    copyPip: "Copy pip command",
    errApiNotFound: "API endpoint not found (404). Deploy /api/token (Vercel) or Netlify function first.",
    errApiHtml: "Server returned HTML instead of JSON. Check deployment routes/config."
  },
  id: {
    subtitle: "Helper Pixiv OAuth untuk CLI, GUI, dan Web (PKCE) dengan dukungan deploy Netlify/Vercel.",
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
    errApiHtml: "Server mengembalikan HTML, bukan JSON. Cek konfigurasi route/deploy."
  },
  jp: {
    subtitle: "CLI・GUI・Web向け Pixiv OAuth（PKCE）ヘルパー。Netlify/Vercel に対応。",
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

function t(key) { return (I18N[currentLang] && I18N[currentLang][key]) || I18N.en[key] || key; }

function releaseLink(name) { return `${RELEASE_BASE}/${encodeURIComponent(name)}`; }

function setDownloadLinks() {
  q("dlCliSetup").href = releaseLink("Pixiv OAuth CLi Setup_v1.0.13.exe");
  q("dlCliPortable").href = releaseLink("Pixiv OAuth CLi (Portable).exe");
  q("dlGuiSetup").href = releaseLink("Pixiv OAuth GUi Setup_v1.0.13.exe");
  q("dlGuiPortable").href = releaseLink("Pixiv OAuth GUi (Portable).exe");
  q("dlLinux").href = releaseLink("pixiv_login_plus_linux");
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

function applyLang() {
  q("titleText").textContent = t("title");
  q("subtitleText").textContent = t("subtitle");
  q("langLabel").textContent = t("lang");
  q("openLoginBtn").textContent = t("open");
  q("inputCode").placeholder = t("placeholder");
  q("exchangeBtn").textContent = t("exchange");
  q("refreshBtn").textContent = t("refresh");
  q("resultTitle").textContent = t("result");
  q("copyAccessBtn").textContent = t("copyAccess");
  q("copyRefreshBtn").textContent = t("copyRefresh");
  q("footerResourceTitle").textContent = t("resource");
  q("footerContactTitle").textContent = t("contact");
  q("footerDevTitle").textContent = t("dev");
  q("downloadsTitle").textContent = t("downloadsTitle");
  q("downloadsDesc").textContent = t("downloadsDesc");
  q("quickCmdTitle").textContent = t("quickCmdTitle");
  q("quickCmdDesc").textContent = t("quickCmdDesc");
  q("copyPsBtn").textContent = t("copyPs");
  q("copyCmdBtn").textContent = t("copyCmd");
  q("copyPipBtn").textContent = t("copyPip");
  output.textContent = t("ready");
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
  const tVal = input.trim();
  if (!tVal) return "";
  if (tVal.startsWith("pixiv://")) return new URL(tVal).searchParams.get("code") || "";
  try { return new URL(tVal).searchParams.get("code") || tVal; } catch { return tVal; }
}

function apiBase() {
  if (location.hostname.includes("netlify")) return "/.netlify/functions/token";
  return "/api/token";
}

async function callApi(payload) {
  const res = await fetch(apiBase(), { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
  const raw = await res.text();
  let data;
  try { data = JSON.parse(raw); }
  catch {
    if (res.status === 404) throw new Error(t("errApiNotFound"));
    if ((raw && raw.toLowerCase().includes("<html")) || raw.startsWith("The page")) throw new Error(t("errApiHtml"));
    throw new Error(raw || "Unknown API response");
  }
  if (!res.ok) throw new Error(data.error || JSON.stringify(data));
  return data;
}

q("langSelect").onchange = (e) => {
  currentLang = e.target.value;
  localStorage.setItem("pixiv_lang", currentLang);
  document.documentElement.lang = currentLang === "jp" ? "ja" : currentLang;
  applyLang();
};

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
    const data = await callApi({ grant_type: "authorization_code", code, code_verifier: codeVerifier, redirect_uri: REDIRECT_URI, client_id: CLIENT_ID, include_policy: true });
    tokenState = data;
    output.textContent = JSON.stringify(data, null, 2);
  } catch (e) { output.textContent = `Error: ${e.message}`; }
};

q("refreshBtn").onclick = async () => {
  try {
    if (!tokenState.refresh_token) throw new Error(t("noRefresh"));
    const data = await callApi({ grant_type: "refresh_token", refresh_token: tokenState.refresh_token, client_id: CLIENT_ID, include_policy: true });
    tokenState = data;
    output.textContent = JSON.stringify(data, null, 2);
  } catch (e) { output.textContent = `Error: ${e.message}`; }
};

q("copyAccessBtn").onclick = async () => {
  if (!tokenState.access_token) return (output.textContent = t("nothingAccess"));
  await copyText(tokenState.access_token, t("copiedAccess"));
};

q("copyRefreshBtn").onclick = async () => {
  if (!tokenState.refresh_token) return (output.textContent = t("nothingRefresh"));
  await copyText(tokenState.refresh_token, t("copiedRefresh"));
};

q("copyPsBtn").onclick = async () => copyText(q("psCmd").textContent, "PowerShell command copied.");
q("copyCmdBtn").onclick = async () => copyText(q("cmdCmd").textContent, "CMD command copied.");
q("copyPipBtn").onclick = async () => copyText(q("pipCmd").textContent, "pip command copied.");

(function init() {
  const saved = localStorage.getItem("pixiv_lang");
  if (saved && LANG_ORDER.includes(saved)) currentLang = saved;
  q("langSelect").value = currentLang;
  document.documentElement.lang = currentLang === "jp" ? "ja" : currentLang;
  setDownloadLinks();
  setCommandBlocks();
  applyLang();
})();
