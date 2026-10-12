const { test, expect } = require('./fixtures');
const fs = require('node:fs');
const source = fs.readFileSync('assets/js/ga4-events.js', 'utf8');

async function fixture(page, { host = 'site.example', privacy = false } = {}) {
  await page.addInitScript(({ privacy }) => {
    window.recorded = [];
    window.gtag = (...args) => window.recorded.push(args);
    if (privacy) Object.defineProperty(navigator, 'globalPrivacyControl', { value: true });
  }, { privacy });
  await page.route('https://site.example/**', route => route.fulfill(route.request().url().endsWith('/ga4.js') ? { contentType: 'text/javascript', body: source } : {
    contentType: 'text/html', body: `<!doctype html><html lang="en"><head><title>Events</title><script src="/ga4.js" data-ga4-host="${host}" defer></script></head><body><main data-reader-book="sample" data-reader-chapter="05-example"><div data-reader-scroll style="height:500px;overflow:auto"><article class="book-article" style="height:4000px">Sample chapter</article></div><a href="/assets/books/sample/downloads/book.epub">Download</a><a href="https://github.com/alekpopovic/orch">Source</a><a href="mailto:private@example.com">Contact</a></main></body></html>`
  }));
  await page.goto('https://site.example/books/sample/05-example.html?q=private#private');
}

test('GA4 content events identify chapters, downloads and actions without transmitting private fields', async ({ page }) => {
  await page.clock.install();
  await fixture(page);
  await page.evaluate(() => {
    document.querySelectorAll('a').forEach(link => { link.addEventListener('click', event => event.preventDefault()); link.click(); });
    document.dispatchEvent(new CustomEvent('codepop:analytics', { detail: { name: 'chapter_complete', props: { book_id: 'sample', chapter_slug: '05-example', note: 'private note', query: 'private query', channel: 'mailto:private@example.com' } } }));
    document.dispatchEvent(new CustomEvent('codepop:analytics', { detail: { name: 'private_unknown_event', props: {} } }));
  });
  await page.clock.fastForward(31000);
  await page.evaluate(() => { const panel = document.querySelector('[data-reader-scroll]'); panel.scrollTop = 3200; panel.dispatchEvent(new Event('scroll')); panel.dispatchEvent(new Event('scroll')); });
  const events = await page.evaluate(() => window.recorded);
  expect(events.map(event => event[1])).toEqual(['chapter_open', 'book_download', 'project_open', 'contact_open', 'chapter_complete', 'reading_engaged']);
  expect(events[0][2]).toEqual({ book_id: 'sample', chapter_slug: '05-example' });
  expect(events[1][2]).toEqual({ book_id: 'sample', format: 'epub' });
  expect(events[4][2]).toEqual({ book_id: 'sample', chapter_slug: '05-example' });
  expect(JSON.stringify(events)).not.toContain('private');
});

for (const options of [{ privacy: true }, { host: 'www.alekpopovic.com' }]) {
  test(`GA4 content events stay disabled for ${options.privacy ? 'privacy signals' : 'another hostname'}`, async ({ page }) => {
    await fixture(page, options);
    expect(await page.evaluate(() => window.recorded)).toEqual([]);
  });
}
