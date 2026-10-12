const { test, expect } = require('./fixtures');
const fs = require('node:fs');
const AxeBuilder = require('@axe-core/playwright').default;

test('starting routes combine topic, experience and time in shareable URLs', async ({ page }) => {
  await page.goto('/learn/start/?topic=secrets&experience=experienced&minutes=60');
  await expect(page.locator('#start-result-title')).toHaveText('Kubernetes secret contracts');
  await expect(page.locator('[data-start-steps] li')).toHaveCount(3);
  await expect(page.locator('[data-start-workshop] a')).toHaveAttribute('href', /exercise=gate/);
  await expect(page.locator('[data-start-context]')).toContainText('stale observations');
  await page.locator('[name="minutes"]').selectOption('20');
  await page.getByRole('button', { name: 'Find my starting point' }).focus(); await page.keyboard.press('Enter');
  await expect(page.locator('#start-result-title')).toBeFocused();
  await expect(page.locator('[data-start-steps] li')).toHaveCount(1);
  await expect(page).toHaveURL(/minutes=20/);
  await page.reload(); await expect(page.locator('[data-start-steps] li')).toHaveCount(1);
  for (const [topic, path] of [['ai', 'ai-workflows'], ['delivery', 'reliable-delivery'], ['security', 'logs-and-security'], ['tracking', 'universal-tracking']]) {
    await page.goto(`/learn/start/?topic=${topic}`);
    await expect(page.locator('[data-start-share]')).toHaveAttribute('href', new RegExp(`topic=${topic}`));
    await page.getByRole('button', { name: 'Use this route in My Learning' }).click();
    expect(await page.evaluate(() => JSON.parse(localStorage.getItem('codepop:study-plan')).path_id)).toBe(path);
  }
  await page.goto('/learn/start/?topic=unknown&minutes=100&experience=unknown');
  await expect(page.locator('[name="topic"]')).toHaveValue('ai');
  await expect(page.locator('[name="minutes"]')).toHaveValue('20');
});

