# Multi-format design system

Source identity: [docs/BRAND.md:1](https://github.com/alekpopovic/orch/blob/cbfc94ade5b57e449d6b73bf1485b1c5b1647022/docs/BRAND.md#L1-L52). Orbit-and-node mark geometry stays exact. `style-tokens.json` records original vector hashes and source palette. New book cover/layout composition may use these vectors with attribution; do not redraw them as approximate raster topology.

## Visual hierarchy and specimen

Deep Space `#020617`, Orbit Cyan `#22d3ee`, Control Blue `#2374e1`, Rollout Violet `#8b5cf6`, Success Mint `#a7f3d0`, Slate Text `#0f172a`. On paper, use dark Slate body and a darker `#174f9c` link adaptation because bright cyan/blue are accents, not automatically accessible small text. Source-calculated contrast ratios: {'slate_text/paper': 17.85, 'link_on_paper/paper': 7.97, 'orbit_cyan/deep_space': 11.16, 'success_mint/deep_space': 15.73}. These calculations are actual static checks, not a browser accessibility audit.

Use chapter number, concise H1, learning problem, source panel, failure window, lab, exercises and source references in consistent order. Callouts have explicit text labels **BASELINE**, **OBSERVED**, **EXPECTED**, **TEACHING EXTENSION**; color is supplementary. Tables use visible header cells and row rules. Grayscale must preserve numbered steps, solid/dashed boundaries and captions without hue dependence.

`publication/style-specimen.html` is a local self-contained layout specimen, excluded from public raw copying with the whole canonical folder. It has no tracking scripts because it is research material, not a new public site page. The final book uses the site's shared default/reader layouts and analytics contract.

## Print PDF

Target trim 170 × 240 mm; margins 22 mm inside, 18 mm outside, 19 mm top, 20 mm bottom. Body 10.8 pt with 1.48 leading; code minimum 8.5 pt. Actual renderer/font metrics decide line lengths and final page count. Never shrink a long listing indefinitely: select a shorter exact excerpt or wrap visually while preserving a downloadable unchanged listing. Keep captions with diagrams, repeat table headers and allow rows to break only where meaning remains clear. Front matter includes title/author/rights/preface/contents; numbered chapters follow stable IDs, appendices A–F retain IDs. Generate internal bookmarks and clickable cross-references, then inspect their destinations.

## Reflowable EPUB

No fixed paper dimensions, absolute-positioned body text or forced tiny type. Respect reader font settings; semantic headings and linked contents define navigation. Tables may need stacked definition lists on narrow readers. Give vectors an accessible text alternative and explanatory caption; inspect fallback rendering on an actual reader. Code uses readable relative sizing, safe wrapping or isolated scrolling supported by the reader. Record the final embedded fonts and licenses; do not fetch external fonts during ordinary build.

## Native online reader

The site is Jekyll + Tailwind, with generated book pages and a shared book reader. Reuse keyboard/no-JavaScript navigation, responsive content, local notes, text-size controls, per-section offline opt-in and existing full-text search. Do not transplant a separate WordPress/SPA shell. Keep code overflow inside the listing and tables inside a labeled region; preserve heading IDs and section order when rewriting links. Default layout supplies the single configured Google tag; chapter code never embeds a separate snippet.

## Diagrams and QA

Relationship diagrams use exact vector/code geometry with semantic node labels. An ownership diagram must distinguish process-local memory from external Docker effects; a dashed future DB/HA edge cannot look active. Provide a prose reading order for every diagram. No generated raster network diagram should substitute for precise source topology.

QA will render all PDF pages, inspect first/last page and every chapter/table/listing break at readable scale, validate bookmarks/links and embedded metadata, run EPUBCheck plus spine/media/link checks, and preview phone/tablet/desktop/light/dark/no-JavaScript native pages. This foundation created a specimen and static contrast calculation; it does not claim those final export/browser checks passed.
