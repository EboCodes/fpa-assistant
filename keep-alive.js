/**
 * FPA Assistant - Service Keep-Alive Daemon
 * 
 * Periodically pings Render backend & AI microservices to ensure
 * zero cold-start latency for students.
 */

const https = require('https');
const http = require('http');

const ENDPOINTS = [
  process.env.BACKEND_URL || 'https://fpa-backend-s09g.onrender.com/health',
  process.env.AI_SERVICE_URL || 'https://fpa-ai-service.onrender.com/health'
];

const PING_INTERVAL_MS = 5 * 60 * 1000; // 5 minutes

function pingUrl(targetUrl) {
  return new Promise((resolve) => {
    const protocol = targetUrl.startsWith('https') ? https : http;
    const startTime = Date.now();

    const req = protocol.get(targetUrl, { timeout: 30000 }, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        const duration = Date.now() - startTime;
        console.log(`[${new Date().toISOString()}] 🟢 Ping ${targetUrl} - HTTP ${res.statusCode} (${duration}ms)`);
        resolve(true);
      });
    });

    req.on('error', (err) => {
      console.error(`[${new Date().toISOString()}] 🔴 Ping failed for ${targetUrl}: ${err.message}`);
      resolve(false);
    });

    req.on('timeout', () => {
      req.destroy();
      console.warn(`[${new Date().toISOString()}] ⚠️ Ping timeout for ${targetUrl}`);
      resolve(false);
    });
  });
}

async function runPingCycle() {
  console.log(`\n==================================================`);
  console.log(`📡 FPA Keep-Alive Cycle: ${new Date().toLocaleString()}`);
  console.log(`==================================================`);

  for (const url of ENDPOINTS) {
    await pingUrl(url);
  }
}

// Initial cycle
runPingCycle();

// Recurring interval
setInterval(runPingCycle, PING_INTERVAL_MS);

console.log(`🚀 FPA Keep-Alive Service active. Pinging every ${PING_INTERVAL_MS / 60000} minutes.`);
