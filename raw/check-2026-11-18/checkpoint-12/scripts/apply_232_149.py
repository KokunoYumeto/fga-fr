from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/232.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'232-149',line,'3.1-3.3',
                'Scan leaf 8 at 400 dpi and all three enlarged bands: '+why,kind=kind,count=count)
    r('$f$ plat ;','$f$ plat','3.1(ii)','There is no semicolon after plat.')
    r(r'\operatorname{Pic}_{X/S}',r'\underline{\operatorname{Pic}}_{X/S}','nine Picard-scheme names','Each representing scheme has a straight underline.',count=9)
    r(r'\operatorname{Pic}^{Q}_{X/S}',r'\underline{\operatorname{Pic}}^{Q}_{X/S}','3.3 Hilbert-polynomial piece','The Picard-scheme name is straight underlined here too.')
    r('ceci : soit','ceci : Soit','paragraph after 3.1','Soit begins with a capital S.')
    r('i.e.','i. e.','very ample bundle','The initials are spaced.')
    r(r'\mathbf P(\mathcal E)',r'P(\mathfrak E)','projective immersion','The P is ordinary typed P; the sheaf letter E is handwritten Gothic.')
    r(r'\longrightarrow',r'\to','two morphisms','Both arrows are short.',count=2)
    r('est séparé sur $S$.','est \\uline{séparé} sur $S$.','separatedness conclusion','The affirmative conclusion séparé is straight underlined.')
    for n in ['3.2','3.3']:
        r(r'\result{REMARQUE}{'+n+'}',r'\result{\uline{Remarque}}{'+n+'}','remark '+n,'Remarque is mixed case and straight underlined.')
    r("l'homomorphisme\n\\[\nk(s)\\to H^0(X_s,\\mathcal O_{X_s})\n\\]\nest", "l'homomorphisme\n$k(s)\\to H^0(X_s,\\mathcal O_{X_s})$ est",'3.2 fibrewise condition','The homomorphism is inline in the print.','structure')
    r('« éclate »',"``éclate''",'3.2 first degeneration','The quoted verb has ordinary double quotation marks.')
    r('« fibre multiple »',"``fibre multiple''",'3.2 second degeneration','The phrase has ordinary double quotation marks.')
    r('droites concourantes ; un exemple','droites concourantes, un exemple','3.2 examples','The print has a comma after concourantes.')
    r('fourni par D. Mumford,','fourni par D. MUMFORD,','3.2 attribution','The surname is printed in capitals.')
    note=list(footnotes(page_text(rel,149)[0])); assert len(note)==1
    r(r'\footnote{'+note[0][2]+'}','', '3.3 editorial note','The scan has no footnote or note marker. The 1962 answer remains in its separate erratum, not inserted into the exposé.','structure')
    r(r'\mathbf Q[t]',r'\text{\uwave{Q}}[t]','Hilbert-polynomial coefficient field','The field Q is ordinary typed with a wavy underline, distinct from the ununderlined polynomial Q.')
    r('projectif localement\n','projectif \\uline{localement}\n','last paragraph','Only localement is straight underlined.')
    upright_page(rel,layer,'232-149')
event('232-3.1','carried as background without fault found','Read the complete hypotheses across pp. 148-149: locally Noetherian schemes, projectivity, flatness and geometrically integral fibres, followed by existence of the Picard scheme. The proof is expressly deferred to sections 4 and 5, so the existence claim is not yet marked proved in this reading. The stronger translated-open description is also read as the forthcoming construction.','232, pp. 148-149, theorem 3.1 and following paragraph')
event('232-3.1-separatedness','targeted proof check','Conditional on the asserted open U, each U minus n xi is separated because U is a disjoint union of quasi-projective S-schemes. These translated opens form an increasing cover. Every product of two such opens lies in the square of a common larger separated open; therefore the diagonal is closed locally on a covering of the product. The Picard scheme is separated. Stable by translation is used as inclusion U+xi contained in U, not equality.','232, p. 149, last conclusion after 3.1')
event('232-3.2-conic','independent re-proof','Over R=k[[t]], take the projective conic xy=t z^2. Its generic fibre is smooth and geometrically integral in every characteristic; its special fibre is two transverse lines. The total space is regular, and each special component D is a Cartier divisor. The bundle O(D) is trivial on the generic fibre but has degrees -1 and 1 on the two special components, hence is nontrivial on the special fibre. The fibrewise H-zero is k(s) for both fibres. Thus the zero section and the class of O(D) agree generically and differ at the special point, violating separatedness for any representing relative Picard scheme. This checks the first example and the all-characteristic assertion for it, without claiming an independent construction of the representing scheme.','232, p. 149, remarque 3.2, conic example')
event('232-3.2-double-elliptic','carried as background without fault found','Read the attribution to D. Mumford and the assertion of an elliptic curve specializing to a double elliptic curve, valid in every characteristic. The page gives no construction or proof; this second example is not covered by the conic calculation and remains background pending the contextual notes.','232, p. 149, remarque 3.2, second example')
event('232-3.3','targeted proof check','The Hilbert polynomial of an invertible sheaf in a projective flat family is locally constant; twisting by a line bundle from the base does not change it on fibres, and the condition descends along fpqc covers. Hence the represented Picard functor decomposes into open-and-closed polynomial loci as claimed. Zariski-local existence glues uniquely by representability and the natural identifications on overlaps. The question whether each polynomial piece is quasi-projective is retained as a question, with its unprinted later-answer footnote removed. The final warning continues on p. 150.','232, p. 149, remarque 3.3')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='232-149')
record_page('232',149,'Compared both French layers, entry lines 319-369, with scan leaf 8 at 400 dpi and three enlarged bands. Read the end of 3.1, the translated-open description, all of 3.2 and 3.3 through the final page break.\n\nRestored ten straight-underlined Picard-scheme names, ordinary projective-space P with Gothic E, the wavy-underlined rational-field Q, exact prose emphasis, mixed-case underlined remark heads, punctuation and the inline H-zero condition. Removed the unprinted footnote merging a later erratum. The theorem remains a statement awaiting its printed proof; checked the implication from the increasing separated open cover, re-proved the nonseparatedness obstruction in the conic example, and checked the polynomial-locus and Zariski-gluing mechanisms. The double elliptic example remains background. No new mathematical difference between the two French layers was introduced on this page.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
