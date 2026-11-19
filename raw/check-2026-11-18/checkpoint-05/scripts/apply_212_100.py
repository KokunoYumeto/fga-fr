from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/212.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'212-100',line,'1. Equivalence relations and coequalizers','400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 r(r"\subsection*{1. Relations d'équivalence, relations d'équivalence effectives}",r"\subsection*{\textnormal{1. \uline{Relations d'équivalence, relations d'équivalence effectives}.}}",'section heading',why='Roman heading with an underline over the title words and a final period.')
 r(r"\emph{couple d'équivalence}",r"\fquote{\uline{couple d'équivalence}}",'first defined term',why='Underlined words inside ordinary double quotation marks.')
 for word in ['but','source','conoyau']:
  r(r'\emph{'+word+'}',r'\uline{'+word+'}','defined term '+word,why='Printed underline, not italics.')
 r(r'\longrightarrow',r'\to','relation graph arrow',why='The printed arrow has ordinary length.')
 r("entre les couples d'équivalence de but","entre les couples d'équivalences de but",'plural wording in definition',why='The local printed wording has a final s in équivalences; it is retained in both layers.')
 r("une relation d'équivalence évidente;", "une relation d'équivalence évidente,",'equivalence-of-couples punctuation',why='The scan has a comma, not a semicolon.')
 r(r"\emph{$\mathcal C$-relation d'équivalence dans $X$}",r"$\mathcal C$\uline{-relation d'équivalence} dans $X$",'category-relation emphasis',why='The category letter has its own wavy underline; only the hyphen and relation d’équivalence are straight-underlined. Dans X is outside the emphasis.')
 old=r'''le sous-ensemble de
\[
  (X\times X)(T)=X(T)\times X(T)
\]
qui correspond'''
 new=r'''le sous-ensemble de $(X\times X)(T)=X(T)\times X(T)$ qui correspond'''
 r(old,new,'product-of-points identity',kind='structure',why='This identity is inline in the printed second paragraph.')
 r('le foncteur covariant en $Z$','le foncteur covariant en $Z$ :','coequalizer display introduction',why='The printed sentence has a colon before the display.')
 for a,b in [(r'$X/(p_1,p_2)$',r'$Y/(p_1,p_2)$'),(r'$X/R$',r'$Y/R$')]:
  r(a,b,'quotient notation: printed '+b,why='The enlarged lower band clearly shows Y as the numerator in both quotient names.')
  if tree=='fr':
   r(b,a,'quotient notation: corrected '+a,kind='misprint of the original',why='The pair has target X and defines a relation on X; Y has just been introduced as the resulting coequalizer. The quotient notation must therefore take X as numerator. No relation on Y has been specified.')
 s,_,_=page_text(rel,100)
 r(r'\mathcal C',r'\text{\uwave{C}}','category letter',count=s.count(r'\mathcal C'),why='Every category C is an upright letter with a short wavy underline.')
 upright_page(rel,layer,'212-100')

event('212-1-equivalence-relation','targeted proof check','If X times X exists, the pair R to X times X is a monomorphism exactly when Hom(T,R) to Hom(T,X times X) is injective for every T. The stated bijection onto an equivalence graph gives this injectivity and hence the subobject formulation. Conversely a subobject with those pointwise graphs gives the original pair. Equivalent pairs are uniquely isomorphic over X times X, so the change from representatives to relation subobjects is legitimate.','212, p. 100, definition and second paragraph')
event('212-1-equivalence-diagrams','targeted proof check','Pointwise reflexivity gives a natural diagonal lift X(T) to R(T), symmetry gives a natural involution of R(T), and transitivity gives a natural composite R(T) times_X(T) R(T) to R(T). Yoneda represents these by arrows in the category when the stated products exist. Their required identities hold because the embedding R(T) into X(T) squared determines each related pair uniquely. Conversely applying Hom(T,-) to these diagrams gives the three set-theoretic axioms. This verifies the advertised diagrammatic formulation and the reference to 195 A.1.','212, p. 100, diagrammatic formulation')
event('212-1-coequalizer-notation','targeted proof check','A representation Hom(Y,Z) of the equalizing subfunctor Hom_(p1,p2)(X,Z) yields q:X to Y by the image of id_Y. Naturality identifies every element with a unique composite vq, so this is the coequalizer universal property. Uniqueness is unique compatibility with q, not absence of unrelated automorphisms. Since p1,p2 have target X and R is a relation on X, the quotient is denoted X/(p1,p2) or X/R. The printed Y numerators name a quotient of the already introduced result and have no defined relation; both are corrected only in the corrected layer.','212, p. 100, coequalizer definition and last two formulas')
record_page('212',100,r'''Compared sources/fr_printed/fr/212.tex and sources/fr/fr/212.tex entry lines 43–94 with scan leaf 3 at 400 dpi, full page and all three enlarged bands. Inspected both double arrows, every p subscript and T argument, the product and fibre-product bases, Hom subscripts, and both printed Y quotient numerators.

Both layers restore the underlined roman heading and its period, quoted first defined term, selective straight underlines, wavy category C, ordinary graph arrow, printed plural équivalences and comma, inline product-of-points identity, missing colon before the last display and upright variables. The printed layer has Y/(p1,p2) and Y/R; the corrected layer retains X in both places, now with explicit misprint evidence and the universal-property reason.

Checked the equivalence between monomorphic pairs and pointwise relation subobjects, derived reflexivity/symmetry/transitivity diagrams by Yoneda, and checked the covariant representation of a coequalizer including its compatible uniqueness. No other formula or hypothesis is changed.''')
from update_record_counts import update
update()
