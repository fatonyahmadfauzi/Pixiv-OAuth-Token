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
    const isMobile = window.innerWidth <= 768 || /Mobi|Android|iPhone/i.test(navigator.userAgent);
    if (isMobile) {
      if (output) {
        const lang = document.documentElement.lang || "en";
        const msg = {
          en: "Error: This version is not supported on mobile because you cannot inspect the web to copy the code. Currently, it only works on desktop environments that support inspect element.",
          id: "Error: Versi saat ini tidak support pada mobile karena Anda tidak bisa inspect web untuk menyalin kode. Saat ini hanya berfungsi pada desktop yang dapat di-inspect elemennya.",
          zh: "错误：当前版本不支持移动设备，因为您无法检查网页以复制代码。目前它仅在使用支持检查元素功能的桌面环境中工作。",
          jp: "エラー：モバイル版ではウェブを検証してコードをコピーできないため、このバージョンはサポートされていません。現在は要素を検証できるデスクトップ環境でのみ動作します。",
          kr: "오류: 모바일에서는 웹을 검사하여 코드를 복사할 수 없으므로 이 버전은 지원되지 않습니다. 현재는 요소 검사를 지원하는 데스크톱 환경에서만 작동합니다.",
          pl: "Błąd: Ta wersja nie jest obsługiwana na urządzeniach mobilnych, ponieważ nie można tam zinspectować strony w celu skopiowania kodu. Obecnie działa to tylko w środowiskach stacjonarnych obsługujących funkcję Inspekji.",
          de: "Fehler: Diese Version wird auf Mobilgeräten nicht unterstützt, da Sie die Webseite nicht untersuchen können, um den Code zu kopieren. Derzeit funktioniert es nur in Desktop-Umgebungen.",
          fr: "Erreur : Cette version n'est pas prise en charge sur mobile car vous ne pouvez pas inspecter le web pour copier le code. Actuellement, cela ne fonctionne que sur les environnements de bureau.",
          es: "Error: Esta versión no es compatible en dispositivos móviles ya que no puede inspeccionar la web para copiar el código. Actualmente solo funciona en entornos de escritorio.",
          ru: "Ошибка: эта версия не поддерживается на мобильных устройствах, поскольку вы не можете инспектировать веб-страницы для копирования кода. Работает только в десктопных средах.",
          pt: "Erro: Esta versão não é suportada em dispositivos móveis porque você não pode inspecionar a web para copiar o código. No momento, só funciona em ambientes de desktop."
        };
        output.textContent = msg[lang] || msg["en"];
      }
      return;
    }

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
