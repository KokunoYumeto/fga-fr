from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/212.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'212-102',line,'1.1; 2. Finite preschemes','400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 r(r'$X\longrightarrow Y$ (qui',r'$X\to Y$, (qui','Proposition 1.1 parenthesis',why='An ordinary arrow and a comma precede the printed parenthesis.')
 r(r'\subsection*{2. Exemple: préschémas finis sur $S$}',r'\subsection*{\textnormal{2. \uline{Exemple} : \uline{préschémas finis sur} $S$.}}','section heading',why='The heading is roman, with separate underlines under Exemple and préschémas finis sur; S and the final period are outside the underline.')
 r(r'(i.e. qui',r'(i. e. qui','finite-algebra abbreviation',why='The print separates i. and e. by a space.')
 r('correspondent en effet (comme', 'correspondent en effet, (comme','coequalizer parenthesis',why='A comma precedes the opening parenthesis in print.')
 r('au sous-anneau de $C$ formé par l\'ensemble des éléments','au sous-anneau de $C$ ensemble des éléments','equalizer subring wording',why='The words formé par l’ were supplied by the transcription and are absent from the scan. The compressed apposition is retained in both layers.')
 r(r'\emph{tous}',r'\uline{tous}','last emphasized word',why='A straight underline emphasizes tous.')
 s,_,_=page_text(rel,102)
 r(r'\mathcal C',r'\text{\uwave{C}}','category letters',count=s.count(r'\mathcal C'),why='All category C letters have a wavy underline.')
 upright_page(rel,layer,'212-102')

event('212-1.1','targeted proof check','The two constructions are inverse by the two effectiveness conditions: the kernel pair of X to X/R is R, and the coequalizer of the kernel pair of an effective quotient X to Y is Y, with the unique compatible isomorphism. A containment R in R-prime is equivalent to the quotient map for R-prime equalizing R, hence to a unique factorization X/R to X/R-prime. This proves the asserted compatibility with the natural quotient order. Objects are understood up to compatible isomorphism, as in the preceding definition.','212, p. 102, Proposition 1.1')
event('212-2-sets-sheaves','targeted proof check','In sets, a surjection is the coequalizer of its fibre relation and every equivalence relation has its set of classes. For sheaves, sheafify the presheaf of equivalence classes. Two sections have the same image exactly when they are locally related; since the relation is itself a subsheaf this is equivalent to their being related. Epimorphisms of sheaves are locally surjective, so the same construction recovers each quotient. This checks the two examples of categories with effective quotients and relations.','212, p. 102, paragraph after Proposition 1.1')
event('212-2-finite-algebra-limits','targeted proof check','Over affine noetherian S=Spec(A), finite schemes are opposite to finite A-algebras. Tensor products and quotients by the differences u(c)-v(c) have the required product and equalizer universal properties and remain finite. Finite products of algebras and the subalgebra ker(u-v) have the opposite universal properties; the latter is finite because it is an A-submodule of a finite A-module over noetherian A. Localization is exact, commutes with these finite constructions, and allows the coherent algebra constructions to glue over a locally noetherian base. This verifies existence in the category of finite S-schemes.','212, p. 102, section 2, algebra formulas')
event('212-2-finite-colimits-all-preschemes','carried as background without fault found','The additional assertion that these finite colimits are colimits in the category of all preschemes is retained as an unproved background claim here. The algebra calculation above proves only the universal property against affine targets. Extending it to arbitrary targets requires the topological quotient and localization/gluing argument for finite morphisms; that extra step has not been claimed as proved by the algebra calculation.','212, p. 102, last sentence')
record_page('212',102,r'''Compared sources/fr_printed/fr/212.tex and sources/fr/fr/212.tex entry lines 139–182 with scan leaf 5 at 400 dpi, full page and all three enlarged bands. Read Proposition 1.1, every fibre-product and tensor base, both pairs of double arrows and their reversed ring directions, the difference u(c)-v(c), the category alphabets and all punctuation.

Both layers restore the ordinary arrow and comma in Proposition 1.1, the selective underlines and period in the section heading, wavy category letters, the i. e. spacing, the comma before the second parenthesis, the printed compressed apposition C ensemble des éléments, the underline on tous and upright variables. No mathematical correction separates the layers on this page.

Verified the correspondence and its order statement, the set/sheaf examples, and finite limits and colimits via finite algebras and localization. Recorded the last extension to arbitrary prescheme targets as background requiring an additional topological/gluing argument, rather than counting the affine calculation as a complete proof.''')
from update_record_counts import update
update()
