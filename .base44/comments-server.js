// Tiny comment store for the preview feedback tool. No dependencies. Data lives in /data/comments.json (a docker volume, not the repo).
const http = require('http');
const fs = require('fs');
const FILE = '/data/comments.json';
let items = [];
try { items = JSON.parse(fs.readFileSync(FILE, 'utf8')); } catch (e) {}
const save = () => fs.writeFileSync(FILE, JSON.stringify(items, null, 2));
const send = (res, code, body) => { res.writeHead(code, { 'Content-Type': 'application/json' }); res.end(JSON.stringify(body)); };

http.createServer((req, res) => {
  const u = new URL(req.url, 'http://x');
  const m = u.pathname.match(/^\/_b44_api\/comments(?:\/(\w+))?$/);
  if (!m) return send(res, 404, { error: 'not found' });
  const id = m[1];
  if (req.method === 'GET') return send(res, 200, items);
  if (req.method === 'DELETE' && id) { items = items.filter(c => c.id !== id); save(); return send(res, 200, { ok: true }); }
  let raw = '';
  req.on('data', d => { raw += d; if (raw.length > 100000) req.destroy(); });
  req.on('end', () => {
    let b = {};
    try { b = JSON.parse(raw || '{}'); } catch (e) { return send(res, 400, { error: 'bad json' }); }
    if (req.method === 'POST' && !id) {
      const c = {
        id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6),
        author: String(b.author || 'Anonymous').slice(0, 60),
        file: String(b.file || '').slice(0, 300),
        element: String(b.element || '').slice(0, 300),
        selector: String(b.selector || '').slice(0, 500),
        text: String(b.text || '').slice(0, 2000),
        resolved: false,
        createdAt: new Date().toISOString()
      };
      if (!c.text.trim()) return send(res, 400, { error: 'empty' });
      items.push(c); save(); return send(res, 200, c);
    }
    if (req.method === 'PATCH' && id) {
      const c = items.find(x => x.id === id);
      if (!c) return send(res, 404, { error: 'not found' });
      c.resolved = !!b.resolved; save(); return send(res, 200, c);
    }
    send(res, 405, { error: 'method' });
  });
}).listen(8080, '0.0.0.0');
