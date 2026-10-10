const { test, expect } = require('./fixtures');
const AxeBuilder = require('@axe-core/playwright').default;

const routes = [
  '/posts/a-timeout-is-not-a-stopped-deployment/', '/posts/codex-slash-commands/',
  '/books/logbranik/', '/books/agentplane/18-approvals.html',
  '/projects/orch/', '/cv/', '/codepop/', '/videos/',
];

test('sharing uses canonical public URLs and encoded titles across content types', async ({ page }) => {
  const socialRequests = [];
  page.on('request', request => {
    if (/^https:\/\/(www\.)?(linkedin\.com|facebook\.com|twitter\.com|wa\.me|reddit\.com)\//.test(request.url())) socialRequests.push(request.url());
  });
  for (const route of routes) {
    await page.goto(route + '?ref=private#main-content');
    const group = page.locator('[data-share]');
    await expect(group).toHaveCount(1);
    const canonical = await page.locator('link[rel="canonical"]').getAttribute('href');
    const title = await group.getAttribute('data-share-title');
    expect(canonical).not.toMatch(/127\.0\.0\.1|localhost|private|#/);
    await expect(group).toHaveAttribute('data-share-url', canonical);
    const linkedin = new URL(await group.getByRole('link', { name: /^Share on LinkedIn/ }).getAttribute('href'));
    const facebook = new URL(await group.getByRole('link', { name: /^Share on Facebook/ }).getAttribute('href'));
    const x = new URL(await group.getByRole('link', { name: /^Share on X / }).getAttribute('href'));
    const whatsapp = new URL(await group.getByRole('link', { name: /^Share on WhatsApp/ }).getAttribute('href'));
    const email = new URL(await group.getByRole('link', { name: 'Share by email' }).getAttribute('href'));
    const reddit = new URL(await group.getByRole('link', { name: /^Share on Reddit/ }).getAttribute('href'));
    expect(linkedin.searchParams.get('url')).toBe(canonical);
    expect(facebook.searchParams.get('u')).toBe(canonical);
    expect(x.searchParams.get('url')).toBe(canonical);
    expect(x.searchParams.get('text')).toBe(title);
    expect(whatsapp.searchParams.get('text')).toBe(`${title} ${canonical}`);
    expect(email.searchParams.get('subject')).toBe(title);
    expect(email.searchParams.get('body')).toBe(`${title} ${canonical}`);
    expect(email.search).not.toContain('+');
    expect(reddit.searchParams.get('url')).toBe(canonical);
    expect(reddit.searchParams.get('title')).toBe(title);
    for (const link of await group.locator('a[target="_blank"]').all()) {
      await expect(link).toHaveAttribute('rel', 'noopener noreferrer');
    }
  }
  expect(socialRequests).toEqual([]);
});

test('social links work without JavaScript on posts, AI guides, books and chapters', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  for (const route of routes.slice(0, 4)) {
    await page.goto('http://127.0.0.1:4173' + route);
    const group = page.locator('[data-share]');
    await group.scrollIntoViewIfNeeded();
    await expect(group.getByRole('link')).toHaveCount(6);
    await expect(group.getByRole('link', { name: /^Share on Facebook/ })).toBeVisible();
    await expect(group.locator('[data-share-copy]')).toBeHidden();
    await expect(group.locator('[data-share-native]')).toBeHidden();
  }
  await context.close();
});

test('keyboard copying shares the public link and announces success', async ({ page }) => {
  await page.addInitScript(() => {
    Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText: async text => { window.copiedLink = text; } } });
    Object.defineProperty(navigator, 'share', { configurable: true, value: undefined });
  });
  await page.goto('/posts/codex-slash-commands/?private=true#main-content');
  const group = page.locator('[data-share]');
  const copy = group.locator('[data-share-copy]');
  await copy.focus();
  await page.keyboard.press('Enter');
  await expect(group.getByRole('status')).toHaveText('Link copied to clipboard.');
  expect(await page.evaluate(() => window.copiedLink)).toBe(await group.getAttribute('data-share-url'));
  await expect(copy).toContainText('Copied');
  await expect(copy).toBeFocused();
  await expect(copy.locator('svg')).toBeVisible();
  await expect(group.locator('[data-share-native]')).toBeHidden();
});

