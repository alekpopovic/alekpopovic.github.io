#!/usr/bin/env python3
"""Check original Python syntax and deterministic lifecycle art in owned temporary output."""
from pathlib import Path
import ast,hashlib,json,shutil,subprocess,tempfile
from PIL import Image,ImageChops
import cairosvg
B=Path(__file__).resolve().parents[1];paths=list((B/'examples/teaching-extensions').rglob('*.py'))+[B/'examples/diagrams/generate_task_lifecycle.py']
for p in paths:ast.parse(p.read_text(),filename=str(p))
with tempfile.TemporaryDirectory(prefix='inside-orch-diagram-review-')as d:
 root=Path(d);dest=root/'examples/diagrams';dest.mkdir(parents=True);script=dest/'generate_task_lifecycle.py';shutil.copyfile(B/'examples/diagrams/generate_task_lifecycle.py',script)
 subprocess.run(['python3',str(script)],check=True,cwd=root)
 svg=dest/'task-lifecycle.svg';assert svg.read_bytes()==(B/'examples/diagrams/task-lifecycle.svg').read_bytes(),'SVG generator stale'
 original=Image.open(B/'examples/diagrams/task-lifecycle.png').convert('RGBA');png=dest/'task-lifecycle.png';cairosvg.svg2png(url=str(svg),write_to=str(png),output_width=original.width,output_height=original.height)
 fresh=Image.open(png).convert('RGBA');assert fresh.size==original.size;assert ImageChops.difference(fresh,original).getbbox()is None,'PNG raster differs'
print(json.dumps({'status':'passed','python_programs_syntax_checked':len(paths),'svg_regeneration':'byte-identical','png_raster_comparison':'pixel-identical','png_size':original.size,'scope':'Actual isolated diagram generator + raster equality and Python AST syntax. Original teaching scripts have separate semantic execution records.'},indent=2))
