(() => {
  const prefix = 'codepop:reading:';
  const get = key => { try { return JSON.parse(localStorage.getItem(key)); } catch { return null; } };
  let storageAvailable = true;
  const put = (key, value) => { try { localStorage.setItem(key, JSON.stringify(value)); } catch { storageAvailable = false; } };
  const valid = (saved, root) => {
    if (!saved || typeof saved.url !== 'string' || !Number.isFinite(saved.progress)) return false;
    try {
      const url = new URL(saved.url, location.origin);
      return url.origin === location.origin && url.pathname.startsWith(root) && url.pathname.endsWith('.html') && !url.pathname.endsWith('/license.html');
    } catch { return false; }
  };
  for (const link of document.querySelectorAll('[data-resume-book]')) {
    const saved = get(prefix + link.dataset.resumeBook);
    if (!valid(saved, link.dataset.bookRoot)) continue;
    link.href = `${saved.url}?resume=1`;
    link.title = `Continue: ${saved.title || 'your last chapter'}`;
    link.hidden = false;
  }
  const reader = document.querySelector('[data-reader-book]');
  if (!reader) return;
  const article = reader.querySelector('.book-article');
  const scrollPort = reader.querySelector('[data-reader-scroll]');
  const size = reader.querySelector('#reader-size');
  const theme = reader.querySelector('#reader-theme');
  const status = reader.querySelector('[data-reader-status]');
  const resume = reader.querySelector('[data-resume-here]');
  const key = prefix + reader.dataset.readerBook;
  const saved = get(key);
  const storedPrefs = get('codepop:reader-preferences');
  const prefs = storedPrefs && typeof storedPrefs === 'object' ? storedPrefs : {};
  const isSavedPage = valid(saved, reader.dataset.readerRoot) && new URL(saved.url, location.origin).pathname === location.pathname;
  const choices = (select, value, fallback) => [...select.options].some(option => option.value === value) ? value : fallback;
  size.value = choices(size, prefs.size, 'regular');
  theme.value = choices(theme, prefs.theme, 'paper');
  const apply = () => {
    reader.dataset.textSize = size.value;
    reader.dataset.theme = theme.value;
  };
  apply();
  reader.querySelector('[data-reader-toolbar]').hidden = false;
  reader.querySelector('[data-reader-session]').hidden = false;
  reader.querySelector('[data-reader-progress-bar]').hidden = false;
  const siteHeader = document.querySelector('.site-header');
  const navigation = reader.querySelector('[data-reader-navigation]');
  const focus = reader.querySelector('[data-reader-focus]');
  let navigationOverride = document.documentElement.classList.contains('reader-navigation-hidden') ? false : null;
  let printing = false, printPosition = 0;
  const syncNavigation = () => {
    const hidden = focus.getAttribute('aria-pressed') === 'true' || (navigationOverride === null ? scrollPort.scrollTop > 8 : !navigationOverride);
    document.body.classList.toggle('reader-scrolled', hidden);
    document.documentElement.classList.toggle('reader-navigation-hidden', hidden);
    try { sessionStorage.setItem('codepop:reader-navigation:' + reader.dataset.readerBook, hidden ? 'hidden' : 'visible'); } catch { /* Navigation still works without browser storage. */ }
    siteHeader.inert = hidden;
    navigation.setAttribute('aria-expanded', String(!hidden));
    navigation.setAttribute('aria-label', hidden ? 'Show site navigation' : 'Hide site navigation');
    navigation.title = hidden ? 'Show site navigation' : 'Hide site navigation';
    if (hidden && siteHeader.contains(document.activeElement)) scrollPort.focus({ preventScroll: true });
  };
  navigation.hidden = false;
  syncNavigation();
  const sidebar = reader.querySelector('.reader-sidebar');
  const contents = reader.querySelector('[data-reader-contents]');
  const mobile = matchMedia('(max-width: 980px)');
  const setSidebar = open => {
    sidebar.hidden = !open;
    reader.dataset.contents = open ? 'open' : 'closed';
    contents.setAttribute('aria-expanded', String(open));
  };
  setSidebar(!mobile.matches);
  mobile.addEventListener('change', () => setSidebar(!mobile.matches));
  contents.addEventListener('click', () => setSidebar(sidebar.hidden));
  scrollPort.addEventListener('pointerdown', () => { if (mobile.matches) setSidebar(false); });
  sidebar.addEventListener('click', event => {
    if (mobile.matches && event.target.closest('a[href^="#"]')) setSidebar(false);
  });
  reader.querySelector('#reader-chapter').addEventListener('change', event => {
    location.assign(event.target.value);
  });
  const filter = reader.querySelector('#reader-chapter-query');
  reader.querySelector('[data-reader-filter]').hidden = false;
  filter.addEventListener('input', () => {
    let matches = 0;
    const query = filter.value.trim().toLocaleLowerCase();
    for (const item of reader.querySelectorAll('.reader-chapters li')) {
      item.hidden = !item.textContent.toLocaleLowerCase().includes(query);
      if (!item.hidden) matches++;
    }
    reader.querySelector('[data-reader-chapter-empty]').hidden = matches > 0;
  });
  const headingLinks = new Map();
  const outline = reader.querySelector('[data-reader-headings]');
  for (const heading of article.querySelectorAll('h2[id]')) {
    const item = document.createElement('li');
    const link = document.createElement('a');
    link.href = `#${encodeURIComponent(heading.id)}`;
    link.textContent = heading.textContent;
    item.append(link); outline.append(item);
    headingLinks.set(heading, link);
  }
  reader.querySelector('[data-reader-outline]').hidden = headingLinks.size === 0;
  const progress = reader.querySelector('[data-reader-progress]');
  const percent = reader.querySelector('[data-reader-percent]');
  const readingOffset = () => scrollPort.getBoundingClientRect().top + 24;
  const articleStart = () => article.getBoundingClientRect().top - scrollPort.getBoundingClientRect().top + scrollPort.scrollTop;
  let progressFrame = false;
  const updateProgress = () => {
    const box = article.getBoundingClientRect();
    const value = Math.round(Math.max(0, Math.min(1, (scrollPort.getBoundingClientRect().bottom - box.top) / Math.max(1, box.height))) * 100);
    progress.value = value;
    percent.textContent = `${value}%`;
    let current = null;
    for (const [heading, link] of headingLinks) {
      link.removeAttribute('aria-current');
      if (heading.getBoundingClientRect().top <= readingOffset() + 80) current = link;
    }
    if (current) current.setAttribute('aria-current', 'location');
    progressFrame = false;
  };
  const scheduleProgress = () => {
    if (!progressFrame) { progressFrame = true; requestAnimationFrame(updateProgress); }
  };
  scrollPort.addEventListener('scroll', () => {
    if (printing) return;
    navigationOverride = null;
    syncNavigation();
    scheduleProgress();
  }, { passive: true });
  window.addEventListener('resize', scheduleProgress);
  if (typeof ResizeObserver !== 'undefined') {
    const observer = new ResizeObserver(scheduleProgress);
    observer.observe(article);
    observer.observe(scrollPort);
  }
  document.fonts.ready.then(scheduleProgress);
  scheduleProgress();
  const setFocus = active => {
    document.body.classList.toggle('reader-focused', active);
    focus.setAttribute('aria-pressed', String(active));
    focus.setAttribute('aria-label', active ? 'Exit focus mode' : 'Enter focus mode');
    focus.title = active ? 'Exit focus mode (Esc)' : 'Focus mode';
    if (!active) navigationOverride = true;
    syncNavigation();
    scheduleProgress();
  };
  focus.addEventListener('click', () => setFocus(focus.getAttribute('aria-pressed') !== 'true'));
  navigation.addEventListener('click', () => {
    const show = navigation.getAttribute('aria-expanded') !== 'true';
    if (focus.getAttribute('aria-pressed') === 'true') setFocus(false);
    navigationOverride = show;
    syncNavigation();
    scheduleProgress();
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    if (mobile.matches && !sidebar.hidden) { setSidebar(false); contents.focus(); }
    else if (focus.getAttribute('aria-pressed') === 'true') { setFocus(false); focus.focus(); }
    else if (document.body.classList.contains('reader-scrolled')) { navigationOverride = true; syncNavigation(); }
  });
  reader.querySelector('[data-reader-start]').addEventListener('click', event => {
    event.preventDefault();
    scrollPort.scrollTo({ top: 0, behavior: 'instant' });
    navigationOverride = true;
    syncNavigation();
    scrollPort.focus({ preventScroll: true });
  });
  scrollPort.addEventListener('keydown', event => {
    if (event.target !== scrollPort || event.altKey || event.ctrlKey || event.metaKey) return;
    const step = scrollPort.clientHeight * .85;
    const targets = {
      PageDown: scrollPort.scrollTop + step,
      PageUp: scrollPort.scrollTop - step,
      ArrowDown: scrollPort.scrollTop + 40,
      ArrowUp: scrollPort.scrollTop - 40,
      Home: 0,
      End: scrollPort.scrollHeight,
      ' ': scrollPort.scrollTop + (event.shiftKey ? -step : step),
    };
    if (!(event.key in targets)) return;
    event.preventDefault();
    // Keep keyboard scrolling inside the document, without a pending browser
    // animation that could override a subsequent jump to the beginning.
    scrollPort.scrollTo({ top: targets[event.key], behavior: 'instant' });
  });
  reader.querySelector('[data-reader-print]').addEventListener('click', () => window.print());
  let restored = false, interacted = false, timer;
  const save = () => {
    // Opening another chapter without reading must not erase the last saved place.
    if (printing || (!interacted && !restored)) return;
    const box = article.getBoundingClientRect();
    const progress = Math.max(0, Math.min(1, (scrollPort.scrollTop + 24 - articleStart()) / Math.max(1, box.height)));
    put(key, { url: location.pathname, title: reader.dataset.readerTitle, progress, updated: Date.now() });
    if (!storageAvailable) status.textContent = 'Saving is unavailable in this browser. Reading controls still work.';
  };
  const restore = async () => {
    if (!isSavedPage || restored) return;
    restored = true;
    await document.fonts.ready;
    scrollPort.scrollTo({ top: Math.max(0, articleStart() + article.getBoundingClientRect().height * Math.max(0, Math.min(1, saved.progress)) - 24), behavior: 'instant' });
    resume.hidden = true;
    status.textContent = 'Returned to your saved place.';
    const url = new URL(location.href); url.searchParams.delete('resume'); history.replaceState(null, '', url);
  };
  if (isSavedPage && saved.progress > .02) {
    resume.hidden = false;
    resume.addEventListener('click', event => { event.preventDefault(); restore(); });
    if (new URLSearchParams(location.search).get('resume') === '1') restore();
  }
  [size, theme].forEach(select => select.addEventListener('change', () => {
    apply(); put('codepop:reader-preferences', { size: size.value, theme: theme.value });
    status.textContent = storageAvailable ? 'Reading preferences saved on this device.' : 'Preferences apply here; saving is unavailable in this browser.';
  }));
  reader.querySelector('[data-reader-reset]').addEventListener('click', () => {
    size.value = 'regular'; theme.value = 'paper'; apply();
    put('codepop:reader-preferences', { size: 'regular', theme: 'paper' });
    status.textContent = 'Reading preferences reset.';
  });
  ['pointerdown', 'keydown', 'wheel', 'touchstart'].forEach(name => window.addEventListener(name, () => { interacted = true; }, { once: true, passive: true }));
  scrollPort.addEventListener('scroll', () => { clearTimeout(timer); timer = setTimeout(save, 250); }, { passive: true });
  window.addEventListener('beforeprint', () => {
    printPosition = scrollPort.scrollTop;
    printing = true;
    clearTimeout(timer);
  });
  window.addEventListener('afterprint', () => {
    printing = false;
    scrollPort.scrollTo({ top: printPosition, behavior: 'instant' });
    syncNavigation();
    scheduleProgress();
  });
  window.addEventListener('pagehide', save);
  document.addEventListener('visibilitychange', () => { if (document.hidden) save(); });
})();
