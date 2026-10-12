// Content events use identifiers only; never send notes, queries, or contact data.
(() => {
  const config = document.querySelector('script[data-ga4-host]');
  if (!config || location.hostname !== config.dataset.ga4Host || location.protocol !== 'https:' || navigator.doNotTrack === '1' || navigator.globalPrivacyControl || typeof window.gtag !== 'function') return;
  const reader = document.querySelector('[data-reader-book]');
  const chapter = reader ? { book_id: reader.dataset.readerBook, chapter_slug: reader.dataset.readerChapter } : {};
  const identifiers = new Set(['book_id', 'chapter_slug', 'format', 'project_id', 'channel', 'kind', 'path_id', 'step']);
  const allowed = new Set(['book_download', 'project_open', 'contact_open', 'chapter_open', 'chapter_complete', 'reading_engaged', 'learning_step_complete']);
  const send = (name, props = {}) => {
    if (!allowed.has(name)) return;
    const clean = {};
    for (const [key, value] of Object.entries(props)) {
      if (identifiers.has(key) && ((typeof value === 'string' && /^[a-z0-9_-]{1,100}$/i.test(value)) || (typeof value === 'number' && Number.isFinite(value)))) clean[key] = value;
    }
    window.gtag('event', name, clean);
  };
  if (reader) send('chapter_open', chapter);
  document.addEventListener('codepop:analytics', event => send(event.detail?.name, event.detail?.props));
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (!link) return;
    const url = new URL(link.href);
    const download = url.pathname.match(/^\/assets\/books\/([^/]+)\/.*\.(pdf|epub)$/i);
    if (url.origin === location.origin && download) send('book_download', { book_id: download[1], format: download[2].toLowerCase() });
    else if (['mailto:', 'tel:', 'viber:', 'whatsapp:'].includes(url.protocol) || url.hostname === 'wa.me') send('contact_open', { channel: url.hostname === 'wa.me' ? 'whatsapp' : url.protocol.slice(0, -1) });
    else if (url.hostname === 'github.com' && url.pathname.startsWith('/alekpopovic/')) {
      const project = url.pathname.split('/')[2];
      if (['orch', 'cloudivision', 'clusterforge', 'container-desk'].includes(project)) send('project_open', { project_id: project });
    }
  });
  const reading = document.querySelector('[data-post-content], .book-article');
  if (!reading) return;
  const panel = document.querySelector('[data-reader-scroll]');
  const opened = performance.now();
  let sent = false;
  const check = () => {
    if (sent || document.hidden || performance.now() - opened < 30000) return;
    const box = reading.getBoundingClientRect();
    const bottom = panel ? panel.getBoundingClientRect().bottom : innerHeight;
    if ((bottom - box.top) / Math.max(1, box.height) < .75) return;
    sent = true;
    send('reading_engaged', { kind: reader ? 'chapter' : 'post', ...chapter });
  };
  (panel || window).addEventListener('scroll', check, { passive: true });
  document.addEventListener('visibilitychange', check);
  setTimeout(check, 30050);
})();
