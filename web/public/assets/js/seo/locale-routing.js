import { LANG_ORDER, setDisplayLanguage, DISPLAY_LANG } from "../core/i18n.js";

/**
 * Initializes and determines locale on page load based on URL or navigator
 */
export function initLocaleRouting() {
  const parts = window.location.pathname.split("/").filter(Boolean);
  let parsedLang = null;

  if (parts.length > 0 && LANG_ORDER.includes(parts[0])) {
    parsedLang = parts[0];
  }

  if (parsedLang) {
    setDisplayLanguage(parsedLang);
    localStorage.setItem("pixiv_lang", parsedLang);
  } else {
    const saved = localStorage.getItem("pixiv_lang");
    if (saved && LANG_ORDER.includes(saved)) {
      setDisplayLanguage(saved);
    } else {
      const langMap = {
        id: "id",
        in: "id",
        ja: "jp",
        jp: "jp",
        zh: "zh",
        "zh-cn": "zh",
        "zh-tw": "zh",
        "zh-sg": "zh",
        ko: "kr",
        kr: "kr",
        de: "de",
        fr: "fr",
        es: "es",
        pt: "pt",
        "pt-br": "pt",
        "pt-pt": "pt",
        ru: "ru",
        pl: "pl",
        en: "en",
      };
      const candidates = Array.from(
        navigator.languages || [navigator.language || "en"],
      );
      let detected = "en";

      for (const lang of candidates) {
        const lower = String(lang).toLowerCase(),
          exact = langMap[lower],
          baseLang = langMap[lower.split("-")[0]];
        if (exact) {
          detected = exact;
          break;
        }
        if (baseLang) {
          detected = baseLang;
          break;
        }
      }
      setDisplayLanguage(detected);
    }
  }

  document.documentElement.lang =
    DISPLAY_LANG === "jp" ? "ja" : DISPLAY_LANG === "kr" ? "ko" : DISPLAY_LANG;
}

/**
 * Route to a new language folder when user clicks dropdown
 * @param {string} selectedLang
 */
export function updateUrlLocale(selectedLang) {
  localStorage.setItem("pixiv_lang", selectedLang);
  const parts = window.location.pathname.split("/").filter(Boolean);
  let newPath = "";
  if (parts.length > 0 && LANG_ORDER.includes(parts[0])) {
    parts[0] = selectedLang;
    newPath = "/" + parts.join("/");
  } else {
    newPath =
      "/" +
      selectedLang +
      ("/" === window.location.pathname ? "" : window.location.pathname);
  }
  window.location.href =
    newPath + window.location.search + window.location.hash;
}
