const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  timeout: 30000,
  fullyParallel: true,
  workers: process.env.CI ? 2 : 2,
  retries: process.env.CI ? 1 : 0,
  outputDir: `test-results/${process.env.SITE_BROWSER || 'chromium'}`,
  reporter: [['list'], ['html', { open: 'never', outputFolder: `playwright-report/${process.env.SITE_BROWSER || 'chromium'}` }]],
  use: {
    browserName: process.env.SITE_BROWSER || 'chromium',
    baseURL: 'http://127.0.0.1:4173',
    viewport: { width: 1440, height: 1000 },
    reducedMotion: 'reduce',
    trace: 'retain-on-failure',
    launchOptions: process.env.CHROME_PATH && (!process.env.SITE_BROWSER || process.env.SITE_BROWSER === 'chromium') ? { executablePath: process.env.CHROME_PATH, args: ['--no-sandbox'] } : {},
  },
  webServer: {
    command: 'python3 scripts/serve-site.py',
    url: 'http://127.0.0.1:4173',
    reuseExistingServer: !process.env.CI,
    timeout: 10000,
  },
});
