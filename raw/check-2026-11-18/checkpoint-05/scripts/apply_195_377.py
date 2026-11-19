from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/195.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'195-377',line,'A.5 / B.1','400-dpi full scan and three enlarged bands. '+why,kind,count=count)
 r('de nature cohomologique.','de nature \\uline{cohomologique}.','opening continuation',why='Printed selective underline.')
 r(r'\emph{anneaux'+'\nde définition}',r'\uline{anneaux de définition}','rings of definition',why='Printed underline, not italic.')
 r('un plus petit sous-anneau','un \\uline{plus petit} sous-anneau','minimal defining ring',why='Only plus petit is underlined.')
 r("l'anneau de définition de l'objet $\\xi\\in F(A)$", "l'\\uline{anneau de définition de l'objet} $\\xi\\in F(A)$",'definition phrase',why='The printed phrase is underlined after the initial elision.')
 r('près\néquivalentes au fait','près \\uline{équivalentes} au fait','qualified converse',why='Printed selective underline.')
 r(r"\fsection{B}{Les deux théorèmes d'existence}",r"\fsection{\normalfont B}{\normalfont\uline{Les deux théorèmes d'existence}.}",'section B heading',why='Roman underlined title and final period.')
 r(r'F:\mathcal C\longrightarrow(\operatorname{Ens}) ;',r'F:\mathcal C\longrightarrow(\operatorname{Ens})','opening functor display',why='No semicolon is printed after the display.')
 r('pro-représentable, i.e.','pro-représentable, i. e.','criterion introduction',why='Printed abbreviation spacing.')
 r('proposition 3.1,','proposition 3, 1.,','corollary reference punctuation',why='The print has the comma-numbered 3, 1 followed by a period and comma; both are retained.')
 r('exact à gauche. Dans','\\uline{exact à gauche}. Dans','criterion emphasis',why='Printed selective underline.')
 r('technique de descente (cf.','technique de descente, (cf.','historical question reference',why='A comma precedes the parenthesis.')
 r('[3], p. 9), ce critère','[3], p. 9) ce critère','historical question reference end',why='No comma follows the parenthesis.')
 r(r'\item[(i)]',r'\item[i.]','first condition label',why='Printed roman label followed by a period.')
 r(r'\item[(ii)] pour',r'\item[ii.] Pour','second condition label and initial',why='Printed roman label and capital Pour.')
 r('([3], A, définition 1.2),','([3] A, définition 1, 2.),','exactness reference',why='The scan has no comma after [3], a comma-numbered 1, 2 and a period inside the closing parenthesis. Definition 1.2 in exposé 190 defines exactness for sets; that reference is meaningful for the underlying ring diagram.')
 s,_,_=page_text(rel,377)
 r(r'\mathcal C',r'\text{\uwave{C}}','category letters',count=s.count(r'\mathcal C'),why='The category is upright C with a wavy underline.')
 upright_page(rel,layer,'195-377')

event('195-A5-rings-of-definition','targeted proof check','An element xi corresponds to a continuous Lambda-algebra map phi:O to A. Its image A-prime is a finite-length Lambda-submodule and a subalgebra, hence an object of C. The induced map to A-prime represents a lift of xi; uniqueness follows from injectivity of A-prime to A. Any other defining subalgebra contains the image, so this is the least one. For u:A to B, image(u composed with phi)=u(image phi), proving the stated compatibility. The approximate converse needs additional axioms: the constant two-element functor has least defining subalgebras and compatible unique lifts but does not preserve the terminal object or finite products, so it is not pro-representable. The text already says a peu de choses pres, and no exact converse is attributed to it.','195, p. 377, rings-of-definition paragraph')
event('195-B1-necessity','targeted proof check','A pro-representable functor is left exact by A.3, so it preserves finite products and every equalizer diagram of the displayed special form. The two ring maps from A-prime to its tensor square send a to a tensor 1 and 1 tensor a. This tensor square remains a finite-length Lambda-algebra, since it is a quotient of the Lambda tensor product of two finite-length algebras. Expose 190, A, Definition 1.2 supplies exactness of the underlying sets, which agrees with the equalizer in this algebra category. The statement continues on page 378; sufficiency is not claimed before reading that continuation and proof.','195, p. 377, Theorem 1, conditions i–ii and both displayed diagrams')
event('195-A5-obstruction-prospect','carried as background without fault found','The continuation calls the obstruction problem cohomological but specifies neither the deformation problem nor the group on this page. No particular obstruction group or vanishing theorem is inferred. Such identifications require the individual applications discussed later.','195, pp. 376–377, sentence spanning the page boundary')
record_page('195',377,r'''Compared sources/fr_printed/fr/195.tex entry lines 405–453 and sources/fr/fr/195.tex entry lines 406–454 with scan leaf 10 at 400 dpi, full page and all three enlarged bands. Read every prime, xi/eta, both maps on defining rings, all tensor-square indices and arrows, and the three internal references.

Both layers restore the selective underlines, roman section heading and item labels, capital Pour, spaced abbreviation, unpunctuated functor display, exact reference punctuation (including the printed period-comma after 3, 1), wavy C and upright letters. The reference to exposé 190, A, Definition 1, 2 is retained: it is the underlying-set exactness definition and is appropriate here. No mathematical difference between the French layers was introduced.

Checked the least defining ring as the image of O and its compatibility with a homomorphism of target algebras. Recorded what the qualified approximate converse leaves out, illustrated by a constant two-element functor. Checked necessity of the two conditions in Theorem 1 and membership of the tensor square in C. The theorem and its sufficiency argument continue on the next page. The general cohomological-obstruction remark remains identified background.''')
from update_record_counts import update
update()
