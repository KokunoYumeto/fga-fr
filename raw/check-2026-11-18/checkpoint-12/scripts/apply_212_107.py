from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/212.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'212-107',line,'4. Internal categories and simplex categories','400-dpi full scan, all three enlarged bands, and the extra crop of the missing S. '+why,kind,count=count)
 r(r'\emph{morphisme composition}','morphisme composition','first prose line',why='The printed phrase has no underline or other emphasis and no hyphen.')
 r(r'\longrightarrow',r'\to','three displayed arrows',count=3,why='The scan has ordinary-length arrows.')
 r('suivant:', 'suivant :','two introductions',count=2,why='The colon is separated from the preceding word.')
 r('catégorie (resp. de groupoïde)', 'catégorie, (resp. de groupoïde)','first paragraph',why='The print has a comma before the parenthesis.')
 r('« ensembliste »',r'\fquote{ensembliste}','diagram paragraph',why='The printed quotation marks are ordinary double quotes.')
 r('i.e.','i. e.','left exact functor',why='The abbreviation is spaced in the print.')
 for term in ['opérations simpliciales','applications quelconques','non vides','non vide','applications croissantes']:
  r(r'\emph{'+term+'}',r'\uline{'+term+'}','emphasis: '+term,why='A straight underline marks this phrase.')
 r(r'\emph{catégorie $\mathcal S$ des simplexes-types}',r'\uline{catégorie} $\mathcal S$ \uline{des simplexes-types}','simplex category definition',why='The prose has straight underlines and S a separate wavy underline.')
 r(r'\Delta_n=[0,n],\qquad\text{où }n\geq 0',r'\Delta_n=[0,n]\qquad\text{où }n\geqslant 0','simplex display',why='No comma follows the closing bracket; the lower stroke of the inequality is slanted.')
 r(r"On désigne par $\mathcal S'$",r"On désigne par $\text{\uwave{\phantom{S}}}'$",'definition of the ordered simplex category',why='The scan has a blank above the wavy underline, followed by a prime. The separate enlarged crop confirms that the S itself is absent. Both layers first restore this printed omission.')
 if tree=='fr':
  r(r"On désigne par $\text{\uwave{\phantom{S}}}'$",r"On désigne par $\text{\uwave{S}}'$",'definition of the ordered simplex category',kind='misprint of the original',why='The missing category letter is S: this is the subcategory of the just-defined S with the same objects and increasing maps, consistently called S prime in the subsequent construction. A prime and underline without a base letter cannot supply the intended category name.')
 s,_,_=page_text(rel,107)
 for old,new in [(r'\mathcal C',r'\text{\uwave{C}}'),(r'\mathcal S',r'\text{\uwave{S}}')]:
  r(old,new,'category alphabet',count=s.count(old),why='The category letter has a wavy underline, not a script typeface.')
 upright_page(rel,layer,'212-107')

event('212-4-left-exact-functors','targeted proof check','A functor preserving finite products and fibre products identifies F(R times_X R) with F(R) times_F(X) F(R). Apply F to p1,p2,pi,D and, for a groupoid, s, then transport composition through this comparison. Functors preserve each morphism identity and composition, so the source/target, associativity, unit and inverse diagrams checked on p. 106 remain commutative. Thus the asserted preservation of internal categories and groupoids follows. The statement assumes the needed finite limits exist; finite products include the empty product.','212, p. 107, first paragraph, exact-left functor sentence')
event('212-4-simplex-categories','targeted proof check','Every nonempty finite set is isomorphic to a unique cardinality representative [0,n], and allowing all functions makes S a skeleton of nonempty finite sets. A nonempty finite coproduct is the disjoint union, still nonempty and finite. A pushout is the disjoint union modulo the generated identifications; it is again nonempty finite. Restricting to weakly increasing functions instead gives a skeleton of nonempty finite totally ordered sets. The missing S above the underline in the printed name of S prime is restored only in the corrected layer; the absent letter is visible in the dedicated crop.','212, p. 107, second paragraph and last six lines')
record_page('212',107,r'''Compared sources/fr_printed/fr/212.tex and sources/fr/fr/212.tex entry lines 366–413 with scan leaf 10 at 400 dpi, full page and all three enlarged bands, plus a separate enlarged crop of the missing category letter near the bottom. Read the three displayed morphisms, every fibre-product index, the simplex interval and inequality, and every category symbol.

Both layers restore the unemphasized morphisme composition, ordinary arrows and quotes, punctuation, spaced i. e., straight prose underlines, wavy category letters, the absence of a comma after [0,n], the slanted inequality and upright mathematical letters. In the printed layer the name of the ordered simplex category is a blank over a wavy underline followed by a prime, exactly as the scan shows. The corrected layer supplies the missing S. This is the sole mathematical difference on this page.

Checked preservation of the internal-category equations by a left exact functor, and the equivalences and finite colimits asserted for the category of nonempty finite sets. Historical semi-simplicial and simplicial terminology is retained for checking against the definitions that follow.''')
from update_record_counts import update
update()
