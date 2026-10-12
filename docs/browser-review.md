# Browser and accessibility review

Review date: 2026-10-13. The production build uses local assets and the owner's
configured measurement settings. Synthetic browser visits block Google tag and
Analytics requests.

## Completed checks

- 138 Playwright Chromium tests cover navigation, combined filters and shared
  URLs, empty results, full-text search, reading controls, printing, notes,
  offline chapters, backup validation/merge/replacement/rollback, blocked
  storage, no-JavaScript reading, recording playback/transcripts, and automated
  accessibility checks. They also cover all four browser workshop starters and
  solutions, worker network isolation and timeout recovery, knowledge checks
  and answer backups, themed dropdown keyboard interaction, all five paths and 50 questions, mistake
  review, combined My Learning progress, source-matched workshop results, raw
  draft backup rollback, explicit code import, keyboard execution, bounded
  reference comparison, field-metric allowlisting, contextual book
  search, figure zoom, and glossary links.
- Twenty-five critical reading, keyboard, workshop, filtering, and no-JavaScript
  scenarios pass in both Playwright Firefox and WebKit. These are browser-engine tests on Linux,
  not claims about Safari or a physical iPhone.
- Mobile screenshots at 390 × 844 were visually reviewed for the reading
  backup page, AI workshops, newsletter, and public case studies. The reader
  was also visually reviewed at 1440 × 1000. The modern AI dropdowns were
  reviewed at both sizes, including their open popups. My Learning and the syntax-colored workshop
  editor were reviewed on desktop and mobile, and the AgentPlane overview title
  was checked on mobile after the Tailwind migration. Automated layout checks cover widths from
  320 to 1920 pixels.
- Backup preview receives keyboard focus; cancelling returns focus to the file
  chooser. Reader notes, contents, size controls, and hidden site navigation
  remain keyboard-operable across all three engines.
- Mobile Lighthouse checks pass on 16 representative routes: performance
  89–96, accessibility/best practices/SEO 100, and CLS below 0.015. These are
  local lab measurements, not field Core Web Vitals. The largest page loads
  110,409 bytes of CSS and 49,365 bytes of JavaScript, within the existing
  per-page ceilings.
- A separate build with an empty measurement ID contains no Google tag,
  initialization, GA4 event adapter, or field-metrics adapter on all 310 HTML resources. Google's
  exact-text verification resource is checked separately as a machine resource.

Local WebKit needed runtime libraries unpacked under `/tmp`, and a child
environment without inherited VS Code Snap GTK/GIO module paths. No system
libraries or repository browser binaries were changed. CI installs its browser
dependencies normally with `playwright install --with-deps`.

## Checks needing the owner's devices or accounts

Automated checks and screenshot inspection do not establish full accessibility
conformance. A physical phone and an actual screen-reader session were not
available for this review. Check VoiceOver with Safari on iOS and NVDA with
Firefox or Chrome on Windows when those devices are available. Follow the same
reading/notes/backup scenario, including focus order, announced labels/status,
200% zoom, and navigating to the next chapter while the site menu is hidden.

Search Console verification, GA4 event receipt, and email subscription delivery
must be confirmed in the owner's accounts. Public metadata and local event
queues do not prove receipt. See [measurement](measurement.md) and
[newsletter setup](newsletter.md). The Tailwind migration removes the previous build dependency finding; a clean
`npm ci` and registry-backed npm audit report zero known npm vulnerabilities.
See [dependency maintenance](dependencies.md), [owner setup](owner-setup.md), and
the [real-device worksheet](manual-accessibility.md).
