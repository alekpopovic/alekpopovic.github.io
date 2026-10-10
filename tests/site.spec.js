const { test, expect } = require('./fixtures');
const AxeBuilder = require('@axe-core/playwright').default;
const fs = require('node:fs');
const postCount = fs.readdirSync('_posts').filter(name => name.endsWith('.md')).length;
const catalog = JSON.parse(fs.readFileSync('_data/books.json', 'utf8'));
const projectCount = JSON.parse(fs.readFileSync('_data/projects.json', 'utf8')).length;
const directoryCount = catalog.reduce((count, book) => count + book.chapters.length + 1, 0) + postCount + projectCount + 2;

const sampleChapters = {
  agentplane: '18-approvals',
  'secret-contract-operator': '13-rotacija-i-rollout',
  'universal-tracking': '16-realtime',
};

for (const [id, chapterSlug] of Object.entries(sampleChapters)) {
  test(`${id}: full contents, editions, chapter notes, filters and saved place`, async ({ page, request }) => {
    const book = catalog.find(item => item.id === id);
    const chapter = book.chapters.find(item => item.slug === chapterSlug);
    await page.goto(book.url);
    await expect(page.locator('.book-contents-list li')).toHaveCount(book.chapters.length);
    const cover = page.locator('.overview-cover img');
    await expect.poll(() => cover.evaluate(image => image.complete && image.naturalWidth > 0)).toBe(true);
    await expect(cover).toHaveAttribute('width', String(book.cover_width));
    await expect(cover).toHaveAttribute('height', String(book.cover_height));
    for (const format of ['pdf', 'epub']) {
      await expect(page.locator(`a[download][href="${book[format]}"]`)).toBeVisible();
      const response = await request.get(book[format]);
      expect(response.status()).toBe(200);
      expect((await response.body()).length).toBeGreaterThan(50000);
    }
    await page.goto(chapter.url);
    await expect(page.locator('.book-article')).toHaveAttribute('lang', book.language);
    await expect(page.locator('.book-article img')).toBeVisible();
    await expect(page.locator('.book-related-notes a')).toHaveCount(1);
    await page.locator('.book-related-notes a').click();
    await expect(page.locator(`.post-article a[href="${chapter.url}"]`).first()).toBeVisible();
    await page.goto(book.url);
    await expect(page.locator(`[data-resume-book="${id}"]`)).toHaveAttribute('href', `${chapter.url}?resume=1`);
    await page.goto(`/posts/?book=${id}`);
    await expect(page.locator('#posts-grid .post-card:visible')).toHaveCount(3);
    await page.reload();
    await expect(page.locator('#posts-grid .post-card:visible')).toHaveCount(3);
  });
}

test('tracking notes combine shareable filters and chapters appear in full-text search', async ({ page }) => {
  await page.goto('/posts/?book=universal-tracking&category=Security&q=precision');
  await expect(page.locator('#posts-grid .post-card:visible')).toHaveCount(1);
  await expect(page.locator('#posts-grid .post-card:visible')).toContainText('An approximate marker needs an approximate payload');
  await page.reload();
  await expect(page.locator('#posts-grid .post-card:visible')).toHaveCount(1);
  await page.locator('#post-search').fill('no-such-tracking-topic-8746');
  await expect(page.locator('[data-post-empty]')).toBeVisible();
  await page.goto('/search/?q=sequence%20epochs&type=chapters');
  await expect(page.locator('[data-search-results] a[href="/books/universal-tracking/12-idempotency-quality.html"]')).toBeVisible();
});

test('post filters combine body search, book and category and survive reload', async ({ page }) => {
  await page.goto('/posts/');
  await page.locator('[data-book-filter="modern-ci"]').click();
  await page.locator('#post-category').selectOption('Delivery');
  await page.locator('#post-search').fill('cache');
  await expect(page.locator('#posts-grid .post-card:visible')).toHaveCount(1);
  await page.reload();
  await expect(page.locator('#posts-grid .post-card:visible')).toHaveCount(1);
  await page.locator('[data-post-reset]').click();
  await page.locator('#post-search').fill('password-reset');
  await expect(page.locator('#posts-grid .post-card:visible')).toHaveCount(1);
  await page.locator('#post-search').fill('no-such-topic-8746');
  await expect(page.locator('[data-post-empty]')).toBeVisible();
});

