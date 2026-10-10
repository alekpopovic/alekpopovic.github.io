(() => {
  document.querySelectorAll('[data-share]').forEach(group => {
    const url = group.dataset.shareUrl;
    const title = group.dataset.shareTitle;
    const copy = group.querySelector('[data-share-copy]');
    const label = group.querySelector('[data-copy-label]');
    const native = group.querySelector('[data-share-native]');
    const status = group.querySelector('[data-share-status]');
    const manual = group.querySelector('.share-manual');
    let reset, copying = false, sharing = false;
    copy.hidden = false;
    copy.addEventListener('click', async () => {
      if (copying) return;
      copying = true;
      clearTimeout(reset);
      status.textContent = '';
      copy.setAttribute('aria-busy', 'true');
      try {
        if (!window.isSecureContext || !navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(url);
        manual.hidden = true;
        label.textContent = 'Copied ✓';
        status.textContent = 'Link copied to clipboard.';
        reset = setTimeout(() => { label.textContent = 'Copy link'; }, 2200);
      } catch {
        label.textContent = 'Copy link';
        manual.hidden = false;
        const input = manual.querySelector('input');
        input.focus();
        input.select();
        status.textContent = 'Select and copy the link below.';
      } finally { copying = false; copy.removeAttribute('aria-busy'); }
    });
    if (window.isSecureContext && typeof navigator.share === 'function') {
      native.hidden = false;
      native.addEventListener('click', async () => {
        if (sharing) return;
        sharing = true;
        status.textContent = '';
        native.setAttribute('aria-busy', 'true');
        try { await navigator.share({ title, url }); }
        catch (error) {
          if (error?.name !== 'AbortError') status.textContent = 'Choose a network above or copy the link to share.';
        } finally { sharing = false; native.removeAttribute('aria-busy'); }
      });
    }
  });
})();
