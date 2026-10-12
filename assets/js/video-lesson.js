(() => {
  const root = document.querySelector('[data-video-lesson]'); if (!root) return;
  const toSeconds = value => /^\d+:[0-5]\d$/.test(value) ? value.split(':').reduce((sum, part) => sum * 60 + Number(part), 0) : NaN;
  const duration = root.dataset.videoDuration.split(':').reduce((sum, part) => sum * 60 + Number(part), 0), form = root.querySelector('[data-video-time-form]');
  let time = Number(new URLSearchParams(location.search).get('t'));
  if (!Number.isSafeInteger(time) || time < 0 || time >= duration) time = 0;
  const paint = () => {
    form.elements.time.value = `${Math.floor(time / 60)}:${String(time % 60).padStart(2, '0')}`;
    const url = new URL(location.href); url.search = time ? `t=${time}` : '';
    const link = root.querySelector('[data-video-time-link]'); link.href = url.href; link.textContent = `Open this video at ${form.elements.time.value} →`;
    root.querySelector('[data-lesson-youtube]').href = `https://www.youtube.com/watch?v=${root.dataset.videoId}&t=${time}s`;
  };
  form.hidden = false; paint();
  form.addEventListener('submit', event => {
    event.preventDefault(); const next = toSeconds(form.elements.time.value), status = root.querySelector('[data-video-time-status]');
    if (!Number.isSafeInteger(next) || next < 0 || next >= duration) { status.textContent = `Choose a time before ${root.dataset.videoDuration}.`; return; }
    time = next; paint(); history.replaceState(null, '', root.querySelector('[data-video-time-link]').href); status.textContent = 'Timestamp link ready. Open the link to watch from this moment.';
  });
  root.querySelector('[data-lesson-play]').addEventListener('click', event => {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); const player = root.querySelector('iframe'); player.src = `https://www.youtube-nocookie.com/embed/${root.dataset.videoId}?start=${time}&autoplay=1&rel=0`; player.hidden = false; event.currentTarget.hidden = true; player.focus();
  });
})();
