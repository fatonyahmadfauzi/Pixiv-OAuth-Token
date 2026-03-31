const LICENSE_REPO = "fatonyahmadfauzi/Pixiv-OAuth-Token";
const LICENSE_API = `/api/github?path=repos/${LICENSE_REPO}/contents/LICENSE`;
const LICENSE_WEB_URL = `https://github.com/${LICENSE_REPO}/blob/master/LICENSE`;

function escapeHtmlLocal(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function tSafe(key, fallback) {
  try {
    if (typeof t === "function") {
      const translated = t(key);
      if (translated && translated !== key) return translated;
    }
  } catch {}
  return fallback;
}

function decodeBase64Utf8(input) {
  try {
    return decodeURIComponent(
      atob(String(input || "").replace(/\n/g, ""))
        .split("")
        .map((c) => `%${c.charCodeAt(0).toString(16).padStart(2, "0")}`)
        .join("")
    );
  } catch {
    return atob(String(input || "").replace(/\n/g, ""));
  }
}

function renderLicense(text) {
  const skeleton = document.getElementById("docSkeleton");
  const body = document.getElementById("docBody");
  if (!body) return;

  body.innerHTML =
    '<pre style="background:transparent;border:none;padding:0;overflow-x:auto;"><code>' +
    escapeHtmlLocal(text) +
    "</code></pre>";

  if (skeleton) skeleton.remove();
  body.hidden = false;
}

function renderError() {
  const skeleton = document.getElementById("docSkeleton");
  const body = document.getElementById("docBody");
  if (!body) return;

  const errorText = tSafe("licenseErrorMsg", "Failed to load License. Please check GitHub directly.");
  const buttonText = tSafe("licenseViewBtn", "View on GitHub");

  if (skeleton) skeleton.remove();
  body.innerHTML =
    '<div class="gh-error-state">' +
    '<i class="bi bi-exclamation-triangle" aria-hidden="true"></i>' +
    `<p>${escapeHtmlLocal(errorText)}</p>` +
    `<a href="${escapeHtmlLocal(LICENSE_WEB_URL)}" target="_blank" rel="noopener" class="btn link-btn">${escapeHtmlLocal(buttonText)}</a>` +
    "</div>";
  body.hidden = false;
}

async function loadLicense() {
  try {
    const res = await fetch(LICENSE_API);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const data = await res.json();
    if (!data || !data.content) throw new Error("Missing content");

    const text = decodeBase64Utf8(data.content);
    renderLicense(text);
  } catch {
    renderError();
  }
}

loadLicense();
