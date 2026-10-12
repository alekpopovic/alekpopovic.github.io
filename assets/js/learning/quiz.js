(() => {
  for (const root of document.querySelectorAll('[data-knowledge-check]')) {
    const key = `codepop:knowledge:${root.dataset.knowledgeCheck}`, questions = [...root.querySelectorAll('[data-question]')];
    const status = root.querySelector('[data-knowledge-status]');
    let available = true, checked = false;
    const choices = () => Object.fromEntries(questions.flatMap(question => { const choice = question.querySelector('input:checked'); return choice ? [[question.dataset.question, Number(choice.value)]] : []; }));
    const save = () => { try { localStorage.setItem(key, JSON.stringify(choices())); } catch { available = false; } };
    const draw = () => {
      let correct = 0, answered = 0;
      for (const question of questions) {
        const choice = question.querySelector('input:checked'), result = question.querySelector('[data-question-result]');
        if (choice) answered++;
        const right = choice && choice.value === question.dataset.answer;
        if (right) correct++;
        result.hidden = !checked;
        result.textContent = !choice ? 'Choose an answer before checking this scenario.' : right ? 'Correct. Explain why the other choices fail.' : 'Try again. Read the explanation and revisit the linked material.';
        if (checked) question.dataset.result = right ? 'correct' : 'retry'; else delete question.dataset.result;
      }
      status.textContent = `${answered} of ${questions.length} answered${checked ? ` · ${correct} correct` : ''}. ${available ? 'Choices saved on this device.' : 'Storage unavailable; choices work for this visit.'}`;
    };
    try {
      const stored = JSON.parse(localStorage.getItem(key));
      if (stored && typeof stored === 'object' && !Array.isArray(stored)) for (const question of questions) {
        const value = stored[question.dataset.question];
        if (Number.isInteger(value)) { const choice = [...question.querySelectorAll('input')].find(input => Number(input.value) === value); if (choice) choice.checked = true; }
      }
    } catch { available = false; }
    root.querySelector('[data-knowledge-controls]').hidden = false; status.hidden = false; draw();
    root.addEventListener('change', () => { checked = false; save(); draw(); });
    root.querySelector('form').addEventListener('submit', event => {
      event.preventDefault(); checked = true; save(); draw();
      const missing = questions.find(question => !question.querySelector('input:checked'));
      if (missing) missing.querySelector('input').focus();
    });
    root.querySelector('[data-knowledge-reset]').addEventListener('click', () => { root.querySelector('form').reset(); checked = false; save(); draw(); questions[0].querySelector('input').focus(); });
  }
})();
