#!/usr/bin/env node
const fs = require("fs");
const path = require("path");

const PUBLIC_DIR = path.join(__dirname, "../public");
const I18N_JS_PATH = path.join(PUBLIC_DIR, "assets/js/core/i18n.js");

const LANG_ORDER = [
  "de",
  "en",
  "es",
  "fr",
  "id",
  "jp",
  "kr",
  "pl",
  "pt",
  "ru",
  "zh",
];
const SEO_MAP = { jp: "ja", kr: "ko" };

// Correct IETF region codes for og:locale
const LOCALE_REGION_MAP = {
  de: "de_DE",
  en: "en_US",
  es: "es_ES",
  fr: "fr_FR",
  id: "id_ID",
  jp: "ja_JP",
  kr: "ko_KR",
  pl: "pl_PL",
  pt: "pt_PT",
  ru: "ru_RU",
  zh: "zh_CN",
};

function getLangCode(folder) {
  return SEO_MAP[folder] || folder;
}

function getOgLocale(folder) {
  if (!folder) return "en_US";
  return LOCALE_REGION_MAP[folder] || `${getLangCode(folder)}_${getLangCode(folder).toUpperCase()}`;
}

// 1. Extract Translations from i18n.js to populate SEO Metadata safely.
function getTranslations() {
  const code = fs.readFileSync(I18N_JS_PATH, "utf8");
  const match = code.match(/export\s+const\s+DISPLAY_LANGUAGES\s*=\s*\{/);
  if (!match) throw new Error("Could not find DISPLAY_LANGUAGES in i18n.js");

  const startObj = code.indexOf("{", match.index);
  let braceCount = 0;
  let inString = false;
  let escape = false;
  let endIdx = -1;

  for (let i = startObj; i < code.length; i++) {
    const char = code[i];
    if (escape) {
      escape = false;
      continue;
    }
    if (char === "\\") {
      escape = true;
      continue;
    }
    if (char === '"' || char === "'") {
      if (inString === char) inString = false;
      else if (!inString) inString = char;
    }
    if (!inString) {
      if (char === "{") braceCount++;
      if (char === "}") {
        braceCount--;
        if (braceCount === 0) {
          endIdx = i;
          break;
        }
      }
    }
  }

  const objStr = code.substring(startObj, endIdx + 1);
  return new Function("return " + objStr)();
}

const translations = getTranslations();

// 2. Discover all base HTML files in public/
const htmlFiles = fs
  .readdirSync(PUBLIC_DIR)
  .filter(
    (f) =>
      f.endsWith(".html") && fs.statSync(path.join(PUBLIC_DIR, f)).isFile(),
  );

// 3. Generate Hreflang Tags Block
function generateHreflangs(fileName) {
  let relativeUrl =
    fileName === "index.html" ? "" : fileName.replace(".html", "");
  let tags = [];

  // Root level (x-default)
  tags.push(
    `<link rel="alternate" hreflang="x-default" href="https://pixiv-o-auth-token.vercel.app/${relativeUrl}" />`,
  );

  for (const locale of LANG_ORDER) {
    const langCode = getLangCode(locale);
    const pathUrl = relativeUrl ? `${locale}/${relativeUrl}` : `${locale}/`;
    tags.push(
      `<link rel="alternate" hreflang="${langCode}" href="https://pixiv-o-auth-token.vercel.app/${pathUrl}" />`,
    );
  }
  return tags.join("\n    ");
}

// 4. Generate JSON-LD Schema
function generateJsonLd(locale, seoLang, pageUrl, trans, titleVal, descVal) {
  let jsonString = `
    {
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "name": "${titleVal.replace(/"/g, '\\"')}",
      "description": "${descVal.replace(/"/g, '\\"')}",
      "inLanguage": "${seoLang}",
      "url": "${pageUrl}",
      "applicationCategory": "DeveloperApplication",
      "operatingSystem": "Web, Windows"
    }`;
  return `<script type="application/ld+json">${jsonString}</script>`;
}

// Helper to get page-specific SEO metadata
function getPageMetaData(fileName, trans) {
  const baseName = fileName.replace(".html", "");
  let pageTitle = trans.title || "Pixiv OAuth";
  let pageDesc = trans.subtitle || "Toolkit to generate and refresh Pixiv OAuth tokens";

  switch (baseName) {
    case "index":
      pageTitle = trans.title || "Pixiv OAuth";
      pageDesc = trans.subtitle || "Toolkit to generate and refresh Pixiv OAuth tokens";
      break;
    case "downloads":
      pageTitle = trans.downloadsTitle || "Downloads";
      pageDesc = trans.downloadsDesc || "Download latest build directly from GitHub Releases.";
      break;
    case "tutorial":
      pageTitle = trans.tutorialTitle || "Tutorial";
      pageDesc = trans.tutorialDesc || "Steps to guide users from login to token exchange.";
      break;
    case "contact":
      pageTitle = trans.contactUsTitle || "Contact Us";
      pageDesc = trans.contactUsDesc || "Have questions, suggestions, or need help?";
      break;
    case "issues":
      pageTitle = trans.reportPageTitle || "Report an Issue";
      pageDesc = trans.reportPageDesc || "Browse open issues or submit a new one.";
      break;
    case "discussions":
      pageTitle = trans.discussPageTitle || "Discussions";
      pageDesc = trans.discussPageDesc || "Join our community on GitHub Discussions.";
      break;
    case "documentation":
      pageTitle = trans.docsPageTitle || "Documentation";
      pageDesc = trans.docsPageDesc || "Read the project documentation.";
      break;
    case "changelog":
      pageTitle = trans.changelogPageTitle || "Changelog";
      pageDesc = trans.overviewDesc || "Project overview and history.";
      break;
    case "license":
      pageTitle = trans.licensePageTitle || "License";
      pageDesc = trans.licensePageDesc || "This project is licensed under the MIT License.";
      break;
    case "privacy-policy":
      pageTitle = trans.privacyTitle || "Privacy Policy";
      pageDesc = trans.privacyIntro || "Independent open-source utility for Pixiv OAuth.";
      break;
    case "terms-conditions":
      pageTitle = trans.termsTitle || "Terms & Conditions";
      pageDesc = trans.termsIntro || "By using this website and tool, you agree to these terms.";
      break;
    case "support":
      pageTitle = trans.supportPageTitle || "Support / Donate";
      pageDesc = trans.supportPageDescHtml
        ? trans.supportPageDescHtml.replace(/<[^>]+>/g, "")
        : "Thank you for supporting this project!";
      break;
    case "404":
      pageTitle = trans.notFoundTitle || "404";
      pageDesc = trans.notFoundDesc || "Page Not Found";
      break;
    case "enable-javascript":
      // Use translated title if available, else fallback
      pageTitle = trans.notFoundSubtitle ? "JavaScript Required" : "JavaScript Required";
      pageDesc = "Please enable JavaScript to use Pixiv OAuth Web.";
      break;
  }

  let titleVal = `${pageTitle} | Pixiv OAuth`;
  if (baseName === "index") {
    titleVal = `${pageTitle} | Professional Token Helper`;
  }
  return { titleVal, descVal: pageDesc };
}

// 5. Process HTML files
function processFile(filePath, fileName, localeFolder) {
  let content = fs.readFileSync(filePath, "utf8");
  let seoLang = getLangCode(localeFolder || "en");
  let trans = translations[localeFolder] || translations["en"];
  let canonicalUrl = "";

  // remove any existing hreflangs first to avoid duplicate if script runs twice
  content = content.replace(
    /<link rel="alternate"[^>]+hreflang="[^"]+"[^>]*>\s*/g,
    "",
  );
  content = content.replace(
    /<script type="application\/ld\+json">.*?<\/script>\s*/gs,
    "",
  );

  let relativeUrl =
    fileName === "index.html" ? "" : fileName.replace(".html", "");

  // Update Canonical
  if (localeFolder) {
    const pathUrl = relativeUrl
      ? `${localeFolder}/${relativeUrl}`
      : `${localeFolder}/`;
    canonicalUrl = `https://pixiv-o-auth-token.vercel.app/${pathUrl}`;
  } else {
    canonicalUrl = `https://pixiv-o-auth-token.vercel.app/${relativeUrl}`;
  }
  content = content.replace(
    /<link\s+rel="canonical"\s+href="[^"]*"/gi,
    `<link rel="canonical" href="${canonicalUrl}"`,
  );

  // Apply Language and Meta Tags to ALL versions (root and localized)
  content = content.replace(
    /<html[^>]*lang="[^"]*"[^>]*>/i,
    `<html lang="${seoLang}">`,
  );

  const { titleVal, descVal } = getPageMetaData(fileName, trans);

  content = content.replace(
    /<title>.*?<\/title>/gi,
    `<title>${titleVal}</title>`,
  );
  content = content.replace(
    /<meta\s+name="description"\s+content="[^"]*"/gi,
    `<meta name="description" content="${descVal}"`,
  );
  content = content.replace(
    /property="og:title"\s+content="[^"]*"/gi,
    `property="og:title" content="${titleVal}"`,
  );
  content = content.replace(
    /property="og:description"\s+content="[^"]*"/gi,
    `property="og:description" content="${descVal}"`,
  );
  content = content.replace(
    /name="twitter:title"\s+content="[^"]*"/gi,
    `name="twitter:title" content="${titleVal}"`,
  );
  content = content.replace(
    /name="twitter:description"\s+content="[^"]*"/gi,
    `name="twitter:description" content="${descVal}"`,
  );
  // Fix og:locale with proper IETF region code (e.g. ja_JP not ja_JA)
  const ogLocale = getOgLocale(localeFolder);
  content = content.replace(
    /property="og:locale"\s+content="[^"]*"/gi,
    `property="og:locale" content="${ogLocale}"`,
  );

  // Update og:image:alt and twitter:image:alt with translated title
  content = content.replace(
    /property="og:image:alt"\s+content="[^"]*"/gi,
    `property="og:image:alt" content="Pixiv OAuth Web \u2013 ${titleVal}"`,
  );
  content = content.replace(
    /name="twitter:image:alt"\s+content="[^"]*"/gi,
    `name="twitter:image:alt" content="Pixiv OAuth Web \u2013 ${titleVal}"`,
  );

  // Update keywords — use translated subtitle words as keywords if available
  const keywordsBase = "pixiv oauth token, pixiv api, pkce, oauth2, pixiv login";
  const localizedKeyword = trans.kicker || "Pixiv OAuth Toolkit";
  const localizedTitle = trans.title || "Pixiv OAuth Web";
  content = content.replace(
    /name="keywords"\s+content="[^"]*"/gi,
    `name="keywords" content="${localizedKeyword}, ${localizedTitle}, ${keywordsBase}"`,
  );

  // Add schema before </head>
  const jsonLd = generateJsonLd(localeFolder, seoLang, canonicalUrl, trans, titleVal, descVal);
  content = content.replace("</head>", `${jsonLd}\n</head>`);

  // Inject hreflang before </head> if not exists
  const hreflangs = generateHreflangs(fileName);
  content = content.replace("</head>", `    ${hreflangs}\n  </head>`);

  return content;
}

