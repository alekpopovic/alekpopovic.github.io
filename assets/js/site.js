(() => {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.main-nav');
  const mobile = window.matchMedia('(max-width: 980px)');
  if (!toggle || !nav) return;

  const setOpen = (open, returnFocus = false) => {
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    if (returnFocus) toggle.focus();
  };

  toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true'));
  nav.addEventListener('click', event => { if (event.target.closest('a')) setOpen(false); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') setOpen(false, true);
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) setOpen(false);
  });
  mobile.addEventListener('change', () => setOpen(false));

  const header = document.querySelector('.site-header');
  const footer = document.querySelector('.site-footer');
  let framePending = false;
  const updateHeader = () => {
    header.classList.toggle('is-scrolled', window.scrollY > 32);
    header.classList.toggle('is-on-blue', footer.getClientRects().length > 0 && footer.getBoundingClientRect().top < 80);
    framePending = false;
  };
  window.addEventListener('scroll', () => {
    if (!framePending) {
      framePending = true;
      requestAnimationFrame(updateHeader);
    }
  }, { passive: true });
  window.addEventListener('resize', updateHeader);
  updateHeader();

})();
