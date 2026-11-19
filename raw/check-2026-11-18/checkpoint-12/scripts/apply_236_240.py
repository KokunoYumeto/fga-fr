from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'236-240',line,'3.5-3.8',
                'Scan leaf 21 at 400 dpi, full page, three enlarged bands and tangent, structure and Omega details: '+why,kind=kind,count=count)
    r('obstruction qui se trouve dans\n\\[\nH^2(X_0\\times P_0,\\mathcal O_{X_0\\times P_0})\\otimes_k V\n\\qquad(\\text{où }V=\\mathfrak m^{n+1}/\\mathfrak m^{n+2}),\n\\]\net même dans le sous-espace\n\\[\nH^1(X_0,\\mathcal O_{X_0})\\otimes\nH^1(P_0,\\mathcal O_{P_0})\\otimes_k V\n\\]\n',
      'obstruction qui se trouve dans un $H^2(X_0\\times P_0,\\mathcal O_{X_0\\times P_0})\\otimes_k V$\n(où $V=m^{n+1}/m^{n+2}$), et même dans le sous-espace\n$H^1(X_0,\\mathcal O_{X_0})\\otimes H^1(P_0,\\mathcal O_{P_0})\\otimes_k V$\n',
      'obstruction and mixed summand','The two cohomology formulas and V definition are inline; un precedes the first H2 and the maximal ideal has an ordinary typed m.','structure')
    r("Or ce dernier espace n'est autre que\n\\[\nH^1(P_0,\\mathcal T_{P_0/k})\\otimes V,\n\\]\noù", 
      "Or ce dernier espace n'est autre que $H^1(P_0,\\mathcal T_{P_0/k})\\otimes V$, où",
      'deformation space','The tangent cohomology formula is inline, with the comma outside mathematics.','structure')
    r(r'\mathcal T',r'\mathfrak G','two tangent sheaf symbols',
      'Both hand-inserted glyphs are the Gothic capital G used for derivations, confirmed by the tight crop; they are not a script T.',count=2)
    for num in ['3.7','3.8']:
        r(r'\result{REMARQUE}{'+num+'}',r'\noindent\uline{Remarque} '+num+'. -',
          'remark headings','The print has mixed-case Remarque with a straight underline and a short dash.')
    r('$\\operatorname{Pic}_{X/S}$',r'$\underline{\operatorname{Pic}}_{X/S}$',
      '3.6 tangent module','The Picard name has a straight underline.')
    r('$\\operatorname{Pic}_{X/S}^\\circ$',r'$\underline{\operatorname{Pic}}_{X/S}^\circ$',
      '3.7 conclusion','The Picard name in the conclusion is straight-underlined; the preceding X-prime/S-prime name has no underline and stays plain.')
    r('Rosenlicht--Serre','ROSENLICHT-SERRE','exterior algebra attribution','Both names are capitals, joined by a short hyphen.')
    r('pour tout\n$i$','pour \\uline{tout}\n$i$','all cohomology degrees','Only tout is underlined.')
    r(r'f:X\longrightarrow S',r'f:X\to S','3.8 morphism','The arrow has the short printed shaft.')
    r('théorie de Hodge','théorie de HODGE','3.8 attribution','HODGE is in capitals.')
    r(r'\Omega^q',r'\mathord{\underset{\sim}{\Omega}}^q','3.8 differentials',
      'The tight crop confirms a wavy underline under capital Omega, with the exponent q above and X/S below.')
    if tree=='fr_printed':
        r('la structure connue','la rtructure connue','3.7 exterior algebra',
          'The enlarged word has initial r, giving the printed rtructure; the typographical error is retained in this layer.')
    else:
        r('la structure connue','la rtructure connue','3.7 exterior algebra',
          'Record the printed initial r before the separate correction of the original.')
        r('la rtructure connue','la structure connue','3.7 exterior algebra',
          'The initial r produces no French word. The sentence describes the known exterior-algebra structure, so structure is required.','misprint of the original')
    upright_page(rel,layer,'236-240')
event('236-3.5-obstruction','targeted proof check',
      'Conditional on the stated deformation theory and unobstructed lifting of abelian schemes: the trivial restrictions of the rigidified Poincare bundle to the two factors kill the pure Kunneth summands, leaving H1(X0,O) tensor H1(P0,O) tensor V. Translation trivializes the tangent sheaf of P0 with fibre H1(X0,O), identifying the displayed mixed space with H1(P0,G) tensor V. The argument then requires that changing the marked lift of P_n acts by this identification on the obstruction; this compatibility and the unobstructedness theorem are background, not independently proved here. Uniqueness is read as uniqueness of the marked deformation class, not of an unmarked scheme or a literal gluing.',
      '236, p. 240, proof of 3.5, first paragraph')
event('236-3.6','targeted proof check',
      'Given 3.5, the identity-neighbourhood Picard scheme is smooth; its Lie module is locally free and commutes with arbitrary base change. The previously established tangent description identifies this Lie module with R1 f_* O_X. This checks the corollary conditional on representability, the tangent identification, and 3.5.',
      '236, p. 240, corollary 3.6 and following sentence')
event('236-3.7','carried as background without fault found',
      'Read the extension of the identity Picard scheme across a coherent nilpotent thickening, the existence of the dual abelian scheme over an Artinian base, and the exterior-power description of higher coherent direct images for an abelian scheme. Nilpotent extension/effectivity, the fibre cohomology exterior-algebra theorem attributed to Rosenlicht and Serre, and the cohomology/base-change passage are named inputs. The cup-product map becomes the asserted exterior-power isomorphism on fibres once those inputs are supplied; no independent proof of the inputs is claimed.',
      '236, p. 240, remark 3.7')
event('236-3.8','carried as background without fault found',
      'Read the characteristic-zero projective smooth case over a reduced base and the asserted local freeness of all Hodge direct images. The transcendental Hodge-theory argument and its descent to the stated base remain background. The counterexample sentence continues on p. 241 and is not yet assessed.',
      '236, p. 240, beginning of remark 3.8')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='236-240')
record_page('236',240,'Compared sources/fr_printed/fr/236.tex and sources/fr/fr/236.tex with scan leaf 21 at 400 dpi, the full page, three enlarged bands and tight tangent-glyph, structure-word and Omega crops. Read the end of the lifting proof, corollary 3.6, remark 3.7 and the beginning of 3.8.\n\nRestored the three inline formulas, the omitted un, ordinary maximal-ideal m, Gothic derivation sheaf, local Picard underline distinction, mixed-case remark headings, capitals, short arrow and hyphen, emphasis on tout and wavy Omega. Printed French retains rtructure; corrected French supplies structure. Checked the obstruction-space identification and tangent corollary conditional on the explicitly named deformation inputs, without claiming those inputs proved. The Hodge counterexample sentence continues on the next page.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
