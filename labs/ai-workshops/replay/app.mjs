// Teaching fixture: applying every message trusts order and identity too early.
export function recoverEvents(snapshot, events, tenant) {
  const positions = { ...snapshot.positions };
  for (const event of events) positions[event.subject_id] = event.value;
  return { status: 'ready', cursor: events.at(-1)?.seq ?? snapshot.cursor, positions };
}
