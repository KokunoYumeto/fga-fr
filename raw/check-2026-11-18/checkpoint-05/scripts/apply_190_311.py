from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='4(a)',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-311',line,statement,'400-dpi full page and enlarged top, middle and bottom bands. '+why,kind,count=count)
 r("$n$, est égal à\n\\[\n  F(T\\times_ST\\times_S\\cdots\\times_ST)\n\\]\n", "$n$ est égal à $F(T\\times_ST\\times_S\\cdots\\times_ST)$ ",'lines 1–2',kind='structure',why='The fiber-power expression runs inline, without a comma after n.')
 r('Notons que, comme',"Notons que comme",'line 3',why='No comma after que.')
 r('correspondant aux deux projections','correspondants aux deux projections','line 7',why='The print has plural correspondants.')
 r(r'\emph{augmentation}',r'\uline{augmentation}','line 8',why='Underlined word.')
 r('« exact à\ngauche »',r'\fquote{exact à gauche}','line 11',why='Printed double quotes.')
 r('i.e.','i. e.','line 13',why='Spaced abbreviation.')
 r('commutatifs), $H^1(T/S,F)$','commutatifs), $H^1(T,F)$','line 15',why='The print uses the abbreviated H¹(T,F). This is valid with the slice category understood, as explained on 310, and is restored in both layers.')
 if tree=='fr':
  r('du sous-groupe $Z^1(T/S,F)$','du sous-ensemble $Z^1(T/S,F)$','line 15',kind='misprint of the original',why='Nonabelian cocycles need not form a subgroup under pointwise multiplication. The print itself calls them a sous-ensemble three lines later. Exact two-point matrix counterexample in check_190_nonabelian.py.')
  r(r'F(p_{31})(g)=F(p_{32})(g)\,F(p_{21})(g)',r'F(p_{31})(g)=F(p_{21})(g)\,F(p_{32})(g)','cocycle display',kind='misprint of the original',why='With p_ij=(p_i,p_j) and the printed gauge action h_2 g h_1^-1, cancellation requires g_31=g_21 g_32. The printed reverse order is not preserved even by a gauge transform of the identity; exact matrix witness recorded.')
 r('$C^1(T/S,F)$ et, en particulier,','$C^1(T/S,F)$ et en particulier,','line after cocycle display',why='No comma before en.')
 r(r"F(p_1)(g')^{-1}.",r"F(p_1)(g')^{-1}",'gauge-action display',why='No final period.')
 r("\\operatorname{Hom}(\\xi\\times_SS',\\eta\\times_SS').","\\operatorname{Hom}(\\xi\\times_SS',\\eta\\times_SS')",'Hom display','4(b)',why='No final period.')
 r(r"\emph{dire que le morphisme d'augmentation}",r"\uline{dire que le morphisme d'augmentation}",'augmentation criterion opening','4(b)',why='Printed underline.')
 old="\\emph{est un isomorphisme pour tout couple d'éléments\n$\\xi,\\eta\\in\\mathcal F_S$ signifie que\n$\\alpha:S'\\longrightarrow S$ est un morphisme de $\\mathcal F$-descente}"
 plain="est un isomorphisme pour tout couple d'éléments $\\xi,\\eta\\in\\mathcal F_S$, signifie que $\\alpha:S'\\longrightarrow S$ est un morphisme de $\\mathcal F$-descente"
 r(old,underline_prose(plain),'augmentation criterion conclusion','4(b)',why='Printed comma after F_S and prose underlining excluding mathematical letters.')
 if tree=='fr_printed':
  r('au-dessus de $S$,\n\\[','au-dessus de\n\\[','4(c), first line','4(c)',why='The scan omits S after au-dessus de and has no comma there. Corrected French retains the missing base and its introductory comma.')
 r("\\operatorname{Aut}(\\xi\\times_SS') ;","\\operatorname{Aut}(\\xi\\times_SS'),",'Aut display','4(c)',why='Comma after the formula, not semicolon.')
 page,_,_=page_text(rel,311)
 r(r'\mathcal C',r'\text{\uwave{C}}','category letters','4',why='Ordinary wavy-underlined C, retaining primes and subscripts.',count=page.count(r'\mathcal C'))
 upright_page(rel,layer,'190-311')
