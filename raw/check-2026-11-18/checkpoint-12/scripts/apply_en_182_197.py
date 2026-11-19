from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-197'
def ch(old,new,where,why,kind='terminology'):
    replace(rel,old,new,'English',page,where,'Theorem 2 and corollaries',
      'French 182-197 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands: '+why,kind=kind)
align_math(rel,'en','182',197,[(i,i) for i in range(38)],(38,38))
ch('Serre [4]','SERRE [4]','opening sentence','Restore printed author capitals.',kind='structure')
ch('The $\\symup{R^{q}f_{*}(F)}$ are\ncoherent sheaves on $\\symup{Y}$ (which is a special case of Theorem 1), and the natural\nhomomorphisms',
   '\\uline{The} $\\symup{R^{q}f_{*}(F)}$ \\uline{are\ncoherent sheaves on} $\\symup{Y}$ (which is a special case of Theorem 1), \\uline{and the natural\nhomomorphisms}',
   'Theorem 2 statement','Restore the exact emphasis including the exclusion of the parenthesis.')
ch('\nare isomorphisms.','\n\\uline{are isomorphisms}.','Theorem 2 conclusion','Restore source underlining.')
ch('There are canonical isomorphisms\n$\\symup{\\overline{R^{q}f_{*}(F)}=R^{q}\\overline f_{*}(\\overline F)}$',
   '\\uline{There are canonical isomorphisms}:\n$\\symup{\\overline{R^{q}f_{*}(F)}=R^{q}\\overline f_{*}(\\overline F)}$.',
   'Corollary 1','Restore the source inline identity, colon and final period; the formula alignment already changed display to inline.',kind='structure')
ch('functions,”','functions”,','paragraph after Corollary 1','Restore quotation punctuation.',kind='structure')
ch('theorem.”','theorem”.','paragraph after Corollary 1','Restore quotation punctuation.',kind='structure')
ch(r'(\textit{ii})','(ii)','reference to Theorem 1','Restore the roman reference marker.',kind='structure')
ch('finite-type $\\symup{A}$-modules', '$\\symup{A}$-modules of finite type','Corollary 2','Use the glossary rendering module of finite type (SGA English glossary row module de type fini).')
ch('a finite-type $\\symup{A}$-module','a module of finite type over $\\symup{A}$','Corollary 3','Use the same module of finite type terminology.')
for number in [2,3]:
    text,_,_=page_text(rel,197)
    head=r'\result{COROLLARY}{'+str(number)+'} '
    body=text.split(head,1)[1].split('\n\n',1)[0]
    ch(body,underline_prose(body),'Corollary '+str(number),'Restore underlining of the statement prose, excluding mathematical symbols.')
ch('with which convention\n','so that\n','functoriality of completion','Moyennant quoi expresses the consequence of the morphism construction, with no added convention.',kind='translation')
ch('preceding Corollaries 2 and 3 then give\n','preceding Corollaries 2 and 3 then give:\n','last display introduction','Restore the printed colon.',kind='structure')
record_translation_page('en','182',197,rel,
    'Read Theorem 2, Corollaries 1–3, the q=0 discussion and the complete-base consequence. Approved all 38 formula correspondences; Corollary 1 is inline in the print and sheaf Hom has wavy underlining. Restored all statement emphasis and punctuation and unified module of finite type terminology. Checked that the author distinguishes the trivial q=0 case of Theorem 1(ii) from the last step of the descending induction in Theorem 2.',(182,238))
event('en-182-Theorem2','carried as background without fault found',
    'Read the theorem of formal functions and the stated descending-induction argument without replacing it by an independent proof. The completion is on the whole higher direct image, and the projective-limit expression retains f_n* and F_n.',
    '182, p. 197, Theorem 2')
event('en-182-Theorem2-Cor1','targeted proof check',
    'With Theorems 1(ii) and 2 as hypotheses, both sides identify canonically with the same projective limit R^q f_n* F_n; composing these canonical isomorphisms gives the displayed identity. This checks the corollary, not its two input theorems.',
    '182, p. 197, Corollary 1')
event('en-182-Theorem2-Cor2','targeted proof check',
    'Over affine Y, the higher direct-image coherent module has global sections H^q(X,F), by affine acyclicity and Leray. Its J-adic completion gives the formal cohomology by the preceding comparison; finiteness is the coherence assertion on the affine base.',
    '182, p. 197, Corollary 2')
event('en-182-Theorem2-Cor3','targeted proof check',
    'Apply Corollary 2 in degree zero to coherent sheaf Hom(F,G). Locally finite presentation of F and flatness of Noetherian completion identify completed sheaf Hom with sheaf Hom of the completions. Taking sections gives the stated completed Hom module. When A is already complete, its finite modules are complete, giving the two concluding identities.',
    '182, p. 197, Corollary 3 and final paragraph')
update()