test('global search finds body text, filters types, restores URLs and handles empty results safely', async ({ page }) => {
  await page.goto('/search/?q=password-reset&type=posts');
  await expect(page.locator('[data-search-results] li')).toHaveCount(1);
  await expect(page.locator('[data-search-results] a')).toHaveAttribute('href', '/posts/your-access-log-does-not-need-that-token/');
  await page.locator('#search-type').selectOption('chapters');
  await page.locator('#site-query').fill('nginx');
  await expect(page.locator('[data-search-results] li').first()).toBeVisible();
  await expect(page).toHaveURL(/type=chapters/);
  await page.reload();
  await expect(page.locator('#site-query')).toHaveValue('nginx');
  await expect(page.locator('#search-type')).toHaveValue('chapters');
  await page.locator('#site-query').fill('<img src=x onerror=alert(1)>');
  await expect(page.locator('[data-search-status]')).toContainText('No results');
  await expect(page.locator('[data-search-results] img')).toHaveCount(0);
  await page.goto('/search/?q=r%C3%A9covery&type=invalid');
  await expect(page.locator('#search-type')).toHaveValue('all');
  await expect(page.locator('[data-search-results] li').first()).toBeVisible();
});

test('search falls back to a usable directory if its index cannot load', async ({ page }) => {
  await page.route('**/search-index.json', route => route.abort());
  await page.goto('/search/?q=deploy');
  await expect(page.locator('[data-search-status]')).toContainText('temporarily unavailable');
  await expect(page.locator('[data-search-directory]')).toBeVisible();
  await expect(page.locator('[data-search-directory] a').first()).toHaveAttribute('href', '/books/modern-ci/');
});

test('reader saves preferences and restores a real reading position from the book overview', async ({ page }) => {
  await page.goto('/books/modern-ci/10-fences.html');
  await page.locator('#reader-theme').selectOption('dark');
  await page.locator('#reader-size').selectOption('large');
  await page.keyboard.press('PageDown');
  await page.locator('.book-article h2').nth(2).scrollIntoViewIfNeeded();
  await expect.poll(() => page.evaluate(() => JSON.parse(localStorage.getItem('codepop:reading:modern-ci') || '{}').progress || 0)).toBeGreaterThan(.05);
  await page.goto('/books/modern-ci/');
  const resume = page.locator('[data-resume-book="modern-ci"]');
  await expect(resume).toBeVisible();
  await expect(resume).toHaveAttribute('href', '/books/modern-ci/10-fences.html?resume=1');
  await resume.click();
  await expect(page.locator('#reader-theme')).toHaveValue('dark');
  await expect(page.locator('#reader-size')).toHaveValue('large');
  await expect.poll(() => page.locator('[data-reader-scroll]').evaluate(element => element.scrollTop)).toBeGreaterThan(500);
  expect(await page.evaluate(() => scrollY)).toBe(0);
  await expect(page).not.toHaveURL(/resume=/);
  await page.locator('[data-reader-reset]').click();
  await expect(page.locator('#reader-theme')).toHaveValue('paper');
  await expect(page.locator('#reader-size')).toHaveValue('regular');
});

test('reader still works when storage is unavailable or corrupted', async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem('codepop:reader-preferences', '{broken');
    localStorage.setItem('codepop:reading:modern-ci', JSON.stringify({ url: 'https://example.com/evil.html', progress: .5 }));
    Storage.prototype.setItem = () => { throw new Error('Storage unavailable'); };
  });
  await page.goto('/books/modern-ci/');
  await expect(page.locator('[data-resume-book]')).toBeHidden();
  await page.goto('/books/modern-ci/10-fences.html');
  await page.locator('#reader-size').selectOption('extra');
  await expect(page.locator('[data-reader-status]')).toContainText('unavailable');
  await expect(page.locator('.book-reader')).toHaveAttribute('data-text-size', 'extra');
});

