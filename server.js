/**
 * Project ORCA — Unified Node.js Frontend & Gateway Server
 * Serves tactical frontend on port 5173 and transparently proxies /v1 & /health to FastAPI on port 8000.
 */
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 5173;
const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';
const FRONTEND_DIR = path.join(__dirname, 'frontend');

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const pathname = url.pathname;

  // 1. Transparent Proxy for Backend API Routes (/v1/*, /health, /docs, /openapi.json)
  if (pathname.startsWith('/v1') || pathname.startsWith('/health') || pathname.startsWith('/docs') || pathname === '/openapi.json') {
    const targetUrl = new URL(pathname + url.search, BACKEND_URL);
    
    const proxyReq = http.request(targetUrl, {
      method: req.method,
      headers: {
        ...req.headers,
        host: targetUrl.host
      }
    }, (proxyRes) => {
      res.writeHead(proxyRes.statusCode, proxyRes.headers);
      proxyRes.pipe(res);
    });

    proxyReq.on('error', (err) => {
      console.error(`[Node Proxy Error] Failed to reach FastAPI backend at ${targetUrl}:`, err.message);
      res.writeHead(502, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        error: 'Bad Gateway',
        message: 'FastAPI backend is offline on port 8000. Start backend using: py -m uvicorn src.main:app --app-dir backend --port 8000 --reload'
      }));
    });

    req.pipe(proxyReq);
    return;
  }

  // 2. Serve Frontend Static Files
  let filePath = path.join(FRONTEND_DIR, pathname === '/' ? 'index.html' : pathname);

  // Security check: prevent directory traversal
  if (!filePath.startsWith(FRONTEND_DIR)) {
    res.writeHead(403, { 'Content-Type': 'text/plain' });
    res.end('Forbidden');
    return;
  }

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      // Fallback to index.html for SPA routing
      filePath = path.join(FRONTEND_DIR, 'index.html');
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    fs.readFile(filePath, (readErr, content) => {
      if (readErr) {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Internal Server Error');
        return;
      }
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content);
    });
  });
});

server.listen(PORT, () => {
  console.log(`=======================================================`);
  console.log(`  Project ORCA — Node.js Frontend Gateway Active`);
  console.log(`  Local URL : http://localhost:${PORT}`);
  console.log(`  Backend   : ${BACKEND_URL}`);
  console.log(`=======================================================`);
});
