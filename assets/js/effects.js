// Optional decoration: content is visible before this script and without it.
(() => {
  if (document.body.classList.contains('book-reading-page')) return;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const precise = window.matchMedia('(hover: hover) and (pointer: fine)');
  // Saturated project cards retain their original contrast and lift/rotate hover.
  const surfaces = [...document.querySelectorAll('.post-card, .feature-card, .discovery-card, .cv-skills article, .ai-console')];
  const scenes = [...document.querySelectorAll('[data-scene]')];
  surfaces.forEach(element => element.classList.add('effect-surface'));
  const seen = new WeakSet();
  const animations = new Set();
  let observer, listeners;
  let cleanups = [];

  const stop = () => {
    observer?.disconnect();
    listeners?.abort();
    animations.forEach(animation => animation.cancel());
    animations.clear();
    cleanups.forEach(cleanup => cleanup());
    cleanups = [];
  };

  const trackPointer = (element, scene = false) => {
    let frame = 0, clientX = 0, clientY = 0;
    const reset = () => {
      cancelAnimationFrame(frame);
      frame = 0;
      element.classList.remove('is-lit');
      ['--light-x', '--light-y', '--scene-x', '--scene-y', '--scene-turn'].forEach(name => element.style.removeProperty(name));
    };
    cleanups.push(reset);
    element.addEventListener('pointermove', event => {
      if (event.pointerType !== 'mouse' && event.pointerType !== 'pen') return;
      clientX = event.clientX;
      clientY = event.clientY;
      if (frame) return;
      frame = requestAnimationFrame(() => {
        frame = 0;
        const rect = element.getBoundingClientRect();
        if (!rect.width || !rect.height) return;
        const x = Math.max(0, Math.min(clientX - rect.left, rect.width));
        const y = Math.max(0, Math.min(clientY - rect.top, rect.height));
        if (scene) {
          element.style.setProperty('--scene-x', `${(x / rect.width - .5) * 14}px`);
          element.style.setProperty('--scene-y', `${(y / rect.height - .5) * 10}px`);
          element.style.setProperty('--scene-turn', `${(x / rect.width - .5) * 3}deg`);
        } else {
          element.style.setProperty('--light-x', `${x}px`);
          element.style.setProperty('--light-y', `${y}px`);
          element.classList.add('is-lit');
        }
      });
    }, { passive: true, signal: listeners.signal });
    element.addEventListener('pointerleave', reset, { signal: listeners.signal });
  };

  const start = () => {
    stop();
    if (reduced.matches) return;
    listeners = new AbortController();
    if ('IntersectionObserver' in window && typeof Element.prototype.animate === 'function') {
      observer = new IntersectionObserver(entries => {
        if (reduced.matches) return;
        let order = 0;
        entries.forEach(({ target, isIntersecting }) => {
          if (!isIntersecting || target.closest('[hidden]')) return;
          observer.unobserve(target);
          seen.add(target);
          if (target.contains(document.activeElement)) return;
          const animation = target.animate([
            { opacity: .65, translate: '0 22px' },
            { opacity: 1, translate: '0 0' },
          ], { duration: 540, delay: Math.min(order++, 3) * 55, easing: 'cubic-bezier(.2,.7,.2,1)' });
          animations.add(animation);
          animation.finished.then(() => animations.delete(animation), () => animations.delete(animation));
        });
      }, { threshold: .08, rootMargin: '0px 0px -24px 0px' });
      document.querySelectorAll('.section-heading, .section-top, .book-feature > *, .feature-card, .work-card, .post-card, .discovery-heading, .discovery-card, .process-step, .cv-skills article, .ai-tool-strip a, .ai-bottom-note').forEach(element => {
        if (seen.has(element)) return;
        // Never animate the initial view, a restored position, or the LCP heading.
        if (element.getClientRects().length && element.getBoundingClientRect().top < window.innerHeight * .95) {
          seen.add(element);
        } else observer.observe(element);
      });
      document.addEventListener('focusin', event => {
        animations.forEach(animation => {
          if (animation.effect?.target.contains(event.target)) animation.cancel();
        });
      }, { signal: listeners.signal });
    }
    if (precise.matches) {
      surfaces.forEach(element => trackPointer(element));
      scenes.forEach(element => trackPointer(element, true));
    }
    window.addEventListener('blur', () => cleanups.forEach(cleanup => cleanup()), { signal: listeners.signal });
  };
  reduced.addEventListener('change', start);
  precise.addEventListener('change', start);
  window.addEventListener('beforeprint', stop);
  window.addEventListener('afterprint', start);
  window.addEventListener('pagehide', stop);
  window.addEventListener('pageshow', event => { if (event.persisted) start(); });
  start();
})();
