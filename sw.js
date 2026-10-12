---
layout: null
sitemap: false
---
const SHELL = 'codepop-reader-shell-v1';
const CHAPTERS = 'codepop-reader-chapters-v1';
const MANIFEST = '{{ "/offline-manifest.json" | relative_url }}';
const FALLBACK = '{{ "/offline/" | relative_url }}';
const LIMIT = 24;
self.addEventListener('install', event => event.waitUntil(self.skipWaiting()));
self.addEventListener('activate', event => event.waitUntil(self.clients.claim()));
const manifest = async () => {
  try {
    const response = await fetch(MANIFEST, { cache: 'no-cache' });
    if (!response.ok) throw new Error('Manifest unavailable');
    const data = await response.clone().json();
    await (await caches.open(SHELL)).put(MANIFEST, response);
    return data;
  } catch (error) {
    const saved = await (await caches.open(SHELL)).match(MANIFEST);
    if (saved) return saved.json();
    throw error;
  }
};
self.addEventListener('message', event => {
  if (!event.ports[0]) return;
  event.waitUntil((async () => {
    try {
      const data = await manifest();
      const cache = await caches.open(CHAPTERS);
      const url = new URL(event.data.url || FALLBACK, self.location.origin);
      if (url.origin !== self.location.origin) throw new Error('Only chapters on this site can be saved.');
      const path = url.pathname;
      if (event.data.action === 'list') {
        const keys = new Set((await cache.keys()).map(request => new URL(request.url).pathname));
        event.ports[0].postMessage({ ok: true, chapters: data.chapters.filter(chapter => keys.has(chapter.url)) }); return;
      }
      const chapter = data.chapters.find(chapter => chapter.url === path);
      if (!chapter) throw new Error('Choose a section from a book to save offline.');
      if (event.data.action === 'save') {
        if (!(await cache.match(path)) && (await cache.keys()).length >= LIMIT) throw new Error(`You can save ${LIMIT} sections. Remove an offline copy before adding another.`);
        const response = await fetch(path, { cache: 'reload' });
        if (!response.ok || !response.headers.get('Content-Type')?.includes('text/html')) throw new Error('The section could not be downloaded. Try again online.');
        // Store the chapter last, so incomplete shell downloads are never reported as ready.
        await (await caches.open(SHELL)).addAll([...new Set([...data.assets, ...(chapter.assets || []), FALLBACK])]);
        await cache.put(path, response);
      } else if (event.data.action === 'remove') await cache.delete(path);
      else if (event.data.action !== 'status') throw new Error('Unknown offline action.');
      event.ports[0].postMessage({ ok: true, saved: !!(await cache.match(path)) });
    } catch (error) { event.ports[0].postMessage({ ok: false, error: error.message || 'Offline storage is unavailable.' }); }
  })());
});
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (event.request.method !== 'GET' || url.origin !== self.location.origin) return;
  const path = url.pathname;
  if (event.request.mode === 'navigate') {
    event.respondWith((async () => {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 3000);
      try {
        const response = await fetch(event.request, { signal: controller.signal });
        const cache = await caches.open(CHAPTERS);
        if (response.ok && await cache.match(path)) await cache.put(path, response.clone());
        return response; // Preserve actual server 404s and other status codes.
      } catch {
        const chapter = await (await caches.open(CHAPTERS)).match(path);
        if (chapter) return chapter;
        const fallback = await (await caches.open(SHELL)).match(FALLBACK);
        if (fallback) return new Response(await fallback.text(), { status: 503, headers: { 'Content-Type': 'text/html; charset=utf-8' } });
        return Response.error();
      } finally { clearTimeout(timeout); }
    })());
  } else if (path === MANIFEST || /^\/assets\//.test(path)) {
    event.respondWith((async () => {
      try {
        const response = await fetch(event.request);
        const cache = await caches.open(SHELL);
        if (response.ok && await cache.match(path)) await cache.put(path, response.clone());
        return response;
      } catch { return (await (await caches.open(SHELL)).match(path)) || Response.error(); }
    })());
  }
});
