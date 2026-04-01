/**
 * Tutorial page module
 * The tutorial page scroll/step interactions are already handled
 * by the shared applyLang + setupMobileSidebar in main.js.
 * This module provides tutorial-specific extras.
 */
export function setupTutorialPage() {
  // 1. Handle missing tutorial missing images gracefully (CSP Compliant fallback)
  const tutorialImages = document.querySelectorAll(".tutorial-img");
  if (tutorialImages.length > 0) {
    tutorialImages.forEach(img => {
      // Create a fallback message matching the original inline script logic
      img.addEventListener('error', function() {
        const card = this.closest('.tutorial-doc-card');
        
        // Extract original filename for the fallback text, e.g., 'step_1.png'
        const filename = this.src.substring(this.src.lastIndexOf('/') + 1);
        
        // Replace image element with text string
        const fallbackText = document.createTextNode(`Add tutorial_images/${filename}`);
        this.replaceWith(fallbackText);
        
        // Apply missing style to card
        if (card) {
          card.classList.add('missing');
        }
      });
      
      // If image is already broken before JS loads (e.g. cached fail), trigger manually
      if (img.complete && img.naturalHeight === 0) {
        img.dispatchEvent(new Event('error'));
      }
    });
  }

  // 2. Activation of tab navigation on tutorial page
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
