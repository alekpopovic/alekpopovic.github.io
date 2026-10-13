"""Boundary tests for nested source selection and native reference handling."""
import importlib.util,tempfile,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('orch_publisher',Path(__file__).resolve().parents[1]/'scripts/build.py');pub=importlib.util.module_from_spec(spec);spec.loader.exec_module(pub)
class AdapterTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.original=pub.ROOT;pub.ROOT=self.root
  self.man=self.root/'manuscript';(self.man/'chapters').mkdir(parents=True);(self.man/'appendices').mkdir()
  self.entries=['00-preface.md']+[f'chapters/{n:02d}-topic.md' for n in range(1,41)]+[f'appendices/{letter.lower()}-reference.md' for letter in 'ABCDEF']
  self.titles=['Preface']+[f'Chapter {n} - Topic' for n in range(1,41)]+[f'Appendix {letter} - Reference' for letter in 'ABCDEF']
  for entry,title in zip(self.entries,self.titles):(self.man/entry).write_text('# '+title+'\n\n## Repeat\nOne.\n\n## Repeat\nTwo.\n')
  self.write_order()
 def tearDown(self):pub.ROOT=self.original;self.tmp.cleanup()
 def write_order(self):(self.man/'Book.txt').write_text('\n'.join(self.entries)+'\n')
 def test_nested_order_and_native_titles(self):
  paths=pub.selection();self.assertEqual(len(paths),47);self.assertEqual(pub.title(paths[40]),'Chapter 40 - Topic');self.assertEqual(pub.title(paths[41]),'Appendix A - Reference')
 def test_traversal_rejected(self):
  (self.root/'outside.md').write_text('# Preface\n');self.entries[0]='../outside.md';self.write_order()
  with self.assertRaises(ValueError):pub.selection()
 def test_symlink_escape_rejected(self):
  outside=self.root/'outside.md';outside.write_text('# Preface\n');(self.man/'00-preface.md').unlink();(self.man/'00-preface.md').symlink_to(outside)
  with self.assertRaises(ValueError):pub.selection()
 def test_duplicate_stem_rejected(self):
  p=self.man/'appendices/01-topic.md';p.write_text('# Appendix A - Reference\n');self.entries[41]='appendices/01-topic.md';self.write_order()
  with self.assertRaises(ValueError):pub.selection()
 def test_wrong_title_grammar_rejected(self):
  (self.man/self.entries[1]).write_text('# Chapter 1: Topic\n')
  with self.assertRaises(ValueError):pub.selection()
 def test_duplicate_heading_ids_and_print_prefix(self):
  p=pub.selection()[1];site=pub.render(p);self.assertIn('id="repeat"',site);self.assertIn('id="repeat-1"',site)
  printed=pub.render(p,'print');self.assertIn('id="01-topic-repeat-1"',printed)
 def test_lifecycle_and_invariant_tables_keep_distinct_column_layouts(self):
  p=self.man/'appendices/b-lifecycle.md'
  p.write_text('# Appendix B - Reference\n\n| From | Allowed | Duplicate |\n| --- | --- | --- |\n| running | stopped | yes |\n\n| ID | Invariant | Scope | Counterexample |\n| --- | --- | --- | --- |\n| I1 | Placement | Memory | Lost process |\n')
  printed=pub.render(p,'print')
  self.assertEqual(printed.count('class="lifecycle-reference"'),1)
  self.assertEqual(printed.count('class="invariant-reference"'),1)
 def test_cross_section_fragment_and_query(self):
  paths=pub.selection();p=paths[1]
  self.assertEqual(pub.target_reference(p,'02-topic.md?q=1#repeat','site',paths),'/books/inside-orch/02-topic.html?q=1#repeat')
  self.assertEqual(pub.target_reference(p,'02-topic.md#repeat','print',paths),'#02-topic-repeat')
  self.assertEqual(pub.target_reference(p,'02-topic.md#repeat','epub',paths),'02-topic.xhtml#repeat')
 def test_companion_and_raw_evidence_boundaries(self):
  paths=pub.selection();p=paths[1];sol=self.man/'solutions/ch01.md';sol.parent.mkdir();sol.write_text('# Worked answers\n')
  self.assertEqual(pub.target_reference(p,'../solutions/ch01.md','site',paths),'/books/inside-orch/companion/manuscript/solutions/ch01.html')
  p.write_text('# Chapter 1 - Topic\n\n[Answers](../solutions/ch01.md)\n');self.assertEqual(pub.companions(),[sol])
  denied=self.root/'evidence/orch/internal.go';denied.parent.mkdir(parents=True);denied.write_text('package internal\n')
  with self.assertRaises(ValueError):pub.target_reference(p,'../../evidence/orch/internal.go','site',paths)
 def test_unsupported_and_missing_historical_path_rejected(self):
  paths=pub.selection();p=paths[1];binary=self.root/'labs/blob.bin';binary.parent.mkdir();binary.write_bytes(b'xx')
  with self.assertRaises(ValueError):pub.target_reference(p,'../../labs/blob.bin','site',paths)
  with self.assertRaises(ValueError):pub.target_reference(p,'renamed-old-chapter.md','site',paths)
 def test_print_companion_fragments_use_unique_document_prefix(self):
  paths=pub.selection();p=self.man/'solutions/ch01.md';p.parent.mkdir();p.write_text('# Answers\n\n## Details\n[Jump](#details)\n')
  rendered=pub.render(p,'print',paths)
  self.assertIn('id="companion-manuscript-solutions-ch01-md-details"',rendered)
  self.assertIn('href="#companion-manuscript-solutions-ch01-md-details"',rendered)
 def test_print_images_use_local_files_without_network_fetch(self):
  paths=pub.selection();p=paths[1];image=self.root/'examples/diagram.svg';image.parent.mkdir();image.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
  p.write_text('# Chapter 1 - Topic\n\n![A checked diagram](../../examples/diagram.svg)\n')
  self.assertIn('src="'+image.as_uri()+'"',pub.render(p,'print',paths))
  self.assertIn('/assets/books/inside-orch/examples/diagram.svg',pub.render(p,'site',paths))
 def test_print_rejects_remote_image_fetches(self):
  paths=pub.selection();p=paths[1];p.write_text('# Chapter 1 - Topic\n\n![Remote](https://example.com/image.png)\n')
  with self.assertRaises(ValueError):pub.render(p,'print',paths)
 def test_offline_companion_links_round_trip_without_root_paths(self):
  paths=pub.selection();p=paths[1];sol=self.man/'solutions/ch01.md';sol.parent.mkdir();sol.write_text('# Answers\n')
  self.assertEqual(pub.target_reference(p,'../solutions/ch01.md#details','offline',paths),'companion/manuscript/solutions/ch01.html#details')
  self.assertEqual(pub.target_reference(sol,'../chapters/01-topic.md#repeat','offline',paths),'../../../01-topic.html#repeat')
if __name__=='__main__':unittest.main()
