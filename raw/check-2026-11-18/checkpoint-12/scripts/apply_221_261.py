from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-261',line,'3.3 / Grassmannian embedding',
                'Scan leaf 14 at 400 dpi and all three enlarged page bands: '+why,kind=kind,count=count)
    r('$k\\geq0$ (cf.','$k\\geq0$, (cf.','first line','The scan has a comma before the parenthetical citation.')
    r('ceci (comparer [4], IV).','ceci (comparer [4], IV,).','first representability criterion','A comma is printed after IV immediately before the closing parenthesis.')
    if tree=='fr':
        r('ceci (comparer [4], IV,).','ceci (comparer [4], IV).','first representability criterion','The extra comma closes no list item or clause and is immediately followed by the closing parenthesis; remove this duplicated citation punctuation.','misprint of the original')
    s,_,_=page_text(rel,261)
    m=re.search(r'(Pour que le foncteur.*?)(?=\n\n)',s,re.S)
    r(m.group(1),underline_prose(m.group(1)),'opening representability criterion','The prose of the entire criterion is straight-underlined, with the mathematical symbols unmarked.')
    r(r'\bigoplus',r'\sum','two graded-module definitions','Both displayed aggregate signs are plain capital summation sigmas, not circled pluses. Preserve the author notation for graded direct sums.',count=2)
    r(r"f'_*(\mathcal F'(n))",r"f'_*(\mathcal F(n))",'second display','The script F inside the primed direct image has no printed prime.')
    if tree=='fr':
        r(r"f'_*(\mathcal F(n))",r"f'_*(\mathcal F'(n))",'second display','The primed morphism has source X-prime, so this direct image must take the pullback F-prime. The adjacent tensor identity explicitly defines the base-changed module.','misprint of the original')
    r(r"de $M'_n$ pour",r"de $M_n$ pour",'kernel reconstruction','The ambient module here is printed without the prime.')
    if tree=='fr':
        r(r"de $M_n$ pour",r"de $M'_n$ pour",'kernel reconstruction','The kernel direct images are O_S-prime modules inside the base-changed M-prime_n, as established in (a-double-prime), not inside M_n on S.','misprint of the original')
    r('application injective','\\uline{application injective}','first Grassmannian map','These two words are straight-underlined.')
    r(r'\longrightarrow',r'\to','three Grassmannian arrows','All three arrows on the page are short.',count=3)
    r("de $M'_\\nu$, d'où","de $M'$, d'où",'rank-P(nu) quotient description','The printed M-prime has no degree subscript here.')
    if tree=='fr':
        r("de $M'$, d'où","de $M'_\\nu$, d'où",'rank-P(nu) quotient description','The just-displayed Grassmannian parametrizes quotients of degree-nu M-prime_nu. M-prime without a degree would be the entire graded module, not this finite locally free source.','misprint of the original')
    r('homomorphisme fonctoriel','homomorphisme \\uline{fonctoriel}','natural transformation','Only fonctoriel is straight-underlined.')
    r(r'\underline{\operatorname{Grass}}',r'\mathop{\text{\uwave{Grass}}}\nolimits','Grassmannian functor','The functor has a wavy underline; the three other Grass signs have none.')
    s,_,_=page_text(rel,261)
    m=re.search(r'(\\result\{LEMME\}\{3\.3\} )(.*?)(?=\n\n)',s,re.S)
    parts=m.group(2).split('ce qui implique que')
    assert len(parts)==2
    new='ce qui implique que'.join(underline_prose(x) for x in parts)
    r(m.group(2),new,'Lemma 3.3','The statement prose is straight-underlined except the parenthetical connecting words ce qui implique que.')
    r('IV) : supposons','IV) : Supposons','last paragraph','Supposons is printed with an initial capital.')
    upright_page(rel,layer,'221-261')
event('221-3-A_nu-open-cover','carried as background without fault found','Read the continuation of the finite-generation openness argument and the representability criterion by an increasing open cover Q_nu. The assertions rely on the cohomology and local representability results cited in [4] and [5]; no independent reconstruction of those cited theorems is claimed here.','221, p. 261, first paragraph')
event('221-3-Grassmannian-injection','targeted proof check','For a fixed-P member of A_nu, higher-cohomology vanishing gives rank P(n) for f-prime-star G(n); the exact sequence and R^1 f-prime-star K(n)=0 make it a quotient of M-prime_n. At n=nu the kernel determines all later graded kernel pieces by (c), and these recover the coherent kernel sheaf by sheafification. Thus the degree-nu quotient determines G and gives the asserted injection. This also identifies the missing F-prime, M-prime_n and M-prime_nu marks in the print.','221, p. 261, graded modules, (a-prime), (a-double-prime), and injection')
event('221-3.3','carried as background without fault found','Read representability of A_nu and the immersion into Grass_{P(nu)}(M_nu), hence quasi-projectivity. The proof is only introduced on this page and continues with the universal quotient criterion; no proof-complete verdict is assigned.','221, p. 261, Lemma 3.3 and final paragraph')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-261')
record_page('221',261,'Compared printed French entry lines 583-631 and corrected French entry lines 584-632 with scan leaf 14 at 400 dpi and all three enlarged bands. Read every paragraph, all four displays, (a-prime), (a-double-prime), Lemma 3.3 and its introductory universal-quotient paragraph. Checked the sum signs, stars, single and double primes, degree subscripts, P(nu), arrows, emphasis and citations.\n\nRestored sigma notation in both graded-module sums, wavy Grass functor notation, three short arrows, all straight emphasis spans, capital Supposons and printed citation punctuation. In corrected French retained the necessary F-prime and M-prime_n, supplied M-prime_nu at the quotient description, and removed the stray comma before a closing citation parenthesis. The degree-nu injection has a targeted exact-sequence and graded-reconstruction check. The existence of the locally closed representing scheme is only background here, pending the continuation.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
