const { test, expect } = require('./fixtures');
const fs = require('node:fs');

const source = fs.readFileSync('assets/js/analytics.js', 'utf8');

async function mockSite(page, privacy = false, readerPanel = false) {
  await page.addInitScript(({ privacy }) => {
    window.recordedEvents = [];
    window.fetch = async (_url, options) => { window.recordedEvents.push(JSON.parse(options.body)); return new Response('', { status: 202 }); };
    if (privacy) Object.defineProperty(navigator, 'globalPrivacyControl', { value: true });
  }, { privacy });
  await page.route('https://site.example/**', route => {
    if (route.request().url().includes('/analytics.js')) return route.fulfill({ contentType: 'text/javascript', body: source });
    return route.fulfill({ contentType: 'text/html', body: `<!doctype html><html lang="en"><head><title>Analytics fixture</title><script src="/analytics.js" data-domain="site.example" data-endpoint="https://stats.example/api/event" defer></script></head><body>${readerPanel ? '<div data-reader-scroll style="height:500px;overflow:auto">' : ''}<article class="book-article" style="height:4000px">Reading fixture</article>${readerPanel ? '</div>' : ''}<a href="/assets/books/new-book/downloads/new.pdf">Download</a><a href="https://github.com/alekpopovic/orch">Project</a><a href="mailto:private@example.com">Contact</a></body></html>` });
  });
  await page.goto('https://site.example/reading/?q=private#section');
}

test('the Google tag initializes once across page layouts', async ({ page }) => {
  for (const path of ['/', '/codepop/', '/cv/', '/books/universal-tracking/16-realtime.html', '/posts/a-timeout-is-not-a-stopped-deployment/', '/404.html']) {
    await page.goto(path);
    const tag = page.locator('head script[src^="https://www.googletagmanager.com/gtag/js"]');
    await expect(tag).toHaveCount(1);
    await expect(tag).toHaveAttribute('src', 'https://www.googletagmanager.com/gtag/js?id=G-QCGFECRJDS');
    expect(await tag.evaluate(script => script.async)).toBe(true);
    const events = await page.evaluate(() => window.dataLayer.map(event => Array.from(event)));
    expect(events).toHaveLength(2);
    expect(events[0][0]).toBe('js');
    expect(events[0][1]).toBeInstanceOf(Date);
    expect(events[1]).toEqual(['config', 'G-QCGFECRJDS', { page_location: 'http://127.0.0.1:4173' + path, page_referrer: expect.any(String) }]);
  }
});

test('Plausible stays disabled without owner configuration', async ({ page }) => {
  const analyticsRequests = [];
  page.on('request', request => { if (request.url().includes('plausible')) analyticsRequests.push(request.url()); });
  await page.goto('/');
  await expect(page.locator('script[data-domain]')).toHaveCount(0);
  expect(analyticsRequests).toEqual([]);
});

test('configured analytics records useful events and omits query and contact data', async ({ page }) => {
  await page.clock.install();
  await mockSite(page);
  await expect.poll(() => page.evaluate(() => window.recordedEvents.length)).toBe(1);
  await page.evaluate(() => {
    // Prevent fixture navigation without interfering with the document listener.
    document.querySelectorAll('a').forEach(link => link.addEventListener('click', event => event.preventDefault()));
    document.querySelectorAll('a').forEach(link => link.click());
  });
  await page.clock.fastForward(31000);
  await page.evaluate(() => { scrollTo(0, 3200); dispatchEvent(new Event('scroll')); });
  const events = await page.evaluate(() => window.recordedEvents);
  expect(events.map(event => event.name)).toEqual(['pageview', 'Book download', 'Project click', 'Contact click', 'Engaged reading']);
  expect(events[1].props).toEqual({ book: 'new-book', format: 'pdf' });
  expect(events[2].props).toEqual({ project: 'orch' });
  expect(events[3].props).toEqual({ channel: 'mailto' });
  expect(events.every(event => event.url === 'https://site.example/reading/')).toBe(true);
  expect(JSON.stringify(events)).not.toContain('private');
});

test('configured analytics respects the browser privacy signal', async ({ page }) => {
  await mockSite(page, true);
  expect(await page.evaluate(() => window.recordedEvents)).toEqual([]);
});

test('configured chapter analytics measures the text panel independently of the page', async ({ page }) => {
  await page.clock.install();
  await mockSite(page, false, true);
  await page.clock.fastForward(31000);
  await page.evaluate(() => {
    const panel = document.querySelector('[data-reader-scroll]');
    panel.scrollTop = 3200;
    panel.dispatchEvent(new Event('scroll'));
    panel.dispatchEvent(new Event('scroll'));
  });
  expect(await page.evaluate(() => scrollY)).toBe(0);
  const events = await page.evaluate(() => window.recordedEvents);
  expect(events.map(event => event.name)).toEqual(['pageview', 'Engaged reading']);
  expect(events[1].props).toEqual({ kind: 'chapter' });
});
