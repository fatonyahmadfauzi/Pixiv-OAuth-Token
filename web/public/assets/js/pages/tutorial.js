/**
 * Tutorial page module
 * The tutorial page scroll/step interactions are already handled
 * by the shared applyLang + setupMobileSidebar in main.js.
 * This module provides tutorial-specific extras.
 */
export function setupTutorialPage() {
  // Activation of tab navigation on tutorial page
  const tabs = document.querySelectorAll(".tutorial-tabs-nav .tab-btn");
  const panels = document.querySelectorAll(".tutorial-tab-panel");
  if (!tabs.length || !panels.length) return;

  const activate = (index) => {
    tabs.forEach((t, i) => {
      t.classList.toggle("active", i === index);
      t.setAttribute("aria-selected", i === index ? "true" : "false");
    });
    panels.forEach((p, i) => p.classList.toggle("active", i === index));
  };

  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => activate(index));
  });
  activate(0);
}
