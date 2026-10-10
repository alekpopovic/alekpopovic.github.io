(() => {
  const cards = [...document.querySelectorAll('[data-playlist]')];
  for (const card of cards) {
    const player = card.querySelector('iframe');
    card.addEventListener('click', event => {
      const video = event.target.closest('.playlist-video');
      const load = event.target.closest('[data-load-playlist]');
      if ((!video && !load) || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      // Reload the other player without autoplay to stop its audio.
      for (const other of cards) {
        if (other === card) continue;
        const otherPlayer = other.querySelector('iframe');
        if (!otherPlayer.hasAttribute('src')) continue;
        otherPlayer.removeAttribute('src');
        otherPlayer.hidden = true;
        other.querySelector('[data-load-playlist]').hidden = false;
      }
      const selected = video ? new URL(`https://www.youtube-nocookie.com/embed/${video.dataset.videoId}`) : new URL(player.dataset.playerSrc);
      selected.search = new URLSearchParams({ list: card.dataset.playlist, autoplay: '1', rel: '0', playsinline: '1' });
      player.src = selected.href;
      player.hidden = false;
      card.querySelector('[data-load-playlist]').hidden = true;
      player.title = video ? `${video.querySelector('.video-title').textContent.trim()} — YouTube video` : `${card.querySelector('h2').textContent.trim()} — YouTube playlist`;
      if (video) card.querySelectorAll('.playlist-video').forEach(link => {
        if (link === video) link.setAttribute('aria-current', 'true');
        else link.removeAttribute('aria-current');
      });
      player.scrollIntoView({ behavior: 'auto', block: 'center' });
      player.focus({ preventScroll: true });
    });
  }
  const selected = new URLSearchParams(location.search).get('video');
  if (selected) {
    const match = [...document.querySelectorAll('[data-video-id]')].find(link => link.dataset.videoId === selected);
    if (match) match.click();
  }
})();
