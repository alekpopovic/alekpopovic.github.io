(() => {
  const reader = document.querySelector('[data-reader-book]');
  if (!reader) return;
  const workspace = reader.querySelector('[data-reader-study]');
  const button = reader.querySelector('[data-reader-study-open]');
  const bookmark = reader.querySelector('[data-reader-bookmark]');
  const complete = reader.querySelector('[data-reader-complete]');
  const note = reader.querySelector('#reader-note');
  const message = reader.querySelector('[data-study-status]');
  const panel = reader.querySelector('[data-reader-scroll]');
  const links = [...reader.querySelectorAll('.reader-chapters a')];
  const known = new Map(links.map(link => [new URL(link.href).pathname, link.textContent.trim()]));
  const key = `codepop:library:${reader.dataset.readerBook}`;
  let records = {}, available = true;
  try { const value = JSON.parse(localStorage.getItem(key)); if (value && typeof value === 'object' && !Array.isArray(value)) records = value; } catch { available = false; }
  // Reject corrupted or foreign URLs and bound values read from browser storage.
  for (const [url, entry] of Object.entries(records)) {
    if (!known.has(url) || !entry || typeof entry !== 'object' || Array.isArray(entry)) { delete records[url]; continue; }
    records[url] = { bookmarked: entry.bookmarked === true, completed: entry.completed === true, note: typeof entry.note === 'string' ? entry.note.slice(0, 10000) : '', anchor: typeof entry.anchor === 'string' && /^#[a-z0-9_%.-]+$/i.test(entry.anchor) ? entry.anchor : '' };
  }
  const current = () => records[location.pathname] ||= { bookmarked: false, completed: false, note: '', anchor: '' };
  const persist = text => {
    try { localStorage.setItem(key, JSON.stringify(records)); } catch { available = false; }
    message.textContent = available ? text : 'Saving is unavailable in this browser. Changes last for this visit; export your notes to keep them.';
  };
  const render = () => {
    const entry = current();
    bookmark.setAttribute('aria-pressed', String(entry.bookmarked));
    bookmark.textContent = entry.bookmarked ? 'Remove bookmark' : 'Bookmark this place';
    complete.checked = entry.completed;
    reader.querySelector('[data-study-progress]').textContent = `${Object.values(records).filter(value => value.completed).length} of ${known.size} sections completed.`;
    for (const link of links) {
      const done = records[new URL(link.href).pathname]?.completed === true;
      link.classList.toggle('chapter-completed', done);
      const old = link.querySelector('.chapter-completed-label');
      if (old) old.remove();
      if (done) { const label = document.createElement('span'); label.className = 'chapter-completed-label sr-only'; label.textContent = ' — completed'; link.append(label); }
    }
    const list = reader.querySelector('[data-reader-bookmarks]'); list.replaceChildren();
    for (const [url, value] of Object.entries(records)) {
      if (!value.bookmarked) continue;
      const item = document.createElement('li'), link = document.createElement('a');
      link.href = url + value.anchor; link.textContent = known.get(url); item.append(link); list.append(item);
    }
    if (!list.children.length) { const item = document.createElement('li'); item.textContent = 'No bookmarks yet.'; list.append(item); }
  };
  workspace.hidden = false; button.hidden = false;
  note.value = current().note; render();
  if (!available) persist('');
  button.addEventListener('click', () => {
    const contents = reader.querySelector('[data-reader-contents]');
    if (contents.getAttribute('aria-expanded') !== 'true') contents.click();
    workspace.open = true;
    workspace.scrollIntoView({ block: 'nearest' });
    note.focus({ preventScroll: true });
  });
  bookmark.addEventListener('click', () => {
    const entry = current(); entry.bookmarked = !entry.bookmarked;
    if (entry.bookmarked) {
      const headings = [...reader.querySelectorAll('.book-article :is(h1,h2,h3)[id]')];
      const heading = headings.filter(item => item.getBoundingClientRect().top <= panel.getBoundingClientRect().top + 80).at(-1);
      entry.anchor = heading ? `#${encodeURIComponent(heading.id)}` : '';
    }
    persist(entry.bookmarked ? 'This place is bookmarked.' : 'Bookmark removed.'); render();
  });
  complete.addEventListener('change', () => {
    current().completed = complete.checked;
    persist(complete.checked ? 'Section marked complete.' : 'Section marked incomplete.'); render();
    if (complete.checked) document.dispatchEvent(new CustomEvent('codepop:analytics', { detail: { name: 'chapter_complete', props: { book_id: reader.dataset.readerBook, chapter_slug: reader.dataset.readerChapter } } }));
  });
  let dirty = false;
  note.addEventListener('input', () => { dirty = true; message.textContent = 'Unsaved note. Use Save note to keep it.'; });
  const saveNote = () => { current().note = note.value; persist('Note saved on this device.'); dirty = false; };
  reader.querySelector('[data-reader-note-save]').addEventListener('click', saveNote);
  window.addEventListener('pagehide', () => { if (dirty) saveNote(); });
  document.addEventListener('visibilitychange', () => { if (document.hidden && dirty) saveNote(); });
  reader.querySelector('[data-reader-export]').addEventListener('click', () => {
    if (dirty) saveNote();
    const sections = Object.entries(records).filter(([, entry]) => entry.note || entry.bookmarked || entry.completed).map(([url, entry]) => `## ${known.get(url)}\n\n${url}${entry.anchor}\n\nCompleted: ${entry.completed ? 'yes' : 'no'}\nBookmarked: ${entry.bookmarked ? 'yes' : 'no'}\n\n${entry.note}\n`);
    const blob = new Blob([`# Reading notes: ${reader.dataset.readerBook}\n\n${sections.join('\n')}`], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob), link = document.createElement('a');
    link.href = url; link.download = `${reader.dataset.readerBook}-notes.md`; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    message.textContent = 'Notes exported as Markdown.';
  });
})();
