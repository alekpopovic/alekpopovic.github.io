# 20. Build an operator interface that explains state


## The dashboard is a diagnostic tool

A useful dashboard answers why work is waiting, what is currently executing, what changed, and what needs an operator decision. It should not only rank recent failures. The most valuable first screen may be a clear distinction between no eligible runner, exhausted capacity, missing approval, and uncertain deployment state.

Use Angular as a client of the versioned server API, not as an alternate policy engine. Organize features around projects, runs, runner pools, artifacts, environments, and administration. Keep generated contract types separate from presentation models and record the schema receipt described in Chapter 4.

Angular Signals provides reactive state primitives; the framework documentation explains how values and derived state are tracked. Use them for view state where appropriate, without mixing transport replay rules into arbitrary component side effects. [S12](e-sources.md#s12)

## Snapshot first, ordered events second

Load an authorized snapshot with a revision or cursor, then subscribe to changes after that point. Without a consistent boundary, an event can arrive between the initial GET and the stream connection and disappear from the screen.

Apply events only when their identity and ordering match the current subscription. Duplicate events should be harmless. If the browser detects a gap or an unsupported event version, refresh the snapshot rather than guessing what state was missed. Switching projects must close the old subscription and clear sensitive view state.

The API remains authoritative. A Cancel button can optimistically display “requesting cancellation,” but it should not invent the terminal state before confirmation. An approval form should show the exact subject being approved and detect if it changed while the dialog was open.

## Give large data a bounded presentation

Use pagination for history and server-side filters for large run sets. Use a virtualized or paged log view rather than adding every line to the DOM. Preserve selection, scroll position, and the user's decision to stop following live output.

The pipeline graph needs a keyboard-readable alternative, such as a job table with dependencies, state, and reason. Do not rely only on color to convey outcomes. A screen-reader label should distinguish failed, cancelled, blocked, and uncertain states instead of saying “red node.”

Timestamps should reveal the timezone and offer exact values. Show duration separately from wall-clock time. Distinguish queued time, execution time, and time spent awaiting approval so the product does not blame the runner for a human decision delay.

## Treat output as untrusted text

Repository names, branch names, commit messages, report text, and logs can contain hostile markup. Angular's security guidance describes escaping, sanitization, and the risks of bypassing trust protections. Avoid inserting raw build output into HTML or using bypass APIs merely to preserve formatting. [S13](e-sources.md#s13)

Use narrowly controlled rendering for any supported ANSI styles. External links should be visibly external, with an intentional navigation policy. Error messages returned by the server should not expose stack traces, SQL, credential material, or internal target URLs to an unauthorized viewer.

Access checks belong on every server endpoint. Client route guards improve navigation but do not establish security. Test direct API calls independently of what the interface chooses to display.

## Design interruption as a normal state

A reconnecting banner should say whether data may be stale and when it was last confirmed. A deleted artifact should display the retention reason if available, not a generic unexpected error. An inaccessible project should clear cached content after access revocation.

When an action fails, preserve the operator's context. A failed deployment approval should not send the user back to a blank dashboard. Show the failure and the current subject so the next decision can be deliberate.

## Exercise

The web page receives events 201 and 203 but never 202. Event 203 says the run succeeded. Should the client simply advance its cursor to 203?

## Worked answer

Not unless the protocol explicitly makes event 203 a complete authoritative snapshot. With incremental events, the missing update may contain a critical state transition or resource change. Detect the gap and refresh from an authorized snapshot or replay endpoint. The browser must not manufacture a coherent history from incomplete data.

## Completion evidence

Test event gaps, duplicate events, revocation during a session, escaped output, large logs, keyboard navigation, exact approval subjects, and reconnection through the actual production proxy path. This book contains the design, not a compiled Angular application.
