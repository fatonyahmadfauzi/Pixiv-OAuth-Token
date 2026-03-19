const SITE_FOOTER_HTML = `
    <div class="footer-inner">
      <div class="footer-columns">
        <section class="footer-col" id="footerProductCol">
          <h4 id="footerProductTitle">Product</h4>
          <ul>
            <li><a href="/" id="footerHomeLink">Homepage</a></li>
            <li><a href="/downloads" id="footerDownloadLink">Downloads</a></li>
            <li><a href="/tutorial" id="footerTutorialLink">Tutorial</a></li>
            <li><a href="https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token" target="_blank" rel="noopener" id="footerSourceLink">Source Code</a></li>
          </ul>
        </section>
        <section class="footer-col" id="footerResourceCol">
          <h4 id="footerResourceTitle">Resources &amp; Docs</h4>
          <ul>
            <li><a href="/documentation" id="footerDocsLink">Documentation</a></li>
            <li><a href="/license" data-i18n="footerLicenseLink">License</a></li>
            <li><a href="https://oauth.secure.pixiv.net/auth/token" target="_blank" rel="noopener" id="footerPixivLink">Pixiv OAuth Endpoint</a></li>
            <li><a href="https://www.python.org/" target="_blank" rel="noopener" id="footerPythonLink">Python 3.11+</a></li>
            <li><a href="https://vercel.com/" target="_blank" rel="noopener" id="footerVercelLink">Deployed on Vercel</a></li>
          </ul>
        </section>
        <section class="footer-col" id="footerSupportCol">
          <h4 id="footerSupportTitle">Support</h4>
          <ul>
            <li><a href="/contact" data-i18n="footerContactLink">Contact Us</a></li>
            <li><a href="/issues" id="footerIssueLink">Report an Issue</a></li>
            <li><a href="/discussions" id="footerDiscussLink">Discussions</a></li>
            <li><a href="https://github.com/fatonyahmadfauzi" target="_blank" rel="noopener" id="footerDevLink">Fatony Ahmad Fauzi</a></li>
            <li><a href="https://teer.id/fatonyahmadfauzi" target="_blank" rel="noopener" id="footerDonateLink">Support / Donate</a></li>
          </ul>
        </section>
      </div>
      <div class="footer-social-section">
        <h4 id="footerContactTitle">Social</h4>
        <div class="footer-social-icons">
          <a href="https://github.com/fatonyahmadfauzi" target="_blank" rel="noopener" aria-label="GitHub"><i class="bi bi-github"></i></a>
          <a href="https://www.linkedin.com/in/fatonyahmadfauzi" target="_blank" rel="noopener" aria-label="LinkedIn"><i class="bi bi-linkedin"></i></a>
        </div>
      </div>
      <div class="footer-brand-block">
        <span class="footer-ghost-text">Pixiv OAuth</span>
      </div>
      <p class="footer-copyright">© 2025 Pixiv OAuth Web · Built by Fatony Ahmad Fauzi</p>
    </div>
`;
const foot = document.getElementById('mainFooter') || document.querySelector('.site-footer');
if (foot) {
    foot.innerHTML = SITE_FOOTER_HTML;
}