test('document reader supports contents, outline, progress, focus and chapter navigation', async ({ page }) => {
  await page.goto('/books/universal-tracking/16-realtime.html');
  const contents = page.locator('[data-reader-contents]');
  await expect(contents).toHaveAttribute('aria-expanded', 'true');
  await page.locator('#reader-chapter-query').fill('idempotency');
  await expect(page.locator('.reader-chapters li:visible')).toHaveCount(1);
  await page.locator('#reader-chapter-query').fill('no-matching-chapter-8746');
  await expect(page.locator('[data-reader-chapter-empty]')).toBeVisible();
  await page.locator('#reader-chapter-query').fill('');
  await expect(page.locator('.reader-chapters li:visible')).toHaveCount(42);
  await page.locator('.book-navigation > summary').click();
  const outline = page.locator('[data-reader-headings] a').nth(1);
  const target = await outline.getAttribute('href');
  await outline.click();
  await expect(page).toHaveURL(new RegExp(`${target}$`));
  await expect.poll(() => page.locator('[data-reader-progress]').evaluate(element => element.value)).toBeGreaterThan(20);
  const headingTop = await page.locator(target).evaluate(element => element.getBoundingClientRect().top);
  const toolbarBottom = await page.locator('.reader-deskbar').evaluate(element => element.getBoundingClientRect().bottom);
  expect(headingTop).toBeGreaterThan(toolbarBottom);
  await contents.click();
  await expect(page.locator('.reader-sidebar')).toBeHidden();
  await contents.click();
  await expect(page.locator('.reader-sidebar')).toBeVisible();
  const focus = page.locator('[data-reader-focus]');
  await focus.click();
  await expect(focus).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('.site-header')).toBeHidden();
  await expect(page.locator('.book-article')).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(focus).toHaveAttribute('aria-pressed', 'false');
  await expect(focus).toBeFocused();
  await expect(page.locator('.site-header')).toBeVisible();
  await page.locator('#reader-chapter').selectOption('/books/universal-tracking/12-idempotency-quality.html');
  await expect(page).toHaveURL(/12-idempotency-quality.html$/);
  await expect(page.locator('.book-article h1')).toContainText('Idempotency');
});

test('document reader controls stay usable on a small screen and print only the section', async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 900 });
  await page.goto('/books/modern-ci/10-fences.html');
  const contents = page.locator('[data-reader-contents]');
  await expect(contents).toHaveAttribute('aria-expanded', 'false');
  await contents.focus(); await page.keyboard.press('Enter');
  await expect(page.locator('.reader-sidebar')).toBeVisible();
  await contents.click();
  await page.locator('#reader-size').selectOption('extra');
  await page.keyboard.press('PageDown');
  await page.locator('.book-article h2').last().scrollIntoViewIfNeeded();
  const toolbar = await page.locator('.reader-deskbar').boundingBox();
  expect(toolbar.y).toBe(0);
  expect(toolbar.y + toolbar.height).toBeLessThan(450);
  await page.evaluate(() => { window.print = () => { document.body.dataset.printRequested = 'true'; }; });
  await page.locator('[data-reader-print]').click();
  await expect(page.locator('body')).toHaveAttribute('data-print-requested', 'true');
  const readingPosition = await page.locator('[data-reader-scroll]').evaluate(element => element.scrollTop);
  await page.pdf({ format: 'A4' });
  await expect.poll(() => page.locator('[data-reader-scroll]').evaluate(element => element.scrollTop)).toBe(readingPosition);
  await page.emulateMedia({ media: 'print' });
  await expect(page.locator('.reader-deskbar')).toBeHidden();
  await expect(page.locator('.site-footer')).toBeHidden();
  await expect(page.locator('.reader-pager')).toBeHidden();
  await expect(page.locator('.book-article h1')).toBeVisible();
  expect(await page.locator('[data-reader-scroll]').evaluate(element => getComputedStyle(element).overflowY)).toBe('visible');
  expect((await page.locator('.reader-content').boundingBox()).height).toBeGreaterThan(900);
});

