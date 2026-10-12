const { test, expect } = require('./fixtures');

test('mobile reading controls and chapter navigation work across browser engines', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/books/logbranik/05-logs-without-secrets.html');
  await page.getByRole('button', { name: 'Open bookmarks and notes' }).click();
  await page.locator('#reader-note').fill('A portable note.');
  await page.getByRole('button', { name: 'Save note', exact: true }).click();
  await page.locator('#reader-size').selectOption('large');
  await page.reload();
  await page.getByRole('button', { name: 'Open bookmarks and notes' }).click();
  await expect(page.locator('#reader-note')).toHaveValue('A portable note.');
  await expect(page.locator('#reader-size')).toHaveValue('large');
  await page.getByRole('button', { name: /contents/i }).click();
  await page.locator('[data-reader-scroll]').focus();
  await page.keyboard.press('PageDown');
  await expect(page.locator('body')).toHaveClass(/reader-scrolled/);
  await page.getByRole('button', { name: 'Show site navigation', exact: true }).click();
  await expect(page.locator('.site-header')).toBeVisible();
});

test('keyboard users can preview and cancel a backup file', async ({ page }) => {
  await page.goto('/reading/');
  await page.locator('[data-backup-file]').setInputFiles({ name: 'empty.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify({ format: 'codepop-reading', version: 1, books: {}, learning: {} })) });
  await expect(page.locator('#backup-preview-title')).toBeFocused();
  await page.getByRole('button', { name: 'Cancel', exact: true }).focus();
  await page.keyboard.press('Enter');
  await expect(page.locator('[data-backup-file]')).toBeFocused();
});

test('books, workshops, and paths remain readable without JavaScript', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  for (const url of ['/reading/', '/ai/workshops/', '/posts/ai-workshop-design-retry-tests/', '/learn/ai-workflows/']) {
    await page.goto(url);
    await expect(page.locator('main h1')).toBeVisible();
    await expect(page.locator('main a').first()).toBeVisible();
  }
  await context.close();
});
