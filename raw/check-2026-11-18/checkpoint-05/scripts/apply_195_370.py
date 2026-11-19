from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/195.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'195-370',line,'A.1','400-dpi full scan and three enlarged bands. '+why,kind,count=count)
 r('Notons de plus que,','Notons de plus, que,','opening punctuation',why='The print has the extra comma after plus.')
 r(r'h:X\longmapsto h_X',r'h:X\rightsquigarrow h_X','object assignment',why='The printed assignment arrow has a wavy shaft.')
 r('« noyaux » [2],',r'\fquote{noyaux} [2]','kernel terminology',why='Double quotes and no comma after the reference.')
 r('existe, i.e.','existe, i. e.','product explanation',why='Printed spaced abbreviation.')
 r("(i.e. d'une « loi de composition »",r"(i. e. d'une \fquote{\uline{loi de composition}}",'composition-law definition',why='Printed spacing, quotes and selective underline.')
 r("\\[\n  h_{X\\times X'}=h_X\\times h_{X'}\\longrightarrow h_{X''},\n\\]","$h_{X\\times X'}=h_X\\times h_{X'}\\longrightarrow h_{X''}$,",'natural transformation of products',kind='structure',why='This formula is inline in the printed paragraph.')
 r("i.e. à la donnée pour tout",'i. e. à la donnée pour tout','pointwise operation',why='Printed spaced abbreviation.')
 r("d'une loi de composition\nd'ensembles",r"d'une loi de composition d'\uline{ensembles}",'set-valued law',why='Only ensembles is underlined.')
 if tree=='fr_printed':
  r(r"h_{X^{(i)}}(Y)\longleftarrow h_{X^{(i)}}(Y')",r"h_{X^{(i)}}(Y)\longrightarrow h_{X^{(i)}}(Y')",'displayed naturality arrow',why='The print incorrectly points right; corrected French retains the contravariant left arrow.')
  r("h_X(Y)\\longleftarrow h_X(Y')","h_X(Y)\\longrightarrow h_X(Y')",'inline group-homomorphism arrow',why='The same reversed arrow appears in the print here.')
 for old,new,line in [
  ('« $\\mathcal C$-groupe »',r'\fquote{$\mathcal C$-groupe}','group object'),
  ('« $\\mathcal C$-anneau »',r'\fquote{$\mathcal C$-anneau}','ring object'),
  ('commode, par\nexemple,','commode par\nexemple,','example punctuation'),
  (r'\operatorname{Gl}(n)',r'\operatorname{G}\ell(n)','general linear group'),
  ('« fibré vectoriel »',r'\fquote{fibré vectoriel}','vector-bundle terminology')]:
  r(old,new,line,why='Restore printed punctuation, quotation marks or the handwritten looped l.')
 old="le yoga général étant d'identifier purement et simplement, à l'aide du\nfoncteur canonique $h$, les objets de $\\mathcal C$ à des foncteurs\ncontravariants particuliers, les foncteurs représentables,"
 r(old,underline_prose(old),'concluding principle',why='All prose of the concluding principle is underlined; the mathematical identifiers are excluded from that straight underline.')
 s,_,_=page_text(rel,370)
 r(r'\mathcal C',r'\text{\uwave{C}}','category identifiers',count=s.count(r'\mathcal C'),why='Ordinary wavy-underlined C.')
 r(r'\mathcal F',r'\text{\uwave{F}}','two module identifiers',count=2,why='Ordinary wavy-underlined F, not script F.')
 upright_page(rel,layer,'195-370')
with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 for line,old,new in [
  ('displayed naturality arrow',"h_{X^{(i)}}(Y)\\longrightarrow h_{X^{(i)}}(Y')","h_{X^{(i)}}(Y)\\longleftarrow h_{X^{(i)}}(Y')"),
  ('inline group-homomorphism arrow',"h_X(Y)\\longrightarrow h_X(Y')","h_X(Y)\\longleftarrow h_X(Y')")]:
  w.writerow(['sources/fr/fr/195.tex','French corrected','195-370',line,'A.1',old,new,'The enlarged scan points right in this occurrence. For u:Y to Y-prime and h_X(Y)=Hom(Y,X), the induced map is precomposition, Hom(Y-prime,X) to Hom(Y,X), so it must point left. Existing corrected reading confirmed.','misprint of the original','low'])
event('195-A1-limits','targeted proof check','For any existing limit L of a diagram X_i, its universal property identifies Hom(Y,L) with compatible families in the Hom(Y,X_i), naturally in Y. Limits of set-valued functors are formed pointwise, so h_L is the corresponding limit of h_X_i. This gives both product formulas and the statements about fiber products and equalizers, including any infinite limit that exists.','195, p. 370, first paragraph and first two displays')
event('195-A1-algebraic-structures','targeted proof check','Combining product preservation with full faithfulness identifies a map X times X-prime to X-double-prime with a natural family of operations on their Y-points. Precomposition with u:Y to Y-prime goes from points over Y-prime to points over Y, proving that the two right-pointing printed arrows must be reversed. Equalities expressing associativity, units and inverses can be tested after h by faithfulness, which gives the group/ring-object dictionary. For V(F)=Spec_S Sym(F), its Y-points are O_Y-linear maps from the pullback of F to O_Y and hence carry the additive and scalar operations. Arbitrary quasi-coherent F need not give an ordinary locally free vector bundle; the printed quoted terminology is retained. Grassmannian and flag representability is not separately proved by this argument.','195, p. 370, composition laws and final examples')
record_page('195',370,r'''Compared sources/fr_printed/fr/195.tex and sources/fr/fr/195.tex entry lines 55–107 with scan leaf 3 at 400 dpi, full page and all three enlarged bands. Read every product subscript, prime, indexed h, isomorphism sign and arrow, including the two erroneously covariant printed arrows.

Restored the wavy assignment arrow, one inline formula, ordinary wavy-underlined C and F, the looped l in the group name, selective prose underlines, double quotes, abbreviation spacing and punctuation. Printed French restores both right-pointing arrows; corrected French retains the required left-pointing arrows, with separate correction rows for the displayed and inline occurrences.

Checked preservation of limits directly from the universal property, the dictionary between morphisms and natural pointwise operations, and the two contravariant arrow directions. Checked the scalar/additive structure on V(F) through its symmetric-algebra functor of points. The quoted vector-bundle terminology is kept without adding a local-freeness hypothesis, and no proof of all the flag-space existence statements is claimed.''')
from update_record_counts import update
update()
