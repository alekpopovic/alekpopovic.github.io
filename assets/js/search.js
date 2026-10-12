(() => {
  const missing = document.querySelector('#missing-query');
  if (missing && location.pathname !== '/404.html') {
    const segment = location.pathname.split('/').filter(Boolean).pop() || '';
    try { missing.value = decodeURIComponent(segment).replace(/\.html$/, '').replace(/[-_]/g, ' ').slice(0, 120); } catch { /* Keep the empty field for malformed URLs. */ }
  }
  const root = document.querySelector('[data-site-search]');
  if (!root) return;
  const form = root.querySelector('form');
  const query = root.querySelector('#site-query');
  const type = root.querySelector('#search-type');
  const book = root.querySelector('#search-book');
  const helper = window.CodepopSearch;
  if (!helper) return; // Keep the readable directory if enhancement cannot load.
  const results = root.querySelector('[data-search-results]');
  const status = root.querySelector('[data-search-status]');
  const more = root.querySelector('[data-search-more]');
  const normalize = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  let documents = [], matches = [], limit = 24, timer, ready = false;

  const readUrl = () => {
    const params = new URLSearchParams(location.search);
    query.value = (params.get('q') || '').slice(0, 120);
    book.value = [...book.options].some(option => option.value === params.get('book')) ? params.get('book') : '';
    type.value = [...type.options].some(option => option.value === params.get('type')) ? params.get('type') : 'all';
  };
  const draw = () => {
    const fragment = document.createDocumentFragment();
    for (const item of matches.slice(0, limit)) {
      const row = document.createElement('li');
      const link = document.createElement('a'); link.href = item.url;
      if (item.type === 'chapters' && query.value.trim()) { const url = new URL(item.url, location.origin); url.searchParams.set('find', query.value.trim()); link.href = url.pathname + url.search; }
      const label = document.createElement('span'); label.className = 'eyebrow'; label.textContent = `${item.type === 'chapters' ? 'Chapter' : item.type.replace(/s$/, '')} · ${item.label}`;
      const heading = document.createElement('h2'); heading.textContent = item.title;
      const text = document.createElement('p'); helper.highlight(text, helper.excerpt(item.text, query.value, item.description), query.value);
      link.append(label, heading, text); row.append(link); fragment.append(row);
    }
    results.replaceChildren(fragment);
    more.hidden = matches.length <= limit;
    status.textContent = matches.length ? `${matches.length} ${matches.length === 1 ? 'result' : 'results'}${query.value.trim() ? ` for “${query.value.trim()}”` : ' to explore'}${matches.length > limit ? ` · showing ${limit}` : ''}` : 'No results. Try fewer words, another topic, or choose Everything.';
  };
  const syncUrl = () => {
    const url = new URL(location.href); url.search = '';
    if (query.value.trim()) url.searchParams.set('q', query.value.trim());
    if (type.value !== 'all') url.searchParams.set('type', type.value);
    if (book.value) url.searchParams.set('book', book.value);
    history.replaceState(null, '', url);
  };
  const search = (updateUrl = true) => {
    if (!ready) return;
    const terms = normalize(query.value).trim().split(/\s+/).filter(Boolean).slice(0, 12);
    matches = documents.filter(item => (type.value === 'all' || item.type === type.value) && (!book.value || item.book_id === book.value) && terms.every(term => item.haystack.includes(term)))
      .map(item => ({ ...item, score: terms.reduce((score, term) => score + (item.heading.includes(term) ? 10 : 1), 0) }))
      .sort((a, b) => b.score - a.score || a.title.localeCompare(b.title));
    limit = 24;
    if (updateUrl) syncUrl();
    draw();
  };
  readUrl();
  root.querySelectorAll('[data-search-filter]').forEach(filter => { filter.hidden = false; });
  root.querySelector('[data-search-panel]').hidden = false;
  status.textContent = 'Loading the library…';
  fetch(root.dataset.index).then(response => {
    if (!response.ok) throw new Error('Search index unavailable');
    return response.json();
  }).then(index => {
    documents = index.map(item => ({ ...item, body: normalize(item.text), heading: normalize(item.title), haystack: normalize([item.title, item.description, item.label, item.text, (item.tags || []).join(' ')].join(' ')) }));
    ready = true;
    root.querySelector('[data-search-directory]').hidden = true;
    search(false);
  }).catch(() => { status.textContent = 'Search is temporarily unavailable. Browse the library below.'; });
  form.addEventListener('submit', event => { event.preventDefault(); clearTimeout(timer); search(); });
  query.addEventListener('input', () => { syncUrl(); clearTimeout(timer); timer = setTimeout(() => search(false), 180); });
  type.addEventListener('change', () => search());
  book.addEventListener('change', () => search());
  more.addEventListener('click', () => { limit += 24; draw(); });
  window.addEventListener('popstate', () => { clearTimeout(timer); readUrl(); search(false); });
})();
