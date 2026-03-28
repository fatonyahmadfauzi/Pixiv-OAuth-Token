/**
 * api/github.js — Secure GitHub API Proxy
 * Reads GITHUB_TOKEN from Vercel environment variables.
 * Frontend calls /api/github?path=repos/owner/repo/issues&...
 * Never exposes the token to the client.
 */

const { checkSecurity } = require('./_security');

const ALLOWED_PREFIXES = [
  'repos/fatonyahmadfauzi/Pixiv-OAuth-Token/issues',
  'repos/fatonyahmadfauzi/Pixiv-OAuth-Token/pulls',
  'repos/fatonyahmadfauzi/Pixiv-OAuth-Token',
];

module.exports = async (req, res) => {
  // Only allow GET requests
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const sec = checkSecurity(req);
  if (!sec.ok) {
    return res.status(sec.status).json({ error: sec.error });
  }

  const { path, ...params } = req.query;

  // Validate path exists
  if (!path) {
    return res.status(400).json({ error: 'Missing path parameter' });
  }

  // Security: only allow specific GitHub API paths for this repo
  const isAllowed = ALLOWED_PREFIXES.some(prefix => path.startsWith(prefix));
  if (!isAllowed) {
    return res.status(403).json({ error: 'Forbidden: path not allowed' });
  }

  // Build query string from remaining params
  const qs = new URLSearchParams(params).toString();
  const url = `https://api.github.com/${path}${qs ? '?' + qs : ''}`;

  const headers = {
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'User-Agent': 'Pixiv-OAuth-Web/1.0',
  };

  // Attach token from env if available (5000 req/hr instead of 60)
  if (process.env.GITHUB_TOKEN) {
    headers['Authorization'] = `Bearer ${process.env.GITHUB_TOKEN}`;
  }

  try {
    const upstream = await fetch(url, { headers });

    // Forward rate limit headers to client (useful for debugging)
    const rl = upstream.headers.get('x-ratelimit-remaining');
    if (rl) res.setHeader('X-RateLimit-Remaining', rl);

    const data = await upstream.json();
    return res.status(upstream.status).json(data);
  } catch (err) {
    return res.status(502).json({ error: 'Failed to fetch from GitHub API', detail: err.message });
  }
};
