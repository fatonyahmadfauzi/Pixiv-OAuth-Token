import { t } from "../core/i18n.js";

/**
 * Contact page: custom file input behaviour
 */
export function setupContactFileInput() {
  const fileInput = document.getElementById("attachment"),
    customBtn = document.getElementById("customFileBtn"),
    customText = document.getElementById("customFileText");

  if (!fileInput || !customBtn || !customText) return;

  customBtn.addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
      const names = Array.from(fileInput.files)
        .map((f) => f.name)
        .join(", ");
      customText.textContent = names;
      customText.removeAttribute("data-i18n");
    } else {
      customText.setAttribute("data-i18n", "contactNoFile");
      customText.textContent = t("contactNoFile");
    }
  });
}
