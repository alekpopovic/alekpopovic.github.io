const { test, expect } = require('./fixtures');
const AxeBuilder = require('@axe-core/playwright').default;
const fs = require('node:fs');

const root = '/books/inside-orch/';
const chapter = `${root}06-follow-one-request-through-the-control-plane.html`;

test('Inside orch exposes all 47 sections and exact reviewed download copies', async ({ page, request }) => {
  await page.goto(root);
  await expect(page.locator('.book-contents-list li')).toHaveCount(47);
  const image = page.locator('.overview-cover img');
  await expect.poll(() => image.evaluate(value => value.complete && value.naturalWidth > 0)).toBe(true);
  for (const format of ['pdf', 'epub']) {
    const url = `/assets/books/inside-orch/downloads/inside-orch.${format}`;
    await expect(page.locator(`a[download][href="${url}"]`)).toBeVisible();
    const response = await request.get(url);
    expect(response.status()).toBe(200);
    expect(await response.body()).toEqual(fs.readFileSync(`books/inside-orch/dist/inside-orch.${format}`));
  }
});

test('Inside orch connects chapter notes, saved reading and combined post filters', async ({ page }) => {
  await page.goto(chapter);
  await expect(page.locator('.reader-chapters li')).toHaveCount(47);
  await expect(page.locator('.book-article h1')).toHaveText('Chapter 6 - Follow One Request Through the Control Plane');
  await page.locator('.book-related-notes a').first().click();
  await expect(page.locator(`.post-article a[href="${chapter}"]`).first()).toBeVisible();
  await page.goto(root);
  await expect(page.locator('[data-resume-book="inside-orch"]')).toHaveAttribute('href', `${chapter}?resume=1`);
  await page.goto('/posts/?book=inside-orch&category=Reliability&q=ready');
  await expect(page.locator('#posts-grid .post-card:visible')).toHaveCount(1);
  await page.reload();
  await expect(page.locator('#posts-grid .post-card:visible')).toHaveCount(1);
  await page.locator('#post-search').fill('no-orch-topic-918273');
  await expect(page.locator('[data-post-empty]')).toBeVisible();
});

test('Inside orch mobile reading retains keyboard controls and accessible diagrams', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(`${root}04-domain-models-and-state-machines.html`);
  const figure = page.locator('.book-article img');
  await expect(figure).toHaveAttribute('alt', /task|lifecycle|transition/i);
  await expect.poll(() => figure.evaluate(value => value.complete && value.naturalWidth > 0)).toBe(true);
  const notes = page.getByRole('button', { name: 'Open bookmarks and notes' });
  await notes.focus(); await page.keyboard.press('Enter');
  await expect(page.locator('#reader-note')).toBeFocused();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  const audit = await new AxeBuilder({ page }).analyze();
  expect(audit.violations.filter(item => ['serious', 'critical'].includes(item.impact))).toEqual([]);
});

test('Inside orch answers and full contents remain readable without JavaScript', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  try {
    await page.goto(`http://127.0.0.1:4173${chapter}`);
    await expect(page.locator('.book-article h1')).toBeVisible();
    await expect(page.locator('.reader-chapters li')).toHaveCount(47);
    await page.locator('.book-article a[href*="/companion/manuscript/solutions/ch06.html"]').click();
    await expect(page.locator('main')).toContainText(/answer|solution/i);
    const response = await page.goto(`http://127.0.0.1:4173${root}nonexistent-section.html`);
    expect(response.status()).toBe(404);
  } finally {
    await context.close();
  }
});

test('Inside orch notes still export when browser storage is unavailable', async ({ page }) => {
  await page.addInitScript(() => {
    Storage.prototype.getItem = () => { throw new DOMException('Unavailable', 'SecurityError'); };
    Storage.prototype.setItem = () => { throw new DOMException('Unavailable', 'SecurityError'); };
  });
  await page.goto(chapter);
  await page.getByRole('button', { name: 'Open bookmarks and notes' }).click();
  await page.locator('#reader-note').fill('Synthetic Inside orch reading note.');
  await page.getByRole('button', { name: 'Save note', exact: true }).click();
  await expect(page.locator('[data-study-status]')).toContainText('Saving is unavailable');
  const pending = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Export notes', exact: true }).click();
  const download = await pending;
  expect(fs.readFileSync(await download.path(), 'utf8')).toContain('Synthetic Inside orch reading note.');
});
