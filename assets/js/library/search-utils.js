(() => {
  const normalize = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const terms = query => [...new Set(normalize(query).trim().split(/\s+/).filter(Boolean))].slice(0, 12);
  // Map folded characters to original offsets so accented text stays intact.
  const ranges = (text, query) => {
    let folded = '', offset = 0; const starts = [], ends = [];
    for (const character of text) { const value = normalize(character); for (let i = 0; i < value.length; i++) { starts.push(offset); ends.push(offset + character.length); } folded += value; offset += character.length; }
    const found = [];
    for (const term of terms(query)) { let position = 0, at; while ((at = folded.indexOf(term, position)) >= 0 && found.length < 500) { found.push([starts[at], ends[at + term.length - 1]]); position = at + term.length; } }
    found.sort((a, b) => a[0] - b[0]); const merged = [];
    for (const range of found) { const last = merged[merged.length - 1]; if (last && range[0] <= last[1]) last[1] = Math.max(last[1], range[1]); else merged.push(range); }
    return merged;
  };
  const highlight = (node, text, query) => {
    let offset = 0;
    for (const [start, end] of ranges(text, query)) { node.append(document.createTextNode(text.slice(offset, start))); const mark = document.createElement('mark'); mark.textContent = text.slice(start, end); node.append(mark); offset = end; }
    node.append(document.createTextNode(text.slice(offset)));
  };
  const excerpt = (text, query, fallback = '') => {
    const first = ranges(text, query)[0]; if (!first) return fallback || text.slice(0, 230);
    const start = Math.max(0, first[0] - 65), end = Math.min(text.length, start + 240);
    return `${start ? '…' : ''}${text.slice(start, end)}${end < text.length ? '…' : ''}`;
  };
  window.CodepopSearch = { normalize, terms, ranges, highlight, excerpt };
})();
