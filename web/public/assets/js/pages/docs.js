import { t, DISPLAY_LANG } from "../core/i18n.js";

const DOCS_REPO = "fatonyahmadfauzi/Pixiv-OAuth-Token";
const RAW_BASE = `https://raw.githubusercontent.com/${DOCS_REPO}/master`;

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function normalizeLangCode(input) {
  const lang = String(input || "").toLowerCase();
  const map = {
    en: "en",
    "en-us": "en",
    "en-gb": "en",
    id: "id",
    in: "id",
    jp: "jp",
    ja: "jp",
    "ja-jp": "jp",
    kr: "kr",
    ko: "kr",
    "ko-kr": "kr",
    zh: "zh",
    "zh-cn": "zh",
    "zh-tw": "zh",
    "zh-sg": "zh",
    pl: "pl",
    de: "de",
    fr: "fr",
    es: "es",
    ru: "ru",
    pt: "pt",
    "pt-br": "pt",
    "pt-pt": "pt",
  };
  if (map[lang]) return map[lang];
  return map[lang.split("-")[0]] || "en";
}

function getRouteLang() {
  const parts = window.location.pathname.split("/").filter(Boolean);
  if (parts.length > 0) {
    const n = normalizeLangCode(parts[0]);
    if (n !== "en" || parts[0].toLowerCase() === "en") return n;
  }
  if (typeof DISPLAY_LANG !== "undefined" && DISPLAY_LANG)
    return normalizeLangCode(DISPLAY_LANG);
  return normalizeLangCode(document.documentElement.lang || "en");
}

function getLocalizedDocPath(fileName, lang) {
  const safeFile = (fileName || "README.md").trim();
  const dotIndex = safeFile.lastIndexOf(".");
  const base = (
    dotIndex === -1 ? safeFile : safeFile.slice(0, dotIndex)
  ).toUpperCase();
  const ext = (dotIndex === -1 ? "" : safeFile.slice(dotIndex)).toLowerCase();

  if (lang === "en") return `${RAW_BASE}/${base}${ext}`;
  return `/docs/lang/${base}-${lang.toUpperCase()}${ext}`;
}

async function fetchDocWithFallback(fileName) {
  const preferred = getRouteLang();
  const candidates = Array.from(new Set([preferred, "en"]));
  let lastError = null;
  for (const lang of candidates) {
    try {
      const response = await fetch(getLocalizedDocPath(fileName, lang));
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const text = await response.text();
      if (
        text.trim().toLowerCase().startsWith("<!doctype") ||
        text.trim().toLowerCase().startsWith("<html")
      ) {
        throw new Error("Received HTML fallback instead of markdown");
      }
      return { markdown: text, lang };
    } catch (err) {
      lastError = err;
    }
  }

  // Ultimate fallback to the default root README.md if language/en fetch fails
  try {
    const fallbackResponse = await fetch(`${RAW_BASE}/README.md`);
    if (fallbackResponse.ok) {
      const text = await fallbackResponse.text();
      if (
        !text.trim().toLowerCase().startsWith("<!doctype") &&
        !text.trim().toLowerCase().startsWith("<html")
      ) {
        return { markdown: text, lang: "en" };
      }
    }
  } catch (e) {}

  throw lastError || new Error("Failed to fetch documentation");
}

function buildTOC() {
  const body = document.getElementById("docBody");
  const toc = document.getElementById("tocNav");
  if (!body || !toc) return;
  const headings = body.querySelectorAll("h2, h3");
  if (!headings.length) return;
  toc.innerHTML = Array.from(headings)
    .map((heading) => {
      const text = heading.textContent;
      const id = text
        .toLowerCase()
        .replace(/[^\w\s-]/g, "")
        .replace(/\s+/g, "-");
      heading.id = id;
      const klass = heading.tagName === "H3" ? "gh-toc-h3" : "";
      return `<a href="#${escapeHtml(id)}" class="gh-toc-link ${klass}">${escapeHtml(text)}</a>`;
    })
    .join("");
  const links = toc.querySelectorAll(".gh-toc-link");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach((l) => l.classList.remove("active"));
        const active = toc.querySelector(`a[href="#${entry.target.id}"]`);
        if (active) active.classList.add("active");
      });
    },
    { rootMargin: "-10% 0px -80% 0px" },
  );
  headings.forEach((h) => observer.observe(h));
}

