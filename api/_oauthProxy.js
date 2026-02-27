const AUTH_TOKEN_URL = "https://oauth.secure.pixiv.net/auth/token";
const USER_AGENT = "PixivAndroidApp/5.0.234 (Android 11; Pixel 5)";
const CLIENT_SECRET_FALLBACK = "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj";

function buildForm(payload) {
  const form = new URLSearchParams();
  for (const [k, v] of Object.entries(payload || {})) {
    if (v !== undefined && v !== null && v !== "") form.set(k, String(v));
  }
  form.set("client_secret", process.env.PIXIV_CLIENT_SECRET || CLIENT_SECRET_FALLBACK);
  return form;
}

async function forwardTokenRequest(payload) {
  const form = buildForm(payload);
  const res = await fetch(AUTH_TOKEN_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "User-Agent": USER_AGENT,
      "App-OS": "android",
      "App-OS-Version": "11",
      "App-Version": "5.0.234",
      "Accept-Language": "en-US",
    },
    body: form,
  });

  const text = await res.text();
  let data;
  try { data = JSON.parse(text); } catch { data = { raw: text }; }

  if (!res.ok) {
    return { status: res.status, data: { error: data?.error || "Token request failed", details: data } };
  }
  return { status: 200, data };
}

module.exports = { forwardTokenRequest };
