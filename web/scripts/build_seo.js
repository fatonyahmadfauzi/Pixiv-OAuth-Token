#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const PUBLIC_DIR = path.join(__dirname, '../public');
const I18N_JS_PATH = path.join(PUBLIC_DIR, 'assets/js/core/i18n.js');

const LANG_ORDER = ["de", "en", "es", "fr", "id", "jp", "kr", "pl", "pt", "ru", "zh"];
const SEO_MAP = { jp: "ja", kr: "ko" };

function getLangCode(folder) {
  return SEO_MAP[folder] || folder;
}

// 1. Extract Translations from i18n.js to populate SEO Metadata safely.
function getTranslations() {
  const code = fs.readFileSync(I18N_JS_PATH, 'utf8');
  const match = code.match(/export\s+const\s+DISPLAY_LANGUAGES\s*=\s*\{/);
  if (!match) throw new Error('Could not find DISPLAY_LANGUAGES in i18n.js');
  
  const startObj = code.indexOf('{', match.index);
  let braceCount = 0;
  let inString = false;
  let escape = false;
  let endIdx = -1;
  
  for (let i = startObj; i < code.length; i++) {
    const char = code[i];
    if (escape) { escape = false; continue; }
    if (char === '\\') { escape = true; continue; }
    if (char === '"' || char === "'") {
       if (inString === char) inString = false;
       else if (!inString) inString = char;
    }
    if (!inString) {
      if (char === '{') braceCount++;
      if (char === '}') {
        braceCount--;
        if (braceCount === 0) { endIdx = i; break; }
      }
    }
  }
  
  const objStr = code.substring(startObj, endIdx + 1);
  return new Function('return ' + objStr)();
}

const translations = getTranslations();

// 2. Discover all base HTML files in public/
const htmlFiles = fs.readdirSync(PUBLIC_DIR)
  .filter(f => f.endsWith('.html') && fs.statSync(path.join(PUBLIC_DIR, f)).isFile());

// 3. Generate Hreflang Tags Block
function generateHreflangs(fileName) {
  let relativeUrl = fileName === 'index.html' ? '' : fileName.replace('.html', '');
  let tags = [];
  
  // Root level (x-default)
  tags.push(`<link rel="alternate" hreflang="x-default" href="https://pixiv-o-auth-token.vercel.app/${relativeUrl}" />`);
  
  for (const locale of LANG_ORDER) {
    const langCode = getLangCode(locale);
    const pathUrl = relativeUrl ? `${locale}/${relativeUrl}` : `${locale}/`;
    tags.push(`<link rel="alternate" hreflang="${langCode}" href="https://pixiv-o-auth-token.vercel.app/${pathUrl}" />`);
  }
  return tags.join('\n    ');
}

// 4. Generate JSON-LD Schema
function generateJsonLd(locale, seoLang, pageUrl, trans) {
  let jsonString = `
    {
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "name": "${(trans.title || 'Pixiv OAuth Web').replace(/"/g, '\\"')}",
      "description": "${(trans.subtitle || '').replace(/"/g, '\\"')}",
      "inLanguage": "${seoLang}",
      "url": "${pageUrl}",
      "applicationCategory": "DeveloperApplication",
      "operatingSystem": "Web, Windows"
    }`;
  return `<script type="application/ld+json">${jsonString}</script>`;
}

// 5. Process HTML files
function processFile(filePath, fileName, localeFolder) {
  let content = fs.readFileSync(filePath, 'utf8');
  let seoLang = 'en';
  let trans = translations['en'];
  let canonicalUrl = '';
  
  // remove any existing hreflangs first to avoid duplicate if script runs twice
  content = content.replace(/<link rel="alternate"[^>]+hreflang="[^"]+"[^>]*>\s*/g, '');
  content = content.replace(/<script type="application\/ld\+json">.*?<\/script>\s*/gs, '');

  let relativeUrl = fileName === 'index.html' ? '' : fileName.replace('.html', '');

  if (localeFolder) {
    seoLang = getLangCode(localeFolder); 
    trans = translations[localeFolder] || translations['en'];
    
    // Replace lang attribute
    content = content.replace(/<html[^>]*lang="[^"]*"[^>]*>/i, `<html lang="${seoLang}">`);
    
    const titleVal = `${trans.title || 'Pixiv OAuth'} | Professional Token Helper`;
    const descVal = trans.subtitle || 'Toolkit to generate and refresh Pixiv OAuth tokens';
    
    content = content.replace(/<title>.*?<\/title>/gi, `<title>${titleVal}</title>`);
    content = content.replace(/<meta\s+name="description"\s+content="[^"]*"/gi, `<meta name="description" content="${descVal}"`);
    content = content.replace(/property="og:title"\s+content="[^"]*"/gi, `property="og:title" content="${titleVal}"`);
    content = content.replace(/property="og:description"\s+content="[^"]*"/gi, `property="og:description" content="${descVal}"`);
    content = content.replace(/name="twitter:title"\s+content="[^"]*"/gi, `name="twitter:title" content="${titleVal}"`);
    content = content.replace(/name="twitter:description"\s+content="[^"]*"/gi, `name="twitter:description" content="${descVal}"`);
    
    // Replace OpenGraph locale if it existed
    content = content.replace(/property="og:locale"\s+content="[^"]*"/gi, `property="og:locale" content="${seoLang}_${seoLang.toUpperCase()}"`);
    
    // Update Canonical
    const pathUrl = relativeUrl ? `${localeFolder}/${relativeUrl}` : `${localeFolder}/`;
    canonicalUrl = `https://pixiv-o-auth-token.vercel.app/${pathUrl}`;
    content = content.replace(/<link\s+rel="canonical"\s+href="[^"]*"/gi, `<link rel="canonical" href="${canonicalUrl}"`);

  } else {
    // For root files, ensure basic canonical
    canonicalUrl = `https://pixiv-o-auth-token.vercel.app/${relativeUrl}`;
    content = content.replace(/<link\s+rel="canonical"\s+href="[^"]*"/gi, `<link rel="canonical" href="${canonicalUrl}"`);
  }

  // Add schema before </head>
  const jsonLd = generateJsonLd(localeFolder, seoLang, canonicalUrl, trans);
  content = content.replace('</head>', `${jsonLd}\n</head>`);
  
  // Inject hreflang before </head> if not exists
  const hreflangs = generateHreflangs(fileName);
  content = content.replace('</head>', `    ${hreflangs}\n  </head>`);

  return content;
}

console.log('Building SEO multi-region architecture...');

htmlFiles.forEach(file => {
  const filePath = path.join(PUBLIC_DIR, file);
  
  // 1. Process and save the root file (x-default)
  const rootContent = processFile(filePath, file, null);
  fs.writeFileSync(filePath, rootContent, 'utf8');
  console.log(`[Root]  Updated ${file}`);
  
  // 2. Generate locale specific folders and files
  LANG_ORDER.forEach(locale => {
    const localeDir = path.join(PUBLIC_DIR, locale);
    if (!fs.existsSync(localeDir)) {
      fs.mkdirSync(localeDir, { recursive: true });
    }
    
    const localeContent = processFile(filePath, file, locale);
    fs.writeFileSync(path.join(localeDir, file), localeContent, 'utf8');
  });
});

console.log('✅ SEO HTML Generation Complete!');
