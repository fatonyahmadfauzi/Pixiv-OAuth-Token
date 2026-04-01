const fs = require('fs');
const path = require('path');

const i18nPath = path.join(__dirname, '../web/public/assets/js/core/i18n.js');
let i18nContent = fs.readFileSync(i18nPath, 'utf8');

const translations = {
  en: 'Professional Token Helper',
  pl: 'Profesjonalny Asystent Tokenów',
  zh: '专业令牌助手',
  jp: 'プロフェッショナルトークンヘルパー',
  de: 'Professioneller Token-Helfer',
  fr: 'Assistant de Jeton Professionnel',
  es: 'Asistente de Tokens Profesional',
  ru: 'Профессиональный Помощник по Токенам',
  pt: 'Assistente de Token Profissional',
  id: 'Asisten Token Profesional',
  kr: '전문 토큰 도우미'
};

for (const [lang, suffix] of Object.entries(translations)) {
  const regex = new RegExp(`(${lang}:\\s*\\{[\\s\\S]*?title:\\s*".*?",)`);
  if (!i18nContent.includes(`indexTitleSuffix:`)) {
    i18nContent = i18nContent.replace(regex, `$1\n    indexTitleSuffix: "${suffix}",`);
  } else if (!i18nContent.match(new RegExp(`indexTitleSuffix:`, 'g')) || i18nContent.match(new RegExp(`indexTitleSuffix:`, 'g')).length < 11) {
    // Attempt insert if partially available
    if (i18nContent.match(regex)) {
        let block = i18nContent.match(regex)[1];
        if (!block.includes('indexTitleSuffix:')) {
            i18nContent = i18nContent.replace(regex, `$1\n    indexTitleSuffix: "${suffix}",`);
        }
    }
  }
}

fs.writeFileSync(i18nPath, i18nContent, 'utf8');

const buildSeoPath = path.join(__dirname, '../web/scripts/build_seo.js');
let buildSeoContent = fs.readFileSync(buildSeoPath, 'utf8');

buildSeoContent = buildSeoContent.replace(
  /let titleVal = \`\$\{pageTitle\} \| Pixiv OAuth\`;\s*if \(baseName === "index"\) \{\s*titleVal = \`\$\{pageTitle\} \| Professional Token Helper\`;\s*\}/,
  `let titleVal = \`\$\{pageTitle\} | Pixiv OAuth\`;\n  if (baseName === "index") {\n    const defaultSuffix = "Professional Token Helper";\n    const suffix = trans.indexTitleSuffix || defaultSuffix;\n    titleVal = \`\$\{pageTitle\} | \$\{suffix\}\`;\n  }`
);

// update og:image:alt and twitter:image:alt with translated title
buildSeoContent = buildSeoContent.replace(
  /property="og:image:alt" content="Pixiv OAuth Web \\u2013 \$\{titleVal\}"/g,
  `property="og:image:alt" content="\$\{trans.title || "Pixiv OAuth Web"\} \\u2013 \$\{titleVal\}"`
).replace(
  /name="twitter:image:alt" content="Pixiv OAuth Web \\u2013 \$\{titleVal\}"/g,
  `name="twitter:image:alt" content="\$\{trans.title || "Pixiv OAuth Web"\} \\u2013 \$\{titleVal\}"`
);

fs.writeFileSync(buildSeoPath, buildSeoContent, 'utf8');
console.log('Patched i18n.js and build_seo.js done!');
