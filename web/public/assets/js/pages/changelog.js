/**
 * Changelog page module
 * Re-uses the docs fetcher with changelog.md as the target file.
 */
export function setupChangelogPage() {
  // The changelog page uses the same docs fetcher mechanism as docs.js
  // but targets changelog.md. It sets `data-file="changelog.md"` in HTML.
  // If the docs.js module is loaded, it reads that attribute automatically.
  // This module is a no-op hook reserved for changelog-specific enhancements.
  if (!document.getElementById("docBody")) return;
}
