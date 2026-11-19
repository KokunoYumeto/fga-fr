from audit_utils import *
from collections import Counter
import csv
wq=r'\mathop{\text{\uwave{Quot}}}\nolimits'
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-259',line,'3.1 / Quot functor and polynomial strata',
                'Scan leaf 12 at 400 dpi and all three enlarged page bands: '+why,kind=kind,count=count)
    if r'\uline{Sous ces conditions' not in page_text(rel,259)[0]:
        s,_,_=page_text(rel,259)
        for a,b,body in list(footnotes(s)):
            r(s[a:b],'','base-change paragraph editorial note','The print has no footnote.','structure')
        if tree=='fr':
            r('transforme les Modules','transforme Modules','base-change paragraph','The print omits the article les.')
            r('transforme Modules','transforme les Modules','base-change paragraph','French transforme les Modules S-prime-plats en Modules S-double-prime-plats requires the article before the specified source class; the supplied grammatical repair is retained.','misprint of the original')
        r('formée des quotients cohérents','formé des quotients cohérents','polynomial-stratum definition','The printed participle is formé without the final e.')
        r('est égal à $P$','est égal à $\\mathcal F$','polynomial-stratum definition','The printed target is the same script F glyph as the sheaf, not the ordinary P.')
        if tree=='fr':
            r('formé des quotients cohérents','formée des quotients cohérents','polynomial-stratum definition','The participle agrees with the feminine noun partie.','misprint of the original')
            r('est égal à $\\mathcal F$','est égal à $P$','polynomial-stratum definition','The condition fixes the Hilbert polynomial to the rational polynomial P(n) just quantified. The sheaf F is not a polynomial and cannot be the target of this equality.','misprint of the original')
        r("$S''$-plats","$S''$-Plats",'base-change paragraph','The second Plats begins with a capital P in the print.')
        r('au-dessus de','au dessus de','contravariance explanation','The print has no hyphen between au and dessus.')
        old="image inverse\n\\[\n\\mathcal G'\\longmapsto\n\\mathcal G'\\otimes_{\\mathcal O_{S'}}\\mathcal O_{S''}\n\\]\nde la catégorie"
        new="image inverse\n$\\mathcal G'\\rightsquigarrow\\mathcal G'\\otimes_{\\mathcal O_{S'}}\\mathcal O_{S''}$\nde la catégorie"
        r(old,new,'inverse-image functor formula','The object assignment is inline and uses a wavy arrow without a mapsto bar.','structure')
        r(r'\longrightarrow',r'\to','base-change morphism and induced Quot map','The two printed arrows are short.',count=2)
        r(r'\underline{\operatorname{Quot}}',wq,'Quot functor symbols','The eight supplied underlined functor signs have a wavy underline.',count=8)
        r('un foncteur\ncontravariant en','un \\uline{foncteur\ncontravariant en}','contravariance explanation','The words foncteur contravariant en are straight-underlined.')
        r('est projectif sur','est \\uline{projectif} sur','standing hypotheses','The word projectif is straight-underlined.')
        r('noethérien,','\\uline{noethérien},','standing hypotheses','The word noethérien is straight-underlined.')
        r('cohérent, et nous','\\uline{cohérent}, et nous','standing hypotheses','The word cohérent is straight-underlined.')
        s,_,_=page_text(rel,259)
        m=re.search(r'(\\result\{THÉORÈME\}\{3\.1\} )(.*?)(?=\n\n)',s,re.S)
        assert m
        parts=m.group(2).split('représentable')
        assert len(parts)==2
        new='représentable'.join(underline_prose(x) for x in parts)
        new=new.replace(r'\operatorname{Quot}_{',r'\underline{\operatorname{Quot}}_{')
        r(m.group(2),new,'Theorem 3.1','The prose is straight-underlined except représentable. The two scheme-name Quot words carry straight emphasis underlines; the functor sign remains wavy.')
        r('implique ceci : pour que','implique ceci : Pour que','final representability criterion','The initial Pour is capitalized.')
        r(r'$S$-préschéma $\operatorname{Quot}_{\mathcal F/X/S}$ qui le représente est',
          r'$S$-préschéma $'+wq+r'_{\mathcal F/X/S}$, qui le représente, est',
          'final representability criterion, representing scheme','The printed scheme symbol is also wavy-underlined here, and the relative clause is set off by two commas. Preserve this local notation rather than silently regularizing it.')
        r(r'$\operatorname{Quot}^P_{\mathcal F/X/S}$ qui représentent',
          r'$'+wq+r'^P_{\mathcal F/X/S}$ qui représentent',
          'final representability criterion, summands','The printed summand symbols are wavy-underlined even though they name the representing schemes. This local identification is preserved.')
    s,_,_=page_text(rel,259)
    m=re.search(r'(Pour que\s+.*?)(?= Ceci posé,)',s,re.S)
    assert m
    r(m.group(1),underline_prose(m.group(1)),'final representability criterion','The entire criterion prose is straight-underlined; the subsequent Ceci posé sentence is not.')
    s,_,_=page_text(rel,259)
    m=re.search(r'\\\[\n(.*?)\n\\\]',s,re.S)
    assert m and r'\qquad\text' in m.group(1)
    left=m.group(1).split(r'\qquad')[0].rstrip()
    new='\\[\n\\symup{'+left+"}\n\\qquad\\text{(où $\\symup{X'=X\\times_SS'}$)}.\n\\]"
    r(m.group(0),new,'first defining display','The typed variables in the main expression and parenthetical base-change identity are upright.')
    upright_page(rel,layer,'221-259')