console.log("Building SEO multi-region architecture...");

htmlFiles.forEach((file) => {
  const filePath = path.join(PUBLIC_DIR, file);

  // 1. Process and save the root file (x-default)
  const rootContent = processFile(filePath, file, null);
  fs.writeFileSync(filePath, rootContent, "utf8");
  console.log(`[Root]  Updated ${file}`);

  // 2. Generate locale specific folders and files
  LANG_ORDER.forEach((locale) => {
    const localeDir = path.join(PUBLIC_DIR, locale);
    if (!fs.existsSync(localeDir)) {
      fs.mkdirSync(localeDir, { recursive: true });
    }

    const localeContent = processFile(filePath, file, locale);
    fs.writeFileSync(path.join(localeDir, file), localeContent, "utf8");
  });
});

console.log("✅ SEO HTML Generation Complete!");

// 6. Generate Sitemap
function generateSitemap(htmlFiles) {
  const baseUrl = "https://pixiv-o-auth-token.vercel.app";
  let sitemapContent = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n`;

  const priorities = {
    "index": "1.0",
    "tutorial": "0.9",
    "downloads": "0.9",
    "documentation": "0.8",
    "changelog": "0.8",
    "issues": "0.8",
    "discussions": "0.8",
    "contact": "0.8",
    "support": "0.8",
    "license": "0.7",
    "privacy-policy": "0.6",
    "terms-conditions": "0.6"
  };

  const changeFrequencies = {
    "index": "weekly",
    "privacy-policy": "monthly",
    "terms-conditions": "monthly",
    "license": "monthly"
  };

  const today = new Date().toISOString().split('T')[0];

  htmlFiles.forEach((file) => {
    if (file === "404.html" || file === "enable-javascript.html") return;

    let relativeUrl = file === "index.html" ? "" : file.replace(".html", "");
    const baseName = file.replace(".html", "");
    const priority = priorities[baseName] || "0.8";
    const changefreq = changeFrequencies[baseName] || "weekly";

    let hreflangLinks = `\n    <xhtml:link rel="alternate" hreflang="x-default" href="${baseUrl}/${relativeUrl}" />`;
    for (const locale of LANG_ORDER) {
      const langCode = getLangCode(locale);
      const pathUrl = relativeUrl ? `${locale}/${relativeUrl}` : `${locale}/`;
      hreflangLinks += `\n    <xhtml:link rel="alternate" hreflang="${langCode}" href="${baseUrl}/${pathUrl}" />`;
    }

    const rootUrl = relativeUrl ? `${baseUrl}/${relativeUrl}` : `${baseUrl}/`;
    sitemapContent += `  <url>
    <loc>${rootUrl}</loc>
    <lastmod>${today}</lastmod>
    <changefreq>${changefreq}</changefreq>
    <priority>${priority}</priority>${hreflangLinks}
  </url>\n`;

    LANG_ORDER.forEach(locale => {
      const pathUrl = relativeUrl ? `${locale}/${relativeUrl}` : `${locale}/`;
      const locUrl = `${baseUrl}/${pathUrl}`;
      sitemapContent += `  <url>
    <loc>${locUrl}</loc>
    <lastmod>${today}</lastmod>
    <changefreq>${changefreq}</changefreq>
    <priority>${priority}</priority>${hreflangLinks}
  </url>\n`;
    });
  });

  sitemapContent += `</urlset>\n`;
  fs.writeFileSync(path.join(PUBLIC_DIR, "sitemap.xml"), sitemapContent, "utf8");
  console.log("✅ sitemap.xml generated with localized variations.");
}

generateSitemap(htmlFiles);
