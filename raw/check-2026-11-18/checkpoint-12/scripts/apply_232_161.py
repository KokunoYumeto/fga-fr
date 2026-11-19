from audit_utils import *
from collections import Counter
import csv,re
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/232.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'232-161',line,'6.8, bibliography',
                'Scan leaf 20 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    r('« désingulariser »',"``désingulariser''",'opening paragraph','The word has ordinary double quotation marks.')
    r(r'\section*{BIBLIOGRAPHIE}',r'\begin{center}BIBLIOGRAPHIE\end{center}','bibliography heading','The uppercase heading is centered and of ordinary weight.')
    for i in range(1,13):
        r(r'\item[{['+str(i)+r']}]',r'\item[{\normalfont['+str(i)+r']}]',f'bibliography [{i}] label','The bracketed reference number has ordinary weight.')
    s,_,_=page_text(rel,161)
    for em in dict.fromkeys(re.findall(r'\\emph\{([^{}]*)\}',s,re.S)):
        r(r'\emph{'+em+'}',em,'bibliographic titles and journals','The words are upright in the print.',count=s.count(r'\emph{'+em+'}'))
    s,_,_=page_text(rel,161)
    r('--','-','bibliographic separators and ranges','The print uses short hyphens.',count=s.count('--'))
    r('Hautes Études','Hautes Etudes','references [2] and [9]','There is no accent on the capital E in either occurrence.',count=2)
    r('Etudes Scientifiques,\nPublications mathématiques, 9','Etudes Scientifiques.\nPublications mathématiques, 9','reference [9] imprint','The separator after Scientifiques is a full stop, unlike the comma in reference [2].')
    r('\\par\\smallskip\n\\begingroup\\footnotesize\n\\endgroup','\\begin{center}\n  \\rule{.20\\linewidth}{.3pt}\n\\end{center}','closing rule','The exposé ends with a centered short horizontal rule.','structure')
    upright_page(rel,layer,'232-161')
event('232-6.8-local-class-group','carried as background without fault found','Read the completed announcement: the divisor class group of a complete normal two-dimensional equicharacteristic local ring A is to be realized as the k-rational points of an algebraic group G over its residue field k, with the canonical structure qualified by a chosen coefficient field. The higher-dimensional pro-algebraic analogue is explicitly plausible, and the proposed inverse-limit construction is conditional on desingularization. Establishing these claims requires formal Picard representability, comparison with the resolved punctured spectrum, control of exceptional divisor classes and a stabilization argument in dimension two. Those results are not proved here; the announcement and its qualifications are retained without strengthening.','232, pp. 160-161, remarque 6.8, final paragraph')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='232-161')
record_page('232',161,'Compared both French layers, entry lines 887-949, with scan leaf 20 at 400 dpi, the full page and all three enlarged bands. Read the end of remark 6.8 and all twelve bibliography entries, including every name, title, year, volume, page count, range and punctuation mark.\n\nRestored the ordinary quotation marks, upright mathematical letters, centered ordinary-weight heading and reference labels, upright titles and journals, short separators and ranges, the unaccented Etudes in both imprints, the printed full stop in reference [9], and the closing rule. No mathematical difference between the two French layers is introduced. The coefficient-field qualification and the explicitly conjectural higher-dimensional extension are preserved; their proof requirements are recorded as background.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
