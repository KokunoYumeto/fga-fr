from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/195.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'195-381',line,'C.2','400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 r(r'$Y_T=Y\times_ST$, et',r'$Y_T=Y\times_ST$ et','opening base changes',why='No comma follows the second base change.')
 r(r'\operatorname{Hom}_S(T\times_SX,Y).',r'\operatorname{Hom}_S(T\times_SX,Y)','first universal-property display punctuation',why='No terminal period is printed.')
 r(r'$S$-automorphismes',r'$S$-\uline{automorphismes}','automorphism variant',why='Printed underline excludes S and its hyphen.')
 r('en groupes), pré-schéma','en \\uline{groupes}), pré-schéma','automorphism group assertion',why='Printed selective underline.')
 r(r'$S$-homomorphismes',r'$S$-\uline{homomorphismes}','group-homomorphism variant',why='Printed selective underline.')
 r('en groupes dans un autre','en \\uline{groupes} dans un autre','source group',why='Only groupes is underlined.')
 r('est commutatif), etc.','est commutatif) etc.','variant-list punctuation',why='No comma before etc.')
 r('« sections »',r'\fquote{sections}','section terminology',why='Ordinary double quotation marks.')
 r(r'=\operatorname{Hom}_{X_T}(X_T,Z_T).',r'=\operatorname{Hom}_{X_T}(X_T,Z_T)','restriction-of-scalars display punctuation',why='No terminal period is printed.')
 r("l'existence des schémas du type", "l'\\uline{existence} des schémas du type",'existence question emphasis',why='Underline starts after the elision.')
 r("constate d'abord que, pour", "constate d'abord que pour",'necessity discussion punctuation',why='No comma after que.')
 r('$X$ est plat sur','$X$ est \\uline{plat} sur','flatness condition',why='Printed selective underline.')
 r('$X$ est de plus propre sur','$X$ est de plus \\uline{propre} sur','properness condition',why='Printed selective underline.')
 r('à condition, le\ncas échéant,','à condition le\ncas échéant','qualification punctuation',why='Neither comma around le cas échéant is printed.')
 r('« quasi projective »',r'\fquote{quasi-projective}','quasi-projectivity qualification',why='The scan has a hyphen and ordinary double quotation marks.')
 r('sur $Y/S$, resp.','sur $Y/S$ resp.','respective conditions punctuation',why='No comma before resp.')
 r('$Y$ est affine sur','$Y$ est \\uline{affine} sur','affine case',why='Printed selective underline.')
 r('$X$ est fini sur','$X$ est \\uline{fini} sur','finite case',why='Printed selective underline.')
 s,_,_=page_text(rel,381)
 r(r'\underline{\operatorname{Hom}}',r'\text{\uwave{Hom}}','representing Hom symbols',count=s.count(r'\underline{\operatorname{Hom}}'),why='Every representing Hom has a wavy underline; Hom sets remain unadorned.')
 upright_page(rel,layer,'195-381')

event('195-C2-universal-properties','targeted proof check','Projection from Y_T=Y times_S T gives a natural bijection Hom_T(X_T,Y_T)=Hom_S(X_T,Y); its inverse pairs an S-map with the structural map X_T to T. Substitution X_T=X times_S T gives the first display. Yoneda gives the representing universal-property isomorphism. A section of Z_T over X_T is exactly an X_T-map X_T to Z_T; for Z=Y times_S X these sections are the same maps into Y. Both displayed Weil-restriction formulas therefore have the stated X_T subscripts. Base change follows by applying these bijections to an S-prime test scheme; products are preserved because sections into a fiber product are compatible pairs of sections. These verifications concern formulas whenever the objects exist.','195, p. 381, four displays and Z=Y times_S X specialization')
event('195-C2-group-variants','targeted proof check','When Hom(X,X) exists, pairs (f,g) with fg=gf=id are represented by a finite fiber product using the two composition maps. The inverse g is unique, giving Aut(X), and composition/inversion define its group structure by Yoneda. Homomorphisms of group schemes are obtained as an equalizer of the multiplication-compatibility maps into Hom(G times_S G,H), assuming these Hom objects exist; unit and inverse compatibility follow from the group laws. If H is commutative, pointwise multiplication and inversion preserve the homomorphism condition and give a commutative group object.','195, p. 381, automorphism and group-homomorphism variants')
event('195-C2-flatness-and-finite-case','targeted proof check','For an affine X=Spec(B) over Spec(A), the A1-valued Hom functor on an A-algebra R is B tensor_A R. Use square-zero A-algebras A plus M to A plus N induced by an injection M to N. Their spectra have the same underlying topological space Spec(A), and the map of structure sheaves is injective on every distinguished open. Two maps from Spec(A plus M) to any scheme agreeing after Spec(A plus N) have the same underlying map and can be compared in the same affine target neighborhoods, where injectivity of the ring maps proves equality. This argument is specific to the square-zero probes; injectivity for arbitrary injections of test algebras is not asserted. Injectivity of B tensor M to B tensor N follows, so B is flat. This verifies flatness necessity in the affine case; the general nonaffine necessity is not reconstructed here. For finite free B and affine Z over B, write the images of algebra generators in a fixed basis of B. Expansion of each relation supplies polynomial equations in the coefficients, representing the restriction of scalars; localization on the base treats finite locally free B.','195, p. 381, final paragraph, flatness and finite cases')
event('195-C2-global-existence-prospect','carried as background without fault found','The properness discussion and sufficiency with quasi-projective targets are expressly phrased as expectation, with examples. In the locally finite-type category, X=A1 and Y=A1 already have the infinite-dimensional tangent space k[t] at the zero map, explaining an obstruction without properness. Existence for a general proper flat X and affine Y uses coherent cohomology and its base-change representation; gluing finite restrictions for quasi-projective targets uses additional geometric arguments. Those general constructions remain background. Neither necessity for every possible target nor the announced sufficiency is claimed to have been completely proved by the affine checks.','195, p. 381, final paragraph')
record_page('195',381,r'''Compared sources/fr_printed/fr/195.tex entry lines 593–644 and sources/fr/fr/195.tex entry lines 594–645 with scan leaf 14 at 400 dpi, full page and all three enlarged bands. Read all four displays, the T/S/X_T subscripts, product order, equality versus isomorphism arrow, Pi subscripts and representing versus ordinary Hom.

Both layers restore wavy underlines on representing Hom only, selective prose underlining, ordinary quotes, the hyphen in quasi-projective, exact comma placement, unpunctuated universal-property displays and upright letters. No mathematical difference between the French layers was introduced; the small dot under the first Hom in the isomorphism display is treated as ink.

Checked the natural base-change bijections, section specialization, product/base-change identities, group-object variants, affine flatness necessity and the coefficient construction for finite free affine restriction of scalars. The general nonaffine necessity and global existence arguments are explicitly distinguished as background; the author's expectation is retained as such.''')
from update_record_counts import update
update()
