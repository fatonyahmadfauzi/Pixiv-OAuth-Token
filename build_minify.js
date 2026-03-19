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

const FILES = [
  'public/assets/app.js',
  'public/assets/issues.js',
  'public/assets/docs.js',
  'public/assets/license.js',
  'public/assets/schema.js',
  'public/assets/contact.js',
  'public/components/footer.js',
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

let totalBefore = 0, totalAfter = 0;

FILES.forEach(f => {
  if (!fs.existsSync(f)) {
    console.log(`[SKIP]  ${f} — file not found`);
    return;
  }

  // 1. Backup
  const backupPath = path.join(BACKUP_DIR, f.replace(/\//g, '__'));
  fs.copyFileSync(f, backupPath);

  const before = fs.statSync(f).size;
  totalBefore += before;

  // 2. Minify with terser
  //    --compress: remove dead code, reduce expressions
  //    --mangle:   rename variables/functions to short names (obfuscation)
  //    --module:   treat as ES module
  try {
    execSync(
      `npx terser "${f}" --compress passes=2,drop_console=false --mangle --output "${f}" --ecma 2020`,
      { stdio: 'pipe' }
    );

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
});

const totalSaved = (((totalBefore - totalAfter) / totalBefore) * 100).toFixed(1);
console.log(`\n✅ Done! Total: ${kb(totalBefore)} → ${kb(totalAfter)} (saved ${totalSaved}%)`);
console.log(`📦 Backups saved to: ${BACKUP_DIR}/`);
console.log(`⚠️  To restore originals: node build_minify.js --restore`);

function kb(bytes) {
  return (bytes / 1024).toFixed(1) + 'KB';
}
