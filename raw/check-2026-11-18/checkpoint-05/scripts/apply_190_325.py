from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='B.6',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-325',line,statement,'400-dpi full scan and three enlarged bands. '+why,kind,count=count)
 for old,new,line in [
  ('est un isomorphisme.','est un \\uline{isomorphisme}.','end of formal definition'),
  ('dorénavant $G$ plat sur','dorénavant $G$ \\uline{plat} sur','group hypothesis'),
  ('nom de fibré principal homogène sous','nom de \\uline{fibré principal homogène} sous','torsor terminology'),
  ('qui est fidèlement plat et quasi-compact sur','qui est \\uline{fidèlement plat} et \\uline{quasi-compact} sur','torsor definition'),
  ('une extension fidèlement\nplate et quasi-compacte','une \\uline{extension fidèlement plate} et \\uline{quasi-compacte}','trivializing extension'),
  ("soit trivial, i.e.","soit \\uline{trivial}, i. e.",'triviality explanation'),
  ('(i.e. admette','(i. e. admette','section explanation'),
  ('les points fermés de','les points \\uline{fermés} de','Jacobson reduction'),
  ("d'un $S'$ fini et plat\nsur","d'un $S'$ \\uline{fini et plat}\nsur",'finite cover'),
  ('si de plus $G$ est simple sur','si de plus $G$ est \\uline{simple} sur','smooth group'),
  ("supposer $S'$ étalé sur","supposer $S'$ \\uline{étalé} sur",'etale cover'),
  ('« cas géométrique »',r'\fquote{\uline{cas géométrique}}','geometric case'),
  ("si et seulement s'il est trivial","si et seulement si il est trivial",'geometric-case conclusion'),
  ('de Serre ([6], p. 1--12)','de SERRE ([6] p. 1-12)','first reference'),
  ('« trivialité locale »',r'\fquote{trivialité locale}','local-triviality terminology'),
  ('en particulier que $P$','en particulier, que $P$','definition punctuation'),
  ('isotrivial (resp. strictement isotrivial) si',r'\uline{isotrivial} (resp. \uline{strictement isotrivial}) si','two defined terms'),
  ('un morphisme fini et fidèlement plat (resp. un\nrevêtement étale surjectif)','un morphisme \\uline{fini et fidèlement plat} (resp. un\n\\uline{revêtement étale surjectif})','isotriviality conditions'),
  ('terminologie de Serre\n[6]','terminologie de SERRE\n[6]','second author name'),
  ('isotrivial.) La stricte','isotrivial). La stricte','parenthesis end'),
  ('$G$ est affine sur','$G$ est \\uline{affine} sur','last paragraph'),
  ('« descendre »',r'\fquote{descendre}','last word')]:
  r(old,new,line,why='Restore the printed typography, emphasis or punctuation at this exact occurrence.')
 r("\\[\n  P'=P\\times_SS'\n\\]","$P'=P\\times_SS'$",'base-changed torsor',kind='structure',why='Inline formula.')
 r("\\[\n  \\widehat P_s=P\\times_S\\operatorname{Spec}(\\widehat{\\mathcal O}_s)\n\\]","$\\widehat P_s=P\\times_S\\operatorname{Spec}(\\widehat{\\mathcal O}_s)$",'completed torsor',kind='structure',why='Inline formula.')
 r(r'\widehat P_s',r'\overline P_s','completed torsor letter',why='Straight completion bar, not a hat.')
 r(r'\widehat{\mathcal O}_s',r'\overline{\mathcal O}_s','four complete local rings',count=4,why='Straight completion bars.')
 r('« pré-schéma de\nJacobson »',r'\fquote{pré-schéma de Jacobson}','Jacobson terminology',why='Printed double quotes.')
 r("ou le spectre d'un anneau de\nJacobson plus généralement","ou un anneau de Jacobson plus généralement",'Jacobson example',why='The printed wording uses the ordinary ring-for-spectrum shorthand; the supplied expansion is not needed as a correction.')
 if tree=='fr_printed':
  r('terminologie de SERRE\n[6]','terminologie de SERRE\n[1]','second reference',why='The printed reference is [1]; its contrast with [6] above is recorded for bibliography verification.')
 else:
  r(r'\uline{fini et plat}',r'\uline{fini et fidèlement plat}','finite cover',kind='misprint of the original',why='The trivializing finite flat map must be surjective. Otherwise the empty finite flat map trivializes every formal torsor, even P empty over a nonempty base. Over a local connected base, requiring a nonempty finite flat cover is equivalent to faithful flatness.')
 s,_,_=page_text(rel,325)
 r(r'\mathcal O',r'\text{\uwave{O}}','six structure-ring identifiers',why='Ordinary wavy-underlined O.',count=s.count(r'\mathcal O'))
 upright_page(rel,layer,'190-325')
