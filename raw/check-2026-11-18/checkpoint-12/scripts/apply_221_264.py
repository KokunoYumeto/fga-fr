from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-264',line,'3.4, 3.6 proofs / 3.7',
                'Scan leaf 17 at 400 dpi, all three enlarged bands and a 3x stable-index crop: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,264)
    for a,b,body in list(footnotes(s)):
        r(s[a:b],'','ambient-scheme note','The print has no footnote.','structure')
    r(r'\longrightarrow',r'\to','seven presentation arrows','Every arrow in the two exact sequences and the final presentation map is short.',count=7)
    r('i.e.','i. e.','matrix proof','The printed abbreviation has a space between its parts.')
    r('le sous-schéma fermé de','le sous-schéma \\uline{fermé} de','definition of Z_n','Only fermé is straight-underlined.')
    r("Alors les $Z'_N$","Alors les $Z_N$",'descending intersection sequence','The print drops the prime in this occurrence.')
    r("constante des $Z'_N$","constante des $Z_W$",'stationary value','The enlarged crop clearly shows a W subscript and no prime. The following heavily overinked parameter is retained as N, provisionally for the final row review.')
    if tree=='fr':
        r("Alors les $Z_N$","Alors les $Z'_N$",'descending intersection sequence','The sequence being considered is the sequence of finite intersections Z-prime_N, just defined, rather than the individual rank loci Z_n.','misprint of the original')
        r("constante des $Z_W$","constante des $Z'_N$",'stationary value','W is undefined. The eventual constant subscheme is the stabilized value of the finite intersections Z-prime_N.','misprint of the original')
        r('sous-schémas fermés de $S$','sous-schémas fermés de $Z$','ambient scheme of the sequence','The print has Z here.')
        r('sous-schémas fermés de $Z$','sous-schémas fermés de $S$','ambient scheme of the sequence','The Z_n and their intersections are closed in the noetherian base S; the target Z is only defined as the eventual value in the next sentence. Retain the supplied ambient-base correction.','misprint of the original')
    r(r'\underline{\operatorname{Quot}}',r'\mathop{\text{\uwave{Quot}}}\nolimits','Quot functor','The underline is wavy.')
    s,_,_=page_text(rel,264)
    m=re.search(r'(est représentable par un.*?)(?= Pour aller plus loin,)',s,re.S)
    r(m.group(1),underline_prose(m.group(1)),'representability conclusion','The prose from est représentable through quasi-projectifs sur is straight-underlined; the introductory On a donc prouvé que is not.')
    r('est quasi-compact (car','est \\uline{quasi-compact}, (car','boundedness paragraph','The word quasi-compact is underlined and followed by a comma before the parenthesis.')
    r('est propre sur','est \\uline{propre} sur','properness reduction','Only propre is underlined.')
    s,_,_=page_text(rel,264)
    m=re.search(r'(\\result\{LEMME\}\{3\.7\} )(.*?)(?=\n\n|$)',s,re.S)
    r(m.group(2),underline_prose(m.group(2)),'Lemma 3.7','All statement prose is straight-underlined; the script sheaves and fiber subscripts remain distinct.')
    upright_page(rel,layer,'221-264')
event('221-3.6','targeted proof check','On the open locus of fiber rank at most r, Nakayama gives locally a presentation O^q -> O^r -> M -> 0. After any base change, M becomes locally free of rank r exactly when the surjection from O^r is an isomorphism, equivalently the presentation matrix vanishes. Its coefficients define the closed locus, and the universal property glues these local closed loci inside that open set. Under the global rank bound the locus is closed in S. Negative r gives the empty locus. The printed (*) is read here as the corresponding single-module rank bound of 3.6.','221, p. 264, first paragraph')
event('221-3.4','targeted proof check','After the rank-upper-bound open restriction, each degree rank locus Z_n is closed by 3.6. Finite intersections Z-prime_N correspond to increasing sums of ideal sheaves; noetherianity makes this chain stationary, so one closed subscheme imposes every degree condition. This checks the construction and identifies the necessary ambient S and Z-prime_N notation in the print. It uses the refined stationarity argument recorded for 3.5.','221, p. 264, second paragraph')
event('221-3.3','used and rechecked in this run','Combining the verified quotient criterion on p. 262, the just-checked graded rank locus and the cohomology-vanishing open locus yields the claimed immersion into the Grassmannian. The cohomology/base-change assertions and finite flat stratification remain cited background inputs, explicitly not independent re-proofs.','221, p. 264, end of second paragraph')
event('221-3.2-quasi-compactness','carried as background without fault found','Read the passage from an increasing union of quasi-projective opens to quasi-compactness via a finite-type parameter space, then to a single Q_nu and the valuative properness criterion [5], II, 7.3.8. The invocation of 2.1 uses its sufficient boundedness direction, which is absent from its printed statement and is assigned to the separate erratum; 2.2 at s=0 also supplies the needed boundedness for a fixed Hilbert polynomial. Parameterizing quotient maps from a bounded sheaf family uses the earlier Hom/quotient construction. No complete re-proof of these cited inputs is claimed.','221, p. 264, third paragraph')
event('221-3.7','carried as background without fault found','Read existence and uniqueness of a quasi-coherent base-flat quotient extending a generic-fiber quotient over a discrete valuation ring. No properness hypothesis on X is part of this extension lemma. Its proof follows on p. 265.','221, p. 264, Lemma 3.7')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-264')
record_page('221',264,'Compared printed French entry lines 729-770 and corrected French entry lines 730-771 with scan leaf 17 at 400 dpi and all three enlarged bands. A 3x crop confirms the printed W in the stationary-value subscript; the heavily overinked following N remains a provisional glyph reading for final review. Read the presentation-matrix proof of 3.6, the noetherian-intersection proof of 3.4, the boundedness/properness reduction and all of 3.7.\n\nRestored seven short arrows, i. e., the printed Z_N and Z_W variants, the wavy Quot sign, all emphasis and the comma before the boundedness parenthesis. Corrected French identifies both sequence occurrences as Z-prime_N and retains S for the ambient noetherian base; removed its unprinted note. The matrix and ideal-chain arguments have targeted checks. The dependence on the sufficient boundedness direction of 2.1 is explicitly recorded without merging the erratum into the exposé. Lemma 3.7 is only read as background until its proof.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
