from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/149.tex'
 def r(a,b,line,kind='reading',why=''):
  replace(rel,a,b,layer,'149-193',line,'Additif','400-dpi scan and enlarged top band. '+why,kind)
 r(r'\section*{ADDITIF}',r'\section*{\centering\normalfont ADDITIF}','heading',why='Centered roman heading.')
 r('« théorie des schémas »',r'\fquote{théorie des schémas}','paragraph, line 4',why='The source uses ordinary double quotation marks.')
 r('« Éléments de Géométrie algébrique »',r'\fquote{Eléments de Géométrie algébrique}','paragraph, lines 4–5',why='The initial uppercase E is unaccented; the title is enclosed by ordinary double quotes.')
 r('J. Dieudonné et A. Grothendieck','J. DIEUDONNÉ et A. GROTHENDIECK','paragraph, line 5',why='Both surnames are uppercase; the accent on DIEUDONNÉ is visible.')
 r('Grothendieck (A.). ---','GROTHENDIECK (A.). -','reference, first line',why='Uppercase surname and short dash.')
 r(r'\emph{Congrès int. des Mathématiciens}','Congrès int. des Mathématiciens','reference, lines 1–2',why='The proceedings title is roman.')
 r('(à paraître).','(A paraître).','reference, second line',why='The parenthesis begins with an unaccented capital A in the print.')
event('149-additif','carried as background without fault found','Read the April 1959 announcement extending duality to arbitrary singular varieties and schemes. The claim is an announcement, not a proof in this page; its historical and later-literature comparison is deferred to the notes stage. The internal page reference 13 is retained as printed.','149, p. 193, Additif')
record_page('149',193,r'''Compared sources/fr_printed/fr/149.tex entry lines 1319–1342 and sources/fr/fr/149.tex entry lines 1329–1352 with scan leaf 26 at 400 dpi and all three enlarged bands. The text occupies the top band; the remaining bands show the closing rule and page number only.

Restored the centered roman heading, ordinary double quotation marks, unaccented initial E of Eléments, uppercase author surnames, roman proceedings title, short dash and printed capital A in (A paraître). The date, paragraph structure, citation, closing rule and internal page reference 13 were confirmed. Both French layers have identical readings here; no correction of the original is asserted. This completes the first French comparison of all 25 pages of exposé 149; translations and the final second reading are still pending.''')
from update_record_counts import update
update()
