from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'236-238',line,'3.3 proof, 3.4',
                'Scan leaf 19 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    r('Chow.','CHOW.','rigidity attribution','The name is in capitals.')
    r('est étale, ou, dans','est étale, ou dans','proof of (ii)','There is no comma after ou.')
    r('homogène sous $C$ équivaut','homogène sous $C$, équivaut',
      'proof of (iii)','The print has a comma after C.')
    r('dual de $C$. Or, si','dual de $C$. Or si',
      'proof of (iii)','There is no comma after Or.')
    r(r'\result{REMARQUES}{3.4}',r'\result{\uline{Remarques}}{3.4}',
      'remark heading','Remarques has mixed case and a straight underline.')
    r('est réduit, ou, ce qui','est réduit, ou ce qui',
      'reduced-base speculation','There is no comma after ou.')
    r('Soient alors $X_0,X_1$ les fibres spéciale et',
      'Soient alors $X_0,X_1$ la fibre spéciale et',
      'two fibres','The print uses the distributive singular la fibre.')
    r('générique de $X$, et soit\n\\[\nA_1=\\operatorname{Pic}_{X_1/K}^\\circ,\n\\]\noù',
      'générique de $X$, et soit $A_1=\\operatorname{Pic}_{X_1/K_1}$, où',
      'definition of A1','The formula is inline, has K subscript 1, and has no Picard superscript.','structure')
    r('Koizumi','KOIZUMI','good reduction attribution','The name is in capitals.')
    r('(supposant désormais $X$ simple sur $S$), que',
      '(supposant désormais $X$ simple sur $S$) que',
      'extension argument','There is no comma after the closing parenthesis.')
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}',
      'eleven Picard names','All eleven names have straight underlines.',count=11)
    r(r'\longrightarrow',r'\to','seven arrows','All seven arrows are short.',count=7)
    if tree=='fr':
        r(r'$A_1=\underline{\operatorname{Pic}}_{X_1/K_1}$',
          r'$A_1=\underline{\operatorname{Pic}}_{X_1/K}^{\circ\circ}$',
          'definition of A1','K is the fraction field defined in the same sentence; K_1 is undefined. The ensuing A is an abelian scheme, so its generic fibre must be the canonical abelian subscheme just denoted Pic with double circle, rather than the entire Picard scheme. For X=P1, the entire Picard scheme has degree components indexed by Z and cannot be that abelian variety. The previous single-circle correction is insufficient to specify the reduced smooth subgroup in positive characteristic.','misprint of the original')
    upright_page(rel,layer,'236-238')
event('236-3.3-i-continuation','carried as background without fault found',
      'The continuation cites [7] and describes the rigidity statement as a generalization of Chow. No proof of this general rigidity result is supplied on this page; it remains a background input to uniqueness.',
      '236, p. 238, opening continuation of 3.3(i)')
event('236-3.3-ii-proof','targeted proof check',
      'Assuming Hilbert representability by the stated finite-type T and uniqueness, T to S is a surjective monomorphism. A section makes a monomorphism an isomorphism. An étale monomorphism is an open immersion and surjectivity then makes it an isomorphism. A proper monomorphism is a closed immersion; if S is reduced, a surjective closed immersion has defining ideal with zero radical and hence zero ideal, so again is an isomorphism. These deductions check the reduced-base qualification. Hilbert representability, formal étaleness from the Artin tests and the valuative criterion are background inputs.',
      '236, p. 238, proof of theorem 3.3(ii)')
event('236-3.3-iii-proof','carried as background without fault found',
      'Read the correspondence between a C-torsor equipped with a map from X (up to torsor isomorphism) and a group morphism from the dual C prime to Pic. The claimed factorization through the canonical abelian subscheme is justified in the text by finite-order points. This uses abelian duality, torsor descent and schematic density of suitable torsion; no complete proof of these inputs is supplied or claimed here.',
      '236, p. 238, proof of theorem 3.3(iii)')
event('236-3.4-A1','targeted proof check',
      'The print defines A1 as the whole Pic_{X1/K1}, with undefined K1 and no superscript. But A1 is immediately required to be the generic fibre of an abelian scheme A. Already for the constant family P1 over a trait, the whole Picard scheme has components indexed by Z and is not an abelian variety. The context has just defined the canonical abelian subgroup by the double circle. Thus A1 must be Pic^{00}_{X1/K}, with K the fraction field named in the sentence. A single circle does not specify the reduced smooth subgroup when the identity component is nonreduced.',
      '236, p. 238, remark 3.4, definition of A1')
event('236-3.4-good-reduction','carried as background without fault found',
      'Read the infinitesimal Igusa nonexistence example, the reduced-base conjecture, Koizumi good reduction and uniqueness, extension to Pic under the subsequently stated smoothness hypothesis, and the special-fibre surjection with finite p-primary kernel. These are background claims here; the general reduced-base question remains explicitly conjectural. The final sentence continues on p. 239.',
      '236, p. 238, remark 3.4, through formula (*) and its first explanation')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='236-238')
record_page('236',238,'Compared sources/fr_printed/fr/236.tex and sources/fr/fr/236.tex, entry lines 783-833, with scan leaf 19 at 400 dpi, full page and three enlarged bands. Read the conclusion of the proof of 3.3 and remark 3.4 through the first explanation of (*).\n\nRestored capitals, remark heading, punctuation, the distributive singular la fibre, eleven straight Picard names and seven short arrows. Restored the exact inline A1 formula with printed K1 and no superscript; corrected French alone changes it to the canonical abelian Picard subgroup over K, with double circle. Checked the monomorphism argument and the necessity of the reduced-base hypothesis in its properness branch. The torsor duality, rigidity, Koizumi theorem, Igusa example and special-fibre isogeny are recorded as background inputs. The final sentence continues on the next page.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
