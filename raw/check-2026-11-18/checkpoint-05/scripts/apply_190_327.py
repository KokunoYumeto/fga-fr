from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,kind='reading',count=1):
  replace(rel,a,b,layer,'190-327',line,'Bibliography','400-dpi full scan and three enlarged bands: restore the literal bibliography, roman type, capitals, accents, short dashes and numbering.',kind,count=count)
 r(r'\textbf{BIBLIOGRAPHIE}','BIBLIOGRAPHIE.','heading')
 for i in range(1,7):
  r(r'\item[{['+str(i)+r']}]',r'\item[{\normalfont['+str(i)+r']}]',f'entry [{i}] label')
 for old,new,line in [
  ('Dieudonné (J.) et Grothendieck (Alexander). ---','DIEUDONNÉ (J.) et GROTHENDIECK (Alexander). -','entry [1] authors'),
  ('Grauert (H.) und Remmert (R.). ---','GRAUERT (H.) und REMMERT (R.). -','entry [2] authors'),
  ('Grothendieck (Alexander). ---','GROTHENDIECK (Alexander). -','entry [3] author'),
  ('Murre (J. P.). ---','MURRE (J. P.). -','entry [4] author'),
  ('Serre (Jean-Pierre). --- \\emph{Géométrie','SERRE (Jean-Pierre). - \\emph{Géométrie','entry [5] author'),
  ('Serre (Jean-Pierre). --- \\emph{Espaces','SERRE (Jean-Pierre). - \\emph{Espaces','entry [6] author'),
  ('Éléments\n    de géométrie algébrique','Eléments\n    de géométrie algébrique','entry [1] title initial'),
  ('Hautes Études Scientifiques','Hautes Etudes Scientifiques','entry [1] institution'),
  ('245--318','245-318','entry [2] page range'),
  ('no 182',r'n\textsuperscript{o} 182','entry [3] number'),
  ('3--15','3-15','entry [4] page range'),
  ('1955--56','1955-56','entry [5] date'),
  ('1--42','1-42','entry [5] page range'),
  ('no 1.',r'n\textsuperscript{o} 1.','entry [6] number')]:
  r(old,new,line)
 s,_,_=page_text(rel,327)
 for i,m in enumerate(list(re.finditer(r'\\emph\{([^{}]*)\}',s,re.S)),1):
  r(m.group(0),m.group(1),f'entry [{i}] title font')
 r('\\par\\smallskip\n\\begingroup\\footnotesize\n\\endgroup','\\begin{center}\n  \\rule{.14\\linewidth}{.3pt}\n\\end{center}','closing rule','structure')
ledger=ROOT/'CORRECTIONS.tsv'
with ledger.open(newline='') as f:
 rows=list(csv.DictReader(f,delimiter='\t'))
hits=0
for row in rows:
 if row['file']=='sources/fr/fr/190.tex' and row['printed_page']=='190-325' and row['line']=='second reference' and row['kind']=='misprint of the original':
  row['evidence']='The 400-dpi scan of 325 has [1]. On 327 entry [1] is Dieudonné–Grothendieck, Eléments de géométrie algébrique, whereas [6] is Serre, Espaces fibrés algébriques. The same terminology is cited as Serre [6] earlier on 325. The corrected target [6] is therefore confirmed by this bibliography; final row-by-row visual review remains pending.'
  hits+=1
if hits!=1: raise ValueError(f'Expected one provisional reference row, found {hits}')
with ledger.open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=FIELDS,delimiter='\t');w.writeheader();w.writerows(rows)
rec=read('CHECK_RECORD.md')
rec=rec.replace('corrected French provisionally retains [6], to be settled against the bibliography on 327.','corrected French retains [6]. The later reading of bibliography 327 confirmed this target: [1] is the EGA reference and [6] is Serre, Espaces fibrés algébriques.')
write('CHECK_RECORD.md',rec)
event('190-B6-Serre-reference','targeted proof check','The internal bibliography settles the erroneous [1] after the isotriviality terminology on 325: item [1] is Dieudonne–Grothendieck, Elements de geometrie algebrique, and item [6] is Serre, Espaces fibres algebriques. The prior citation of Serre on 325 already points to [6]. Thus the corrected reference is [6], while the printed layer retains [1]. This is a check of the reference target, not a claim that the cited article has been read.','190, p. 325, second Serre citation; p. 327, entries [1] and [6]')
record_page('190',327,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 1439–1463 with scan leaf 30 at 400 dpi, full page and all three enlarged bands. Read every author, title, accent, volume, year, range, abbreviation and reference number; the lower bands also confirm the closing rule and otherwise blank remainder.

Restored the heading period and roman font, ordinary bibliography labels and titles, author capitals, unaccented initial E in Eléments and Etudes, short dashes, raised abbreviation o and the closing rule. Both layers have the same bibliography. The previously provisional [1] to [6] correction on 325 is now justified by these entries; its ledger evidence and page record were updated without changing the printed layer. No external bibliography or edition was consulted.''')
from update_record_counts import update
update()
