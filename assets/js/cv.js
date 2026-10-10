(() => {
  const print = document.querySelector('[data-cv-print]');
  if (!print) return;
  print.hidden = false;
  print.addEventListener('click', () => window.print());
})();
