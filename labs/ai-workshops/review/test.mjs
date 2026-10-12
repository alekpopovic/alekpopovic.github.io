import test from 'node:test';
import assert from 'node:assert/strict';
const { requestEvent } = await import(process.env.LAB_SOLUTION === '1' ? './solution.mjs' : './app.mjs');
const request = { method: 'GET', url: '/books?token=sample-private-value#private', status: 200, duration_ms: 12,
  headers: { authorization: 'Bearer sample-token', cookie: 'session=sample-cookie' }, body: { email: 'example@example.invalid' } };
test('the event uses an explicit field contract', () => {
  assert.deepEqual(Object.keys(requestEvent(request)).sort(), ['duration_ms', 'event', 'method', 'path', 'status']);
});
test('only the route path is retained', () => { assert.equal(requestEvent(request).path, '/books'); });
test('credentials and body are absent from serialized output', () => {
  const text = JSON.stringify(requestEvent(request));
  for (const secret of ['sample-private-value', 'sample-token', 'sample-cookie', 'example@example.invalid']) assert.equal(text.includes(secret), false);
});
test('unknown future fields stay out of the event', () => { assert.equal('new_sensitive_field' in requestEvent({ ...request, new_sensitive_field: 'private' }), false); });
test('building the event does not mutate the request', () => {
  const before = structuredClone(request); requestEvent(request); assert.deepEqual(request, before);
});
