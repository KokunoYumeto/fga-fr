from audit_utils import *
from collections import Counter
import csv
dq=chr(96)*2
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/e236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'e236-303',line,'Errata to TDTE VI',
                'Scan leaf 2 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    r(r'\noindent\textbf{8. TDTE VI : Les schémas de Picard. Propriétés générales.}',r'\noindent 8. \uwave{TDTE} VI : \uwave{Les schémas de Picard. Propriétés générales}.','title','Ordinary type with separate wavy underlines under TDTE and the title words.','typesetting')
    headings=['Page 12, ligne 16',r'Page 16, proposition 3.1, 6\textsuperscript{e} ligne','Page 21, § 4 : Le théorème de finitude pour le schéma de\nPicard']
    for s in headings:
        r(r'\textbf{'+s+'.}',r'\uline{'+s.replace(r'6\textsuperscript{e}','6e')+'}.','three entry headings','Straight underlines and ordinary type; 6e is on the baseline.','typesetting')
    r(r'\textbf{Ligne 18.}',r'- \quad \uline{ligne 18}.','continuation heading','A ditto dash precedes lowercase ligne, with a straight underline.','typesetting')
    r(' ---',' -','four separators','Short dashes are printed.',count=4)
    r('« ',dq,'six quoted readings','Ordinary double quotation marks are printed.',count=6)
    r(' »',"''",'six quoted readings','Ordinary double quotation marks are printed.',count=6)
    r('préschémas de Picard intervenant dans les énoncés existent','préschémas de Picard, intervenant dans les énoncés, existent','standing existence hypothesis','The intervening phrase is set off by two commas.')
    r('alors\n\\[\nf^*: \\operatorname{Pic}_{Y/S}\\longrightarrow\\operatorname{Pic}_{X/S}\n\\]\nest','alors $f^*: \\operatorname{Pic}_{Y/S}\\longrightarrow\\operatorname{Pic}_{X/S}$\nest','assertion (i)','The pullback arrow runs within the line; it is not a separate display.','structure')
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}','two Picard schemes in (i)','Pic has a straight underline.',count=2)
    r(r'\longrightarrow',r'\to ','two arrows','The scan has short arrows.',count=2)
    upright_page(rel,layer,'e236-303')
event('e236-affine-line','targeted proof check','Read the replacements A^1 -> A^1 minus the origin and X[t] -> X[t,t^(-1)]. Checked the defect in an A^1-only test: every morphism A^1_k -> G_m over a field comes from a unit of k[t] and is constant, although G_m is not proper. The punctured affine line detects G_m through its identity map, which cannot extend to P^1. This verifies the need for the changed test, conditional on the remaining group-structure argument in the exposition; it is not a full re-proof of the Picard properness theorem. Both original target phrases stay unmerged.','Erratum 236, p. 303, Page 12, lines 16 and 18; exposé 236, p. 232, proof of Theorem 2.1(ii)')
event('e236-3.1-grammar','used and rechecked in this run','Read the authorial insertion of de after Or and its comma. The proposition proof needs the construction from the stated hypothesis, and the added preposition repairs the sentence. The correction remains in the erratum, not merged into the exposé.','Erratum 236, p. 303, Page 16, Proposition 3.1, line 6; exposé 236, p. 236')
event('e236-i','carried as background without fault found','Read the new finiteness assertion: for a surjective morphism f:X->Y between proper S-schemes, with S noetherian and the indicated relative Picard preschemes existing, pullback Pic_(Y/S)->Pic_(X/S) is of finite type. The direction and both base subscripts match contravariant pullback. A proof of boundedness of the kernel and of the relative finite-type assertion is not supplied on this page and is retained as a dependency. Existence assumptions and the convention that the morphism is over S are material.','Erratum 236, p. 303, finiteness supplement, standing hypotheses and (i)')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='e236-303')
record_page('e236',303,'Compared sources/fr_printed/fr/e236.tex and sources/fr/fr/e236.tex, entry lines 5-38, with scan leaf 2 at 400 dpi, full page and three enlarged bands. Read the title, four erratum headings, standing hypotheses and finiteness assertion (i). Restored wavy title underlines, straight heading underlines, baseline 6e, continuation ditto dash and lowercase ligne, short dashes, ordinary quotation marks, the paired commas around intervenant dans les énoncés, inline pullback, short arrows and straight-underlined Pic. Both French layers agree. Checked the inadequacy of an affine-line-only properness test using G_m; the relative Picard finite-type theorem is carried as background.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
