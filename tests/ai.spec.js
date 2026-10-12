const { test, expect } = require('./fixtures');
const AxeBuilder = require('@axe-core/playwright').default;
const fs = require('node:fs');
const aiCount = fs.readdirSync('_posts').filter(name => name.endsWith('.md') && /\nsection: ai\n/.test(fs.readFileSync(`_posts/${name}`, 'utf8'))).length;
const codingAgentCount = fs.readdirSync('_posts').filter(name => name.endsWith('.md') && /\nsection: ai\n/.test(fs.readFileSync(`_posts/${name}`, 'utf8')) && /\ncategory: Coding agents\n/.test(fs.readFileSync(`_posts/${name}`, 'utf8'))).length;

test('AI Lab is featured and all tool references link to sourced standalone guides', async ({ page, request }) => {
  await page.goto('/');
  await expect(page.locator('#home-ai')).toContainText('Make AI part of');
  await page.locator('.nav-ai').click();
  await expect(page).toHaveURL('/ai/');
  await expect(page.locator('.nav-ai')).toHaveAttribute('aria-current', 'page');
  await expect(page.locator('#ai-posts [data-post-card]')).toHaveCount(aiCount);
  await expect(page.locator('.ai-tool-strip a')).toHaveCount(6);
  for (const link of await page.locator('.ai-tool-strip a').evaluateAll(links => links.map(link => link.getAttribute('href')))) {
    await page.goto(link);
    await expect(page.locator('[data-post-content] table')).not.toHaveCount(0);
    await expect(page.locator('.ai-source-list a')).not.toHaveCount(0);
    await expect(page.locator('.article-source, .article-chapter-callout')).toHaveCount(0);
    await expect(page.locator('head script[src*="gtag/js"]')).toHaveCount(1);
  }
  const index = await (await request.get('/search-index.json')).json();
  expect(index.some(item => item.url === '/ai/' && item.type === 'pages')).toBe(true);
  expect(index.some(item => item.url === '/posts/codex-slash-commands/' && item.text.includes('/diff'))).toBe(true);
  const feed = await (await request.get('/feed.xml')).text();
  expect(feed).toContain('/posts/codex-slash-commands/');
});

test('AI tool, category and full-text command search combine and restore from shared URLs', async ({ page }) => {
  await page.goto('/ai/?tool=codex&category=Coding+agents&q=%2Fdiff');
  await expect(page.locator('[data-ai-search]')).toHaveValue('/diff');
  await expect(page.locator('[data-ai-tool]')).toHaveValue('codex');
  await expect(page.getByRole('button', { name: 'Coding agents', exact: false })).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('#ai-posts [data-post-card]:visible')).toHaveCount(1);
  await expect(page.locator('#ai-posts [data-post-card]:visible')).toHaveAttribute('href', '/posts/codex-slash-commands/');
  await page.reload();
  await expect(page.locator('#ai-posts [data-post-card]:visible')).toHaveCount(1);
  await page.getByRole('button', { name: 'Chat assistants', exact: false }).click();
  await expect(page.locator('[data-ai-empty]')).toBeVisible();
  await expect(page).toHaveURL(/category=Chat\+assistants/);
  await page.getByRole('button', { name: 'Explore all guides', exact: true }).click();
  await expect(page.locator('#ai-posts [data-post-card]:visible')).toHaveCount(aiCount);
  await expect(page.locator('[data-ai-search]')).toBeFocused();
  await expect(page).toHaveURL('/ai/');
  await page.locator('[data-ai-search]').fill('checkpoint-dependent');
  await expect(page.locator('#ai-posts [data-post-card]:visible')).toHaveCount(1);
  await expect(page.locator('#ai-posts [data-post-card]:visible')).toHaveAttribute('data-tool', 'gemini');
  await page.goto('/search/?q=%2Fsandbox-add-read-dir&type=posts');
  await expect(page.locator('[data-search-results] a')).toHaveAttribute('href', '/posts/codex-slash-commands/');
});

test('AI filters handle unknown URL values, browser history and keyboard activation', async ({ page }) => {
  await page.goto('/ai/?tool=missing&category=missing');
  await expect(page.locator('#ai-posts [data-post-card]:visible')).toHaveCount(aiCount);
  await page.locator('[data-ai-search]').fill('/tests');
  await page.goto('/ai/?tool=cursor');
  await expect(page.locator('#ai-posts [data-post-card]:visible')).toHaveCount(1);
  await page.goBack();
  await expect(page.locator('[data-ai-search]')).toHaveValue('/tests');
  await page.locator('[data-ai-reset]').focus();
  await page.keyboard.press('Enter');
  await expect(page.locator('[data-ai-search]')).toBeFocused();
  const category = page.getByRole('button', { name: 'Coding agents', exact: false });
  await category.focus();
  await page.keyboard.press('Space');
  await expect(category).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('#ai-posts [data-post-card]:visible')).toHaveCount(codingAgentCount);
});

test('AI guides and navigation remain readable without JavaScript', async ({ browser, baseURL }) => {
  const context = await browser.newContext({ baseURL, javaScriptEnabled: false, viewport: { width: 390, height: 900 } });
  try {
    const page = await context.newPage();
    await page.goto('/ai/');
    await expect(page.locator('#ai-posts [data-post-card]:visible')).toHaveCount(aiCount);
    await expect(page.locator('[data-ai-search]')).toBeHidden();
    await expect(page.locator('.main-nav .nav-ai')).toBeVisible();
    await page.locator('#ai-posts a[href="/posts/codex-slash-commands/"]').click();
    await expect(page.locator('[data-post-content]')).toContainText('/sandbox-add-read-dir');
    await expect(page.locator('.ai-source-list')).toBeVisible();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
  } finally { await context.close(); }
});

test('AI article print output keeps the guide content', async ({ page }) => {
  await page.goto('/posts/codex-slash-commands/');
  await page.emulateMedia({ media: 'print' });
  await expect(page.locator('[data-post-content]')).toBeVisible();
  await expect(page.locator('.ai-article-sidebar')).toBeHidden();
  await expect(page.locator('.ai-related')).toBeHidden();
});

for (const path of ['/ai/', '/posts/chatgpt-slash-commands/', '/posts/codex-slash-commands/', '/posts/claude-code-slash-commands/', '/posts/gemini-cli-slash-commands/', '/posts/cursor-slash-commands/', '/posts/github-copilot-slash-commands/', '/posts/a-useful-ai-handoff/', '/posts/ai-changes-need-a-verification-loop/']) {
  test(`AI accessibility: ${path}`, async ({ page }) => {
    await page.goto(path);
    await page.evaluate(() => document.fonts.ready);
    const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa', 'best-practice']).analyze();
    expect(result.violations.map(item => ({ id: item.id, targets: item.nodes.map(node => node.target) }))).toEqual([]);
  });
}
