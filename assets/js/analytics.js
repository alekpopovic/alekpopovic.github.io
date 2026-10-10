// Optional Plausible Events API integration. The layout only loads this file
// after an owner configures a domain. No cookies or local analytics storage.
(() => {
  const script = document.querySelector('script[data-domain][data-endpoint]');
  if (!script || !script.dataset.domain || navigator.doNotTrack === '1' || navigator.globalPrivacyControl || ['localhost', '127.0.0.1'].includes(location.hostname) || location.protocol !== 'https:') return;
  const send = (name, props = {}) => {
    const url = new URL(location.href); url.search = ''; url.hash = '';
    let referrer = '';
    try { referrer = document.referrer ? new URL(document.referrer).origin : ''; } catch { /* Invalid referrers are omitted. */ }
    fetch(script.dataset.endpoint, { method: 'POST', credentials: 'omit', keepalive: true,
      headers: { 'Content-Type': 'text/plain' }, body: JSON.stringify({ name, domain: script.dataset.domain, url: url.href, referrer, screen_width: innerWidth, props }) }).catch(() => {});
  };
  send('pageview');
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]'); if (!link) return;
    const url = new URL(link.href);
    if (/\.(pdf|epub)$/i.test(url.pathname)) {
      const parts = url.pathname.split('/'); const index = parts.indexOf('books');
      send('Book download', { format: url.pathname.split('.').pop(), book: link.dataset.bookId || (index >= 0 ? parts[index + 1] : 'unknown') });
    }
    else if (['mailto:', 'tel:', 'viber:', 'whatsapp:'].includes(url.protocol) || url.hostname === 'wa.me') send('Contact click', { channel: url.protocol === 'https:' ? 'WhatsApp' : url.protocol.slice(0, -1) });
    else if (url.hostname === 'github.com' && url.pathname.split('/').filter(Boolean).length >= 2) send('Project click', { project: url.pathname.split('/')[2] });
  });
  const reading = document.querySelector('[data-post-content], .book-article');
  if (!reading) return;
  const scrollPort = document.querySelector('[data-reader-scroll]');
  const opened = performance.now(); let sent = false;
  (scrollPort || window).addEventListener('scroll', () => {
    if (sent || performance.now() - opened < 30000) return;
    const box = reading.getBoundingClientRect();
    const bottom = scrollPort ? scrollPort.getBoundingClientRect().bottom : innerHeight;
    if ((bottom - box.top) / Math.max(1, box.height) < .75) return;
    sent = true; send('Engaged reading', { kind: reading.classList.contains('book-article') ? 'chapter' : 'post' });
  }, { passive: true });
})();
