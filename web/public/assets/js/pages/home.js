import { q } from "../core/dom.js";
import { t } from "../core/i18n.js";

export function setupCustomFileInput() {
  const fileInput = document.getElementById("attachment"),
    customBtn = document.getElementById("customFileBtn"),
    customText = document.getElementById("customFileText");
    
  if (fileInput && customBtn && customText) {
      customBtn.addEventListener("click", () => fileInput.click());
      fileInput.addEventListener("change", () => {
        if (fileInput.files.length > 0) {
          const fileNames = Array.from(fileInput.files)
            .map((f) => f.name)
            .join(", ");
          customText.textContent = fileNames;
          customText.removeAttribute("data-i18n");
        } else {
            customText.setAttribute("data-i18n", "contactNoFile");
            customText.textContent = t("contactNoFile");
        }
      });
      
    // Remove inline style injection and put it in index.css if necessary.
    // However, keeping style injection replicates the exact previous behavior.
    const style = document.createElement("style");
    style.textContent = `
      .custom-file-wrapper {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 5px;
      }
      .custom-file-btn {
        padding: 6px 12px;
        font-size: 0.9rem;
        cursor: pointer;
        background-color: var(--gh-btn-bg);
        border: 1px solid var(--gh-btn-border);
        color: var(--gh-fg);
        border-radius: 6px;
      }
      .custom-file-btn:hover {
        background-color: var(--gh-btn-hover-bg);
      }
      .custom-file-text {
        color: var(--gh-fg-muted);
        font-size: 0.9rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 200px;
      }
    `;
    document.head.appendChild(style);
  }
}


export function setupCliPreviewToggle() {
  const preview = q("cliPreviewBox"),
    toggle = q("cliToggleBtn");
  if (!preview || !toggle) return;
  let expanded = false;
  
  const render = () => {
    preview.classList.toggle("expanded", expanded);
    toggle.textContent = t(expanded ? "showLess" : "showMore");
  };
  
  toggle.addEventListener("click", () => {
    expanded = !expanded;
    render();
  });
  
  render();
}
