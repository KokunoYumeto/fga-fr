"""Render one authorized scan page for the reader; performs no textual adjudication."""
from pathlib import Path
import argparse, subprocess, sys
from PIL import Image
from audit_utils import page_text
p=argparse.ArgumentParser()
p.add_argument('expose'); p.add_argument('page',type=int)
p.add_argument('--workspace',type=Path,default=Path.cwd())
a=p.parse_args(); w=a.workspace
first={'149':169,'182':193,'190':299,'195':369,'212':99,'221':249,'232':143,'236':221,'com':297,'e149':298,'e182':298,'e190':300,'e195':300,'e212':301,'e221':302,'e232':303,'e236':303}
pdfs=list((w/'inputs/scans').glob(f'FGA_{a.expose}_*.pdf'))
if len(pdfs)!=1: raise ValueError('Expected exactly one scan item')
out=w/'tmp/renders'; out.mkdir(parents=True,exist_ok=True)
stem=out/f'{a.expose}-{a.page}'
leaf=a.page-first[a.expose]+2
subprocess.run(['pdftoppm','-f',str(leaf),'-l',str(leaf),'-r','400','-png','-singlefile',str(pdfs[0]),str(stem)],check=True)
im=Image.open(stem.with_suffix('.png')); W,H=im.size
cropdir=w/'tmp/crops';cropdir.mkdir(parents=True,exist_ok=True)
for name,y0,y1 in [('top',.06,.39),('middle',.36,.69),('bottom',.66,.97)]:
    crop=im.crop((int(W*.055),int(H*y0),int(W*.965),int(H*y1)))
    crop.resize((int(crop.width*1.3),int(crop.height*1.3))).save(cropdir/f'{a.expose}-{a.page}-{name}.png')
for tree in ['fr_printed','fr']:
    rel=f'sources/{tree}/fr/{a.expose}.tex'
    try:
        text,lo,hi=page_text(rel,a.page)
        print(f'{rel}, current lines {lo}–{hi}\n{text}')
    except FileNotFoundError:
        print('Source item filename needs explicit mapping',file=sys.stderr)
