from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/232.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'232-156',line,'5.2-5.3',
                'Scan leaf 15 at 400 dpi and all three enlarged bands: '+why,kind=kind,count=count)
    r("relation d'équivalence propre et plate", "relation d'équivalence \\uline{propre} et plate",'first line','Only propre is underlined.')
    r('schéma des diviseurs est remplacé','schéma des diviseurs, est remplacé','second line','There is a comma after diviseurs.')
    r(r'\mathbf P^r_S',r'\text{\uwave{P}}^r_S','projective target of immersions','The typed P has a short wavy underline; its r and S are respectively upper and lower indices.')
    r('résultats de Mumford','résultats de MUMFORD','quotient attribution','The surname is uppercase.')
    r('« beaucoup\nde sections locales »',"``beaucoup\nde sections locales''",'local-sections phrase','The print uses ordinary double quotation marks.')
    note=list(footnotes(page_text(rel,156)[0]))
    assert len(note)==1
    r('\\footnote{'+note[0][2]+'}','','after complet','No footnote occurs here. Keep the separate erratum separate.','structure')
    r('complet à corps résiduel algébriquement\nclos.','complet.','local ring hypothesis','The printed sentence ends at complet. The residue-field restriction is an inserted later erratum and is removed from the expose in both layers.','structure')
    r(r'\mathbf P(\mathcal Q)',r'P(\mathfrak Q)','projective bundle in the technical parenthesis','P is plain upright and the handwritten coherent module Q is Gothic, as on the preceding pages.')
    r('mais par un ouvert dudit','mais par un \\uline{ouvert} dudit','technical parenthesis','Only ouvert is straight underlined.')
    r(r'\result{REMARQUE}',r'\result{\uline{Remarque}}','heading 5.3','The heading is mixed case and underlined.')
    r('Lang','LANG','historical attribution','LANG is uppercase.')
    r('Chevalley','CHEVALLEY','two historical attributions','CHEVALLEY is uppercase.',count=2)
    r('A. Weil','A. WEIL','historical attribution','WEIL is uppercase.')
    r('nous avons prises comme définition','nous avons pris comme définition','definition of Picard properties','The scan reads pris, without es.')
    if tree=='fr':
        r('nous avons pris comme définition','nous avons prises comme définition','definition of Picard properties','The preceding direct object is the feminine plural propriétés, so the past participle agrees as prises.','misprint of the original')
    r('numéro 1\n(','numéro 1,\n(','definition reference','A comma appears before the parenthesis.')
    r('« variétés de\nparamètres »',"``variétés de\nparamètres''",'parameter varieties','The print uses ordinary double quotation marks.')
    r('« jacobiennes\ngénéralisées »',"``jacobiennes\ngénéralisées''",'singular curves','The print uses ordinary double quotation marks; Rosenlicht remains mixed case.')
    upright_page(rel,layer,'232-156')
event('232-5.2-open-Abel-fibre','independent re-proof','For a connected nodal curve made of two projective lines meeting at one point, take a line bundle of degree one on each component. The normalization exact sequence gives h0=2+2-1=3 and h0(O)=1, also after field extension. In the projective plane of sections, sections vanishing identically on either component form two distinct points. Precisely these nonzero sections are zero-divisors at a generic point of a component; all other sections define effective Cartier divisors. Thus the Abel fibre is P2 minus two points and is not proper. This verifies the technical obstruction in 5.2 without claiming that the printed completeness hypothesis suffices for the existence assertion.','232, p. 156, technical parenthesis continuing 5.2')
event('232-5.2-complete-base','carried as background without fault found','The print says only complete local ring. The added algebraically closed residue-field clause and editorial footnote have been removed from both expose layers, in compliance with the separate-errata convention. The claim is recorded as the original historical assertion, with its later correction reserved for the erratum check; no proof of the unqualified claim is asserted.','232, p. 156, lines 6-8')
event('232-5.3','targeted proof check','For an irreducible rational nodal projective curve over an algebraically closed field, a degree-zero line bundle pulls back trivially to the normalization P1. Descent identifies its two fibres over the node by a nonzero scalar; automorphisms of the trivial bundle act by the same scalar on both fibres and do not alter that gluing parameter. Tensor product multiplies parameters, giving Pic0=G_m, which is not proper and hence not an abelian variety. This directly verifies the singular-curve example supporting the remark. Historical priority and the general duality simplification are carried as background, not independently proved.','232, p. 156, remarque 5.3')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='232-156')
record_page('232',156,'Compared both French layers, entry lines 658-700, with scan leaf 15 at 400 dpi and three enlarged overlapping bands. Read the continuation of 5.2 and all of 5.3, including every reference and the two differently marked projective-space letters.\n\nRestored emphasis, wavy projective target, plain projective bundle with Gothic Q, exact names, quotation marks, punctuation and the printed participle pris. Corrected the latter to prises only in corrected French. Removed the later residue-field insertion and its unprinted footnote from the expose. Independently checked a nonproper Abel fibre on a reducible nodal curve and checked Pic0=G_m on a rational nodal curve; historical and general duality assertions remain background.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
