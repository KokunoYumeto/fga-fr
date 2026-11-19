from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-170'
align_math(rel,'en','149',170,[(i,i) for i in range(24)],(35,30))
def ch(old,new,where,why,kind='translation'):
    replace(rel,old,new,'English',page,where,'section 1',
      'French 149-170 and the personally inspected full 400-dpi scan and three enlarged page bands: '+why,kind=kind)
old=page_text(rel,170)[0].split(r'\result{PROPOSITION}{2} ',1)[1].rstrip()
new=r'''\uline{If} $\symup{A}$ \uline{is, in a neighborhood of} $\symup{x}$, \uline{isomorphic to the
cokernel of a homomorphism} $\symup{\Osh^{m}\longrightarrow\Osh^{n}}$, \uline{then} (1.7) \uline{is an isomorphism for every} $\symup{p}$. \uline{This holds in particular if}
$\symup{A}$ \uline{is a coherent} $\symup{\Osh}$-\uline{Module} [3].'''
ch(old,new,'Proposition 2',
   'The French reading withdrew the supplied Ext/pseudocoherence expansion. Restore the printed finite-presentation Hom statement with reference (1.7), retaining its superfluous p rather than making the unsupported reference change to (1.8). The extra resolution hypotheses, degree-zero explanatory sentence and editorial footnote have no counterpart in the retained French. The finite-presentation Hom comparison is valid; higher Ext requires additional hypotheses. Source emphasis and formula typography are included in this restoration.')
for old in [
 r'''For every $\symup{\Osh}$-Module $\symup{A}$, there exists a
cohomological spectral functor on $\symup{\Ccat^{\Osh}}$ converging to the graded functor
$\symup{\bigl(\operatorname{Ext}_{\Osh}^{*}(X;A,B)\bigr)}$, whose initial term is''',
 r'''If $\symup{A}$ is locally isomorphic to $\symup{\Osh^{n}}$, then there are
canonical isomorphisms''',
 'In particular, there is\na canonical isomorphism']:
    ch(old,underline_prose(old),'Proposition 1 / Corollary 1 emphasis',
       'The corresponding assertion prose is underlined in the French. Apply the all/register emphasis rule.',kind='terminology')
ch('From it one obtains edge homomorphisms',r'From it one obtains \fquote{\uline{edge-homomorphisms}}',
   'after (1.4)','The borrowed term is quoted and underlined, with a short hyphen, in the source.',kind='terminology')
ch('(given by edge homomorphisms','(given by edge-homomorphisms','after (1.5)',
   'The repeated source term keeps its hyphen and is not emphasized at this occurrence.',kind='terminology')
record_translation_page('en','149',170,rel,
    'Read every sentence and all six numbered displays plus the restriction identity. Matched the first 24 math spans directly; restored Proposition 2 as a complete source-based passage, reversing the supplied extended Ext/pseudocoherence statement and removing its explanatory footnote. The source reference is (1.7), and the redundant printed p is retained consistently with both French layers. Restored underlined statement prose and the locally quoted edge-homomorphisms. The hypotheses, cohomological degrees, arrow directions, stalk indices and reference [3] were checked from the image.',(59,115))
event('en-149-proposition2-Hom','targeted proof check',
    'Rechecked the degree-zero claim while withdrawing the translation expansion: from a local finite presentation O^m -> O^n -> A -> 0, Hom(A,B) is the kernel of B^n -> B^m. Taking stalks is exact and commutes with these finite products, giving (1.7). This does not establish the all-degree version of (1.8) under only finite presentation. The literal extraneous p stays in the historical wording; the caveat belongs to the notes.',
    '149, p. 170, Proposition 2')
update()
