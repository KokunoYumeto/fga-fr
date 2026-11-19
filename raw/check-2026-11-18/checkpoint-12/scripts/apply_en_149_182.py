from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-182'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'Theorem 3 / Corollary / (D)',
      'French 149-182 and the personally inspected full 400-dpi page and enlarged top, middle and bottom bands: '+why,kind=kind,count=count)
align_math(rel,'en','149',182,[(i,i) for i in range(19)],(19,19))
ch('\\]\nthat is,\n\\begin{equation}', '\\]\n\\begin{equation}',
   'opening pairing','The source i.e. is part of the first display, now restored there; remove the displaced duplicate.',kind='structure')
ch('The homomorphism (5.2) is an isomorphism.',r'\uline{The homomorphism} (5.2) \uline{is an isomorphism}.',
   'Theorem 3','Restore the source emphasis, excluding the equation reference.')
ch('In particular, this recovers', 'In particular, one recovers',
   'before Corollary','The source on retrouve is impersonal.')
ch('of $\\symup{E}$. Then there are\ncanonical isomorphisms','of $\\symup{E}$; one then has\ncanonical isomorphisms:',
   'Corollary','Keep the source period whole, retain on a, and restore the colon before the display.')
t=page_text(rel,182)[0];old=t.split(r'\result{COROLLARY}{} ',1)[1].split('\n\\begin{equation}',1)[0]
ch(old,underline_prose(old),'Corollary assertion','Restore the underlined assertion prose without underlining mathematical variables.')
ch('Corollary 1 to Proposition 1.', 'Corollary 1 of Proposition 1.',
   'Corollary proof','The French corollaire 1 à la proposition 1 identifies which corollary is applied; it does not say to apply a corollary to the proposition.',kind='translation')
ch(r'\noindent\textbf{(D) The following homomorphism}',r'\noindent(D) \uline{The following homomorphism}',
   '(D) heading','Restore a normal label followed by underlined assertion prose.')
ch('induced by the pairing (5.1), is an isomorphism.',r'\uline{induced by the pairing (5.1) is an isomorphism}.',
   '(D) conclusion','The full phrase including (5.1) is underlined; the extra comma is absent.')
ch('Let us first show', 'Let us indeed show',
   'proof of Theorem 2 from (D)','The source en effet gives a reason, not a first step.',kind='translation')
ch('$\\symup{x\\in X}$. Consider the', '$\\symup{x\\in X}$; let us consider the',
   'point sheaf and canonical map','Keep the source period whole and retain the authorial considérons.')
ch('Its transpose identifies', 'its transpose identifies',
   'after (5.3 bis)','The prose continues the preceding period after the display.',kind='structure')
record_translation_page('en','149',182,rel,
    'Read the duality pairings, Theorem 3, its vector-bundle corollary, assertion (D), and the first step deriving Theorem 2. Approved all 19 mathematical correspondences, restoring the underlined differential sheaves and point sheaf, the parenthesized definition of L, displayed i.e., and source punctuation. Kept the already corrected 5.3 bis identifier. Corrected the reference to Corollary 1 of Proposition 1; restored assertion emphasis and the whole source periods. The duality proof continues on the next page.',(675,741))
event('en-149-theorem3-and-D','carried as background without fault found',
    'Read the perfect-pairing assertion and (D), with Ext in degree n-p and the dual of H^p, including the tensor factor L in (5.2 bis). Checked the contravariant direction of the map induced by O_X to the point sheaf and the L-prime factors in (5.4). The proof continues on the next page; no independent proof of duality is claimed here.',
    '149, p. 182, Theorem 3, (D), formulas (5.1) through (5.5)')
event('en-149-corollary-p182','used and rechecked in this run',
    'The locally free first argument makes the sheaf Ext of positive degree vanish, so Corollary 1 of Proposition 1 identifies the global Ext with the cohomology of the Hom sheaf, equal to the top differential sheaf tensored with the dual bundle. Applying Theorem 3 gives (5.3). Corrected the English identification of this corollary.',
    '149, p. 182, Corollary and its one-sentence proof')
update()
