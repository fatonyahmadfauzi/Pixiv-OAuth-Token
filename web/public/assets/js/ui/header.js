export function initializeHeader() {
  const headerEl = document.querySelector("header.tutorial-docs-header");
  if (!headerEl) return;

  const pageLabel = headerEl.getAttribute("data-page-label") || "",
    pageLabelI18n = headerEl.getAttribute("data-page-i18n") || "",
    brandHref = headerEl.getAttribute("data-brand-href") || "/",
    showLangSwitcher = headerEl.getAttribute("data-lang-switcher") === "true",
    navAttr = headerEl.getAttribute("data-nav") || "";

  const HEADER_HTML =
      '<div class="tutorial-docs-inner"><div class="tutorial-docs-top"><a class="tutorial-docs-brand" href="' +
      brandHref +
      '"><strong>Pixiv OAuth</strong>' +
      (pageLabel
        ? "<span" +
          (pageLabelI18n ? ' data-i18n="' + pageLabelI18n + '"' : "") +
          ">" +
          pageLabel +
          "</span>"
        : "") +
      '</a><nav class="tutorial-docs-actions" aria-label="Main navigation"><div class="sidebar-header"><a class="sidebar-brand" href="' +
      brandHref +
      '"><strong>Pixiv OAuth</strong></a> <button class="close-sidebar" aria-label="Close menu"><i class="bi bi-x-lg" aria-hidden="true"></i></button></div>' +
      [
        {
          id: "navConsole",
          href: navAttr === "navConsole" ? "#console" : "/#console",
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
      ].map(function (link) {
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
        .join(" ") +
      "</nav>" +
      (showLangSwitcher
        ? '\n    <div class="lang-wrap">\n      <div class="lang-control" id="langControl">\n        <button type="button" id="langToggle" class="lang-toggle" aria-haspopup="listbox" aria-expanded="false">\n          <span id="langFlag" class="fi fi-gb" aria-hidden="true"></span>\n          <span id="langCurrent">English</span>\n          <i class="bi bi-chevron-down" aria-hidden="true"></i>\n        </button>\n        <ul id="langMenu" class="lang-menu" role="listbox" aria-label="Language">\n          <li role="option" data-lang="en"><span class="fi fi-gb" aria-hidden="true"></span><span>English</span></li>\n          <li role="option" data-lang="pl"><span class="fi fi-pl" aria-hidden="true"></span><span>Polski</span></li>\n          <li role="option" data-lang="zh"><span class="fi fi-cn" aria-hidden="true"></span><span>中文</span></li>\n          <li role="option" data-lang="jp"><span class="fi fi-jp" aria-hidden="true"></span><span>日本語</span></li>\n          <li role="option" data-lang="de"><span class="fi fi-de" aria-hidden="true"></span><span>Deutsch</span></li>\n          <li role="option" data-lang="fr"><span class="fi fi-fr" aria-hidden="true"></span><span>Français</span></li>\n          <li role="option" data-lang="es"><span class="fi fi-es" aria-hidden="true"></span><span>Español</span></li>\n          <li role="option" data-lang="ru"><span class="fi fi-ru" aria-hidden="true"></span><span>Русский</span></li>\n          <li role="option" data-lang="pt"><span class="fi fi-pt" aria-hidden="true"></span><span>Português</span></li>\n          <li role="option" data-lang="id"><span class="fi fi-id" aria-hidden="true"></span><span>Indonesia</span></li>\n          <li role="option" data-lang="kr"><span class="fi fi-kr" aria-hidden="true"></span><span>한국어</span></li>\n        </ul>\n      </div>\n    </div>'
        : "") +
      '<button class="menu-toggle" id="menuToggle" aria-label="Toggle menu"><i class="bi bi-list" aria-hidden="true"></i></button></div></div><div class="sidebar-overlay" id="sidebarOverlay"></div>';
  headerEl.innerHTML = HEADER_HTML;
}