for (const width of [390, 1920]) {
  test(`reader uses the full window and scrolls text independently at ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 900 });
    await page.goto('/books/universal-tracking/16-realtime.html');
    const scrollPort = page.locator('[data-reader-scroll]');
    const sidebar = page.locator('.reader-sidebar');
    const toolbar = page.locator('.reader-deskbar');
    const navigation = page.locator('[data-reader-navigation]');
    await expect(page.locator('.site-header')).toBeVisible();
    const shell = await page.locator('.reader-shell').boundingBox();
    expect(shell.x).toBe(0);
    expect(shell.width).toBe(width);
    if (width > 980) {
      expect((await sidebar.boundingBox()).x).toBe(0);
      await sidebar.evaluate(element => { element.scrollTop = 350; });
      await expect(page.locator('.site-header')).toBeVisible();
      expect(await scrollPort.evaluate(element => element.scrollTop)).toBe(0);
    }
    await scrollPort.hover();
    await page.mouse.wheel(0, 900);
    await expect.poll(() => scrollPort.evaluate(element => element.scrollTop)).toBeGreaterThan(400);
    await expect(page.locator('.site-header')).toBeHidden();
    await expect(navigation).toHaveAttribute('aria-expanded', 'false');
    expect((await toolbar.boundingBox()).y).toBe(0);
    expect(await page.evaluate(() => scrollY)).toBe(0);
    const panel = await scrollPort.boundingBox();
    expect(panel.x + panel.width).toBe(width);
    expect(panel.y + panel.height).toBe(900);
    const textWidth = await page.locator('.book-article').evaluate(element => element.getBoundingClientRect().width);
    expect(textWidth).toBeGreaterThan(panel.width - 100);
    const place = await scrollPort.evaluate(element => element.scrollTop);
    await navigation.click();
    await expect(page.locator('.site-header')).toBeVisible();
    expect(await scrollPort.evaluate(element => element.scrollTop)).toBe(place);
    await scrollPort.focus();
    await page.keyboard.press('PageDown');
    await expect.poll(() => scrollPort.evaluate(element => element.scrollTop)).toBeGreaterThan(place);
    await expect(page.locator('.site-header')).toBeHidden();
    await page.locator('[data-reader-start]').click();
    await expect.poll(() => scrollPort.evaluate(element => element.scrollTop)).toBe(0);
    await expect(page.locator('.site-header')).toBeVisible();
    if (width <= 980) {
      const contents = page.locator('[data-reader-contents]');
      await contents.click();
      expect((await sidebar.boundingBox()).x).toBe(0);
      expect((await scrollPort.boundingBox()).height).toBeGreaterThan(500);
      await page.keyboard.press('Escape');
      await expect(sidebar).toBeHidden();
      await expect(contents).toBeFocused();
    }
  });
}

test('switching chapters preserves the hidden site menu before reader JavaScript loads', async ({ page }) => {
  await page.goto('/books/universal-tracking/16-realtime.html');
  await page.locator('[data-reader-scroll]').hover();
  await page.mouse.wheel(0, 600);
  await expect(page.locator('.site-header')).toBeHidden();
  const nextChapter = await page.locator('.reader-pager a[rel="next"]').getAttribute('href');
  let release;
  const delayed = new Promise(resolve => { release = resolve; });
  await page.route('**/assets/js/reader.js', async route => { await delayed; await route.continue(); });
  try {
    await page.locator(`.reader-chapters a[href="${nextChapter}"]`).click({ noWaitAfter: true });
    await page.waitForURL(nextChapter, { waitUntil: 'commit' });
    await page.locator('.book-article h1').waitFor();
    await expect(page.locator('.site-header')).toBeHidden();
    expect((await page.locator('.reader-deskbar').boundingBox()).y).toBe(0);
    release();
    await expect(page.locator('[data-reader-toolbar]')).toBeVisible();
    await expect(page.locator('[data-reader-navigation]')).toHaveAttribute('aria-expanded', 'false');
    expect(await page.locator('[data-reader-scroll]').evaluate(element => element.scrollTop)).toBe(0);
    await page.reload();
    await expect(page.locator('.site-header')).toBeHidden();
    await page.goto('/books/modern-ci/10-fences.html');
    await expect(page.locator('.site-header')).toBeVisible();
  } finally { release(); }
});

test('the mobile document stays in place while reading controls initialize', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 900 });
  let release;
  const delayed = new Promise(resolve => { release = resolve; });
  await page.route('**/assets/js/reader.js', async route => { await delayed; await route.continue(); });
  try {
    await page.goto('/books/universal-tracking/16-realtime.html', { waitUntil: 'commit' });
    await page.locator('.book-article h1').waitFor();
    await page.waitForFunction(() => getComputedStyle(document.querySelector('[data-reader-toolbar]')).visibility === 'hidden');
    await page.evaluate(() => document.fonts.ready);
    const before = await page.locator('.book-article h1').boundingBox();
    release();
    await expect(page.locator('[data-reader-toolbar]')).toBeVisible();
    const after = await page.locator('.book-article h1').boundingBox();
    expect(Math.abs(after.y - before.y)).toBeLessThan(1);
    const diagram = page.locator('.book-article img').first();
    await expect(diagram).toHaveAttribute('width', /^[1-9]\d+$/);
    await expect(diagram).toHaveAttribute('height', /^[1-9]\d+$/);
  } finally { release(); }
});

test('CV preserves concurrent roles and completed employment periods, projects, books and search', async ({ page }) => {
  await page.goto('/');
  await page.locator('.main-nav .nav-cv').click();
  await expect(page).toHaveURL('/cv/');
  await expect(page.locator('.nav-cv')).toHaveAttribute('aria-current', 'page');
  const companies = page.locator('.cv-experience');
  await expect(companies).toHaveCount(11);
  const currentRoles = companies.nth(0).locator('.cv-roles > div').or(companies.nth(1).locator('.cv-roles > div'));
  await expect(currentRoles.locator('h4')).toHaveText(['DevOps Engineer', 'Back End Developer', 'Founder / CEO']);
  await expect(currentRoles.locator('time')).toHaveText(['May 2023', 'July 2022', 'May 2015']);
  await expect(currentRoles).toContainText(['Present', 'Present', 'Present']);
  await expect(page.locator('.cv-role-skills li')).toHaveCount(9);
  await expect(page.locator('.cv-role-location').first()).toContainText('Remote');
  const pastRoles = [
    ['Carnegie Technologies', 'Software Developer', 'November 2021', 'July 2022', '9 mos', 'Full-time', null],
    ['Pannovate', 'Back End Developer', 'October 2020', 'March 2021', '6 mos', 'Full-time', 'Greater London, England, United Kingdom'],
    ['Upstack.co', 'Software Engineer', 'February 2018', 'August 2020', '2 yrs 7 mos', 'Full-time', '26 Broadway New York, NY 10004'],
    ['Devtech', 'Back End Developer', 'August 2019', 'January 2020', '6 mos', 'Contract', 'Belgrade, Serbia'],
    ['AscalGroup', 'Software Development Architect', 'October 2017', 'April 2018', '7 mos', 'Full-time', 'Cesta v Mestni log 88a 1000 Ljubljana Slovenia Europe'],
    ['DVDPost', 'Web Developer', 'February 2016', 'November 2017', '1 yr 10 mos', 'Full-time', 'Brussels'],
    ['TNation', 'Ruby on Rails Applications Developer', 'May 2015', 'June 2016', '1 yr 2 mos', 'Full-time', 'Belgrade'],
    ['DODO STT d.o.o.', 'Ruby on Rails Application Developer, PHP Application Developer', 'March 2013', 'November 2014', '1 yr 9 mos', 'Full-time', 'Serbia'],
    ['Eurocard d.o.o.', 'Web Application Developer', 'February 2009', 'December 2012', '3 yrs 11 mos', 'Full-time', 'Aleksinac'],
  ];
  for (const [company, title, start, end, duration, context, location] of pastRoles) {
    const card = companies.filter({ has: page.getByRole('heading', { name: company, exact: true }) });
    await expect(card.locator('h4')).toHaveText(title);
    await expect(card.locator('time')).toHaveText([start, end]);
    await expect(card.locator('.cv-roles > div > p').first()).toContainText(duration);
    await expect(card.locator('.cv-company-heading > div > p')).toContainText(`${context} · ${duration}`);
    await expect(card).not.toContainText('Present');
    if (location) await expect(card.locator('.cv-role-location')).toContainText(location);
    else await expect(card.locator('.cv-role-location')).toHaveCount(0);
  }
  await expect(page.locator('.cv-project')).toHaveCount(projectCount);
  await expect(page.locator('.cv-books li')).toHaveCount(catalog.length);
  await expect(page.locator('.cv-profile img')).toBeVisible();
  await expect(page.locator('[data-cv-print]')).toBeVisible();
  await page.locator('.cv-sidebar a[href="#experience"]').click();
  await expect(page).toHaveURL(/#experience$/);
  await page.goto('/search/?q=Founder&type=pages');
  await expect(page.locator('[data-search-results] a[href="/cv/"]')).toBeVisible();
  await page.goto('/search/?q=Carnegie&type=pages');
  await expect(page.locator('[data-search-results] a[href="/cv/"]')).toBeVisible();
  await page.goto('/cv/');
  await page.emulateMedia({ media: 'print' });
  await expect(page.locator('.site-header')).toBeHidden();
  await expect(page.locator('.cv-experience')).toHaveCount(11);
  await expect(page.locator('.cv-hero h1')).toBeVisible();
});

test('CodePop is discoverable, describes the company and connects to its official services and founder', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('.venture-card')).toHaveAttribute('href', '/codepop/');
  await page.locator('.main-nav .nav-codepop').click();
  await expect(page).toHaveURL('/codepop/');
  await expect(page.locator('.nav-codepop')).toHaveAttribute('aria-current', 'page');
  await expect(page.locator('h1')).toHaveText('CodePop.');
  await expect(page.locator('.codepop-services article')).toHaveCount(6);
  await expect(page.locator('.codepop-solutions article')).toHaveCount(4);
  await expect(page.locator('.codepop-process li')).toHaveCount(4);
  await expect(page.locator('#founder')).toContainText('May 2015');
  await expect(page.locator('#founder a[href="/cv/"]')).toBeVisible();
  await expect(page.locator('.footer-codepop')).toHaveAttribute('href', '/codepop/');
  for (const section of ['services', 'solutions', 'process']) {
    await expect(page.locator(`a[href="https://www.codepop.tech/en/${section}"]`)).toBeVisible();
  }
  const graph = await page.locator('script[type="application/ld+json"]').evaluate(element => JSON.parse(element.textContent)['@graph']);
  const company = graph.find(item => item.mainEntity?.['@type'] === 'Organization').mainEntity;
  expect(company.name).toBe('CodePop');
  expect(company.url).toBe('https://www.codepop.tech/en/');
  expect(company.founder['@id']).toMatch(/\/about\/#person$/);
  await expect(page.locator('meta[property="og:image"]')).toHaveAttribute('content', /\/assets\/social\/codepop.png$/);
  await page.getByRole('navigation', { name: 'CodePop sections' }).getByRole('link', { name: 'Let’s talk' }).click();
  await expect(page).toHaveURL(/#company-contact$/);
  await expect(page.locator('#company-contact a[href^="mailto:"]')).toBeInViewport();
  await page.goto('/search/?q=cutover&type=pages');
  await expect(page.locator('[data-search-results] a[href="/codepop/"]')).toBeVisible();
});

test('video embeds load only after a choice and switching playlists stops the previous player', async ({ page }) => {
  await page.route('https://www.youtube-nocookie.com/**', route => route.fulfill({ contentType: 'text/html', body: '<title>Test player</title>' }));
  await page.goto('/videos/');
  await expect(page.locator('iframe[src]')).toHaveCount(0);
  const cards = page.locator('[data-playlist]');
  await cards.nth(0).locator('[data-load-playlist]').click();
  await expect(cards.nth(0).locator('iframe')).toBeVisible();
  await cards.nth(1).locator('.playlist-video').nth(1).click();
  await expect(cards.nth(0).locator('iframe')).toBeHidden();
  await expect(cards.nth(0).locator('iframe')).not.toHaveAttribute('src');
  await expect(cards.nth(1).locator('iframe')).toHaveAttribute('src', /youtube-nocookie\.com\/embed\//);
  await expect(cards.nth(1).locator('.playlist-video[aria-current]')).toHaveCount(1);
  await cards.nth(0).locator('[data-load-playlist]').click();
  await expect(cards.nth(0).locator('iframe')).toHaveAttribute('title', /YouTube playlist$/);
  const selectedId = await cards.nth(1).locator('.playlist-video').nth(1).getAttribute('data-video-id');
  await page.goto(`/videos/?video=${selectedId}`);
  await expect(page.locator('iframe[src]')).toHaveCount(1);
  await expect(page.locator('iframe[src]')).toHaveAttribute('src', new RegExp(selectedId));
});

test('a retired URL returns the useful 404 page with a topic search', async ({ page }) => {
  const response = await page.goto('/posts/routingo/');
  expect(response.status()).toBe(404);
  await expect(page.locator('h1')).toHaveText('A small detour.');
  await expect(page.locator('#missing-query')).toHaveValue('routingo');
  await page.locator('#missing-query').fill('deployment');
  await page.locator('.not-found-search button').click();
  await expect(page).toHaveURL(/\/search\/\?q=deployment/);
  await expect(page.locator('[data-search-results] li').first()).toBeVisible();
});

test('project cards lead to genuine project pages and source repositories', async ({ page }) => {
  await page.goto('/projects/');
  await expect(page.locator('.project-list .work-card')).toHaveCount(4);
  for (const id of ['orch', 'cloudivision', 'clusterforge', 'container-desk']) {
    await page.goto(`/projects/${id}/`);
    await expect(page.locator('.project-flow li')).toHaveCount(5);
    await expect(page.getByRole('link', { name: 'View source' })).toHaveAttribute('href', `https://github.com/alekpopovic/${id}`);
    await expect(page.locator('.project-preview img').first()).toBeVisible();
    await page.locator('.project-preview img').first().scrollIntoViewIfNeeded();
    await expect.poll(() => page.locator('.project-preview img').first().evaluate(image => image.complete && image.naturalWidth > 0)).toBe(true);
  }
});

