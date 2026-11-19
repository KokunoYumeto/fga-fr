from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-201'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'section 5, Proposition 1 and Theorem 7',
      'French 182-201 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands: '+why,kind=kind,count=count)
ch('assumed flat over $Y$', '$F$ being assumed flat over $Y$', 'opening flatness hypothesis','Retain the repeated formula F with the source hypothesis, in accord with the formula standard.')
ch('if $F$ is\nfiltered along', 'if we filter $F$\nalong', 'opening filtration argument','The source has si nous filtrons. Restore the authors’ we required by the register standard.')
old='homomorphism\n\\[\n  u:F|V\\longrightarrow G|V,\n  \\qquad V=f^{-1}(U),\n\\]\nwhere $U$ is a neighborhood of $y$.'
new='homomorphism\n$u:F|V\\longrightarrow G|V$, where $V=f^{-1}(U)$ is the inverse image of a\nneighborhood $U$ of $y$.'
ch(old,new,'Theorem 7 conclusion','The source has two inline formulas separated by où and explicitly describes V as the inverse image of a neighborhood U.',kind='structure')
align_math(rel,'en','182',201,[(i,i) for i in range(60)],(60,60))
ch('the following consequence.', 'the following consequence:', 'Proposition 1 introduction','Restore the colon introducing the result.',kind='structure')
ch('$\\symup{H^1\\bigl(X_y,\\Homsh_{O_X}(F_y,G_y)\\bigr)=0}$\nThen',
   '$\\symup{H^1\\bigl(X_y,\\Homsh_{O_X}(F_y,G_y)\\bigr)=0}$,\nthen',
   'Theorem 7 hypothesis and conclusion','Restore the source comma and continuous conditional sentence after making the vanishing formula inline.',kind='structure')
ch('respectively a monomorphism', 'resp. a monomorphism','Theorem 7 corollary','Keep the printed abbreviation resp. under the register standard.')
for heading in [r'\result{PROPOSITION}{1} ',r'\result{THEOREM}{7} ']:
    text,_,_=page_text(rel,201);body=text.split(heading,1)[1].split('\n\n',1)[0]
    newbody=underline_prose(body).replace(r'\uline{where}', 'where')
    ch(body,newbody,'Proposition 1 or Theorem 7 statement','Restore printed prose emphasis while leaving formulas and the unaccented where outside the underline.')
text,_,_=page_text(rel,201);body=text.split(r'\result{COROLLARY}{} ',1)[1].split('\n\n',1)[0]
pre,rest=body.split('(resp. a monomorphism,\nan epimorphism)',1)
ch(body,underline_prose(pre)+'(resp. a monomorphism,\nan epimorphism)'+underline_prose(rest),
   'Theorem 7 corollary','Restore the underlined main assertion while preserving the unaccented parenthetical variants.')
record_translation_page('en','182',201,rel,
    'Read the flatness filtration, formal-functions formula, Proposition 1, Theorem 7 and its corollary. Approved all 60 math correspondences after restoring repeated F and separating the two inline formulas in Theorem 7. The English already uses X_y, as required by the corrected French, in place of the printed F_y misprint in the formal-functions display. Restored the French completion bar, residue-field symbol, Hom typography and inline statement formulas. The theorem’s O_X scalar notation agrees with the corrected French; no extra explanation is inserted.',(381,439))
event('en-182-Proposition1','targeted proof check',
    'Checked the deduction from flatness and formal functions. Each successive quotient m^nF/m^(n+1)F is a finite direct sum of F_y. H^q(F_y)=0 therefore gives H^q(F/m^nF)=0 by induction and surjective transition maps on H^(q-1). Formal functions and faithful completion of a finite local module give vanishing of (R^q f_*F)_y, hence nearby by coherence. The inverse limit surjects to each H^(q-1)(F/m^nF); the latter is killed by m^n, so this surjection descends from the completion to the uncompleted finite module modulo m^n.',
    '182, p. 201, section 5, Proposition 1')
event('en-182-Theorem7','targeted proof check',
    'Checked the stated application of Proposition 1 to the locally free coherent Hom(F,G), which is flat over Y. With q=1 its fiber H^1 vanishing makes the map from the stalk of f_*Hom(F,G) onto the fiber Hom group surjective. A preimage is represented on a neighborhood of y and hence defines the claimed homomorphism over its inverse image.',
    '182, p. 201, Theorem 7')
event('en-182-Theorem7-Corollary','targeted proof check',
    'Checked extension of the three properties. Fiberwise surjectivity eliminates the coherent cokernel along the fiber by Nakayama. For a fiberwise monomorphism, flatness identifies the m_y-adic graded pieces with tensor products of the fiber map; they are injective. Krull intersection at each point of the fiber then kills the kernel. Properness permits removal of the closed images of these coherent supports, yielding the required neighborhood; an isomorphism combines the two cases.',
    '182, p. 201, corollary to Theorem 7')
update()
