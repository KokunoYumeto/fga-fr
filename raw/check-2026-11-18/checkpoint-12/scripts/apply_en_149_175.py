from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-175'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'Proposition 4 / Corollaries 1–2',
      'French 149-175 and the personally inspected full 400-dpi scan and enlarged bands: '+why,kind=kind,count=count)
note=r'''\footnote{The printed text says
“rank $n$.” Both modules of top-degree forms have rank $1$, as is also required
by the identification with $\bigwedge^{p}(J/J^{2})$ below.}'''
ch(note,'','after the ranks of top forms','This editorial footnote is not printed and is absent from the retained French text. Preserve the corrected rank-one projective assertions; retain their explanation separately in the audit.',kind='structure')
ch('is not a zero divisor.','is not a divisor of $0$.','Proposition 4 hypothesis','Retain the printed zero as a mathematical symbol under the formula standard.')
ch('of dimension $n$','of $\\dim n$','Corollary 1 dimension','The source writes dim n as one mathematical expression; avoid duplicating the word dimension.')
ch('where the prime denotes','where the symbol \\fquote{$\\prime$} denotes','dual notation','Restore the explicit quoted prime symbol in the source.')
align_math(rel,'en','149',175,[(i,i) for i in range(60)],(60,60))
ch('rank $\\symup{1}$. Thus the left-hand\nside equals','rank $\\symup{1}$, so the left-hand\nside equals',
   'proof of Corollary 1','The source keeps the two projective rank assertions and their consequence in one sentence.')
ch('$\\symup{\\operatorname{Ext}_{A}^{p}\\!\\left(A/J,\\bigwedge^{p}(J/J^{2})\\right)}$\nand therefore',
   '$\\symup{\\operatorname{Ext}_{A}^{p}\\!\\left(A/J,\\bigwedge^{p}(J/J^{2})\\right)}$,\nand therefore',
   'proof of Corollary 1','The intermediate Ext expression is inline, followed by the source comma.',kind='structure')
ch('that is, with','i.e. with','after the endomorphism display','Retain the printed abbreviation.')
ch(r'\emph{fundamental class of the ideal $\symup{J}$ in $\symup{A}$}',
   r'\uline{fundamental class} of the ideal $\symup{J}$ in $\symup{A}$',
   'fundamental class','Only fundamental class is underlined; the ideal and ambient ring are not emphasized.')
for marker,end in [(r'\result{PROPOSITION}{4} ','\n\n'),(r'\result{COROLLARY}{1} ','\n\\begin{equation}'),(r'\result{COROLLARY}{2} ','\n\n')]:
    t=page_text(rel,175)[0];old=t.split(marker,1)[1].split(end,1)[0]
    ch(old,underline_prose(old),marker,'Restore the assertion prose underlines visible in the scan while leaving formulas and statement references outside the prose underline.')
record_translation_page('en','149',175,rel,
    'Read Proposition 4, Corollary 1 and its complete determinant argument, and the opening hypotheses of Corollary 2. The existing English projective rank-one assertions agree with corrected French and were retained; the unprinted explanatory footnote was removed from the text. Approved all 60 formula correspondences after restoring explicit zero, dim n and prime-symbol notation. Restored the intermediate Ext expression to inline form, the underlined base field, assertion emphasis and the narrower fundamental-class emphasis. Rechecked the rank-one correction and the canonical determinant cancellation; the regular-sequence acyclicity statement is background in this English pass.',(317,371))
event('en-149-3.5','used and rechecked in this run',
    'The two top exterior powers of the locally free differential modules are projective of rank one, not generally free, and the top exterior power of a rank-n module has rank one. With the conormal exact sequence, the determinant identity gives omega_A restricted to A/J tensor omega_(A/J) dual = determinant(J/J squared). Proposition 4 identifies the resulting top Ext with endomorphisms of this determinant line, canonically A/J. English already had the corrected projective rank-one statements; this check retains them and removes the editorial footnote from the text.',
    '149, p. 175, Corollary 1, (3.5) and proof')
event('en-149-proposition4','carried as background without fault found',
    'Read the full regular-sequence hypotheses, the basis assertion for J/J squared, free Koszul resolution, degree-p isomorphisms and the extra J.M=0 condition for arbitrary degrees. No independent proof of regular-sequence acyclicity is claimed in this English pass.',
    '149, p. 175, Proposition 4')
update()
