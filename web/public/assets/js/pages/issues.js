import { t, DISPLAY_LANG } from "../core/i18n.js";
import { escapeHtml } from "../core/dom.js";

const REPO = "fatonyahmadfauzi/Pixiv-OAuth-Token";
let currentState = "open";
const cache = {};

function timeAgo(dateStr) {
  const seconds = (Date.now() - new Date(dateStr)) / 1000;
  if (seconds < 60) return t("timeJustNow");
  if (seconds < 3600)
    return t("timeMinsAgo", { count: Math.floor(seconds / 60) });
  if (seconds < 86400)
    return t("timeHoursAgo", { count: Math.floor(seconds / 3600) });
  if (seconds < 2592000)
    return t("timeDaysAgo", { count: Math.floor(seconds / 86400) });
  return new Date(dateStr).toLocaleDateString(
    DISPLAY_LANG === "en" ? "en-US" : DISPLAY_LANG,
    { month: "short", day: "numeric", year: "numeric" },
  );
}

function renderIssueCard(issue) {
  const isPR = !!issue.pull_request;
  const iconClass = isPR
    ? "bi bi-git c-pr"
    : issue.state === "open"
      ? "bi bi-circle c-open"
      : "bi bi-check-circle c-closed";
  const labelsHtml = (issue.labels || [])
    .map(
      (label) =>
        `<span class="gh-issue-label gh-label-custom" data-bg="#${escapeHtml(label.color)}">${escapeHtml(label.name)}</span>`,
    )
    .join("");
  const body = issue.body
    ? escapeHtml(issue.body.replace(/\n/g, " ").slice(0, 150)) +
      (issue.body.length > 150 ? "…" : "")
    : "";

  return [
    `<article class="gh-issue-card" role="listitem">`,
    `<div class="gh-issue-icon"><i class="${iconClass}" aria-hidden="true"></i></div>`,
    `<div class="gh-issue-content">`,
    `<div class="gh-issue-top">`,
    `<a class="gh-issue-title" href="${escapeHtml(issue.html_url)}" target="_blank" rel="noopener">${escapeHtml(issue.title)}</a>`,
    isPR ? `<span class="gh-issue-pr-badge">PR</span>` : "",
    `</div>`,
    `<div class="gh-issue-meta">`,
    `<span>#${escapeHtml(String(issue.number))}</span>`,
    `<span>${t("issueOpenedBy", { time: escapeHtml(timeAgo(issue.created_at)) })} `,
    `<a class="gh-issue-author" href="${escapeHtml(issue.user.html_url)}" target="_blank" rel="noopener">`,
    `<img class="gh-issue-avatar" src="${escapeHtml(issue.user.avatar_url)}&s=20" width="16" height="16" alt="${escapeHtml(issue.user.login)}">`,
    escapeHtml(issue.user.login),
    `</a></span>`,
    `</div>`,
    labelsHtml ? `<div class="gh-issue-labels">${labelsHtml}</div>` : "",
    body ? `<p class="gh-issue-body">${body}</p>` : "",
    `</div>`,
    `<div class="gh-issue-aside">`,
    issue.comments > 0
      ? `<span class="gh-issue-comments" title="${escapeHtml(t("issueComments", { count: issue.comments }))}"><i class="bi bi-chat" aria-hidden="true"></i>${escapeHtml(String(issue.comments))}</span>`
      : "",
    `</div>`,
    `</article>`,
  ].join("");
}

function applyLabelColors() {
  document.querySelectorAll(".gh-label-custom").forEach((el) => {
    const bg = el.dataset.bg;
    if (bg) {
      el.style.background = bg + "22";
      el.style.color = bg;
      el.style.borderColor = bg + "44";
    }
  });
}

function renderIssueList(items, state) {
  const listEl = document.getElementById("issueList");
  const emptyEl = document.getElementById("emptyState");
  const skeletonEl = document.getElementById("skeletonWrap");
  const openTabEl = document.getElementById("tabOpen");
  const closedTabEl = document.getElementById("tabClosed");
  const openLabelEl = document.getElementById("openCountLabel");
  const closedLabelEl = document.getElementById("closedCountLabel");

  if (skeletonEl) skeletonEl.remove();

  const issues = items.filter((i) => !i.pull_request);
  const prs = items.filter((i) => !!i.pull_request);

  if (state === "open") {
    openTabEl?.classList.add("active");
    closedTabEl?.classList.remove("active");
    openTabEl?.setAttribute("aria-selected", "true");
    closedTabEl?.setAttribute("aria-selected", "false");
    if (openLabelEl)
      openLabelEl.textContent = t("issueCountOpen", { count: issues.length });
  } else {
    openTabEl?.classList.remove("active");
    closedTabEl?.classList.add("active");
    openTabEl?.setAttribute("aria-selected", "false");
    closedTabEl?.setAttribute("aria-selected", "true");
    if (closedLabelEl)
      closedLabelEl.textContent = t("issueCountClosed", {
        count: issues.length,
      });
  }

  if (!issues.length && !prs.length) {
    if (emptyEl) emptyEl.hidden = false;
    const emptyText = document.getElementById("emptyStateText");
    if (emptyText)
      emptyText.textContent =
        state === "open" ? t("issueEmptyOpen") : t("issueEmptyClosed");
    if (listEl) listEl.innerHTML = "";
    return;
  }

  let html = `<div role="list">`;
  if (issues.length) html += issues.map(renderIssueCard).join("");
  if (prs.length) {
    html += `<div class="gh-section-divider"><span>${t("issuePrSection", { count: prs.length })}</span></div>`;
    html += prs.map(renderIssueCard).join("");
  }
  html += `</div>`;
  if (listEl) listEl.innerHTML = html;
  applyLabelColors();
}

async function loadIssues(state) {
  const listEl = document.getElementById("issueList");
  const skeletonEl = document.getElementById("skeletonWrap");
  const emptyEl = document.getElementById("emptyState");
  if (emptyEl) emptyEl.hidden = true;

  if (!skeletonEl && listEl) {
    listEl.innerHTML = `<div class="gh-skeleton-wrap" id="skeletonWrap">${`<div class="gh-issue-skeleton"></div>`.repeat(5)}</div>`;
  } else if (skeletonEl) {
    skeletonEl.hidden = false;
  }

  if (cache[state]) {
    renderIssueList(cache[state], state);
    return;
  }

  try {
    const params = new URLSearchParams({
      path: `repos/${REPO}/issues`,
      state,
      per_page: 30,
    });
    const res = await fetch(`/api/github?${params}`);
    if (!res.ok) throw new Error(`proxy HTTP ${res.status}`);
    const data = await res.json();
    cache[state] = data;
    renderIssueList(data, state);
  } catch (err) {
    const sk = document.getElementById("skeletonWrap");
    if (sk) sk.remove();
    console.error("[issues.js] Failed to load issues:", err);
  }
}

export function setupIssuesPage() {
  const openTab = document.getElementById("tabOpen");
  const closedTab = document.getElementById("tabClosed");
  if (!openTab && !closedTab) return;

  openTab?.addEventListener("click", (e) => {
    e.preventDefault();
    if (currentState !== "open") {
      currentState = "open";
      loadIssues("open");
    }
  });
  closedTab?.addEventListener("click", (e) => {
    e.preventDefault();
    if (currentState !== "closed") {
      currentState = "closed";
      loadIssues("closed");
    }
  });
  loadIssues("open");
}
