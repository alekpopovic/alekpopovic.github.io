import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import lighthouse from 'lighthouse';
import * as chromeLauncher from 'chrome-launcher';
import { chromium } from '@playwright/test';

const external = process.argv[2]?.startsWith('https://') ? process.argv[2] : null;
const origin = 'http://127.0.0.1:4174';
const routes = external ? [external] : ['/', '/ai/', '/ai/workshops/', '/reading/', '/learn/ai-workflows/', '/projects/container-desk/', '/posts/codex-slash-commands/', '/cv/', '/codepop/', '/books/logbranik/', '/books/universal-tracking/16-realtime.html', '/posts/a-timeout-is-not-a-stopped-deployment/'];
let server, chrome;
fs.mkdirSync('reports', { recursive: true });
try {
  if (!external) {
    try { await fetch(origin); } catch {
      server = spawn('python3', ['scripts/serve-site.py'], { stdio: 'ignore', env: { ...process.env, SITE_TEST_PORT: '4174' } });
      let started = false;
      for (let n = 0; n < 50; n++) {
        try { await fetch(origin); started = true; break; } catch { await new Promise(resolve => setTimeout(resolve, 100)); }
      }
      if (!started) throw new Error('Static site server did not start. Build Jekyll first.');
    }
    // The reader and AI theme are separate bundles. Enforce the CSS a visitor
    // actually loads on every generated HTML page, including pages outside this lab sample.
    let largestCSS = 0, largestJS = 0;
    for (const file of fs.readdirSync('_site', { recursive: true }).filter(file => file.endsWith('.html'))) {
      const html = fs.readFileSync(path.join('_site', file), 'utf8');
      const styles = [...html.matchAll(/<link\b[^>]*rel="stylesheet"[^>]*href="([^"]+)"/g)].map(match => match[1]);
      const css = [...new Set(styles)].reduce((total, url) => total + fs.statSync(path.join('_site', new URL(url, origin).pathname)).size, 0);
      if (css > 130000) throw new Error(`CSS budget exceeded on ${file}: ${css} bytes.`);
      const scripts = [...html.matchAll(/<script\b[^>]*src="(\/assets\/js\/[^"]+)"/g)].map(match => match[1]);
      let js = [...new Set(scripts)].reduce((total, url) => total + fs.statSync(path.join('_site', new URL(url, origin).pathname)).size, 0);
      // The workshop fetches its worker only on its own page. Keep the same
      // 65 KB ceiling on each page's actual JS, including this deferred asset.
      if (scripts.some(url => url.endsWith('/labs/editor.js'))) js += fs.statSync('assets/js/labs/worker.js').size;
      if (js > 65000) throw new Error(`JS budget exceeded on ${file}: ${js} bytes.`);
      largestCSS = Math.max(largestCSS, css); largestJS = Math.max(largestJS, js);
    }
    console.log(`Asset budgets OK: largest page CSS ${largestCSS} bytes, largest page JS ${largestJS} bytes.`);
  }
  chrome = await chromeLauncher.launch({ chromePath: process.env.CHROME_PATH || chromium.executablePath(), chromeFlags: ['--headless', '--no-sandbox', '--disable-dev-shm-usage'] });
  const summaries = [];
  for (const route of routes) {
    const url = external ? route : origin + route;
    const result = await lighthouse(url, { port: chrome.port, output: ['json', 'html'], logLevel: 'error', onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
      // Local lab visits must not contribute traffic to the owner's GA4 property.
      blockedUrlPatterns: external ? [] : ['*googletagmanager.com/*', '*google-analytics.com/*'] });
    const key = external ? 'production' : (route.replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '') || 'home');
    fs.writeFileSync(`reports/lighthouse-${key}.json`, result.report[0]);
    fs.writeFileSync(`reports/lighthouse-${key}.html`, result.report[1]);
    const { lhr } = result;
    if (lhr.runtimeError) throw new Error(`Lighthouse could not measure ${url}: ${lhr.runtimeError.message}`);
    const summary = { url, scores: Object.fromEntries(Object.entries(lhr.categories).map(([name, value]) => [name, Math.round(value.score * 100)])),
      lcp: lhr.audits['largest-contentful-paint'].numericValue, cls: lhr.audits['cumulative-layout-shift'].numericValue,
      tbt: lhr.audits['total-blocking-time'].numericValue };
    summaries.push(summary);
    console.log(JSON.stringify(summary));
    if (!external && (summary.scores.performance < 85 || summary.scores.accessibility < 100 || summary.cls > .1)) process.exitCode = 1;
  }
  fs.writeFileSync(external ? 'reports/production-summary.json' : 'reports/performance-summary.json', JSON.stringify({ measuredAt: new Date().toISOString(), kind: 'Lighthouse mobile lab; not field Core Web Vitals', pages: summaries }, null, 2) + '\n');
} finally {
  if (chrome) await chrome.kill();
  if (server) server.kill();
}
