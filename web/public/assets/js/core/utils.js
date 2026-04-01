import { t } from "./i18n.js";

/**
 * Utils module
 * Shared general purpose helpers
 */

/**
 * Formats a time string into a relative time (e.g. "just now", "5m ago")
 * @param {string} dateString
 * @returns {string}
 */
export function formatTimeRelative(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now - date;
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHrs = Math.floor(diffMin / 60);
  const diffDays = Math.floor(diffHrs / 24);

  if (diffSec < 60) return t("timeJustNow");
  if (diffMin < 60) return t("timeMinsAgo", { count: diffMin });
  if (diffHrs < 24) return t("timeHoursAgo", { count: diffHrs });
  return t("timeDaysAgo", { count: diffDays });
}

/**
 * Copy text to clipboard and update button UI
 * @param {string} textToCopy
 * @param {HTMLButtonElement} btn
 * @param {string} originalHtml
 * @param {string} successHtml
 */
export async function copyToClipboard(
  textToCopy,
  btn,
  originalHtml,
  successHtml,
) {
  if (!textToCopy) return;
  try {
    await navigator.clipboard.writeText(textToCopy);
    if (btn) {
      btn.innerHTML = successHtml;
      btn.classList.add("copied");
      setTimeout(() => {
        btn.innerHTML = originalHtml;
        btn.classList.remove("copied");
      }, 2000);
    }
  } catch (err) {
    console.error("Copy failed:", err);
  }
}
