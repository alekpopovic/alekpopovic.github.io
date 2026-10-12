const { test, expect } = require('./fixtures');
const fs = require('node:fs');
const source = fs.readFileSync('assets/js/web-vitals.js', 'utf8');
const core = `export const onLCP = f => f({name:'LCP',value:1234.56789,rating:'good',entries:['private-selector'],id:'private-id'}); export const onINP = f => { f({name:'INP',value:99,rating:'good'}); f({name:'UNKNOWN',value:1,rating:'good'}); f({name:'INP',value:NaN,rating:'poor'}); }; export const onCLS = f => f({name:'CLS',value:.01234,rating:'good',attribution:'private'});`;
async function fixture(page, options = {}) {
  let imported = 0;
  await page.addInitScript(({ privacy }) => { window.recorded = []; window.gtag = (...args) => window.recorded.push(args); if (privacy) Object.defineProperty(navigator, 'globalPrivacyControl', { value: true }); }, options);
  await page.route('https://metrics.example/**', route => {
    const pathname = new URL(route.request().url()).pathname;
    if (pathname === '/assets/vendor/web-vitals.js') { imported++; return route.fulfill({ contentType: 'text/javascript', body: core }); }
    if (pathname === '/assets/js/web-vitals.js') return route.fulfill({ contentType: 'text/javascript', body: source });
    return route.fulfill({ contentType: 'text/html', body: `<html><head><script src="/assets/js/web-vitals.js" data-vitals-host="${options.host || 'metrics.example'}" defer></script></head><body>Metrics</body></html>` });
  });
  await page.goto('https://metrics.example/example/?q=private#private');
  return () => imported;
}
test('field metrics send bounded core values without selectors, IDs or private query attribution', async ({ page }) => {
  const imported = await fixture(page);
  await expect.poll(() => page.evaluate(() => window.recorded.length)).toBe(3);
  expect(imported()).toBe(1);
  expect(await page.evaluate(() => window.recorded)).toEqual([
    ['event', 'web_vital', { metric_name: 'LCP', metric_value: 1234.568, metric_rating: 'good', non_interaction: true }],
    ['event', 'web_vital', { metric_name: 'INP', metric_value: 99, metric_rating: 'good', non_interaction: true }],
    ['event', 'web_vital', { metric_name: 'CLS', metric_value: .012, metric_rating: 'good', non_interaction: true }]
  ]);
});
for (const options of [{ privacy: true }, { host: 'another.example' }]) test(`field metrics do not even load the core under ${options.privacy ? 'privacy signals' : 'another hostname'}`, async ({ page }) => {
  const imported = await fixture(page, options); expect(imported()).toBe(0); expect(await page.evaluate(() => window.recorded)).toEqual([]);
});
