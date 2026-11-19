from audit_utils import *
from collections import Counter
import csv

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-254',line,'2.1 / 2.2 / dimension filtration',
                'Scan leaf 7 at 400 dpi and all three enlarged page bands: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,254)
    for a,b,body in list(footnotes(s)):
        r(s[a:b],'','Theorem 2.1 / filtration paragraph notes','Neither editorial footnote occurs in the print. The later erratum stays in its separate section; the filtration correction has its ledger justification.','structure')
    r('faut et il suffit qu\'il','faut qu\'il','Theorem 2.1 introductory condition','The print states necessity only. The supplied explicit incorporation of the later erratum is withdrawn in both layers under the requested separation of the historical exposé and its errata.','structure')
    r('Donc les faisceaux','Donc les faisceau','opening paragraph, line 3','The print has the singular faisceau after les.')
    r(r'\mathcal O(-n)^N',r'\mathcal O(-n)','opening paragraph, fibre quotient','The exponent N is absent in the printed fibre expression.')
    r(r'N_{r+1}/N_r',r'N_r/N_{r+1}','dimension-filtration paragraph','The printed numerator is N_r and denominator N_{r+1}.')
    r('ont comme cycles premiers','ont comme cycle premiers','dimension-filtration paragraph','The print has singular cycle before premiers associés.')
    r(r'\geq s-1',r'\leq s-1','Theorem 2.2, condition (b_s)','The inequality has its vertex pointing left: less than or equal to.')
    if tree=='fr':
        r('Donc les faisceau','Donc les faisceaux','opening paragraph, line 3','The plural article les and following induits/quotients require plural faisceaux.','misprint of the original')
        r(r'\mathcal O(-n)',r'\mathcal O(-n)^N','opening paragraph, fibre quotient','Pullback of the preceding surjection preserves its N summands. A single line bundle cannot surject onto a sheaf of generic rank two; the missing exponent N is necessary.','misprint of the original')
        r(r'N_r/N_{r+1}',r'N_{r+1}/N_r','dimension-filtration paragraph','N_r consists of sections supported in dimension less than r, so N_r is contained in N_{r+1}; the successive quotient must have the larger term in the numerator.','misprint of the original')
        r('ont comme cycle premiers','ont comme cycles premiers','dimension-filtration paragraph','The plural modifiers premiers associés and the ensuing exactly-the-cycles phrase require cycles.','misprint of the original')
        r(r'\leq s-1',r'\geq s-1','Theorem 2.2, condition (b_s)','For s=0 the printed condition bounds only negative-degree coefficients and is vacuous. On P^1, all O_Z for finite subschemes Z are quotients of fixed O_X, yet F_(0)=O_Z has unbounded constant Hilbert polynomial as length(Z) grows. Thus the printed version is false. Bounding coefficients in degrees at least s-1 controls the retained dimensional strata.','misprint of the original')
    r('« il faut »','"il faut"','paragraph before Theorem 2.1','The scan uses ordinary double quotation marks.')
    r('« il suffit »','"il suffit"','paragraph following Theorem 2.1','The scan uses ordinary double quotation marks.')
    r('dans $E$ sont éléments','dans $E$, sont éléments','Theorem 2.1, condition (b)','A comma follows E in the print.')
    r('dans $E$ ont des coefficients','dans $E$, ont des coefficients','Theorem 2.2, condition (b_s)','A comma follows E in the print.')
    s,_,_=page_text(rel,254)
    for head in [r'\result{THÉORÈME}{2.1} ',r'\noindent (a) ',r'\noindent (b) ',r'\result{THÉORÈME}{2.2} ',r'\noindent $(b_s)$ ']:
        m=re.search(re.escape(head)+r'(.*?)(?=\n\n)',s,re.S)
        assert m,head
        old=m.group(1)
        if head==r'\noindent (b) ':
            pieces=old.split('fini')
            assert len(pieces)==2
            new='fini'.join(underline_prose(x) for x in pieces)
        elif head==r'\noindent $(b_s)$ ':
            pieces=old.split('en degrés')
            assert len(pieces)==2
            new='en degrés'.join(underline_prose(x) for x in pieces)
        else:
            new=underline_prose(old)
            if head==r'\result{THÉORÈME}{2.2} ':
                new=new.replace('(2.1)',r'\uline{(2.1)}')
        r(old,new,'Theorem statement prose: '+head,'The prose is straight-underlined, with formulas excluded; fini in (b) and en degrés in (b_s) are visibly not underlined.')
    s,_,_=page_text(rel,254)
    m=re.search(r'(Sous ces conditions,.*?restent minorés\.)',s,re.S)
    assert m
    r(m.group(1),underline_prose(m.group(1)),'Theorem 2.2 conclusion','The conclusion prose is straight-underlined, excluding its formulas.')
    upright_page(rel,layer,'221-254')

event('221-2-fibre-quotient','refuted, with the refined statement\'s id','Printed fibre quotient by O(-n) is false for a coherent sheaf of rank two. Pullback is right exact and takes O_X(-n)^N to O(-n)^N. Corrected statement id: 221-2-fibre-quotient-corrected.','221, p. 254, opening paragraph')
event('221-2-dimension-filtration','targeted proof check','By definition every section with support dimension <r also has support dimension <r+1, so N_r is a submodule of N_{r+1}. The defined increasing filtration has successive quotient N_{r+1}/N_r. The reverse quotient in the print is not defined in general. This verifies the index reversal, not the full associated-prime assertion.','221, p. 254, paragraph between 2.1 and 2.2')
event('221-2.1','carried as background without fault found','Read the necessary quotient-family and finite-polynomial conditions. The print states only necessity; the explicit later-erratum strengthening in the supplied source is removed from the exposé in both layers. The following sentence still announces the sufficiency proof, as printed. No independent proof of the full boundedness theorem is claimed.','221, p. 254, Theorem 2.1 and following sentence')
event('221-2.2-printed','refuted, with the refined statement\'s id','Take s=0, X=P^1 over a field, L=O_X, and E={O_Z: Z a finite subscheme}. All negative-degree Hilbert coefficients vanish, so printed (b_s) is automatic; N_0=0, hence F_(0)=O_Z. Lengths are unbounded, contradicting boundedness because a bounded family has finitely many Hilbert polynomials. Corrected statement id: 221-2.2-corrected, with degrees >=s-1. This counterexample disproves the printed sign, without proving the full corrected theorem.','221, p. 254, Theorem 2.2 condition (b_s)')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-254')
record_page('221',254,'Compared both French 221.tex files, entry lines 239-295, with scan leaf 7 at 400 dpi and all three enlarged bands. Read the two opening paragraphs, all parts of Theorems 2.1 and 2.2, the complete dimension-filtration paragraph, and its displayed quotient. Checked every degree, subscript, exponent, relation sign, script letter and punctuation mark.\n\nRestored ordinary quotation marks, the commas after E, statement underlining and upright typed mathematics; fini and en degrés retain the scan\'s absence of underlining. Removed the two unprinted editorial footnotes. The later erratum\'s explicit addition of sufficiency to 2.1 is withdrawn in both layers, leaving its separate historical treatment for the errata reading. Printed faisceau, missing fibre exponent N, cycle, reversed filtration quotient and <= in (b_s) remain in fr_printed; fr has the five justified local repairs. The rank argument, filtration inclusion and unbounded-length counterexample are recorded as the targeted checks they actually establish.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
