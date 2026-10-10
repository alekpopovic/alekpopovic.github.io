# Search visibility and measurement

Jekyll generates `/sitemap.xml`, `/robots.txt`, `/feed.xml`, canonical URLs,
social previews and JSON-LD. Each chapter has its own canonical URL. Search and
404 pages are marked `noindex` and omitted from the sitemap. Removed articles
without a replacement keep genuine 404 responses with navigation and search.
Old `.html` navigation URLs use static redirect pages. Legacy downloads serve
byte-identical PDF/EPUB copies because GitHub Pages cannot issue custom server
redirects for those files.

## Google Search Console

No account is connected yet. After publishing:

1. Create a **URL-prefix property** for `https://alekpopovic.github.io/` in
   [Search Console](https://search.google.com/search-console/).
2. Choose HTML-tag verification. Put only the `content` token into
   `google_site_verification` in `_config.yml`.
3. Rebuild and publish, then click Verify in Search Console.
4. Submit `https://alekpopovic.github.io/sitemap.xml` and inspect a homepage,
   book, chapter and post.

The URL-prefix method fits GitHub's hosting, since GitHub controls the `github.io`
DNS zone. The token is public metadata. See Google's
[verification guide](https://support.google.com/webmasters/answer/9008080).

## Google Analytics

The owner's GA4 measurement ID `G-QCGFECRJDS` is configured in `google_analytics`
in `_config.yml`. The shared `_includes/google-analytics.html` includes the async
Google tag and initializes it once on every HTML page, including book chapters,
CV, CodePop, 404 and legacy redirect pages. New pages inherit it through their layout.
Set `google_analytics: ""` and rebuild to disable it. Restart the development server
after changing `_config.yml`.

After publishing, check the production site with
[Tag Assistant](https://tagassistant.google.com/) and the property's Realtime
report. Local checks verify the rendered tag and initialization; they do not
verify access to the owner's account or receipt of events in Google Analytics.
Search Console still needs its separate verification token.

UI tests stub the Google tag and local Lighthouse runs block Google Analytics
requests so synthetic visits do not enter the owner's reports. Production
Lighthouse runs include the real tag. See Google's
[Google tag guide](https://developers.google.com/tag-platform/gtagjs).

## Optional Plausible analytics

The separate Plausible adapter stays disabled while `analytics.domain` is empty.
RSS subscriptions work without an account.
The adapter supports Plausible Cloud or a compatible self-hosted endpoint. Create
a site in that service, then configure:

```yaml
analytics:
  domain: "alekpopovic.github.io"
  endpoint: "https://plausible.io/api/event"
```

| Event | Properties | Trigger |
| --- | --- | --- |
| Book download | book, format | PDF or EPUB link activation |
| Project click | project | Repository link activation |
| Contact click | channel | Email, phone, Viber or WhatsApp activation |
| Engaged reading | kind | 30 seconds on a post or chapter and 75% reached |

These custom events belong to the Plausible adapter; the Google tag uses its own
standard configuration. Create matching custom-event goals in the Plausible
dashboard. Search queries,
fragments, contact addresses and phone numbers are omitted. Requests use no
cookies; localhost and browser privacy signals are respected. See the
[Plausible Events API reference](https://plausible.io/docs/events-api).

## Reproducible quality checks

```sh
npm run build
bundle exec jekyll build
python scripts/check-books.py
npm run check:site
npx playwright install chromium
npm run test:ui
npm run check:performance
```

Use `CHROME_PATH=/usr/bin/google-chrome` for an existing Chrome. UI tests run on
a static server at port 4173. Coverage includes search, filters, saved reading
position, document controls, focus mode, print layouts, CV navigation,
unavailable storage, keyboard navigation, video switching, 404,
AI category/tool/search combinations, shareable AI URLs, responsive layouts
and automated WCAG A/AA checks. Automated checks supplement
manual keyboard/screen-reader testing; they do not certify full conformance.

Lighthouse reports go to ignored `reports/`. CI requires mobile performance >= 85,
accessibility = 100 and CLS <= 0.1 on the homepage, AI Lab, AI guide, CV, CodePop,
book overview, chapter reader, and engineering post. Total CSS has a 130 KB budget
(including the separate AI theme) and total JS has a 65 KB budget. These assets
are generated locally. Lighthouse is a lab measurement; field LCP, INP and CLS
depend on actual visits and should be reviewed in Search Console.

To measure the currently published homepage without publishing local changes:

```sh
npm run check:performance -- https://alekpopovic.github.io/
```
