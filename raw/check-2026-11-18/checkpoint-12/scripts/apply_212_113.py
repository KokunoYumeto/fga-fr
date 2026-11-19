from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/212.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'212-113',line,'6.1; 6.2','400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 s,_,_=page_text(rel,113)
 for a,b,body in list(footnotes(s)):
  r(s[a:b],'','Theorem 6.1(i)',kind='structure',why='There is no footnote or call on this page. The later erratum must remain in its own section.')
 r("(si $S$ est noethérien et si $R$ provient d'une\nrelation d'équivalence)","(si $S$ est noethérien)",'Theorem 6.1(i)',why='The scan has only the noetherian hypothesis. The added restriction is a merged authorial erratum, not a printed reading.')
 a="\\begin{enumerate}\n\\item[(a)] $p_1:R_1\\to X$ est propre et plat;\n\\item[(b)] $R_1\\to X\\times_S X$ est un morphisme fini, ou ce qui revient au\nmême en vertu de (a), à fibres finies (condition automatiquement vérifiée si\n$R$ provient d'une relation d'équivalence).\n\\end{enumerate}\nSous ces conditions:"
 b="(a) $p_1:R_1\\to X$ est propre et plat ; (b) $R_1\\to X\\times_S X$ est un morphisme fini, ou ce qui revient au\nmême en vertu de (a), à fibres finies (condition automatiquement vérifiée si\n$R$ provient d'une relation d'équivalence). Sous ces conditions :"
 r(a,b,'Theorem 6.1 hypotheses',kind='structure',why='The two hypotheses and the introduction to the conclusions form one running paragraph, not a displayed list.')
 r('i.e.','i. e.','Theorems 6.1(iii) and 6.2(b)',count=2,why='Both printed abbreviations are spaced.')
 r('En résumé:', 'En résumé :','Scholie introduction',why='The colon is spaced.')
 r('fidèlement plat, et surjectif','fidèlement plat et surjectif','Scholie',why='There is no comma after plat.')
 r('résultat suivant:', 'résultat suivant :','Theorem 6.2 introduction',why='The colon is spaced.')
 a="on suppose que:\n\\begin{enumerate}\n\\item[(a)] $p_1:R_1\\to X$ est plat et de type fini;\n\\item[(b)] le morphisme $R_1\\to X\\times_S X$ est quasi-fini (i. e. à fibres\nfinies).\n\\end{enumerate}\nAlors il existe"
 b="on suppose que : (a) $p_1:R_1\\to X$ est plat et de type fini ; (b) Le morphisme $R_1\\to X\\times_S X$ est quasi-fini, (i. e. à fibres\nfinies). Alors il existe"
 r(a,b,'Theorem 6.2 hypotheses',kind='structure',why='The hypotheses run in the theorem paragraph; Le is capitalized, and quasi-fini is followed by a comma before the parenthesis.')
 r('dense dans $X$ '+r'\emph{saturé}',r'\uline{dense} dans $X$ \uline{saturé}','Theorem 6.2 conclusion introduction',why='Both dense and saturé are straight-underlined.')
 r('tel que:', 'tel que :','Theorem 6.2 conclusion introduction',why='The colon is spaced.')
 r('pour $R_U$ (donc','pour $R_U$, (donc','Theorem 6.2(ii)',why='The scan has a comma before the parenthesis.')
 r("\\[\n  (R_U)_1\\longrightarrow U\\times_{U/R_U}U\n\\]\nest surjectif.",r'$(R_U)_1\to U\times_{U/R_U}U$ est surjectif.','Theorem 6.2(ii), last formula',kind='structure',why='The comparison map is inline and has an ordinary arrow.')
 for a,b,count in [('$R$ provient',r'$\mathcal R$ provient',2),('mod $R$',r'mod $\mathcal R$',1),('définie par $R$',r'définie par $\mathcal R$',1),('pour $R$',r'pour $\mathcal R$',2),('$R$ une',r'$\mathcal R$ une',1),('par $R$ dans',r'par $\mathcal R$ dans',1),(r'$X/R=Y$',r'$X/\mathcal R=Y$',1)]:
  r(a,b,'whole groupoid symbols',count=count,why='The groupoid letter is script R; the relation scheme in the Scholie remains ordinary R.')
 s,_,_=page_text(rel,113)
 r('R_U',r'\mathcal R_U','restricted groupoid symbols in 6.2',count=s.count('R_U'),why='The restricted groupoid is script R with subscript U, including inside the final comparison map.')
 upright_page(rel,layer,'212-113')

