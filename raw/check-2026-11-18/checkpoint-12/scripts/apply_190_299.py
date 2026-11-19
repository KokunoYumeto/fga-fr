from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-299',line,statement,'400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 r(r'12\textsuperscript{e} année','12e année','seminar header','heading',why='The e after 12 is on the baseline.')
 r(r'190\\Décembre 1959',r'190\\\hfill Décembre 1959','seminar date','heading',why='The date is on the right on its own line.')
 txt,_,_=page_text(rel,299)
 for m in re.finditer('« (.*?) »',txt,re.S):r(m.group(0),r'\fquote{'+m.group(1)+'}','quotation '+m.group(1).replace('\n',' '),'introduction',why='The print uses ordinary double quotation marks.')
 for a,b in [('Weil','WEIL'),('Cartier','CARTIER')]:r(a,b,'first paragraph named authors','introduction',why='These surnames are uppercase.',count=2)
 r("À l'heure actuelle","A l'heure actuelle",'second paragraph opening','introduction',why='The initial A has no accent.')
 r('ladite','la dite','second paragraph','introduction',why='The print separates la and dite.')
 r('Kodaira--Spencer','KODAIRA-SPENCER','second paragraph','introduction',why='Uppercase surnames joined by a single short hyphen.')
 r('ci-dessous sont','ci-dessous, sont','third paragraph','introduction',why='The comma after ci-dessous is printed.')
 r('préschémas','pré-schémas','last paragraph','introduction',why='The print uses the internal hyphen.')
 txt,_,_=page_text(rel,299)
 for a,b,body in list(footnotes(txt)):
  r(txt[a:b],'','after the general existence claim','introduction',kind='structure',why='There is no footnote on this page. The supplied note summarizes the author’s later erratum; that erratum must remain in its own section and is not merged into the exposé.')
event('190-introduction-existence','carried as background without fault found','Read the author’s broad claim about descent and formal geometry as methods for existence theorems, and the expectations for analytic analogues and singular moduli. These are introductory programmatic assessments, not precise theorems established on this page. The later-erratum footnote inserted by the supplied edition is removed from both French exposé layers, leaving the later erratum for separate examination in printed order.','190, p. 299, second paragraph')
record_page('190',299,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 3–45 with scan leaf 2 at 400 dpi and all three enlarged bands. Read the seminar header, two-line title, byline and all four introductory paragraphs through et les at the page foot; the next-page marker is correct.

Restored baseline 12e, right-positioned date, ordinary quotation marks, uppercase WEIL/CARTIER/KODAIRA-SPENCER, the short surname hyphen, unaccented initial A, la dite as two words, the comma after ci-dessous and the spelling pré-schémas. Removed the unprinted editorial footnote merging a summary of the later author erratum into the introduction from both layers. No correction of an original mathematical formula occurs on this prose page. The broad historical and programmatic claims are read as such, without treating them as newly proved results.''')
from update_record_counts import update
update()
