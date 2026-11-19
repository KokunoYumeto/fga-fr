from audit_utils import *
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
 prior_operations={(x['file'],x['printed_page'],x['old'],x['new']) for x in csv.DictReader(f,delimiter='\t')}

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/195.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  if (rel,'195-376',a,b) in prior_operations: return
  replace(rel,a,b,layer,'195-376',line,'A.5','400-dpi full scan and three enlarged bands. '+why,kind,count=count)
 s,_,_=page_text(rel,376)
 for a,b,body in list(footnotes(s)):
  r(s[a:b],'','editorial erratum footnote',kind='structure',why='There is no footnote in the printed page. Remove the supplied editorial integration of later errata; those will remain in their own sections.')
 r('une structure de $A$-module','une structure de $A$-\\uline{module}','intrinsic module structure',why='Only module is underlined in the print.')
 r('« se réduisent suivant $\\xi$ »',r'\fquote{se réduisent suivant $\xi$}','reduction terminology',why='The print uses ordinary double quotation marks.')
 r("$A$-module s'identifie à\n\\[\n  \\operatorname{Hom}_{\\Lambda}(\\mathfrak m_\\xi/\\mathfrak m_\\xi^2,A),\n\\]\noù", "$A$-module s'identifie à $\\operatorname{Hom}_{\\Lambda}(\\mathfrak m_\\xi/\\mathfrak m_\\xi^2,A)$, où",'first tangent identification',kind='structure',why='The Hom expression runs in the text; it is not displayed.')
 r('i.e. si $A$','i. e. si $A$','kernel explanation',why='Printed abbreviation spacing.')
 r(r'\result{PROPOSITION}{5.1}',r'\result{PROPOSITION}{5, 1}','first proposition number',why='Printed comma-numbered statement.')
 r('soit un anneau\nnoethérien,','soit un anneau \\uline{noethérien},','noetherian condition',why='Printed selective underline.')
 r('un espace vectoriel de dimension\nfinie sur $K$','un espace vectoriel de \\uline{dimension finie} sur $K$','finite-dimensional condition',why='Printed selective underline.')
 old=r'''\[
  F(I_K,\xi)=
  \operatorname{Hom}\!\left(
    \frac{\mathfrak m_\xi/\mathfrak m_\xi^2}
         {\operatorname{im}(\mathfrak n_\xi/\mathfrak n_\xi^2)},K
  \right),
\]'''
 new=r'''\[
  F(I_K,\xi)=\operatorname{Hom}(\mathfrak m_\xi/\mathfrak m_\xi^2+\mathfrak n_\xi\text{\uwave{O}}_\xi),K)
\]'''
 r(old,new,'Proposition 5, 1 displayed formula',why='The scan already has the base-ideal summand n_xi O_xi, a slash quotient, a local wavy O, and the printed unmatched parenthesis. Restore that exact formula instead of the supplied nested quotient attributed to an erratum.')
 r("où $\\mathfrak n_\\xi$ est l'idéal maximal de $\\Lambda$, noyau de\nl'homomorphisme $\\Lambda\\longrightarrow K$.", "(où $\\mathfrak n_\\xi$ est l'idéal maximal de $\\Lambda$ noyau de l'homomorphisme $\\Lambda\\longrightarrow K$),",'base-ideal parenthesis',why='The explanation is parenthetical, with no comma after Lambda and a comma after the closing parenthesis.')
 r('\nEn particulier, la dimension','\nen particulier, la dimension','dimension sentence continuation',why='The sentence continues with lowercase en after the parenthesis.')
 r("la dimension de l'espace vectoriel ainsi corrigé sur le corps", "la dimension de l'espace vectoriel $\\mathfrak m_\\xi/\\mathfrak m_\\xi^2$ sur le corps",'following dimension comparison',why='The print explicitly gives the absolute m_xi/m_xi-squared. Remove the editorial ainsi corrigé replacement; a later erratum is not merged here.')
 r('soit local complet, et $O=O_\\xi$. On dit que $O$ est\n\\emph{simple sur $\\Lambda$}', 'soit local complet, et $O=O_\\xi$. On dit que $O$ \\uline{est simple sur} $\\Lambda$','first simplicity definition',why='The print underlines est simple sur, leaving Lambda separate.')
 r('$O$ est simple sur $\\Lambda$ si','$O$ \\uline{est simple sur} $\\Lambda$ si','general simplicity definition',why='The same prose phrase is underlined.')
 r('est triviale (par exemple,','est triviale, (par exemple,','residue-extension parenthesis',why='Restore the comma before the parenthesis.')
 r(r'\result{PROPOSITION}{5.2}',r'\result{PROPOSITION}{5, 2}','second proposition number',why='Printed comma-numbered statement.')
 r('pour tout homomorphisme surjectif','pour tout homomorphisme \\uline{surjectif}','lifting condition',why='Printed selective underline.')
 r("$F(A)\\longrightarrow F(A')$ est surjectif.","$F(A)\\longrightarrow F(A')$ est \\uline{surjectif}.",'surjectivity of F',why='Printed selective underline.')
 r('quand $A$ est local,','quand $A$ est \\uline{local},','local test',why='Printed selective underline.')
 r('des invariants infinitésimaux','des invariants \\uline{infinitésimaux}','last word emphasis',why='The final word is underlined, continuing into the following page.')
 if tree=='fr_printed':
  r("ce\n$A$-module s'identifie", "ce\n$K$-module s'identifie",'first tangent module scalar',why='The print has K although the construction and target are over A.')
  r("$A\\longrightarrow A'$ dans", "$A\\longrightarrow A'$. dans",'first surjection punctuation',why='The print has a stray period after the displayed-in-line A-prime before dans.')
 else:
  r(r'\mathfrak m_\xi/\mathfrak m_\xi^2+\mathfrak n_\xi\text{\uwave{O}}_\xi)',r'\mathfrak m_\xi/(\mathfrak m_\xi^2+\mathfrak n_\xi\text{\uwave{O}}_\xi)','Proposition 5, 1 denominator grouping',kind='misprint of the original',why='Insert the missing opening parenthesis after the slash. The existing closing parenthesis and the base-ideal term show that the denominator is the sum m-squared plus nO; the Hom call is then balanced. This repairs a printed delimiter, without merging the later change to the dimension sentence.')
 s,_,_=page_text(rel,376)
 r(r'\mathcal C',r'\text{\uwave{C}}','category letters',count=s.count(r'\mathcal C'),why='The category is an upright C with a wavy underline.')
 upright_page(rel,layer,'195-376')

