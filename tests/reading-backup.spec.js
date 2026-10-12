const { test, expect } = require('./fixtures');
const fs = require('node:fs');
const AxeBuilder = require('@axe-core/playwright').default;
const chapter = '/books/logbranik/05-logs-without-secrets.html';
const libraryKey = 'codepop:library:logbranik';
const entry = note => ({ note, bookmarked: true, completed: true, anchor: '' });
const backup = note => ({ format: 'codepop-reading', version: 1, books: { logbranik: { records: { [chapter]: entry(note) }, resume: { url: chapter, progress: .4, updated: 1234 } } }, learning: { 'ai-workflows': { 0: true, 1: false } }, preferences: { size: 'large', theme: 'dark' } });
const choose = async (page, value) => page.locator('[data-backup-file]').setInputFiles({ name: 'reading.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(value)) });

test('reading backup restores notes, bookmarks, progress, preferences and learning on a fresh device', async ({ page }) => {
  const note = '<img src=x onerror="window.backupExecuted=true"> My own explanation.';
  await page.goto('/reading/');
  await choose(page, backup(note));
  await expect(page.locator('[data-backup-preview]')).toBeVisible();
  expect(await page.evaluate(key => localStorage.getItem(key), libraryKey)).toBeNull();
  await page.getByRole('button', { name: 'Restore this backup', exact: true }).click();
  await expect(page.locator('[data-backup-status]')).toContainText('Backup restored');
  const exported = page.waitForEvent('download');
  await page.getByRole('button', { name: 'Download reading backup' }).click();
  const file = await exported;
  const data = JSON.parse(fs.readFileSync(await file.path(), 'utf8'));
  expect(data.books.logbranik.records[chapter].note).toBe(note);
  expect(data.books.logbranik.resume.progress).toBe(.4);
  await page.goto(chapter);
  await page.getByRole('button', { name: 'Open bookmarks and notes' }).click();
  await expect(page.locator('#reader-note')).toHaveValue(note);
  await expect(page.locator('[data-reader-complete]')).toBeChecked();
  await expect(page.locator('#reader-theme')).toHaveValue('dark');
  await expect(page.locator('#reader-size')).toHaveValue('large');
  expect(await page.evaluate(() => window.backupExecuted)).toBeUndefined();
  await page.goto('/learn/ai-workflows/');
  await expect(page.locator('[data-learning-step="0"]')).toBeChecked();
});

test('merge preserves local notes and unchecked checklist choices; replacement is explicit', async ({ page }) => {
  await page.goto('/reading/');
  await page.evaluate(({ key, chapter }) => {
    localStorage.setItem(key, JSON.stringify({ [chapter]: { note: 'Local note', bookmarked: false, completed: false, anchor: '' } }));
    localStorage.setItem('codepop:learning:ai-workflows', JSON.stringify({ 0: false }));
    localStorage.setItem('codepop:library:modern-ci', JSON.stringify({ untouched: true }));
  }, { key: libraryKey, chapter });
  await choose(page, backup('Imported note'));
  await page.getByRole('button', { name: 'Restore this backup', exact: true }).click();
  expect(await page.evaluate(({ key, chapter }) => JSON.parse(localStorage.getItem(key))[chapter].note, { key: libraryKey, chapter })).toBe('Local note');
  expect(await page.evaluate(() => JSON.parse(localStorage.getItem('codepop:learning:ai-workflows'))['0'])).toBe(false);
  await choose(page, backup('Imported note'));
  await page.getByRole('radio', { name: /^Replace entries/ }).check();
  await page.getByRole('button', { name: 'Restore this backup', exact: true }).click();
  expect(await page.evaluate(({ key, chapter }) => JSON.parse(localStorage.getItem(key))[chapter].note, { key: libraryKey, chapter })).toBe('Imported note');
  expect(await page.evaluate(() => localStorage.getItem('codepop:library:modern-ci'))).toBe('{"untouched":true}');
});

for (const [name, mutate] of [
  ['foreign URL', data => { data.books.logbranik.resume.url = 'https://untrusted.example/'; }],
  ['unknown section', data => { data.books.logbranik.records['/books/logbranik/missing.html'] = entry('bad'); }],
  ['oversized note', data => { data.books.logbranik.records[chapter].note = 'x'.repeat(10001); }],
  ['unsupported version', data => { data.version = 99; }],
  ['unknown path', data => { data.learning.foreign = { 0: true }; }],
]) {
  test(`invalid backup is rejected without saving: ${name}`, async ({ page }) => {
    await page.goto('/reading/');
    const data = backup('Never saved'); mutate(data); await choose(page, data);
    await expect(page.locator('[data-backup-status]')).toContainText('Nothing has been saved');
    await expect(page.locator('[data-backup-preview]')).toBeHidden();
    expect(await page.evaluate(key => localStorage.getItem(key), libraryKey)).toBeNull();
  });
}

test('a failed restore rolls back prior writes instead of losing existing notes', async ({ page }) => {
  await page.goto('/reading/');
  await page.evaluate(({ key, chapter }) => {
    localStorage.setItem(key, JSON.stringify({ [chapter]: { note: 'Keep me', bookmarked: false, completed: false, anchor: '' } }));
    const original = Storage.prototype.setItem; let failed = false;
    Storage.prototype.setItem = function (key, value) {
      if (key === 'codepop:learning:ai-workflows' && !failed) { failed = true; throw new DOMException('Full', 'QuotaExceededError'); }
      return original.call(this, key, value);
    };
  }, { key: libraryKey, chapter });
  await choose(page, backup('Replacement'));
  await page.getByRole('radio', { name: /^Replace entries/ }).check();
  await page.getByRole('button', { name: 'Restore this backup', exact: true }).click();
  await expect(page.locator('[data-backup-status]')).toContainText('Existing data was kept');
  expect(await page.evaluate(({ key, chapter }) => JSON.parse(localStorage.getItem(key))[chapter].note, { key: libraryKey, chapter })).toBe('Keep me');
  expect(await page.evaluate(() => localStorage.getItem('codepop:reading:logbranik'))).toBeNull();
});

test('blocked storage and cancelled imports retain usable navigation', async ({ page }) => {
  await page.addInitScript(() => { Storage.prototype.getItem = () => { throw new DOMException('Unavailable', 'SecurityError'); }; });
  await page.goto('/reading/');
  await expect(page.locator('[data-backup-status]')).toContainText('storage is unavailable');
  await choose(page, backup('A note'));
  await page.getByRole('button', { name: 'Cancel', exact: true }).click();
  await expect(page.locator('[data-backup-preview]')).toBeHidden();
  await page.getByRole('button', { name: 'Download reading backup' }).click();
  await expect(page.locator('[data-backup-status]')).toContainText('Could not export');
  await expect(page.getByRole('link', { name: 'Browse the books →', exact: true })).toBeVisible();
});

test('backup and workshop pages fit mobile screens and pass accessibility checks', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  for (const url of ['/reading/', '/ai/workshops/']) {
    await page.goto(url);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    expect((await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()).violations).toEqual([]);
  }
});

test('new workshops appear in the AI library, filters and search', async ({ page }) => {
  await page.goto('/ai/?category=Testing&tool=codex');
  await expect(page.locator('.post-card:visible')).toHaveCount(1);
  await expect(page.locator('.post-card:visible')).toContainText('retry tests');
  await page.goto('/search/?q=reproducible%20release');
  await expect(page.locator('[data-search-results]')).toContainText('AI workshop');
});
