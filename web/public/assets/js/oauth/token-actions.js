import { t } from "../core/i18n.js";
import { q } from "../core/dom.js";
import { copyToClipboard } from "../core/utils.js";
import { callApi } from "./api.js";
import {
  createPkce,
  parseCode,
  getCodeVerifier,
  getTokenState,
  setTokenState,
} from "./pkce.js";
import { LOGIN_URL, REDIRECT_URI, CLIENT_ID } from "../core/config.js";

function bindClick(id, handler) {
  const el = q(id);
  if (el) el.onclick = handler;
}

/**
 * Binds all the OAuth console buttons
 */
export function setupOAuthConsole() {
  const output = q("output");

  bindClick("openLoginBtn", async () => {
    const { codeChallenge } = await createPkce();
    const url = `${LOGIN_URL}?${new URLSearchParams({ code_challenge: codeChallenge, code_challenge_method: "S256", client: "pixiv-android" })}`;
    window.open(url, "_blank", "noopener");
    if (output) output.textContent = t("opened");
  });

  bindClick("exchangeBtn", async () => {
    try {
      const input = q("inputCode");
      const code = parseCode(input?.value || "");
      if (!code) throw new Error(t("codeEmpty"));
      if (!getCodeVerifier()) throw new Error(t("clickOpen"));

      const data = await callApi({
        grant_type: "authorization_code",
        code: code,
        code_verifier: getCodeVerifier(),
        redirect_uri: REDIRECT_URI,
        client_id: CLIENT_ID,
        include_policy: true,
      });
      setTokenState(data);
      if (output) output.textContent = JSON.stringify(data, null, 2);
    } catch (e) {
      if (output) output.textContent = `Error: ${e.message}`;
    }
  });

  bindClick("refreshBtn", async () => {
    try {
      const tokenState = getTokenState();
      if (!tokenState.refresh_token) throw new Error(t("noRefresh"));
      const data = await callApi({
        grant_type: "refresh_token",
        refresh_token: tokenState.refresh_token,
        client_id: CLIENT_ID,
        include_policy: true,
      });
      setTokenState(data);
      if (output) output.textContent = JSON.stringify(data, null, 2);
    } catch (e) {
      if (output) output.textContent = `Error: ${e.message}`;
    }
  });

  bindClick("copyAccessBtn", async () => {
    const tokenState = getTokenState();
    if (tokenState.access_token) {
      await copyText(tokenState.access_token, t("copiedAccess"));
    } else {
      if (output) output.textContent = t("nothingAccess");
    }
  });

  bindClick("copyRefreshBtn", async () => {
    const tokenState = getTokenState();
    if (tokenState.refresh_token) {
      await copyText(tokenState.refresh_token, t("copiedRefresh"));
    } else {
      if (output) output.textContent = t("nothingRefresh");
    }
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

  async function copyText(text, okMessage) {
    await navigator.clipboard.writeText(text);
    if (output) output.textContent = okMessage;
  }
}