for (const width of [320, 390, 768, 981, 1024, 1440]) {
  test(`navigation and new layouts work at ${width}px without overflow`, async ({ page }) => {
    await page.setViewportSize({ width, height: 900 });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    for (const path of ['/', '/ai/', '/posts/claude-code-slash-commands/', '/cv/', '/codepop/', '/search/?q=deployment', '/projects/container-desk/', '/books/logbranik/05-logs-without-secrets.html', '/books/agentplane/', '/books/agentplane/18-approvals.html', '/books/secret-contract-operator/', '/books/secret-contract-operator/13-rotacija-i-rollout.html', '/books/universal-tracking/', '/books/universal-tracking/16-realtime.html', '/posts/an-approximate-marker-needs-an-approximate-payload/', '/videos/']) {
      await page.goto(path);
      await page.evaluate(() => document.fonts.ready);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), path).toBe(true);
      const titlesFit = await page.locator('.book-feature-copy :is(h1.display, h2.display)').evaluateAll(titles => titles.every(title => {
        const range = document.createRange();
        range.selectNodeContents(title);
        return [...range.getClientRects()].every(rect => rect.right <= title.getBoundingClientRect().right + 1);
      }));
      expect(titlesFit, `Book titles fit their columns on ${path}`).toBe(true);
      const cvTitleFits = await page.locator('.cv-hero h1').evaluateAll(titles => titles.every(title => {
        const range = document.createRange(); range.selectNodeContents(title);
        return [...range.getClientRects()].every(rect => rect.right <= title.getBoundingClientRect().right + 1);
      }));
      expect(cvTitleFits, `CV title fits its column on ${path}`).toBe(true);
    }
    if (width <= 980) {
      const menu = page.locator('.menu-toggle');
      await menu.focus(); await page.keyboard.press('Enter');
      await expect(menu).toHaveAttribute('aria-expanded', 'true');
      await expect(page.locator('.main-nav')).toBeVisible();
      await page.keyboard.press('Escape');
      await expect(menu).toHaveAttribute('aria-expanded', 'false');
      await expect(menu).toBeFocused();
    }
    expect(errors).toEqual([]);
  });
}

