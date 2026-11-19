from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-257',line,'2.5 / 2.6',
                'Scan leaf 10 at 400 dpi and all three enlarged page bands: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,257)
    for a,b,body in list(footnotes(s)):
        r(s[a:b],'','Lemma 2.6 proof editorial note','There is no note in the print; the degree-to-dimension correction is justified in the ledger.','structure')
    r('réunion des composantes de dimension','réunion des composantes de degré','Lemma 2.6 proof opening','The printed word is degré.')
    if tree=='fr':
        r('réunion des composantes de degré','réunion des composantes de dimension','Lemma 2.6 proof opening','F_(r) is defined by removing sections of support dimension <r. Since its Hilbert polynomial has degree at most r here, the retained support components have dimension r; their projective degrees need not equal r.','misprint of the original')
        r(r'b_{\mathcal F}>0',r'b_{\mathcal F}\geq0','paragraph after the first display','The zero quotient sheaf is permitted and has a_F=b_F=d=0. The displayed formula with a_F,d nonnegative gives b_F>=0; strict positivity requires the nonzero torsion-free case. The non-strict inequality is the valid uniform conclusion.','misprint of the original')
    r(r'\mathcal O_{\mathbf P^r_K}(d)$ (puisque',r'\mathcal O_{\mathbf P^r_K}(d)$, (puisque','opening sentence','A comma precedes the parenthesis.')
    r('reste borné ; montrons','reste borné, montrons','paragraph after the first display','The scan has a comma, not a semicolon.')
    r("i.e. d'un homomorphisme","i. e. d'un homomorphisme",'section-map introduction','The two abbreviation letters are separated.')
    old="\\[\ns:\\bigwedge^a\\mathcal L_K\\longrightarrow\\mathcal O_{\\mathbf P^r_K}(d),\n\\]\npermet"
    new=r'$s:\bigwedge^a\mathcal L_K\longrightarrow\mathcal O_{\mathbf P^r_K}(d)$, permet'
    r(old,new,'section-map formula','The map s is in the running sentence, not a separate display.','structure')
    r(r'\operatorname{Hom}',r'\mathop{\text{\uwave{Hom}}}\nolimits','composite-map display','Both Hom symbols are wavy-underlined sheaf Hom.',count=2)
    r(r'\longrightarrow',r'\to','section map and composite display','All three arrows are short.',count=3)
    r(r'\bigwedge^{a-1}',r'\mathop{\bigwedge}\limits^{a-1}','composite display','The exterior degree a-1 is above the sign.',count=2)
    r(r'\bigwedge^a',r'\mathop{\bigwedge}\limits^{a}','section map and composite display','The exterior degree a is above the sign.',count=2)
    s,_,_=page_text(rel,257)
    assert s.count(r'\mathbf P')==7
    r(r'\mathbf P',r'\mathfrak P','projective-space letters','All seven projective-space letters have the handwritten Gothic form.',count=7)
    old="P_{\\mathcal F}(n)=a_{\\mathcal F}\\frac{n^r}{r!}\n+b_{\\mathcal F}\\frac{n^{r-1}}{(r-1)!}\n+\\text{termes de degré $<r-1$},"
    new=r'\symup{P_{\mathcal F}(n)=a_{\mathcal F}n^r/r!+b_{\mathcal F}n^{r-1}/(r-1)!}+\text{termes de degré $\symup{<r-1}$},'
    r(old,new,'Lemma 2.6 display','The print uses slash fractions and upright typed variables.')
    r(r'$\operatorname{supp}\mathcal F_{(r)}$, réunion',r'$\operatorname{supp}\mathcal F_{(r)}=$ réunion','Lemma 2.6 proof opening','An equals sign, not a comma, joins the support to its descriptive union.')
    s,_,_=page_text(rel,257)
    m=re.search(r'(\\result\{LEMME\}\{2\.6\} )(.*?)(?=\n\\\[)',s,re.S)
    assert m
    r(m.group(2),underline_prose(m.group(2)).replace('(2.1)',r'\uline{(2.1)}'),'Lemma 2.6 opening prose','The prose and the reference (2.1) are straight-underlined.')
    m=re.search(r'(et que les coefficients.*?sont limités\.)',s,re.S)
    assert m
    r(m.group(1),underline_prose(m.group(1)),'Lemma 2.6 conclusion','All conclusion prose is straight-underlined, excluding formulas.')
    upright_page(rel,layer,'221-257')
event('221-2.5-positive-coefficient','refuted, with the refined statement\'s id','The zero sheaf is a quotient of the fixed free sheaf and is torsion-free; its Hilbert polynomial vanishes, so b_F=0. Thus the unconditional strict >0 assertion is false. The displayed b=a(r+1)/2+d with a,d>=0 yields >=0, which is sufficient for the proof. Refined statement id: 221-2.5-nonnegative-coefficient. The nonzero torsion-free case still has strict positivity.','221, p. 257, sentence following the first display')
event('221-2.5-coimage','targeted proof check','For positive generic rank a, the map v |-> (w |-> s(v wedge w)) has, over the function field, exactly the kernel of L_K->F, by the nondegenerate determinant pairing on the rank-a quotient. The composite vanishes on that kernel globally. Conversely any additional kernel section has zero image in F generically and hence is zero in torsion-free F. Therefore its coimage is F. The zero sheaf can be omitted separately from the boundedness family.','221, p. 257, coimage construction and composite display')
event('221-2.6-dimension','targeted proof check','The Hilbert polynomial degree is at most r, so dim supp F<=r. The quotient F_(r) removes the submodule supported in dimensions below r. Its surviving irreducible support components therefore have dimension r, independently of their degrees. This verifies degré-to-dimension.','221, p. 257, proof opening after Lemma 2.6')
event('221-2.6','carried as background without fault found','Read the coefficient-boundedness statement, algebraic-closure reduction, reduced-support construction, degree bound and generic-length bound leading to the ideal J_F. The proof continues on the next page; no independent proof of the whole lemma is claimed here.','221, p. 257, Lemma 2.6 and proof fragment')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-257')
record_page('221',257,'Compared both French 221.tex files, entry lines 384-439, with scan leaf 10 at 400 dpi and all three enlarged bands. Read the end of Lemma 2.5 proof, the coefficient identity, the inline section map and displayed Hom composite, Lemma 2.6 with its full display, and the proof fragment through the ideal J_F. Checked all exponents, indices, relation signs, parentheses and both forms of underlining.\n\nRestored the inline map s, short arrows, above-sign exterior degrees, wavy sheaf Hom, Gothic projective-space letters, slash fractions, statement underlining, punctuation and the equals sign introducing the support union. The printed handwritten script J is retained. Removed the unprinted note. The printed degree r is retained only in fr_printed, while fr uses dimension r for the defined dimension filtration. The additional corrected-layer change >0 to >=0 accounts for the permitted zero sheaf; the counterexample and the positive-rank coimage argument are recorded explicitly.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
