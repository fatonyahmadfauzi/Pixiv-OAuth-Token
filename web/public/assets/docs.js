function getDocUrl(fileName, lang) {
  const safeFile = (fileName || "README.md").trim();
  if (!lang || lang === "en") {
    return `https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/${safeFile}`;
  }
  const dotIndex = safeFile.lastIndexOf(".");
  const base = dotIndex === -1 ? safeFile : safeFile.slice(0, dotIndex);
  const ext = dotIndex === -1 ? "" : safeFile.slice(dotIndex);
  return `https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/web/public/docs/lang/${base}-${lang.toUpperCase()}${ext}`;
}

async function fetchDocWithFallback(fileName) {
  const selectedLang = (document.documentElement.lang || "en").toLowerCase();
  const primaryLang = selectedLang.split("-")[0];
  const candidates = selectedLang === "en"
    ? ["en"]
    : Array.from(new Set([selectedLang, primaryLang, "en"]));

  let lastError = null;
  for (const lang of candidates) {
    try {
      const response = await fetch(getDocUrl(fileName, lang));
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const markdown = await response.text();
      return { markdown, lang };
    } catch (err) {
      lastError = err;
    }
  }
  throw lastError || new Error("Failed to fetch README fallback chain");
}

function buildTOC() {
  var e = document.getElementById("docBody"), t = document.getElementById("tocNav");
  if (e && t) {
    var r = e.querySelectorAll("h2, h3");
    if (r.length) {
      t.innerHTML = Array.from(r).map(function(e) {
        var t = e.textContent, r = t.toLowerCase().replace(/[^\w\s-]/g, "").replace(/\s+/g, "-");
        e.id = r;
        var a = "H3" === e.tagName ? "gh-toc-h3" : "";
        return '<a href="#' + escapeHTML(r) + '" class="gh-toc-link ' + a + '">' + escapeHTML(t) + "</a>"
      }).join("");
      var a = t.querySelectorAll(".gh-toc-link"), o = new IntersectionObserver(function(e) {
        e.forEach(function(e) {
          if (e.isIntersecting) {
            a.forEach(function(e) { e.classList.remove("active") });
            var r = t.querySelector('a[href="#' + e.target.id + '"]');
            r && r.classList.add("active")
          }
        })
      }, { rootMargin: "-10% 0px -80% 0px" });
      r.forEach(function(e) { o.observe(e) })
    }
  }
}

async function loadDocs() {
  var e = document.getElementById("docSkeleton");
  var t = document.getElementById("docBody");
  var fileHint = document.querySelector("[data-file]");
  var fileName = fileHint ? fileHint.getAttribute("data-file") || "README.md" : "README.md";
  try {
    if (e) e.style.display = '';
    t.hidden = true;
    t.innerHTML = '';

    var readmeResult = await fetchDocWithFallback(fileName);
    var a = readmeResult.markdown;
    
    t.innerHTML = marked.parse(a);
    if (e) e.style.display = 'none';
    t.hidden = false;
    
    t.querySelectorAll('blockquote').forEach(function(bq) {
      if (bq.textContent.includes('🌐')) {
        var nextEl = bq.nextElementSibling;
        bq.remove();
        if (nextEl && nextEl.tagName === 'HR') {
          nextEl.remove();
        }
      }
    });

    // Rewrite relative .md links so they work on the web app instead of 404-ing.
    // e.g. CHANGELOG.md → /changelog, README.md → /documentation
    var mdRouteMap = {
      'changelog.md': '/changelog',
      'readme.md': '/documentation',
      'license': '/license',
      'license.md': '/license'
    };
    t.querySelectorAll('a[href]').forEach(function(anchor) {
      var href = anchor.getAttribute('href') || '';
      // Only rewrite relative links (no protocol, no leading /)
      if (!href.startsWith('http') && !href.startsWith('/') && !href.startsWith('#') && !href.startsWith('mailto')) {
        // Strip any language suffix like -JP, -ID, etc. before .md to normalize
        var normalized = href.replace(/-[A-Z]{2,5}\.md$/i, '.md').toLowerCase().split('#')[0].trim();
        var route = mdRouteMap[normalized];
        if (route) {
          anchor.setAttribute('href', route);
          anchor.removeAttribute('target');
        }
      }
    });

    buildTOC();
    t.querySelectorAll("pre code").forEach(function(e) {
      hljs.highlightElement(e)
    });
  } catch (err) {
    console.error("[docs.js] Failed to load README:", err);
    if (e) e.style.display = 'none';
  }
}

marked.use({ gfm: true, breaks: true });
if (typeof hljs !== "undefined") {
  hljs.configure({ ignoreUnescapedHTML: true });
  ["bat", "cmd", "powershell", "ps1", "ps", "text", "plain"].forEach(function(langAlias) {
    try {
      hljs.registerAliases(langAlias, { languageName: "plaintext" });
    } catch (err) {}
  });
}

loadDocs();

var langObserver = new MutationObserver(function(mutations) {
  mutations.forEach(function(mutation) {
    if (mutation.type === "attributes" && mutation.attributeName === "lang") {
      loadDocs();
    }
  });
});

langObserver.observe(document.documentElement, {
  attributes: true
});