test('session plan follows explicit unfinished steps and survives reload and backup', async ({ page }) => {
  await page.goto('/learn/start/?topic=ai');
  await page.evaluate(() => localStorage.setItem('codepop:learning:ai-workflows', JSON.stringify({ 0: true, 2: true })));
  await page.getByRole('button', { name: 'Use this route in My Learning' }).click();
  await page.goto('/learn/workspace/#study-plan');
  await page.locator('#study-goal').fill('Explain ownership <img src=x onerror=alert(1)>');
  await page.locator('[name="sessions"]').selectOption('2');
  await page.getByRole('button', { name: 'Save my plan', exact: true }).click();
  await expect(page.locator('[data-plan-sessions] a').first()).toHaveAttribute('href', '/learn/ai-workflows/#learning-step-1');
  await expect(page.locator('[data-plan-sessions] a').nth(1)).toHaveAttribute('href', '/learn/ai-workflows/#learning-step-3');
  await expect(page.locator('[data-plan-sessions]')).toContainText('1 further practical step remains');
  await expect(page.locator('[data-plan-goal] img')).toHaveCount(0);
  await page.reload(); await expect(page.locator('[data-plan-goal]')).toContainText('<img');
  await page.goto('/reading/');
  const downloading = page.waitForEvent('download'); await page.getByRole('button', { name: 'Download reading backup' }).click();
  const data = JSON.parse(fs.readFileSync(await (await downloading).path(), 'utf8'));
  expect(data.plan.sessions).toBe(2); expect(data.learning['ai-workflows']).toEqual({ 0: true, 2: true });
  await page.evaluate(() => localStorage.setItem('codepop:study-plan', JSON.stringify({ path_id: 'logs-and-security', session_minutes: 40, sessions: 3, goal: 'Keep my existing goal' })));
  const upload = () => page.locator('[data-backup-file]').setInputFiles({ name: 'plan.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(data)) });
  await upload(); await expect(page.locator('[data-backup-summary]')).toContainText('learning plan');
  await page.getByRole('button', { name: 'Restore this backup', exact: true }).click();
  expect(await page.evaluate(() => JSON.parse(localStorage.getItem('codepop:study-plan')).goal)).toBe('Keep my existing goal');
  await upload(); await page.locator('[value="replace"]').check(); await page.getByRole('button', { name: 'Restore this backup', exact: true }).click();
  expect(await page.evaluate(() => JSON.parse(localStorage.getItem('codepop:study-plan')).sessions)).toBe(2);
  data.plan.path_id = '../../unknown'; await upload(); await expect(page.locator('[data-backup-status]')).toContainText('learning plan is invalid');
  await page.goto('/learn/workspace/'); await page.getByRole('button', { name: 'Remove this plan', exact: true }).click();
  expect(await page.evaluate(() => localStorage.getItem('codepop:study-plan'))).toBeNull();
  expect(await page.evaluate(() => JSON.parse(localStorage.getItem('codepop:learning:ai-workflows')))).toEqual({ 0: true, 2: true });
});

test('review queue links wrong valid answers and correcting them never completes a practical step', async ({ page }) => {
  await page.goto('/learn/workspace/');
  await page.evaluate(() => localStorage.setItem('codepop:knowledge:ai-workflows', JSON.stringify({ scope: 0, evidence: 1, approval: 99, unknown: 1 })));
  await page.reload(); await expect(page.locator('[data-review-list] li')).toHaveCount(1);
  await page.locator('[data-review-list] li a').first().click();
  await expect(page).toHaveURL(/review=mistakes#question-ai-workflows-scope/);
  await expect(page.locator('[data-knowledge-review]')).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('[data-question="evidence"]')).toBeHidden();
  await page.locator('[data-question="scope"] input[value="1"]').check();
  await page.goto('/learn/workspace/'); await expect(page.locator('[data-review-list] li')).toHaveCount(0);
  expect(await page.evaluate(() => localStorage.getItem('codepop:learning:ai-workflows'))).toBeNull();
});

test('corrupt and blocked storage keep recommendations and visit-only plans usable', async ({ page }) => {
  await page.goto('/learn/workspace/'); await page.evaluate(() => { localStorage.setItem('codepop:study-plan', '{broken'); localStorage.setItem('codepop:knowledge:ai-workflows', '{broken'); });
  await page.reload(); await expect(page.locator('[data-plan-status]')).toContainText('unreadable');
  await expect(page.locator('[data-review-status]')).toContainText('could not be read');
  expect(await page.evaluate(() => localStorage.getItem('codepop:study-plan'))).toBe('{broken');
  await page.addInitScript(() => { Storage.prototype.getItem = Storage.prototype.setItem = () => { throw new Error('Blocked'); }; });
  await page.goto('/learn/start/'); await page.getByRole('button', { name: 'Use this route in My Learning' }).click();
  await expect(page.locator('[data-start-status]')).toContainText('Storage is unavailable');
  await page.goto('/learn/workspace/'); await page.locator('#study-goal').fill('A goal for this visit');
  await page.getByRole('button', { name: 'Save my plan', exact: true }).click();
  await expect(page.locator('[data-plan-preview]')).toBeVisible(); await expect(page.locator('[data-plan-status]')).toContainText('Storage is unavailable');
});

for (const id of ['gate', 'replay']) {
  test(`${id} staged workshop shares eight canonical checks and invalidates stale results`, async ({ page }) => {
    await page.goto(`/ai/workshops/?exercise=${id}#workshop-lab`);
    await expect(page.locator('[data-workshop-stages] > li')).toHaveCount(3);
    await page.getByRole('button', { name: 'Run tests', exact: false }).click();
    await expect(page.locator('[data-workshop-results] li')).toHaveCount(8);
    await expect(page.locator('[data-workshop-results] [data-passed="false"]')).not.toHaveCount(0);
    await page.locator('#workshop-code').fill(fs.readFileSync(`labs/ai-workshops/${id}/solution.mjs`, 'utf8'));
    await page.getByRole('button', { name: 'Run tests', exact: false }).click();
    await expect(page.locator('[data-workshop-result]')).toContainText('8 of 8 tests passed');
    for (const text of await page.locator('[data-stage-progress]').allTextContents()) expect(text).toMatch(/(\d+) of \1 stage checks passed/);
    await page.locator('#workshop-code').fill('export function broken() {}');
    await expect(page.locator('[data-stage-progress]').first()).toContainText('Code changed');
    await page.locator('[data-workshop-stages] summary').first().focus(); await page.keyboard.press('Enter');
    await expect(page.locator('[data-workshop-stages] details').first()).toHaveAttribute('open', '');
    await page.locator('#workshop-exercise').selectOption('bugfix');
    await expect(page.locator('[data-workshop-stages] details[open]')).toHaveCount(0);
  });
}

test('video companions offer bounded timestamp links without loading a player automatically', async ({ page, context, request }) => {
  const index = await (await request.get('/search-index.json')).json();
  const videos = index.filter(item => item.type === 'videos'); expect(videos).toHaveLength(15);
  expect(videos.every(item => /^\/videos\/[\w-]+\/$/.test(item.url))).toBe(true);
  await context.route('https://www.youtube-nocookie.com/**', route => route.fulfill({ contentType: 'text/html', body: '<html lang="en"><title>Player fixture</title></html>' }));
  await page.goto('/videos/cloudivision-delivery/?t=61');
  await expect(page.locator('.lesson-player iframe')).not.toHaveAttribute('src', /./);
  await expect(page.locator('#video-time')).toHaveValue('1:01');
  await page.locator('#video-time').fill('2:05'); await page.getByRole('button', { name: 'Create timestamp link' }).click();
  await expect(page).toHaveURL(/\?t=125$/);
  await expect(page.locator('[data-video-time-link]')).toHaveAttribute('href', /t=125$/);
  await expect(page.locator('.lesson-player iframe')).not.toHaveAttribute('src', /./);
  await page.locator('#video-time').fill('99:00'); await page.getByRole('button', { name: 'Create timestamp link' }).click();
  await expect(page.locator('[data-video-time-status]')).toContainText('before 6:26');
  await page.locator('[data-lesson-play]').click(); await expect(page.locator('.lesson-player iframe')).toHaveAttribute('src', /start=125/);
  await page.goto('/books/modern-ci/01-runs-not-scripts.html');
  await expect(page.locator('.related-video-lessons')).toContainText('Cloudivision CI CD');
});

test('native project capture plays and explains the backend verification boundary', async ({ page }) => {
  await page.goto('/projects/container-desk/'); const proof = page.locator('.project-native-proof');
  await expect(proof).toContainText('does not show a connected desktop UI');
  const video = proof.locator('video'); await video.scrollIntoViewIfNeeded(); await video.evaluate(async element => { element.muted = true; await element.play(); });
  await expect.poll(() => video.evaluate(element => element.currentTime)).toBeGreaterThan(0); await video.evaluate(element => element.pause());
  await proof.locator('summary').click(); await expect(proof.locator('pre')).toContainText('PASS real Engine direct-known');
});

test('new learning and video pages reflow, pass automated checks, and preserve no-JS navigation', async ({ page, browser }) => {
  await page.setViewportSize({ width: 320, height: 780 });
  for (const url of ['/learn/start/', '/learn/workspace/', '/videos/cloudivision-delivery/', '/ai/workshops/?exercise=gate#workshop-lab', '/projects/container-desk/']) {
    await page.goto(url); if (url.includes('workshops')) await expect(page.locator('#workshop-code')).toBeVisible();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    expect((await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze()).violations).toEqual([]);
  }
  const context = await browser.newContext({ javaScriptEnabled: false }), fallback = await context.newPage();
  try {
    await fallback.goto('http://127.0.0.1:4173/learn/start/'); await expect(fallback.locator('.learning-grid .learning-card')).toHaveCount(5);
    await fallback.goto('http://127.0.0.1:4173/videos/cloudivision-delivery/'); await expect(fallback.locator('[data-lesson-play]')).toHaveAttribute('href', 'https://www.youtube.com/watch?v=B48cbgaer7w');
    await expect(fallback.getByRole('heading', { name: 'A practical follow-up' })).toBeVisible();
    await fallback.goto('http://127.0.0.1:4173/ai/workshops/'); await expect(fallback.locator('.workshop-route-directory > details')).toHaveCount(6);
    await fallback.locator('.workshop-route-directory > details').last().locator('summary').first().click();
    await expect(fallback.getByRole('heading', { name: 'Keep failure atomic', exact: true })).toBeVisible();
  } finally { await context.close(); }
});
