import fs from 'node:fs';
import postcss from 'postcss';
import tailwind from '@tailwindcss/postcss';
import selectors from 'postcss-selector-parser';

const prune = (css, known) => {
  known.add('not-prose');
  const tree = postcss.parse(css);
  tree.walkRules(rule => {
    if (rule.parent.type === 'atrule' && /keyframes$/i.test(rule.parent.name)) return;
    for (let parent = rule.parent; parent; parent = parent.parent) if (parent.type === 'atrule' && parent.name === 'layer' && ['utilities', 'base', 'theme', 'properties'].includes(parent.params)) return;
    const ast = selectors().astSync(rule.selector);
    for (const selector of [...ast.nodes]) {
      let keep = true;
      selector.walkClasses(node => {
        for (let parent = node.parent; parent; parent = parent.parent) if (parent.type === 'pseudo' && parent.value === ':not') return;
        if (!known.has(node.value)) keep = false;
      });
      if (!keep) selector.remove();
    }
    if (!ast.nodes.length) rule.remove(); else rule.selector = ast.toString();
  });
  return tree.toString();
};
const words = files => new Set(files.flatMap(file => fs.readFileSync(file, 'utf8').match(/[a-zA-Z_][\w:-]*/g) || []));
const sources = fs.readdirSync('.').filter(file => file.endsWith('.html'));
for (const directory of ['_layouts', '_includes', '_posts', 'book-pages', 'learn', 'ai', 'projects', 'codepop', 'newsletter', 'assets/js']) {
  if (fs.existsSync(directory)) sources.push(...fs.readdirSync(directory, { recursive: true }).filter(file => /\.(html|md|js)$/.test(file)).map(file => `${directory}/${file}`));
}
const allClasses = words(sources);
// Book overview classes are emitted by the Jekyll generator, rather than
// present literally in a source template. Keep every catalogued variant.
for (const book of JSON.parse(fs.readFileSync('_data/books.json', 'utf8'))) allClasses.add(`book-feature-${book.id}`);
for (const name of ['site', 'ai', 'reader']) {
  const from = `src/${name === 'site' ? 'input' : name}.css`, to = `assets/css/${name}.css`;
  const output = await postcss([tailwind({ optimize: { minify: true } })]).process(fs.readFileSync(from, 'utf8'), { from, to, map: false });
  fs.writeFileSync(to, (name === 'site' ? prune(output.css, allClasses) : output.css).trim() + '\n');
}
// Tailwind 4 keeps custom component rules. Prune the reader shell by the actual
// classes in its shared templates and scripts, preserving global/base rules.
const files = ['_layouts/default.html', '_layouts/book.html', '_includes/footer.html', '_includes/icon.html', '_includes/flower.html', '_includes/share-links.html', '_includes/content-feedback.html', '_data/footer.yml', 'assets/js/site.js', 'assets/js/share.js', 'assets/js/reader.js', 'assets/js/reader-library.js'];
fs.writeFileSync('assets/css/reader-shell.css', prune(fs.readFileSync('assets/css/site.css', 'utf8'), words(files)));
const aiFiles = [...files, 'ai.html', 'ai/workshops.html', '_includes/ai-article.html', '_includes/post-card.html', '_includes/workshop-lab.html', '_includes/post-art.html', 'assets/js/article.js', 'assets/js/ai.js'];
fs.writeFileSync('assets/css/ai-shell.css', prune(fs.readFileSync('assets/css/site.css', 'utf8'), words(aiFiles)));
fs.writeFileSync('assets/css/ai-cards.css', prune(fs.readFileSync('assets/css/ai.css', 'utf8'), words([...files, 'index.html', 'posts.html', '_includes/post-card.html'])));
console.log('Built local Tailwind 4 styles and the shared reader shell.');
