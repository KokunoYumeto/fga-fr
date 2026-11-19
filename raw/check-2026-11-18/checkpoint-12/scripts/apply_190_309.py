from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-309',line,statement,'400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 if tree=='fr_printed':
  for old,new,line in [("réciproque $\\mathfrak T'$ sur $\\overline{S'}$", "réciproque $\\mathfrak T'$ sur $S'$",'first analytic pullback'),("cohérent $\\mathcal A'$ d'algèbres sur $\\overline{S'}$", "cohérent $\\mathcal A$ d'algèbres sur $S'$",'first analytic algebra'),("Par hypothèse, sur $\\overline{S'}$", "Par hypothèse, sur $S'$",'normal-case hypothesis')]:
   r(old,new,line,'3',why='The scan omits the indicated analytic-base bar; at the first algebra mention it also omits the prime on A. Corrected French retains the typed identifiers appropriate to the pullback.')
 r("D'autre part, $\\mathcal A'$", "D'autre part $\\mathcal A'$",'canonical analytic descent datum','3',why='No comma after part.')
 r('i.e.','i. e.','five explanatory abbreviations','3',why='Spaced abbreviation.',count=5)
 old="deux images réciproques sur\n\\[\n  \\overline{S'}\\times_{\\overline S}\\overline{S'}\n  =\\overline{(S'\\times_SS')},\n\\]\n(satisfaisant aux conditions (i), (ii)), et"
 new="deux images réciproques sur $\\overline S'\\times_{\\overline S}\\overline S'=\\overline{(S'\\times_SS')}$, (satisfaisant des conditions (i), (ii)) et"
 r(old,new,'analytic fiber product identity','3',kind='structure',why='The identity runs in the line, primes outside the S bars; the print says des conditions and has no comma after the parenthesis.')
 r("\\overline{S'}\\longrightarrow\\overline S", "\\overline S'\\longrightarrow\\overline S",'analytic base map','3',why='The prime lies outside the bar.')
 r("$A'$", "$\\text{\\uwave{A}}'$",'two algebraic algebra occurrences','3',why='Algebraic A is an ordinary wavy-underlined letter, unlike the analytic script A.',count=2)
 r('$A$ sur $S$','$\\text{\\uwave{A}}$ sur $S$','descended algebra','3',why='Ordinary wavy-underlined A.')
 for term in ['complétés','réduit','homéomorphisme universel']:
  r('\\emph{'+term+'}','\\uline{'+term+'}','emphasized term '+term,'3',why='Underline in the print.')
 r('Grauert--Remmert','Grauert-Remmert','theorem name','3',why='Short hyphen.')
 r(r'\mathcal O',r'\text{\uwave{O}}','two structure-sheaf letters','3',why='Ordinary wavy-underlined O.',count=2)
 r('« formelle »',r'\fquote{formelle}','formal-locality description','3',why='Double quotes.')
 r('préschéma','pré-schéma','prescheme spelling','3',why='Printed hyphen.',count=4)
 r(r'\emph{fini, surjectif, radiciel}',r'\uline{fini}, \uline{surjectif}, \uline{radiciel}','universal-homeomorphism hypotheses','3',why='Underlined words, commas outside underlines.')
 r('tel que, pour tout','tel que pour tout','universal-homeomorphism parenthesis','3',why='No comma after que.')
 old="Alors le foncteur\n$T\\longmapsto T'$ est une \\emph{équivalence de catégories de la catégorie des\npré-schémas $T$ étalés sur $S$ avec la catégorie des pré-schémas $T'$ étalés sur\n$S'$}."
 plain="Alors le foncteur $T\\rightsquigarrow T'$ est une équivalence de catégories de la catégorie des pré-schémas $T$ étalés sur $S$ avec la catégorie des pré-schémas $T'$ étalés sur $S'$."
 r(old,underline_prose(plain),'equivalence of étale categories','3',why='The entire conclusion prose from Alors is underlined, excluding variables and final period; the assignment arrow is wavy.')
 r("$S'=(S,\\text{\\uwave{O}}_S/\\mathcal J)$,", "$S'=(S,\\text{\\uwave{O}}_S/\\mathcal J)$",'last nilpotent quotient formula','3',why='No comma is printed at the end of the page.')
 upright_page(rel,layer,'190-309')
