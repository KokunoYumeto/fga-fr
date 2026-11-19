from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='B.3',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-319',line,statement,'400-dpi full image and three enlarged bands. '+why,kind,count=count)
 old='\\subsection*{3. Descente par morphismes finis fidèlement plats}\n\\addcontentsline{toc}{subsection}{3. Descente par morphismes finis fidèlement plats}\n\nSoit'
 new='\\addcontentsline{toc}{subsection}{3. Descente par morphismes finis fidèlement plats}\n\\result{3. \\uline{Descente par morphismes finis fidèlement plats}}{} Soit'
 r(old,new,'section heading',kind='structure',why='Roman underlined run-in heading, with period and dash.')
 r('un morphisme fini,','un morphisme \\uline{fini},','first sentence',why='Fini is underlined.')
 r('qui est localement libre de type fini','qui est \\uline{localement libre} de type fini','first sentence',why='Selective underline.')
 old="\\[\n  F'\\otimes_{\\mathcal O_S}\\mathcal A'\n  \\quad\\text{et}\\quad\n  \\mathcal A'\\otimes_{\\mathcal O_S}F'.\n\\]"
 new="$F'\\otimes_{\\mathcal O_S}\\mathcal A'$ et $\\mathcal A'\\otimes_{\\mathcal O_S}F'$."
 r(old,new,'two pullback modules',kind='structure',why='Both tensor products run inline with the prose.')
 r("$(\\mathcal A'\\otimes_{\\mathcal O_S}\\mathcal A')$-modules et, compte tenu que","$(\\mathcal A'\\otimes\\mathcal A')$-module, et compte tenu que",'homomorphism between pullbacks',why='The tensor base is omitted here, module is singular, and the comma precedes et. These printed choices are retained in both layers.')
 r("\\operatorname{Hom}_{\\mathcal O_S}(F',F'),\n\\]","\\operatorname{Hom}_{\\mathcal O_S}(F',F')\n\\]",'endomorphism display',why='No terminal comma.')
 r('i.e.','i. e.','prose and formula abbreviations',why='Printed spacing.',count=2)
 r('T_{f\\xi}(x)=fT_\\xi(x),','T_{f\\xi}(x)=fT_\\xi(x)','first equality','(3.1)',why='No comma between the two equalities.')
 r('T_{\\xi f}(x)=T_\\xi(fx),','T_{\\xi f}x=T_\\xi(fx)','second equality','(3.1)',why='The left argument has no parentheses; no terminal comma.')
 r(r"\operatorname{id}_{F'},",r"\operatorname{id}_{F'}",'identity end','(3.2)',why='No terminal comma.')
 r('T_{\\xi\\eta}=T_\\xi T_\\eta.','T_{\\xi\\eta}=T_\\xi T_\\eta','representation identity','(3.3)',why='No terminal period.')
 span="une donnée de descente sur $F'$ équivaut à une\nreprésentation du faisceau de $\\mathcal O_S$-algèbres\n$\\mathcal U=\\operatorname{Hom}_{\\mathcal O_S}(\\mathcal A',\\mathcal A')$ dans\nle faisceau de $\\mathcal O_S$-algèbres\n$\\operatorname{Hom}_{\\mathcal O_S}(F',F')$, satisfaisant les deux conditions de\nlinéarité (3.1)."
 r('\\emph{'+span+'}',underline_prose(span.replace('\n',' ')),'representation summary',why='Prose underline excludes variables, formulas and the numbered reference.')
 r(r'\mathcal A',r'\text{\uwave{A}}','twenty algebra identifiers',why='Ordinary wavy-underlined A, including the dual with a check accent.',count=20)
 r(r'\mathcal O',r'\text{\uwave{O}}','eleven structure-ring identifiers',why='Ordinary wavy-underlined O.',count=11)
 r(r'\operatorname{Hom}',r'\mathop{\text{\uwave{Hom}}}\nolimits','four internal Hom operators',why='All four Hom signs are wavy-underlined.',count=4)
 r(r'\mathcal U',r'\text{\uwave{U}}','five endomorphism-algebra identifiers',why='The principal occurrences are ordinary wavy-underlined U; the unit subscripts are handled separately.',count=5)
 if tree=='fr_printed':
  r(r'1_{\text{\uwave{U}}}',r'1_U','two unit subscripts','(3.2)',why='The printed U letters in these two subscripts have no wavy underline.',count=2)
 upright_page(rel,layer,'190-319')
