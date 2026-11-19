from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-255',line,'2.3 / 2.4 / 2.5',
                'Scan leaf 8 at 400 dpi, all three enlarged bands and focused glyph crops: '+why,kind=kind,count=count)
    old="du terme dominant de\n\\[\nP_{\\mathcal O_Y}=a\\frac{n^r}{r!}+\\cdots.\n\\]"
    new=r'du terme dominant de $P_{\mathcal O_Y}=an^r/r!+\ldots$.'
    r(old,new,'degree explanation following Lemma 2.4','The polynomial is in the running sentence, with a slash fraction and three baseline dots.','structure')
    old="P_{\\mathcal F}(n)=a_{\\mathcal F}\\frac{n^r}{r!}\n+b_{\\mathcal F}\\frac{n^{r-1}}{(r-1)!}\n+\\text{termes de degré $<r-1$}."
    new=r'\symup{F_{\mathcal F}(n)=a_{\mathcal F}n^r/r!+b_{\mathcal F}n^{r-1}/(r-1)!}+\text{termes de degré $\symup{<r-1}$}.'
    r(old,new,'Lemma 2.5 defining display','The printed first letter is F (two horizontal arms with no closed bowl), confirmed in the focused crop. Both fractions use slashes; the typed variables are upright.')
    if tree=='fr':
        r(r'F_{\mathcal F}(n)=a_',r'P_{\mathcal F}(n)=a_','Lemma 2.5 defining display','The polynomial being expanded is the Hilbert polynomial P_F defined on p. 253 and used throughout the surrounding argument. No scalar polynomial F_F has been introduced; F for P is a letter misprint.','misprint of the original')
    s,_,_=page_text(rel,255)
    for head in [r'\result{COROLLAIRE}{2.3} ',r'\result{LEMME 2.4 (CHOW)}{} ',r'\result{LEMME}{2.5} ']:
        if head==r'\result{LEMME}{2.5} ':
            m=re.search(re.escape(head)+r'(.*?)(?=\n\\\[)',s,re.S)
        else:
            m=re.search(re.escape(head)+r'(.*?)(?=\n\n)',s,re.S)
        assert m
        new=underline_prose(m.group(1)).replace('(2.1)',r'\uline{(2.1)}')
        r(m.group(1),new,'underlined statement '+head,'All statement prose is straight-underlined, excluding formulas; the reference (2.1) in Corollary 2.3 is also underlined.')
    s,_,_=page_text(rel,255)
    m=re.search(r'(Alors le coefficient.*?est limitée\.)',s,re.S)
    assert m
    r(m.group(1),underline_prose(m.group(1)),'Lemma 2.5 conclusion','The conclusion prose is straight-underlined.')
    r(r'\emph{Démonstration.} --',r'DÉMONSTRATION. -','proof heading','The scan has an ordinary uppercase heading followed by a short dash.')
    r('un morphisme fini\n','un morphisme \\uline{fini}\n','first proof paragraph','The adjective fini is underlined.')
    r(r'\longrightarrow',r'\to','first proof paragraph morphism','The arrow is short.')
    r(r'\mathbf P',r'\mathfrak P','first proof paragraph, projective spaces','The handwritten projective-space P has the looped Gothic form, not a bold typed P.',count=2)
    upright_page(rel,layer,'221-255')
event('221-2.3','carried as background without fault found','Read the associated-cycle dimension interval s<=d<=r and the restricted range s-1 through r of polynomial coefficients. No independent proof of the boundedness corollary is claimed.','221, p. 255, Corollary 2.3')
event('221-2.4','carried as background without fault found','Read Chow boundedness for reduced equidimensional subschemes of bounded degree over algebraically closed residue-field extensions, together with its Hilbert leading-term notation. Its dependence on Chow coordinates is carried as background.','221, p. 255, Lemma 2.4 and degree explanation')
event('221-2.5-polynomial','targeted proof check','Checked the identity of the polynomial being expanded: P_F was defined on p. 253 and appears in 2.1-2.3, whereas F_F is undefined. The focused crop confirms an F, so the corrected layer uses P and the printed layer preserves F. This checks the notation repair, not the lemma.','221, p. 255, Lemma 2.5 display')
event('221-2.5','carried as background without fault found','Read the coefficient bounds and boundedness conclusion, and the reduction by a finite morphism to projective r-space. Preserved all hypotheses and the direct-image identity; the finite-projection construction and equivalence of boundedness are not independently reproved here.','221, p. 255, Lemma 2.5 and proof opening')
event('221-2.5-finite-filtration','targeted proof check','For a finite morphism, a coherent module and its finite direct image have supports related by a finite map; dimensions of closed supports are preserved. Thus sections supported in dimension <r give the same submodule under finite direct image. Exactness of finite direct image then gives (f_*F)_(r)=f_*(F_(r)), as displayed.','221, p. 255, last displayed identity')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-255')
record_page('221',255,'Compared both French 221.tex files, entry lines 293-343, with scan leaf 8 at 400 dpi, the three enlarged bands and focused threefold crops of the leading polynomial letter and handwritten projective-space letter. Read Corollary 2.3, Lemmas 2.4 and 2.5, the intervening explanations and the first proof paragraph. Checked all dimension bounds, coefficient indices, factorials, direct-image stars and parentheses.\n\nRestored statement underlining, the inline degree polynomial, slash fractions, baseline ellipsis, ordinary uppercase proof heading, short arrow and the Gothic handwritten projective-space letters. The focused crop unambiguously shows F rather than P at the start of the Lemma 2.5 expansion; fr_printed preserves it and fr repairs it to the defined Hilbert-polynomial symbol P. The last filtration identity was checked using preservation of support dimension and exactness under finite direct image; the rest of the boundedness assertions are recorded as background reading.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
