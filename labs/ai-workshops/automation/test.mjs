import test from 'node:test';
import assert from 'node:assert/strict';
const { releaseManifest } = await import(process.env.LAB_SOLUTION === '1' ? './solution.mjs' : './app.mjs');
const artifact = name => ({ name, sha256: 'A'.repeat(64), size: 42 });
test('manifest fields are fixed and output order is deterministic', () => {
  assert.deepEqual(releaseManifest([artifact('z.zip'), artifact('a.zip')]), { version: 1, files: [{ ...artifact('a.zip'), sha256: 'a'.repeat(64) }, { ...artifact('z.zip'), sha256: 'a'.repeat(64) }] });
});
test('equivalent input orders produce byte-identical JSON', () => {
  assert.equal(JSON.stringify(releaseManifest([artifact('a'), artifact('b')])), JSON.stringify(releaseManifest([artifact('b'), artifact('a')])));
});
test('duplicate names and paths are rejected', () => {
  assert.throws(() => releaseManifest([artifact('a'), artifact('a')]));
  for (const name of ['../secret', '/absolute', 'folder/file']) assert.throws(() => releaseManifest([artifact(name)]));
});
test('invalid hashes and byte sizes are rejected', () => {
  assert.throws(() => releaseManifest([{ ...artifact('a'), sha256: 'not-a-hash' }]));
  for (const size of [0, -1, 1.5, Infinity]) assert.throws(() => releaseManifest([{ ...artifact('a'), size }]));
});
test('input order and unknown input fields are not persisted', () => {
  const list = [{ ...artifact('z'), internal: 'private' }, artifact('a')], before = structuredClone(list);
  const result = releaseManifest(list); assert.deepEqual(list, before); assert.equal('internal' in result.files[1], false);
});
