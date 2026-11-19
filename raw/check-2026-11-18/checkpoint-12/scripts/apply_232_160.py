from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/232.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'232-160',line,'6.6-6.8',
                'Scan leaf 19 at 400 dpi and three enlarged bands: '+why,kind=kind,count=count)
    notes=list(footnotes(page_text(rel,160)[0])); assert len(notes)==2
    for note in notes:
        r('\\footnote{'+note[2]+'}','','remarks 6.7-6.8','No editorial footnote is printed; later errata remain separate.','structure')
    r('disons simple sur $k$,','disons régulier,','6.8 opening hypothesis','The print says régulier. Restore it in both expose layers instead of merging the later erratum.')
    r("correspondant\n\\[\n\\operatorname{Pic}_{X/k}\\longrightarrow\\operatorname{Pic}_{X'/k}\n\\]\nest", "correspondant\n$\\text{\\uwave{Pic}}_{X/k}\\longrightarrow\\text{\\uwave{Pic}}_{X'/k}$ est",'opening functorial map','The morphism is inline and both Pic names are wavy underlined.','structure')
    r("que $\\operatorname{Pic}_{X'/k}$ est représentable", "que $\\text{\\uwave{Pic}}_{X'/k}$ est représentable",'known representable functor','Pic is wavy underlined.')
    r('$\\operatorname{Pic}_{X/k}$ aux préschémas réduits', '$\\text{\\uwave{Pic}}_{X/k}$ aux préschémas réduits','restricted functor','Pic is wavy underlined.')
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}','eight scheme names','All remaining Pic symbols have straight scheme underlines.',count=8)
    r("conjecturer que\n\\[\n\\underline{\\operatorname{Pic}}_{X/k}\\longrightarrow\\underline{\\operatorname{Pic}}_{X'/k}\n\\]\nest", "conjecturer que\n$\\underline{\\operatorname{Pic}}_{X/k}\\longrightarrow\\underline{\\operatorname{Pic}}_{X'/k}$ est",'6.7 conjectural affine map','This scheme morphism is inline.','structure')
    r('réduits ($X$','réduits, ($X$','opening parenthesis','There is a comma before the parenthesis.')
    r('Chevalley','CHEVALLEY','attribution','The surname is uppercase.')
    r('Seshadri','SESHADRI','attribution','The surname is uppercase.')
    r(r'\result{REMARQUE}',r'\result{\uline{Remarque}}','two remark headings','The headings are mixed case and straight underlined.',count=2)
    r('est un morphisme affine,','est un morphisme \\uline{affine},','6.7 conjecture','Only affine is straight underlined.')
    r('Néron--Severi','Néron-Severi','two group names','The compound uses a short hyphen.',count=2)
    r('« voisinages\ninfinitésimaux »',"``voisinages\ninfinitésimaux''",'6.8 infinitesimal neighborhoods','The print uses ordinary double quotation marks.')
    r(r'\geq',r'\geqslant','two dimension bounds','The lower stroke in each greater-or-equal sign is slanted.',count=2)
    r('Mumford','MUMFORD','local divisor-class conjecture','The surname is uppercase.')
    r(r'\longrightarrow',r'\to','four morphisms','All arrows are short.',count=4)
    upright_page(rel,layer,'232-160')
event('232-6.6-reduced-tests','targeted proof check','Every morphism from a reduced scheme T to a scheme P kills the nilradical of O_P and hence factors uniquely through P_red. Thus restricting a representable Picard functor to reduced tests sees precisely the reduced Picard scheme and cannot detect its nilpotent structure. This checks the logical distinction made in the remark. The historical constructions by Chevalley and Seshadri are recorded as cited background, and the proposed nonflat descent theorem retains its conjectural status.','232, p. 160, continuation of remarque 6.6')
event('232-6.7','targeted proof check','Checked the stated consequence conditionally on the proposed affine Picard morphism. The inverse image of the target identity component is affine over that finite-type component and is locally of finite type, hence of finite type; it has finitely many connected components. Its component classes are exactly the kernel on Neron-Severi groups after quotient by the source identity component, so that kernel is finite and therefore torsion. The finite-type identity-component theorem is background. Affineness itself is not proved here and remains a conjecture in the expose; the later erratum is not merged.','232, p. 160, remarque 6.7')
event('232-6.8-hyperplane-comparison','carried as background without fault found','The announced comparison with sufficiently thick infinitesimal hyperplane neighborhoods is a formal Lefschetz/Picard theorem requiring algebraization, depth or cohomological vanishing, and control of algebraically trivial classes in dimension three. It is not proved on this page. The original regular hypothesis is restored in both expose layers; its later smoothness correction remains in the separate erratum. The dimensions at least four and at least three, and the restriction to inverse images of Neron-Severi torsion in the latter case, are checked against the image.','232, p. 160, remarque 6.8, first part')
event('232-6.8-local-class-group','carried as background without fault found','The closing sentence begins an announced application of formal geometry and nilpotent Picard schemes to a complete normal two-dimensional local ring in equal characteristic. The sentence continues on p. 161, so its precise group-scheme and residue-field qualifications are reserved for that continuation. No proof of this announcement is claimed here.','232, p. 160, remarque 6.8, final sentence fragment')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='232-160')
record_page('232',160,'Compared both French layers, entry lines 842-895, with scan leaf 19 at 400 dpi and three enlarged bands. Read the end of remark 6.6, all of 6.7 and 6.8 through the page-ending local-class-group sentence fragment.\n\nRestored four wavy functors and eight straight-underlined schemes, two inline morphisms, headings, exact names, comma, affine emphasis, short hyphens and arrows, ordinary quotes and the slanted greater-or-equal signs. Removed two unprinted footnotes and restored régulier in place of the merged later erratum. Checked the reduced-test factorization and the conditional finite-kernel consequence of the affine-morphism conjecture. Kept the formal Lefschetz and local-class-group announcements explicitly background. No mathematical difference between the two expose layers is introduced here.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
