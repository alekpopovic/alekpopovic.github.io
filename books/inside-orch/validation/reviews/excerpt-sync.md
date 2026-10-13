# Exact source and fragment review

Passed for the frozen corpus: 137 fenced blocks inventoried, 80 displayed exact/current or historical listings byte-compared, and all 157 excerpt metadata records checked against their specific Git objects. The inventory also retains 710 inline code references. Every exact listing has a full SHA, path, measured line interval, raw hash, displayed hash and explicitly recorded presentation transform. Both preceding and following immutable attributions are checked. Historical excerpts retain historical filenames and SHAs.

The checker classified every remaining block as a procedure, teaching configuration or illustrative response. All 54 shell fences passed actual Bash syntax checking; they were not executed as operations. YAML/JSON parsing establishes syntax only. Exact fragments retain surrounding package/import context through their pinned source file and the companion examples guide. No fragment is declared independently compilable.

Run `.venv/bin/python books/inside-orch/scripts/audit_book_examples.py --git-dir /tmp/inside-orch-reference-history.git` to reproduce extraction and stale-text diagnostics. Actual command evidence is `074-excerpt-post-copyedit-command.json` (with the earlier `074-excerpt-final-command.json` retained); the detailed result is `../excerpts/index.json`. No source patch, unsupported historical substitution or unidentified adaptation was needed. Technical behavior claims were not upgraded merely because their text matched.

Mechanical coverage is complete. The reviewer authored Chapters 1–8/33–40; independent reviewers cover those narratives separately. This review independently covered Chapters 17–24 and AppendixD, resolving the rollout's physical-stop-accounting overstatement with an exact audit. Byte equality does not establish runtime wiring, durable state or production fitness.

The final prose freeze was audited again on 2026-10-13 at 02:31:40 UTC. The new record binds the refreshed inventory to the current canonical text; existing program execution evidence remains unchanged.
