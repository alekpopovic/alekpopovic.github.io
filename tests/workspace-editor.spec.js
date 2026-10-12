const { test, expect } = require('./fixtures');
const fs = require('node:fs');
const AxeBuilder = require('@axe-core/playwright').default;
const chapter = '/books/logbranik/05-logs-without-secrets.html';
const solution = fs.readFileSync('labs/ai-workshops/bugfix/solution.mjs', 'utf8');
const inputFile = (name, content) => ({ name, mimeType: 'text/javascript', buffer: Buffer.from(content) });

test('workspace combines known progress and resumes the last chapter without changing practical steps', async ({ page }) => {
  await page.goto('/learn/workspace/');
  await page.evaluate(({ chapter, solution }) => {
    localStorage.setItem('codepop:library:logbranik', JSON.stringify({ [chapter]: { completed: true, bookmarked: true, note: 'Private note' }, '/unknown': { completed: true } }));
    localStorage.setItem('codepop:reading:logbranik', JSON.stringify({ url: chapter, updated: 1234, progress: .4 }));
    localStorage.setItem('codepop:learning:secret-contracts', JSON.stringify({ 0: true, 99: true }));
    localStorage.setItem('codepop:knowledge:secret-contracts', JSON.stringify({ 'status-oracle': 0, 'rbac-read': 99 }));
    localStorage.setItem('codepop:workshop:bugfix', solution);
    localStorage.setItem('codepop:workshop-check:bugfix', JSON.stringify({ source: solution, passed: 5, total: 5, checked_at: 100 }));
  }, { chapter, solution });
  await page.reload();
  await expect(page.locator('[data-workspace-book="logbranik"]')).toContainText('1 of 24 sections completed · 1 bookmarks · 1 notes');
  await expect(page.locator('[data-workspace-continue]')).toHaveAttribute('href', `${chapter}?resume=1`);
  await expect(page.locator('[data-workspace-path="secret-contracts"]')).toContainText('1 of 5 steps completed · 1 of 10 questions answered');
  await expect(page.locator('[data-workspace-path="secret-contracts"] [data-workspace-link]')).toHaveAttribute('href', '/learn/secret-contracts/#learning-step-1');
  await expect(page.locator('[data-workspace-workshop="bugfix"]')).toContainText('5 of 5 tests passed');
  await page.evaluate(() => localStorage.setItem('codepop:workshop:bugfix', 'changed'));
  await page.reload();
  await expect(page.locator('[data-workspace-workshop="bugfix"]')).toContainText('Code changed since the last test run');
  expect(await page.evaluate(() => JSON.parse(localStorage.getItem('codepop:learning:secret-contracts')))).toEqual({ 0: true, 99: true });
});

test('unreadable and blocked storage retain workspace links without destroying data', async ({ page }) => {
  await page.goto('/learn/workspace/');
  await page.evaluate(() => localStorage.setItem('codepop:library:logbranik', 'broken-json'));
  await page.reload(); await expect(page.locator('[data-workspace-status]')).toContainText('could not be read');
  expect(await page.evaluate(() => localStorage.getItem('codepop:library:logbranik'))).toBe('broken-json');
  await page.addInitScript(() => { Storage.prototype.getItem = () => { throw new Error('Blocked'); }; });
  await page.reload();
  await expect(page.locator('[data-workspace-status]')).toContainText('storage is unavailable');
  await expect(page.locator('[data-workspace-next]')).toBeHidden();
  await expect(page.locator('[data-workspace-path="secret-contracts"] h3 a')).toBeVisible();
});

