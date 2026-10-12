(() => {
  const root = document.querySelector('[data-learning-start]');
  if (!root) return;
  const catalog = JSON.parse(root.querySelector('[data-learning-catalog]').textContent);
  const form = root.querySelector('[data-start-form]'), result = root.querySelector('[data-start-result]');
  const field = name => form.elements.namedItem(name);
  const params = new URLSearchParams(location.search);
  for (const name of ['topic', 'experience', 'minutes']) if ([...field(name).options].some(option => option.value === params.get(name))) field(name).value = params.get(name);
  let selected;
  const render = (focus = false) => {
    const route = catalog.starts.find(item => item.id === field('topic').value), path = catalog.paths.find(item => item.id === route.path_id);
    selected = { path_id: path.id, session_minutes: Number(field('minutes').value), sessions: 3, goal: path.outcome };
    const title = root.querySelector('#start-result-title'); title.textContent = path.title;
    root.querySelector('[data-start-context]').textContent = route[field('experience').value];
    const list = root.querySelector('[data-start-steps]'); list.replaceChildren();
    for (const step of path.step_items.slice(0, selected.session_minutes === 20 ? 1 : 3)) {
      const item = document.createElement('li'), link = document.createElement('a'), detail = document.createElement('p');
      link.href = step.url; link.textContent = step.title; detail.textContent = `Try: ${step.exercise}`; item.append(link, detail); list.append(item);
    }
    const workshop = catalog.workshops.find(item => item.id === route.workshop), bench = root.querySelector('[data-start-workshop]'); bench.replaceChildren();
    if (workshop) { const link = document.createElement('a'); link.href = workshop.url; link.textContent = `Optional practice: ${workshop.title} →`; bench.append(link); }
    const url = new URL(location.href); url.search = new URLSearchParams({ topic: route.id, experience: field('experience').value, minutes: String(selected.session_minutes) });
    history.replaceState(null, '', url); root.querySelector('[data-start-share]').href = url.href;
    root.querySelector('[data-start-status]').textContent = ''; result.hidden = false; if (focus) title.focus();
  };
  form.hidden = false; render();
  form.addEventListener('submit', event => { event.preventDefault(); render(true); });
  root.querySelector('[data-start-save]').addEventListener('click', () => {
    try { localStorage.setItem('codepop:study-plan', JSON.stringify(selected)); root.querySelector('[data-start-status]').textContent = 'Route saved on this device. Open My Learning to adjust your goal and session plan. Existing reading progress has not changed.'; }
    catch { root.querySelector('[data-start-status]').textContent = 'Storage is unavailable. Use the recommendation link to keep this route, or follow the reading links now.'; }
  });
})();
