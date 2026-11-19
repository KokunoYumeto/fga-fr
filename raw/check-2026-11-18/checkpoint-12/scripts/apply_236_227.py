from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'236-227',line,'1.1, 1.5',
                'Scan leaf 8 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,227)
    for a,b,body in list(footnotes(s)):
        r(s[a:b],'','two edition footnotes','Neither explanatory footnote is present in the print; its mathematical justification belongs in the audit records.','structure')
    r(r"g_2=g^{bm},\qquad\text{d'où}",r"g_2=g^{bm}\qquad\text{d'où}",'first display','There is no comma between the second assignment and d’où.')
    r('donc, par construction','donc par construction','paragraph following first display','The print has no comma after donc.')
    r('$G^\\circ$ est fermé, il', '$G^\\circ$ est fermé il','specialization step','There is no comma after fermé.')
    r("Or, de l'hypothèse et du fait", "Or de l'hypothèse, et du fait",'quasi-section paragraph','The comma is after hypothèse, not after Or.')
    r('« quasi-section »',chr(96)*2+"quasi-section''",'quasi-section paragraph','The printed quotation marks are ordinary double quotes.')
    r("construction, $g'(y)=g(y)=x$, et\n\\[\ng'(y')=g_1(y')g'_2(y')\\in G^\\sigma,\n\\]\ndonc", "construction, $g'(y)=g(y)=x$, et\n$g'(y')=g_1(y')g'_2(y')\\in G^\\sigma$, donc",'conclusion of iii','The generic-fibre product is printed inline, not displayed.','structure')
    r("donc $g'(y')=x'$","donc $g(y')=x'$",'conclusion of iii','The print omits the prime on this occurrence of g.')
    r(r'\varphi_{p^h}',r'\varphi_{n^h}','reduction in iv','The subscript is printed n to the power h.')
    r(r'\longrightarrow',r'\to ','two arrows','Both arrows are short.',count=2)
    r("soit universellement ouvert\n(par exemple étale), posons\n\\[\nG^{(n)}=\\varphi_n^{-1}(G^\\circ),\n\\]\net supposons que, dans chaque fibre géométrique $G_{\\bar s}$, le sous-ensemble",
      "soit universellement ouvert,\n(par exemple étale) posons\n$G^{(n)}=\\varphi_n^{-1}(G^\\circ)$, et supposons que les fibres connexes $G_s^\\circ$ ne "+chr(96)*2+"contiennent pas de",
      'opening of corollary 1.5','The definition is inline. The print has the comma before the parenthesis, none after it, then the connected fibres G_s zero and an opening ordinary quote before contiennent pas de. The edition had rewritten this unfinished hypothesis.','structure')
    if tree=='fr':
        r("donc $g(y')=x'$","donc $g'(y')=x'$",'conclusion of iii','The constructed section is g prime=g_1 g_2 prime. Its generic value was just shown to lie in G sigma; the original g can retain a nonzero p-primary component. The conclusion must use g prime, confirming the existing edition correction.','misprint of the original')
        r(r'\varphi_{n^h}',r'\varphi_{p^h}','reduction in iv','A p-primary component class is killed by a suitable power of p, the characteristic exponent; no n has yet been fixed and prime-to-p powers would not kill a nontrivial p-primary class. This confirms the existing edition correction.','misprint of the original')
    upright_page(rel,layer,'236-227')
event('236-1.1-sigma-bezout','targeted proof check','The displayed Bezout identity splits the section into g_1 of component order prime to p and g_2 of p-primary component order at the generic point. Closedness of the two loci in this equal-positive-characteristic case preserves their membership at the special point. Since g(y) and g_1(y) lie in G sigma, g_2(y) lies in both loci, hence in G zero. Conditional on the stated existence of a replacement section g_2 prime in G zero, the product g prime=g_1 g_2 prime has the required special value and generic sigma membership. The last g must therefore be primed.','236, p. 227, first three displays and conclusion of iii')
event('236-1.1-sigma-quasisection','carried as background without fault found','The passage from openness of G minus (G_y minus G_y zero) to a quasi-section through the chosen point and then a section g_2 prime of G zero is read, but not counted as proved here. A complete proof must justify that the replacement section can be chosen in the identity-component locus after base extension, not merely in the displayed ambient open. No textual change is made without a verified counterexample or a justified replacement argument.','236, p. 227, quasi-section paragraph')
event('236-1.1-rho-open','targeted proof check','After applying a suitable p-power, reduce the special point to G zero; using n^h would not give this reduction. Prime-to-p power maps are surjective on the connected finite-type group and open by hypothesis. Thus every generization is in phi_n(U) for a quasi-compact open U containing the special identity component. The order function has finitely many values on U by 1.4 and Noetherian induction, so choose n divisible by all their prime-to-p parts. Every component class in phi_n(U) then has p-power order, proving the required membership. Surjectivity of multiplication prime to p on the connected group and the relevant generic-point reductions are standard background inputs.','236, p. 227, proof of iv')
event('236-1.5-opening','carried as background without fault found','The corollary starts here with n greater than 1, universal openness of phi_n and the definition of G^(n). Restored the literal unfinished hypothesis about the connected fibres G_s zero; its completion is on the following printed page and is not anticipated in this page record.','236, p. 227, corollary 1.5 opening')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='236-227')
record_page('236',227,'Compared sources/fr_printed/fr/236.tex and sources/fr/fr/236.tex, entry lines 282-337, with scan leaf 8 at 400 dpi, full page and three enlarged bands. Read the Bezout splitting, every displayed and inline membership, the quasi-section passage, conclusion of (iii), proof of (iv), and the start of 1.5.\n\nRestored exact commas, ordinary quotes, inline placement of the product and corollary definition, the literal connected-fibre hypothesis, and printed g without prime and n^h; removed two unprinted footnotes. Corrected French confirms the two existing mathematical repairs, g prime and p^h. Checked the splitting and the bounded-order power argument. The step selecting a quasi-section inside G zero remains a clearly identified background requirement, not a proved assertion in this audit. Corollary 1.5 continues on the next page.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
