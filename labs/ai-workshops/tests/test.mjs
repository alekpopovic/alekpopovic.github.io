import test from 'node:test';
import assert from 'node:assert/strict';
const { retryDelay } = await import(process.env.LAB_SOLUTION === '1' ? './solution.mjs' : './app.mjs');
const now = Date.parse('Mon, 12 Oct 2026 10:00:00 GMT');
test('delay-seconds supports zero and whitespace', () => { assert.equal(retryDelay('0', now), 0); assert.equal(retryDelay(' 12 ', now), 12000); });
test('an HTTP date is relative to an injected clock', () => { assert.equal(retryDelay('Mon, 12 Oct 2026 10:00:05 GMT', now), 5000); });
test('a past HTTP date never creates negative waiting time', () => { assert.equal(retryDelay('Mon, 12 Oct 2026 09:59:59 GMT', now), 0); });
test('negative, fractional, partial, missing, and overflowing values are rejected', () => {
  for (const value of ['-1', '1.5', '12garbage', '', '9999999999999999999999', 'Mon, 30 Feb 2026 10:00:00 GMT', null]) assert.equal(retryDelay(value, now), null);
});
test('an invalid clock is rejected', () => { assert.equal(retryDelay('12', NaN), null); });