test('books, notes, video links and search directory work without JavaScript', async ({ browser, baseURL }) => {
  const context = await browser.newContext({ baseURL, javaScriptEnabled: false, viewport: { width: 390, height: 900 } });
  try {
    const page = await context.newPage();
    await page.goto('/search/');
    await expect(page.locator('[data-search-directory]')).toBeVisible();
    await expect(page.locator('[data-search-directory] a')).toHaveCount(directoryCount);
    await page.goto('/posts/');
    await expect(page.locator('#posts-grid .post-card:visible')).toHaveCount(postCount);
    await page.goto('/books/modern-ci/10-fences.html');
    await expect(page.locator('.book-article h1')).toBeVisible();
    await expect(page.locator('[data-reader-toolbar]')).toBeHidden();
    await expect(page.locator('.book-navigation')).toBeVisible();
    await expect(page.locator('.reader-document-actions a[download]')).toHaveCount(2);
    for (const id of Object.keys(sampleChapters)) {
      const book = catalog.find(item => item.id === id);
      await page.goto(book.url);
      await expect(page.locator('.book-contents-list li')).toHaveCount(book.chapters.length);
      await page.goto(book.first_chapter);
      await expect(page.locator('.book-article h1')).toBeVisible();
    }
    await page.goto('/videos/');
    await expect(page.locator('.playlist-video')).toHaveCount(15);
    await expect(page.locator('iframe[src]')).toHaveCount(0);
    await page.goto('/cv/');
    await expect(page.locator('.cv-roles h4')).toHaveCount(12);
    await expect(page.getByRole('heading', { name: 'Eurocard d.o.o.', exact: true })).toBeVisible();
    await expect(page.locator('.main-nav .nav-cv')).toBeVisible();
    await expect(page.locator('[data-cv-print]')).toBeHidden();
    await page.goto('/codepop/');
    await expect(page.locator('.codepop-services article')).toHaveCount(6);
    await expect(page.locator('.main-nav .nav-codepop')).toBeVisible();
    await page.getByRole('navigation', { name: 'CodePop sections' }).getByRole('link', { name: 'Let’s talk' }).click();
    await expect(page.locator('#company-contact a[href^="mailto:"]')).toBeInViewport();
  } finally { await context.close(); }
});