with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 csv.writer(f,delimiter='\t').writerow(['sources/fr/fr/190.tex','French corrected','190-311','4(c), first line','4(c)','au-dessus de','au-dessus de $S$,','Confirmed the supplied completion of the broken phrase against the bottom band: the printed line ends at de before the Aut display. The base S is required by the immediately used slice category and fiber product.','misprint of the original','low'])
event('190-4a-nonabelian-cocycle-order','refuted, with the refined statement\'s id','Printed order refuted; refined statement 190-4a-nonabelian-cocycle-order-corrected uses F(p31)g=F(p21)g F(p32)g. Under g(i,j)↦h(j)g(i,j)h(i)^-1, the two middle h factors cancel precisely in this order. With h=(I,A,B), A=[[1,1],[0,1]], B=[[1,0],[1,1]], the gauge transform of the identity fails the printed order. This also independently reinforces the correction of 1(c) on p. 302.','190, p. 311, 4(a), cocycle and action displays')
event('190-4a-cocycles-not-subgroup','refuted, with the refined statement\'s id','Printed sous-groupe refuted; refined statement 190-4a-cocycles-subset. For a two-point cover and group SL2(Z), the coboundaries determined by (I,A) and (I,B) are cocycles; their pointwise product is not, since its two opposite edge values multiply to A^-1 B^-1 A B, which is not I. The subsequent printed sous-ensemble is correct.','190, p. 311, 4(a), quotient definition')
event('190-4a-nonabelian-matrix-certificate','computation or formal certificate','Executed scripts/check_190_nonabelian.py: integer matrix multiplication checks the corrected cocycle for all triples, failure of the printed order under gauge transformation, and failure of multiplicative closure for two cocycles. No floating-point calculation or appeal to another edition.','190, p. 311, 4(a)')
event('190-4ab-augmentation-and-descent','targeted proof check','H⁰ is the equalizer of the two pullbacks. The augmentation lands there because the two maps to S agree. For a contravariant functor carrying the strict-epimorphism coequalizer to an equalizer, augmentation is an isomorphism, which is the quoted exactness condition. Taking the Hom functor, equalizer elements are precisely arrows compatible with the canonical descent data, so bijectivity for every pair is full faithfulness, i.e. F-descent. The abbreviation H¹(T,F) is valid in the slice category and has not been treated as an original error.','190, p. 311, 4(a)–(b)')
event('190-4a-internal-nonabelian-cohomology','carried as background without fault found','The concrete category-of-sets construction is checked by the formulas above. The preceding reference to group objects in an arbitrary category presupposes the required equalizers and orbit objects; their existence is not proved here and the statement is not marked independently verified in that generality.','190, p. 311, 4(a), group objects paragraph')
record_page('190',311,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 633–695 with scan leaf 14, full page at 400 dpi and all three enlarged bands. Read every formula, index, arrow direction and paragraph transition. Restored the first fiber-power formula inline, comma choices, plural correspondants, double quotes, spaced abbreviation, selective underlining and wavy category letters; removed unprinted display periods and changed the last formula's semicolon to the printed comma.

Restored H¹(T,F) in both layers: this is a legitimate abbreviation with the slice category understood, not a misprint. Restored the visibly missing base after au-dessus de only in printed French and explicitly confirmed its completion in corrected French. Corrected sous-groupe to sous-ensemble and reversed the nonabelian cocycle product only in corrected French. The source's gauge-action formula is retained and supplies a direct consistency check.

Verified the equalizer/augmentation interpretation and its equivalence to full faithfulness for Hom functors. Executed exact integer-matrix witnesses for the cocycle order and failure of the subgroup assertion. The internal construction in a general category remains conditional on existence of the necessary equalizers and orbit objects; no proof of existence has been claimed.''')
from update_record_counts import update
update()
