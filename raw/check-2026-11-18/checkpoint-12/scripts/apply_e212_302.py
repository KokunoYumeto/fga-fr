from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/e212.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'e212-302',line,'Erratum 212 continuation',
                'Scan leaf 3 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    r(r'\src{302}',r'''\src{302}
\begingroup
\makeatletter
\renewcommand\@makefnmark{\hbox{\normalfont(\textsuperscript{\@thefnmark})}}
\makeatother''','footnote-marker format','The note call and note label use baseline parentheses around a raised numeral 3. The definition is scoped to this continuation.','typesetting')
    r(r'MUMFORD\footnote{',r'MUMFORD\footnote[3]{','note call','The printed note is numbered 3, with its call before the sentence period.','typesetting')
    r(' --- ',' - ','footnote separator','The bibliography separator is short.')
    r(r'\emph{Bull. Amer. Math. Soc.}','Bull. Amer. math. Soc.','journal title','The title is upright and math. begins with a lowercase m.')
    r('483--486','483-486','page range','A short joining dash is printed.')
    r('voir SHMT.',r'voir \uwave{SHMT}.'+'\n'+r'\endgroup','final reference','SHMT has a wavy underline; close the local note-label group.','typesetting')
event('e212-mumford','carried as background without fault found','Completed the authorial report of a theorem of Mumford on the quotient-existence problem and its refinement/applications in SHMT. The footnote gives the exact bibliographic title and pages, but states no theorem hypotheses or conclusion; no stronger result is inferred or claimed checked.','Erratum 212, p. 302, continuation and footnote 3')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='e212-302')
record_page('e212',302,'Compared sources/fr_printed/fr/e212.tex and sources/fr/fr/e212.tex, entry lines 30-35, with scan leaf 3 rendered at 400 dpi, full page and three enlarged bands. Read the continuation, footnote call, final SHMT reference and complete bibliographic footnote. Restored raised 3 within baseline parentheses with a local TeX group, wavy SHMT, upright journal lettering with lowercase math., and short bibliography/page-range dashes. Both layers agree. The theorem and refinement report remains background because this page supplies bibliography but no exact theorem statement.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
