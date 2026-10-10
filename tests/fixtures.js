const { test: base, expect } = require('@playwright/test');

// Keep synthetic browser visits out of the owner's GA4 reports.
const test = base.extend({
  context: async ({ context }, use) => {
    await context.route('https://www.googletagmanager.com/**', route => route.fulfill({ contentType: 'text/javascript', body: '' }));
    await context.route(/^https:\/\/([^/]+\.)?google-analytics\.com\//, route => route.abort());
    await use(context);
  },
});

module.exports = { test, expect };
