const USER_AGENT = "PixivAndroidApp/5.0.234 (Android 11; Pixel 5)";
const CLIENT_ID = "MOBrBDS8blbauoSck0ZfDbtuzpyT";
const REDIRECT_URI = "https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback";
const LOGIN_URL = "https://app-api.pixiv.net/web/v1/login";

let codeVerifier = "";
let tokenState = { access_token: "", refresh_token: "" };

const q = (id) => document.getElementById(id);
const output = q("output");

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
  const t = input.trim();
  if (!t) return "";
  if (t.startsWith("pixiv://")) {
    const u = new URL(t);
    return u.searchParams.get("code") || "";
  }
  try {
    const u = new URL(t);
    return u.searchParams.get("code") || t;
  } catch {
    return t;
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

q("openLoginBtn").onclick = async () => {
  const { codeChallenge } = await createPkce();
  const url = `${LOGIN_URL}?${new URLSearchParams({
    code_challenge: codeChallenge,
    code_challenge_method: "S256",
    client: "pixiv-android",
  })}`;
  window.open(url, "_blank", "noopener");
  output.textContent = "Login page opened. After login, paste pixiv:// callback URL or code.";
};

q("exchangeBtn").onclick = async () => {
  try {
    const code = parseCode(q("inputCode").value);
    if (!code) throw new Error("Code is empty.");
    if (!codeVerifier) throw new Error("Click 'Open Login Page' first.");

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
    if (!tokenState.refresh_token) throw new Error("No refresh_token available.");
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
  if (!tokenState.access_token) return;
  await navigator.clipboard.writeText(tokenState.access_token);
};
q("copyRefreshBtn").onclick = async () => {
  if (!tokenState.refresh_token) return;
  await navigator.clipboard.writeText(tokenState.refresh_token);
};
