(() => {
  const reader = document.querySelector('[data-reader-book]');
  if (!reader || !window.CodepopSearch) return;
  const helper = window.CodepopSearch, article = reader.querySelector('.book-article');
  const panel = reader.querySelector('[data-reader-assist]'), input = reader.querySelector('#reader-find-query');
  const status = reader.querySelector('[data-reader-find-status]'), previous = reader.querySelector('[data-reader-find-prev]'), next = reader.querySelector('[data-reader-find-next]');
  let marks = [], position = -1, indexPromise, generation = 0;
  panel.hidden = false;
  reader.querySelector('[data-reader-find-open]').addEventListener('click', () => {
    if (reader.querySelector('.reader-sidebar').hidden) reader.querySelector('[data-reader-contents]').click();
    panel.open = true; input.focus();
  });
  const clear = () => { for (const mark of marks) mark.replaceWith(document.createTextNode(mark.textContent)); article.normalize(); marks = []; position = -1; previous.disabled = next.disabled = true; };
  const jump = step => {
    if (!marks.length) return;
    marks[position]?.removeAttribute('data-current'); position = (position + step + marks.length) % marks.length;
    marks[position].dataset.current = 'true'; marks[position].scrollIntoView({ block: 'center', behavior: 'instant' });
    status.textContent = `${position + 1} of ${marks.length} matches${marks.length === 500 ? ' (first 500)' : ''} in this section.`;
  };
  const find = () => {
    clear(); const query = input.value.trim();
    if (!query) { status.textContent = 'Enter a word or phrase to find in this section.'; return; }
    const walker = document.createTreeWalker(article, NodeFilter.SHOW_TEXT), nodes = []; let node;
    while ((node = walker.nextNode())) if (!node.parentElement.closest('script,style,button,svg')) nodes.push(node);
    for (const text of nodes) {
      if (marks.length >= 500) break;
      if (!helper.ranges(text.textContent, query).length) continue;
      const fragment = document.createDocumentFragment(); helper.highlight(fragment, text.textContent, query);
      const added = [...fragment.querySelectorAll('mark')], room = 500 - marks.length;
      for (const overflow of added.slice(room)) overflow.replaceWith(document.createTextNode(overflow.textContent));
      marks.push(...added.slice(0, room));
      text.replaceWith(fragment);
    }
    previous.disabled = next.disabled = marks.length === 0;
    if (marks.length) jump(1); else status.textContent = 'No matches in this section. Try searching the whole book.';
  };
  reader.querySelector('[data-reader-find-form]').addEventListener('submit', event => { event.preventDefault(); find(); });
  previous.addEventListener('click', () => jump(-1)); next.addEventListener('click', () => jump(1));
  reader.querySelector('[data-reader-find-clear]').addEventListener('click', () => { clear(); input.value = ''; status.textContent = 'Highlights cleared.'; reader.querySelector('[data-reader-book-results]').replaceChildren(); reader.querySelector('[data-reader-book-status]').textContent = ''; generation++; input.focus(); });
  reader.querySelector('[data-reader-book-search]').addEventListener('click', async () => {
    const query = input.value.trim(), token = ++generation, output = reader.querySelector('[data-reader-book-results]'), message = reader.querySelector('[data-reader-book-status]'); output.replaceChildren();
    if (!query) { message.textContent = 'Enter a word or phrase first.'; input.focus(); return; }
    message.textContent = 'Searching this book…';
    try {
      if (!indexPromise) indexPromise = fetch(reader.dataset.searchIndex).then(response => { if (!response.ok) throw new Error(); return response.json(); }).catch(error => { indexPromise = null; throw error; });
      const index = await indexPromise; if (token !== generation) return;
      const terms = helper.terms(query), matches = index.filter(item => item.type === 'chapters' && item.book_id === reader.dataset.readerBook && terms.every(term => helper.normalize(`${item.title} ${item.text}`).includes(term)));
      for (const item of matches.slice(0, 12)) {
        const row = document.createElement('li'), link = document.createElement('a'), snippet = document.createElement('p');
        const url = new URL(item.url, location.origin); url.searchParams.set('find', query); link.href = url.pathname + url.search; link.textContent = item.title;
        helper.highlight(snippet, helper.excerpt(item.text, query), query); row.append(link, snippet); output.append(row);
      }
      message.textContent = matches.length ? `${matches.length} matching sections${matches.length > 12 ? ' · first 12 shown; narrow your search for more' : ''}. Open a result to highlight its text.` : 'No sections match all these words. Try fewer or different words.';
    } catch { if (token === generation) message.textContent = 'Book search is unavailable. Try again when online; section search still works.'; }
  });
  const requested = new URLSearchParams(location.search).get('find');
  if (requested) { input.value = requested.slice(0, 120); panel.open = true; requestAnimationFrame(find); }
  // Native dialog supplies keyboard focus containment and Escape-to-close.
  const dialog = document.createElement('dialog'); dialog.className = 'reader-figure-dialog'; dialog.setAttribute('aria-label', 'Expanded book figure');
  const title = document.createElement('h2'); title.textContent = 'Figure viewer';
  const close = document.createElement('button'); close.type = 'button'; close.className = 'study-button'; close.textContent = 'Close figure';
  const zoomLabel = document.createElement('label'); zoomLabel.textContent = 'Figure size'; const zoom = document.createElement('input'); zoom.type = 'range'; zoom.min = '100'; zoom.max = '300'; zoom.step = '25'; zoom.value = '100'; zoomLabel.append(zoom);
  const viewport = document.createElement('div'); viewport.className = 'reader-figure-viewport'; const image = document.createElement('img'); viewport.append(image);
  dialog.append(title, close, zoomLabel, viewport); reader.append(dialog);
  close.addEventListener('click', () => dialog.close()); dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  zoom.addEventListener('input', () => { image.style.width = `${zoom.value}%`; });
  for (const figure of article.querySelectorAll('img')) {
    const button = document.createElement('button'); button.type = 'button'; button.className = 'study-button reader-figure-open'; button.textContent = 'Expand figure ↗'; button.setAttribute('aria-label', `Expand figure: ${figure.alt || 'book diagram'}`); figure.after(button);
    button.addEventListener('click', () => { image.src = figure.currentSrc || figure.src; image.alt = figure.alt; title.textContent = figure.alt || 'Book figure'; zoom.value = '100'; image.style.width = '100%'; dialog.showModal(); });
  }
})();
