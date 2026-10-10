# 13. Move live logs without hiding gaps


## Logs are streams with identity

A useful log protocol identifies organization, project, run, attempt, stream, and segment sequence. The attempt matters: a retry must not append into the previous attempt's output as if the two were one execution. Keep stdout and stderr either separately identified or explicitly framed in a combined stream.

Store bounded segments in object storage and their ownership, ordering, hash, size, and retention metadata in PostgreSQL. Do not insert one database row per arbitrary log line. The runner uses a bounded local spool and resumes from the last acknowledged sequence after reconnecting.

The laboratory's `LogStore` models a single stream. It accepts the next sequence, acknowledges identical retries, rejects conflicting bytes for an existing sequence, and refuses gaps. It copies input data rather than trusting the caller not to mutate a buffer later. Its memory quota is a teaching constraint; durable object storage needs a separate transaction and garbage-collection design.

## Commit metadata after durable bytes

An upload normally writes bytes to an attempt-scoped temporary object, verifies their hash and size, then finalizes the segment's metadata. Do not make metadata claim that a segment exists before the storage operation has met the selected durability contract. A failed metadata commit may leave an orphan object; collect it after a retention grace period rather than exposing it as accepted output.

A signed upload URL is a capability. Limit it to one scoped key, method, size policy, and short lifetime where the storage service supports those constraints. Validate ownership when finalizing. An old attempt must not obtain a path belonging to a newer attempt or another project.

When the spool fills, choose an explicit policy: block output consumption, terminate the job, or record an intentional truncation with a visible gap. Silent dropping is not acceptable. Backpressure itself can change process behavior, so the chosen policy belongs in the executor contract and tests.

## Separate transport from browser state

Server-Sent Events provides an event stream with identifiers and reconnection behavior, including a last-event identifier. It is a useful browser transport, but replay is still the application's responsibility. The stream format and browser behavior are specified by the HTML standard. [S14](e-sources.md#s14)

Send resumable cursors tied to the authorized stream. A browser reconnecting with an old cursor should receive the missing range or an explicit retention-expired response. Do not invent continuity when the requested logs have been deleted. Authorize the reconnect just as carefully as the first request.

Use a same-origin session strategy or a carefully scoped alternative for browser authentication. Avoid embedding durable bearer tokens into query strings that may appear in logs and history. Configure proxy buffering and idle timeouts intentionally, and test the deployed proxy path rather than only a direct development connection.

## Render repository-controlled output as data

Log text can contain HTML, terminal control sequences, misleading links, and enormous lines. Escape it, restrict any supported ANSI formatting, and provide a plain-text view. A line saying “click here to authorize deployment” is not part of the platform interface simply because a build printed it.

The browser should virtualize or page large outputs instead of holding every line in the DOM. Keep tail-following optional so the viewport does not jump while an operator reads an earlier error. Display truncation, missing segments, reconnecting state, and retention boundaries visibly.

Secret redaction must account for secrets split across transport chunks, but it is still a secondary defense. Never treat a redaction helper as permission to expose credentials to code that should not have them.

## Exercise

A runner retries segment 12 after a lost acknowledgement. The stored segment 12 has a different hash. Should the server overwrite it because the retry is more recent?

## Worked answer

No. The same segment identity must denote immutable bytes. Reject the conflict and preserve the original accepted segment. A mutable overwrite could corrupt evidence or let a stale process rewrite history. The runner should diagnose its spool or identity mismatch rather than assign new meaning to an existing sequence.

## Completion evidence

Test lost acknowledgements, duplicate segments, conflicting content, quota exhaustion, reconnect cursors, expired retention, browser escaping, and an object write that succeeds before metadata commit fails.
