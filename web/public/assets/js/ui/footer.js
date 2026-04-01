/**
 * Footer Component
 * Injects the shared site footer HTML into the page.
 */

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
      </div>
      <div class="footer-social-section">
        <h4 id="footerContactTitle" data-i18n="footerContactTitle">Social</h4>
        <div class="footer-social-icons">
          <a href="https://github.com/fatonyahmadfauzi" target="_blank" rel="noopener" aria-label="GitHub"><i class="bi bi-github"></i></a>
          <a href="https://www.linkedin.com/in/fatonyahmadfauzi" target="_blank" rel="noopener" aria-label="LinkedIn"><i class="bi bi-linkedin"></i></a>
        </div>
      </div>
      <div class="footer-brand-block">
        <span class="footer-ghost-text" data-i18n="footerBrandText">Pixiv OAuth</span>
      </div>
      <p class="footer-copyright" data-i18n="footerCopyright">© 2025 Pixiv OAuth Web · Built by Fatony Ahmad Fauzi</p>
    </div>
`;

export function initializeFooter() {
  const foot = document.getElementById("mainFooter") || document.querySelector(".site-footer");
  if (foot) foot.innerHTML = SITE_FOOTER_HTML;
}
