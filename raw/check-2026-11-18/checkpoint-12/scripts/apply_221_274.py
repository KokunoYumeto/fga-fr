from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-274',line,'6, norm morphisms / (a)',
                'Scan leaf 27 at 400 dpi and all three enlarged bands: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,274)
    for a,b,body in list(footnotes(s)):
        r(s[a:b],'','inequality editorial note','There is no footnote in the print.','structure')
    old="en général : \\[ \\pi_{X/S}:\\operatorname{Quot}^n_{\\mathcal F/X/S} \\longrightarrow\\Gamma^n_S(X). \\] Si $X$ est plat sur $S$, on identifie cette cible à $\\operatorname{Symm}^n_S(X)$.\nIndépendamment de l'identification précédente, lorsque $X$ est séparé sur $S$, la construction par la famille finie et plate pour $\\mathcal F=\\mathcal O_X$ donne un morphisme :"
    new="en particulier, si la puissance symétrique $n$-ième de $X$ sur $S$ existe :\n\\[\n\\pi_{X/S}:\\operatorname{Quot}^n_{\\mathcal F/X/S}\\to\\operatorname{Symm}^n_S(X).\n\\]\nLe cas le plus important est celui où $\\mathcal F=\\mathcal O_X$, qui donne un morphisme :"
    r(old,new,'middle norm construction','The print has the symmetric-power specialization and the sentence Le cas le plus important. It has neither divided powers nor the added flatness/separatedness qualifications. Restore the actual text in both layers; the supplied rewrite is not a proved correction.','structure')
    r(r'\pi',r'\mathcal N','six norm symbols','The printed norm letter is a script capital N.',count=6)
    r(r'\mathcal N^u_{X/S}(\mathcal F)',r'\mathcal N^u_{X/S}(F)','opening norm argument','The first F on this page is an ordinary capital; later F letters are script.')
    r(r'\underline{\operatorname{Quot}}',r'\mathop{\text{\uwave{Quot}}}\nolimits','quotient functor','The functor sign has a wavy underline.')
    r(r'\operatorname{Quot}',r'\underline{\operatorname{Quot}}','six representing Quot scheme signs','The scheme signs have straight underlines.',count=6)
    r(r'\operatorname{Hilb}',r'\underline{\operatorname{Hilb}}','two Hilbert scheme signs','Both Hilb signs have straight underlines.',count=2)
    r("sur $S'$ et de rang relatif","sur $S$ et de rang relatif",'flatness in the quotient-functor definition','The print omits the prime on S.')
    r(r'\mathcal F/X/S}$. (Lorsque',r'\mathcal F/X/S}$ (Lorsque','parenthetic existence explanation','There is no full stop before the opening parenthesis.')
    r(r'\longrightarrow',r'\to','two remaining displayed arrows','Both arrows are short.',count=2)
    r('$n>1$','$n\\geq1$','noninjectivity threshold','The print clearly has greater-than-or-equal, with a second stroke.')
    r(r'\mathfrak i','i','two primary-ideal signs','The printed ideal sign is ordinary lower-case i, not Gothic.',count=2)
    if tree=='fr':
        r('sur $S$ et de rang relatif',"sur $S'$ et de rang relatif",'flatness in the quotient-functor definition','A family over the test scheme S prime must be flat over S prime. For S=Spec Z, X=S, F=O and S prime=Spec F_p, the canonical rank-one quotient is flat over S prime but not over S; the printed condition would exclude this required point.','misprint of the original')
        r('$n\\geq1$','$n>1$','noninjectivity threshold','The preceding sentence already identifies the n=1 morphism as an isomorphism. The failure under discussion starts with n=2, as shown by the two distinct length-two ideals in CHECK_EVENTS.','misprint of the original')
    upright_page(rel,layer,'221-274')
event('221-6-norm-morphisms','targeted proof check','Given the base-change-compatible section construction of the preceding paragraph, evaluate it on the universal quotient to obtain the morphism from Quot^n to Y; naturality verifies the Yoneda correspondence. Taking the symmetric-quotient map as u gives the symmetric-power target, and F=O_X gives the Hilbert specialization. This checks the representability step conditional on the general norm construction, not a new proof of that construction. The printed quotient families must be flat over S prime, as the Spec Z to Spec F_p rank-one example shows.','221, p. 274, first two paragraphs and three displays')
event('221-6-length-threshold','targeted proof check','In the standing Hilbert setup, length zero gives the empty subscheme and length one gives a section, so the norm maps for n=0 and n=1 are isomorphisms. In A^2_k, the distinct ideals (x,y^2) and (x^2,y) both give length-two subschemes supported at the origin and the same cycle 2[0]. Thus the norm can fail to be injective already at n=2; the corrected threshold excludes the previously settled n=1 case.','221, p. 274, noninjectivity paragraph')
event('221-6(a)','targeted proof check','After an étale base change, a finite étale degree-n subscheme splits into n disjoint sections. Conversely an unordered set of n pairwise disjoint sections descends to that finite étale closed subscheme. Both functors are therefore the quotient of the ordered distinct-point configuration open by the free symmetric-group action, and the norm sends the subscheme to the sum of its sections. These constructions are inverse and descend, giving the stated isomorphism on the open loci.','221, p. 274, (a)')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-274')
record_page('221',274,'Compared printed French entry lines 1180-1226 and corrected French entry lines 1181-1227 with scan leaf 27 at 400 dpi and all three enlarged bands. Read the monoid specialization, the universal norm morphisms, the length-zero/one cases and noninjectivity discussion, and all of (a).\n\nRestored the original symmetric-power passage and its omitted sentence in place of the modern divided-power rewrite. Restored script N, the first ordinary F, the wavy quotient functor versus straight-underlined representing schemes, short arrows, ordinary ideal i, and punctuation. Printed French restores flatness over S and n greater than or equal to 1. Corrected French requires flatness over the test base S prime and excludes n=1 from the failure range. Checked the universal-family/Yoneda step, supplied explicit distinct length-two ideals with identical cycle, and checked (a) through the distinct-section configuration quotient.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
