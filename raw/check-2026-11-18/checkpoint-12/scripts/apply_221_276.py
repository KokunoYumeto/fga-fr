from audit_utils import *
from collections import Counter
import csv,re
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-276',line,'7, bibliography, additif',
                'Scan leaf 29 at 400 dpi, all three enlarged bands and the final group-letter detail: '+why,kind=kind,count=count)
    r(r'\Pi',r'\prod\limits','two section-scheme signs','The product signs have their base quotients underneath.',count=2)
    r(r'\section*{BIBLIOGRAPHIE}',r'\begin{center}BIBLIOGRAPHIE\end{center}','bibliography heading','The heading is centered, upright and of ordinary weight.')
    for i in range(1,9):
        r(r'\item[{['+str(i)+r']}]',r'\item[{\normalfont['+str(i)+r']}]',f'bibliography [{i}] label','The bracketed label is of ordinary weight.')
    s,_,_=page_text(rel,276)
    for i,m in enumerate(list(re.finditer(r'\\item.*?(?=\\item|\\end\{description\})',s,re.S)),1):
        old=m.group(0)
        for em in re.findall(r'\\emph\{([^{}]*)\}',old,re.S):
            r(r'\emph{'+em+'}',em,f'bibliography [{i}] title','The printed title and journal words are upright, not italic.')
    s,_,_=page_text(rel,276)
    r('--','-','bibliographic separators, title hyphen and page ranges','The typewritten punctuation uses short single hyphens.',count=s.count('--'))
    r('I, II, III, Séminaire','I., II., III., Séminaire','reference [2] parts','Each Roman part number has its printed full stop.')
    r('I, II, III, IV.','I., II., III., IV.','reference [3] parts','The first three Roman part numbers also end in full stops.')
    r('IV, V, Séminaire','IV., V., Séminaire','reference [4] parts','Both Roman part numbers end in full stops.')
    r('II, III, IV (à paraître)','II., III., IV. (à paraître)','reference [5] parts','All three Roman part numbers end in full stops.')
    r('Sc. U.S.A.','Sc. U. S. A.','reference [7] journal','Spaces separate the three national initials in the print.')
    r(r'\section*{ADDITIF}',r'\begin{center}ADDITIF\end{center}','addendum heading','The heading is centered in upright capitals of ordinary weight.')
    r(r'{\small [ajouté à la correction des épreuves]}','[ajouté à la correction des épreuves]','addendum subtitle','The bracketed subtitle uses the body type size.')
    r('$G$',r'$\mathfrak G$','last line','The enlarged handwritten group letter is Gothic capital G, with the curled top and separate lower bowl, not ordinary G.')
    r('\\par\\smallskip\n\\begingroup\\footnotesize\n\\endgroup','\\begin{center}\n  \\rule{.14\\linewidth}{.3pt}\n\\end{center}','closing rule','A short centered horizontal rule closes the exposé.','structure')
    upright_page(rel,layer,'221-276')
event('221-7-affine-section-scheme','carried as background without fault found','The existence and affineness of the section scheme for affine Z over projective flat X/S is retained. A full proof requires coherent linear-functor representability and closed equations imposing the algebra relations; those inputs are not proved afresh on this page. No stronger general-base conclusion is inserted.','221, p. 276, opening paragraph')
event('221-7-vector-section-scheme','targeted proof check','Checked the linear-algebra step conditional on a cohomology-and-base-change complex K beginning in degree zero: H^0 after arbitrary base change is ker(K^0 tensor A prime to K^1 tensor A prime), represented by Spec Sym(coker((K^1)^dual to (K^0)^dual)). This is a linear scheme over S. The print calls the input vector fibration locally trivial but does not repeat locally trivial for the output; a locally free conclusion would not follow when the kernel dimension jumps. That historical distinction is retained, with no unjustified constant-rank correction. Existence of the required proper-flat cohomology complex is a background input, not established here.','221, p. 276, opening paragraph, second assertion')
event('221-additif-quotient-conjectures','carried as background without fault found','The proof-stage addendum explicitly withdraws the existence and quasi-projectivity conjectures of [2], III, no. 8 even in characteristic zero and with closed action graph. The reference points to exposé 212 section 8. This page states the withdrawal without providing a counterexample; the announcement is faithfully retained and is not logged as an independently proved refutation.','221, p. 276, Additif')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-276')
record_page('221',276,'Compared printed French entry lines 1271-1331 and corrected French entry lines 1272-1332 with scan leaf 29 at 400 dpi, all three enlarged bands and a further enlargement of the last group letter. Read the continuation of section 7, every bibliographic name, title, date, locator and punctuation mark, and the complete proof-stage Additif.\n\nBoth layers restore product signs with lower limits, the ordinary centered headings and reference labels, upright titles and journals, short punctuation, the periods on the Roman part numbers, spaced U. S. A., body-sized addendum subtitle, Gothic G, and the closing rule. No mathematical divergence is introduced. In particular, the output fibré vectoriel is not silently strengthened to locally trivial: the conditional cohomology-complex check represents a linear scheme that need not have constant rank. The affine representability statement and the announced quotient counterexamples are recorded with their unproved inputs clearly identified.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
