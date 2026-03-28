/**
 * api/_security.js
 * L7 Application Security Middleware
 * - Blocks suspicious Bots (Missing/Bad User-Agent)
 * - Validates Origin/Referer to prevent Cross-Origin exploitation
 * - Simple memory-based IP Rate Limiting (Protects Vercel quotas and Upstream limits)
 */

const ipRequestCounts = new Map();
const RESET_INTERVAL_MS = 15 * 60 * 1000; // 15 minutes window
const MAX_REQUESTS = 30; // Max allowed requests per window

// Clean memory periodically to prevent leaks in long-running lambdas
setInterval(() => {
  ipRequestCounts.clear();
}, RESET_INTERVAL_MS);

function checkSecurity(req) {
  // 1. Rate Limiting (IP Based)
  const clientIp = req.headers['x-forwarded-for'] || req.socket.remoteAddress || 'unknown';
  const currentCount = ipRequestCounts.get(clientIp) || 0;

  if (currentCount >= MAX_REQUESTS) {
    return { ok: false, status: 429, error: "Too Many Requests. Please try again later." };
  }
  ipRequestCounts.set(clientIp, currentCount + 1);

  // 2. User-Agent Validation (Block simple scripted attacks)
  const ua = (req.headers['user-agent'] || '').toLowerCase();
  if (!ua || ua.includes('curl/') || ua.includes('python-requests') || ua.includes('postman')) {
    return { ok: false, status: 403, error: "Forbidden: Suspicious User-Agent detected." };
  }

  // 3. Origin/Referer Validation (Prevent cross-origin API abuse)
  const referer = (req.headers['referer'] || '').toLowerCase();
  const origin = (req.headers['origin'] || '').toLowerCase();
  
  // Exempt localhost for development purposes
  if (origin.includes('localhost') || referer.includes('localhost')) {
    return { ok: true };
  }

  // Production check: Only allow your vercel app / custom domain
  // Replace these domains with your actual production domains if you have custom ones
  const allowedDomains = ['pixiv-oauth', 'faton', 'vercel.app'];
  
  const isRefererValid = referer && allowedDomains.some(d => referer.includes(d));
  const isOriginValid = origin && allowedDomains.some(d => origin.includes(d));

  if (!isRefererValid && !isOriginValid && req.method !== 'GET') {
    // We allow GET (github.js) without strict origin if it was opened directly,
    // but POST (token.js) MUST come from our domain.
    return { ok: false, status: 403, error: "Forbidden: Invalid Origin/Referer." };
  }

  return { ok: true };
}

module.exports = { checkSecurity };
