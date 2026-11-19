from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='B.1 theorem 3',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-318',line,statement,'400-dpi full image and three enlarged bands. '+why,kind,count=count)
 segment,_,_=page_text(rel,318)
 for a,b,body in footnotes(segment):
  if body.startswith("L'erratum de 1962 répond"):
   r(segment[a:b],'','after historical projectivity question','B.1 remarks',kind='structure',why='No footnote appears on the printed page. The later author erratum belongs in its separate section and is not merged here.')
 r(r'\emph{fini}',r'\uline{fini}','first paragraph and remarks',why='Underline.',count=2)
 r(r'\emph{critère de Weil}',r'\uline{critère de} Weil','Weil criterion',why='Only critère de is underlined; Weil remains plain and mixed case.')
 r('en particulier\nainsi si','en particulier\nainsi, si','first paragraph',why='Printed comma after ainsi.')
 r('dans ce cas on peut','dans ce cas, on peut','first paragraph',why='Printed comma after cas.')
 r('préschéma','pré-schéma','seven occurrences',why='Printed hyphens.',count=7)
 r('« descendu »',r'\fquote{descendu}','first paragraph',why='Double quotes.')
 for word in ['radiciel','morphisme de descente strict']:
  r('\\emph{'+word+'}','\\uline{'+word+'}','theorem '+word,why='Underline.')
 r('en tout cas','en tous cas','remark first sentence','B.1 remarks',why='Printed tous.')
 r('« formelle »',r'\fquote{formelle}','remark first sentence','B.1 remarks',why='Double quotes.')
 span="pour tout point de $S$\nexiste un voisinage ouvert $U$, un $U'$ fini et fidèlement plat sur $U$, et un\n$S$-morphisme de $U'$ dans $S'$."
 r('\\emph{'+span+'}',underline_prose(span.replace('\n',' ')),'weaker hypothesis','B.1 remarks',why='Prose underlines exclude the variables.')
 r(r'\widehat A',r'\bar A','completion notation','B.1 remarks',why='Both printed accents are horizontal bars, not hats.',count=2)
 r('i.e.','i. e.','quasi-finite parenthesis','B.1 remarks',why='Printed spacing.')
 old='\\subsection*{2. Application à la descente de certaines propriétés de morphismes}\n\\addcontentsline{toc}{subsection}{2. Descente de propriétés de morphismes}\n\nSoit'
 new='\\addcontentsline{toc}{subsection}{2. Descente de propriétés de morphismes}\n\\result{2. \\uline{Application à la descente de certaines propriétés de morphismes}}{} Soit'
 r(old,new,'section 2 heading','B.2',kind='structure',why='The printed Roman underlined heading runs into the first paragraph, with period and dash.')
 r("« $f'\\in P$ »",r"\fquote{$f'\in P$}",'first quoted condition','B.2',why='Double quotes.')
 r('« $f\\in P$ »',r'\fquote{$f\in P$}','second quoted condition','B.2',why='Double quotes.')
 r(r'\emph{fidèlement plat et quasi-compact}',r'\uline{fidèlement plat} et \uline{quasi-compact}','base-change hypotheses','B.2',why='The conjunction et is not underlined.')
 upright_page(rel,layer,'190-318')
event('190-B1-theorem3','carried as background without fault found','Read the radicial fpqc effectivity assertion and the finite fpqc assertion for quasi-projective or projective objects. The former needs the invariant-open/affine-cover argument after localizing the base; the latter needs the finite-orbit affine-neighborhood criterion and a proof that the descended object remains quasi-projective, with properness giving the projective case. These full existence and ampleness arguments are not independently proved on this page.','190, p. 318, theorem 3 and opening paragraph')
event('190-B1-theorem3-local-refinement','targeted proof check','Assuming the finite assertion of theorem 3, restrict a datum along each finite faithfully flat U-prime to U mapping into S-prime. It descends there to X_U. Over S-prime times_S U the comparison to the original object is verified after the faithfully flat base change by U-prime; theorem 2 full faithfulness descends the comparison and checks its inverse. These comparisons yield the overlap isomorphisms between X_U and their cocycle identities, so ordinary open gluing gives the desired object. The assertion about projectivity uses the local convention for relative projectivity.','190, p. 318, underlined hypothesis in remarks')
event('190-B1-theorem3-historical-question','carried as background without fault found','Read the two historical cases (completion of a noetherian local ring, and quasi-finite nonfinite base change) and the question whether projectivity descends. Removed the supplied editorial footnote that inserts the 1962 answer into this exposé: it is absent from the scan. The separate printed erratum remains to be checked in its prescribed position. No modern answer is inserted into the question.','190, p. 318, remarks')
event('190-B2-properties-basic','targeted proof check','For surjectivity, lift a point of Y through the surjective base change and then through f-prime. For radiciality use the criterion that every geometric fiber has at most one point, which is detected after field extension. Flatness descends because tensor exactness can be checked after faithfully flat base extension, and faithful flatness then also uses descended surjectivity. Isomorphisms descend by descending the inverse with theorem 2 and checking the two composites. Open immersions descend by quotient topology and this isomorphism test. Closed immersions descend their quasi-coherent ideals using theorem 1, corollary 2. Affine morphisms descend their algebras using theorem 2; finite morphisms additionally require finite generation to descend.','190, p. 318, B.2 property list, basic cases')
event('190-B2-properties-remaining','carried as background without fault found','Read every listed property through separated morphisms, including the extra finite-type and locally-noetherian qualification for immersions. Smooth/simple, finite type, quasi-finite and immersion descent are not independently proved here. Their proofs require the corresponding finite-presentation/generation and local criteria. For open/closed maps and homeomorphisms one must use the quotient topology after the relevant base changes, not only a set-theoretic bijection. The list continues on 319.','190, p. 318, B.2 property list')
record_page('190',318,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 994–1053 with scan leaf 21 at 400 dpi, full page and all three enlarged bands. Read theorem 3, the weaker finite-cover hypothesis, both barred completion symbols, the projectivity question and every property in the beginning of B.2.

Removed the unprinted footnote merging the later 1962 erratum into the exposé, in both layers. Restored the completion bars, printed tous, hyphens, commas and double quotes, selective underlining (Weil and the B.2 conjunction et remain plain), and the run-in section heading. No new correction of the printed mathematical assertions is made here.

The full radicial/finite effectivity and ampleness assertions are carried as background with proof requirements stated. Checked the formal reduction using local finite faithfully flat refinements, conditional on theorem 3, and several basic property-descent cases. The remaining property list is explicitly carried as background, not described as a completed proof. The author's historical projectivity question remains intact for comparison with the separately printed erratum later.''')
from update_record_counts import update
update()
