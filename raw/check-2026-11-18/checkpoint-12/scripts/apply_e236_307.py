from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/e236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'e236-307',line,'Final affineness supplement',
                'Scan leaf 6 at 400 dpi, full page and enlarged paragraph/rule crop: '+why,kind=kind,count=count)
    r('le morphisme\n\\[\n\\operatorname{Pic}_{Y/k}\\longrightarrow\\operatorname{Pic}_{X/k}\n\\]\nest affine','le morphisme\n$\\operatorname{Pic}_{Y/k}\\longrightarrow\\operatorname{Pic}_{X/k}$\nest affine','final paragraph','The morphism is inline.','structure')
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}','two Picard schemes','The labels are straight-underlined.',count=2)
    r(r'\longrightarrow',r'\to ','pullback arrow','The printed arrow is short.')
    r('est affine (','est '+r'\uline{affine} (','affineness conclusion','Only affine is straight-underlined in this phrase.','typesetting')
    old=r'''\par\smallskip
\begingroup\footnotesize
\noindent\textit{La lecture imprimée demande que les coefficients $a_1$ et $a_2$ restent bornés, sans préciser le cas $n<2$. La lecture courante explicite seulement la convention des coefficients absents en basse dimension. Il ne s'agit pas d'une assertion imprimée démontrée fausse.}\par
\endgroup'''
    r(old,r'\par\medskip\begin{center}\rule{4cm}{0.4pt}\end{center}','end of item','The scan ends with a short horizontal rule and has no editorial paragraph on coefficient conventions. Remove that supplied addition from both layers.','structure')
    upright_page(rel,layer,'e236-307')
event('e236-affineness','carried as background without fault found','Read the stronger conclusion over a field: the pullback morphisms under (i) and (ii) are affine. This directly answers the affineness question in exposé 232, Remark 6.7, p. 160, as the e232 entry promises. The final paragraph refers back to the proofs without supplying a complete affine-kernel/descent argument, so affineness is not upgraded to an independently proved result. It is stronger than the finite-type assertions and must be retained in every translation.','Erratum 236, p. 307, final paragraph; exposé 232, p. 160, Remark 6.7; erratum 232, p. 303, Page 18, Remark 6.7')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='e236-307')
record_page('e236',307,'Compared sources/fr_printed/fr/e236.tex and sources/fr/fr/e236.tex, entry lines 190-201, with scan leaf 6 at 400 dpi, full page and enlarged crop of the entire paragraph and terminal rule. Restored the inline morphism, straight-underlined Pic and affine, short arrow and terminal rule; removed the unprinted editorial paragraph on missing coefficients. Both French layers agree. Read the stronger affineness assertion and checked its link to 232, Remark 6.7, p. 160. Its proof remains background. This completes the sequential first reading of all 211 French item/page keys.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
