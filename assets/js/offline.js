(() => {
  const controls = document.querySelector('[data-offline-controls]');
  const directory = document.querySelector('[data-offline-directory]');
  if (!controls && !directory) return;
  const supported = 'serviceWorker' in navigator && 'caches' in window && window.isSecureContext;
  const status = document.querySelector('[data-offline-status]');
  if (!supported) { if (status) status.textContent = 'Offline storage is unavailable here. You can still download the PDF or EPUB.'; return; }
  if (controls) controls.hidden = false;
  const request = async (action, url = location.pathname, register = false) => {
    let registration = await navigator.serviceWorker.getRegistration('/');
    if (register) registration = await navigator.serviceWorker.register('/sw.js', { scope: '/' });
    if (!registration) return { ok: true, saved: false, chapters: [] };
    if (!registration.active) await new Promise((resolve, reject) => {
      const worker = registration.installing || registration.waiting;
      if (!worker) { reject(new Error('Offline reader is not ready. Try again.')); return; }
      const timer = setTimeout(() => reject(new Error('Offline reader is not ready. Try again.')), 10000);
      const check = () => { if (worker.state === 'activated') { clearTimeout(timer); resolve(); } else if (worker.state === 'redundant') { clearTimeout(timer); reject(new Error('Offline reader could not start.')); } };
      worker.addEventListener('statechange', check); check();
    });
    return new Promise((resolve, reject) => {
      const channel = new MessageChannel();
      const timer = setTimeout(() => { channel.port1.close(); reject(new Error('Saving took too long. Check your connection and try again.')); }, 30000);
      channel.port1.onmessage = event => { clearTimeout(timer); channel.port1.close(); event.data.ok ? resolve(event.data) : reject(new Error(event.data.error)); };
      registration.active.postMessage({ action, url }, [channel.port2]);
    });
  };
  const report = error => { if (status) status.textContent = error.message || 'Offline storage is unavailable. Reading still works.'; };
  const save = document.querySelector('[data-offline-save]');
  const remove = document.querySelector('[data-offline-remove]');
  const update = saved => { save.textContent = saved ? 'Refresh offline copy' : 'Save this section offline'; remove.hidden = !saved; status.textContent = saved ? 'This section is available offline on this device.' : 'Save up to 24 sections. PDFs and EPUBs are not cached.'; };
  if (controls) {
    request('status').then(result => update(result.saved)).catch(report);
    for (const [button, action] of [[save, 'save'], [remove, 'remove']]) button.addEventListener('click', async () => {
      save.disabled = true; remove.disabled = true;
      status.textContent = action === 'save' ? 'Downloading this section and reading tools…' : 'Removing offline copy…';
      try { const result = await request(action, location.pathname, action === 'save'); update(result.saved); } catch (error) { report(error); }
      finally { save.disabled = false; remove.disabled = false; }
    });
  }
  if (directory) {
    const render = async () => {
      const result = await request('list'); directory.replaceChildren();
      for (const chapter of result.chapters) {
        const item = document.createElement('li'), link = document.createElement('a'), button = document.createElement('button');
        link.href = chapter.url; link.textContent = `${chapter.book}: ${chapter.title}`;
        button.type = 'button'; button.className = 'study-button'; button.textContent = 'Remove'; button.setAttribute('aria-label', `Remove offline copy: ${chapter.title}`);
        button.addEventListener('click', async () => { button.disabled = true; try { await request('remove', chapter.url); await render(); } catch (error) { button.disabled = false; report(error); } });
        item.append(link, button); directory.append(item);
      }
      status.textContent = result.chapters.length ? `${result.chapters.length} sections saved on this device.` : 'No offline sections saved in this browser yet.';
    };
    render().catch(report);
  }
})();
