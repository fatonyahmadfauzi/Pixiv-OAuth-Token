import { t, DISPLAY_LANG } from "../core/i18n.js";

const LICENSE_REPO = "fatonyahmadfauzi/Pixiv-OAuth-Token";
const RAW_BASE = `https://raw.githubusercontent.com/${LICENSE_REPO}/master`;
const LICENSE_WEB_URL = `https://github.com/${LICENSE_REPO}/blob/master/LICENSE`;

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function normalizeLangCode(input) {
  const lang = String(input || "").toLowerCase();
  const map = {
    en: "en",
    "en-us": "en",
    "en-gb": "en",
    id: "id",
    in: "id",
    jp: "jp",
    ja: "jp",
    "ja-jp": "jp",
    kr: "kr",
    ko: "kr",
    "ko-kr": "kr",
    zh: "zh",
    "zh-cn": "zh",
    "zh-tw": "zh",
    "zh-sg": "zh",
    pl: "pl",
    de: "de",
    fr: "fr",
    es: "es",
    ru: "ru",
    pt: "pt",
    "pt-br": "pt",
    "pt-pt": "pt",
  };
  if (map[lang]) return map[lang];
  return map[lang.split("-")[0]] || "en";
}

function getRouteLang() {
  const parts = window.location.pathname.split("/").filter(Boolean);
  if (parts.length > 0) {
    const n = normalizeLangCode(parts[0]);
    if (n !== "en" || parts[0].toLowerCase() === "en") return n;
  }
  if (typeof DISPLAY_LANG !== "undefined" && DISPLAY_LANG)
    return normalizeLangCode(DISPLAY_LANG);
  return normalizeLangCode(document.documentElement.lang || "en");
}

function getLocalizedLicensePath(lang) {
  if (lang === "en") return `${RAW_BASE}/LICENSE`;
  return `/docs/lang/LICENSE-${lang.toUpperCase()}`;
}

async function fetchLicenseWithFallback() {
  const preferred = getRouteLang();
  const candidates = Array.from(new Set([preferred, "en"]));
  let lastError = null;
  for (const lang of candidates) {
    try {
      const response = await fetch(getLocalizedLicensePath(lang));
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const text = await response.text();
      if (
        text.trim().toLowerCase().startsWith("<!doctype") ||
        text.trim().toLowerCase().startsWith("<html")
      ) {
        throw new Error("Received HTML fallback instead of markdown");
      }
      return text;
    } catch (err) {
      lastError = err;
    }
  }

  // Ultimate fallback to root LICENSE
  try {
    const fallbackResponse = await fetch(`${RAW_BASE}/LICENSE`);
    if (fallbackResponse.ok) {
      const text = await fallbackResponse.text();
      if (
        !text.trim().toLowerCase().startsWith("<!doctype") &&
        !text.trim().toLowerCase().startsWith("<html")
      ) {
        return text;
      }
    }
  } catch (e) {}

  throw lastError || new Error("Failed to fetch license");
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
    const text = await fetchLicenseWithFallback();
    if (!text) throw new Error("Missing content");
    renderLicense(text);
  } catch {
    renderLicenseError();
  }
}

export function setupLicensePage() {
  const fileHint = document.querySelector("[data-file]");
  const fileName = (fileHint && fileHint.getAttribute("data-file")) || "";
  if (!fileName.toLowerCase().includes("license")) return;

  if (!document.getElementById("docBody")) return;
  loadLicense();
}
