(() => {
  const root = document.querySelector('[data-learning-workspace]');
  if (!root) return;
  const catalog = JSON.parse(root.querySelector('[data-learning-catalog]').textContent);
  const object = value => value && typeof value === 'object' && !Array.isArray(value);
  const render = () => {
    let unavailable = false, unreadable = false, latest;
    const read = key => {
      let value;
      try { value = localStorage.getItem(key); } catch { unavailable = true; return null; }
      try { return value === null ? null : JSON.parse(value); } catch { unreadable = true; return null; }
    };
    for (const book of catalog.books) {
      const card = root.querySelector(`[data-workspace-book="${book.id}"]`), records = read(`codepop:library:${book.id}`), resume = read(`codepop:reading:${book.id}`);
      const values = book.chapters.map(chapter => object(records?.[chapter.url]) ? records[chapter.url] : {});
      card.querySelector('[data-workspace-detail]').textContent = `${values.filter(value => value.completed === true).length} of ${book.chapters.length} sections completed · ${values.filter(value => value.bookmarked === true).length} bookmarks · ${values.filter(value => typeof value.note === 'string' && value.note).length} notes`;
      const chapter = object(resume) && book.chapters.find(chapter => chapter.url === resume.url);
      if (chapter) {
        const link = card.querySelector('[data-workspace-link]'); link.href = `${chapter.url}?resume=1`; link.textContent = `Continue: ${chapter.title} →`;
        if (Number.isFinite(resume.updated) && (!latest || resume.updated > latest.updated)) latest = { updated: resume.updated, url: link.getAttribute('href'), title: chapter.title, detail: `Continue reading ${book.title}.` };
      }
    }
    for (const path of catalog.paths) {
      const card = root.querySelector(`[data-workspace-path="${path.id}"]`), steps = read(`codepop:learning:${path.id}`), answers = read(`codepop:knowledge:${path.id}`);
      const done = path.step_items.filter((_, index) => object(steps) && steps[index] === true).length;
      const answered = path.questions.filter(question => object(answers) && Number.isInteger(answers[question.id]) && answers[question.id] >= 0 && answers[question.id] < question.options).length;
      card.querySelector('[data-workspace-detail]').textContent = `${done} of ${path.steps} steps completed · ${answered} of ${path.questions.length} questions answered`;
      const next = path.step_items.findIndex((_, index) => !object(steps) || steps[index] !== true), link = card.querySelector('[data-workspace-link]');
      link.href = next >= 0 ? `${path.url}#learning-step-${next}` : `${path.url}#knowledge-title-${path.id}`;
      link.textContent = next >= 0 ? `Continue: ${path.step_items[next].title} →` : 'Revisit the knowledge check →';
      if (!latest && done > 0 && next >= 0) latest = { updated: -1, url: link.getAttribute('href'), title: path.step_items[next].title, detail: `Continue the ${path.title} learning path.` };
    }
    for (const workshop of catalog.workshops) {
      const card = root.querySelector(`[data-workspace-workshop="${workshop.id}"]`);
      let draft;
      try { draft = localStorage.getItem(`codepop:workshop:${workshop.id}`); } catch { unavailable = true; }
      const check = read(`codepop:workshop-check:${workshop.id}`), valid = typeof draft === 'string' && draft.length <= 40000;
      let detail = valid ? 'Draft saved on this device.' : 'No saved draft yet. Start with the failing example.';
      if (valid && object(check) && check.source === draft && Number.isInteger(check.total) && check.total > 0 && check.total <= 20 && Number.isInteger(check.passed) && check.passed >= 0 && check.passed <= check.total) detail += ` Last run: ${check.passed} of ${check.total} tests passed.`;
      else if (valid && object(check)) detail += ' Code changed since the last test run; run it again.';
      card.querySelector('[data-workspace-detail]').textContent = detail;
      card.querySelector('[data-workspace-link]').textContent = valid ? 'Continue your saved draft →' : 'Open the exercise →';
    }
    const next = root.querySelector('[data-workspace-next]'); next.hidden = unavailable;
    if (!unavailable) {
      const action = latest || { url: catalog.paths[0].url, title: 'Start with a guided learning path', detail: 'Choose a practical step, keep the evidence, and check your reasoning.' };
      const link = next.querySelector('[data-workspace-continue]'); link.href = action.url; link.textContent = `${action.title} →`;
      next.querySelector('[data-workspace-next-detail]').textContent = action.detail;
    }
    const status = root.querySelector('[data-workspace-status]'); status.hidden = false;
    status.textContent = unavailable ? 'Browser storage is unavailable. Open any material below; saved progress cannot be read on this visit.' : unreadable ? 'Some saved records could not be read. Valid records are shown; existing data has not been changed.' : 'Progress is read from this browser only. Open a card to continue; nothing is uploaded.';
  };
  render(); window.addEventListener('pageshow', render); window.addEventListener('storage', render);
})();
