import { t } from "../core/i18n.js";

const LICENSE_REPO = "fatonyahmadfauzi/Pixiv-OAuth-Token";
const LICENSE_RAW_URL = `https://raw.githubusercontent.com/${LICENSE_REPO}/master/LICENSE`;
const LICENSE_WEB_URL = `https://github.com/${LICENSE_REPO}/blob/master/LICENSE`;

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

function renderLicense(text) {
  const skeleton = document.getElementById("docSkeleton");
  const body = document.getElementById("docBody");
  if (!body) return;
  body.innerHTML = `<pre style="background:transparent;border:none;padding:0;overflow-x:auto;"><code>${escapeHtml(text)}</code></pre>`;
  if (skeleton) skeleton.remove();
  body.hidden = false;
}

function renderLicenseError() {
  const skeleton = document.getElementById("docSkeleton");
  const body = document.getElementById("docBody");
  if (!body) return;
  const errorText = t("licenseErrorMsg");
  const buttonText = t("licenseViewBtn");
  if (skeleton) skeleton.remove();
  body.innerHTML =
    `<div class="gh-error-state">` +
    `<i class="bi bi-exclamation-triangle" aria-hidden="true"></i>` +
    `<p>${escapeHtml(errorText)}</p>` +
    `<a href="${escapeHtml(LICENSE_WEB_URL)}" target="_blank" rel="noopener" class="btn link-btn">${escapeHtml(buttonText)}</a>` +
    `</div>`;
  body.hidden = false;
}

async function loadLicense() {
  try {
    const res = await fetch(LICENSE_RAW_URL);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const text = await res.text();
    if (!text) throw new Error("Missing content");
    renderLicense(text);
  } catch { renderLicenseError(); }
}

export function setupLicensePage() {
  if (!document.getElementById("docBody")) return;
  loadLicense();
}
