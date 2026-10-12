const { test, expect } = require('./fixtures');
const fs = require('node:fs');
const AxeBuilder = require('@axe-core/playwright').default;

for (const id of ['bugfix', 'review', 'tests', 'automation']) {
  test(`browser ${id} workshop runs canonical failing starter and passing solution`, async ({ page }) => {
    await page.goto(`/ai/workshops/?exercise=${id}#workshop-lab`);
    await expect(page.locator('#workshop-exercise')).toHaveValue(id);
    await expect(page.locator('#workshop-code')).toBeVisible();
    await page.getByRole('button', { name: 'Run tests', exact: false }).click();
    await expect(page.locator('[data-workshop-results] li')).toHaveCount(5);
    await expect(page.locator('[data-workshop-results] [data-passed="false"]')).not.toHaveCount(0);
    await page.locator('#workshop-code').fill(fs.readFileSync(`labs/ai-workshops/${id}/solution.mjs`, 'utf8'));
    await page.getByRole('button', { name: 'Run tests', exact: false }).click();
    await expect(page.locator('[data-workshop-result]')).toContainText('5 of 5 tests passed');
    await page.reload();
    await expect(page.locator('#workshop-code')).toHaveValue(fs.readFileSync(`labs/ai-workshops/${id}/solution.mjs`, 'utf8'));
    const download = page.waitForEvent('download'); await page.getByRole('button', { name: 'Download my app.mjs' }).click();
    expect(fs.readFileSync(await (await download).path(), 'utf8')).toContain('export function');
  });
}

test('runner blocks network and site storage; syntax errors and loops recover without blocking controls', async ({ page, context }) => {
  const attempts = [];
  await context.route('**/*runner-probe*', route => { attempts.push(route.request().url()); return route.abort(); });
  await page.goto('/ai/workshops/?exercise=bugfix#workshop-lab');
  const source = fs.readFileSync('labs/ai-workshops/bugfix/solution.mjs', 'utf8');
  await page.locator('#workshop-code').fill(`
    if (typeof document !== 'undefined' || typeof localStorage !== 'undefined') throw new Error('Page access leaked');
    for (const url of ['https://example.invalid/runner-probe', '${new URL('/runner-probe', 'http://127.0.0.1:4173')}']) {
      let denied = false; try { await fetch(url); } catch { denied = true; }
      if (!denied) throw new Error('Network access leaked');
    }
    ${source}`);
  await page.getByRole('button', { name: 'Run tests', exact: false }).click();
  await expect(page.locator('[data-workshop-result]')).toContainText('5 of 5 tests passed'); expect(attempts).toEqual([]);
  await page.locator('#workshop-code').fill('export function broken( {');
  await page.getByRole('button', { name: 'Run tests', exact: false }).click();
  await expect(page.locator('[data-workshop-result]')).toContainText('Could not run');
  await page.locator('#workshop-code').fill('while (true) {}');
  await page.getByRole('button', { name: 'Run tests', exact: false }).click();
  await expect(page.locator('[data-workshop-result]')).toContainText('Stopped after 4 seconds', { timeout: 7000 });
  await page.getByRole('button', { name: 'Run tests', exact: false }).click();
  await page.getByRole('button', { name: 'Stop', exact: true }).click();
  await expect(page.locator('[data-workshop-result]')).toContainText('Your code is still');
  await page.locator('#workshop-code').fill(source);
  await page.getByRole('button', { name: 'Run tests', exact: false }).click();
  await expect(page.locator('[data-workshop-result]')).toContainText('5 of 5 tests passed');
});

test('workshop drafts and quizzes still work when storage is blocked', async ({ page }) => {
  await page.addInitScript(() => { Storage.prototype.getItem = Storage.prototype.setItem = () => { throw new Error('Unavailable'); }; });
  await page.goto('/ai/workshops/#workshop-lab');
  await page.locator('#workshop-code').fill(fs.readFileSync('labs/ai-workshops/bugfix/solution.mjs', 'utf8'));
  await expect(page.locator('[data-workshop-draft]')).toContainText('unavailable');
  await page.getByRole('button', { name: 'Run tests', exact: false }).click();
  await expect(page.locator('[data-workshop-result]')).toContainText('5 of 5 tests passed');
  await page.goto('/learn/logs-and-security/');
  await page.locator('[data-question="fields"] input[value="2"]').check();
  await expect(page.locator('[data-knowledge-status]')).toContainText('1 of 10 answered');
  await expect(page.locator('[data-knowledge-status]')).toContainText('Storage unavailable');
});