event('212-6.1-hypotheses','targeted proof check','Since X is separated over S, X times_S X is separated over X. Any X-morphism from R1, proper over X by (a), into that separated X-scheme is proper (graph is closed, followed by a proper projection). Consequently finite fibres imply quasi-finiteness and, with properness, finiteness. Here finite type follows from properness and the locally noetherian assumptions. For a genuine equivalence relation, the comparison is a monomorphism and therefore has at most one geometric point per fibre; the same argument gives the parenthetical automatic condition. Proper plus quasi-finite implies finite is the standard input.','212, pp. 112–113, Theorem 6.1(a),(b)')
event('212-6.1','carried as background without fault found','The source gives only a reduction by suitable quasi-sections to 5.1. A full proof requires construction of those quasi-sections, the finite quotient theorem, descent and gluing of the resulting quotient, and verification of the asserted properness and effectiveness. These substantial steps have not been independently established here. The unconditional quasi-projectivity conclusion printed in (i) is restored in both layers; the previously merged later erratum is removed and will be examined in its own place. This is not a claim that the original unrestricted quasi-projectivity conclusion has been proved.','212, p. 113, Theorem 6.1(i)–(iii) and proof sketch')
event('212-6.1-open','targeted proof check','Once the orbit fibres and quotient topology in (ii) are known, openness follows directly: the saturation of an open V in X is p2(p1 inverse(V)). Both projections are flat and locally of finite presentation over the locally noetherian X, hence open, so the saturation is open. Quotient topology then makes f(V) open. This checks only the openness deduction, not existence of the quotient or its full base-change properties.','212, p. 113, Theorem 6.1(ii)')
event('212-6-scholie','used and rechecked in this run','A proper faithfully flat morphism has the effective kernel relation by fpqc descent, and its projections are proper and flat by base change. Conversely, for X quasi-projective over locally noetherian S, a proper flat equivalence relation satisfies the extra finite-fibre condition of 6.1 by the monomorphism argument above; 6.1 supplies its effective quotient. Thus the Scholie is conditional on the substantive existence theorem, with the coequalizer property giving uniqueness. The redundant word surjectif is preserved.','212, p. 113, Scholie')
event('212-6.2','carried as background without fault found','The dense saturated open quotient theorem is stated with a flat finite-type source projection and quasi-finite comparison map. The present page supplies no proof beyond saying that the same method applies. A proof must construct an invariant dense open simultaneously across the generic components and descend the local quotient there; ordinary generic flatness alone does not supply these steps. The continuation of (iii) will be read on p. 114.','212, p. 113, Theorem 6.2(a),(b),(i),(ii)')
record_page('212',113,r'''Compared sources/fr_printed/fr/212.tex entry lines 653–712 and sources/fr/fr/212.tex entry lines 656–715 with scan leaf 16 at 400 dpi, full page and all three enlarged bands. Read all hypotheses, conclusions and the proof sketch of 6.1, the Scholie and 6.2 through (ii).

Removed the unprinted footnote and merged later restriction on quasi-projectivity from both French layers. The printed hypothesis in 6.1(i) is simply that S is noetherian. Both layers restore the running hypothesis paragraphs in 6.1 and 6.2, the inline final comparison map, script groupoid letters (including the restricted groupoid), the separate ordinary relation letter in the Scholie, the two underlined words dense and saturé, exact commas, capital Le, spaced abbreviations and upright mathematics. No new mathematical correction distinguishes the French layers on this page.

Checked the finite-fibre equivalence in 6.1(b), the openness deduction from orbit fibres and quotient topology, and the dependence of the Scholie on effective descent. The quotient-existence theorems and their quasi-section reductions are explicitly background steps, not labelled as independently proved. The later erratum concerning 6.1(i) remains to be examined in source order.''')
from update_record_counts import update
update()
