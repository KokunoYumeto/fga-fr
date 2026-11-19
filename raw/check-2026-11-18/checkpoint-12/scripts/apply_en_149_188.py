from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-188'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'Theorem 4 / formulas (7.2)–(7.5)',
      'French 149-188 and the personally inspected full 400-dpi page and enlarged top, middle and bottom bands: '+why,kind=kind,count=count)
ch('\\footnote{The printed text has $f_{*}(\\xi^{m,m})$. Since\n$\\xi^{m,m}\\in H^{m}(X,\\Omega_X^{m})$ and both sides belong to\n$H^{m}(Y,\\Omega_Y^{m})$, the required map is $f^{*}$.}', '',
   'after (7.4 bis)','Remove the unprinted editorial explanation; keep the justified corrected f^* in the formula and its separate record.',kind='structure')
align_math(rel,'en','149',188,[(i,i) for i in range(23)],(23,23))
ch('transposition gives a homomorphism of vector\nspaces','one obtains by transposition a homomorphism of vector\nspaces:',
   'before (7.3)','Restore on obtient and the source colon.')
ch('We saw in Section 4','One has seen in no. 4','after (7.3)','Preserve impersonal on and the source no. reference form.')
ch('following special case.','following special case:','before Theorem 4','Restore the colon introducing the theorem.',kind='structure')
ch('the fundamental element in $\\symup{H^{m}(Y,\\underline{\\Omega}_Y^{m})}$. For nonsingular projective\nvarieties this gives a new definition of the cohomology class associated with',
   'the fundamental element in $\\symup{H^{m}(Y,\\underline{\\Omega}_Y^{m})}$, and, for nonsingular projective\nvarieties, this formula gives a new definition of the cohomology class associated with',
   'after (7.4 bis)','Keep the source explanatory period whole and retain the formula as the subject.',kind='structure')
ch('To prove Theorem 4, Theorem 3 lets us interpret the transpose of the\nhomomorphism',
   'To prove Theorem 4, one interprets, using Theorem 3, the transpose of the\nhomomorphism',
   'proof','Restore impersonal on interprète.')
ch('already in Section 4','already in no. 4','last paragraph','Retain the source no. reference form.')
ch('formulated---and in fact hold---for','formulated, and in fact hold, for',
   'last paragraph','The printed parenthesis is delimited by commas, not dashes.',kind='structure')
for start,end in [(r'\result{THEOREM}{4} ','\n\\begin{equation}'),('where the right-hand side','\n\n')]:
    t=page_text(rel,188)[0]
    if start.startswith('where'):
        old=start+t.split(start,1)[1].split(end,1)[0]
    else:
        old=t.split(start,1)[1].split(end,1)[0]
    ch(old,underline_prose(old),'Theorem 4 assertion','Restore the printed underlined assertion prose.')
record_translation_page('en','149',188,rel,
    'Read the pullback and transpose definitions, Theorem 4, its equivalent (7.4 bis), and the proof through the continuing last sentence. Approved 23 mathematical correspondences, restoring underlined differentials, directed isomorphisms and the absence of added display punctuation. Kept the existing corrected f^* in (7.4 bis), removed its unprinted editorial footnote, and restored assertion underlining, impersonal register, reference abbreviations and source sentence punctuation.',(987,1048))
event('en-149-7.4bis','used and rechecked in this run',
    'Checked the equivalence with (7.4): adjointness gives <xi,f_*1_Y>=<f^*xi,1_Y>, and the normalized fundamental element epsilon_Y identifies the last top-degree class with its trace times epsilon_Y. The right side must therefore be f^*, from X to Y; the printed f_* is a domain/codomain error. This checks the correction and the stated equivalence, not every local compatibility used to prove Theorem 4.',
    '149, p. 188, (7.4) and (7.4 bis)')
event('en-149-theorem4','carried as background without fault found',
    'Read the theorem and the duality-based argument, checking the n-m indices, middle contravariant Ext arrow and identity endomorphism at the right of (7.5). The local compatibility identifying that identity with the fundamental cycle class is carried as background here; it was not independently re-proved in this translation pass.',
    '149, p. 188, Theorem 4 and (7.5)')
update()