test('editor highlights text safely, imports explicitly, runs by keyboard and compares a reference', async ({ page }) => {
  await page.goto('/ai/workshops/?exercise=bugfix#workshop-lab');
  await expect(page.locator('#workshop-code')).toBeVisible();
  await expect(page.locator('[data-editor-lines]')).toContainText('1\n2');
  await page.locator('[data-editor-import] summary').click();
  await page.locator('#workshop-import-file').setInputFiles(inputFile('app.mjs', solution));
  await expect(page.locator('[data-editor-import-apply]')).toBeEnabled();
  await expect(page.locator('#workshop-code')).not.toHaveValue(solution);
  await page.locator('[data-editor-import-apply]').click();
  await expect(page.locator('#workshop-code')).toHaveValue(solution);
  await page.locator('#workshop-code').press('Control+Enter');
  await expect(page.locator('[data-workshop-result]')).toContainText('5 of 5 tests passed');
  await page.locator('.workshop-diff summary').click();
  await page.locator('[data-editor-compare]').click();
  await expect(page.locator('[data-editor-diff-status]')).toContainText('0 removed lines · 0 added lines');
  const code = '// <img src=x onerror="window.editorExecuted=true">\n' + solution;
  await page.locator('#workshop-code').fill(code);
  await expect(page.locator('[data-editor-highlight]')).toContainText('<img src=x');
  await expect(page.locator('[data-editor-highlight] img')).toHaveCount(0);
  await page.locator('[data-editor-compare]').click();
  await expect(page.locator('[data-editor-diff-status]')).toContainText('1 removed lines');
  expect(await page.evaluate(() => window.editorExecuted)).toBeUndefined();
  await page.locator('#workshop-code').focus(); await page.keyboard.press('Tab');
  await expect(page.locator('#workshop-code')).not.toBeFocused();
  await page.goto('/learn/workspace/');
  await expect(page.locator('[data-workspace-workshop="bugfix"]')).toContainText('Code changed since the last test run');
});

test('editor rejects unsuitable imports, bounds diff work and drops imports on exercise changes', async ({ page }) => {
  await page.goto('/ai/workshops/#workshop-lab');
  await expect(page.locator('#workshop-code')).toBeVisible();
  const initial = await page.locator('#workshop-code').inputValue();
  await page.locator('[data-editor-import] summary').click();
  for (const [name, content] of [['app.txt', 'bad'], ['large.js', 'x'.repeat(40001)], ['binary.js', 'bad\0text']]) {
    await page.locator('#workshop-import-file').setInputFiles(inputFile(name, content));
    await expect(page.locator('[data-editor-import-apply]')).toBeDisabled();
    await expect(page.locator('#workshop-code')).toHaveValue(initial);
  }
  await page.locator('#workshop-import-file').setInputFiles(inputFile('good.mjs', solution));
  await expect(page.locator('[data-editor-import-apply]')).toBeEnabled();
  await page.locator('#workshop-exercise').selectOption('review');
  await expect(page.locator('[data-editor-import-apply]')).toBeDisabled();
  await page.locator('#workshop-code').fill('// line\n'.repeat(300));
  await page.locator('.workshop-diff summary').click(); await page.locator('[data-editor-compare]').click();
  await expect(page.locator('[data-editor-diff-status]')).toContainText('limited to the first 240 lines');
});

test('expanded quizzes cover every path and review only wrong or missing answers', async ({ page }) => {
  for (const path of ['ai-workflows', 'reliable-delivery', 'logs-and-security', 'secret-contracts', 'universal-tracking']) {
    await page.goto(`/learn/${path}/`);
    await expect(page.locator('[data-question]')).toHaveCount(10);
    await expect(page.locator('[data-question] .knowledge-explanation a')).toHaveCount(10);
  }
  const questions = page.locator('[data-question]');
  for (let i = 0; i < 10; i++) {
    const question = questions.nth(i), correct = Number(await question.getAttribute('data-answer'));
    await question.locator(`input[value="${i === 0 ? (correct + 1) % 3 : correct}"]`).check();
  }
  await page.getByRole('button', { name: 'Check my answers' }).click();
  await expect(page.locator('[data-knowledge-status]')).toContainText('9 correct');
  await page.getByRole('button', { name: 'Review mistakes' }).click();
  await expect(page.locator('[data-question]:visible')).toHaveCount(1);
  await expect(page.locator('[data-knowledge-status]')).toContainText('Showing 1 scenarios');
  const first = questions.first(), correct = await first.getAttribute('data-answer');
  await first.locator(`input[value="${correct}"]`).check();
  await expect(page.locator('[data-question]:visible')).toHaveCount(10);
  await page.getByRole('button', { name: 'Check my answers' }).click();
  await expect(page.locator('[data-knowledge-status]')).toContainText('10 correct');
  await expect(page.getByRole('button', { name: 'Review mistakes' })).toBeDisabled();
  await expect(page.locator('[data-learning-step]:checked')).toHaveCount(0);
});

