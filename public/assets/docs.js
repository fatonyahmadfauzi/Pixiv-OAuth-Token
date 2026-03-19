/**
 * docs.js — Documentation page logic
 * Loads README.md from GitHub, renders with marked.js + highlight.js,
 * and builds a sidebar Table of Contents.
 */

const RAW_README = 'https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/README.md';

// Configure marked with highlight.js
marked.setOptions({
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value;
    }
    return hljs.highlightAuto(code).value;
  },
  breaks: true,
  gfm: true,
});

function buildTOC() {
  const body = document.getElementById('docBody');
  const nav  = document.getElementById('tocNav');
  if (!body || !nav) return;

  const headings = body.querySelectorAll('h2, h3');
  if (!headings.length) return;

  nav.innerHTML = Array.from(headings).map(function(h) {
    const text = h.textContent;
    const id   = text.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-');
    h.id = id;
    const indent = h.tagName === 'H3' ? 'gh-toc-h3' : '';
    return '<a href="#' + id + '" class="gh-toc-link ' + indent + '">' + text + '</a>';
  }).join('');

  // Highlight active TOC link on scroll
  const links    = nav.querySelectorAll('.gh-toc-link');
  const observer = new IntersectionObserver(function(entries) {
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
  const skeleton = document.getElementById('docSkeleton');
  const body     = document.getElementById('docBody');
  const error    = document.getElementById('docError');

  try {
    const res = await fetch(RAW_README);
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const md = await res.text();
    body.innerHTML = marked.parse(md);
    skeleton.hidden = true;
    body.hidden = false;
    buildTOC();
    // Apply highlight.js to all code blocks
    body.querySelectorAll('pre code').forEach(function(el) {
      hljs.highlightElement(el);
    });
  } catch (e) {
    skeleton.hidden = true;
    error.hidden = false;
  }
}

loadDocs();
