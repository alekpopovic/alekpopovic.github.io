# EPUB Reading Preview

**Passed** for final EPUB `e5ba1daf5715b0daa064d53cec68512e243340ef16b3fc2976e245f674f0562b`. Actual local Chromium rendered 24 cases: Chapters 4 and 17 plus Appendices A, B, C and F, at 390px and 1280px widths, 16px and 24px type, and light/dark themes. Every extracted archive member was byte-checked before browser launch. All 47 canonical reading sections are present.

The initial preview found table overflow; the corrected final CSS gives zero page overflow, no missing images, and working contents → chapter → worked answers → chapter navigation. Cover, lifecycle diagram, source listing, long historical HTML URLs/emoji, and reference tables were inspected in captured screenshots. Narrow large-type tables wrap into taller rows. The diagram alternative and caption describe selected legal edges and conditional cleanup; they do not promise a complete state graph. No footnote markup exists in this edition.

The JSON records exact Chromium version, command, inputs, timestamps, screenshot hashes, actions and observations. Screenshots stay in the internal `/tmp/inside-orch-epub-preview-e5ba1daf5715/screenshots/` directory. EPUBCheck and detailed archive structure are separate root-owned checks. Kindle, Apple Books, Kobo, Calibre and proprietary pagination were not tested; this is a documented Chromium XHTML preview.
