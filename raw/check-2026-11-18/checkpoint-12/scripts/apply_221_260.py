from audit_utils import *
from collections import Counter
import csv
wq=r'\mathop{\text{\uwave{Quot}}}\nolimits'
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-260',line,'3.2 / open subfunctors A_nu',
                'Scan leaf 13 at 400 dpi and all three enlarged page bands: '+why,kind=kind,count=count)
    r(r'\underline{\operatorname{Quot}}',wq,'two Quot functor signs','Both functor signs carry wavy underlines; the representing scheme in 3.2 has no underline.',count=2)
    s,_,_=page_text(rel,260)
    m=re.search(r'(\\result\{THÉORÈME\}\{3\.2\} )(.*?)(?=\n\n)',s,re.S)
    r(m.group(2),underline_prose(m.group(2)),'Theorem 3.2','All statement prose is straight-underlined, including représentable; mathematical signs retain their own alphabets.')
    r(r"\mathcal S'_k f'_*(\mathcal K(\nu))",r"\mathcal S'_k f'_*(H(\nu))",'condition (c), right side','The right-hand sheaf letter is a plain capital H, unlike the script K on the left.')
    if tree=='fr':
        r(r"\mathcal S'_k f'_*(H(\nu))",r"\mathcal S'_k f'_*(\mathcal K(\nu))",'condition (c), right side','The kernel K is the only sheaf defined here. The condition is generation of its graded direct-image module from degree nu; the final formula on this page also uses K on both sides. H is undefined.','misprint of the original')
        r("plats sur $S'$, et satisfaisant","plats sur $S'$, de polynôme de Hilbert $P$, et satisfaisant",'definition of A_nu','The later asserted inclusion in Quot^P requires the missing polynomial restriction. For X=Spec(k), F=O and P=1, the zero quotient satisfies all three displayed conditions for nu=0 but is not in Quot^1. Restricting to polynomial P is the minimal repair.','misprint of the original')
    r(r"\mathcal S'_* =\mathcal S_*\otimes",r"\mathcal S' =\mathcal S\otimes",'graded algebra base change','The two stars are absent in the printed base-change identity. This is retained as shorthand for the graded algebra, not silently regularized.')
    r(r"homogène de $\mathcal S'_*$",r"homogène de $\mathcal S'$",'graded algebra sentence','The printed S-prime has no star subscript here.')
    r(r'\mathbf P',r'\mathfrak P','four projective spaces','All four printed projective-space letters are the looped Gothic P.',count=4)
    r(r'\mathcal O_{\mathfrak P^r_U}(1)',r'\mathcal O_{\mathfrak P^r_u}(1)','inducing invertible sheaf','The printed base subscript under this projective-space symbol is lowercase u.')
    if tree=='fr':
        r(r'\mathcal O_{\mathfrak P^r_u}(1)',r'\mathcal O_{\mathfrak P^r_U}(1)','inducing invertible sheaf','The open set just quantified is U; no lowercase u is defined. The inducing sheaf lives on projective space over U.','misprint of the original')
    r(r'\mathcal O_{\mathfrak P^r_S}^{N}',r'(\mathcal O_{\mathfrak P^r_S})^{N}','free sheaf','The scan places parentheses around the structure sheaf before the N exponent.')
    r("également plats sur $S'$","également plats $S'$",'kernel flatness','The print omits sur before the base.')
    if tree=='fr':
        r("également plats $S'$","également plats sur $S'$",'kernel flatness','The phrase requires plats sur S-prime (or S-prime-plats); restore the missing preposition.','misprint of the original')
    r('([5], III, \\S~7) que les conditions','([5], III, \\S~7), et de (b) que les conditions','Künneth citation','The scan visibly includes the inserted words et de (b) and a preceding comma.')
    r(r"de $f'_*(\mathcal K(n))$ commute",r"de $F'_*(\mathcal K(n))$ commute",'direct-image base change','The second direct-image letter is printed as capital F.')
    if tree=='fr':
        r(r"de $F'_*(\mathcal K(n))$ commute",r"de $f'_*(\mathcal K(n))$ commute",'direct-image base change','The structural morphism is f-prime. Capital F-prime is neither that morphism nor a defined direct-image functor.','misprint of the original')
    r('est un foncteur contravariant en','\\uline{est un foncteur contravariant en}','subfunctor paragraph','The whole phrase, including est un, is straight-underlined.')
    r('façon\nprécise un sous-foncteur de','\\uline{façon\nprécise un sous-foncteur de}','subfunctor paragraph','The underline starts at façon, after the unmarked de, and runs through sous-foncteur de.')
    r('de\nSerre [5]','de\nSERRE [5]','Serre citation','SERRE is printed in capitals.')
    r("plat sur $S'$, $s$ un élément de $S'$","plat sur $S$, $s$ un élément de $S$",'openness paragraph bases','Both bases in this phrase are printed without primes.')
    r(r"\operatorname{Spec}(k(s))\longrightarrow S'",r"\operatorname{Spec}(k(s))\to S",'residue-field point','The arrow is short and its target is printed without a prime.')
    if tree=='fr':
        r("plat sur $S$, $s$ un élément de $S$","plat sur $S'$, $s$ un élément de $S'$",'openness paragraph bases','G is a quotient on X-prime over S-prime. The point s, its neighborhood U, and f-prime inverse(U) must all refer to S-prime.','misprint of the original')
        r(r'\operatorname{Spec}(k(s))\to S',r"\operatorname{Spec}(k(s))\to S'",'residue-field point','The residue-field point is a point of the same base S-prime; the printed target loses its prime.','misprint of the original')
    r('changement de base $','changement de base, $','residue-field point','The scan has a comma after base.')
    r(r'$\mathcal G_s$ de $\mathcal F_s$',r'$G_s$ de $F_s$','fiber sheaves','The fiber letters here are ordinary typed G and F, unlike the surrounding script sheaf letters. Preserve the local typography.')
    r(r'A_\nu(\operatorname{Spec}(k(s)))',r'A_\nu\operatorname{Spec}(k(s))','fiber membership','The scan uses juxtaposition without outer argument parentheses; the Spec parentheses remain.')
    r('i.e.','i. e.','two explanatory abbreviations','The printed abbreviation separates i. and e.',count=2)
    r('« théorème des fonctions holomorphes »','"théorème des fonctions holomorphes"','openness citation','The scan uses plain double quotation marks.')
    s,_,_=page_text(rel,260)
    m=re.search(r'\\begin\{align\*\}.*?\\end\{align\*\}',s,re.S)
    assert m
    h=r'\mathcal K' if tree=='fr' else 'H'
    new=(r'\begin{align*}'+'\n'
         r'\text{a.}\quad &\symup{R^if^\prime_*(\mathcal G(n))=0} &&\text{pour $\symup{i>0}$ et $\symup{n\geq\nu}$}\\'+'\n'
         r'\text{b.}\quad &\symup{R^if^\prime_*(\mathcal K(n))=0} &&\text{pour $\symup{i>0}$ et $\symup{n\geq\nu}$}\\'+'\n'
         r'\text{c.}\quad &\symup{f^\prime_*(\mathcal K(\nu+k))=\mathcal S^\prime_k f^\prime_*('+h+r'(\nu))} &&\text{pour $\symup{k\geq0}$}.'+'\n'
         r'\end{align*}')
    r(m.group(0),new,'conditions (a)-(c), alignment','Typed letters are upright. The first two lines have no terminal commas; only (c) ends in a period. Prime notation is mechanically braced in the alignment without changing the printed single primes.','typesetting')
    upright_page(rel,layer,'221-260')
