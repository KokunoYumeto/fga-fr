from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'236-235',line,'2.8, 2.9, 2.10(i)',
                'Scan leaf 16 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    r("Picard) sont séparés sur l'ouvert de $S$ où $n$ est inversible (compte tenu\nqu'ils sont étales sur cet ouvert grâce à (2.5)).",
      "Picard) sont \\uline{séparés} sur $S$, (compte tenu\nqu'ils sont étales sur $S$ grâce à (2.5)).",
      'continuation of 2.8','The print says sur S twice, with no invertibility qualification, underlines séparés and has a comma before the parenthesis.')
    r(r"\tag{***}\alpha\leq\alpha',\qquad\lambda\geq\lambda',",
      r"\tag{***}\alpha\leqslant\alpha',\qquad\lambda\geqslant\lambda'",
      'formula (***)','Both inequalities have slanted lower strokes; the only comma is between them.')
    r(r'\result{REMARQUE}{2.9}',r'\result{\uline{Remarque}}{2.9}',
      'remark heading','Remarque has mixed case and a straight underline.')
    r('Mumford','MUMFORD','two name occurrences','Both occurrences have capitals.',count=2)
    r(r'simple) que $\operatorname{Pic}_{X/S}^\tau$ soit',
      r'simple) que $\operatorname{Pic}_{X/S}$ soit',
      'flatness speculation','The Picard name after que has no superscript.')
    r('Il semblerait que, même','Il semblerait que même','second remark paragraph','There is no comma after que.')
    r('sont réduites et sans',r'sont \uline{réduites} et sans',
      'geometric fibres','The word réduites has a straight underline.')
    r(r'\result{PROPOSITION}{2.10}',r'\par\noindent PROPOSITION 2.10.',
      'proposition heading','The heading ends with a period and has no dash.','structure')
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}',
      'fifteen Picard names','All fifteen names have straight underlines.',count=15)
    r(r'\longrightarrow',r'\to','four structure arrows','All four arrows are short.',count=4)
    if tree=='fr':
        r("Picard) sont \\uline{séparés} sur $S$, (compte tenu\nqu'ils sont étales sur $S$ grâce à (2.5)).",
          "Picard) sont \\uline{séparés} sur l'ouvert de $S$ où $n$ est inversible, (compte tenu\nqu'ils sont étales sur cet ouvert grâce à (2.5)).",
          'continuation of 2.8','The étaleness supplied by 2.5 requires n invertible. For an elliptic curve in characteristic p, the tangent map of multiplication by p is zero and its p-torsion has a nonzero tangent space, so that kernel is not étale. The prime-to-characteristic torsion argument is used only on the invertibility open. This records and justifies the existing qualification.','misprint of the original')
    upright_page(rel,layer,'236-235')
event('236-2.8-torsion','targeted proof check',
      'The appeal to 2.5 makes the n-torsion kernel étale only on the open where n is a unit. For an elliptic curve over a field of characteristic p, d[p]=p on its one-dimensional tangent space is zero, so the p-kernel has a nonzero tangent space and is not étale. Thus the unqualified printed parenthesis cannot hold for arbitrary n. The corrected layer retains the existing invertibility qualification, now explicitly separated from the printed reading. The specialization injection for separated étale prime-to-characteristic torsion and its conversion to (**) are background inputs.',
      '236, p. 235, continuation of 2.8, opening lines')
event('236-2.8-conjectures','carried as background without fault found',
      'Read the proposed equality in (*) and the proposed inequalities alpha<=alpha prime, lambda>=lambda prime in (***). They are expressly conjectural in the text; no proof or affirmative verdict is claimed. The reference to 1.3 is kept as a partial result, not a proof of these conjectures.',
      '236, p. 235, 2.8, formula (***) and following paragraph')
event('236-2.9','carried as background without fault found',
      'Read the Mumford infinitesimal Igusa-surface example and the open flatness questions as historical claims and questions. No construction of that example has been checked here. The printed speculative flatness sentence names the whole Picard scheme, with no tau; the transcription is restored. The smoothness assertion on Pic sigma is conditional on 1.8 and 2.5 and the preceding openness result, and the stronger normal-fibre assertion is a forward reference to 3.5, not yet examined.',
      '236, p. 235, remark 2.9')
event('236-2.10-i','targeted proof check',
      'Assuming the multiplication maps are étale for locally invertible n by 2.5, 1.12 propagates smoothness or flatness from the identity along Pic sigma. Translation by any S-section is an S-isomorphism carrying the identity section to that section, so it preserves both properties. This checks the stated deduction; the general openness and multiplication results remain its previously identified inputs.',
      '236, p. 235, proposition 2.10(i)')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='236-235')
record_page('236',235,'Compared sources/fr_printed/fr/236.tex and sources/fr/fr/236.tex, entry lines 636-685, with scan leaf 16 at 400 dpi, full page and three enlarged bands. Read the continuation of 2.8, remark 2.9 and proposition 2.10(i).\n\nRestored the two printed sur S phrases before recording the necessary invertibility qualification in corrected French alone. Checked its necessity by the tangent space of elliptic p-torsion. Restored the absent superscript in the speculative flatness sentence, the fifteen straight Picard names, underlined words, heading case and punctuation, capitals and short arrows. Kept the conjectures as conjectures and the unconstructed Mumford example as background; checked the translation argument in 2.10(i). The remaining parts of 2.10 are on the next page.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