async function loadDocs() {
  const skeleton = document.getElementById("docSkeleton");
  const body = document.getElementById("docBody");
  if (!body) return;
  const fileHint = document.querySelector("[data-file]");
  const fileName =
    (fileHint && fileHint.getAttribute("data-file")) || "README.md";
  try {
    if (skeleton) skeleton.style.display = "";
    body.hidden = true;
    body.innerHTML = "";
    const { markdown } = await fetchDocWithFallback(fileName);
    body.innerHTML = marked.parse(markdown);
    if (skeleton) skeleton.style.display = "none";
    body.hidden = false;

    // Strip GitHub-only header elements (logo, badges, language links, centered h1)
    // 1. Remove <p> elements that contain only <img> tags (logo)
    body.querySelectorAll("p").forEach((p) => {
      const imgs = p.querySelectorAll("img");
      const text = p.textContent.trim();
      if (imgs.length > 0 && text === "") p.remove();
    });
    // 2. Remove <p> elements containing only badge/shield links
    body.querySelectorAll("p").forEach((p) => {
      const links = p.querySelectorAll("a");
      const imgs = p.querySelectorAll("img");
      if (links.length > 0 && imgs.length > 0 && p.textContent.trim() === "") p.remove();
    });
    // 3. Remove the centered <h1> (from <h1 align="center">)
    const firstH1 = body.querySelector("h1");
    if (firstH1) firstH1.remove();
    // 4. Remove language-links blockquote (contains 🌐)
    body.querySelectorAll("blockquote").forEach((bq) => {
      if (!bq.textContent.includes("🌐")) return;
      const next = bq.nextElementSibling;
      bq.remove();
      if (next && next.tagName === "HR") next.remove();
    });

    // 5. Inject plain (non-centered) title at the top
    const titleEl = document.createElement("h1");
    titleEl.textContent = "Pixiv OAuth Token";
    body.prepend(titleEl);

    const mdRouteMap = {
      "changelog.md": "/changelog",
      "readme.md": "/documentation",
      license: "/license",
      "license.md": "/license",
    };
    body.querySelectorAll("a[href]").forEach((anchor) => {
      const href = anchor.getAttribute("href") || "";
      if (
        href.startsWith("http") ||
        href.startsWith("/") ||
        href.startsWith("#") ||
        href.startsWith("mailto")
      )
        return;
      const normalized = href
        .replace(/-[A-Z]{2,5}\.md$/i, ".md")
        .toLowerCase()
        .split("#")[0]
        .trim();
      const route = mdRouteMap[normalized];
      if (!route) return;
      anchor.setAttribute("href", route);
      anchor.removeAttribute("target");
    });
    buildTOC();
    body
      .querySelectorAll("pre code")
      .forEach((el) => hljs.highlightElement(el));
  } catch (err) {
    console.error("[docs.js] Failed to load docs:", err);
    if (skeleton) skeleton.style.display = "none";
  }
}

export function setupDocsPage() {
  const fileHint = document.querySelector("[data-file]");
  const fileName = (fileHint && fileHint.getAttribute("data-file")) || "";
  if (fileName.toLowerCase().includes("license")) return;

  if (!document.getElementById("docBody")) return;
  if (typeof marked === "undefined") return;
  if (typeof hljs !== "undefined") {
    hljs.configure({ ignoreUnescapedHTML: true });
    ["bat", "cmd", "powershell", "ps1", "ps", "text", "plain"].forEach(
      (alias) => {
        try {
          hljs.registerAliases(alias, { languageName: "plaintext" });
        } catch {}
      },
    );
  }
  marked.use({ gfm: true, breaks: true });
  loadDocs();
  const langObserver = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.type === "attributes" && mutation.attributeName === "lang")
        loadDocs();
    });
  });
  langObserver.observe(document.documentElement, { attributes: true });
}
