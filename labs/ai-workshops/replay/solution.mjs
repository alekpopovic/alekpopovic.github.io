export function recoverEvents(snapshot, events, tenant) {
  const object = value => value && typeof value === 'object' && !Array.isArray(value);
  const text = value => typeof value === 'string' && value.length > 0;
  const cursor = value => Number.isSafeInteger(value) && value >= 0;
  if (!text(tenant) || !object(snapshot) || snapshot.tenant_id !== tenant || !cursor(snapshot.cursor) || !object(snapshot.positions) || !Array.isArray(events)) throw new Error('Invalid snapshot');
  if (Object.entries(snapshot.positions).some(([id, value]) => !text(id) || !Number.isFinite(value))) throw new Error('Invalid positions');
  const positions = { ...snapshot.positions }, seen = new Map(); let next = snapshot.cursor;
  const resync = () => ({ status: 'resync', cursor: snapshot.cursor, positions: { ...snapshot.positions } });
  for (const event of events) {
    if (!object(event) || event.tenant_id !== tenant || !cursor(event.seq) || !text(event.event_id) || !text(event.subject_id) || !Number.isFinite(event.value)) return resync();
    if (event.seq <= snapshot.cursor) continue;
    const identity = JSON.stringify([event.seq, event.subject_id, event.value]);
    if (seen.has(event.event_id)) { if (seen.get(event.event_id) !== identity) return resync(); continue; }
    if (event.seq !== next + 1) return resync();
    Object.defineProperty(positions, event.subject_id, { value: event.value, enumerable: true, writable: true, configurable: true });
    seen.set(event.event_id, identity); next = event.seq;
  }
  return { status: 'ready', cursor: next, positions };
}
