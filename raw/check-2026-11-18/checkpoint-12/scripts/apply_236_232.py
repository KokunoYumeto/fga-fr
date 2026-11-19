from audit_utils import *
from collections import Counter
import csv
dq=chr(96)*2
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'236-232',line,'2.1(ii), 2.2, 2.3, 2.4',
                'Scan leaf 13 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,232)
    for a,b,body in reversed(list(footnotes(s))):
        r(s[a:b],'','two later-erratum footnotes','The exposé has neither footnote. The later erratum remains in its separate printed section.','structure')
    r("droite\naffine privée de l'origine","droite\naffine",'alternative proof','The exposé says only droite affine. The later erratum is not merged into either French layer.')
    r(r'X[t,t^{-1}]',r'X[t]','alternative proof, polynomial extension','The exposé prints X[t]; the Laurent extension belongs to the separate erratum.')
    r("dans $\\operatorname{Pic}_{X/k}^\\tau$ est constant",
      "dans $\\operatorname{Pic}_{X/S}^\\tau$ est constant",
      'alternative proof, Picard base','The printed denominator in this particular occurrence is S.')
    r('famille de quadriques','famille de quadratiques','opening counterexample','The print spells the substantive quadratiques; it is retained as written.')
    for a,b in [
        ('« codimension $\\leq2$ »',dq+"codimension $\\leq2$''"),
        ('« codimension\n$\\leq1$ »',dq+"codimension $\\leq1$''"),
        ('« normal »',dq+"normal''"),
        ("« critères d'équivalence »",dq+"critères d'équivalence''"),
        ('« égale\ncaractéristique »',dq+"égale caractéristique''")
    ]:
        r(a,b,'quoted prose','The print uses ordinary double quotation marks.')
    r('i.e.','i. e.','two explanatory abbreviations','The print spaces the two components.',count=2)
    r(r'\mathbf P',r'P','two projective-space symbols','Both P letters are ordinary upright letters without bold or underline.',count=2)
    r(r'\leq',r'\leqslant','two codimension signs','The lower strokes are slanted in the enlarged image.',count=2)
    r(r'\geq',r'\geqslant','dimension inequality','The lower stroke is slanted in the enlarged image.')
    r('telles que\n\\[\n\\operatorname{Pic}_{X/k}^\\tau\\longrightarrow\n\\prod_i\\operatorname{Pic}_{Y_i/k}^\\tau\n\\]\nsoit',
      'telles que $\\operatorname{Pic}_{X/k}^\\tau\\to\\prod\\limits_i\\operatorname{Pic}_{Y_i/k}^\\tau$ soit',
      'restriction monomorphism','The morphism is inline; the product index is below its sign and the arrow is short.','structure')
    r(r'\longrightarrow',r'\to','two corollary structure arrows','Both arrows are short.',count=2)
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}',
      'twelve Picard schemes','All twelve scheme names have straight underlines.',count=12)
    r('Chevalley--Borel','CHEVALLEY-BOREL','structure theorem attribution','Both names are in capitals and joined by a short dash.')
    if tree=='fr':
        r("dans $\\underline{\\operatorname{Pic}}_{X/S}^\\tau$ est constant",
          "dans $\\underline{\\operatorname{Pic}}_{X/k}^\\tau$ est constant",
          'alternative proof, Picard base','Part (ii) fixes the base field k. The preceding three Picard names are over k, and S is undefined in this proof. This corrects the inconsistent denominator while leaving the separate affine-line erratum unmerged.','misprint of the original')
    upright_page(rel,layer,'236-232')
    # The already viewed preceding-page inequalities have the same slanted bars.
    replace(rel,r'\leq',r'\leqslant',layer,'236-231','remark 2.2, two codimension signs','2.2',
            'Scan leaf 12 at 400 dpi, enlarged bottom band, compared again with leaf 13: both printed lower inequality strokes are slanted.',count=2)
event('236-2.2-quadric-degeneration','targeted proof check',
      'Over k[[t]] with characteristic not 2, take the quadric xy=z^2-t^2 w^2 in projective 3-space. The generic fibre is a split smooth quadric and the special fibre is the normal quadric cone. A generic ruling bundle O(1,0) has twisted Euler polynomial (n+2)(n+1). An invertible sheaf on the cone is O(m), with polynomial (n+m+1)^2. The linear coefficients cannot agree for integer m, so the generic ruling bundle cannot extend in this flat family. This verifies the failure asserted for merely normal fibres. The standard Picard calculation for a projective quadric cone is the background input in this explicit test.',
      '236, p. 232, completion of remark 2.2')
event('236-2.1-ii-curve-restriction','carried as background without fault found',
      'Read the Chow reduction, smooth-curve sections and the monomorphism from Pic tau into a product of curve Pic tau schemes, with the ordinary projective-space P and all subscripts checked against the image. On identity components a finite-type group monomorphism is a closed immersion, so the stated restriction criterion would imply properness. The Chow/Bertini/equivalence criteria and finite-type group-immersion theorem are the substantial inputs; they are not independently reproved here. The needed geometric base extensions are implicit in this argument.',
      '236, p. 232, proof of 2.1(ii), first route')
event('236-2.1-ii-affine-line-gap','targeted proof check',
      'The printed alternative uses A1 and X[t]. Invariance of line bundles under A1 prevents additive subgroups but does not rule out a torus: every morphism A1 to G_m is constant, since the only units of k[t] are constants, although G_m is not proper. Thus that line alone is insufficient for the claimed Chevalley-Borel reduction. The supplied source had merged the later punctured-line/Laurent erratum; both exposé layers now keep the original, with the erratum reserved for its own sequential reading. Corrected French changes only the undefined denominator S to k.',
      '236, p. 232, alternative proof of 2.1(ii)')
event('236-2.3','carried as background without fault found',
      'The closedness and properness assertions for the four loci are the corresponding deductions from 1.1 once geometric normality gives proper identity-component fibres by 2.1(ii) and separatedness of the relative Picard scheme is available. The latter separatedness is an additional valuative Picard input, not supplied by 2.1(i), whose hypotheses are smooth. The equal-characteristic restriction on sigma is correctly retained. No independent complete proof is claimed.',
      '236, p. 232, corollary 2.3')
event('236-2.4','targeted proof check',
      'A summand P^(i) in a disjoint scheme sum is open and closed. With the assumed finite type over S, it satisfies exactly the closed finite-type-part condition in 2.1(i), hence is proper. This checks the deduction conditional on 2.1(i). The final paragraph explicitly leaves properness of Pic tau for normal families as an open question; it is preserved as such.',
      '236, p. 232, corollary 2.4 and final paragraph')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='236-232')
record_page('236',232,'Compared sources/fr_printed/fr/236.tex and sources/fr/fr/236.tex, entry lines 508-563, with scan leaf 13 at 400 dpi, full page and three enlarged bands. Read the quadric degeneration, both proposed routes for 2.1(ii), 2.3, 2.4 and the final open question.\n\nRestored quadratiques, ordinary quotes, punctuation, plain projective-space P, twelve straight Picard names, CHEVALLEY-BOREL, the inline product map and slanted inequalities. The two codimension signs on the preceding already-viewed page were also corrected to slanted bars with separate rows. Removed the two unprinted erratum footnotes and restored droite affine and X[t] in both layers. Corrected French alone resolves the alternative proof denominator S to k. The affine-line route has a recorded torus gap, to be compared with the separate erratum later. Checked the normal-quadric degeneration obstruction and the immediate deduction of 2.4; identified the substantial inputs to the other arguments as background.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
