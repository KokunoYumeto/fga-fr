from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-271',line,'5.4 / 5.5',
                'Scan leaf 24 at 400 dpi, all enlarged bands and tight glyph crops: '+why,kind=kind,count=count)
    r(r'\mathcal N_{Y_0/X_0}',r'\check{\mathcal N}_{X_0/Y_0}','six normal-sheaf signs','The normal-sheaf sign has a check accent and the printed subscript order is X_0/Y_0.',count=6)
    r(r'\check{\mathcal N}_{Y_0/X_0}',r'\mathcal N_{Y_0/X_0}','opening conormal-sheaf sign','The opening conormal sign has no check accent and its subscript is Y_0/X_0.')
    r("sur $Y_0$. D'ailleurs","sur $Y$. D'ailleurs",'opening cohomology space','The print has Y without a zero at this occurrence.')
    r('est garantie ;','est garantie,','local lifting sentence','The print has a comma.')
    r(r'\mathcal J_0/\mathcal J_0^2',r'\mathcal J/\mathcal J^2','local freeness of the conormal module','Neither J in the print has a zero.')
    r(r'\operatorname{Hilb}_{X/S}','X','5.4 smoothness conclusion','The print names the Hilbert scheme X, not Hilb with subscripts.')
    r('complète dans $X_0$ définie par une équation',r'complète dans $\phantom{X}_0$ définie par \uline{une} équation','5.5 first sentence','The tight crop shows only the orphan subscript zero: the X is absent. Only une is underlined.')
    r('i.e.','i. e.','Cartier-divisor explanation','The abbreviation is spaced.')
    r('« diviseur de Cartier »','"diviseur de Cartier"','Cartier-divisor term','The print has ordinary double quotes.')
    r(r'\mathcal J_0^{-1}',r'\mathcal J^{-1}','invertible sheaf of the divisor','The printed ideal has no zero.')
    r(r'et $H^0(Y_0,\check{\mathcal N}_{X_0/Y_0})$',r'et $\mathcal H^0(Y_0,\check{\mathcal N}_{X_0/Y_0})$','5.5 characteristic map target','The H at this particular occurrence is a handwritten script capital, unlike the typed cohomology H above.')
    r('« homomorphisme caractéristique »',r'"\uline{homomorphisme caractéristique}"','historical term','The quoted words are straight-underlined and use ordinary double quotes.')
    r('« famille continue complète »','"famille continue complète"','historical parameter family','The print has ordinary double quotes.')
    r("de notre point de vue, d'une composante","de notre point de vue, une composante",'description of the parameter variety','The print says une, without a preceding d apostrophe.')
    r('munie de la structure réduite',r'muni de la structure \uline{réduite}','reduced induced structure','The print says muni and underlines réduite.')
    r('un sous-espace de',r'un \uline{sous-espace} de','tangent-space inclusion','The term sous-espace is underlined.')
    r('Zappa [8]','ZAPPA [8]','last-line attribution','The surname is in capitals.')
    if tree=='fr':
        r("sur $Y$. D'ailleurs","sur $Y_0$. D'ailleurs",'opening cohomology space','The sheaf A is on the given closed subscheme Y_0; a lift Y is not yet assumed to exist.','misprint of the original')
        r(r'\mathcal J/\mathcal J^2',r'\mathcal J_0/\mathcal J_0^2','local freeness of the conormal module','This is the conormal ideal of Y_0 in X_0. The unindexed J is the square-zero ideal on the base, not this ideal.','misprint of the original')
        r('préschéma de Hilbert\n$X$','préschéma de Hilbert\n$Q$','5.4 smoothness conclusion','The point x parametrizes a quotient and belongs to Q, the Hilbert scheme in the F=O_X case. X denotes the ambient scheme and is not the scheme whose smoothness the obstruction calculation proves.','misprint of the original')
        r(r'dans $\phantom{X}_0$ définie','dans $X_0$ définie','5.5 Cartier-divisor ambient scheme','The missing letter is X: the divisor Y_0 is a closed subscheme of X_0 throughout this statement.','misprint of the original')
        r(r'\mathcal J^{-1}',r'\mathcal J_0^{-1}','invertible ideal of the divisor','The invertible ideal of Y_0 in X_0 is J_0. The square-zero base ideal J is not the invertible ideal defining this Cartier divisor.','misprint of the original')
        r(r'muni de la structure \uline{réduite}',r'munie de la structure \uline{réduite}','reduced induced structure','The reduced induced structure is that of the irreducible component representing T. The feminine agreement prevents this from attaching to the whole Hilbert open D, whose possible nonreduced structure is the point of the discussion.','misprint of the original')
    upright_page(rel,layer,'221-271')
event('221-lci-local-lifts','targeted proof check','Locally write the ideal of Y_0 by a regular sequence in the flat S_0-algebra of X_0, and lift its generators to the S-flat algebra of X. The local flatness criterion, applied successively to the lifted non-zero-divisors, gives an S-flat quotient lifting Y_0. The conormal module is finite locally free, so Hom(J_0/J_0^2,O_Y0 tensor J) identifies with the normal sheaf tensor J. This check uses the standard local flatness criterion. The print defines its checked N with subscript X_0/Y_0 as the normal sheaf, while the unaccented conormal sign was printed Y_0/X_0; the explicit definitions make the intended sheaves unambiguous, so their alphabet and subscript convention are retained rather than modernized.','221, p. 271, opening paragraph')
event('221-5.4','targeted proof check','The tangent statement is 5.3 with the ideal-to-conormal factorization. For a small extension of local Artinian test algebras with residue field K, the kernel I is a K-vector space; the lci calculation gives local lifts and their gluing obstruction lies in H^1(Y_0,N) tensor_K I. Vanishing of H^1 therefore permits every such lift. The infinitesimal smoothness criterion for the locally finite-presentation representing Hilbert scheme yields smoothness at x. The scheme in that conclusion must be Q, not the ambient X printed there. The standard infinitesimal criterion is used as an input, not independently re-proved.','221, p. 271, Corollary 5.4')
event('221-5.5','targeted proof check','For an effective Cartier divisor with invertible ideal I=J_0, I/I^2=I tensor O_Y0; its dual is I inverse restricted to Y_0. The closed immersion of the reduced irreducible parameter component T into D induces a surjection on cotangent spaces and hence an injection on tangent spaces. If D is integral at x, its local reduced component is the same germ, so the tangent inclusion is an isomorphism. This checks the mathematical comparison; the historical claims and the forthcoming Zappa example remain background pending their continuation.','221, p. 271, Remark 5.5')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-271')
record_page('221',271,'Compared printed French entry lines 1059-1099 and corrected French entry lines 1060-1100 with scan leaf 24 at 400 dpi, all three enlarged bands and 3x crops of the missing ambient letter and the script cohomology H. Read the local-complete-intersection lifting paragraph, all of 5.4 and the first part of 5.5.\n\nRestored the printed conormal and checked normal notation, including its differing subscript order; the normal sheaf is explicitly defined in the prose, so this convention is retained in both layers. Restored the missing indices, orphan zero, X naming the Hilbert scheme, script H, quotation marks, underlining, punctuation, muni, une composante and the capitalized ZAPPA. Corrected French restores the required Y_0 and J_0 indices, the missing X in X_0, the Hilbert scheme Q in the smoothness conclusion and feminine agreement with the parameter component. Checked local lci lifts using flatness, the H^1 obstruction criterion for smoothness and the Cartier normal sheaf and tangent inclusion.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
