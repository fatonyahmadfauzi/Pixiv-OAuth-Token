import {
  t,
  DISPLAY_LANG,
  LANG_ORDER,
  FLAG_CLASS,
  LANG_NAME,
  setDisplayLanguage,
} from "./i18n.js";

/**
 * DOM Utils Module
 * DOM manipulation and element fetching helpers
 */

/**
 * Shorthand for document.getElementById
 * @param {string} id
 * @returns {HTMLElement | null}
 */
export const q = (id) => document.getElementById(id);

/**
 * Escapes HTML characters to prevent XSS.
 * @param {string} str
 * @returns {string}
 */
export function escapeHtml(str) {
  if (typeof str !== "string") return str;
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

/**
 * Update language flags in the DOM
 */
export function updateLangFlag() {
  const el = document.getElementById("langFlag"),
    current = document.getElementById("langCurrent");
  if (el) el.className = `fi ${FLAG_CLASS[DISPLAY_LANG] || "fi-gb"}`;
  if (current) current.textContent = LANG_NAME[DISPLAY_LANG] || "English";

  document.querySelectorAll("#langMenu li").forEach((li) => {
    li.classList.toggle("active", li.dataset.lang === DISPLAY_LANG);
  });
}

export function updateNavLinks() {
  document.querySelectorAll("a").forEach((a) => {
    let e = a.getAttribute("href");
    if (
      !e ||
      e.startsWith("http") ||
      e.startsWith("mailto:") ||
      e.startsWith("#")
    )
      return;
    if (!e.startsWith("/")) return;

    let rawPath = a.getAttribute("data-raw-href");
    if (!rawPath) {
      const parts = e.split("/").filter(Boolean);
      if (parts.length > 0 && LANG_ORDER.includes(parts[0])) {
        parts.shift();
      }
      rawPath = "/" + parts.join("/");
      a.setAttribute("data-raw-href", rawPath);
    }

    const t = window.location.pathname.split("/").filter(Boolean),
      i = t.length > 0 && LANG_ORDER.includes(t[0]);

    if ("en" === DISPLAY_LANG && !i) {
      a.href = rawPath;
      return;
    }

    const o = "/" === rawPath ? "" : rawPath;
    a.href = "/" + DISPLAY_LANG + o;
  });
}

/**
 * Traverse the DOM replacing strings based on locale
 */
export function applyLang() {
  updateNavLinks();

  // Specific IDs
  Object.entries({
    kickerText: "kicker",
    titleText: "title",
    subtitleText: "subtitle",
    badgePkce: "badgePkce",
    badgeDeploy: "badgeDeploy",
    badgeRelease: "badgeRelease",
    docsBtnLabel: "docs",
    oauthTitle: "oauthTitle",
    openLoginBtnLabel: "open",
    openLoginBtnLabel2: "open",
    exchangeBtnLabel: "exchange",
    refreshBtnLabel: "refresh",
    resultTitle: "result",
    copyAccessBtnLabel: "copyAccess",
    copyRefreshBtnLabel: "copyRefresh",
    footerContactTitle: "contact",
    downloadsTitle: "downloadsTitle",
    downloadsDesc: "downloadsDesc",
    quickCmdTitle: "quickCmdTitle",
    quickCmdDesc: "quickCmdDesc",
    copyPsBtnLabel: "copyPs",
    copyCmdBtnLabel: "copyCmd",
    copyPipBtnLabel: "copyPip",
    navHomepageLabel: "navHomepage",
    navConsole: "navConsole",
    navDownloads: "navDownloads",
    navQuickCmd: "navQuickCmd",
    navTutorial: "navTutorial",
    downloadsTabLabel: "downloadsTitle",
    quickCmdTabLabel: "quickCmdTitle",
    needVisualGuideText: "needVisualGuide",
    tutorialCtaBtnLabel: "openTutorialPage",
    windowsPreviewBadge: "windowsPreviewBadge",
    windowsPreviewTitle: "windowsPreviewTitle",
    windowsPreviewDesc: "windowsPreviewDesc",
    cliPreviewBadge: "cliPreviewBadge",
    cliPreviewTitle: "cliPreviewTitle",
    cliPreviewDesc: "cliPreviewDesc",
    downloadsCtaBtnLabel: "openDownloadsPage",
    tutorialTabStart: "tutorialTabStart",
    tutorialTabSteps: "tutorialTabSteps",
    tutorialTabTips: "tutorialTabTips",
    tutorialPageTitle: "tutorialPageTitle",
    tutorialPageDesc: "tutorialPageDesc",
    tutorialStepsTitle: "tutorialStepsTitle",
    tutorialBackBtnLabel: "tutorialBackBtn",
    cliPreviewFigure: "cliPreviewFigure",
    downloadsDedicatedDesc: "downloadsDedicatedDesc",
    tutorialStep1Title: "tutorialStep1Title",
    tutorialStep1Desc: "tutorialStep1Desc",
    tutorialStep2Title: "tutorialStep2Title",
    tutorialStep2Desc: "tutorialStep2Desc",
    tutorialStep3Title: "tutorialStep3Title",
    tutorialStep3Desc: "tutorialStep3Desc",
    tutorialStep4Title: "tutorialStep4Title",
    tutorialStep4Desc: "tutorialStep4Desc",
    tutorialStep5Title: "tutorialStep5Title",
    tutorialStep5Desc: "tutorialStep5Desc",
    tutorialStep6Title: "tutorialStep6Title",
    tutorialStep6Desc: "tutorialStep6Desc",
    footerProductTitle: "footerProductTitle",
    footerHomeLink: "footerHomeLink",
    footerDownloadLink: "footerDownloadLink",
    footerTutorialLink: "footerTutorialLink",
    footerSourceLink: "footerSourceLink",
    footerResourceTitle: "footerResourceTitle",
    footerDocsLink: "footerDocsLink",
    footerPixivLink: "footerPixivLink",
    footerPythonLink: "footerPythonLink",
    footerVercelLink: "footerVercelLink",
    footerSupportTitle: "footerSupportTitle",
    footerIssueLink: "footerIssueLink",
    footerDiscussLink: "footerDiscussLink",
    footerDevLink: "footerDevLink",
    dlCatAgent: "dlCatAgent",
    dlSidebarWin: "dlSidebarWin",
    dlCatSdk: "dlCatSdk",
    dlSidebarPy: "dlSidebarPy",
    dlBadgeWin: "dlBadgeWin",
    dlTitleWin: "dlTitleWin",
    dlInstallWin: "dlInstallWin",
    dlTabDl: "dlTabDl",
    dlTabPs: "dlTabPs",
    dlTabCmd: "dlTabCmd",
    dlDescWin1: "dlDescWin1",
    dlDescWinHelp: "dlDescWinHelp",
    dlDescPs: "dlDescPs",
    dlDescCmd: "dlDescCmd",
    dlBadgePy: "dlBadgePy",
    dlTitlePy: "dlTitlePy",
    navHeaderContact: "navHeaderContact",
    navHeaderIssues: "navHeaderIssues",
    navHeaderDiscuss: "navHeaderDiscuss",
    navHeaderDocs: "navHeaderDocs",
    navHeaderLicense: "navHeaderLicense",
    contactUsTitle: "contactUsTitle",
    contactUsDesc: "contactUsDesc",
    contactSuccessTitle: "contactSuccessTitle",
    contactSuccessDesc: "contactSuccessDesc",
    contactFirstName: "contactFirstName",
    contactLastName: "contactLastName",
    contactEmail: "contactEmail",
    contactAttachment: "contactAttachment",
    contactFileLimit: "contactFileLimit",
    contactMessage: "contactMessage",
    contactSendBtn: "contactSendBtn",
    reportPageTitle: "reportPageTitle",
    reportPageDesc: "reportPageDesc",
    discussPageTitle: "discussPageTitle",
    discussPageDesc: "discussPageDesc",
    discussViewBtn: "discussViewBtn",
    discussQaTitle: "discussQaTitle",
    discussQaDesc: "discussQaDesc",
    discussIdeasTitle: "discussIdeasTitle",
    discussIdeasDesc: "discussIdeasDesc",
    discussGeneralTitle: "discussGeneralTitle",
    discussGeneralDesc: "discussGeneralDesc",
    docsPageTitle: "docsPageTitle",
    docsPageDesc: "docsPageDesc",
    docsLoadingLabel: "docsLoadingLabel",
    docsErrorLabel: "docsErrorLabel",
    licensePageTitle: "licensePageTitle",
    licensePageDesc: "licensePageDesc",
    notFoundTitle: "notFoundTitle",
    notFoundSubtitle: "notFoundSubtitle",
    notFoundDesc: "notFoundDesc",
    notFoundBackHome: "notFoundBackHome",
    notFoundBackPrev: "notFoundBackPrev",
    dlMinReqWinTitle: "dlMinReqWinTitle",
    dlMinReqWin1: "dlMinReqWin1",
    dlMinReqWin2: "dlMinReqWin2",
    dlMinReqWin3: "dlMinReqWin3",
    dlMinReqPyTitle: "dlMinReqPyTitle",
    dlMinReqPy1: "dlMinReqPy1",
    dlMinReqPy2: "dlMinReqPy2",
    dlMinReqPy3: "dlMinReqPy3",
    dlMinReqPy4: "dlMinReqPy4",
    dlInstallPy: "dlInstallPy",
    dlDescPyDirect: "dlDescPyDirect",
    dlPyDirectWinTitle: "dlPyDirectWinTitle",
    dlPyDirectLinuxTitle: "dlPyDirectLinuxTitle",
    dlPyClone: "dlPyClone",
    dlPyOpen: "dlPyOpen",
    dlPyVenv: "dlPyVenv",
    dlPyReqs: "dlPyReqs",
    dlPyRun: "dlPyRun",
  }).forEach(([id, key]) => {
    const el = document.getElementById(id);
    if (el) el.textContent = t(key);
  });

  // data-i18n tags
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    const translated = t(key);
    if (!translated || translated === key) return;
    const firstTextNode = Array.from(el.childNodes).find(
      (n) => n.nodeType === Node.TEXT_NODE,
    );
    if (firstTextNode) {
      firstTextNode.textContent = translated + " ";
    } else {
      el.textContent = translated;
    }
  });

  // data-i18n-html tags
  document.querySelectorAll("[data-i18n-html]").forEach((el) => {
    const key = el.getAttribute("data-i18n-html");
    const translated = t(key, { file: el.dataset.file || "" });
    if (el.innerHTML !== translated) el.innerHTML = translated;
  });

  // placeholders
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const key = el.getAttribute("data-i18n-placeholder");
    const translated = t(key);
    if (translated && translated !== key) el.placeholder = translated;
  });

  const inputCode = document.getElementById("inputCode");
  if (inputCode) inputCode.placeholder = t("placeholder");

  const output = document.getElementById("output");
  if (output && output.textContent === "Ready.")
    output.textContent = t("ready");

  const cliToggleBtn = document.getElementById("cliToggleBtn");
  if (cliToggleBtn) {
    const expanded = document
      .getElementById("cliPreviewBox")
      ?.classList.contains("expanded");
    cliToggleBtn.textContent = t(expanded ? "showLess" : "showMore");
  }

  const footerVersion = document.getElementById("footerVersion");
  if (footerVersion && footerVersion.dataset.version) {
    footerVersion.textContent = t("footerVersion", {
      version: footerVersion.dataset.version,
    });
  }

  updateLangFlag();
  document.dispatchEvent(new CustomEvent("lang-applied"));
}
