const { test, expect } = require('./fixtures');
const AxeBuilder = require('@axe-core/playwright').default;
const fs = require('node:fs');

test('learning paths save a checklist and preserve meaningful exercises', async ({ page }) => {
  await page.goto('/learn/');
  await expect(page.locator('.learning-card')).toHaveCount(5);
  await page.getByRole('link', { name: 'AI for developers', exact: true }).click();
  await expect(page.locator('.learning-step')).toHaveCount(5);
  await expect(page.locator('[data-learning-status]')).toContainText('0 of 5');
  await page.locator('[data-learning-step="1"]').check();
  await page.reload();
  await expect(page.locator('[data-learning-step="1"]')).toBeChecked();
  await expect(page.locator('[data-learning-status]')).toContainText('1 of 5');
  await expect(page.locator('.learning-exercise').first()).toContainText('Keep as evidence');
});

test('the mobile notes control has a visible icon and opens the workspace by keyboard', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/books/logbranik/05-logs-without-secrets.html');
  const button = page.getByRole('button', { name: 'Open bookmarks and notes' });
  await expect(button.locator('svg')).toBeVisible();
  await button.focus(); await page.keyboard.press('Enter');
  await expect(page.locator('#reader-note')).toBeFocused();
  await expect(page.locator('[data-reader-study]')).toHaveAttribute('open', '');
});

test('learning and notes remain usable when browser storage fails', async ({ page }) => {
  await page.addInitScript(() => {
    Storage.prototype.getItem = () => { throw new Error('Storage unavailable'); };
    Storage.prototype.setItem = () => { throw new Error('Storage unavailable'); };
  });
  await page.goto('/learn/logs-and-security/');
  await page.locator('[data-learning-step="0"]').check();
  await expect(page.locator('[data-learning-status]')).toContainText('1 of 4');
  await expect(page.locator('[data-learning-status]')).toContainText('unavailable');
  await page.goto('/books/logbranik/05-logs-without-secrets.html');
  await page.getByRole('button', { name: 'Open bookmarks and notes' }).click();
  await page.locator('#reader-note').fill('Export this temporary note.');
  await page.getByRole('button', { name: 'Save note', exact: true }).click();
  await expect(page.locator('[data-study-status]')).toContainText('Saving is unavailable');
  const downloaded = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Export notes', exact: true }).click();
  const download = await downloaded;
  expect(fs.readFileSync(await download.path(), 'utf8')).toContain('Export this temporary note.');
});

test('reader bookmarks, completion, and notes survive chapter changes without rendering note HTML', async ({ page }) => {
  const chapter = '/books/logbranik/05-logs-without-secrets.html';
  const note = '<img src=x onerror="window.noteExecuted=true"> A synthetic question.';
  await page.goto(chapter);
  await page.getByRole('button', { name: 'Open bookmarks and notes' }).click();
  await page.getByRole('button', { name: 'Bookmark this place', exact: true }).click();
  await page.locator('[data-reader-complete]').check();
  await page.locator('#reader-note').fill(note);
  await page.getByRole('button', { name: 'Save note', exact: true }).click();
  await page.goto('/books/logbranik/09-client-ip-and-proxy-trust.html');
  await page.getByRole('button', { name: 'Open bookmarks and notes' }).click();
  await expect(page.locator('#reader-note')).toHaveValue('');
  await expect(page.locator('[data-study-progress]')).toHaveText('1 of 24 sections completed.');
  await page.locator('[data-reader-bookmarks] a').click();
  await page.getByRole('button', { name: 'Open bookmarks and notes' }).click();
  await expect(page.locator('#reader-note')).toHaveValue(note);
  await expect(page.locator('[data-reader-complete]')).toBeChecked();
  await expect(page.locator('[data-reader-bookmark]')).toHaveAttribute('aria-pressed', 'true');
  expect(await page.evaluate(() => window.noteExecuted)).toBeUndefined();
  const downloaded = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Export notes', exact: true }).click();
  const download = await downloaded;
  expect(download.suggestedFilename()).toBe('logbranik-notes.md');
  expect(fs.readFileSync(await download.path(), 'utf8')).toContain(note);
});

test('offline reading is opt-in, keeps the reader working, and preserves online 404s', async ({ page, context }) => {
  await page.goto('/books/universal-tracking/16-realtime.html');
  expect(await page.evaluate(() => navigator.serviceWorker.getRegistrations().then(value => value.length))).toBe(0);
  await page.getByRole('button', { name: 'Open bookmarks and notes' }).click();
  await page.getByRole('button', { name: 'Save this section offline' }).click();
  await expect(page.locator('[data-offline-status]')).toContainText('available offline', { timeout: 25000 });
  const cached = await page.evaluate(async () => (await (await caches.open('codepop-reader-chapters-v1')).keys()).map(request => new URL(request.url).pathname));
  expect(cached).toEqual(['/books/universal-tracking/16-realtime.html']);
  await context.setOffline(true);
  await page.reload();
  await expect(page.locator('.book-article h1')).toBeVisible();
  await expect(page.locator('[data-reader-toolbar]')).toBeVisible();
  await page.goto('/offline/');
  await expect(page.locator('[data-offline-directory] li')).toHaveCount(1);
  await page.getByRole('button', { name: /^Remove offline copy:/ }).click();
  await expect(page.locator('[data-offline-status]')).toContainText('No offline sections');
  await context.setOffline(false);
  const response = await page.goto('/there-is-no-offline-replacement-93848.html');
  expect(response.status()).toBe(404);
});

test('project architecture walkthroughs are labeled and work by keyboard', async ({ page }) => {
  await page.goto('/projects/orch/');
  await expect(page.locator('[data-project-walkthrough]')).toContainText('Conceptual walkthrough');
  await page.locator('[data-project-step="4"]').focus();
  await page.keyboard.press('Enter');
  await expect(page.locator('[data-project-output]')).toContainText('Docker executes');
  await expect(page.locator('[data-project-step="4"]')).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('a[href*="/blob/"]').first()).toHaveAttribute('href', /\/blob\/[a-f0-9]{40}\/README\.md$/);
});

test('learning paths, project explanations, feeds and correction links work without JavaScript', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  try {
    await page.goto('http://127.0.0.1:4173/learn/ai-workflows/');
    await expect(page.locator('.learning-step')).toHaveCount(5);
    await expect(page.locator('.learning-exercise').first()).toContainText('Keep as evidence:');
    await expect(page.locator('[data-learning-step]').first()).toBeHidden();
    await page.goto('http://127.0.0.1:4173/projects/orch/');
    await expect(page.locator('[data-project-explanations] li')).toHaveCount(5);
    await expect(page.locator('[data-project-explanations]')).toBeVisible();
    await expect(page.locator('[data-project-steps]')).toBeHidden();
    await page.goto('http://127.0.0.1:4173/subscribe/');
    await expect(page.locator('main a[href="/feed.xml"]')).toBeVisible();
    await expect(page.locator('main a[href="/updates.xml"]')).toBeVisible();
    await page.goto('http://127.0.0.1:4173/books/logbranik/05-logs-without-secrets.html');
    await expect(page.locator('.book-article')).toBeVisible();
    await expect(page.getByRole('link', { name: 'Report a correction' })).toHaveAttribute('href', /issues\/new\?title=/);
  } finally { await context.close(); }
});

for (const path of ['/learn/', '/learn/ai-workflows/', '/subscribe/', '/updates/', '/offline/', '/projects/container-desk/']) {
  test(`new reading routes are accessible and fit a mobile screen: ${path}`, async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(path);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
    const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
    expect(results.violations).toEqual([]);
  });
}
