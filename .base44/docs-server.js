// Document visibility store: only the admin (B44_ADMIN_PASSWORD) can change which documents
// the public front page shows. Data lives in /data/documents.json (a docker volume, not the repo).
// Public read: GET /_b44_api/documents -> { configured, published, updatedAt }
// Admin write: PUT /_b44_api/documents  body { published: ["path/to/file.html", ...] } (Bearer auth)
const http = require('http');
const crypto = require('crypto');
const fs = require('fs');

const FILE = '/data/documents.json';
const PASS = process.env.B44_ADMIN_PASSWORD || '';

let state = { configured: false, published: [] };
try {
  const raw = JSON.parse(fs.readFileSync(FILE, 'utf8'));
  if (raw && typeof raw === 'object') {
    state.configured = !!raw.configured;
    state.published = Array.isArray(raw.published) ? raw.published.filter(s => typeof s === 'string') : [];
  }
} catch (e) {}

const save = () => fs.writeFileSync(FILE, JSON.stringify(state, null, 2));
const send = (res, code, body) => {
  res.writeHead(code, { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' });
  res.end(JSON.stringify(body));
};
const safeEqual = (a, b) => {
  const ab = Buffer.from(String(a));
  const bb = Buffer.from(String(b));
  if (ab.length !== bb.length) return false;
  return crypto.timingSafeEqual(ab, bb);
};
function isAuthorized(req) {
  if (!PASS) return false; // admin password not configured -> no admin access
  const h = req.headers['authorization'] || '';
  return h.startsWith('Bearer ') && safeEqual(h.slice(7), PASS);
}

http.createServer((req, res) => {
  const u = new URL(req.url, 'http://x');
  if (u.pathname !== '/_b44_api/documents') return send(res, 404, { error: 'not found' });

  if (req.method === 'GET') return send(res, 200, state);

  // Every mutation requires the admin password.
  if (!isAuthorized(req)) return send(res, 401, { error: 'unauthorized' });

  let raw = '';
  req.on('data', d => { raw += d; if (raw.length > 200000) req.destroy(); });
  req.on('end', () => {
    let b = {};
    try { b = JSON.parse(raw || '{}'); } catch (e) { return send(res, 400, { error: 'bad json' }); }
    if (req.method === 'PUT') {
      const pub = Array.isArray(b.published)
        ? b.published.filter(s => typeof s === 'string').map(s => s.slice(0, 1000))
        : [];
      state = { configured: true, published: pub, updatedAt: new Date().toISOString() };
      save();
      return send(res, 200, state);
    }
    send(res, 405, { error: 'method' });
  });
}).listen(8081, '0.0.0.0');
