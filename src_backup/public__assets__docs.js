function getReadmeUrl() {
  const lang = document.documentElement.lang || "en";
  if (lang === "en") {
    return "https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/README.md";
  } else {
    return `https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/public/docs/lang/README-${lang.toUpperCase()}.md`;
  }
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
  try {
    if (e) e.style.display = '';
    t.hidden = true;
    t.innerHTML = '';

    var r = await fetch(getReadmeUrl());
    if (!r.ok) throw new Error("HTTP " + r.status);
    var a = await r.text();
    
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