for (const path of ['/', '/about/', '/cv/', '/codepop/', '/contact/', '/posts/', '/posts/a-timeout-is-not-a-stopped-deployment/', '/posts/a-validation-result-can-reveal-a-secret/', '/posts/an-approximate-marker-needs-an-approximate-payload/', '/search/', '/books/logbranik/', '/books/modern-ci/10-fences.html', '/books/agentplane/', '/books/agentplane/18-approvals.html', '/books/secret-contract-operator/', '/books/secret-contract-operator/13-rotacija-i-rollout.html', '/books/universal-tracking/', '/books/universal-tracking/16-realtime.html', '/books/universal-tracking/94-appendix-runbooks.html', '/videos/', '/projects/container-desk/', '/404.html']) {
  test(`accessibility: ${path}`, async ({ page }) => {
    await page.goto(path);
    await page.evaluate(() => document.fonts.ready);
    if (path === '/search/') await expect(page.locator('[data-search-status]')).not.toHaveText('Loading the library…');
    const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa', 'best-practice']).analyze();
    expect(result.violations.map(item => ({ id: item.id, targets: item.nodes.map(node => node.target) }))).toEqual([]);
  });
}

test('dark reader meets automated accessibility checks', async ({ page }) => {
  await page.goto('/books/logbranik/05-logs-without-secrets.html');
  await page.locator('#reader-theme').selectOption('dark');
  const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']).analyze();
  expect(result.violations.map(item => ({ id: item.id, targets: item.nodes.map(node => node.target) }))).toEqual([]);
});
