(() => {
  const root = document.querySelector('[data-learning-workspace]');
  if (!root) return;
  const catalog = JSON.parse(root.querySelector('[data-learning-catalog]').textContent);
  const form = root.querySelector('[data-plan-form]'), status = root.querySelector('[data-plan-status]'), preview = root.querySelector('[data-plan-preview]');
  const field = name => form.elements.namedItem(name), object = value => value && typeof value === 'object' && !Array.isArray(value);
  const valid = plan => object(plan) && catalog.paths.some(path => path.id === plan.path_id) && [20, 40, 60].includes(plan.session_minutes) && [2, 3, 5].includes(plan.sessions) && typeof plan.goal === 'string' && plan.goal.trim().length > 0 && plan.goal.length <= 300;
  const read = key => { const value = localStorage.getItem(key); return value === null ? null : JSON.parse(value); };
  function drawPlan(plan) {
    preview.hidden = !plan; if (!plan) return;
    const path = catalog.paths.find(path => path.id === plan.path_id);
    let checklist; try { checklist = read(`codepop:learning:${path.id}`); } catch {}
    const remaining = path.step_items.map((step, index) => ({ ...step, index })).filter(step => !object(checklist) || checklist[step.index] !== true);
    root.querySelector('[data-plan-goal]').textContent = plan.goal;
    const list = root.querySelector('[data-plan-sessions]'); list.replaceChildren();
    const perSession = plan.session_minutes / 20;
    for (let index = 0; index < plan.sessions; index++) {
      const item = document.createElement('li'), heading = document.createElement('h4');
      heading.textContent = `Session ${index + 1} · about ${plan.session_minutes} minutes`; item.append(heading);
      const steps = remaining.slice(index * perSession, (index + 1) * perSession);
      if (steps.length) {
        for (const step of steps) { const link = document.createElement('a'), evidence = document.createElement('p'); link.href = `${path.url}#learning-step-${step.index}`; link.textContent = step.title; evidence.textContent = `Keep: ${step.evidence}`; item.append(link, evidence); }
      } else {
        const link = document.createElement('a'); link.href = `${path.url}?review=mistakes#knowledge-title-${path.id}`; link.textContent = 'Review the knowledge check and explain a difficult case →'; item.append(link);
      }
      list.append(item);
    }
    const covered = plan.sessions * perSession;
    if (remaining.length > covered) { const item = document.createElement('li'), count = remaining.length - covered; item.textContent = `${count} further practical ${count === 1 ? 'step remains' : 'steps remain'} after this plan. Adjust the plan when you are ready.`; list.append(item); }
  }
  function drawReview() {
    const list = root.querySelector('[data-review-list]'); list.replaceChildren(); let unavailable = false, unreadable = false, count = 0;
    for (const path of catalog.paths) {
      let answers; try { answers = read(`codepop:knowledge:${path.id}`); } catch (error) { if (error instanceof SyntaxError) unreadable = true; else unavailable = true; continue; }
      if (!object(answers)) continue;
      for (const question of path.questions) {
        const choice = answers[question.id];
        if (!Number.isInteger(choice) || choice < 0 || choice >= question.options || choice === question.answer) continue;
        count++; const item = document.createElement('li'), link = document.createElement('a'), reading = document.createElement('a');
        link.href = `${path.url}?review=mistakes#question-${path.id}-${question.id}`; link.textContent = `${path.title}: ${question.prompt}`;
        reading.href = question.url; reading.textContent = 'Revisit the explanation material →'; item.append(link, reading); list.append(item);
      }
    }
    root.querySelector('[data-review-status]').textContent = unavailable ? 'Storage is unavailable. Open any path below to revisit its knowledge check.' : unreadable ? 'Some quiz records could not be read. Valid choices are shown; saved records have not changed.' : count ? `${count} saved answers to revisit. Correcting a quiz answer updates this list; it never completes a practical step.` : 'No incorrect saved answers to revisit. Unanswered questions are available in each path; this is not proof that a path is complete.';
  }
  const restore = () => {
    try {
      const plan = read('codepop:study-plan');
      if (plan !== null && !valid(plan)) { status.textContent = 'The saved plan is unreadable. It has not been changed; save a new plan to replace it.'; preview.hidden = true; }
      else { if (plan) for (const name of ['goal', 'path_id', 'session_minutes', 'sessions']) field(name).value = String(plan[name]); drawPlan(plan); status.textContent = plan ? 'Plan restored from this browser. Use a workspace backup to move it to another device.' : 'Save a goal to create your session plan.'; }
    } catch (error) { preview.hidden = true; status.textContent = error instanceof SyntaxError ? 'The saved plan is unreadable. It has not been changed; save a new plan to replace it.' : 'Storage is unavailable. You can plan for this visit.'; }
    drawReview();
  };
  form.hidden = false; restore();
  form.addEventListener('submit', event => {
    event.preventDefault(); const plan = { goal: field('goal').value.trim(), path_id: field('path_id').value, session_minutes: Number(field('session_minutes').value), sessions: Number(field('sessions').value) };
    if (!valid(plan)) { status.textContent = 'Choose a listed path and a goal of 1–300 characters.'; return; }
    drawPlan(plan); try { localStorage.setItem('codepop:study-plan', JSON.stringify(plan)); status.textContent = 'Plan saved on this device. Practical progress and quiz answers have not changed.'; } catch { status.textContent = 'Plan ready for this visit. Storage is unavailable; keep a separate copy of your goal.'; }
  });
  root.querySelector('[data-plan-clear]').addEventListener('click', () => { try { localStorage.removeItem('codepop:study-plan'); form.reset(); drawPlan(null); status.textContent = 'Plan removed. Reading progress, notes, quiz answers, and drafts are preserved.'; } catch { status.textContent = 'Could not remove the saved plan. Storage is unavailable.'; } });
  window.addEventListener('storage', restore); window.addEventListener('pageshow', restore);
})();
