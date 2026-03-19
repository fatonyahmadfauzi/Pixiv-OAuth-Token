/**
 * issues.js — Issues page logic
 * Fetches GitHub Issues via /api/github proxy (PAT stored in Vercel env).
 * CSP-compliant: no inline styles, no inline scripts.
 */

var REPO     = 'fatonyahmadfauzi/Pixiv-OAuth-Token';
var API_BASE = '/api/github';
var currentState = 'open';
var cache = {};

function timeAgo(dateStr) {
  var diff = (Date.now() - new Date(dateStr)) / 1000;
  if (diff < 60)      return t('timeJustNow');
  if (diff < 3600)    return t('timeMinsAgo', {count: Math.floor(diff / 60)});
  if (diff < 86400)   return t('timeHoursAgo', {count: Math.floor(diff / 3600)});
  if (diff < 2592000) return t('timeDaysAgo', {count: Math.floor(diff / 86400)});
  return new Date(dateStr).toLocaleDateString(DISPLAY_LANG === 'en' ? 'en-US' : DISPLAY_LANG, { month: 'short', day: 'numeric', year: 'numeric' });
}

function renderIssue(issue) {
  var isPR = !!issue.pull_request;
  // Use CSS classes instead of inline style for CSP compliance
  var iconClass = isPR
    ? 'bi bi-git c-pr'
    : (issue.state === 'open' ? 'bi bi-circle c-open' : 'bi bi-check-circle c-closed');

  var labels = (issue.labels || []).map(function(l) {
    // Use data attributes for custom colors, applied via JS classList
    return '<span class="gh-issue-label gh-label-custom" data-bg="#' + escapeHTML(l.color) + '">' + escapeHTML(l.name) + '</span>';
  }).join('');

  var body = issue.body
    ? escapeHTML(issue.body.replace(/\n/g, ' ').slice(0, 140)) + (issue.body.length > 140 ? '…' : '')
    : '';

  return [
    '<article class="gh-issue-card" role="listitem">',
      '<div class="gh-issue-icon"><i class="' + iconClass + '" aria-hidden="true"></i></div>',
      '<div class="gh-issue-content">',
        '<div class="gh-issue-top">',
          '<a class="gh-issue-title" href="' + escapeHTML(issue.html_url) + '" target="_blank" rel="noopener">' + escapeHTML(issue.title) + '</a>',
          isPR ? '<span class="gh-issue-pr-badge">PR</span>' : '',
        '</div>',
        '<div class="gh-issue-meta">',
          '<span>#' + escapeHTML(String(issue.number)) + '</span>',
          '<span>' + t('issueOpenedBy', {time: escapeHTML(timeAgo(issue.created_at))}) + ' ',
            '<a class="gh-issue-author" href="' + escapeHTML(issue.user.html_url) + '" target="_blank" rel="noopener">',
              '<img class="gh-issue-avatar" src="' + escapeHTML(issue.user.avatar_url) + '&s=20" width="16" height="16" alt="' + escapeHTML(issue.user.login) + '">',
              escapeHTML(issue.user.login),
            '</a>',
          '</span>',
        '</div>',
        labels ? '<div class="gh-issue-labels">' + labels + '</div>' : '',
        body   ? '<p class="gh-issue-body">' + body + '</p>' : '',
      '</div>',
      '<div class="gh-issue-aside">',
        issue.comments > 0
          ? '<span class="gh-issue-comments" title="' + escapeHTML(t('issueComments', {count: issue.comments})) + '"><i class="bi bi-chat" aria-hidden="true"></i>' + escapeHTML(String(issue.comments)) + '</span>'
          : '',
      '</div>',
    '</article>'
  ].join('');
}

// Apply custom label colors via JS after render (avoids inline style in HTML)
function applyLabelColors() {
  document.querySelectorAll('.gh-label-custom').forEach(function(el) {
    var bg = el.dataset.bg;
    if (!bg) return;
    el.style.background    = bg + '22';
    el.style.color         = bg;
    el.style.borderColor   = bg + '44';
  });
}

async function loadIssues(state) {
  var list     = document.getElementById('issueList');
  var skeleton = document.getElementById('skeletonWrap');
  var empty    = document.getElementById('emptyState');

  empty.hidden = true;

  if (!skeleton) {
    list.innerHTML = '<div class="gh-skeleton-wrap" id="skeletonWrap">'
      + '<div class="gh-issue-skeleton"></div>'.repeat(4)
      + '</div>';
  } else {
    skeleton.hidden = false;
  }

  if (cache[state]) { renderList(cache[state], state); return; }

  try {
    var params = new URLSearchParams({ path: 'repos/' + REPO + '/issues', state: state, per_page: 30 });
    var res = await fetch('/api/github?' + params);
    if (!res.ok) throw new Error('proxy HTTP ' + res.status);
    var data = await res.json();

    cache[state] = data;
    renderList(data, state);
  } catch (e) {
    var sw = document.getElementById('skeletonWrap');
    if (sw) sw.remove();
  }
}

function renderList(data, state) {
  var list      = document.getElementById('issueList');
  var empty     = document.getElementById('emptyState');
  var sw        = document.getElementById('skeletonWrap');
  if (sw) sw.remove();

  var issues = data.filter(function(i) { return !i.pull_request; });
  var prs    = data.filter(function(i) { return !!i.pull_request; });

  var openLabel   = document.getElementById('openCountLabel');
  var closedLabel = document.getElementById('closedCountLabel');
  if (state === 'open')   openLabel.textContent   = t('issueCountOpen', {count: issues.length});
  else                    closedLabel.textContent = t('issueCountClosed', {count: issues.length});

  if (!issues.length && !prs.length) {
    empty.hidden = false;
    document.getElementById('emptyStateText').textContent = state === 'open'
      ? t('issueEmptyOpen')
      : t('issueEmptyClosed');
    list.innerHTML = '';
    return;
  }

  var html = '<div role="list">';
  if (issues.length) html += issues.map(renderIssue).join('');
  if (prs.length) {
    html += '<div class="gh-section-divider"><span>' + t('issuePrSection', {count: prs.length}) + '</span></div>';
    html += prs.map(renderIssue).join('');
  }
  html += '</div>';
  list.innerHTML = html;
  applyLabelColors();
}

// Tab switching
document.getElementById('tabOpen').addEventListener('click', function() {
  document.getElementById('tabOpen').classList.add('active');
  document.getElementById('tabClosed').classList.remove('active');
  document.getElementById('tabOpen').setAttribute('aria-selected', 'true');
  document.getElementById('tabClosed').setAttribute('aria-selected', 'false');
  currentState = 'open';
  loadIssues('open');
});
document.getElementById('tabClosed').addEventListener('click', function() {
  document.getElementById('tabClosed').classList.add('active');
  document.getElementById('tabOpen').classList.remove('active');
  document.getElementById('tabClosed').setAttribute('aria-selected', 'true');
  document.getElementById('tabOpen').setAttribute('aria-selected', 'false');
  currentState = 'closed';
  loadIssues('closed');
});

loadIssues('open');
