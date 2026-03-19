/**
 * docs.js — Documentation page logic
 * Loads README.md from GitHub, renders with marked.js + highlight.js,
 * and builds a sidebar Table of Contents.
 *
 * NOTE: marked v12 removed the `highlight` option from setOptions.
 * Code highlighting is now done post-render via hljs.highlightElement().
 */

var RAW_README = 'https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/README.md';

// marked v12 API — use marked.use() instead of setOptions({ highlight })
marked.use({ gfm: true, breaks: true });

// Suppress hljs warnings for unknown languages (bat, powershell, etc.)
if (typeof hljs !== 'undefined') {
  hljs.configure({ ignoreUnescapedHTML: true });
  // Register common aliases that readme files use
  ['bat','cmd','powershell','ps1','ps','text','plain'].forEach(function(lang) {
    try { hljs.registerAliases(lang, { languageName: 'plaintext' }); } catch(e) {}
  });
}

function buildTOC() {
  var body = document.getElementById('docBody');
  var nav  = document.getElementById('tocNav');
  if (!body || !nav) return;

  var headings = body.querySelectorAll('h2, h3');
  if (!headings.length) return;

  nav.innerHTML = Array.from(headings).map(function(h) {
    var text   = h.textContent;
    var id     = text.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-');
    h.id       = id;
    var indent = h.tagName === 'H3' ? 'gh-toc-h3' : '';
    return '<a href="#' + id + '" class="gh-toc-link ' + indent + '">' + text + '</a>';
  }).join('');

  // Highlight active TOC link on scroll
  var links    = nav.querySelectorAll('.gh-toc-link');
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        links.forEach(function(l) { l.classList.remove('active'); });
        var active = nav.querySelector('a[href="#' + entry.target.id + '"]');
        if (active) active.classList.add('active');
      }
    });
  }, { rootMargin: '-10% 0px -80% 0px' });

  headings.forEach(function(el) { observer.observe(el); });
}

async function loadDocs() {
  var skeleton = document.getElementById('docSkeleton');
  var body     = document.getElementById('docBody');
  var error    = document.getElementById('docError');

  try {
    var res = await fetch(RAW_README);
    if (!res.ok) throw new Error('HTTP ' + res.status);
    var md = await res.text();

    // Parse markdown → HTML (highlight option removed in marked v12)
    body.innerHTML = marked.parse(md);
    skeleton.hidden = true;
    body.hidden     = false;

    buildTOC();

    // Apply highlight.js post-render (after DOM is populated)
    body.querySelectorAll('pre code').forEach(function(el) {
      hljs.highlightElement(el);
    });
  } catch (e) {
    console.error('[docs.js] Failed to load README:', e);
    if (skeleton) skeleton.hidden = true;
    if (error)    error.hidden    = false;
  }
}

loadDocs();
