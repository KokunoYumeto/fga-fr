from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/232.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'232-153',line,'4.3-4.5',
                'Scan leaf 12 at 400 dpi and three enlarged bands: '+why,kind=kind,count=count)
    r('diviseurs de zéro sur les','diviseurs de $0$ sur les','opening continuation','The print uses the numeral 0, not the word zéro.')
    r('i.e.','i. e.','three abbreviations','The initials are spaced.',count=3)
    r(r'\mathcal Q',r'\mathfrak Q','coherent module letters','The coherent module has the same Gothic Q as on p. 152.',count=13)
    r(r'\mathbf P',r'P','four projective space signs','P is ordinary upright, not bold.',count=4)
    r(r'\longrightarrow',r'\to','three arrows','All three arrows are short.',count=3)
    r('(Nakayama)','(NAKAYAMA)','surjectivity criterion','The attribution is uppercase.')
    r('des Modules quotients inversibles de','des \\uline{Modules quotients inversibles de}','quotient interpretation','The underline includes Modules through de, stopping before Q.')
    r('de $\\operatorname{Pic}(X\\times_SS\'/S\')$).','de $\\operatorname{Pic}(X\\times_SS\'/S\')$.','theorem parenthesis','The print omits the closing parenthesis for the parenthetical i. e. clause; the visible parenthesis closes Pic only.')
    r(r'\operatorname{Div}_{X/S}',r'\text{\uwave{Div}}_{X/S}','corollary divisor functor','Div has a wavy underline.')
    r(r'\operatorname{Pic}_{X/S}',r'\text{\uwave{Pic}}_{X/S}','corollary Picard functor','Pic has a wavy underline.')
    r(r'\result{REMARQUE}{4.5}',r'\result{\uline{Remarque}}{4.5}','remark heading','The heading is mixed case with a straight underline.')
    r('faire des sauts.','faire des \\uline{sauts}.','variation of dimension','Only sauts is straight underlined.')
    r('$s$ (auquel cas','$s$, (auquel cas','flatness parenthesis','A comma occurs before the parenthesis.')
    r('« commute avec le changement de base au',"``\\uline{commute avec le changement de base au}",'last line','The quote is ordinary double and the phrase is underlined through the page break.')
    if tree=='fr':
        r('de $\\operatorname{Pic}(X\\times_SS\'/S\')$.','de $\\operatorname{Pic}(X\\times_SS\'/S\')$).','theorem parenthesis','Close the parenthetical i. e. clause opened two lines earlier; Pic already has its own inner parentheses.','misprint of the original')
    upright_page(rel,layer,'232-153')
event('232-4.3','targeted proof check','The universal coherent module Q of p. 152 represents sections of L by Hom(Q,O). For each integral fibre, a section is regular exactly when nonzero; the corresponding linear functional on Q tensor k is then surjective. Nakayama converts this to local surjectivity Q to O. Dividing by base units and gluing yields invertible quotients of Q, represented by P(Q), compatibly with every base change. This proves 4.3 given the cohomology-module existence input. The uniqueness of Q is read with that preceding universal construction; the projective bundle alone would not determine Q, since tensoring by a base line bundle preserves its projectivization. The printed numbering jumps from 4.1 to 4.3 and is preserved.','232, p. 153, first paragraph and theorem 4.3')
event('232-4.4','targeted proof check','A section of X/S identifies each Picard class with a line bundle by 2.1, so 4.3 represents its divisor fibre by P(Q). The argument is local when the section exists locally. For projective flat X/S with integral geometric fibres, finite locally free quasi-sections locally on the base permit finite-flat descent; the appropriate norm of a relatively ample line bundle supplies the descended ample polarization, giving a projective representing morphism. Existence of the quasi-section and the finite-flat effectiveness/ample-norm descent theorem are background inputs, not independent proofs here.','232, p. 153, corollary 4.4 and paragraph following')
event('232-4.5-flatness','independent re-proof','Work locally at s with a minimal presentation A^r onto Q, where r=dim Q tensor k. If r=0, Nakayama gives Q=0 nearby and both assertions hold. Otherwise P(Q) is a closed subscheme of P^(r-1)_A with the entire special fibre. If P(Q) is A-flat at all points of that fibre, tensoring its ideal sequence with k shows that the ideal has zero fibre; Nakayama makes it zero near the special fibre. Properness of ambient projective space lets one shrink the base to make that ideal zero everywhere. Every degree-one relation then vanishes as a section of O(1), hence is zero; Q is free. Conversely, free Q gives projective space, which is smooth and flat. The final base-change equivalence continues on p. 154. The possibility of jumping dimensions is not interpreted as an iff criterion on nonreduced bases.','232, p. 153, remarque 4.5')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='232-153')
record_page('232',153,'Compared both French layers, entry lines 510-559, with scan leaf 12 at 400 dpi and three enlarged bands. Read the quotient-to-projectivization argument, theorem 4.3, corollary 4.4 and the start of 4.5 through the final underlined clause.\n\nRestored numeric 0, Gothic Q, ordinary P, wavy functor names, short arrows, uppercase attribution, exact prose emphasis and punctuation. Preserved the printed numbering and the missing closing parenthesis in the diplomatic layer; corrected French closes the parenthetical clause. Rechecked the projective-bundle representation from the universal section module, separated the descent inputs from the direct argument, and independently proved the equivalence between local freeness of Q and flatness of its projectivization at the fibre.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
