from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-173'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'(2.6)–(3.2)',
      'French 149-173 and the personally inspected full 400-dpi image and enlarged page bands: '+why,kind=kind,count=count)
align_math(rel,'en','149',173,[(i,i) for i in range(24)],(24,24))
ch('multiplicative structures. More\nprecisely, there is a pairing',
   'multiplicative structures; more\nprecisely, one has a pairing',
   'spectral sequence paragraph','Preserve the one long source sentence and the impersonal on a, as required by the register standard.')
ch('$\\symup{E(A,C)}$. At the abutment it reduces',
   '$\\symup{E(A,C)}$, which at the abutment reduces',
   'spectral sequence paragraph','The source continues the same relative clause; it does not start a new sentence.')
ch('global $\\symup{\\operatorname{Ext}}$ groups, while on the initial term it is the\npairing',
   'global $\\symup{\\operatorname{Ext}}$, and on the initial term to the\npairing',
   'spectral sequence paragraph','Retain the paired clauses of the source sentence, without the added noun groups.')
ch('local $\\symup{\\operatorname{Ext}}$ groups.','local $\\symup{\\operatorname{Ext}}$.',
   'local composition','The source leaves Ext unexpanded; do not restrict the local functor notation to groups.',kind='translation')
ch('the edge homomorphisms',r'the \fquote{edge-homomorphisms}',
   'before (2.6)','Restore the quoted source term and its short hyphen.')
ch('\\end{equation}\nand\n\\begin{equation}\\tag{2.7}',
   '\\end{equation}\n\\begin{equation}\\tag{2.7}',
   'between (2.6) and (2.7)','The two consecutive displayed formulas have no intervening prose in the source.',kind='structure')
ch('global $\\symup{\\operatorname{Ext}}$ groups in terms',
   'global $\\symup{\\operatorname{Ext}}$ in terms',
   'end of section 2','Keep the source Ext notation without an added explanatory noun.',kind='translation')
ch(r'\fsection{3}{Results in local cohomology}',
   r'\fsection{\normalfont3}{\normalfont\uline{Results in local cohomology}.}',
   'section 3 heading','Retain source emphasis and the terminal period.')
ch('For a\nvarying $\\symup{A}$-module $\\symup{M}$, we shall define functorial homomorphisms',
   'We shall define, for a\nvarying $\\symup{A}$-module $\\symup{M}$, functorial homomorphisms',
   'section 3 opening','Keep the source order of the introduction and variable-module clause under the register standard.')
ch('over the ring $\\symup{A}$. Notice also\nthat',
   'over the ring $\\symup{A}$; notice also\nthat',
   'after (3.1)','Retain the source semicolon and the single sentence.')
record_translation_page('en','149',173,rel,
    'Read the spectral-sequence compatibility paragraph and the opening construction in section 3 against French. Approved all 24 formula correspondences: the semicolon after X in (2.6), the opposite Tor arrow in (3.1), the shared underlined x subscripts and the two rightward maps in (3.2) agree with the scan. Restored the source sentence boundaries, clause order, quoted edge-homomorphisms and heading emphasis under the terminology/register standard. The compatibility claim remains background, not a new proof.',(217,276))
event('en-149-2.6-3.2','carried as background without fault found',
    'Read and compared both paragraphs and all formula fields. Ext maps toward Hom in (3.1), whereas the exterior-power tensor expression maps toward Tor; both specialized phi maps in (3.2) point right. Checked (1.4), (1.5), Proposition 1 and the four formula tags against the scan. No new proof of multiplicative spectral-sequence compatibility is claimed.',
    '149, p. 173, (2.6), (2.7), (3.1), (3.2)')
update()
