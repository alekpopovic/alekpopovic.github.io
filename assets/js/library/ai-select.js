(() => {
  const library = document.querySelector('[data-ai-library]');
  if (!library) return;
  const controls = [];
  for (const select of library.querySelectorAll('.ai-select select')) {
    const wrapper = select.parentElement, label = wrapper.querySelector('label');
    const options = [...select.options];
    const button = document.createElement('button'); button.type = 'button'; button.className = 'ai-select-trigger';
    button.setAttribute('role', 'combobox'); button.setAttribute('aria-haspopup', 'listbox'); button.setAttribute('aria-expanded', 'false');
    const value = document.createElement('span'); value.id = `${select.id}-value`; value.className = 'ai-select-value';
    const caret = document.createElement('span'); caret.className = 'ai-select-caret'; caret.setAttribute('aria-hidden', 'true');
    button.append(value, caret); button.setAttribute('aria-labelledby', `${label.id} ${value.id}`);
    const popup = document.createElement('div'); popup.id = `${select.id}-options`; popup.className = 'ai-select-popup'; popup.hidden = true;
    popup.setAttribute('role', 'listbox'); popup.setAttribute('aria-labelledby', label.id); button.setAttribute('aria-controls', popup.id);
    const rows = options.map((option, index) => {
      const row = document.createElement('div'); row.id = `${select.id}-option-${index}`; row.dataset.optionIndex = index; row.className = 'ai-select-option'; row.setAttribute('role', 'option');
      if (select.hasAttribute('data-ai-tool')) { const mark = document.createElement('span'); mark.className = 'ai-tool-mark'; mark.dataset.tool = option.value; mark.textContent = option.dataset.mark || '✳'; mark.setAttribute('aria-hidden', 'true'); row.append(mark); }
      const text = document.createElement('span'); text.textContent = option.textContent;
      const check = document.createElement('span'); check.className = 'ai-select-check'; check.textContent = '✓'; check.setAttribute('aria-hidden', 'true');
      row.append(text, check); popup.append(row); return row;
    });
    let active = select.selectedIndex, buffer = '', typedAt = 0;
    const closed = () => popup.hidden;
    const close = () => { popup.hidden = true; button.setAttribute('aria-expanded', 'false'); button.removeAttribute('aria-activedescendant'); wrapper.classList.remove('is-open'); buffer = ''; };
    const move = index => {
      active = Math.max(0, Math.min(options.length - 1, index));
      rows.forEach((row, index) => row.classList.toggle('is-active', index === active));
      button.setAttribute('aria-activedescendant', rows[active].id);
      rows[active].scrollIntoView({ block: 'nearest', behavior: 'instant' });
    };
    const sync = () => {
      value.textContent = options[select.selectedIndex].textContent;
      wrapper.classList.toggle('has-value', Boolean(select.value));
      rows.forEach((row, index) => { row.setAttribute('aria-selected', String(index === select.selectedIndex)); });
    };
    const open = () => {
      controls.forEach(control => control.close());
      const box = wrapper.getBoundingClientRect(), below = innerHeight - box.bottom - 16, above = box.top - 106;
      wrapper.dataset.side = below < 240 && above > below ? 'top' : 'bottom';
      popup.style.maxHeight = `${Math.max(100, Math.min(300, wrapper.dataset.side === 'top' ? above : below))}px`;
      popup.hidden = false; wrapper.classList.add('is-open'); button.setAttribute('aria-expanded', 'true'); move(select.selectedIndex);
    };
    const commit = (focus = true) => {
      const changed = select.selectedIndex !== active; select.selectedIndex = active; close(); sync();
      if (changed) select.dispatchEvent(new Event('change', { bubbles: true }));
      if (focus) button.focus({ preventScroll: true });
    };
    button.addEventListener('click', () => closed() ? open() : close());
    button.addEventListener('keydown', event => {
      if (event.ctrlKey || event.metaKey) return;
      if (event.key === 'Tab') { if (!closed()) commit(false); return; }
      if (event.key === 'Escape') { if (!closed()) { event.preventDefault(); event.stopPropagation(); close(); } return; }
      if (['Enter', ' ', 'ArrowDown', 'ArrowUp', 'Home', 'End', 'PageUp', 'PageDown'].includes(event.key)) {
        event.preventDefault();
        if (event.altKey && event.key === 'ArrowUp') { if (!closed()) commit(); return; }
        if (['Enter', ' '].includes(event.key)) { closed() ? open() : commit(); return; }
        const wasClosed = closed(); if (wasClosed) open();
        if (event.key === 'Home') move(0);
        else if (event.key === 'End') move(options.length - 1);
        else if (!wasClosed || event.key === 'ArrowUp') move(active + ({ ArrowDown: 1, ArrowUp: -1, PageDown: 10, PageUp: -10 }[event.key] || 0));
        return;
      }
      if (event.key.length === 1 && !event.altKey) {
        event.preventDefault(); if (closed()) open();
        const now = Date.now(); if (now - typedAt > 700) buffer = ''; typedAt = now; buffer += event.key.toLowerCase();
        const repeated = [...buffer].every(letter => letter === buffer[0]), prefix = repeated ? buffer[0] : buffer;
        const start = repeated ? active + 1 : 0;
        for (let n = 0; n < options.length; n++) { const index = (start + n) % options.length; if (options[index].textContent.toLowerCase().startsWith(prefix)) { move(index); break; } }
      }
    });
    button.addEventListener('blur', close);
    popup.addEventListener('pointerdown', event => event.preventDefault());
    popup.addEventListener('pointermove', event => { const row = event.target.closest('[data-option-index]'); if (row && Number(row.dataset.optionIndex) !== active) move(Number(row.dataset.optionIndex)); });
    popup.addEventListener('click', event => { const row = event.target.closest('[data-option-index]'); if (row) { active = Number(row.dataset.optionIndex); commit(); } });
    label.addEventListener('click', event => { event.preventDefault(); button.focus(); });
    select.addEventListener('change', sync);
    select.setAttribute('aria-hidden', 'true'); select.tabIndex = -1;
    wrapper.classList.add('ai-select-enhanced'); wrapper.append(button, popup); sync(); controls.push({ wrapper, close, sync });
  }
  library.addEventListener('codepop:filter-sync', () => controls.forEach(control => { control.close(); control.sync(); }));
  document.addEventListener('pointerdown', event => controls.forEach(control => { if (!control.wrapper.contains(event.target)) control.close(); }));
  window.addEventListener('resize', () => controls.forEach(control => control.close()));
})();
