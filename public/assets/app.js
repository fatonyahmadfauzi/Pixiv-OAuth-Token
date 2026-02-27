const CLIENT_ID = "MOBrBDS8blbauoSck0ZfDbtuzpyT";
const REDIRECT_URI = "https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback";
const LOGIN_URL = "https://app-api.pixiv.net/web/v1/login";

let codeVerifier = "";
let tokenState = { access_token: "", refresh_token: "" };

const q = (id) => document.getElementById(id);
const output = q("output");

const I18N = {
  id: {
    title: "Pixiv OAuth Web",
    subtitle: "Helper token OAuth yang clean, responsive, untuk Netlify/Vercel.",
    lang: "Bahasa",
    open: "1) Buka Halaman Login",
    placeholder: "2) Tempel URL callback pixiv:// atau code di sini",
    exchange: "Ambil Token",
    refresh: "Refresh Token",
    result: "Hasil",
    copyAccess: "Salin access_token",
    copyRefresh: "Salin refresh_token",
    ready: "Siap.",
    opened: "Halaman login dibuka. Setelah login, tempel URL pixiv:// atau code.",
    codeEmpty: "Code kosong.",
    clickOpen: "Klik 'Buka Halaman Login' dulu.",
    noRefresh: "Belum ada refresh_token.",
    copiedAccess: "access_token tersalin.",
    copiedRefresh: "refresh_token tersalin.",
    nothingAccess: "Belum ada access_token.",
    nothingRefresh: "Belum ada refresh_token."
  },
  en: {
    title: "Pixiv OAuth Web",
    subtitle: "Clean, responsive OAuth token helper for Netlify/Vercel.",
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
    nothingRefresh: "No refresh_token available."
  },
  jp: {
    title: "Pixiv OAuth Web",
    subtitle: "Netlify/Vercel向けのクリーンでレスポンシブなOAuthトークンヘルパー。",
    lang: "言語",
    open: "1) ログインページを開く",
    placeholder: "2) pixiv:// コールバックURLまたはコードを貼り付け",
    exchange: "トークン取得",
    refresh: "トークン更新",
    result: "結果",
    copyAccess: "access_tokenをコピー",
    copyRefresh: "refresh_tokenをコピー",
    ready: "準備完了。",
    opened: "ログインページを開きました。ログイン後にpixiv:// URLかコードを貼り付けてください。",
    codeEmpty: "コードが空です。",
    clickOpen: "先に「ログインページを開く」を押してください。",
    noRefresh: "refresh_tokenがありません。",
    copiedAccess: "access_tokenをコピーしました。",
    copiedRefresh: "refresh_tokenをコピーしました。",
    nothingAccess: "access_tokenがありません。",
    nothingRefresh: "refresh_tokenがありません。"
  }
};

let currentLang = "id";

function t(key) {
  return (I18N[currentLang] && I18N[currentLang][key]) || I18N.en[key] || key;
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
  if (output.textContent.trim() === "Ready." || output.textContent.trim() === "Siap." || output.textContent.trim() === "準備完了。") {
    output.textContent = t("ready");
  }
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
  const codeChallenge = b64Url([...new Uint8Array(digest)]);
  return { codeVerifier, codeChallenge };
}

function parseCode(input) {
  const tVal = input.trim();
  if (!tVal) return "";
  if (tVal.startsWith("pixiv://")) {
    const u = new URL(tVal);
    return u.searchParams.get("code") || "";
  }
  try {
    const u = new URL(tVal);
    return u.searchParams.get("code") || tVal;
  } catch {
    return tVal;
  }
}

function apiBase() {
  if (location.hostname.includes("netlify")) return "/.netlify/functions/token";
  return "/api/token";
}

async function callApi(payload) {
  const res = await fetch(apiBase(), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
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
  const url = `${LOGIN_URL}?${new URLSearchParams({
    code_challenge: codeChallenge,
    code_challenge_method: "S256",
    client: "pixiv-android",
  })}`;
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
      include_policy: true,
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
      include_policy: true,
    });
    tokenState = data;
    output.textContent = JSON.stringify(data, null, 2);
  } catch (e) {
    output.textContent = `Error: ${e.message}`;
  }
};

q("copyAccessBtn").onclick = async () => {
  if (!tokenState.access_token) return (output.textContent = t("nothingAccess"));
  await navigator.clipboard.writeText(tokenState.access_token);
  output.textContent = t("copiedAccess");
};

q("copyRefreshBtn").onclick = async () => {
  if (!tokenState.refresh_token) return (output.textContent = t("nothingRefresh"));
  await navigator.clipboard.writeText(tokenState.refresh_token);
  output.textContent = t("copiedRefresh");
};

(function init() {
  const saved = localStorage.getItem("pixiv_lang");
  if (saved && I18N[saved]) currentLang = saved;
  q("langSelect").value = currentLang;
  document.documentElement.lang = currentLang === "jp" ? "ja" : currentLang;
  q("yearNow").textContent = String(new Date().getFullYear());
  applyLang();
})();
