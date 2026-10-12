(() => {
  const root = document.querySelector('[data-reading-library]');
  if (!root) return;
  const catalog = JSON.parse(root.querySelector('[data-reading-catalog]').textContent);
  const books = new Map(catalog.books.map(book => [book.id, { ...book, sections: new Map(book.chapters.map(chapter => [chapter.url, chapter.title])) }]));
  const paths = new Map(catalog.paths.map(path => [path.id, path.steps]));
  const status = root.querySelector('[data-backup-status]');
  const preview = root.querySelector('[data-backup-preview]');
  const fileInput = root.querySelector('[data-backup-file]');
  const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
  const ensure = (condition, message) => { if (!condition) throw new Error(message); };
  const read = key => { const value = localStorage.getItem(key); return value === null ? null : JSON.parse(value); };
  const tell = message => { status.textContent = message; };
  let pending = null, generation = 0;
  // Only catalogued paths and bounded values can reach storage. Notes stay text.
  const validate = input => {
    ensure(object(input) && input.format === 'codepop-reading' && input.version === 1, 'Choose a supported CodePop reading backup (version 1).');
    ensure(object(input.books) && object(input.learning), 'The backup is missing its books or learning checklists.');
    const entries = new Map(); let sections = 0, notes = 0, checklists = 0;
    for (const [id, value] of Object.entries(input.books)) {
      const book = books.get(id);
      ensure(book && object(value) && object(value.records), 'The backup references an unknown book or invalid section data.');
      const records = {};
      for (const [url, entry] of Object.entries(value.records)) {
        ensure(book.sections.has(url) && object(entry), 'The backup references an unknown section.');
        ensure(typeof entry.note === 'string' && entry.note.length <= 10000 && typeof entry.bookmarked === 'boolean' && typeof entry.completed === 'boolean', 'A section has invalid notes or completion data.');
        ensure(typeof entry.anchor === 'string' && entry.anchor.length <= 200 && (!entry.anchor || /^#[a-z0-9_%.-]+$/i.test(entry.anchor)), 'A bookmark has an invalid heading.');
        records[url] = { note: entry.note, bookmarked: entry.bookmarked, completed: entry.completed, anchor: entry.anchor };
        sections++; if (entry.note) notes++;
      }
      entries.set(`codepop:library:${id}`, records);
      if (value.resume !== null && value.resume !== undefined) {
        const resume = value.resume;
        ensure(object(resume) && book.sections.has(resume.url) && Number.isFinite(resume.progress) && resume.progress >= 0 && resume.progress <= 1 && Number.isFinite(resume.updated) && resume.updated >= 0, 'A saved reading position is invalid.');
        entries.set(`codepop:reading:${id}`, { url: resume.url, title: book.sections.get(resume.url), progress: resume.progress, updated: resume.updated });
      }
    }
    for (const [id, value] of Object.entries(input.learning)) {
      ensure(paths.has(id) && object(value), 'The backup references an unknown learning path.');
      const steps = {};
      for (const [step, done] of Object.entries(value)) {
        ensure(/^(0|[1-9]\d*)$/.test(step) && Number(step) < paths.get(id) && typeof done === 'boolean', 'A learning checklist has an invalid step.');
        steps[step] = done;
      }
      entries.set(`codepop:learning:${id}`, steps); checklists++;
    }
    if (input.preferences !== null && input.preferences !== undefined) {
      const prefs = input.preferences;
      ensure(object(prefs) && ['small', 'regular', 'large', 'extra'].includes(prefs.size) && ['paper', 'light', 'dark'].includes(prefs.theme), 'Reading preferences are invalid.');
      entries.set('codepop:reader-preferences', { size: prefs.size, theme: prefs.theme });
    }
    return { entries, summary: `${Object.keys(input.books).length} books, ${sections} saved sections, ${notes} notes, and ${checklists} learning checklists.` };
  };
  const snapshot = () => {
    const data = { format: 'codepop-reading', version: 1, exported_at: new Date().toISOString(), books: {}, learning: {}, preferences: read('codepop:reader-preferences') };
    for (const [id] of books) {
      const records = read(`codepop:library:${id}`), resume = read(`codepop:reading:${id}`);
      if (records !== null || resume !== null) data.books[id] = { records: records || {}, resume };
    }
    for (const [id] of paths) { const steps = read(`codepop:learning:${id}`); if (steps !== null) data.learning[id] = steps; }
    validate(data); return data;
  };
  const render = () => {
    const shelf = root.querySelector('[data-reading-shelf]'); shelf.replaceChildren();
    for (const [id, book] of books) {
      const records = read(`codepop:library:${id}`) || {}, resume = read(`codepop:reading:${id}`);
      const values = object(records) ? Object.entries(records).filter(([url, entry]) => book.sections.has(url) && object(entry)).map(([, entry]) => entry) : [];
      const card = document.createElement('article'); card.className = 'learning-card';
      const heading = document.createElement('h3'), link = document.createElement('a'), details = document.createElement('p');
      link.href = book.url; link.textContent = book.title; heading.append(link);
      details.textContent = `${values.filter(entry => entry.completed === true).length} of ${book.sections.size} sections completed · ${values.filter(entry => entry.bookmarked === true).length} bookmarks · ${values.filter(entry => typeof entry.note === 'string' && entry.note).length} notes`;
      card.append(heading, details);
      if (object(resume) && book.sections.has(resume.url)) { const next = document.createElement('a'); next.href = `${resume.url}?resume=1`; next.textContent = `Continue: ${book.sections.get(resume.url)} →`; card.append(next); }
      shelf.append(card);
    }
  };
  root.querySelector('[data-backup-controls]').hidden = false;
  try { render(); tell('Your reading data stays in this browser. Download a backup to keep a separate copy.'); }
  catch { tell('Browser storage is unavailable or contains unreadable data. Existing reading controls and book downloads remain available.'); }
  root.querySelector('[data-backup-export]').addEventListener('click', () => {
    try {
      const data = snapshot(), blob = new Blob([JSON.stringify(data, null, 2) + '\n'], { type: 'application/json' });
      const url = URL.createObjectURL(blob), link = document.createElement('a');
      link.href = url; link.download = `codepop-reading-${new Date().toISOString().slice(0, 10)}.json`; link.click();
      setTimeout(() => URL.revokeObjectURL(url), 1000); tell('Reading backup downloaded. It includes the text of your saved notes.');
    } catch { tell('Could not export: storage is unavailable or saved data is invalid. Your existing data has not been changed.'); }
  });
  fileInput.addEventListener('change', async () => {
    const token = ++generation; pending = null; preview.hidden = true;
    try {
      const file = fileInput.files[0]; if (!file) return;
      ensure(file.size <= 10 * 1024 * 1024, 'Choose a backup smaller than 10 MB.');
      const candidate = validate(JSON.parse(await file.text()));
      if (token !== generation) return;
      pending = candidate; root.querySelector('[data-backup-summary]').textContent = candidate.summary;
      root.querySelector('[value="merge"]').checked = true;
      preview.hidden = false; root.querySelector('#backup-preview-title').focus(); tell('Backup checked. Review the restore options, then choose Restore this backup.');
    } catch (error) { if (token === generation) tell(error instanceof SyntaxError ? 'This file is not valid JSON. Nothing has been saved.' : `${error.message} Nothing has been saved.`); }
  });
  root.querySelector('[data-backup-cancel]').addEventListener('click', () => { generation++; pending = null; preview.hidden = true; fileInput.value = ''; fileInput.focus(); tell('Restore cancelled. Your saved data has not changed.'); });
  root.querySelector('[data-backup-import]').addEventListener('click', () => {
    if (!pending) return;
    const old = new Map(), written = [];
    try {
      const merge = root.querySelector('[name="backup-mode"]:checked').value === 'merge';
      const changes = [...pending.entries].map(([key, value]) => {
        const previous = localStorage.getItem(key); old.set(key, previous);
        if (merge && previous !== null) {
          const existing = JSON.parse(previous);
          ensure(object(existing), 'Existing data is unreadable; save a copy before replacing it.');
          value = key.startsWith('codepop:library:') || key.startsWith('codepop:learning:') ? { ...value, ...existing } : existing;
        }
        return [key, JSON.stringify(value)];
      });
      for (const [key, value] of changes) { localStorage.setItem(key, value); written.push(key); }
      pending = null; preview.hidden = true; fileInput.value = ''; render();
      tell('Backup restored on this device. Open a book or learning path to continue.'); root.querySelector('[data-backup-export]').focus();
    } catch {
      let recovered = true;
      for (const key of written.reverse()) { try { const value = old.get(key); if (value === null) localStorage.removeItem(key); else localStorage.setItem(key, value); } catch { recovered = false; } }
      tell(recovered ? 'Restore failed. Existing data was kept; storage may be full, unavailable, or unreadable. Keep your backup and try again.' : 'Restore stopped and some writes could not be undone. Keep your backup and review this device before trying again.');
    }
  });
  window.addEventListener('storage', () => { try { render(); } catch { tell('Could not refresh this device’s reading data.'); } });
})();
