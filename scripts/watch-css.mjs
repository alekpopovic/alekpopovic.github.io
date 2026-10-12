import fs from 'node:fs';
import { spawn } from 'node:child_process';
const files = ['src', '_layouts', '_includes', '_posts', '_data', 'book-pages', 'assets/js', 'learn', 'ai', 'projects', 'codepop', 'newsletter'];
let timer, running = false, pending = false;
const build = () => {
  if (running) { pending = true; return; }
  running = true;
  const child = spawn(process.execPath, ['scripts/build-css.mjs'], { stdio: 'inherit' });
  child.on('exit', () => { running = false; if (pending) { pending = false; build(); } });
};
const changed = () => { clearTimeout(timer); timer = setTimeout(build, 200); };
for (const file of files) if (fs.existsSync(file)) fs.watch(file, { recursive: true }, changed);
fs.watch('.', (_, name) => { if (name?.endsWith('.html') || name === 'tailwind.config.js') changed(); });
build();
