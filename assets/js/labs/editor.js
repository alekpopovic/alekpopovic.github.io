(() => {
  const root = document.querySelector('[data-workshop-lab]');
  if (!root) return;
  const select = root.querySelector('#workshop-exercise'), editor = root.querySelector('#workshop-code');
  const status = root.querySelector('[data-workshop-result]'), results = root.querySelector('[data-workshop-results]');
  const run = root.querySelector('[data-workshop-run]'), stop = root.querySelector('[data-workshop-stop]');
  const draft = root.querySelector('[data-workshop-draft]');
  let catalog, workerSource, current, dispose;
  const key = () => `codepop:workshop:${current.id}`;
  const save = () => { try { localStorage.setItem(key(), editor.value); draft.textContent = 'Draft saved in this browser'; } catch { draft.textContent = 'Storage unavailable · download your code to keep it'; } };
  const end = () => { if (dispose) dispose(); dispose = null; run.disabled = false; stop.disabled = true; editor.readOnly = false; };
  function load(id, updateUrl = true) {
    end(); current = catalog.find(item => item.id === id) || catalog[0]; select.value = current.id;
    editor.value = current.starter; draft.textContent = 'Draft stays in this browser';
    try { const stored = localStorage.getItem(key()); if (stored !== null && stored.length <= 40000) { editor.value = stored; draft.textContent = 'Restored your saved draft'; } } catch { draft.textContent = 'Storage unavailable · draft lasts for this visit'; }
    root.querySelector('[data-workshop-contract]').textContent = current.contract;
    root.querySelector('[data-workshop-hint]').textContent = current.hint;
    root.querySelector('[data-workshop-guide]').href = current.guide;
    root.querySelector('[data-workshop-tests]').textContent = current.display_tests;
    root.querySelector('[data-workshop-reference]').textContent = current.solution;
    root.querySelector('[data-workshop-solution]').open = false;
    results.replaceChildren(); status.textContent = 'The starter intentionally fails. Run the tests to see the behavior.';
    if (updateUrl) { const url = new URL(location.href); url.searchParams.set('exercise', current.id); history.replaceState(null, '', url); }
  }
  // The opaque-origin frame's Blob worker inherits its connection-denying CSP.
  function frameBoot() {
    let worker;
    addEventListener('message', event => {
      if (event.source !== parent) return;
      if (event.data.stop) { worker?.terminate(); return; }
      const url = URL.createObjectURL(new Blob([event.data.worker], { type: 'text/javascript' }));
      try {
        worker = new Worker(url);
        worker.onmessage = message => { if (!['result', 'error'].includes(message.data?.type)) return; parent.postMessage(message.data, '*'); worker.terminate(); URL.revokeObjectURL(url); };
        worker.onerror = event => { parent.postMessage({ type: 'error', message: event.message || 'The JavaScript module could not run. Check its syntax and exported function.' }, '*'); worker.terminate(); };
        worker.postMessage({ source: event.data.source, tests: event.data.tests });
      } catch { parent.postMessage({ type: 'error', message: 'This browser could not start the isolated runner. Use the downloadable Node.js workspace.' }, '*'); }
    });
    parent.postMessage({ type: 'ready' }, '*');
  }
  run.addEventListener('click', () => {
    end(); save(); run.disabled = true; stop.disabled = false; editor.readOnly = true; results.replaceChildren(); status.textContent = 'Running acceptance tests…';
    let started = false;
    const frame = document.createElement('iframe'); frame.hidden = true; frame.title = 'Isolated workshop runner'; frame.setAttribute('sandbox', 'allow-scripts');
    frame.srcdoc = `<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline' blob:; worker-src blob:; connect-src 'none'"><script>(${frameBoot.toString()})()<\/script>`;
    const timeout = setTimeout(() => { end(); status.textContent = 'Stopped after 4 seconds. Check for a loop or unfinished promise, then try again.'; }, 4000);
    const receive = event => {
      if (event.source !== frame.contentWindow) return;
      if (event.data?.type === 'ready' && !started) { started = true; frame.contentWindow.postMessage({ worker: workerSource, source: editor.value, tests: current.tests }, '*'); return; }
      if (event.data?.type === 'error') { status.textContent = `Could not run: ${String(event.data.message).slice(0, 500)}`; end(); return; }
      if (event.data?.type !== 'result' || !Array.isArray(event.data.results)) return;
      const rows = event.data.results.slice(0, 20), passed = rows.filter(row => row.passed === true).length;
      for (const row of rows) { const item = document.createElement('li'); item.dataset.passed = String(row.passed === true); item.textContent = `${row.passed === true ? 'PASS' : 'FAIL'} · ${String(row.name).slice(0, 200)}${row.message ? ` — ${String(row.message).slice(0, 500)}` : ''}`; results.append(item); }
      status.textContent = `${passed} of ${rows.length} tests passed. ${passed === rows.length && rows.length ? 'The exercise contract passes. Review your change and explain what the tests do not cover.' : 'Read a failing case, make a focused change, and run again.'}`; end();
    };
    window.addEventListener('message', receive);
    dispose = () => { clearTimeout(timeout); window.removeEventListener('message', receive); frame.remove(); };
    document.body.append(frame);
  });
  stop.addEventListener('click', () => { end(); status.textContent = 'Stopped. Your code is still in the editor.'; });
  editor.addEventListener('input', () => { save(); results.replaceChildren(); status.textContent = 'Code changed. Run tests to check this version.'; });
  select.addEventListener('change', () => load(select.value));
  root.querySelector('[data-workshop-reset]').addEventListener('click', () => { end(); editor.value = current.starter; save(); results.replaceChildren(); status.textContent = 'Starter restored. Run the tests before changing it.'; editor.focus(); });
  root.querySelector('[data-workshop-download]').addEventListener('click', () => { const url = URL.createObjectURL(new Blob([editor.value], { type: 'text/javascript' })), link = document.createElement('a'); link.href = url; link.download = `${current.id}-app.mjs`; link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000); });
  window.addEventListener('pagehide', end);
  window.addEventListener('popstate', () => { if (catalog) load(new URLSearchParams(location.search).get('exercise'), false); });
  Promise.all([fetch(root.dataset.workshopIndex).then(response => { if (!response.ok) throw new Error(); return response.json(); }), fetch(root.dataset.workerSource).then(response => { if (!response.ok) throw new Error(); return response.text(); })]).then(([data, source]) => {
    catalog = data; workerSource = source; load(new URLSearchParams(location.search).get('exercise'), false);
    root.querySelector('[data-workshop-controls]').hidden = false; root.querySelector('[data-workshop-loading]').hidden = true;
  }).catch(() => { root.classList.add('workshop-unavailable'); root.querySelector('[data-workshop-loading]').textContent = 'The browser workspace could not load. Download the files below or reload to retry.'; });
})();