for (const unavailable of [true, false]) {
  test(`copying provides a selectable link when clipboard ${unavailable ? 'is missing' : 'permission is denied'}`, async ({ page }) => {
    await page.addInitScript(missing => {
      Object.defineProperty(navigator, 'clipboard', { configurable: true, value: missing ? undefined : { writeText: async () => { throw new DOMException('Denied', 'NotAllowedError'); } } });
    }, unavailable);
    await page.goto('/books/agentplane/18-approvals.html');
    const group = page.locator('[data-share]');
    await group.locator('[data-share-copy]').click();
    const input = group.getByRole('textbox', { name: 'Link to share' });
    await expect(input).toBeVisible();
    await expect(input).toBeFocused();
    await expect(input).toHaveValue(await group.getAttribute('data-share-url'));
    expect(await input.evaluate(node => node.selectionStart === 0 && node.selectionEnd === node.value.length)).toBe(true);
    await expect(group.getByRole('status')).toHaveText('Select and copy the link below.');
    await expect(group.locator('[data-share-copy]')).toBeEnabled();
    expect((await new AxeBuilder({ page }).include('[data-share]').analyze()).violations).toEqual([]);
  });
}

test('native sharing passes the canonical URL and handles cancellation and errors', async ({ page }) => {
  await page.addInitScript(() => {
    Object.defineProperty(navigator, 'share', { configurable: true, value: async data => {
      window.sharedData = data;
      if (window.shareError) throw new DOMException('Share failed', window.shareError);
    } });
  });
  await page.goto('/books/logbranik/?private=true');
  const group = page.locator('[data-share]');
  const native = group.getByRole('button', { name: 'More sharing options' });
  await native.click();
  expect(await page.evaluate(() => window.sharedData)).toEqual({ title: await group.getAttribute('data-share-title'), url: await group.getAttribute('data-share-url') });
  await page.evaluate(() => { window.shareError = 'AbortError'; });
  await native.click();
  await expect(group.locator('[data-share-status]')).toBeEmpty();
  await page.evaluate(() => { window.shareError = 'NotAllowedError'; });
  await native.click();
  await expect(group.getByRole('status')).toContainText('Choose a network');
  await expect(native).toBeEnabled();
});

for (const width of [320, 390, 1440]) {
  test(`share controls fit at ${width}px and stay out of print output`, async ({ page }) => {
    await page.addInitScript(() => {
      Object.defineProperty(navigator, 'share', { configurable: true, value: async () => {} });
    });
    await page.setViewportSize({ width, height: 1000 });
    for (const route of routes.slice(0, 4)) {
      await page.goto(route);
      const group = page.locator('[data-share]');
      await group.scrollIntoViewIfNeeded();
      const bounds = await group.boundingBox();
      expect(bounds.x).toBeGreaterThanOrEqual(0);
      expect(bounds.x + bounds.width).toBeLessThanOrEqual(width + 1);
      expect(await group.evaluate(node => node.scrollWidth <= node.clientWidth)).toBe(true);
      const button = group.locator('[data-share-copy]');
      expect((await button.boundingBox()).height).toBeGreaterThanOrEqual(32);
      const controls = await group.locator('.share-row').evaluate(node => [...node.children].filter(item => !item.hidden).map(item => {
        const bounds = item.getBoundingClientRect();
        return { top: bounds.top, width: bounds.width };
      }));
      expect(controls).toHaveLength(8);
      expect(new Set(controls.map(item => Math.round(item.top))).size).toBe(1);
      expect(controls.every(item => item.width >= 24)).toBe(true);
      await expect(button).toBeVisible();
      expect((await new AxeBuilder({ page }).include('[data-share]').analyze()).violations).toEqual([]);
      await page.emulateMedia({ media: 'print' });
      await expect(group).toBeHidden();
      await page.emulateMedia({ media: 'screen' });
    }
  });
}
