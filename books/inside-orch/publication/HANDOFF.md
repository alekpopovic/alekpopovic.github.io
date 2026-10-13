# Inside orch — author handoff

The English edition and native Jekyll integration are ready for local review. **No push, pull request, default-branch change or live deployment was performed.** The selected manuscript rights are **All rights reserved**. The existing site checkout is on local branch `book/inside-orch-000`, based on `80801c8d3d97a4d8ff78e0fe69f3f902beda00c0`.

## Open and inspect

Local preview: **http://localhost:4000/books/inside-orch/** while the owned preview process is running. Online publication target, not a claim of deployment: `https://www.alekpopovic.com/books/inside-orch/`.

Ready files are in `books/inside-orch/dist/`: `inside-orch.pdf`, `inside-orch.epub`, `inside-orch.md`, `inside-orch-offline.zip`, `inside-orch-sources.zip`, `inside-orch-release.zip`, and `SHA256SUMS.txt`. The final ZIP includes the exact exports plus provenance, rights and review records. For a standalone reader, extract the offline ZIP and open `inside-orch/reader/index.html`.

The book contains a preface, 40 chapters and 6 appendices, 47 native reading sections, worked answers and 8 executed labs. Measured meaningful manuscript length is 101,211 words, excluding code/output and the separate lab guides; the PDF has 546 pages. The source is locked to `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`. See `edition-manifest.json` and `RELEASE_NOTES.md` for the exact identity and acceptance scope.

Minimal author review:

1. Verify the five hashes from the website root: `cd books/inside-orch/dist` then `sha256sum -c SHA256SUMS.txt`.
2. Read the preface and Chapters 5, 6, 17, 19, 30, 34 to review the most consequential implementation boundaries. Inspect the three new editorial posts, contents and downloads in the local reader.
3. Open the shipped PDF and EPUB; review the cover, title/rights pages, representative code/tables, bookmarks and reflow. All 546 PDF pages already have actual visual-review coverage and exact final-raster equivalence; EPUBCheck and a Chromium reading preview passed. Personal e-reader hardware compatibility has not been claimed.
4. Read the minor lab naming erratum below and the source/asset rights notices. Review the final gate and skeptical-reader reports before choosing whether and when to publish.
5. Follow `PUBLISH_CHECKLIST.md` in the canonical checkout for the next publication action. That later checklist and final tracker may postdate the frozen release snapshot; their absence from an earlier archive is not represented as a failed save or invented completion.

## Actual acceptance and limitations

`validation/RELEASE_GATE.md` and `validation/release-gate.json` passed for the exact final formats. `validation/reviews/final-independent-review.md` reconciles the developer, DevOps and architect lenses and records no remaining blocker. Reviewer authorship scopes are explicit; this is AI-assisted engineering review, not outside human endorsement.

Actual build and validation evidence covers npm/Jekyll, book links/posts/downloads, site metadata/analytics/search/feed/sitemap, content checks, browser/accessibility behavior, 20-route synthetic performance and offline reading. The full UI invocation retained 151 passes/one stale five-book assertion; the corrected six-book assertion passed in a focused rerun. Original database fixture failures and six external baseline skips remain recorded, alongside the separately passing full-schema teaching extension. See the gate and release notes rather than interpreting a single status as proof that every optional experiment ran.

Important application limits are explained in the book: default process-local state; unwired default persistence/HA/autoscaling; no global capacity reservation or partition fencing; missing ordinary runtime resource propagation; logical stop accounting before physical acknowledgement; partial GitOps; logical namespaces/local-volume limits. The book does not silently patch the application or certify its production fitness.

**Accepted minor erratum FINAL-OPS-001:** name every disposable database **`inside_orch_lab_<unique_run>_test`**. Prefix-only names pass the book precheck but fail safely in the immutable upstream reset test. Actual runs used the suffix. A later edition should strengthen the book guard and guide with a unit case. Never point a reset/restore procedure at production or a database you do not own.

The owned PostgreSQL lab container was removed and its absence verified; no unrelated resource was pruned. The static site preview is the intentionally retained local process. Lab privileges, fake-versus-real boundaries and optional unrun procedures are documented with their records.

## Snapshot and reproducibility contract

`REPRODUCE.md` explains the separate reader/source packages and tools. The editable source ZIP is the 095 snapshot. The outer final release adds the 096 gate, 097 reports, 098 freeze tool, release notes and this handoff as distinct members. Its tracker is the actual snapshot at assembly, with 098 still in progress and 099 pending; the canonical tracker is updated only after those tasks have real evidence. Do not describe the frozen ZIP as containing those later completion rows.

`publication/site-adapter/changes.patch` is the reviewed 095 source integration patch. Later gate/handoff files are present in the canonical local branch; the final publication checklist specifies the complete file set to review. Generated `book-pages/`, `assets/books/` and `_data/books.json` stay ignored. The pack does not replace root `AGENTS.md` or `README.md`.

Final archive encoding uses fixed metadata and repeat-byte checks. PDF rebuilding is not byte deterministic across every invocation/platform; the accepted final PDF's 546 raster pages and extracted content match the earlier reviewed build. Verify shipped hashes instead of rebuilding merely to inspect them. New source or format bytes require the affected acceptance checks again.

No local commit or public release is claimed here. Publishing is the author's next decision, with a concrete branch, exports, patch, PR draft and checks available for review.
