from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='4(a)',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-310',line,statement,'400-dpi full scan and enlarged top, middle and bottom bands. '+why,kind,count=count)
 r(r'\mathcal O',r'\text{\uwave{O}}','line 1','3',why='Ordinary wavy-underlined structure-sheaf letter.')
 r('implique en particulier que','implique en particulier, que','line 3','3',why='Printed comma after particulier.')
 r("« \\emph{invariance topologique du groupe fondamental\nd'un préschéma} »", "\\fquote{\\uline{invariance topologique du groupe fondamental d'un pré-schéma}}",'lines 4–5','3',why='Double quotes, underline and hyphenated pré-schéma.')
 r(r'\subsection*{4. Relations avec la 1-cohomologie}',r'\subsection*{\normalfont 4. \uline{Relations avec la} 1-\uline{cohomologie}.}','section heading',kind='structure',why='Roman heading with two underline spans and a final period; the numeral 1 is outside the underline.')
 if tree=='fr_printed':
  r('une catégorie où le produit','une catégorie ou le produit','first line of 4(a)',why='No accent over the printed ou; corrected French retains grammatical où.')
 else:
  r('un foncteur covariant de\nla catégorie des ensembles finis','un foncteur contravariant de\nla catégorie des ensembles finis','lines 9–10',kind='misprint of the original',why='The print says covariant. A function I→J induces T^J→T^I by selecting coordinates, so this occurrence must be contravariant. The later covariant dependence on T is correct and retained.')
 r('$T^I$ ; pour','$T^I$, pour','line 8',why='Comma, not semicolon.')
 r('i.e.','i. e.','line 10',why='Spaced abbreviation.')
 for term in ['objet simplicial','domine']:
  r('\\emph{'+term+'}','\\uline{'+term+'}','definition of '+term,why='Printed underline.')
 r("d'ailleurs, si","d'ailleurs si",'line 11',why='No comma after ailleurs.')
 old="si $u,v$ sont deux morphismes\n$T\\longrightarrow T'$, alors les morphismes correspondants\n$K_T\\longrightarrow K_{T'}$ sont homotopes."
 r(old,underline_prose(old),'lines 11–13',why='The homotopy assertion is underlined in its prose, excluding mathematical variables and final period.')
 r('qui précède que, si','qui précède que si','line 14',why='No comma after que.')
 r("$K_T\\longrightarrow K_{T'}$ ; en\nparticulier, si", "$K_T\\longrightarrow K_{T'}$, en\nparticulier si",'line 16',why='Comma after the map and none after particulier.')
 r("abélienne $\\mathcal C'$", "\\uline{abélienne} $\\mathcal C'$",'line 19',why='The adjective abélienne is underlined.')
 r('domination), les','domination) les','line 27',why='No comma after this parenthesis.')
 r('au-dessus de $S$ ; on écrira','au-dessus de $S$, on écrira','line 32',why='Comma, not semicolon.')
 r(r'\mathcal C',r'\text{\uwave{C}}','seventeen category letters',why='The category letter is ordinary wavy-underlined C, including its primes and base subscripts.',count=17)
 upright_page(rel,layer,'190-310')
with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 csv.writer(f,delimiter='\t').writerow(['sources/fr/fr/190.tex','French corrected','190-310','first line of 4(a)','4(a)','une catégorie ou le produit','une catégorie où le produit','Confirmed supplied corrected relative adverb against the unaccented ou visible in the enlarged top band. The sentence introduces the category in which products exist.','misprint of the original','low'])
event('190-3-topological-invariance-conclusion','targeted proof check','The equivalence of étale categories preserves finite étale covers and their geometric fiber functors, hence yields the asserted fundamental-group isomorphism (with compatible base points). The nilpotent case is the étale lifting result already used at 182, Lemma 6. The full universal-homeomorphism theorem itself remains a background input here, not an independent re-proof. The empty printed reference brackets are retained and flagged rather than filled by inference.','190, p. 310, first paragraph')
event('190-4a-index-variance','refuted, with the refined statement\'s id','Printed covariant in the finite-set variable is false; refined statement 190-4a-index-variance-corrected. For f:I→J the product maps give f*:T^J→T^I; already {0,1}→{0} yields the diagonal T→T². Contravariance in I is also what makes F(K_T) cosimplicial when F is contravariant. Covariance in the object T is retained.','190, p. 310, 4(a), first three sentences')
event('190-4a-homotopy','targeted proof check','For u,v:T→T-prime the prism maps h_j:T^(n+1)→T-prime^(n+2), 0≤j≤n, have coordinates (u t_0,...,u t_j,v t_j,...,v t_n). Coordinate deletion gives the simplicial homotopy identities: interior terms cancel in the alternating sum and the two end faces give v and u. Applying any contravariant F into an abelian category gives a cochain homotopy. Thus parallel maps induce the same cohomology map; mutual domination gives inverse maps on cohomology. Products dominate both factors, giving the directed system in the refinement orientation. The phrase that K_T and K_T-prime dominate each other is retained: domination extends to the simplicial category and evaluation in degree zero recovers maps of T objects.','190, p. 310, 4(a), homotopy and domination paragraphs')
event('190-4a-cohomological-functor','targeted proof check','The alternating coface sum of F(K_T) squares to zero by pairwise cancellation. A pointwise short exact sequence of abelian-category-valued functors yields a short exact sequence of these cochain complexes and hence the long exact cohomology sequence, giving the stated cohomological functor in F. Passing to the slice category replaces ordinary products by fiber products. The historical use of objet simplicial for the nonempty-finite-set construction is retained; restriction to the simplex category supplies the ordinary simplicial object.','190, p. 310, 4(a), two displayed definitions and final paragraph')
record_page('190',310,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 583–633 against scan leaf 13, rendered at 400 dpi: full page and all three enlarged bands personally read. Inspected every index, prime, star, arrow and underline; both cohomological formulas remain displays. The empty reference brackets are visibly empty and remain unresolved in both layers.

Restored the wavy-underlined O and seventeen category C letters, double quotes and pre-scheme hyphen, selective underlines (including the homotopy assertion and abélienne), heading punctuation, spaced abbreviation and the printed comma choices. Restored unaccented ou only in printed French and explicitly confirmed où in corrected French. Newly corrected covariant to contravariant only for the finite-set variable I, with the coordinate-reindexing test recorded. The dependence on T remains covariant.

Checked the prism homotopy, independence of the cohomological maps, directedness by products, mutual-domination isomorphisms and the cohomological functor construction. Distinguished the fundamental-group consequence of equivalence from the universal-homeomorphism theorem carried as background. No author erratum has been merged.''')
from update_record_counts import update
update()