with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 for line in ['first unit subscript','second unit subscript']:
  w.writerow(['sources/fr/fr/190.tex','French corrected','190-319',line,'(3.2)',r'1_U',r'1_{\text{\uwave{U}}}','The middle crop omits the wavy underline in this subscript. Corrected French identifies the unit with the same wavy-underlined endomorphism algebra defined immediately above.','misprint of the original','low'])
event('190-B2-proper','used and rechecked in this run','Properness descends from finite type, separatedness and universal closedness. Separatedness is closed-immersion descent applied to the diagonal. For universal closedness, repeat the closed-map descent argument after every base change; the faithfully flat quasi-compact cover remains such a cover. Finite-type descent is the background input already identified on 318. The sentence about the then-unsettled projective case is historical and retained.','190, p. 319, opening two lines')
event('190-B3-finite-algebra','targeted proof check','A finite locally free algebra sheaf of positive rank is flat and has nonzero residue fibers, hence gives a faithfully flat finite morphism. The equivalence between quasi-coherent sheaves on its relative Spec and modules over that algebra identifies the two pullbacks with F-prime tensor A-prime and A-prime tensor F-prime in the printed order.','190, p. 319, B.3 opening paragraph')
event('190-3.1-3.3','targeted proof check','Locally put B=A-prime, N=F-prime and U=End_A(B)=B tensor B-dual. Given the B tensor B-linear map phi:N tensor B to B tensor N, set delta(n)=phi(n tensor 1) and T_(b tensor lambda)(n)=b(lambda tensor id)delta(n). This gives exactly T_(f xi)=f T_xi and T_(xi f)(n)=T_xi(fn). A dual basis e_i,lambda_i reconstructs delta(n)=sum e_i tensor T_(1 tensor lambda_i)(n), so the correspondence is reversible. The diagonal condition is multiplication composed with delta=id, equivalently T_(id_B)=id_N. The cocycle condition is the coassociativity identity for delta; using the rank-one composition (b tensor lambda)(c tensor mu)=b lambda(c) tensor mu identifies it with T_(xi eta)=T_xi T_eta. Thus the operator order and both linearity formulas are consistent.','190, p. 319, (3.1)–(3.3) and representation summary')
record_page('190',319,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 1040–1108 with scan leaf 22 at 400 dpi, full page and all three enlarged bands. Read every algebra and structure-ring identifier, the dual check accent, four internal Hom signs, the five U occurrences, all subscripts and operator orders in (3.1)–(3.3), and the concluding pairing.

Restored the run-in heading, selective prose underlines, the two initial tensor products inline, the printed omission of a repeated tensor base, singular module, comma placement, abbreviation spacing and equation punctuation. Removed the unprinted parentheses around x on the left of the second equality in (3.1). Restored wavy-underlined A, O, U and internal Hom. The two plain U unit subscripts of (3.2) are represented in printed French; their notation repairs in corrected French have separate rows. Small ink specks near the first quasi-cohérents and the concluding U are not interpreted as additional mathematical punctuation and remain points for the final visual review.

Checked the finite locally free setup and the operator description using an explicit dual-basis conversion, including the two linearity laws, identity and multiplication order. Properness descent is checked from the preceding cases with finite-type descent kept as the stated background input. The pairing discussion continues on 320.

Process incident: the first application of this page's script stopped at a Python quoting syntax error before any edit. The same tool batch then prematurely prepared page 320 and returned its source text. The quoting error was repaired, and this page's edits and record were completed before resuming the page-320 audit. No page-320 edit or completion was made during that premature preparation.''')
from update_record_counts import update
update()
