from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/212.tex'
 def r(a,b,line,why,kind='reading',count=1):
  replace(rel,a,b,layer,'212-118',line,'Bibliography','Scan leaf 21 at 400 dpi, full page and all enlarged bands: '+why,kind=kind,count=count)
 r(r'\section*{BIBLIOGRAPHIE}',r'\begin{center}BIBLIOGRAPHIE\end{center}','heading','The heading is centered in ordinary upright capitals, not a bold section heading.')
 for i in range(1,4):
  r(r'\item[{['+str(i)+r']}]',r'\item[{\normalfont['+str(i)+r']}]',f'entry [{i}] label','The bracketed numeral has ordinary weight.')
 s,_,_=page_text(rel,118)
 for i,m in enumerate(list(re.finditer(r'\\item.*?(?=\\item|\\end\{description\})',s,re.S)),1):
  old=m.group(0);new=old.replace('---','-')
  if old!=new:r(old,new,f'entry [{i}] punctuation','Each author separator, and the Paris separator in [3], is a short single dash.')
 r('\\par\\smallskip\n\\begingroup\\footnotesize\n\\endgroup','\\begin{center}\n  \\rule{.14\\linewidth}{.3pt}\n\\end{center}','closing rule','A short centered rule closes the bibliography; the rest of the page is blank.','structure')
 upright_page(rel,layer,'212-118')
record_page('212',118,r'''Compared sources/fr_printed/fr/212.tex entry lines 879-905 and sources/fr/fr/212.tex entry lines 885-911 with scan leaf 21 at 400 dpi, full page and all three enlarged bands. The final three prose lines, the heading, every bibliography word, name, date, number and punctuation mark, and the closing rule were read.

Both layers restore the centered ordinary-weight heading, three ordinary-weight reference labels, the short separators in the three entries, the closing rule and upright G. Nine operations per layer: eight reading and one structure. The bibliography points to exposés 190 and 195 and EGA I with the printed years, page counts and volume number. No external edition was consulted; no mathematical emendation is introduced here.''')
from update_record_counts import update
update()
