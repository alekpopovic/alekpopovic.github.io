(() => {
  const controls = document.querySelector('[data-post-controls]');
  if (!controls) return;
  const cards = [...document.querySelectorAll('#posts-grid [data-post-card]')];
  const buttons = [...controls.querySelectorAll('[data-book-filter]')];
  const search = document.querySelector('#post-search');
  const category = document.querySelector('#post-category');
  const results = document.querySelector('#post-results');
  const reset = document.querySelector('[data-post-reset]');
  const empty = document.querySelector('[data-post-empty]');
  let book = '';
  const normalize = value => value.toLocaleLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
  const index = cards.map(card => ({ card, text: normalize(card.dataset.search) }));

  function update(writeUrl = true) {
    const terms = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
    let count = 0;
    index.forEach(({ card, text }) => {
      const matches = (!book || card.dataset.book === book) && (!category.value || card.dataset.category === category.value) && terms.every(term => text.includes(term));
      card.hidden = !matches;
      if (matches) count += 1;
    });
    buttons.forEach(button => {
      const active = button.dataset.bookFilter === book;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    const filtered = Boolean(book || category.value || terms.length);
    results.textContent = filtered ? `${count} of ${cards.length} notes found` : `${cards.length} notes to explore`;
    reset.hidden = !filtered;
    empty.hidden = count !== 0;
    if (writeUrl) {
      const url = new URL(window.location.href);
      [['q', search.value.trim()], ['book', book], ['category', category.value]].forEach(([key, value]) => value ? url.searchParams.set(key, value) : url.searchParams.delete(key));
      window.history.replaceState(null, '', url);
    }
  }

  function readUrl() {
    const params = new URLSearchParams(window.location.search);
    search.value = params.get('q') || '';
    const requestedBook = params.get('book') || '';
    book = buttons.some(button => button.dataset.bookFilter === requestedBook) ? requestedBook : '';
    const requestedCategory = params.get('category') || '';
    category.value = [...category.options].some(option => option.value === requestedCategory) ? requestedCategory : '';
    update(false);
  }
  function clear() { book = ''; search.value = ''; category.value = ''; update(); search.focus(); }
  buttons.forEach(button => button.addEventListener('click', () => { book = button.dataset.bookFilter; update(); }));
  search.addEventListener('input', () => update());
  category.addEventListener('change', () => update());
  reset.addEventListener('click', clear);
  document.querySelector('[data-post-clear]').addEventListener('click', clear);
  window.addEventListener('popstate', readUrl);
  readUrl();
  controls.hidden = false;
})();
