# Continue existing work in the Claude edition

Prompt IDs and implementation targets are unchanged. A project already using the earlier
pack should keep its code, deployment configuration and evidence. This edition changes
the assistant entrypoints and instruction paths, not the Nginx protocol or architecture.

1. Install this edition into `docs/claude-pack/` without overwriting the old pack.
2. From the application repository root, preview progress import:

```bash
python3 docs/claude-pack/tools/import_progress.py --source docs/codex-pack/tracking/state.json --dry-run
python3 docs/claude-pack/tools/import_progress.py --source docs/codex-pack/tracking/state.json
```

3. If a previous handoff exists, read it and carry relevant context into the new handoff,
   changing current instruction paths to docs/claude-pack. The importer retains its source
   path as a reference but does not blindly copy potentially stale execution instructions.
4. Use RESUME_PROMPT.md. Claude must inspect actual code/evidence and reconcile status.

The importer requires matching project, count, ID order and titles; valid dependencies;
at most one in-progress task; and real nonempty evidence files for done tasks. Run it from
the app repository root so relative evidence paths resolve. It imports only into a pristine
pending tracker and creates a backup. It preserves status, evidence path, notes, timestamps
and source history while retaining the new edition's paths and effort metadata.

Missing evidence is reported rather than turning an old completion label into a verified pass.
Supply the original evidence or record the actual checks before retrying. Neither the
importer nor this new edition executes application tests by itself.
