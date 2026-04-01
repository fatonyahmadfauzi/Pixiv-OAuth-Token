import { initLocaleRouting } from "./seo/locale-routing.js";
import { injectSchema } from "./seo/schema.js";
import { initMetaTags } from "./seo/meta.js";
import { initHreflangTags } from "./seo/hreflang.js";
import { applyLang } from "./core/dom.js";
import { setupLanguageMenu } from "./ui/language-switcher.js";
import { setupMobileSidebar } from "./ui/sidebar.js";
import { setupHelpWidget } from "./ui/help-widget.js";
import { setupOAuthConsole } from "./oauth/token-actions.js";
import { setupCustomFileInput, setupCliPreviewToggle } from "./pages/home.js";
import {
    setupMobilePlatformDropdown,
    setupDownloadCategorySwitch,
    setupDownloadTabs,
    setupArchDownloadRows,
    setupCommandCopyButtons,
    hydrateReleaseAssets
} from "./pages/downloads.js";
import { initializeHeader } from "./ui/header.js";
import { initializeFooter } from "./ui/footer.js";
import { setupIssuesPage } from "./pages/issues.js";
import { setupDocsPage } from "./pages/docs.js";
import { setupLicensePage } from "./pages/license.js";
import { setupChangelogPage } from "./pages/changelog.js";
import { setupTutorialPage } from "./pages/tutorial.js";

/**
 * Main application orchestrator
 */
document.addEventListener("DOMContentLoaded", async () => {
    // 1. Inject HTML layouts
    initializeHeader();
    initializeFooter();
    setupHelpWidget();
    injectSchema();

    // 2. Decide locale based on routing and local storage
    initLocaleRouting();
    initMetaTags();
    initHreflangTags();

    // 3. Setup core UI and interaction
    setupLanguageMenu();
    setupMobileSidebar();

    // 4. Apply i18n translations to DOM
    applyLang();

    // 5. Setup OAuth console hooks
    setupOAuthConsole();

    // 6. Page-specific scripts (return silently if DOM elements are absent)
    setupCustomFileInput();
    setupCliPreviewToggle();
    setupMobilePlatformDropdown();
    setupDownloadCategorySwitch();
    setupDownloadTabs();
    setupArchDownloadRows();
    setupCommandCopyButtons();
    setupIssuesPage();
    setupDocsPage();
    setupLicensePage();
    setupChangelogPage();
    setupTutorialPage();

    // 7. Hydrate API calls
    try {
        await hydrateReleaseAssets();
    } catch (e) {
        console.error("Failed to hydrate release assets", e);
    }
});