test('workshop backups preserve raw source during merge, replacement and failed writes', async ({ page }) => {
  await page.goto('/reading/');
  const value = { format: 'codepop-reading', version: 1, books: {}, learning: {}, workshops: { bugfix: { draft: solution, check: { source: solution, passed: 5, total: 5, checked_at: 100 } } } };
  const choose = () => page.locator('[data-backup-file]').setInputFiles({ name: 'workshops.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(value)) });
  await page.evaluate(() => localStorage.setItem('codepop:workshop:bugfix', 'Local source'));
  await choose(); await page.getByRole('button', { name: 'Restore this backup', exact: true }).click();
  expect(await page.evaluate(() => localStorage.getItem('codepop:workshop:bugfix'))).toBe('Local source');
  await choose(); await page.getByRole('radio', { name: /^Replace entries/ }).check();
  await page.getByRole('button', { name: 'Restore this backup', exact: true }).click();
  expect(await page.evaluate(() => localStorage.getItem('codepop:workshop:bugfix'))).toBe(solution);
  const event = page.waitForEvent('download'); await page.getByRole('button', { name: 'Download reading backup' }).click();
  const data = JSON.parse(fs.readFileSync(await (await event).path(), 'utf8'));
  expect(data.workshops.bugfix).toEqual(value.workshops.bugfix);
  await page.evaluate(() => {
    localStorage.setItem('codepop:workshop:bugfix', 'Keep this draft');
    const original = Storage.prototype.setItem; let failed = false;
    Storage.prototype.setItem = function (key, value) { if (key === 'codepop:workshop-check:bugfix' && !failed) { failed = true; throw new Error('Quota'); } return original.call(this, key, value); };
  });
  await choose(); await page.getByRole('radio', { name: /^Replace entries/ }).check();
  await page.getByRole('button', { name: 'Restore this backup', exact: true }).click();
  await expect(page.locator('[data-backup-status]')).toContainText('Existing data was kept');
  expect(await page.evaluate(() => localStorage.getItem('codepop:workshop:bugfix'))).toBe('Keep this draft');
  value.workshops.bugfix.check.passed = 99;
  await choose(); await expect(page.locator('[data-backup-status]')).toContainText('test record is invalid');
});

test('new routes fit narrow and zoomed layouts, retain forced-color editing, and pass accessibility checks', async ({ page }) => {
  for (const url of ['/learn/workspace/', '/learn/secret-contracts/', '/learn/universal-tracking/', '/newsletter/', '/newsletter/2026-10/', '/ai/workshops/#workshop-lab']) {
    await page.setViewportSize({ width: 320, height: 800 }); await page.goto(url);
    if (url.includes('workshops')) await expect(page.locator('#workshop-code')).toBeVisible();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    expect((await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()).violations).toEqual([]);
    await page.setViewportSize({ width: 720, height: 500 });
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  }
  await page.emulateMedia({ forcedColors: 'active' });
  await expect(page.locator('#workshop-code')).toHaveCSS('color', 'rgb(0, 0, 0)');
  await page.locator('#workshop-code').fill(solution);
  await expect(page.locator('#workshop-code')).toHaveValue(solution);
});

test('workspace and newsletter archive stay useful without JavaScript or email service', async ({ browser, request }) => {
  const context = await browser.newContext({ javaScriptEnabled: false }), page = await context.newPage();
  try {
    await page.goto('http://127.0.0.1:4173/learn/workspace/');
    await expect(page.locator('[data-workspace-book]')).toHaveCount(5);
    await expect(page.locator('[data-workspace-path]')).toHaveCount(5);
    await expect(page.locator('[data-workspace-workshop]')).toHaveCount(4);
    await page.goto('http://127.0.0.1:4173/newsletter/');
    await expect(page.getByRole('link', { name: 'Read the issue →' })).toHaveAttribute('href', '/newsletter/2026-10/');
    await expect(page.getByRole('link', { name: 'Subscribe by email' })).toHaveCount(0);
    await page.getByRole('link', { name: 'Read the issue →' }).click();
    await expect(page.getByRole('heading', { name: 'Four small AI engineering workshops' })).toBeVisible();
    expect(await (await request.get('/newsletter.xml')).text()).toContain('/newsletter/2026-10/');
  } finally { await context.close(); }
});
