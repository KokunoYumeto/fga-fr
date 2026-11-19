from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-262',line,'3.3 proof / 3.4',
                'Scan leaf 15 at 400 dpi, all three enlarged bands, and the focused point-letter crop: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,262)
    for a,b,body in list(footnotes(s)):
        r(s[a:b],'','graded-localization note','No footnote is printed here.','structure')
    r(r'\longrightarrow',r'\to','seven morphism arrows','The printed arrows are short.',count=7)
    r('i.e.','i. e.','change of notation','The abbreviation has a space between its two parts.')
    r("d'un élément de $A_\\nu(S)$","d'un élément de $A(s)$",'criterion introduction','The print has A(s), with lowercase s and no nu subscript.')
    if tree=='fr':
        r("d'un élément de $A(s)$","d'un élément de $A_\\nu(S)$",'criterion introduction','The criterion concerns the image of the degree-nu functor on the base S just fixed. A(s) is undefined and loses both the degree condition and the base.','misprint of the original')
    old="sous-Module gradué\n\\[\nR_* =\\sum_{k\\geq0}\\mathcal S_kR_\\nu\n\\]\nde $M_*$"
    new="sous-Module gradué\n$R_* =\\sum\\limits_{k\\geq0}\\mathcal S_kR_\\nu$\nde $M_*$"
    r(old,new,'condition (ii), graded kernel','The defining sum is inline, with its lower bound placed below the sigma.','structure')
    r(r'$\mathcal G=\mathcal F/\mathcal K$'+'\nsatisfont',r'$\mathcal G=\mathcal F/\mathcal K$,'+'\nsatisfont','condition (ii)','The print has a comma after the quotient formula.')
    r('plus haut.\n\nCes conditions','plus haut. Ces conditions','necessity paragraph','The explanation continues in the same printed paragraph.','structure')
    r('manifestement nécessaires ;','manifestement nécessaires,','necessity paragraph','The printed separator is a comma.')
    r(r'$M_{\nu+k}/\mathcal S_kR_\nu$, est plat',r'$M_{n+k}/\mathcal S_kR$, est plat','description of N-star','The scan has n+k in the numerator and no nu subscript on R in this occurrence.')
    if tree=='fr':
        r(r'$M_{n+k}/\mathcal S_kR$, est plat',r'$M_{\nu+k}/\mathcal S_kR_\nu$, est plat','description of N-star','The summands are the exact quotients from condition (i), indexed by k>=0 with fixed nu. Both the numerator degree and the fixed kernel piece must agree with that definition.','misprint of the original')
        r('localisés de $N_*$','localisés de $N$','homogeneous localization','The printed letter N has no star.')
        r('localisés de $N$','localisés de $N_*$','homogeneous localization','The localization used to form the associated sheaf is that of the graded S-star module N-star. The earlier N, now renamed N_nu, is only its degree-nu quotient and does not supply these homogeneous localizations. Retain the supplied repair with this type justification.','misprint of the original')
    r('est plat sur','est \\uline{plat} sur','flatness explanation','Only plat is straight-underlined.')
    r('homomorphisme surjectif de','homomorphisme \\uline{surjectif} de','same-rank comparison','Only surjectif is straight-underlined.')
    old="donc on a\n\\[\nf_*(\\mathcal K(\\nu+k))=\\mathcal S_kR_\\nu\n\\quad\\text{pour tout $k\\geq0$},\n\\]\nce qui"
    new="donc on a\n$f_*(\\mathcal K(\\nu+k))=\\mathcal S_kR_\\nu$ pour tout $k\\geq0$,\nce qui"
    r(old,new,'kernel equality','The equality and its quantifier are inline in the print.','structure')
    r(r'$s\in S$ tels',r'$e\in S$ tels','definition of U','The enlarged crop shows a closed bowl and horizontal middle stroke: a lowercase e, not s.')
    if tree=='fr':
        r(r'$e\in S$ tels',r'$s\in S$ tels','definition of U','The same clause uses the fiber X_s; the point being quantified is s. The printed e leaves s unbound.','misprint of the original')
    r(r'$M_*$ un $\mathcal S_*$-Module',r'$M_*$ un $\mathcal S$-Module','Lemma 3.4 algebra notation','The algebra letter in this module qualifier has no star in the print; retain the shorthand.')
    r(r'$\nu$ un entier. Alors',r'$\nu$ un entier, Alors','Lemma 3.4 punctuation','The scan has a comma before the capital Alors.')
    s,_,_=page_text(rel,262)
    m=re.search(r'(\\result\{LEMME\}\{3\.4\} )(.*?)(?=\n\n|$)',s,re.S)
    r(m.group(2),underline_prose(m.group(2)),'Lemma 3.4','All statement prose is straight-underlined, including the uniqueness parenthesis.')
    upright_page(rel,layer,'221-262')
event('221-3.3-criterion','targeted proof check','Condition (i) makes the graded quotient N-star a direct sum of base-flat locally free modules. Its homogeneous localizations remain base-flat, and the degree-zero stalks are direct summands, so the associated sheaf G is base-flat. Here the printed word fibres means stalks of the sheaf. The eventual graded ranks give Hilbert polynomial P. Under (ii), the natural surjection N_n -> f-star G(n) is between locally free modules of the same rank, hence is an isomorphism locally by an invertible determinant. The kernels then give condition (c). This checks the stated criterion and the necessary index/base repairs.','221, p. 262, conditions (i)-(ii) and verification')
event('221-3.3-Grassmannian-kernel-convention','targeted proof check','The print calls R_nu the Grassmannian element although the Grassmannian was described using quotient modules. This is retained: a quotient of the fixed M_nu is determined uniquely, up to the quotient equivalence used here, by its kernel R_nu. No mathematical correction is needed for this standard identification.','221, p. 262, end of criterion verification')
event('221-3.3-reduction-to-3.4','carried as background without fault found','Read the reduction of (i) to the locally closed rank locus of Lemma 3.4 and of (ii) to the stated cohomology-vanishing open set U. Conditional on the cited base-change results and Lemma 3.4, the intersection represents the desired subfunctor. The remaining rank-locus lemma is only begun here.','221, p. 262, second main paragraph')
event('221-3.4','carried as background without fault found','Read the hypotheses and uniqueness claim of the graded-module rank-locus lemma; its universal property continues on p. 263.','221, p. 262, Lemma 3.4 opening')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-262')
record_page('221',262,'Compared printed French entry lines 632-689 and corrected French entry lines 633-690 with scan leaf 15 at 400 dpi, all three enlarged bands and a 3x crop of the quantified point letter. Read the continuation of the universal criterion, (i)-(ii), the flatness and rank argument, the open-locus reduction and the beginning of 3.4. Inspected every graded degree, the N/N-star distinction, the A(s) reading, the plain printed e and the underline extents.\n\nRestored the two inline formulas, continuous paragraph after (ii), comma punctuation, seven short arrows, i. e., plain algebra shorthand and all emphasis. Corrected French repairs A(s) to A_nu(S), the summand indices to nu+k and R_nu, the localization module to N-star, and e to s. Removed the unprinted note. The printed use of R_nu for the Grassmannian quotient is retained under the kernel/quotient identification. The criterion has a targeted check; the remaining representability and rank-locus assertions are recorded at their actual provisional stage.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