event('221-3.2','carried as background without fault found','Read projectivity and representability of the fixed-polynomial Quot functor. The existence proof starts here and continues on the next pages; no complete proof verdict is assigned yet.','221, p. 260, Theorem 3.2')
event('221-3-A_nu-polynomial-omission','refuted, with the refined statement id 221-3-A_nu-fixed-P','As written A_nu contains all flat coherent quotients satisfying (a)-(c), without a Hilbert-polynomial restriction. For X=Spec(k), F=O, P=1 and nu=0, the zero quotient satisfies (a)-(c) but has Hilbert polynomial 0, contradicting A_nu subset Quot^1. Corrected French adds the restriction to Hilbert polynomial P.','221, p. 260, definition of A_nu and subfunctor assertion')
event('221-3-A_nu-fixed-P','targeted proof check','After imposing the fixed polynomial P, (a),(b) express higher-cohomology vanishing and (c) generation of the graded kernel direct image from degree nu. The H on the right of (c) must be K; the final formula confirms the same module. Under the stated reduction F=O^N, K is base-flat by the exact sequence with flat quotient G. Vanishing and the cohomology/base-change assertion then preserve (c) under base change. The cited Kunneth/base-change theorem is used here, not independently re-proved.','221, p. 260, conditions and base-change paragraph')
event('221-3-A_nu-local-openness','carried as background without fault found','Read the Serre-vanishing exhaustion and fiberwise openness argument through the formula continued on p. 261. Checked that G, s, U and f-prime inverse(U) require base S-prime, and that the second direct image is f-prime-star. The full uniform finite-degree argument awaits its continuation; no independent proof is claimed.','221, p. 260, final paragraph')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-260')
record_page('221',260,'Compared printed French entry lines 533-583 and corrected French entry lines 534-584 with scan leaf 13 at 400 dpi and all three enlarged bands. Read the complete theorem, definition, three conditions, reduction to a free sheaf on projective space, base-change argument and the openness paragraph ending mid-sentence. Inspected all primes, star and degree subscripts, the plain H and capital direct-image F, Gothic projective-space letters, ordinary fiber letters, quotation marks and underline extents.\n\nRestored the printed shorthand without graded stars, parentheses around the free sheaf, the inserted et de (b), capital SERRE, ordinary G_s/F_s, short residue-field arrow and the juxtaposed functor argument. Corrected French repairs undefined H, lowercase u for U, missing sur, capital F-star for f-star, and the three missing base primes. Its A_nu definition now includes the polynomial P: the zero quotient over a point gives an explicit counterexample to the unqualified printed inclusion. The theorem is recorded as background; the local type and base-change checks and the counterexample have distinct events.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
