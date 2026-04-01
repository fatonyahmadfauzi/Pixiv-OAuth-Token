import { setDisplayLanguage, FLAG_CLASS, LANG_NAME } from "../core/i18n.js";
import { applyLang } from "../core/dom.js";
import { updateUrlLocale } from "../seo/locale-routing.js";

/**
 * UI: Language Switcher
 */
export function setupLanguageMenu() {
  const langToggle = document.getElementById("langToggle");
  const langMenu = document.getElementById("langMenu");
  const langCurrent = document.getElementById("langCurrent");
  const langFlag = document.getElementById("langFlag");
  const langControl = document.getElementById("langControl");

  if (!langToggle || !langMenu || !langCurrent || !langFlag || !langControl)
    return;

  langToggle.addEventListener("click", () => {
    const isExpanded = langToggle.getAttribute("aria-expanded") === "true";
    langToggle.setAttribute("aria-expanded", !isExpanded);
    langMenu.classList.toggle("open");
  });

  const langOptions = langMenu.querySelectorAll("li[data-lang]");
  langOptions.forEach((option) => {
    option.addEventListener("click", () => {
      const selectedLang = option.getAttribute("data-lang");

      // Update DOM
      langCurrent.textContent = LANG_NAME[selectedLang];
      langFlag.className = `fi ${FLAG_CLASS[selectedLang]}`;
      langToggle.setAttribute("aria-expanded", "false");
      langMenu.classList.remove("open");

      // Update language state
      setDisplayLanguage(selectedLang);

      // Propagate translations to DOM
      applyLang();

      // Route URL (e.g., /jp/downloads) without reloading
      // if supported by locale-routing (PushState)
      updateUrlLocale(selectedLang);
    });
  });

  document.addEventListener("click", (e) => {
    if (!langControl.contains(e.target)) {
      langToggle.setAttribute("aria-expanded", "false");
      langMenu.classList.remove("open");
    }
  });
}
