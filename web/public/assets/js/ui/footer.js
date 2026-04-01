/**
 * Footer Component
 * Injects the shared site footer HTML into the page.
 */
import { t } from "../core/i18n.js";

const SITE_FOOTER_HTML = `
    <div class="footer-inner">
      <div class="footer-columns">
        <section class="footer-col" id="footerProductCol">
          <h4 id="footerProductTitle" data-i18n="footerProductTitle">Product</h4>
          <ul>
            <li><a href="/" id="footerHomeLink" data-i18n="footerHomeLink">Homepage</a></li>
            <li><a href="/downloads" id="footerDownloadLink" data-i18n="footerDownloadLink">Downloads</a></li>
            <li><a href="/tutorial" id="footerTutorialLink" data-i18n="footerTutorialLink">Tutorial</a></li>
            <li><a href="https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token" target="_blank" rel="noopener" id="footerSourceLink" data-i18n="footerSourceLink">Source Code</a></li>
          </ul>
        </section>
        <section class="footer-col" id="footerResourceCol">
          <h4 id="footerResourceTitle" data-i18n="footerResourceTitle">Resources &amp; Docs</h4>
          <ul>
            <li><a href="/documentation" id="footerDocsLink" data-i18n="footerDocsLink">Documentation</a></li>
            <li><a href="/changelog" id="footerChangelogLink" data-i18n="footerChangelogLink">Changelog</a></li>
            <li><a href="/license" data-i18n="footerLicenseLink">License</a></li>
            <li><a href="/privacy-policy" data-i18n="footerPrivacy">Privacy Policy</a></li>
            <li><a href="/terms-conditions" data-i18n="footerTerms">Terms &amp; Conditions</a></li>
            <li><a href="https://oauth.secure.pixiv.net/auth/token" target="_blank" rel="noopener" id="footerPixivLink" data-i18n="footerPixivLink">Pixiv OAuth Endpoint</a></li>
            <li><a href="https://www.python.org/" target="_blank" rel="noopener" id="footerPythonLink" data-i18n="footerPythonLink">Python 3.11+</a></li>
            <li><a href="https://vercel.com/" target="_blank" rel="noopener" id="footerVercelLink" data-i18n="footerVercelLink">Deployed on Vercel</a></li>
          </ul>
        </section>
        <section class="footer-col" id="footerSupportCol">
          <h4 id="footerSupportTitle" data-i18n="footerSupportTitle">Support</h4>
          <ul>
            <li><a href="/contact" data-i18n="footerContactLink">Contact Us</a></li>
            <li><a href="/issues" id="footerIssueLink" data-i18n="footerIssueLink">Report an Issue</a></li>
            <li><a href="/discussions" id="footerDiscussLink" data-i18n="footerDiscussLink">Discussions</a></li>
            <li><a href="https://github.com/fatonyahmadfauzi" target="_blank" rel="noopener" id="footerDevLink" data-i18n="footerDevLink">Fatony Ahmad Fauzi</a></li>
            <li><a href="/support" id="footerDonateLink" data-i18n="footerDonateLink">Support / Donate</a></li>
          </ul>
        </section>
        <section class="footer-col footer-social-col" id="footerSocialCol">
          <h4 id="footerContactTitle" data-i18n="footerContactTitle">Social</h4>
          <ul>
            <li><a href="https://github.com/fatonyahmadfauzi" target="_blank" rel="noopener"><i class="bi bi-github footer-inline-icon"></i>GitHub</a></li>
            <li><a href="https://www.linkedin.com/in/fatonyahmadfauzi" target="_blank" rel="noopener"><i class="bi bi-linkedin footer-inline-icon"></i>LinkedIn</a></li>
          </ul>
        </section>
      </div>
      <p class="footer-disclaimer" id="footerDisclaimer" data-i18n="footerDisclaimer">Pixiv OAuth Token is an independent open-source project and is not affiliated with Pixiv Inc.</p>
      <p class="footer-version" id="footerVersion"></p>
      <p class="footer-copyright" data-i18n="footerCopyright">© 2025 Pixiv OAuth Web · Built by Fatony Ahmad Fauzi</p>
    </div>
`;

async function updateFooterVersion() {
  const versionEl = document.getElementById("footerVersion");
  if (!versionEl) return;

  let versionText = "v0.0.0";
  try {
    const response = await fetch("/version.json", { cache: "no-store" });
    if (response.ok) {
      const data = await response.json();
      if (data && typeof data.version === "string" && data.version.trim()) {
        versionText = `v${data.version.replace(/^v/i, "")}`;
      }
    }
  } catch (_) {
    // Keep fallback value when version file is unavailable.
  }

  versionEl.dataset.version = versionText;
  versionEl.textContent = t("footerVersion", { version: versionText });
}

export function initializeFooter() {
  const foot =
    document.getElementById("mainFooter") ||
    document.querySelector(".site-footer");
  if (foot) {
    foot.innerHTML = SITE_FOOTER_HTML;
    updateFooterVersion();
  }
}
