(() => {
  const library = document.querySelector('[data-ai-library]');
  if (!library) return;
  const cards = [...library.querySelectorAll('[data-post-card]')];
  const categories = [...library.querySelectorAll('[data-ai-category]')];
  const search = library.querySelector('[data-ai-search]');
  const tools = library.querySelector('[data-ai-tool]');
  const extra = ['environment', 'format', 'level'].map(name => ({ name, select: library.querySelector(`[data-ai-${name}]`) }));
  const results = library.querySelector('[data-ai-results]');
  const reset = library.querySelector('[data-ai-reset]');
  const empty = library.querySelector('[data-ai-empty]');
  const normalize = value => value.toLocaleLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
  const index = cards.map(card => ({ card, text: normalize(card.dataset.search) }));
  let category = '';

  function update(writeUrl = true) {
    const terms = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
    let count = 0;
    index.forEach(({ card, text }) => {
      const matches = (!category || card.dataset.category === category) && (!tools.value || card.dataset.tool === tools.value) && extra.every(({ name, select }) => !select.value || (name === 'environment' ? card.dataset.environments.split(' ').includes(select.value) : card.dataset[name] === select.value)) && terms.every(term => text.includes(term));
      card.hidden = !matches;
      if (matches) count += 1;
    });
    categories.forEach(button => {
      const active = button.dataset.aiCategory === category;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    const filtered = Boolean(category || tools.value || terms.length || extra.some(item => item.select.value));
    results.textContent = filtered ? `${count} of ${cards.length} guides found` : `${cards.length} guides to explore`;
    reset.hidden = !filtered;
    empty.hidden = count > 0;
    if (writeUrl) {
      const url = new URL(location.href);
      [['q', search.value.trim()], ['tool', tools.value], ['category', category], ...extra.map(item => [item.name, item.select.value])].forEach(([key, value]) => value ? url.searchParams.set(key, value) : url.searchParams.delete(key));
      history.replaceState(null, '', url);
    }
    library.dispatchEvent(new Event('codepop:filter-sync'));
  }
  function readUrl() {
    const params = new URLSearchParams(location.search);
    search.value = (params.get('q') || '').slice(0, 120);
    const requested = params.get('category') || '';
    category = categories.some(button => button.dataset.aiCategory === requested) ? requested : '';
    const tool = params.get('tool') || '';
    tools.value = [...tools.options].some(option => option.value === tool) ? tool : '';
    extra.forEach(({ name, select }) => { const value = params.get(name) || ''; select.value = [...select.options].some(option => option.value === value) ? value : ''; });
    update(false);
  }
  function clear() { category = ''; tools.value = ''; search.value = ''; extra.forEach(item => { item.select.value = ''; }); update(); search.focus(); }
  categories.forEach(button => button.addEventListener('click', () => { category = button.dataset.aiCategory; update(); }));
  search.addEventListener('input', () => update());
  tools.addEventListener('change', () => update());
  extra.forEach(item => item.select.addEventListener('change', () => update()));
  reset.addEventListener('click', clear);
  library.querySelector('[data-ai-clear]').addEventListener('click', clear);
  window.addEventListener('popstate', readUrl);
  readUrl();
  library.querySelectorAll('[data-ai-controls]').forEach(control => { control.hidden = false; });
})();
