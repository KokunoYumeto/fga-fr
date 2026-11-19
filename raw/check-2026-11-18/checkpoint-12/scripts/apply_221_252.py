from audit_utils import *
import csv
from collections import Counter

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-252',line,'1.2',
                'Scan leaf 5 at 400 dpi, full image and all enlarged bands: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,252)
    for a,b,body in list(footnotes(s)):
        r(s[a:b],'','universal extension / footnote','No footnote is printed; the reason for swapping the endpoint terms remains in the ledger.','structure')
    r(r'\operatorname{Tor}_i',r'\mathop{\text{\uwave{Tor}}}\nolimits_i','opening paragraph, line 2','The local Tor operator is wavy-underlined.')
    r('N. B. -- Ici','N. B. - Ici','opening paragraph, parenthesis','The note abbreviation is followed by one short dash.')
    s,_,_=page_text(rel,252)
    for pat,loc in [
        (r'(\\result\{PROPOSITION\}\{1\.2\} )(.*?)(\n\n)','proposition introductory sentence'),
        (r'(\\noindent \(i\) )(.*?)(\n\n)','proposition part (i)'),
        (r'(\\noindent \(ii\) )(.*?)(\n\n)','proposition part (ii)')]:
        m=re.search(pat,s,re.S)
        assert m,loc
        r(m.group(2),underline_prose(m.group(2)),loc,'The assertion prose is straight-underlined, with mathematical letters excluded.')
    r(r'f_{T*}(',r'f_T(','proof, direct image','The print has f_T with no star. Its action on the indicated sheaf is the direct-image shorthand in this sentence; the supplied extra star is withdrawn rather than treated as a necessary emendation.')
    r(r'\operatorname{Hom}_{X_T}',r'\mathop{\text{\uwave{Hom}}}\nolimits_{O_{X_T}}','proof, Hom subscript','The internal Hom is wavy-underlined and its ring subscript is ordinary O with lower X_T.')
    r(r'\operatorname{Ext}^{1}_{f_T}',r'\mathop{\text{\uwave{Ext}}}\nolimits^{1}_{f_T}','proof, relative Ext','Relative Ext is wavy-underlined; the preceding prose Ext globaux remains ununderlined.')
    printed="0\\longrightarrow\\mathcal G_{T_1}\\longrightarrow\\mathcal G''\n\\longrightarrow\\mathcal G'_{T_1}\\longrightarrow0"
    corrected="0\\longrightarrow\\mathcal G'_{T_1}\\longrightarrow\\mathcal G''\n\\longrightarrow\\mathcal G_{T_1}\\longrightarrow0"
    if tree=='fr':
        r(corrected,printed,'displayed extension','The scan has unprimed G at the left and primed G at the right; first restore it to make the existing correction explicit.')
        r(printed,corrected,'displayed extension',
          'Ext^1(G,G-prime) classifies extensions 0 to G-prime to middle term to G to 0. The vector bundle T_1 above has that Ext sheaf of sections, and (ii) specifies extensions of F by F-prime. The supplied reversal of the printed endpoints is therefore retained.',
          'misprint of the original')
    s,_,_=page_text(rel,252)
    r(r'\longrightarrow',r'\to','all arrows','Each arrow is a short single arrow, as visible beside its letters and in the displayed sequence.',count=s.count(r'\longrightarrow'))
    upright_page(rel,layer,'221-252')

event('221-1.2','carried as background without fault found',
      'Read both boundedness assertions and the first part of the parameter-space argument. The existence of the required flattening and base-change strata is carried as cited background, not independently proved here.',
      '221, p. 252, Proposition 1.2 and proof')
event('221-1.2-extension-order','targeted proof check',
      'Checked the variance defining Ext^1(G,G-prime): the subobject is G-prime and the quotient is G. This matches part (ii) and the preceding relative Ext sheaf. Confirmed the supplied endpoint swap in corrected French; printed French preserves the reversed sequence.',
      '221, p. 252, displayed universal extension')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-252')
record_page('221',252,'Compared sources/fr_printed/fr/221.tex and sources/fr/fr/221.tex, entry lines 142-190, with scan leaf 5 at 400 dpi and enlarged top, middle and bottom bands. Read both opening paragraphs, all of Proposition 1.2, its proof through the page end, the only displayed sequence, and every index, prime and reference.\n\nRestored the wavy-underlined local operators, the explicit O_X_T ring index, the unstarred printed direct-image shorthand f_T, straight statement underlining, short arrows and the note dash. The global Ext in the opening prose is intentionally ununderlined. Removed the unprinted explanatory footnote. Retained the existing endpoint swap in the corrected universal extension, with an explicit variance check, while preserving the reversed printed sequence in the printed layer. References [5], III, section 6 and [5], IV are retained as printed, pending their bibliography-context check.\n\nOperation counts: '+ '; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final second reading pending.')
from update_record_counts import update
update()
