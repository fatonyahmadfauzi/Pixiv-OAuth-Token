/**
 * discussions.js — Discussions page logic
 * Fetches repo stats via /api/github proxy (PAT stored in Vercel env).
 * CSP-compliant: no inline styles, no inline scripts.
 */

var REPO = 'fatonyahmadfauzi/Pixiv-OAuth-Token';

async function loadRepoStats() {
  var statsEl = document.getElementById('repoStats');
  try {
    var params = new URLSearchParams({ path: 'repos/' + REPO });
    var res = await fetch('/api/github?' + params);
    if (!res.ok) throw new Error('proxy HTTP ' + res.status);
    var r = await res.json();
    statsEl.innerHTML = [
      '<div class="gh-stat-card">',
        '<i class="bi bi-star c-blue" aria-hidden="true"></i>',
        '<div class="gh-stat-value">' + r.stargazers_count.toLocaleString() + '</div>',
        '<div class="gh-stat-label">Stars</div>',
      '</div>',
      '<div class="gh-stat-card">',
        '<i class="bi bi-diagram-2 c-blue" aria-hidden="true"></i>',
        '<div class="gh-stat-value">' + r.forks_count.toLocaleString() + '</div>',
        '<div class="gh-stat-label">Forks</div>',
      '</div>',
      '<div class="gh-stat-card">',
        '<i class="bi bi-eye c-blue" aria-hidden="true"></i>',
        '<div class="gh-stat-value">' + (r.subscribers_count != null ? r.subscribers_count : r.watchers_count) + '</div>',
        '<div class="gh-stat-label">Watchers</div>',
      '</div>',
      '<div class="gh-stat-card">',
        '<i class="bi bi-circle c-open" aria-hidden="true"></i>',
        '<div class="gh-stat-value">' + r.open_issues_count.toLocaleString() + '</div>',
        '<div class="gh-stat-label">Open Issues</div>',
      '</div>',
    ].join('');
  } catch (e) {
    statsEl.innerHTML = '';
  }
}

loadRepoStats();
