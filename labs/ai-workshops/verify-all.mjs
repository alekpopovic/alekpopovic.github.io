import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

let failures = 0;
for (const id of ['bugfix', 'review', 'tests', 'automation', 'gate', 'replay']) {
  for (const solution of [false, true]) {
    const result = spawnSync(process.execPath, [fileURLToPath(new URL('./verify.mjs', import.meta.url)), id, ...(solution ? ['--solution'] : [])], { encoding: 'utf8', timeout: 12000 });
    const passed = solution ? result.status === 0 : result.status === 1 && result.stdout.includes('ERR_ASSERTION');
    console.log(`${id}: ${solution ? 'solution passes' : 'starter fails assertions'} — ${passed ? 'OK' : 'FAILED'}`);
    if (!passed) { failures++; console.error(result.error || '', result.stdout, result.stderr); }
  }
}
process.exitCode = failures ? 1 : 0;