with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 writer=csv.writer(f,delimiter='\t')
 for line,old,new,reason in [
  ('first analytic pullback',"réciproque $\\mathfrak T'$ sur $S'$","réciproque $\\mathfrak T'$ sur $\\overline{S'}$",'The pulled-back analytic cover is on the analytification of S-prime.'),
  ('first analytic algebra, prime',"cohérent $\\mathcal A$ d'algèbres", "cohérent $\\mathcal A'$ d'algèbres",'This is the pullback algebra, distinguished from A on S-bar and denoted A-prime in every following occurrence.'),
  ('first analytic algebra, base',"d'algèbres sur $S'$, image", "d'algèbres sur $\\overline{S'}$, image",'The analytic coherent algebra is on S-prime analytified.'),
  ('normal-case hypothesis',"Par hypothèse, sur $S'$", "Par hypothèse, sur $\\overline{S'}$",'The hypothesis algebraizes analytic covers of the analytification of S-prime.')]:
  writer.writerow(['sources/fr/fr/190.tex','French corrected','190-309',line,'3',old,new,'Confirmed the supplied corrected identifier against the omission visible in the 400-dpi top band. '+reason,'misprint of the original','low'])
event('190-3-grauert-remmert-reduction','targeted proof check','Checked the reduction under a finite strict epimorphism. Analytic full faithfulness algebraizes the descent isomorphism; faithfulness transfers the cocycle. The candidate descended finite module is a kernel and hence coherent over the noetherian base. Flat completion commutes with this kernel and the finite algebra operations; algebraic and analytic local completions coincide. Analytic effectiveness therefore makes the candidate completed module flat and its completed pullback map an isomorphism; faithful flatness of completion detects both. Multiplication/unit descend compatibly and étaleness is checked after the same local comparison. This argument uses completion flatness, analytic/algebraic completion comparison and the normal-case theorem as background. Iteration uses the finite factorization assertion from 2(b), not re-proved here.','190, p. 309, first paragraph')
event('190-3-reduction-normalization','targeted proof check','For a reduced finite-type complex scheme, finite normalization is schematically dominant and hence a finite epimorphism by 2(b); the previous reduction applies. Passing from the reduction to a nonreduced scheme uses nilpotent invariance of the étale category, and its analytic counterpart. Finiteness of normalization and the nilpotent invariance are background inputs. This explains the printed brief transition without inserting those proofs into the text.','190, p. 309, end of first paragraph')
event('190-3-universal-homeomorphism','carried as background without fault found','Read the finite-surjective-radicial characterization of a finite-type universal homeomorphism and the asserted equivalence of étale categories. The Hom comparison and nilpotent-thickening reduction are the stated proof inputs; the nilpotent argument continues on 310. The theorem is not marked independently re-proved here. The phrase factorisation pour les épimorphismes stricts finis is retained exactly rather than editorially shortened.','190, p. 309, second paragraph')
record_page('190',309,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 538–590 with scan leaf 12 at 400 dpi, full page and all three enlarged bands. Read the proof through every algebra/analytic distinction, the universal-homeomorphism statement, Hom formula and final quotient. Also viewed a local script/Gothic font specimen solely to assess handwritten letter families, not as textual authority: supplied Gothic T and script analytic A/J are retained provisionally; their handwritten forms remain a second-review point.

Restored three omitted analytic-base bars and the omitted prime at the first analytic algebra mention in printed French; confirmed the supplied corrected identifiers with four explicit corrected-layer rows. Restored the inline fiber-product formula, bar extents, des conditions, comma omissions, five spaced abbreviations, ordinary wavy-underlined algebraic A and O, short Grauert-Remmert hyphen, double quotes, hyphenated pré-schéma, selective underlines and the wavy assignment arrow. The final nilpotent-quotient formula is inline and has no trailing comma.

Checked the finite-strict-epimorphism reduction of analytic algebraization, explaining its coherent-kernel and completion tests and naming the external background inputs without claiming their proofs. Checked how finite normalization and nilpotent invariance complete the reduction, conditional on those background facts. The universal-homeomorphism proof continues on 310 and is carried as background here.''')
from update_record_counts import update
update()
