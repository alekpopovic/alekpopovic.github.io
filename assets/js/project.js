(() => {
  const root = document.querySelector('[data-project-walkthrough]');
  if (!root) return;
  const explanations = [...root.querySelectorAll('[data-project-explanations] li')].map(item => item.textContent);
  const buttons = [...root.querySelectorAll('[data-project-step]')];
  const output = root.querySelector('[data-project-output]');
  if (explanations.length !== buttons.length || !buttons.length) return;
  const select = button => {
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    output.textContent = explanations[Number(button.dataset.projectStep)];
  };
  root.querySelector('[data-project-steps]').hidden = false;
  root.querySelector('[data-project-explanations]').hidden = true;
  output.hidden = false; select(buttons[0]);
  buttons.forEach(button => button.addEventListener('click', () => select(button)));
})();
