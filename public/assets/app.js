const CLIENT_ID = "MOBrBDS8blbauoSck0ZfDbtuzpyT";
const REDIRECT_URI = "https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback";
const LOGIN_URL = "https://app-api.pixiv.net/web/v1/login";

let codeVerifier = "";
let tokenState = { access_token: "", refresh_token: "" };

const q = (id) => document.getElementById(id);
const output = q("output");

const LANG_ORDER = ["en", "pl", "zh", "jp", "de", "fr", "es", "ru", "pt", "id", "kr"];
const I18N = {
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
    nothingRefresh: "No refresh_token available.",
  },
  pl: {
    lang: "Język", open: "1) Otwórz stronę logowania", placeholder: "2) Wklej URL pixiv:// lub kod",
    exchange: "Wymień token", refresh: "Odśwież token", result: "Wynik",
    copyAccess: "Kopiuj access_token", copyRefresh: "Kopiuj refresh_token", ready: "Gotowe.",
    opened: "Strona logowania otwarta. Po logowaniu wklej URL pixiv:// lub kod.",
    codeEmpty: "Kod jest pusty.", clickOpen: "Najpierw kliknij 'Otwórz stronę logowania'.",
    noRefresh: "Brak refresh_token.", copiedAccess: "Skopiowano access_token.", copiedRefresh: "Skopiowano refresh_token.",
    nothingAccess: "Brak access_token.", nothingRefresh: "Brak refresh_token."
  },
  zh: {
    lang: "语言", open: "1) 打开登录页面", placeholder: "2) 粘贴 pixiv:// 回调 URL 或代码",
    exchange: "获取令牌", refresh: "刷新令牌", result: "结果",
    copyAccess: "复制 access_token", copyRefresh: "复制 refresh_token", ready: "准备就绪。",
    opened: "登录页面已打开。登录后请粘贴 pixiv:// URL 或代码。",
    codeEmpty: "代码为空。", clickOpen: "请先点击“打开登录页面”。", noRefresh: "没有 refresh_token。",
    copiedAccess: "已复制 access_token。", copiedRefresh: "已复制 refresh_token。", nothingAccess: "没有 access_token。", nothingRefresh: "没有 refresh_token。"
  },
  jp: {
    lang: "言語", open: "1) ログインページを開く", placeholder: "2) pixiv:// コールバックURLまたはコードを貼り付け",
    exchange: "トークン取得", refresh: "トークン更新", result: "結果",
    copyAccess: "access_tokenをコピー", copyRefresh: "refresh_tokenをコピー", ready: "準備完了。",
    opened: "ログインページを開きました。ログイン後にpixiv:// URLかコードを貼り付けてください。",
    codeEmpty: "コードが空です。", clickOpen: "先に「ログインページを開く」を押してください。", noRefresh: "refresh_tokenがありません。",
    copiedAccess: "access_tokenをコピーしました。", copiedRefresh: "refresh_tokenをコピーしました。", nothingAccess: "access_tokenがありません。", nothingRefresh: "refresh_tokenがありません。"
  },
  de: {
    lang: "Sprache", open: "1) Login-Seite öffnen", placeholder: "2) pixiv:// URL oder Code einfügen",
    exchange: "Token abrufen", refresh: "Token aktualisieren", result: "Ergebnis",
    copyAccess: "access_token kopieren", copyRefresh: "refresh_token kopieren", ready: "Bereit.",
    opened: "Login-Seite geöffnet. Nach Login pixiv:// URL oder Code einfügen.",
    codeEmpty: "Code ist leer.", clickOpen: "Bitte zuerst 'Login-Seite öffnen' klicken.", noRefresh: "Kein refresh_token vorhanden.",
    copiedAccess: "access_token kopiert.", copiedRefresh: "refresh_token kopiert.", nothingAccess: "Kein access_token vorhanden.", nothingRefresh: "Kein refresh_token vorhanden."
  },
  fr: {
    lang: "Langue", open: "1) Ouvrir la page de connexion", placeholder: "2) Collez l'URL pixiv:// ou le code",
    exchange: "Échanger le token", refresh: "Rafraîchir le token", result: "Résultat",
    copyAccess: "Copier access_token", copyRefresh: "Copier refresh_token", ready: "Prêt.",
    opened: "Page de connexion ouverte. Après connexion, collez l'URL pixiv:// ou le code.",
    codeEmpty: "Le code est vide.", clickOpen: "Veuillez d'abord cliquer sur 'Ouvrir la page de connexion'.", noRefresh: "Aucun refresh_token disponible.",
    copiedAccess: "access_token copié.", copiedRefresh: "refresh_token copié.", nothingAccess: "Aucun access_token disponible.", nothingRefresh: "Aucun refresh_token disponible."
  },
  es: {
    lang: "Idioma", open: "1) Abrir página de inicio", placeholder: "2) Pega la URL pixiv:// o el código",
    exchange: "Canjear token", refresh: "Actualizar token", result: "Resultado",
    copyAccess: "Copiar access_token", copyRefresh: "Copiar refresh_token", ready: "Listo.",
    opened: "Página de inicio abierta. Después, pega la URL pixiv:// o el código.",
    codeEmpty: "El código está vacío.", clickOpen: "Primero pulsa 'Abrir página de inicio'.", noRefresh: "No hay refresh_token disponible.",
    copiedAccess: "access_token copiado.", copiedRefresh: "refresh_token copiado.", nothingAccess: "No hay access_token disponible.", nothingRefresh: "No hay refresh_token disponible."
  },
  ru: {
    lang: "Язык", open: "1) Открыть страницу входа", placeholder: "2) Вставьте pixiv:// URL или код",
    exchange: "Получить токен", refresh: "Обновить токен", result: "Результат",
    copyAccess: "Копировать access_token", copyRefresh: "Копировать refresh_token", ready: "Готово.",
    opened: "Страница входа открыта. После входа вставьте pixiv:// URL или код.",
    codeEmpty: "Код пуст.", clickOpen: "Сначала нажмите 'Открыть страницу входа'.", noRefresh: "refresh_token отсутствует.",
    copiedAccess: "access_token скопирован.", copiedRefresh: "refresh_token скопирован.", nothingAccess: "Нет access_token.", nothingRefresh: "Нет refresh_token."
  },
  pt: {
    lang: "Idioma", open: "1) Abrir página de login", placeholder: "2) Cole a URL pixiv:// ou o código",
    exchange: "Trocar token", refresh: "Atualizar token", result: "Resultado",
    copyAccess: "Copiar access_token", copyRefresh: "Copiar refresh_token", ready: "Pronto.",
    opened: "Página de login aberta. Depois, cole a URL pixiv:// ou o código.",
    codeEmpty: "Código vazio.", clickOpen: "Clique primeiro em 'Abrir página de login'.", noRefresh: "Sem refresh_token disponível.",
    copiedAccess: "access_token copiado.", copiedRefresh: "refresh_token copiado.", nothingAccess: "Sem access_token disponível.", nothingRefresh: "Sem refresh_token disponível."
  },
  id: {
    lang: "Bahasa", open: "1) Buka Halaman Login", placeholder: "2) Tempel URL callback pixiv:// atau code di sini",
    exchange: "Ambil Token", refresh: "Refresh Token", result: "Hasil",
    copyAccess: "Salin access_token", copyRefresh: "Salin refresh_token", ready: "Siap.",
    opened: "Halaman login dibuka. Setelah login, tempel URL pixiv:// atau code.",
    codeEmpty: "Code kosong.", clickOpen: "Klik 'Buka Halaman Login' dulu.", noRefresh: "Belum ada refresh_token.",
    copiedAccess: "access_token tersalin.", copiedRefresh: "refresh_token tersalin.", nothingAccess: "Belum ada access_token.", nothingRefresh: "Belum ada refresh_token."
  },
  kr: {
    lang: "언어", open: "1) 로그인 페이지 열기", placeholder: "2) pixiv:// 콜백 URL 또는 코드를 붙여넣기",
    exchange: "토큰 받기", refresh: "토큰 새로고침", result: "결과",
    copyAccess: "access_token 복사", copyRefresh: "refresh_token 복사", ready: "준비 완료.",
    opened: "로그인 페이지를 열었습니다. 로그인 후 pixiv:// URL 또는 코드를 붙여넣으세요.",
    codeEmpty: "코드가 비어 있습니다.", clickOpen: "먼저 '로그인 페이지 열기'를 클릭하세요.", noRefresh: "refresh_token이 없습니다.",
    copiedAccess: "access_token을 복사했습니다.", copiedRefresh: "refresh_token을 복사했습니다.", nothingAccess: "access_token이 없습니다.", nothingRefresh: "refresh_token이 없습니다."
  }
};

for (const code of LANG_ORDER) {
  I18N[code] = { ...I18N.en, ...(I18N[code] || {}) };
}

let currentLang = "en";

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
  } catch (e) {
    output.textContent = `Error: ${e.message}`;
  }
};

q("refreshBtn").onclick = async () => {
  try {
    if (!tokenState.refresh_token) throw new Error(t("noRefresh"));
    const data = await callApi({ grant_type: "refresh_token", refresh_token: tokenState.refresh_token, client_id: CLIENT_ID, include_policy: true });
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
  if (saved && LANG_ORDER.includes(saved)) currentLang = saved;
  q("langSelect").value = currentLang;
  document.documentElement.lang = currentLang === "jp" ? "ja" : currentLang;
  applyLang();
})();
