// Re-render captured terminal evidence, plus the real ContainerDesk browser demo.
// This optional authoring task is never part of an ordinary offline site build.
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from '@playwright/test';

const output = 'assets/projects/demos';
fs.mkdirSync(output, { recursive: true });
const demos = JSON.parse(fs.readFileSync('_data/project_demos.json', 'utf8'));
const preview = process.argv.find(arg => arg.startsWith('--preview='))?.slice(10);
const only = process.argv.find(arg => arg.startsWith('--only='))?.slice(7);
if (preview && !['127.0.0.1', 'localhost'].includes(new URL(preview).hostname)) throw new Error('Use a local ContainerDesk preview URL.');
const browser = await chromium.launch({ args: ['--no-sandbox'] });
try {
  for (const [id, demo] of Object.entries(demos)) {
    if (only && id !== only) continue;
    if (id === 'container-desk' && !preview) continue;
    const context = await browser.newContext({ viewport: { width: 1280, height: 800 }, recordVideo: { dir: '/tmp/codepop-project-video', size: { width: 1280, height: 800 } }, reducedMotion: 'reduce' });
    const page = await context.newPage(), video = page.video();
    if (id === 'container-desk') {
      await page.goto(preview);
      await page.waitForTimeout(1500);
      await page.getByRole('button', { name: 'Open demo', exact: true }).click();
      await page.getByText('DEMO · Synthetic data · No SSH', { exact: true }).waitFor();
      await page.waitForTimeout(2000);
      await page.screenshot({ path: path.join(output, `${id}.webp`), type: 'webp' });
      await page.getByText('demo-web', { exact: true }).click();
      await page.waitForTimeout(3000);
      await page.getByText('Compose', { exact: true }).click();
      await page.waitForTimeout(2500);
      await page.getByText('Images', { exact: true }).click();
      await page.waitForTimeout(2500);
      await page.getByText('Settings', { exact: true }).click();
      await page.waitForTimeout(2500);
    } else {
      await page.setContent('<!doctype html><html lang="en"><meta charset="utf-8"><title>Local verification replay</title><style>body{margin:0;padding:42px;background:#13141e;color:#eeedf5;font:16px/1.7 ui-monospace,monospace}header{color:#c9b0ff;font-size:18px;margin-bottom:12px}h1{font:700 27px/1.3 system-ui;margin:0 0 12px}aside{color:#aeb2c1;font-size:13px;margin-bottom:25px}main{height:565px;overflow:auto;border:1px solid #444656;border-radius:16px;padding:20px 24px;box-sizing:border-box}h2{white-space:pre-wrap;font-size:16px;color:#c1f4b1;margin:0 0 18px}pre{font:13px/1.65 ui-monospace,monospace;white-space:pre-wrap;overflow-wrap:anywhere;margin:0}footer{color:#aeb2c1;font-size:12px;margin-top:12px}</style><header>CodePop / Open engineering</header><h1></h1><aside></aside><main><h2></h2><pre></pre></main><footer></footer></html>');
      await page.evaluate(({ id, demo }) => {
        document.querySelector('h1').textContent = demo.title;
        document.querySelector('aside').textContent = `${id} · ${demo.source_commit.slice(0, 7)} · Captured ${demo.captured_at}`;
        document.querySelector('footer').textContent = 'Replay of actual recorded local command output. Full transcript and scope are available beside this video.';
      }, { id, demo });
      for (let i = 0; i < demo.steps.length; i++) {
        await page.evaluate(step => { document.querySelector('h2').textContent = '$ ' + step.command + (step.excerpt ? '\nOutput excerpt: ' + step.excerpt : ''); document.querySelector('pre').textContent = step.output; document.querySelector('main').scrollTop = 0; }, demo.steps[i]);
        await page.waitForTimeout(2500);
        if (i === 0) await page.screenshot({ path: path.join(output, `${id}.webp`), type: 'webp' });
        await page.evaluate(() => { const box = document.querySelector('main'); if (box.scrollHeight > box.clientHeight) box.scrollTop = box.scrollHeight; });
        await page.waitForTimeout(1800);
      }
    }
    await context.close();
    await video.saveAs(path.join(output, `${id}.webm`));
    console.log(`Saved ${id} recording and poster.`);
  }
} finally { await browser.close(); }
