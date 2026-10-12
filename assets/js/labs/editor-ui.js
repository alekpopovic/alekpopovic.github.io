(() => {
  const root = document.querySelector('[data-workshop-lab]');
  if (!root) return;
  const editor = root.querySelector('#workshop-code'), highlight = root.querySelector('[data-editor-highlight]');
  const gutter = root.querySelector('[data-editor-lines]'), shell = root.querySelector('.code-editor-shell');
  const compare = root.querySelector('[data-editor-diff]'), compareStatus = root.querySelector('[data-editor-diff-status]');
  const upload = root.querySelector('#workshop-import-file'), importStatus = root.querySelector('[data-editor-import-status]'), apply = root.querySelector('[data-editor-import-apply]');
  let candidate = null, generation = 0;
  const tokens = /\/\*[\s\S]*?\*\/|\/\/[^\n]*|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`|\b(?:export|import|from|async|await|function|return|const|let|var|if|else|for|while|throw|new|try|catch|finally|class|extends|true|false|null|undefined|typeof|instanceof|of|in|break|continue)\b|\b\d+(?:\.\d+)?\b/g;
  const paint = () => {
    const text = editor.value, fragment = document.createDocumentFragment(); let at = 0;
    for (const match of text.matchAll(tokens)) {
      fragment.append(document.createTextNode(text.slice(at, match.index)));
      const token = document.createElement('span');
      token.className = match[0].startsWith('/') ? 'code-token-comment' : /^["'`]/.test(match[0]) ? 'code-token-string' : /^\d/.test(match[0]) ? 'code-token-number' : 'code-token-keyword';
      token.textContent = match[0]; fragment.append(token); at = match.index + match[0].length;
    }
    fragment.append(document.createTextNode(text.slice(at) + '\n'));
    highlight.replaceChildren(fragment); gutter.textContent = text.split('\n').map((_, index) => index + 1).join('\n'); syncScroll();
  };
  const syncScroll = () => { highlight.parentElement.scrollTop = editor.scrollTop; highlight.parentElement.scrollLeft = editor.scrollLeft; gutter.style.transform = `translateY(${-editor.scrollTop}px)`; };
  const diff = () => {
    const left = editor.value.split('\n'), right = root.querySelector('[data-workshop-reference]').textContent.split('\n');
    const truncated = left.length > 240 || right.length > 240, a = left.slice(0, 240), b = right.slice(0, 240);
    const matrix = Array.from({ length: a.length + 1 }, () => new Uint16Array(b.length + 1));
    for (let i = a.length - 1; i >= 0; i--) for (let j = b.length - 1; j >= 0; j--) matrix[i][j] = a[i] === b[j] ? matrix[i + 1][j + 1] + 1 : Math.max(matrix[i + 1][j], matrix[i][j + 1]);
    const fragment = document.createDocumentFragment(); let i = 0, j = 0, removed = 0, added = 0;
    const line = (prefix, value, className) => { const node = document.createElement('span'); node.className = className; node.textContent = `${prefix} ${value}\n`; fragment.append(node); };
    while (i < a.length || j < b.length) {
      if (i < a.length && j < b.length && a[i] === b[j]) { line(' ', a[i++], 'diff-same'); j++; }
      else if (j < b.length && (i === a.length || matrix[i][j + 1] > matrix[i + 1][j])) { line('+', b[j++], 'diff-added'); added++; }
      else { line('-', a[i++], 'diff-removed'); removed++; }
    }
    compare.replaceChildren(fragment);
    compareStatus.textContent = `${removed} removed lines · ${added} added lines.${truncated ? ' Preview limited to the first 240 lines of each file.' : ''}`;
  };
  shell.classList.add('is-highlighted'); gutter.parentElement.hidden = false; highlight.parentElement.hidden = false;
  editor.addEventListener('input', paint); editor.addEventListener('scroll', syncScroll);
  editor.addEventListener('keydown', event => { if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') { event.preventDefault(); root.querySelector('[data-workshop-run]').click(); } });
  root.addEventListener('codepop:workshop-loaded', () => { generation++; candidate = null; apply.disabled = true; upload.value = ''; importStatus.textContent = 'The file stays on this device. Review before replacing your draft.'; compare.replaceChildren(); compareStatus.textContent = 'Refresh the comparison after editing your code.'; paint(); });
  root.querySelector('[data-workshop-reset]').addEventListener('click', paint);
  root.querySelector('[data-editor-compare]').addEventListener('click', diff);
  upload.addEventListener('change', async () => {
    const token = ++generation; candidate = null; apply.disabled = true;
    const file = upload.files[0]; if (!file) return;
    if (!/\.(m?js)$/i.test(file.name) || file.size > 40000) { importStatus.textContent = 'Choose a JavaScript .js or .mjs file no larger than 40 KB. Your draft has not changed.'; return; }
    try {
      const content = await file.text(); if (token !== generation) return;
      if (content.length > 40000 || content.includes('\0')) throw new Error();
      candidate = content; apply.disabled = false; importStatus.textContent = `${file.name} · ${file.size} bytes. Use this file to replace the current draft; it will not run automatically.`;
    } catch { if (token === generation) importStatus.textContent = 'This file could not be read as source text. Your draft has not changed.'; }
  });
  apply.addEventListener('click', () => {
    if (candidate === null || editor.readOnly) return;
    editor.value = candidate; editor.dispatchEvent(new Event('input', { bubbles: true })); candidate = null; apply.disabled = true; editor.focus(); importStatus.textContent = 'File opened. Review your code, then run the tests.';
  });
  paint();
})();
