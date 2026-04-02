const fs = require("fs");
const path = require("path");
const { minify: minifyJs } = require("terser");
const CleanCSS = require("clean-css");
const { minify: minifyHtml } = require("html-minifier-terser");

const PUBLIC_DIR = path.join(__dirname, "../public");

// Guard to prevent accidental local execution destroying source files!
// Vercel CI and action environments use ephemeral storage.
if (!process.env.VERCEL && !process.env.CI && process.env.FORCE_MINIFY !== "true") {
  console.log("Skipping minification on local environment to protect source files. (Run with FORCE_MINIFY=true to override/deploy)");
  process.exit(0);
}

console.log("Starting minification for JS, CSS, and HTML...");

async function processDirectory(dir) {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      await processDirectory(fullPath);
    } else if (file.endsWith(".js") && !file.includes(".min.")) {
      console.log("Minifying JS:", fullPath.replace(PUBLIC_DIR, ""));
      const code = fs.readFileSync(fullPath, "utf8");
      try {
        const result = await minifyJs(code, {
          compress: { drop_console: true },
          mangle: false, // Disabled: files are minified independently (no bundler), mangling breaks cross-file ES Module imports
          module: true
        });
        if (result.code) fs.writeFileSync(fullPath, result.code, "utf8");
      } catch (err) {
        console.error(`Failed to minify JS ${fullPath}:`, err);
      }
    } else if (file.endsWith(".css") && !file.includes(".min.")) {
      console.log("Minifying CSS:", fullPath.replace(PUBLIC_DIR, ""));
      const css = fs.readFileSync(fullPath, "utf8");
      try {
        const result = new CleanCSS({ level: 2 }).minify(css);
        if (result.styles) fs.writeFileSync(fullPath, result.styles, "utf8");
      } catch (err) {
        console.error(`Failed to minify CSS ${fullPath}:`, err);
      }
    } else if (file.endsWith(".html")) {
      console.log("Minifying HTML:", fullPath.replace(PUBLIC_DIR, ""));
      const html = fs.readFileSync(fullPath, "utf8");
      try {
        const result = await minifyHtml(html, {
          collapseWhitespace: true,
          removeComments: true,
          minifyJS: true,
          minifyCSS: true
        });
        if (result) fs.writeFileSync(fullPath, result, "utf8");
      } catch (err) {
        console.error(`Failed to minify HTML ${fullPath}:`, err);
      }
    }
  }
}

processDirectory(PUBLIC_DIR).then(() => {
  console.log("✅ Minification complete.");
}).catch(err => {
  console.error("Minification crashed:", err);
  process.exit(1);
});
