# Search visibility and measurement

Jekyll generates `/sitemap.xml`, `/robots.txt`, `/feed.xml`, canonical URLs,
social previews and JSON-LD. Each chapter has its own canonical URL. Search and
404 pages are marked `noindex` and omitted from the sitemap. Removed articles
without a replacement keep genuine 404 responses with navigation and search.
Old `.html` navigation URLs use static redirect pages. Legacy downloads serve
byte-identical PDF/EPUB copies because GitHub Pages cannot issue custom server
redirects for those files.

## Google Search Console

The owner's HTML-tag token is configured in `google_site_verification`. The
owner-supplied `google2ab5b70940fe5c89.html` verification resource is also kept at
the public root, with its exact original text. Public checks validate both.
These files do not establish account verification by themselves. After publishing:

1. Create a **URL-prefix property** for `https://www.alekpopovic.com/` in
   [Search Console](https://search.google.com/search-console/).
2. Choose HTML-tag verification using the supplied token, or the HTML-file
   method if that file was issued for this property.
3. Click Verify in Search Console after the public deployment checks pass.
4. Submit `https://www.alekpopovic.com/sitemap.xml` and inspect a homepage,
   book, chapter and post.

Alternatively, create a domain property for `alekpopovic.com` and add the exact
TXT record supplied by Google to that domain's DNS. Do not reuse Workspace
verification for `codepop.co.rs`: it belongs to a different domain and service.
The HTML token is public metadata. See Google's
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
Search Console still needs the owner to complete verification in their account.

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
  domain: "www.alekpopovic.com"
  endpoint: "https://plausible.io/api/event"
```

| Event | Properties | Trigger |
| --- | --- | --- |
| Book download | book, format | PDF or EPUB link activation |
| Project click | project | Repository link activation |
| Contact click | channel | Email, phone, Viber or WhatsApp activation |
| Engaged reading | kind | 30 seconds on a post or chapter and 75% reached |

These events belong to the optional Plausible adapter and are separate from the
GA4 content events described below. Create matching custom-event goals in the Plausible
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
npx playwright install --with-deps chromium firefox webkit
npm run test:ui
SITE_BROWSER=firefox npm run test:ui -- tests/compatibility.spec.js
SITE_BROWSER=webkit npm run test:ui -- tests/compatibility.spec.js
npm run check:labs
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
book overview, chapter reader, engineering post, learning path and project page.
The workshop directory and reading backup page are included too.
Each generated HTML page has a 130 KB CSS budget for its linked stylesheets;
the reader uses a smaller shared-shell bundle, and reader and AI styles load only
where used. Total JS has a 65 KB budget. These assets
are generated locally. Lighthouse is a lab measurement; field LCP, INP and CLS
depend on actual visits and should be reviewed in Search Console.

To measure the currently published homepage without publishing local changes:

```sh
npm run check:performance -- https://www.alekpopovic.com/
```

## GA4 content events

`assets/js/ga4-events.js` loads only when the owner configures `google_analytics`.
It emits events only on the configured HTTPS production hostname. Custom events
respect Do Not Track and Global Privacy Control; localhost visits are excluded.
The shared Google configuration strips search parameters and fragments from
`page_location` and reduces the configured referrer to its origin. GA4 enhanced
measurement is controlled separately in the owner's account; audit its settings
before claiming that every automatically collected field is sanitized.

| Event | Parameters | Meaning |
| --- | --- | --- |
| `chapter_open` | book_id, chapter_slug | A section was opened; not proof it was read |
| `chapter_complete` | book_id, chapter_slug | The visitor explicitly marked the section complete |
| `reading_engaged` | kind, book_id, chapter_slug | At least 30 seconds elapsed and 75% of the content was reached |
| `book_download` | book_id, format | A download link was activated; not proof a transfer completed |
| `project_open` | project_id | A featured source repository link was activated |
| `contact_open` | channel | A contact link was activated; not proof a message was sent |
| `learning_step_complete` | path_id, step | A visitor marked a learning step complete |

Custom events never include note text, selected text, contact addresses, phone
numbers, or search queries. IDs are allowlisted and bounded. The custom download
event deliberately differs from enhanced measurement's `file_download`; do not
sum both when reporting downloads.

In the owner's GA4 account:

1. Confirm the web stream uses `https://www.alekpopovic.com`.
2. Use Tag Assistant and Realtime/DebugView to perform one real chapter open,
   completion, download and repository click after deployment.
3. Create event-scoped custom dimensions for `book_id`, `chapter_slug`, `format`,
   `project_id`, `channel`, `kind`, `path_id` and `step` where reporting needs them.
4. Choose key events deliberately; ordinary reading and link activations are not
   completed sales or confirmed contacts.
5. Review field Core Web Vitals in Search Console when enough real traffic exists.

Local tests inspect queued events without sending them to the owner's account.
See [Google's event setup documentation](https://developers.google.com/analytics/devguides/collection/ga4/events).

## Subscriptions and editorial maintenance

`/subscribe/` exposes the article Atom feed and `/updates.xml` for site changes.
RSS works immediately after publication without a mailing service. Set an HTTPS
`newsletter_url` only after the owner creates an actual email subscription form;
an empty value renders no email subscription action. This site does not collect
email addresses or pretend to send newsletters.

Add entries with stable IDs to `_data/updates.yml`. Revised articles can use an
explicit `last_modified_at` timestamp; it updates JSON-LD and the article feed.
Never update verification dates automatically. Run `npm run check:content` for
metadata and `python scripts/check-content.py --links --strict-age` for source
links and the 90-day review interval. The scheduled Monday workflow uploads
`reports/content-review.md`; access errors request manual review, while definite
404/410 links and overdue reviews fail. A passing link check does not verify
command behavior or justify changing `verified_at`.

## Checks after deployment

The Pages workflow checks the public site after deployment, allowing time for
GitHub's caches to expose the expected commit. `publication-manifest.json` names
representative pages from every book, every project and the main sections, plus
all PDF/EPUB editions and representative legacy downloads. Checks validate the
revision, canonical/sharing URLs, configured Google tag, download signatures and
MIME types, sitemap/feed origins, robots and a genuine missing-page 404.

```sh
npm run check:publication
python scripts/check-publication.py --base-url http://127.0.0.1:4173
python -m unittest discover -s tests -p 'test_*.py' -v
```

A public check runs only after publication; local success does not mean changes
have been pushed or deployed. Preserve GitHub Pages' custom domain and use
GitHub Actions as its build source.
