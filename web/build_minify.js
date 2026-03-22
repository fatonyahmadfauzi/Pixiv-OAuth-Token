#!/usr/bin/env node
/**
 * build_minify.js — Minify & Obfuscate all public JS files
 *
 * - Originals are always SAFE in git history
 * - Backup copies are saved to src_backup/ folder before overwriting
 * - Uses terser for minification + identifier mangling (obfuscation)
 *
 * Usage:
 *   node build_minify.js          — minify all files
 *   node build_minify.js --restore — restore from backup
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const JavaScriptObfuscator = require('javascript-obfuscator');
const { minify: minifyHtml } = require('html-minifier-terser');
const CleanCSS = require('clean-css');

const FILES = [
  'public/assets/app.js',
  'public/assets/issues.js',
  'public/assets/docs.js',
  'public/assets/license.js',
  'public/assets/schema.js',
  'public/assets/contact.js',
  'public/components/footer.js',
  'public/assets/style.css',
  'public/404.html',
  'public/contact.html',
  'public/discussions.html',
  'public/documentation.html',
  'public/downloads.html',
  'public/index.html',
  'public/issues.html',
  'public/license.html',
  'public/support.html',
  'public/tutorial.html'
];

const BACKUP_DIR = 'src_backup';

// ── RESTORE MODE ──────────────────────────────────────────────────────────────
if (process.argv.includes('--restore')) {
  let ok = 0;
  FILES.forEach(f => {
    const backup = path.join(BACKUP_DIR, f.replace(/\//g, '__'));
    if (fs.existsSync(backup)) {
      fs.copyFileSync(backup, f);
      console.log(`[RESTORED] ${f}`);
      ok++;
    } else {
      console.log(`[SKIP]     ${f} — no backup found`);
    }
  });
  console.log(`\n✅ Restored ${ok} file(s).`);
  process.exit(0);
}

// ── MINIFY MODE ───────────────────────────────────────────────────────────────
if (!fs.existsSync(BACKUP_DIR)) fs.mkdirSync(BACKUP_DIR, { recursive: true });

(async function main() {
  let totalBefore = 0, totalAfter = 0;

  for (const f of FILES) {
    if (!fs.existsSync(f)) {
      console.log(`[SKIP]  ${f} — file not found`);
      continue;
    }

    // 1. Backup
    const backupPath = path.join(BACKUP_DIR, f.replace(/\//g, '__'));
    fs.copyFileSync(f, backupPath);

    const before = fs.statSync(f).size;
    totalBefore += before;

    try {
      const code = fs.readFileSync(f, 'utf8');
      const ext = path.extname(f);
      let outputCode = code;

      if (ext === '.js') {
        const obfuscationResult = JavaScriptObfuscator.obfuscate(code, {
          compact: true,
          controlFlowFlattening: true,
          controlFlowFlatteningThreshold: 1.0,
          deadCodeInjection: true,
          deadCodeInjectionThreshold: 0.4,
          numbersToExpressions: true,
          simplify: true,
          stringArrayShuffle: true,
          splitStrings: true,
          stringArrayThreshold: 1.0
        });
        outputCode = obfuscationResult.getObfuscatedCode();
      } else if (ext === '.css') {
        const output = new CleanCSS({}).minify(code);
        outputCode = output.styles;
      } else if (ext === '.html') {
        outputCode = await minifyHtml(code, {
          collapseWhitespace: true,
          removeComments: true,
          minifyJS: true,
          minifyCSS: true,
          removeRedundantAttributes: false, // Changed to false
          removeEmptyAttributes: true,
          removeScriptTypeAttributes: true, // Added
          removeStyleLinkTypeAttributes: true, // Added
          useShortDoctype: true // Added
        });
      }

      fs.writeFileSync(f, outputCode, 'utf8');

      const after = fs.statSync(f).size;
      totalAfter += after;
      const saved = (((before - after) / before) * 100).toFixed(1);
      console.log(`[OK]    ${f}  ${kb(before)} → ${kb(after)}  (saved ${saved}%)`);
    } catch (err) {
      console.error(`[ERROR] ${f}\n`, err.stderr?.toString() || err.message);
      // Restore backup on error
      fs.copyFileSync(backupPath, f);
      console.log(`        ↩ Restored original due to error.`);
    }
  }

  const totalSaved = (((totalBefore - totalAfter) / totalBefore) * 100).toFixed(1);
  console.log(`\n✅ Done! Total: ${kb(totalBefore)} → ${kb(totalAfter)} (saved ${totalSaved}%)`);
  console.log(`📦 Backups saved to: ${BACKUP_DIR}/`);
  console.log(`⚠️  To restore originals: node build_minify.js --restore`);
})();

function kb(bytes) {
  return (bytes / 1024).toFixed(1) + 'KB';
}
