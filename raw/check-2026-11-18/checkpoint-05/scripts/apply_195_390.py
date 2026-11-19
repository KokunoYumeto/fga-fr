from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/195.tex'
 def r(a,b,line,kind='reading',count=1):
  replace(rel,a,b,layer,'195-390',line,'Bibliography','400-dpi full scan and all three enlarged bands: literal bibliography typography, capitals, punctuation and closing rule.',kind,count=count)
 r(r'\textbf{BIBLIOGRAPHIE}','BIBLIOGRAPHIE','heading font')
 for i in range(1,5):
  r(r'\item[{['+str(i)+r']}]',r'\item[{\normalfont['+str(i)+r']}]',f'entry [{i}] label')
 r('Grothendieck (Alexander). ---','GROTHENDIECK (Alexander). -','entries [1]–[3] author and dash',count=3)
 r('Serre (Jean-Pierre). ---','SERRE (Jean-Pierre). -','entry [4] author and dash')
 r('Tohoku Math. J.','Tohoku math. J.','entry [1] journal capitalization')
 r('119--221','119-221','entry [1] short page-range dash')
 s,_,_=page_text(rel,390)
 for i,m in enumerate(list(re.finditer(r'\\emph\{([^{}]*)\}',s,re.S)),1):
  r(m.group(0),m.group(1),f'entry [{i}] title font')
 r('\\par\\smallskip\n\\begingroup\\footnotesize\n\\endgroup','\\begin{center}\n  \\rule{.14\\linewidth}{.3pt}\n\\end{center}','closing rule','structure')
record_page('195',390,r'''Compared sources/fr_printed/fr/195.tex entry lines 1025–1046 and sources/fr/fr/195.tex entry lines 1026–1047 with scan leaf 23 at 400 dpi, full page and all three enlarged bands. Read all four entries, every year, issue, page range and exposé number; the enlarged lower regions confirm the closing rule and otherwise blank remainder.

Both layers restore a roman heading without a final period, ordinary-weight labels and titles, uppercase surnames, short author and page-range dashes, lower-case math. in Tohoku math. J., and the closing rule. The bibliographic targets [1] Tôhoku, [2] exposé 182, [3] exposé 190 and [4] Serre 185 match the identifications used in this exposé. This verifies the internal references, without consulting another edition or claiming that the external Serre article has been read. No new mathematical correction is made on this bibliography page.''')
from update_record_counts import update
update()
