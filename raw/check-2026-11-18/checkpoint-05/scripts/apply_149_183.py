from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/149.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'149-183',line,statement,'400-dpi page and enlarged top, middle and bottom crops. '+why,kind,count=count)
 if tree=='fr_printed':
  txt,_,_=page_text(rel,183)
  for a,b,body in list(footnotes(txt)):
   r(txt[a:b],'','editorial notes','5',kind='structure',why='These explanatory footnotes belong to the corrected edition; neither is printed on this page.')
  r('Comme (5.3 bis)','Comme (5.3)','line 1','5.3-bis',why='The printed reference is to the repeated label 5.3; corrected French retains the disambiguated reference.')
  r(r"\Osh_P(m+m')",r"\Osh_P(r+r')",'cup-product target','5-lem2',why='The image reads r+r prime. Corrected French retains m+m prime because twisting degrees add under tensor product.')
 old="La computation du cup-produit\n\\[\n  H^{i}(P,\\Osh_P(m))\\times H^{j}(P,\\Osh_P(m'))\n  \\longrightarrow H^{i+j}(P,\\Osh_P("+('r+r' if tree=='fr_printed' else 'm+m')+"'))\n\\]\nnécessaire"
 new="La computation du cup-produit $H^{i}(P,\\Osh_P(m))\\times H^{j}(P,\\Osh_P(m'))\\longrightarrow H^{i+j}(P,\\Osh_P("+('r+r' if tree=='fr_printed' else 'm+m')+"'))$ nécessaire"
 r(old,new,'Lemma 2 proof, cup product','5-lem2','structure','The cup product runs in the sentence, without a separate display.')
 r(r"L'énoncé (D) est vrai si $X=P$ et $F=\Osh_P(m)$.",r"\uline{L'énoncé} (D) \uline{est vrai si} $X=P$ \uline{et} $F=\Osh_P(m)$",'Lemma 2','5-lem2',why='The prose is underlined except D, and there is no terminal full stop.')
 old="on a\n\\[\n  \\operatorname{Ext}_{\\Osh_X}^{i}(X;\\Osh_X(-m),B)=0\n\\]\npour"
 new="on a $\\operatorname{Ext}_{\\Osh_X}^{i}(X;\\Osh_X(-m),B)=0$ pour"
 r(old,new,'Lemma 4','5-lem4','structure','The Ext vanishing runs inline with the statement.')
 for label in [r'\result{LEMME}{3} ',r'\result{LEMME}{4} ',r'\result{COROLLAIRE}{} ']:
  txt,_,_=page_text(rel,183);start=txt.index(label)+len(label);stop=txt.index('\n\n',start);old=txt[start:stop]
  r(old,underline_prose(old),label,'5',why='Restore the statement prose underlining, excluding mathematical variables.')
 r('« engendré par ses sections »',r'\fquote{engendré par ses sections}','Lemma 3 proof','5-lem3',why='Ordinary double quotation marks are printed.')
 r('plus haut ; pour le','plus haut, pour le','Lemma 4 proof','5-lem4',why='The scan has a comma here, not a semicolon.')
 r(r'=H^{i}(X,B\otimes\Osh_X(m))',r'=H^{i}(X,B\otimes\Osh(m))','Lemma 4 proof display','5-lem4',why='The last O has no X subscript in print; this is unambiguous shorthand on X, so both layers retain it.')
 r(r'F\longmapsto H^{r-i}',r'F\longrightarrow H^{r-i}','Corollary','5-cor-lem4',why='The printed functor arrow has no mapsto bar.')
 r('k_x',r'\underline{k}_x','line 2','5.5',why='The point-sheaf k is underlined.')
 txt,_,_=page_text(rel,183);r(r'\Omega',r'\underline{\Omega}','first paragraph','5.5',why='Both differential-sheaf Omegas are underlined.',count=txt.count(r'\Omega'))
 upright_page(rel,layer,'149-183')
event('149-5-D-to-thm2','targeted proof check','Under D, Ext^n(k_x,Omega) is H^0(k_x) dual tensor L. The point Ext group has the fundamental section as a basis by (4.2), so L is nonzero and one-dimensional. Naturality identifies evaluation with (5.5); the fundamental point class is therefore a basis. This also justifies the nonzero tensor factor implicit in passing from (5.4) to (5.5).','149, p. 183, first paragraph')
event('149-5-lem2','targeted proof check','The two line bundles in the displayed-as-inline cup product have twists m and m prime; their tensor product has twist m+m prime, not the printed r+r prime. The supplied correction is confirmed. The full projective-space cohomology computation is left by the author to an explicit calculation and was not independently completed here.','149, p. 183, Lemma 2 proof')
event('149-5-lem3','carried as background without fault found','Read the quotient by a sufficiently negative finite sum of twists and its stated reduction to global generation in [3].','149, p. 183, Lemma 3')
event('149-5-lem4','targeted proof check','The locally free first argument gives Ext^i(O(-m),B)=H^i(B tensor O(m)); hence the sign of m in both the statement and proof agrees. The vanishing theorem from [3] is carried as background.','149, p. 183, Lemma 4')
event('149-5-cor-lem4','targeted proof check','Lemma 3 supplies a surjection from a finite sum of O(-m), and Lemma 4 makes the value of each functor on that source zero for i>0. This is the stated coeffaceability in each variance.','149, p. 183, Corollary')
record_page('149',183,r'''Compared sources/fr_printed/fr/149.tex entry lines 752–809 and sources/fr/fr/149.tex entry lines 755–812 against scan leaf 16 at 400 dpi, followed by enlarged crops of every page band. Read the end of the deduction of Theorem 2, Lemmas 2–4 and their Corollary.

Both layers restore the inline cup product and Ext-vanishing formula, prose underlining, the ordinary functor arrow, double quotes, a comma in the proof of Lemma 4, and the unindexed O(m) shorthand in that proof. Printed French removes two editorial footnotes and restores the reference (5.3) and the twist r+r prime. Corrected French retains the existing number disambiguation and the justified m+m prime twist. The first-paragraph point-class argument and the Ext/twist signs were checked explicitly; the projective-space calculation and Serre vanishing are not represented as independently re-proved.''')
from update_record_counts import update
update()