with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 csv.writer(f,delimiter='\t').writerow(['sources/fr/fr/190.tex','French corrected','190-325','second reference','B.6','SERRE [1]','SERRE [6]','The scan has [1]. The preceding citation of the same Serre terminology on this page is [6]; the exact bibliography target will be rechecked when page 327 is reached. This disposition remains provisional.','misprint of the original','low'])
event('190-B6-formal-torsor','targeted proof check','For a right G-action the map (g,p) to (p,p g) being an isomorphism says that two points of P over a base admit a unique relative group element, functorially. A section p identifies G with P by g maps to p g. Pulling P back along P to S gives the diagonal section, so an fpqc P is trivialized by itself. A flat group scheme is surjective because its identity section meets every fiber.','190, pp. 324–325, formal homogeneous-space definition')
event('190-B6-fpqc-triviality-unrestricted','refuted, with the refined statement\'s id','Without quasi-compactness of G, triviality after an fpqc extension does not imply the printed definition requiring P quasi-compact. Take S=Spec k and G=P the constant group scheme of the infinite group Z. The torsor is already trivial over the identity cover, but is not quasi-compact. Refined statement id: 190-B6-fpqc-triviality-qc. The historical assertion is retained rather than silently adding a group hypothesis.','190, p. 325, first equivalence')
event('190-B6-fpqc-triviality-qc','targeted proof check','If G is flat and quasi-compact, a trivialization P times_S S-prime isom G times_S S-prime over an fpqc cover makes P faithfully flat and quasi-compact by descent of these properties. Conversely an fpqc formal torsor is trivialized by the cover P to S. This is the exact restricted equivalence used in the finite-type and affine cases later on this page.','190, p. 325, refinement of the first equivalence')
event('190-B6-completions','targeted proof check','For each noetherian local base ring its completion is faithfully flat, a background input. Flatness and surjectivity of P over that local spectrum can therefore be tested after completion by faithful flat descent. Testing at every base point recovers global flatness and surjectivity. This verifies the stated completion test. The constructibility assertion for the finite-type family is carried as the standard finite-presentation/constructibility input; on a Jacobson base any nonempty constructible failure locus contains a closed point, giving the reduction to closed points.','190, p. 325, completion and Jacobson paragraphs')
event('190-B6-empty-finite-flat-map','refuted, with the refined statement\'s id','Let S be a nonempty complete local spectrum, G=S the trivial group and P empty. P is formally homogeneous because both sides of its torsor map are empty, but is not faithfully flat. Taking S-prime empty is finite and flat and makes P-prime the trivial torsor over the empty base. Thus the printed finite-and-flat existence condition is vacuous unless the map is a cover. Refined statement id: 190-B6-finite-flat-cover; corrected French adds fidelement.','190, p. 325, finite flat trivialization assertion')
event('190-B6-finite-flat-cover','carried as background without fault found','Existence of a finite faithfully flat multisection of a finite-type faithfully flat scheme over a complete noetherian local base is the substantive input to this claim. A proof needs a finite flat quasi-section and the passage from a quasi-finite neighborhood to a finite object over a henselian base; that full construction has not been supplied here. For a smooth torsor, a separable closed point of the special fiber and henselian lifting give a finite etale trivializing cover. If the residue field is algebraically closed, that cover splits and a section trivializes the torsor. The smoothness hypothesis remains in force in this last conclusion.','190, p. 325, complete-local trivialization and geometric case')
event('190-B6-nonsmooth-isotriviality','targeted proof check','The distinction for nonsmooth groups is real. Over K=F_p(t), the mu_p-torsor Spec K[u]/(u^p-t) becomes trivial over its finite faithfully flat root extension, but not over any finite etale cover. A p-th root of t in a separable extension would be both purely inseparable and separable over K, hence in K, a contradiction. This verifies a concrete reason for retaining the two different isotriviality notions.','190, p. 325, isotriviality definitions and concluding comment')
event('190-B6-affine-torsors','used and rechecked in this run','The pullback of P to its own fpqc cover is G times_S P, affine over P when G is affine over S. Affineness descends by B.2, so P is affine over S. The affine effective-descent statement then follows from theorem 2 and descent of the action and torsor identities. The sentence continues on 326.','190, p. 325, final paragraph')
record_page('190',325,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 1346–1397 with scan leaf 28 at 400 dpi and all three enlarged bands. Read the torsor definition, both inline base changes, every completion bar and local-ring subscript, the finite-flat and étale alternatives, both Serre reference numbers, and the isotriviality definitions.

Restored inline formulas, straight completion bars, wavy O, selective underlines, double quotes, SERRE capitals, the short page-range dash, printed si il, the comma after en particulier and parenthesis punctuation. Restored the printed ring-for-spectrum shorthand in both layers. Printed French has the second Serre reference [1]; corrected French provisionally retains [6], to be settled against the bibliography on 327. Corrected French supplies faithful flatness for the finite trivializing map, since otherwise the empty map gives a counterexample.

Checked trivialization by a section, the cover P itself, faithful flat completion testing and affine descent. An infinite constant group disproves the unrestricted converse from fpqc-local triviality to the printed quasi-compact torsor definition; its quasi-compact refinement is recorded without rewriting the historical claim. The finite-flat multisection theorem remains background. The smooth complete-local implication and its algebraically closed residue-field case retain the smoothness hypothesis. A mu_p-torsor over F_p(t) demonstrates why finite-flat and étale isotriviality differ.''')
from update_record_counts import update
update()