with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 for line,old,new,why in [('first tangent module scalar','K-module','A-module','The fibre F(I_A,xi) was just made into an A-module, and A is the coefficient module in the following Hom; no K has yet been introduced.'),('first surjection punctuation',"A-prime. dans","A-prime dans",'The full stop splits the phrase an epimorphism in C; the printed statement continues as a single sentence.')]:
  w.writerow(['sources/fr/fr/195.tex','French corrected','195-376',line,'A.5',old,new,'Enlarged scan: '+why+' Existing corrected reading confirmed.','misprint of the original','low'])
event('195-A5-tangent-module','targeted proof check','The splitting A to A[t]/t^2 gives the zero of the fibre. The fibre product I_A times_A I_A is A plus At_1 plus At_2 with all t-products zero; the map sending both t_1,t_2 to t defines addition on the fibre after left exactness identifies the fibre of the product. Scaling t by a in A gives scalar multiplication. These polynomial maps satisfy the module laws. In the pro-represented description, a lift of xi is uniquely xi+t d, with d a continuous Lambda-derivation O to A; Leibniz is exactly multiplicativity modulo t^2. This verifies the module structure and the correction K-module to A-module.','195, p. 376, opening tangent construction')
event('195-A5-general-tangent-Hom','refuted, with refined statement 195-A5-continuous-derivations','The displayed-in-line identification with Hom_Lambda(m_xi/m_xi^2,A) is false for general A. Take Lambda=k, O=A=k[e]/e^2 and xi=id. Its kernel m_xi is zero, but d(e)=e defines a nonzero k-derivation O to A, and e maps to e+t e in A[t]/t^2 as a nontrivial lift. The correct general module is the module of continuous Lambda-derivations, equivalently the appropriate continuous differential Hom. The broad printed identification is retained in both layers and qualified in the notes.','195, p. 376, first Hom identification')
event('195-5.1-formula','refuted, with refined statement 195-5.1-relative-tangent','The scan already contains n_xi O_xi in the denominator; only its opening parenthesis is missing. After that delimiter repair, the proposed identification still needs a separability condition on the residue field over the base residue field. For Lambda=F_p(s), O=K=Lambda(u) with u^p=s and xi=id, m_xi=0 but d(u)=1 is a nonzero Lambda-derivation. The tangent module is therefore nonzero while the displayed conormal dual is zero. With separable residue extension the transitivity sequence for differentials gives the relative cotangent-space formula. The following absolute dimension comparison also fails even with identical residue fields: for O=Lambda=k[[s]], F is the singleton functor, so the tangent dimension is zero while dim(m/m^2)=1. The absolute comparison has been restored in both text layers; its later erratum will be checked separately.','195, p. 376, Proposition 5, 1 formula and following dimension sentence')
event('195-5.1-noetherian-criterion','carried as background without fault found','The finite-dimensional tangent/noetherian equivalence requires the complete pro-artinian algebra theorem: finite continuous cotangent dimension yields finitely many topological generators over a complete noetherian local base with finite residue extension, and topological Nakayama produces a quotient of the completed localization of a finite polynomial algebra. That quotient is noetherian. Conversely such a noetherian presentation gives finite tangent dimension. A complete proof of that topological theorem and its exact hypotheses is deferred to the notes; the incorrect displayed identifications are not used as its proof.','195, p. 376, first assertion of Proposition 5, 1')
event('195-5.2','refuted, with refined statement 195-5.2-nilpotent-lifting','The assertion for all epimorphisms, taken literally, fails even for a finite etale algebra. Set Lambda=R and O=C, which is simple by the printed definition with no polynomial variables. The surjection A=R times C to A-prime=C belongs to C. F(A)=Hom_R(C,R) times Hom_R(C,C) is empty, whereas F(A-prime) contains id; thus F(A) to F(A-prime) is not surjective. The infinitesimal/formal-smoothness condition uses surjections with nilpotent kernel. The source sentence reducing arbitrary surjections to local small extensions silently loses discarded connected components. The historical assertion is retained and the correction of the theorem is reserved for the notes.','195, p. 376, Proposition 5, 2 and the subsequent reduction')
event('195-5.2-small-extensions','targeted proof check','For a surjection between nonzero artinian local algebras, the kernel has a finite composition filtration by ideals, with successive kernels annihilated by the maximal ideal. Thus successive lifting reduces nilpotent lifting to the stated small extensions. Finite products handle nilpotent surjections between general artinian algebras because such a surjection preserves the connected-component decomposition. A completed polynomial localization has the lifting property by lifting its coordinates, and a finite etale algebra lifts uniquely after this choice over a nilpotent ideal. The general converse and nonnoetherian presentation theorem are background, to be reconciled with the separate author erratum later.','195, p. 376, simplicity definition and small-extension reduction')
record_page('195',376,r'''Compared sources/fr_printed/fr/195.tex entry lines 355–421 and sources/fr/fr/195.tex entry lines 356–422 with scan leaf 9 at 400 dpi, full page and all three enlarged bands. Inspected the fibre inverse-image exponent, primes, first inline Hom, every term and delimiter of the Proposition 5, 1 display, the following absolute cotangent quotient, and the two surjection arrows.

Removed both unprinted editorial footnotes merging later errata. Restored the actual displayed slash quotient, which already contains the base-ideal summand, the parenthetical definition of n_xi, the absolute m_xi/m_xi-squared dimension sentence instead of “ainsi corrigé”, the inline first Hom, exact punctuation, ordinary quotes, comma-numbered propositions, selective underlining, wavy C and upright letters. The local wavy O in the denominator is retained as printed in both layers. Printed French restores K-module and the stray period after A-prime; corrected French keeps A-module and removes that period. Corrected French additionally inserts the clearly missing opening parenthesis of the denominator. The small loose accent above the opening line is treated as an ink mark, with no textual accent inferred.

Checked the intrinsic module operations and the continuous-derivation interpretation. Recorded explicit counterexamples to the general kernel-Hom formula, to the conormal formula without residue separability, to the absolute dimension comparison, and to Proposition 5, 2 with arbitrary surjections. The finite-tangent/noetherian theorem and general structure theorem remain identified background. The small-extension argument is valid for nilpotent surjections; it does not justify dropping arbitrary components. Substantive qualifications are kept for the notes, and the author's errata remain separate.''')
from update_record_counts import update
update()
