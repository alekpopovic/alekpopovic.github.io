const { test, expect } = require('./fixtures');

test('motion effects respond to preference changes without interrupting keyboard navigation', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'no-preference' });
  await page.goto('/');
  const scene = page.locator('[data-scene]');
  const illustration = scene.locator('.playground');
  const initial = await illustration.evaluate(element => getComputedStyle(element).transform);
  await scene.hover({ position: { x: 90, y: 120 } });
  await expect.poll(() => illustration.evaluate(element => getComputedStyle(element).transform)).not.toBe(initial);

  const note = page.getByRole('link', { name: /Think & try/ });
  await note.hover();
  await expect.poll(() => note.evaluate(element => getComputedStyle(element, '::after').opacity)).toBe('1');
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await expect.poll(() => note.evaluate(element => getComputedStyle(element, '::after').opacity)).toBe('0');
  await expect.poll(() => page.evaluate(() => document.getAnimations().filter(animation => animation.playState === 'running').length)).toBe(0);
  await expect(illustration).toHaveCSS('transform', 'none');
  await note.focus();
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL('/posts/');
  await expect(page.locator('h1')).toBeVisible();
});

for (const fallback of ['missing effects script', 'missing observer API']) {
  test(`${fallback}: learning links, content and combined filters remain usable`, async ({ page }) => {
    if (fallback === 'missing effects script') await page.route('**/effects.js', route => route.abort());
    else await page.addInitScript(() => { delete window.IntersectionObserver; });
    await page.emulateMedia({ reducedMotion: 'no-preference' });
    await page.goto('/');
    await expect(page.locator('.discovery-card')).toHaveCount(3);
    await page.getByRole('link', { name: /Think & try/ }).click();
    await page.locator('[data-book-filter="modern-ci"]').click();
    await page.locator('#post-category').selectOption('Delivery');
    await page.locator('#post-search').fill('cache');
    const result = page.locator('#posts-grid .post-card:visible');
    await expect(result).toHaveCount(1);
    await expect(result).toContainText('A fast cache is not a release artifact');
    await result.focus();
    await page.keyboard.press('Enter');
    await expect(page.locator('[data-post-content]')).toBeVisible();
  });
}

test('mobile learning paths work without JavaScript and lead to complete book editions', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 844 } });
  const page = await context.newPage();
  await page.goto('http://127.0.0.1:4173/');
  await page.getByRole('link', { name: /Read & explore/ }).click();
  await expect(page).toHaveURL(/\/books\/$/);
  await expect(page.locator('.book-feature').first()).toBeVisible();
  await expect(page.locator('a[download][href$=".pdf"]').first()).toBeVisible();
  await expect(page.locator('a[download][href$=".epub"]').first()).toBeVisible();
  await context.close();
});
