import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const id = process.argv[2];
if (!['bugfix', 'review', 'tests', 'automation'].includes(id) || process.argv.slice(3).some(value => value !== '--solution')) {
  console.error('Usage: node verify.mjs <bugfix|review|tests|automation> [--solution]');
  process.exit(2);
}
const result = spawnSync(process.execPath, ['--test', fileURLToPath(new URL(`./${id}/test.mjs`, import.meta.url))], {
  stdio: 'inherit', env: { ...process.env, LAB_SOLUTION: process.argv.includes('--solution') ? '1' : '0' }, timeout: 10000,
});
process.exit(result.status ?? 1);
