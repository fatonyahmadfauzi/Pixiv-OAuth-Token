(function () {
  // Read config from the <script> tag that loaded this file
  var scriptEl = document.currentScript;
  var pageLabel = (scriptEl && scriptEl.getAttribute("data-page-label")) || "";
  var pageLabelI18n =
    (scriptEl && scriptEl.getAttribute("data-page-i18n")) || "";
  var brandHref = (scriptEl && scriptEl.getAttribute("data-brand-href")) || "/";
  var showLangSwitcher =
    (scriptEl && scriptEl.getAttribute("data-lang-switcher")) === "true";

  // Nav links per-page (all pages use the same set but one is "active")
  // Each page customises via data-nav on the script tag, e.g. data-nav="downloads,tutorial"
  var navAttr = (scriptEl && scriptEl.getAttribute("data-nav")) || "";
  var activeNavs = navAttr ? navAttr.split(",") : [];

  var NAV_LINKS = [
    {
      id: "navHomepageLabel",
      href: "/",
      i18n: "navHomepageLabel",
      label: "Homepage",
    },
    {
      id: "navConsole",
      href: "/#console",
      i18n: "navConsole",
      label: "Console",
    },
    {
      id: "navDownloads",
      href: "/downloads",
      i18n: "navDownloads",
      label: "Download",
    },
    {
      id: "navTutorial",
      href: "/tutorial",
      i18n: "navTutorial",
      label: "Tutorial",
    },
  ];

  // Build nav links HTML (exclude the ones listed in data-nav / activeNavs so each page hides its own link)
  var navLinksHTML = NAV_LINKS.filter(function (link) {
    return activeNavs.indexOf(link.id) === -1;
  })
    .map(function (link) {
      return (
        '<a id="' +
        link.id +
        '" href="' +
        link.href +
        '" data-i18n="' +
        link.i18n +
        '">' +
        link.label +
        "</a>"
      );
    })
    .join(" ");

  // Language switcher — only on index.html (home page)
  var langSwitcherHTML = showLangSwitcher
    ? `
    <div class="lang-wrap">
      <div class="lang-control" id="langControl">
        <button type="button" id="langToggle" class="lang-toggle" aria-haspopup="listbox" aria-expanded="false">
          <span id="langFlag" class="fi fi-gb" aria-hidden="true"></span>
          <span id="langCurrent">English</span>
          <i class="bi bi-chevron-down" aria-hidden="true"></i>
        </button>
        <ul id="langMenu" class="lang-menu" role="listbox" aria-label="Language">
          <li role="option" data-lang="en"><span class="fi fi-gb" aria-hidden="true"></span><span>English</span></li>
          <li role="option" data-lang="pl"><span class="fi fi-pl" aria-hidden="true"></span><span>Polski</span></li>
          <li role="option" data-lang="zh"><span class="fi fi-cn" aria-hidden="true"></span><span>中文</span></li>
          <li role="option" data-lang="jp"><span class="fi fi-jp" aria-hidden="true"></span><span>日本語</span></li>
          <li role="option" data-lang="de"><span class="fi fi-de" aria-hidden="true"></span><span>Deutsch</span></li>
          <li role="option" data-lang="fr"><span class="fi fi-fr" aria-hidden="true"></span><span>Français</span></li>
          <li role="option" data-lang="es"><span class="fi fi-es" aria-hidden="true"></span><span>Español</span></li>
          <li role="option" data-lang="ru"><span class="fi fi-ru" aria-hidden="true"></span><span>Русский</span></li>
          <li role="option" data-lang="pt"><span class="fi fi-pt" aria-hidden="true"></span><span>Português</span></li>
          <li role="option" data-lang="id"><span class="fi fi-id" aria-hidden="true"></span><span>Indonesia</span></li>
          <li role="option" data-lang="kr"><span class="fi fi-kr" aria-hidden="true"></span><span>한국어</span></li>
        </ul>
      </div>
    </div>`
    : "";

  // Brand label span (e.g. "TUTORIAL", "DOWNLOAD", etc.)
  var brandLabelHTML = pageLabel
    ? "<span" +
      (pageLabelI18n ? ' data-i18n="' + pageLabelI18n + '"' : "") +
      ">" +
      pageLabel +
      "</span>"
    : "";

  var HEADER_HTML =
    '<div class="tutorial-docs-inner">' +
    '<div class="tutorial-docs-top">' +
    '<a class="tutorial-docs-brand" href="' +
    brandHref +
    '">' +
    "<strong>Pixiv OAuth</strong>" +
    brandLabelHTML +
    "</a>" +
    '<nav class="tutorial-docs-actions" aria-label="Main navigation">' +
    '<div class="sidebar-header">' +
    '<a class="sidebar-brand" href="' +
    brandHref +
    '"><strong>Pixiv OAuth</strong></a> ' +
    '<button class="close-sidebar" aria-label="Close menu"><i class="bi bi-x-lg" aria-hidden="true"></i></button>' +
    "</div>" +
    navLinksHTML +
    "</nav>" +
    langSwitcherHTML +
    '<button class="menu-toggle" id="menuToggle" aria-label="Toggle menu">' +
    '<i class="bi bi-list" aria-hidden="true"></i>' +
    "</button>" +
    "</div>" +
    "</div>" +
    '<div class="sidebar-overlay" id="sidebarOverlay"></div>';

  var headerEl = document.querySelector("header.tutorial-docs-header");
  if (headerEl) {
    headerEl.innerHTML = HEADER_HTML;
  }
})();
