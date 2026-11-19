from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/232.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'232-145',line,'1, (1.6)-(1.8)',
                'Scan leaf 4 at 400 dpi, all three enlarged bands and the initial P(T-prime) detail: '+why,kind=kind,count=count)
    r(r'\mathfrak M',r'(\mathfrak M)','two covering-class signs','The Gothic class letter is parenthesized.',count=2)
    r("dans $P(T'')$. [N.B. --","dans $P(T'')$.\n\n[N. B. -",'N. B. paragraph','The bracketed note begins a new indented paragraph, uses spaced initials and a short dash.','structure')
    r('4(a).]','4 (a).]','reference in N. B.','A space separates 4 and (a).')
    r("sur $T$ fixé\n(toujours","sur $T$ fixé,\n(toujours",'varying-cover sentence','The print has a comma after fixé.')
    r(r'(\mathfrak M)$), les',r'(\mathfrak M)$) les','varying-cover sentence','There is no comma after the parenthesis.')
    r(r"\varinjlim_{T'}",r"\varinjlim\limits_{T'}",'(1.6)','The cover index is directly beneath the limit arrow.')
    r(r'(\mathrm{Sch})/S',r'(\text{\uwave{Sch}})/S','base category','Sch has a wavy underline inside the parentheses.')
    for phrase in ['foncteur de Picard relatif','groupe de Picard relatif']:
        r(r'\emph{'+phrase+'}',r'\uline{'+phrase+'}','Picard definitions','The words are straight underlined.')
    r(r'\operatorname{Pic}_{X/S}',r'\mathop{\text{\uwave{Pic}}}\nolimits_{X/S}','four unprimed Picard functors','The functor names have wavy underlines.',count=4)
    r(r"\operatorname{Pic}'_{X/S}",r"\mathop{\text{\uwave{Pic}}}\nolimits'_{X/S}",'two primed Picard functors','These functor names also have wavy underlines.',count=2)
    r(r'\simeq',r'\overset{\sim}{\to}','(1.7)','The bijection is printed as a short right arrow with tilde above it.')
    r(r'\longrightarrow',r'\to','five morphisms','The arrows are short.',count=5)
    r(r'\xrightarrow{\sim}',r'\overset{\sim}{\to}','(1.8)','The isomorphism uses a short right arrow with tilde above.')
    r("qu'on vient\nd'expliciter) définissent","qu'on vient\nd'expliciter), définissent",'equality of representatives','The print has a comma after the parenthesis.')
    r('introduit plus haut ;','introduit plus haut,','comparison with restricted functor','The print has a comma after haut.')
    r('définit un isomorphisme',r'définit un \uline{isomorphisme}','before (1.8)','Only isomorphisme is straight underlined.')
    r("vient d'expliciter on remplace","vient d'expliciter, on remplace",'last sentence','The print has a comma after expliciter.')
    if tree=='fr':
        old="forment un\nsystème inductif (quand l'ensemble des $T'$ est muni du préordre défini par la\ndomination)"
        new="forment un\ndiagramme (indexé par l'opposée de la catégorie des $T'$ sur $T$ et des\nmorphismes au-dessus de $T$)"
        r(old,new,'indexing of (1.6)','For a nonseparated presheaf, two morphisms of domination can induce different maps on the raw subsets H-bar-zero. For P=Pic, T=Spec k and T-prime=P1, O(1) belongs to H-bar-zero but identity and a degree-two self-map pull it back to O(1) and O(2). Thus the raw sets do not canonically form a diagram over the domination preorder. Keeping all cover morphisms, in the contravariant direction, gives the colimit of local-equivalence classes used immediately below.','misprint of the original')
    upright_page(rel,layer,'232-145')
event('232-1.6-preorder','refuted, with the refined statement id 232-1.6-cover-category','The raw H-bar-zero subsets do not in general have transition maps determined only by the domination preorder. Let P(T)=Pic(T), base Spec k, and cover U=P^1_k. The class O(1) belongs to H-bar-zero because its two pullbacks become trivial on an affine covering of U times U. The identity of U and the finite flat degree-two map [x:y] maps to [x^2:y^2] give the same relation U dominates U but pull O(1) back to O(1) and O(2), which are unequal. Corrected French indexes the diagram by the opposite category of covers and all morphisms over T.','232, p. 145, text before (1.6)')
event('232-1.6-cover-category','targeted proof check','Pullback along each map V to U over T takes locally matching elements to locally matching elements, so the raw sets form a contravariant diagram on the cover category. Its colimit identifies exactly pairs that agree after an fpqc cover of U times_T V. One direction is immediate from such a common refinement; for the other, each diagram identification is locally equal on the product by the defining H-bar-zero condition, and finite chains combine by base change and composition of covers. This gives the representative/equivalence description printed below (1.7) and resolves the preorder ambiguity. The usual associated-sheaf gluing theorem is the remaining background input.','232, p. 145, (1.6) and representative description')
event('232-1.7','targeted proof check','Covers of a T-scheme viewed over S are the same covers used for the base-changed family X times_S T over T. The representative line bundles and their common-refinement equivalence relations therefore agree. Evaluating the relative Picard functor at T gives the relative Picard group of the base-changed family, as in (1.7).','232, p. 145, definition and (1.7)')
event('232-1.8','targeted proof check','The map from absolute Picard classes to the restricted relative group is locally surjective by the definition of R^1 f_* and its sheafification, and two source classes with the same image are locally equal. Thus it is a local equivalence, so applying the finer associated-sheaf construction gives the isomorphism (1.8). This checks the sheafification mechanism; the general topology and size conventions are carried as background. The appeal to 2.3 continues on the next page and is not used before its hypotheses are read.','232, p. 145, comparison paragraph and (1.8)')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='232-145')
record_page('232',145,'Compared both French layers, entry lines 101-152, with scan leaf 4 at 400 dpi, all three enlarged bands and a separate crop confirming the prime in the first P(T prime). Read the H-bar-zero definition, N. B., (1.6), Picard definitions and (1.7), the complete representative/equivalence paragraph and (1.8), and the final sentence up to its page break.\n\nRestored class parentheses, the note paragraph and punctuation, lower limit index, wavy category and Picard-functor underlines, straight prose emphasis, short arrows and the tilde-over-arrow bijections. All H-bars and the final S-one-prime are retained after inspection. A mathematical correction replaces the preorder indexing of raw H-bar-zero sets by the opposite category of covers and their morphisms. The explicit Pic(P1) example shows why the raw maps depend on the morphism, while the categorical colimit gives the intended local-equivalence classes. Checked (1.7) and the local-equivalence mechanism of (1.8), with the general sheafification inputs separately identified.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
