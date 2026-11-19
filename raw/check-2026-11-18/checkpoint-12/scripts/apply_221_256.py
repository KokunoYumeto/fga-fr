from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-256',line,'2.5 proof',
                'Scan leaf 9 at 400 dpi and all three enlarged page bands: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,256)
    for a,b,body in list(footnotes(s)):
        r(s[a:b],'','last paragraph editorial note','No footnote occurs on the printed page.','structure')
    r('libre de rang $a=','libre de rang à $a=','last paragraph, first line','The print has an extra accented à between rang and the variable a.')
    r(r'\bigwedge^a\mathcal O_{\mathbf P^r_K}^{s}',r'\bigwedge^a\mathcal O_{\mathbf P^r_K}^{n}','last paragraph, exterior power','The free-module exponent is n in the print.')
    r(r'\binom{s}{a}',r'\binom{n}{a}','last line, number of canonical sections','The top entry in the printed binomial coefficient is n, not s.')
    if tree=='fr':
        r('libre de rang à $a=','libre de rang $a=','last paragraph, first line','The noun phrase is de rang a; the inserted preposition à is grammatically extraneous.','misprint of the original')
        r(r'\bigwedge^a\mathcal O_{\mathbf P^r_K}^{n}',r'\bigwedge^a\mathcal O_{\mathbf P^r_K}^{s}','last paragraph, exterior power','The fixed free sheaf surjecting onto F has rank s. Its a-th exterior power has rank binomial(s,a), so n (the polynomial variable) is an erroneous rank index.','misprint of the original')
        r(r'\binom{n}{a}',r'\binom{s}{a}','last line, number of canonical sections','The a-th exterior power of a free module with s basis vectors has the binomial(s,a) basis wedges indexed by a-element subsets; this is the number of canonical generating sections.','misprint of the original')
    r(r'faisceau sur $\mathbf P^r_K$',r'faisceau sur $P^r_K$','last paragraph, third printed line','This occurrence is a plain typed P, distinct from the handwritten projective-space letters elsewhere on the page.')
    s,_,_=page_text(rel,256)
    assert s.count(r'\mathbf P')==10
    r(r'\mathbf P',r'\mathfrak P','projective-space occurrences','These ten handwritten letters have the looped Gothic P form.',count=10)
    r(r'\longrightarrow',r'\to','exact sequence','All four printed arrows are short.',count=4)
    r('i.e. de supposer','i. e. de supposer','paragraph after coefficient inequality','The printed abbreviation has an intervening space.')
    r(r'\bigwedge^a',r'\mathop{\bigwedge}\limits^{a}','last paragraph, exterior powers','The degree a is directly above each exterior-power sign, including in running text.',count=3)
    upright_page(rel,layer,'221-256')
event('221-2.5-twist-coefficients','targeted proof check','For P(n)=a*n^r/r!+b*n^(r-1)/(r-1)!+lower terms, P(n-k) has second normalized coefficient b-k*a. Since k is fixed and 0<=a<=s, boundedness and lower boundedness of b are each equivalent before and after the twist. This verifies the stated reduction to the untwisted free sheaf.','221, p. 256, first paragraph and first two displays')
event('221-2.5-torsion-quotient','targeted proof check','Additivity in 0->N_r->F->F_(r)->0 gives b_F=b_F_(r)+b_Nr. The latter term is nonnegative because dim supp N_r<=r-1 and its leading Hilbert coefficient is positive when its dimension is exactly r-1, zero below that dimension. Thus the displayed inequality holds. Printed positif is retained in its nonnegative sense.','221, p. 256, exact sequence through coefficient inequality')
event('221-2.5-exterior-rank','targeted proof check','The source free module has rank s. The standard exterior basis e_i1 wedge ... wedge e_ia, with increasing a-tuples in {1,...,s}, has binomial(s,a) elements. This verifies both n-to-s repairs in the free-sheaf exponent and the section count.','221, p. 256, final two printed lines')
event('221-2.5-determinant-extension','carried as background without fault found','Read local freeness off codimension at least two, the invertible determinant on that open, extension over regular projective space and the O(d) description. These standard structural facts are carried as background; their proofs are not claimed here.','221, p. 256, final paragraph')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-256')
record_page('221',256,'Compared both French 221.tex files, entry lines 339-385, with scan leaf 9 at 400 dpi and all three enlarged bands. Read the complete proof continuation, all five displays and every inline formula, including the exact-sequence arrows, double subscripts, twisting sign, support-dimension inequality, exterior-power degrees and binomial coefficient.\n\nPreserved the printed mix of ten handwritten Gothic projective-space P letters and one ordinary typed P. Restored short arrows, above-sign exterior-power degrees, upright typed variables and the spacing in i. e.; removed the unprinted note. The printed layer restores the extra à in de rang à a and both occurrences of n in the exterior-power argument. The corrected layer removes the grammatical intrusion and retains s in both rank positions, with the exterior-basis count explicitly checked. The twist-coefficient calculation and the nonnegative Hilbert contribution of N_r were also checked; the determinant-extension facts are only background reading.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
