(() => {
  const root = document.querySelector('[data-learning-path]');
  if (!root) return;
  const key = `codepop:learning:${root.dataset.learningPath}`;
  const boxes = [...root.querySelectorAll('[data-learning-step]')];
  const status = root.querySelector('[data-learning-status]');
  let saved = {}, available = true;
  try { const value = JSON.parse(localStorage.getItem(key)); if (value && typeof value === 'object' && !Array.isArray(value)) saved = value; } catch { available = false; }
  const update = () => {
    status.hidden = false;
    status.textContent = `${boxes.filter(box => box.checked).length} of ${boxes.length} steps completed. ${available ? 'Saved in this browser.' : 'Saving is unavailable; your checklist works for this visit.'}`;
  };
  for (const box of boxes) {
    box.checked = saved[box.dataset.learningStep] === true;
    box.closest('label').hidden = false;
    box.addEventListener('change', () => {
      saved[box.dataset.learningStep] = box.checked;
      try { localStorage.setItem(key, JSON.stringify(saved)); } catch { available = false; }
      if (box.checked) document.dispatchEvent(new CustomEvent('codepop:analytics', { detail: { name: 'learning_step_complete', props: { path_id: root.dataset.learningPath, step: Number(box.dataset.learningStep) + 1 } } }));
      update();
    });
  }
  update();
})();
