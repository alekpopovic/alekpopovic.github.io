const { test, expect } = require('./fixtures');
const demos = require('../_data/project_demos.json');

test('project recordings decode, play, and provide readable scoped evidence', async ({ page }) => {
  for (const [id, demo] of Object.entries(demos)) {
    await page.goto(`/projects/${id}/`);
    const region = page.locator('.project-demo');
    await expect(region).toContainText(demo.scope);
    const video = region.locator('video');
    await expect(video).toHaveAttribute('preload', 'none');
    expect(await video.evaluate(element => element.autoplay)).toBe(false);
    await video.evaluate(async element => { element.muted = true; await element.play(); });
    await expect.poll(() => video.evaluate(element => element.currentTime)).toBeGreaterThan(0);
    expect(await video.evaluate(element => ({ error: element.error, width: element.videoWidth, height: element.videoHeight, duration: element.duration }))).toEqual({ error: null, width: 1280, height: 800, duration: expect.any(Number) });
    expect(await video.evaluate(element => element.duration)).toBeGreaterThan(5);
    await video.evaluate(element => element.pause());
    await region.locator('summary').focus();
    await page.keyboard.press('Enter');
    await expect(region.locator('details')).toHaveAttribute('open', '');
    if (demo.steps.length) {
      await expect(region.locator('pre')).toHaveCount(demo.steps.length);
    } else {
      await expect(region.locator('details')).toContainText('synthetic demo');
    }
  }
});
