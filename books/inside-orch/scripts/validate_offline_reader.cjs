/* Actual file-URL and owned-loopback offline reader checks. No external access. */
const fs = require('fs');
const path = require('path');
const http = require('http');
const crypto = require('crypto');
const {pathToFileURL} = require('url');
const {chromium} = require('@playwright/test');

(async () => {
  const book = path.resolve(__dirname, '..');
  const root = path.join(book, 'dist/online');
  const output = path.resolve(process.argv[2] || path.join(book, 'validation/publication/offline-reader.json'));
  const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
  const files = [];
  function walk(dir) {
    for (const entry of fs.readdirSync(dir, {withFileTypes: true})) {
      const full = path.join(dir, entry.name);
      if (entry.isSymbolicLink()) throw new Error('Export contains symlink');
      if (entry.isDirectory()) walk(full); else files.push(path.relative(root, full).split(path.sep).join('/'));
    }
  }
  walk(root);
  const sections = files.filter(n => !n.includes('/') && n.endsWith('.html') && n !== 'index.html').sort();
  if (sections.length !== 47) throw new Error('Expected 47 sections');
  const evidence = {started_at_utc: new Date().toISOString(), source_sha: JSON.parse(fs.readFileSync(path.join(book, 'book.json'))).source_sha,
    scope: 'Actual Chromium with JavaScript disabled; all HTML local targets/fragments checked. Two transports: file URL and temporary owned127.0.0.1 server. No search/modules/service worker required.',
    command: process.argv, working_directory: process.cwd(), input_sha256: {}, cases: [], navigation: [], external_references: 0, external_network_attempts: [], failures: []};
  for (const file of files.sort()) evidence.input_sha256[file] = sha(fs.readFileSync(path.join(root, file)));
  const server = http.createServer((req, res) => {
    try {
      let rel = decodeURIComponent(new URL(req.url, 'http://127.0.0.1').pathname);
      if (rel.endsWith('/')) rel += 'index.html';
      const full = path.resolve(root, '.' + rel);
      if (!full.startsWith(root + path.sep) || !fs.statSync(full).isFile()) {res.writeHead(404); return res.end();}
      const types = {'.html': 'text/html; charset=utf-8', '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png', '.ttf': 'font/ttf'};
      res.writeHead(200, {'Content-Type': types[path.extname(full)] || 'application/octet-stream'}); res.end(fs.readFileSync(full));
    } catch {res.writeHead(404); res.end();}
  });
  let browser;
  try {
    await new Promise((resolve, reject) => {server.once('error', reject); server.listen(0, '127.0.0.1', resolve);});
    const origin = `http://127.0.0.1:${server.address().port}`;
    evidence.owned_server = {origin, binding: '127.0.0.1', ephemeral_port: true};
    browser = await chromium.launch({executablePath: process.env.CHROME_PATH || '/opt/google/chrome/chrome', args: ['--no-sandbox']});
    evidence.browser_version = browser.version();
    const context = await browser.newContext({javaScriptEnabled: false, viewport: {width: 1280, height: 900}});
    await context.route(/^https?:/, route => {
      if (new URL(route.request().url()).origin === origin) return route.continue();
      evidence.external_network_attempts.push(route.request().url()); return route.abort();
    });
    const page = await context.newPage();
    page.on('pageerror', error => evidence.failures.push(String(error)));
    for (const transport of ['file', 'loopback']) {
      const target = rel => transport === 'file' ? pathToFileURL(path.join(root, rel)).href : origin + '/' + rel;
      for (const rel of files.filter(n => n.endsWith('.html'))) {
        await page.goto(target(rel));
        const data = await page.evaluate(() => ({title: document.title, h1: document.querySelector('h1')?.textContent,
          contents: document.querySelectorAll('nav[aria-label="Book contents"] li a').length,
          scripts: document.scripts.length, images: [...document.images].map(i => ({src: i.getAttribute('src'), loaded: i.complete && i.naturalWidth > 0})),
          targets: [...document.querySelectorAll('[href],[src]')].map(e => e.getAttribute('href') || e.getAttribute('src')),
          ids: [...document.querySelectorAll('[id]')].map(e => e.id)}));
        if (!data.h1 || data.scripts || data.images.some(i => !i.loaded)) evidence.failures.push(transport + ':' + rel + ':missing heading/image or script');
        if (sections.includes(rel) && data.contents !== 47) evidence.failures.push(transport + ':' + rel + ':contents');
        evidence.cases.push({transport, file: rel, title: data.title, contents: data.contents, images: data.images});
        for (const href of data.targets) {
          if (!href || /^(mailto:|tel:)/.test(href)) continue;
          if (/^https?:/.test(href)) {evidence.external_references++; continue;}
          const url = new URL(href, target(rel));
          const dest = transport === 'file' ? decodeURIComponent(url.pathname) : path.join(root, decodeURIComponent(url.pathname));
          if (!dest.startsWith(root + path.sep) || !fs.existsSync(dest)) {evidence.failures.push(rel + ':missing/escaped:' + href); continue;}
          if (url.hash && dest.endsWith('.html')) {
            const escaped = decodeURIComponent(url.hash.slice(1)).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            if (!new RegExp('id=["\u0027]' + escaped + '["\u0027]').test(fs.readFileSync(dest, 'utf8'))) evidence.failures.push(rel + ':missing fragment:' + href);
          }
        }
      }
      await page.goto(target('index.html'));
      await page.getByRole('link', {name: 'Start reading', exact: true}).click();
      evidence.navigation.push({transport, action: 'landing to preface', passed: page.url().endsWith('/00-preface.html')});
      await page.locator('a[rel="next"]').click();
      evidence.navigation.push({transport, action: 'preface next', passed: page.url().includes('/01-')});
      await page.locator('a[rel="prev"]').click();
      evidence.navigation.push({transport, action: 'chapter1 previous', passed: page.url().endsWith('/00-preface.html')});
      await page.locator('nav[aria-label="Book contents"] a').nth(4).click();
      await page.locator('a[href*="solutions/ch04.html"]').first().click();
      evidence.navigation.push({transport, action: 'chapter4 contents then worked answers', passed: page.url().includes('/solutions/ch04.html')});
      const sample = [sections[0], sections[4], sections.find(n => n.startsWith('a-cli')), sections.find(n => n.startsWith('b-lifecycle'))];
      for (const width of [390, 1280]) for (const rel of sample) {
        await page.setViewportSize({width, height: 900}); await page.goto(target(rel));
        // FontFaceSet.check may precede lazy font selection after navigation.
        // Explicitly await the actual local font load, rather than a timing guess.
        await page.evaluate(async () => {await document.fonts.load('16px DM'); await document.fonts.ready;});
        const dimensions = await page.evaluate(() => ({width: innerWidth, document_width: document.documentElement.scrollWidth,
          font: getComputedStyle(document.body).fontFamily, fonts_loaded: document.fonts.check('16px DM'), tables: document.querySelectorAll('table').length, code: document.querySelectorAll('pre').length}));
        evidence.cases.push({transport, file: rel, viewport: width, ...dimensions});
        if (dimensions.document_width > width + 2 || !dimensions.fonts_loaded) evidence.failures.push(transport + ':' + rel + ':responsive/font failure');
      }
    }
    if (evidence.navigation.some(n => !n.passed)) evidence.failures.push('Navigation assertion failed');
    if (evidence.external_network_attempts.length) evidence.failures.push('Unexpected network asset request');
    evidence.finished_at_utc = new Date().toISOString(); evidence.status = evidence.failures.length ? 'failed' : 'passed';
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
    evidence.owned_server_closed = !server.listening;
    fs.mkdirSync(path.dirname(output), {recursive: true}); fs.writeFileSync(output, JSON.stringify(evidence, null, 2) + '\n');
  }
  console.log(JSON.stringify({status: evidence.status, cases: evidence.cases.length, sections: sections.length, failures: evidence.failures, owned_server_closed: evidence.owned_server_closed}));
  if (evidence.status !== 'passed') process.exitCode = 1;
})().catch(error => {console.error(error); process.exitCode = 1;});
