# Account steps that remain with the owner

Prepared on 2026-10-13. Publishing the site does not establish access to these
accounts. No account password or provider API key is needed in this repository.

## Google

The supplied Search Console tag and exact-text verification file are published;
the supplied GA4 measurement ID is configured globally. Public checks verify
these resources, and browser tests verify queued events without submitting
synthetic visits. Account verification, data receipt and indexing remain
unconfirmed.

Connect **GSC Wizard** to the Google account that owns the properties if you
want account reports inspected through the available integration. Installation
alone does not confirm access. Alternatively, complete these checks yourself:

1. In Search Console, select the URL-prefix property
   `https://www.alekpopovic.com/` and click Verify using the supplied tag/file.
2. Submit `https://www.alekpopovic.com/sitemap.xml`. Inspect the homepage, a
   chapter, a post and `/learn/workspace/`; record Google's reported indexing
   state. A successful HTTP response is not proof of indexing.
3. In GA4 confirm the web stream hostname, then perform a real chapter open,
   explicit completion, book download and repository click. Check Realtime or
   DebugView for the named events in `measurement.md`. Do not count link clicks
   as successful sales, transfers or sent messages.
4. Review enhanced measurement settings, reporting dimensions and field vitals
   as described in `measurement.md`. Account reports may require traffic/time.

## Email newsletter

The owner confirmed no provider account/form exists. `newsletter_url` stays
empty; no signup button or email delivery is claimed. The dated web archive at
`/newsletter/2026-10/` and `/newsletter.xml` work independently.

Create the Brevo account/form following `newsletter.md`, including double opt-in
and a tested unsubscribe. Supply only its public HTTPS signup URL, then set
`newsletter_url` and rebuild. Test confirmation and receipt before announcing
email delivery. Copy the reviewed web issue into the provider when ready; no
message is sent automatically by this site.

## Real-device accessibility

Follow `manual-accessibility.md` on the owner's physical phone and screen reader.
These sessions remain not run. Browser-engine and automated results are recorded
separately in `browser-review.md`.
