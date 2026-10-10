(() => {
  const content = document.querySelector('[data-post-content]');
  if (!content) return;
  const headings = [...content.querySelectorAll('h2[id]')];
  const toc = document.querySelector('[data-article-toc]');
  const links = document.querySelector('[data-article-toc-links]');
  const progress = document.querySelector('[data-reading-progress]');
  headings.forEach(heading => {
    const link = document.createElement('a');
    link.href = `#${heading.id}`;
    link.textContent = heading.textContent;
    links.append(link);
  });
  if (headings.length) { toc.hidden = false; toc.open = window.matchMedia('(min-width: 1001px)').matches; }
  let scheduled = false;
  function updateReading() {
    scheduled = false;
    const bounds = content.getBoundingClientRect();
    const distance = Math.max(1, bounds.height - window.innerHeight * .4);
    const fraction = Math.max(0, Math.min(1, (window.innerHeight * .25 - bounds.top) / distance));
    progress.style.setProperty('--reading-progress', fraction);
    let current = headings[0];
    headings.forEach(heading => { if (heading.getBoundingClientRect().top <= 180) current = heading; });
    links.querySelectorAll('a').forEach(link => {
      if (current && link.hash === `#${current.id}`) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }
  const schedule = () => { if (!scheduled) { scheduled = true; window.requestAnimationFrame(updateReading); } };
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule);
  progress.hidden = false;
  updateReading();
})();
