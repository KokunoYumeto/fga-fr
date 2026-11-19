from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/149.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'149-192',line,statement,'400-dpi scan and three enlarged page bands. '+why,kind,count=count)
 r(r'\subsection*{REMARQUES}',r'\subsection*{\normalfont REMARQUES.}','heading',why='Roman heading with a final period.')
 r('résolutions finies.',r'résolutions \uline{finies}.','remark 1, line 3','8-rem1',why='The adjective is underlined.')
 r('cohérents, car',r'\uline{cohérents}, car','remark 1, line 5','8-rem1',why='The adjective is underlined.')
 for a in ['A_1','B_1','B_i']:
  r('L('+a+')',r'\underline{L}('+a+')','remarks 1 and 2, resolution symbols','8-rem1;8-rem2',why='The resolution letter L is underlined.')
 r('remplacer un des',r'remplacer \uline{un} des','remark 2, first line','8-rem2',why='Only un is underlined.')
 r(r'=\Extsh_{\Osh_X}^{*}(A,B),',r'=\Extsh_{\Osh_X}^{*}(A,B)','8.8, first row','8.8',why='There is no terminal comma.')
 r(r'=\operatorname{Ext}_{\Osh_X}^{*}(X;A,B).',r'=\operatorname{Ext}_{\Osh_X}^{*}(X;A,B)','8.8, second row','8.8',why='There is no terminal period.')
 r('En particulier, faisant','En particulier faisant','after 8.8','8.8',why='The print has no comma after particulier.')
 r(r'''\[
  T_{0}^{1*}(B)=H^{*}(X,B),
  \qquad
  T_{1}^{0*}(A)=\operatorname{Ext}_{\Osh_X}^{*}(X;A,\Osh_X).
\]''',r'$T_{0}^{1*}(B)=H^{*}(X,B)$, $T_{1}^{0*}(A)=\operatorname{Ext}_{\Osh_X}^{*}(X;A,\Osh_X)$','after 8.8, two identities','8.8','structure','Both identities run in the text, separated by a comma and with no final punctuation.')
 r('degrés positifs et négatifs.',r'degrés positifs \uline{et} négatifs.','remark 3, line 2','8-rem3',why='The conjunction is underlined.')
 if tree=='fr_printed':
  r('On voit sur la formule (8.1)', 'On voit sur la formule (6.1)','remark 3, first line','8-rem3',why='The printed reference reads (6.1). Corrected French retains (8.1): only (8.1) defines the T functors and yields these degree bounds.')
 r('si $s=0$ (et même, sauf erreur, si','si $s=0$, (et sauf erreur même, si','remark 3, penultimate line','8-rem3',why='Restore the printed word order and comma.')
 r(r'\section*{BIBLIOGRAPHIE}',r'\section*{\centering\normalfont BIBLIOGRAPHIE}','bibliography heading',why='The heading is centered and roman.')
 for old,new,n in [('Cartier (Pierre). ---','CARTIER (Pierre). -',1),('Grothendieck (Alexandre). ---','GROTHENDIECK (Alexandre). -',1),('Serre (Jean-Pierre). ---','SERRE (Jean-Pierre). -',2)]:
  r(old,new,'bibliography author labels',why='Surnames are uppercase, followed by a short dash.',count=n)
 for old,new in [(r'\emph{Tohoku Math. J.}','Tohoku math. J.'),(r'\emph{Annals of Math.}','Annals of Math.'),(r'\emph{Proc. Intern. Symp. on Alg. Number Theory}','Proc. Intern. Symp. on alg. number Theory'),('[1955, Tokyo et Nikko]. ---','[1955. Tokyo et Nikko] -')]:
  r(old,new,'bibliography entries 2–4',why='Restore the roman type, original capitalization and punctuation visible in the scan.')
 for a,b in [('119--183','119-183'),('197--278','197-278'),('175--189','175-189')]:
  r(a,b,'bibliography page ranges',why='The printed ranges use short hyphens.')
 upright_page(rel,layer,'149-192')
event('149-8-rem1','carried as background without fault found','Read the extension to infinite resolutions and the warning on coherence. No general unbounded-totalization comparison has been proved in this pass; that claim requires separate conventions and hypotheses.','149, p. 192, remark 1')
event('149-8.8','targeted proof check','For bounded locally free resolutions on the nonsingular X, replacing one covariant resolution by its sheaf preserves the complex up to quasi-isomorphism. With r=s=1 the defining internal Hom computes sheaf Ext and hypercohomology computes global Ext. Setting A=O_X recovers cohomology, and the empty covariant tensor is O_X.','149, p. 192, remark 2 and (8.8)')
event('149-8-rem3','targeted proof check','The reference printed (6.1) must be (8.1), the definition of T. Replacing one of s positive-side resolutions by its sheaf leaves degree range [-(s-1)n,rn]; when s=0 the range is [0,rn]. Hypercohomology adds at most n. The stronger final bound is explicitly tentative in the print and is carried without an independent proof here.','149, p. 192, remark 3')
record_page('149',192,r'''Compared sources/fr_printed/fr/149.tex entry lines 1263–1325 and sources/fr/fr/149.tex entry lines 1273–1335 with scan leaf 25 at 400 dpi and three enlarged bands, including all indices, degree bounds, references and bibliography punctuation.

Restored underlined finies, cohérents, un and et, underlined resolution L, roman heading typography, the inline identities after (8.8), omitted display punctuation, original parenthetical word order, and the bibliography's uppercase surnames, roman journals, original capitalization, short dashes and date punctuation. The printed (6.1) in remark 3 is retained in fr_printed; the existing corrected reading (8.1) is confirmed by the defining formula and degree calculation. The unbounded extension in remark 1 and the expressly tentative stronger bound at the end of remark 3 are not certified as independently proved.''')
from update_record_counts import update
update()
