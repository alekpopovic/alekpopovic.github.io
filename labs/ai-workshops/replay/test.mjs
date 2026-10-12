import test from 'node:test';
import assert from 'node:assert/strict';
const { recoverEvents } = await import(process.env.LAB_SOLUTION === '1' ? './solution.mjs' : './app.mjs');
const snapshot = { tenant_id: 'team-a', cursor: 10, positions: { van: 5 } };
const a = { tenant_id: 'team-a', seq: 11, event_id: 'a', subject_id: 'van', value: 6 };
const b = { tenant_id: 'team-a', seq: 12, event_id: 'b', subject_id: 'bike', value: 2 };
const reset = { status: 'resync', cursor: 10, positions: { van: 5 } };
test('a contiguous replay advances an independent snapshot', () => { assert.deepEqual(recoverEvents(snapshot, [a, b], 'team-a'), { status: 'ready', cursor: 12, positions: { van: 6, bike: 2 } }); });
test('an empty buffer preserves the snapshot cursor', () => { assert.deepEqual(recoverEvents(snapshot, [], 'team-a'), { status: 'ready', cursor: 10, positions: { van: 5 } }); });
test('the exact duplicate delivery is applied only once', () => { assert.deepEqual(recoverEvents(snapshot, [a, { ...a }, b], 'team-a'), { status: 'ready', cursor: 12, positions: { van: 6, bike: 2 } }); });
test('events already represented by the snapshot are ignored', () => { assert.deepEqual(recoverEvents(snapshot, [{ ...a, seq: 9, value: -1 }], 'team-a'), { status: 'ready', cursor: 10, positions: { van: 5 } }); });
test('a gap or out of order buffer requests a fresh snapshot', () => {
  for (const events of [[b], [b, a], [a, { ...b, seq: 13 }]]) assert.deepEqual(recoverEvents(snapshot, events, 'team-a'), reset);
});
test('cross tenant data never reaches a partial result', () => { assert.deepEqual(recoverEvents(snapshot, [a, { ...b, tenant_id: 'team-b' }], 'team-a'), reset); assert.throws(() => recoverEvents(snapshot, [], 'team-b')); });
test('reused delivery identities and malformed events require resync', () => {
  for (const events of [[a, { ...b, event_id: 'a' }], [{ ...a, seq: 11.5 }], [{ ...a, value: NaN }], [{ ...a, event_id: '' }]]) assert.deepEqual(recoverEvents(snapshot, events, 'team-a'), reset);
});
test('inputs and object prototypes remain unchanged', () => {
  const before = structuredClone(snapshot), events = [a, { ...b, subject_id: '__proto__' }], copy = structuredClone(events), result = recoverEvents(snapshot, events, 'team-a');
  assert.deepEqual(snapshot, before); assert.deepEqual(events, copy); assert.notEqual(result.positions, snapshot.positions); assert.equal(Object.getPrototypeOf(result.positions), Object.prototype); assert.equal(Object.hasOwn(result.positions, '__proto__'), true);
});
