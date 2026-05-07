const http = require('http');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

const PORT = process.env.PORT || 3000;
const ROOT = __dirname;
const DATA_PATH = path.join(ROOT, 'data', 'historic-sites.json');
const PUBLIC = path.join(ROOT, 'public');

const clients = new Set();

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8'
};

function sendJson(res, status, body) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(body));
}

function readSites() {
  return JSON.parse(fs.readFileSync(DATA_PATH, 'utf-8'));
}

function serveStatic(res, filePath) {
  if (!filePath.startsWith(PUBLIC)) {
    res.writeHead(403);
    res.end('Forbidden');
    return;
  }

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end('Not Found');
      return;
    }
    const ext = path.extname(filePath);
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
    res.end(data);
  });
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);

  if (req.method === 'GET' && url.pathname === '/api/meta') {
    const sites = readSites();
    const states = [...new Set(sites.map((s) => s.state))].sort();
    return sendJson(res, 200, {
      totalSites: sites.length,
      states,
      transportModes: ['train', 'bus', 'car'],
      budgetTiers: ['low', 'mid', 'high'],
      note: 'NCERT/UPSC-oriented starter list; extend data/historic-sites.json for exhaustive coverage.'
    });
  }

  if (req.method === 'GET' && url.pathname === '/api/sites') {
    const { searchParams } = url;
    const q = (searchParams.get('q') || '').toLowerCase();
    const mode = searchParams.get('mode') || 'all';
    const budgetTier = searchParams.get('budgetTier') || 'all';
    const era = searchParams.get('era') || 'all';
    const state = searchParams.get('state') || 'all';

    let sites = readSites();

    if (q) {
      sites = sites.filter((s) => `${s.name} ${s.city} ${s.state} ${s.type} ${s.ncertUpscTag}`.toLowerCase().includes(q));
    }
    if (mode !== 'all') sites = sites.filter((s) => s.transport.includes(mode));
    if (budgetTier !== 'all') sites = sites.filter((s) => s.budgetTier === budgetTier);
    if (era !== 'all') sites = sites.filter((s) => s.era.toLowerCase().includes(era.toLowerCase()));
    if (state !== 'all') sites = sites.filter((s) => s.state === state);

    return sendJson(res, 200, { count: sites.length, sites });
  }

  if (req.method === 'GET' && url.pathname === '/api/notes/stream') {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      Connection: 'keep-alive'
    });
    res.write('event: connected\ndata: "ok"\n\n');
    clients.add(res);
    req.on('close', () => clients.delete(res));
    return;
  }

  if (req.method === 'POST' && url.pathname === '/api/notes') {
    let body = '';
    req.on('data', (chunk) => (body += chunk));
    req.on('end', () => {
      try {
        const parsed = JSON.parse(body || '{}');
        const message = String(parsed.message || '').trim();
        if (!message) return sendJson(res, 400, { error: 'message is required' });

        const payload = JSON.stringify({ message, at: new Date().toISOString() });
        clients.forEach((client) => client.write(`event: note\ndata: ${payload}\n\n`));
        sendJson(res, 200, { ok: true });
      } catch (error) {
        sendJson(res, 400, { error: 'invalid json' });
      }
    });
    return;
  }

  const requested = url.pathname === '/' ? '/index.html' : url.pathname;
  serveStatic(res, path.join(PUBLIC, requested));
});

server.listen(PORT, () => {
  console.log(`BharatYatra Planner running at http://localhost:${PORT}`);
});
