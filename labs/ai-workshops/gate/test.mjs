import test from 'node:test';
import assert from 'node:assert/strict';
const { deploymentGate } = await import(process.env.LAB_SOLUTION === '1' ? './solution.mjs' : './app.mjs');
const contract = { namespace: 'team-a', secret: 'demo-config', generation: 4 };
const observation = { namespace: 'team-a', secret: 'demo-config', available: true, observedGeneration: 4, observedResourceVersion: '42', currentResourceVersion: '42', satisfied: true };
test('fresh matching evidence permits the deployment', () => { assert.deepEqual(deploymentGate(contract, observation), { allowed: true, reason: 'satisfied' }); });
test('invalid contract identity and generation are rejected', () => {
  for (const input of [null, {}, { ...contract, namespace: '' }, { ...contract, secret: ' ' }, { ...contract, generation: 0 }, { ...contract, generation: 1.2 }]) assert.deepEqual(deploymentGate(input, observation), { allowed: false, reason: 'invalid-contract' });
});
test('missing and unavailable observations remain unknown', () => {
  for (const input of [null, {}, { ...observation, available: false }]) assert.deepEqual(deploymentGate(contract, input), { allowed: false, reason: 'unknown' });
});
test('evidence from a different namespace or secret is refused', () => {
  for (const input of [{ ...observation, namespace: 'team-b' }, { ...observation, secret: 'other-config' }]) assert.deepEqual(deploymentGate(contract, input), { allowed: false, reason: 'wrong-identity' });
});
test('an older generation is stale even when satisfied', () => { assert.deepEqual(deploymentGate(contract, { ...observation, observedGeneration: 3 }), { allowed: false, reason: 'stale' }); });
test('missing or changed resource versions invalidate old evidence', () => {
  for (const input of [{ ...observation, currentResourceVersion: '43' }, { ...observation, observedResourceVersion: '' }, { ...observation, currentResourceVersion: null }]) assert.deepEqual(deploymentGate(contract, input), { allowed: false, reason: 'stale' });
});
test('fresh negative evidence is unsatisfied, never a bypass', () => { assert.deepEqual(deploymentGate(contract, { ...observation, satisfied: false }), { allowed: false, reason: 'unsatisfied' }); });
test('output is static and inputs are preserved', () => {
  const input = { ...observation, raw_error: 'synthetic-secret-value', token: 'synthetic-token' }, before = structuredClone(input);
  assert.deepEqual(Object.keys(deploymentGate(contract, input)).sort(), ['allowed', 'reason']);
  assert.equal(JSON.stringify(deploymentGate(contract, input)).includes('synthetic'), false);
  assert.deepEqual(input, before); assert.deepEqual(contract, { namespace: 'team-a', secret: 'demo-config', generation: 4 });
});
