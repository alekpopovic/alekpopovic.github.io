import test from 'node:test';
import assert from 'node:assert/strict';
const { rankJobs } = await import(process.env.LAB_SOLUTION === '1' ? './solution.mjs' : './app.mjs');
test('larger numeric priorities come first, including multiple digits', () => {
  assert.deepEqual(rankJobs([{ priority: 2 }, { priority: 10 }, { priority: 1 }]).map(job => job.priority), [10, 2, 1]);
});
test('input order stays intact', () => {
  const jobs = [{ priority: 1 }, { priority: 2 }]; rankJobs(jobs);
  assert.deepEqual(jobs.map(job => job.priority), [1, 2]);
});
test('equal priorities retain their arrival order', () => {
  assert.deepEqual(rankJobs([{ id: 'first', priority: 3 }, { id: 'second', priority: 3 }]).map(job => job.id), ['first', 'second']);
});
test('negative, zero, and fractional priorities are numeric', () => {
  assert.deepEqual(rankJobs([{ priority: -1 }, { priority: 0.5 }, { priority: 0 }]).map(job => job.priority), [0.5, 0, -1]);
});
test('empty input produces a new empty array', () => {
  const jobs = []; assert.deepEqual(rankJobs(jobs), []); assert.notEqual(rankJobs(jobs), jobs);
});
