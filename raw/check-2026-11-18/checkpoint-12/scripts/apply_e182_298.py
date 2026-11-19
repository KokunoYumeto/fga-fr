from audit_utils import *
from collections import Counter
import csv
dq=chr(96)*2
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/e182.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'e182-298',line,'Page 8, théorème 6',
                'Scan leaf 2 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    r(r'\textbf{2. Géométrie formelle et géométrie algébrique.}',
      r'2. \uwave{Géométrie formelle et géométrie algébrique}.',
      'title','The ordinary title has a wavy underline, excluding the number and final period.','typesetting')
    r(r'\textbf{Page 8, théorème 6.}',r'\uline{Page 8, théorème 6}.',
      'entry heading','The heading is ordinary text with a straight underline.','typesetting')
    r(' --- ',' - ','entry separator','The dash is short.')
    r('« ',dq,'two quotations','Ordinary double quotation marks are printed.',count=2)
    r(' »',"''",'two quotations','Ordinary double quotation marks are printed.',count=2)
    r('(cf. SGA VIII','(Cf. \\uwave{SGA} VIII','reference','Capital Cf. and wavy-underlined SGA are printed.')
    r(') : tout morphisme',') : Tout morphisme','quoted result','Tout starts with a capital T.')
    r(r'\longrightarrow',r'\to','morphism','The arrow is short.')
    upright_page(rel,layer,'e182-298')
event('e182-th6','carried as background without fault found',
      'Read the weakening of quasi-projective to separated in theorem 6, justified in the erratum by the statement that a quasi-finite separated morphism is quasi-projective, with locator SGA VIII, 6.2. The cited theorem and its hypotheses remain a background input; this page gives no proof. No new alteration of the original theorem is merged into exposé 182.',
      'Erratum 182, p. 298, Page 8, théorème 6')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='e182-298')
record_page('e182',298,'Compared sources/fr_printed/fr/e182.tex and sources/fr/fr/e182.tex, entry lines 5-17, with scan leaf 2 at 400 dpi, full page and three enlarged bands. Read the title, bibliographic bracket and complete first erratum. Restored wavy/straight emphasis, ordinary quotations, capital Cf./Tout, the short morphism arrow and upright variables. The two French layers agree. The weakening of theorem 6 is preserved in this separate erratum, with the cited quasi-finite separated result recorded as background rather than independently proved.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
