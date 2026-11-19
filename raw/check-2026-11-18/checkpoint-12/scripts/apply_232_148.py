from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/232.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'232-148',line,'2.6, 3, beginning of 3.1',
                'Scan leaf 7 at 400 dpi and all three enlarged bands: '+why,kind=kind,count=count)
    r(r'\result{REMARQUE}{2.6}',r'\result{\uline{Remarque}}{2.6}','2.6 heading','Remarque is mixed case and straight underlined.')
    r(r'\longrightarrow',r'\to','ten arrows','All single arrows are short.',count=10)
    r(r'\rightrightarrows',r'\mathrel{\substack{\longrightarrow\\[-0.6ex]\longrightarrow}}','two equalizer diagrams','Both diagrams have two long parallel right arrows.',count=2)
    r('i.e.','i. e.','first sentence','The abbreviation has spaced initials.')
    r('Appliquant 2.4, on trouve une suite exacte\n','Appliquant 2.4, on trouve une suite exacte.\n','before second diagram','A printed period follows exacte.')
    r('« provient »',"``provient''",'after second diagram','The print has ordinary double quotation marks.')
    r('(resp. simple, etc.), de se borner','(resp. simple, etc.) de se borner','finite-type example','There is no comma after the parenthesis.')
    r(r'\longmapsto',r'\rightsquigarrow','Picard-functor assignment','The arrow is wavy and has no initial mapsto bar.')
    r('(resp. simples, etc.)','(resp. simple, etc.)','second parenthesis','The print has singular simple here.')
    r('revêtements plats',r'\uline{revêtements plats}','multisections','The phrase is straight underlined.')
    r(r"\fsection{3}{Le théorème principal d'existence : énoncé}",r"\fsection{3}{\normalfont\uwave{Le théorème principal d'existence} : \uwave{énoncé}.}",'section 3 heading','The two upright title spans are wavy underlined, with the colon and final period outside.')
    r('préschémas de Picard englobant','préschémas de Picard, englobant','opening of section 3','The print has a comma after Picard.')
    r('« pratiquement\nnécessaire »',"``pratiquement\nnécessaire''",'historical qualification','The print uses ordinary double quotation marks.')
    r('soit propre\n','soit \\uline{propre}\n','properness condition','The word propre is straight underlined.')
    r('essentielles) et plat.','essentielles) et \\uline{plat}.','flatness condition','The word plat is straight underlined.')
    r(r'\mathbf C',r'\text{\uwave{C}}','complex field','C is ordinary upright with a short wavy underline, not bold.')
    r('On suppose :','On suppose','3.1 opening','There is no colon after suppose.')
    r('$f$ projectif ;','$f$ projectif','3.1(i)','No semicolon is printed at the end of this page.')
    if tree=='fr':
        r('et de même pour le foncteur de Picard de $X$ sur $S$, puisque,','et de même pour le foncteur de Picard de $X$ sur $S$ si les conditions de 2.2 sont vérifiées après tout changement de base, puisque,','passage from group to whole functor','As in 2.3, applying 2.4 to every test family requires the direct-image condition after arbitrary base change. The punctured real projective-line family from the 2.3 event disproves the unqualified inference, even with a global section. The fixed-base equalizer formulas preceding this sentence need no added hypothesis.','misprint of the original')
    upright_page(rel,layer,'232-148')
event('232-2.6-fixed-base','targeted proof check','The full Picard functor is an fpqc sheaf, giving the first equalizer for S-prime to S. The given S-prime to X supplies a section of X-prime over S-prime, and hence of X-double-prime over S-double-prime. Flat base change preserves the direct-image equality. Applying 2.4 on these two bases identifies their relative groups with the displayed quotients, giving the second equalizer and the stated source of representatives. If f itself is faithfully flat, the diagonal gives the section after S-prime=X; its base changes preserve finite type or smoothness as claimed.','232, p. 148, remarque 2.6, first two displays and examples')
event('232-2.6-functor-printed','refuted, with the refined statement id 232-2.6-universal','The inference to every test scheme T silently requires the hypotheses of 2.2 for X_T to T. The counterexample in event 232-2.3-printed has a global section and f_*O_X=O_S, but at its closed real fibre the nonzero class Pic(U)=Z/2 is killed by complex extension. Taking the original section cover S-prime=S would make the claimed functor description identify that quotient with its associated fpqc Picard group, which is impossible.','232, p. 148, sentence beginning et de même pour le foncteur')
event('232-2.6-universal','targeted proof check','Adding the universal direct-image condition only where the discussion passes to the whole functor makes the fixed-base argument applicable to every X_T to T. The pulled-back cover T-prime=S-prime times_S T then has a section of X_T and yields the desired quotient/equalizer description.','232, p. 148, corrected functor sentence')
event('232-2.6-multisections','carried as background without fault found','The asserted finite flat local multisections for a projective flat family over a locally Noetherian base, and finite etale choices in the separable case, are read and retained. A proof needs the finite-flat quasi-section construction, with a fibrewise smooth or separable choice for the etale version; those existence inputs are not independently established on this page.','232, p. 148, final sentence of 2.6')
event('232-3-introduction','carried as background without fault found','The phrase practically necessary is an explicitly qualified historical description, not a literal necessary-condition theorem. The assertion that proper flat curves over the dual numbers may lack a Picard scheme is recorded as an unproved existence claim here; no example is supplied on this page. The statement of 3.1 only begins here, through projectivity, and will be checked when its remaining hypotheses and conclusion have been read.','232, p. 148, section 3 opening and 3.1(i)')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='232-148')
record_page('232',148,'Compared both French layers, entry lines 269-318, with scan leaf 7 at 400 dpi and all three enlarged bands. Read all of remarque 2.6, both equalizer displays, the complete section 3 introduction and the first hypothesis of 3.1.\n\nRestored mixed-case underlined Remarque, short and paired long arrows, quotation marks, punctuation, the wavy assignment, the printed singular simple, straight emphasis, wavy heading spans, and the ordinary wavy-underlined complex-field C. Retained all primes and fibre-product bases after enlarged inspection. The universal hypothesis needed in 2.3 also qualifies the sentence passing from the fixed-base calculation to the whole Picard functor; it is added only at that sentence in corrected French. Checked both fixed-base equalizers and the diagonal-section example. The multisection existence theorem and the historical nonexistence assertion remain explicitly background claims.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