event('221-3-Quot-base-change','targeted proof check','Right exactness of tensor product carries a quotient of F-prime to a quotient of its base change. Flatness over S-prime is preserved under base change to S-double-prime. The canonical tensor associativity identifications give the contravariant set-valued Quot functor. This checks the stated construction, not representability.','221, p. 259, first two paragraphs')
event('221-3.1','carried as background without fault found','Read representability on locally noetherian S-preschemes under projectivity of X over noetherian S and coherence of F, with a countable disjoint sum of projective S-schemes. The existence proof is not yet read.','221, p. 259, Theorem 3.1')
event('221-3-fixed-Hilbert-polynomial','targeted proof check','The paragraph quantifies a rational polynomial P(n) and defines the P-stratum. Its Hilbert polynomial must equal P. The scan instead has script F, the ambient sheaf. This is a type-inconsistent substitution, repaired to P only in corrected French.','221, p. 259, definition of Quot^P')
event('221-3-polynomial-decomposition','targeted proof check','Assuming the recalled local constancy of Hilbert polynomials in flat projective families, each base splits into open-and-closed polynomial loci. If the full functor is represented, its universal family supplies representing open-and-closed P-loci. Conversely the coproduct of representing P-schemes represents these locally constant decompositions. This verifies the reduction to the next theorem; it does not prove the projectivity assertion. The printed reuse of wavy symbols for representing schemes is preserved as a representable-functor identification.','221, p. 259, final paragraph')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-259')
record_page('221',259,'Compared printed French entry lines 478-535 and corrected French entry lines 479-536 with scan leaf 12 at 400 dpi and all three enlarged bands. Read the complete functor construction, all three displayed equalities/maps, Theorem 3.1, the polynomial-stratum definition and representability reduction. Checked the single and double primes, tensor bases, P superscripts, script sheaf letters and the distinction between straight and wavy underlines.\n\nRestored the inline object assignment with wavy arrow, short morphism arrows, standing-hypothesis and statement emphasis, printed capital Plats, unhyphenated au dessus, initial Pour and relative-clause commas. The word représentable in 3.1 is not underlined in the print. Scheme names have straight emphasis underlines within 3.1 but wavy underlines in the last paragraph; that local reuse is preserved in both layers. Corrected French retains the justified missing article and feminine participle, and repairs the printed sheaf F in the polynomial equality to P. Removed its unprinted note. The construction and coproduct reduction have separate targeted checks; the existence theorem is only read as background at this point.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
