from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-266',line,'Chow comparison / 3.9 / 4a',
                'Scan leaf 19 at 400 dpi and all three enlarged bands: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,266)
    for a,b,body in list(footnotes(s)):
        r(s[a:b],'','unprinted notes','There is no footnote on the printed page. The later erratum stays in its own section.','structure')
    if tree=='fr':
        r('(tel qu', '(telle qu','agreement in opening comparison','The printed word is telle.')
        r('(telle qu','(tel qu','agreement in opening comparison','The antecedent of il is the masculine anneau, so telle is an agreement slip. Retain the supplied correction without its unprinted note.','misprint of the original')
        r(r'$\mathcal F$, ou encore de la classe',r'$\mathcal F$ et de son rang, ou encore de la classe','Chern data and Hilbert polynomial','With ordinary Chern classes, O and O plus O on projective space have identical total Chern class 1 but different Hilbert polynomials. The rank is additionally required; rank plus Chern classes determines the Chern character and hence the Hilbert polynomial.','misprint of the original')
    r("l'anneau de Chow des classes",r"\uline{l'anneau de Chow} des classes",'Chow ring term','The initial ring name is straight-underlined.')
    r("et l'anneau des classes\nde faisceaux de la variété",r"et \uline{l'anneau des classes de faisceaux} de la variété",'sheaf-class ring term','Only the ring name through faisceaux is straight-underlined.')
    r('Riemann--Roch','Riemann-Roch','theorem name','The print has a single hyphen.')
    r(r'\mathbf P',r'\mathfrak P','projective-space letters','The four projective-space letters are Gothic.',count=4)
    r(r'A=\underline{\operatorname{Quot}}',r'A=\mathop{\text{\uwave{Quot}}}\nolimits','4a functor','The functor Quot has a wavy underline.')
    r(r'\operatorname{Quot}',r'\underline{\operatorname{Quot}}','six scheme Quot signs','All six scheme signs have straight underlines.',count=6)
    r(r'\operatorname{Hilb}',r'\underline{\operatorname{Hilb}}','two scheme Hilb signs','Both Hilb scheme signs have straight underlines.',count=2)
    r(r'\longrightarrow',r'\to','base-change arrow','The printed arrow is short.')
    r(r'\underline{\operatorname{Quot}}^{P}_{',r'\underline{\operatorname{Quot}}_{','universal Quot display','There is no P superscript on the right-hand Quot sign in the print.')
    if tree=='fr':
        r(r'\underline{\operatorname{Quot}}_{(\mathcal O_',r'\underline{\operatorname{Quot}}^{P}_{(\mathcal O_','universal Quot display','The left side fixes the Hilbert polynomial P, as does the projective component under discussion. The full Quot on the printed right side ranges over all polynomials; supply the omitted P.','misprint of the original')
    r('Serre [7]','SERRE [7]','cited name','The surname is printed in capitals.')
    r('de Weil si','de WEIL si','cited question','The surname is printed in capitals.')
    r('i.e.','i. e.','relative connectedness','The abbreviation is spaced.')
    for a,b in [('« régulières »','"régulières"'),('« relativement connexes »','"relativement connexes"'),('« variétés de Chow »','"variétés de Chow"')]:
        r(a,b,'quotation marks','The printed quotation marks are ordinary double quotes.')
    r(r'\fsection{4}{Variantes}',r'\fsection{4}{\normalfont\uline{Variantes}.}','section heading','Variantes is ordinary upright and straight-underlined, followed by a period.')
    upright_page(rel,layer,'221-266')
event('221-Chern-data','refuted, with the refined statement id 221-Chern-data-rank','Under ordinary Chern-class notation, the trivial bundles O and O direct-sum O have the same total Chern class 1 but Hilbert polynomials binomial(n+r,r) and twice that polynomial. Thus Chern classes alone do not determine the Hilbert polynomial when rank varies. The corrected layer explicitly includes rank; the printed wording is retained in the diplomatic layer.','221, p. 266, opening paragraph')
event('221-Chern-data-rank','targeted refinement check','For projective r-space, K_0 is free with basis O, O(-1), ..., O(-r), whose Hilbert polynomials form a basis of the integer-valued degree-at-most-r polynomials. Thus the Hilbert polynomial determines the K_0 class. Rank plus Chern classes determines the rational Chern character; the projective-space Chow ring and Riemann-Roch give the polynomial, and torsion-freeness of K_0 makes this sufficient. This uses these standard K-theory and Riemann-Roch facts as explicit background inputs. The possible historical convention of including rank in Chern data remains for contextual review.','221, p. 266, opening paragraph')
event('221-3.9','carried as background without fault found','Read the reduction to projective space, a free ambient sheaf and the integer base, and the questions on connectedness, irreducible components and fields of definition. No answer to those historical questions is inserted. The unprinted Hartshorne erratum note is removed in both layers; the separate erratum will be read in sequence. The missing P on the displayed universal Quot is an immediate fixed-polynomial inconsistency and is repaired only in corrected French.','221, p. 266, Remark 3.9')
event('221-4a-open-support','targeted proof check','On the universal Quot scheme, intersect the support of the universal coherent quotient with the closed complement of U in the projective X. Its image in the base Quot is closed by properness. The complementary open represents precisely the quotients whose support lies in U; support commutes with these base changes for finite modules by the local Nakayama criterion. This verifies the open-subfunctor assertion under the projectivity hypotheses of 3.1. The concluding sentence continues on the next page.','221, p. 266, section 4a')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-266')
record_page('221',266,'Compared printed French entry lines 819-871 and corrected French entry lines 820-872 with scan leaf 19 at 400 dpi and all three enlarged bands. Read the Chow/K-theory comparison, all of Remark 3.9 and the first paragraph of 4a.\n\nRestored the two ring-name underlines, Gothic projective-space letters, straight scheme signs, the wavy functor sign, short arrow, capital surnames, ordinary double quotation marks, spaced abbreviation and section-heading typography. Removed unprinted agreement and Hartshorne notes. Printed French retains telle and the missing P on the universal Quot; corrected French retains tel and supplies P. Corrected French also includes rank in the Chern-data comparison, with the trivial-bundle counterexample and the refined argument recorded explicitly; the possible historical convention remains flagged for contextual review. Checked the open support condition through the proper image of the universal bad-support locus.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
