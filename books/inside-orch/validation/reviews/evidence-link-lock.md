# Final evidence and link lock review

Source edition: `cbfc94ade5b57e449d6b73bf1485b1c5b1647022`. The canonical inventory is `evidence/link-lock.json`, produced by the reproducible offline checker `scripts/lock_book_links.py`. The final executed command is retained in `085-final-link-check-command.json`, with UTC boundaries, working directory, exit code zero and actual stdout/stderr.

The final inventory has 2,626 origin/destination entries and zero errors: 720 pinned source occurrences, 153 associated-commit links, 301 internal manuscript references, 678 EPUB internal targets/fragments, 734 actual clickable PDF URI annotations, two exact public download copies and 38 other reference occurrences. Every current/historical source object was read from the verified bare Git database; line intervals were checked against its actual bytes. All 157 exact excerpt comparisons pass. These comparisons include repeated metadata/registry references and do not mean 157 unique code excerpts.

All 91 original prompt IDs occur exactly once in the provenance mapping. The 66 associated implementation commits can support multiple requests. Retrospective early prompts, nine design prompts and batched late requests retain their distinct evidence relationships. Exact historical release tags match the mapping; no absent 0.2.0 tag is invented. Current `compose.yaml` and historical `docker-compose.yml` remain separately pinned.

LINK-001 found a real incorrect publication-design citation: `BRAND.md` lines 1–56, while the locked file has 52 lines. The publication owner corrected it to 1–52. The initial failure inventory remains retained. Subsequent passes find no invalid source interval, missing Git object, mutable source destination, missing local manuscript anchor or mismatched exact listing.

LINK-002 is resolved for the final export/link scope. The generated public copies exactly match the canonical artifacts:

- PDF: `42b18782ecb996e526f98e000c7dbf59533ee6200737f71f536bbf536c2de51c`.
- EPUB: `e5ba1daf5715b0daa064d53cec68512e243340ef16b3fc2976e245f674f0562b`.

Every inspected EPUB internal href/src destination and fragment exists. The PDF annotation count comes from the actual final document, not projected source links. Clickable annotations do not establish visual legibility or remote availability: all-page PDF inspection belongs to prompt 088, and actual EPUB reading preview belongs to 089. Their separate reports must bind these same artifact hashes.

The checker uses the publisher's real heading normalization, including chapter-stem H1 identifiers and duplicate-heading suffixes. It records its own checksum, manuscript/publication input checksums and final artifact checksums. Official background sources retain their previously recorded retrieval date and exact supported subject in the primary reference register. Other external destinations explicitly remain `not_checked_offline`; this command makes no HTTP requests. Local Git proof does not imply public network reachability.

Original and intermediate records remain available, including author-in-progress missing paths, the incorrect BRAND interval and an internal checker variable-shadowing failure corrected before the final successful run. None is rewritten as a passing execution. The fresh package-integrity command also passed the immutable corpus gate. Structural/link checks support inspectable attribution and reproducibility; technical semantics, visual quality and live-site readiness retain their independent review gates. No deployment or push was performed.

Final546pagePDF rebind passed with the unchanged EPUB at03:40UTC; actual command metadata is `085-final-546-link-check-command.json`. Earlier artifact checks remain historical records.

Final audited NOTICE and accepted546page PDF were rebound again at04:00UTC. Exact PDF SHA256 is `a734dd82a27fde589fd81cf9755693401f8b1abbe9a055d1ebe2e482916caee3`; EPUB remains `e5ba1daf5715b0daa064d53cec68512e243340ef16b3fc2976e245f674f0562b`. The current inventory contains 2632 links and zero errors. Actual metadata: `085-final-notice-pdf-rebind-command.json`.