test('missing workshop data and search enhancement keep useful reading fallbacks', async ({ page }) => {
  await page.route('**/browser-workshops.json', route => route.abort());
  await page.goto('/ai/workshops/#workshop-lab');
  await expect(page.locator('[data-workshop-loading]')).toContainText('could not load');
  await expect(page.locator('[data-workshop-controls]')).toBeHidden();
  await expect(page.getByRole('link', { name: 'Download all workshop files' })).toBeVisible();
  await page.route('**/library/search-utils.js', route => route.abort());
  await page.goto('/search/?q=proxy');
  await expect(page.locator('[data-search-directory]')).toBeVisible();
  await expect(page.locator('[data-search-directory] a').first()).toBeVisible();
});

test('quizzes explain wrong answers, restore choices, and validate backup answers', async ({ page }) => {
  await page.goto('/learn/ai-workflows/');
  await page.getByRole('button', { name: 'Check my answers' }).click();
  await expect(page.locator('[data-question="scope"] input').first()).toBeFocused();
  await page.locator('[data-question="scope"] input[value="0"]').check();
  await page.locator('[data-question="evidence"] input[value="1"]').check();
  await page.locator('[data-question="approval"] input[value="2"]').check();
  await page.getByRole('button', { name: 'Check my answers' }).click();
  await expect(page.locator('[data-knowledge-status]')).toContainText('2 correct');
  await expect(page.locator('[data-question="scope"] [data-question-result]')).toContainText('Try again');
  await page.locator('[data-question="scope"] input[value="1"]').check();
  await page.getByRole('button', { name: 'Check my answers' }).click();
  await expect(page.locator('[data-knowledge-status]')).toContainText('3 correct');
  await page.reload(); await expect(page.locator('[data-question="scope"] input[value="1"]')).toBeChecked();
  await page.goto('/reading/');
  const downloaded = page.waitForEvent('download'); await page.getByRole('button', { name: 'Download reading backup' }).click();
  const data = JSON.parse(fs.readFileSync(await (await downloaded).path(), 'utf8'));
  expect(data.knowledge['ai-workflows']).toEqual({ scope: 1, evidence: 1, approval: 2 });
  await page.evaluate(() => localStorage.clear());
  await page.locator('[data-backup-file]').setInputFiles({ name: 'quiz.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(data)) });
  await page.getByRole('button', { name: 'Restore this backup', exact: true }).click();
  expect(await page.evaluate(() => JSON.parse(localStorage.getItem('codepop:knowledge:ai-workflows')).approval)).toBe(2);
  data.knowledge['ai-workflows'].scope = 99;
  await page.locator('[data-backup-file]').setInputFiles({ name: 'bad.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(data)) });
  await expect(page.locator('[data-backup-status]')).toContainText('A quiz answer is invalid');
});

test('all AI filters combine, share URLs, restore history and clear empty results', async ({ page }) => {
  await page.goto('/ai/?tool=codex&category=Coding+agents&environment=web&format=Workshop&level=Beginner&q=priority');
  await expect(page.locator('#ai-posts .post-card:visible')).toHaveCount(1);
  await expect(page.locator('[data-ai-environment]')).toHaveValue('web');
  await expect(page.locator('[data-ai-level]')).toHaveValue('Beginner');
  await page.reload(); await expect(page.locator('#ai-posts .post-card:visible')).toHaveCount(1);
  await page.locator('[data-ai-environment]').selectOption('ide');
  await expect(page.locator('[data-ai-empty]')).toBeVisible();
  await expect(page).toHaveURL(/environment=ide/);
  await page.getByRole('button', { name: 'Explore all guides' }).click();
  await expect(page.locator('[data-ai-format]')).toHaveValue(''); await expect(page).toHaveURL('/ai/');
  await page.goto('/ai/?environment=ide&format=Command+reference');
  await expect(page.locator('#ai-posts .post-card:visible')).toHaveCount(1);
  await expect(page.locator('#ai-posts .post-card:visible')).toHaveAttribute('data-tool', 'copilot');
  await page.goto('/ai/?environment=unknown&format=unknown&level=unknown');
  await expect(page.locator('[data-ai-format]')).toHaveValue('');
});

test('chapter search highlights a safe excerpt and opens matching text in the reader', async ({ page }) => {
  await page.goto('/search/?q=proxy&type=chapters&book=logbranik');
  await expect(page.locator('#search-book')).toHaveValue('logbranik');
  await expect(page.locator('[data-search-results] mark').first()).toBeVisible();
  const links = await page.locator('[data-search-results] a').evaluateAll(nodes => nodes.map(node => node.getAttribute('href')));
  expect(links.length).toBeGreaterThan(0); expect(links.every(link => link.startsWith('/books/logbranik/') && link.includes('?find='))).toBe(true);
  await page.locator('[data-search-results] a').first().click();
  await expect(page.locator('.book-article mark[data-current]')).toBeVisible();
  await page.getByRole('button', { name: 'Find in this book', exact: true }).click();
  await expect(page.locator('#reader-find-query')).toHaveValue('proxy');
  await page.locator('#reader-find-query').fill('trust');
  await page.getByRole('button', { name: 'Find in section' }).click();
  await expect(page.locator('[data-reader-find-status]')).toContainText('matches');
  await page.getByRole('button', { name: 'Search this whole book' }).click();
  await expect(page.locator('[data-reader-book-results] li').first()).toBeVisible();
  await page.locator('#reader-find-query').fill('nomatchingword_987432'); await page.getByRole('button', { name: 'Find in section' }).click();
  await expect(page.locator('.book-article mark')).toHaveCount(0);
  await expect(page.locator('[data-reader-find-status]')).toContainText('No matches');
});

test('figure zoom preserves focus mode on Escape and glossary links to real chapters', async ({ page }) => {
  await page.goto('/books/logbranik/03-architecture-and-failure-modes.html');
  await page.getByRole('button', { name: 'Enter focus mode', exact: true }).click();
  const trigger = page.getByRole('button', { name: /^Expand figure:/ }).first();
  await trigger.focus(); await page.keyboard.press('Enter');
  await expect(page.getByRole('dialog')).toBeVisible();
  await page.getByRole('slider', { name: 'Figure size' }).fill('200');
  await expect(page.locator('.reader-figure-viewport img')).toHaveAttribute('style', 'width: 200%;');
  await page.keyboard.press('Escape');
  await expect(page.getByRole('dialog')).not.toBeVisible();
  await expect(trigger).toBeFocused();
  await expect(page.locator('body')).toHaveClass(/reader-focused/);
  for (const [id, chapter] of [['logbranik', '03-architecture-and-failure-modes'], ['modern-ci', '01-runs-not-scripts'], ['agentplane', '02-architecture'], ['secret-contract-operator', '05-api-i-semantika'], ['universal-tracking', '06-tenancy-rls']]) {
    await page.goto(`/books/${id}/${chapter}.html`);
    await expect(page.locator('.reader-glossary dt')).toHaveCount(3);
    expect(await page.locator('.reader-glossary a').evaluateAll(nodes => nodes.every(node => node.getAttribute('href').startsWith('/books/')))).toBe(true);
  }
});

test('new learning controls fit mobile, pass accessibility checks, and have readable no-JS fallbacks', async ({ page, browser }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  for (const url of ['/ai/workshops/#workshop-lab', '/ai/', '/learn/ai-workflows/', '/books/logbranik/03-architecture-and-failure-modes.html']) {
    await page.goto(url);
    if (url.includes('workshops')) await expect(page.locator('#workshop-code')).toBeVisible();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    expect((await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()).violations).toEqual([]);
  }
  const context = await browser.newContext({ javaScriptEnabled: false }); const fallback = await context.newPage();
  try {
    await fallback.goto('http://127.0.0.1:4173/learn/ai-workflows/');
    await expect(fallback.locator('[data-question]')).toHaveCount(10);
    await fallback.locator('.knowledge-explanation summary').first().click();
    await expect(fallback.locator('.knowledge-explanation p').first()).toBeVisible();
    await fallback.goto('http://127.0.0.1:4173/books/logbranik/05-logs-without-secrets.html');
    await fallback.locator('.reader-glossary summary').click(); await expect(fallback.locator('.reader-glossary dt').first()).toBeVisible();
    await fallback.goto('http://127.0.0.1:4173/ai/'); await expect(fallback.locator('.ai-comparison-table table')).toBeVisible();
  } finally { await context.close(); }
});
