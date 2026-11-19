from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-202'
def ch(old,new,where,why,kind='terminology',full=False,count=1):
    replace(rel,old,new,'English',page,where,'Theorem 7, Corollaries 2–3 and Proposition 2',
      'French 182-202 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands: '+why,kind=kind,full=full,count=count)
ch(r'\footnote{The printed text does not specify the neighborhood. The local scope of Corollary 2 is restored here; it is also used in the proof of Proposition 2.}',
   '', 'Corollary 3 editorial footnote','The corrected local conclusion is already present, but this explanatory footnote is absent from the print and corrected French; retain the correction in the audit record, not as an inserted footnote.',kind='structure')
whole=read(rel);start=whole.index('\\[\n  e\\longrightarrow \\Osh_Y^*');end=whole.index('\\src{203}',start)+len('\\src{203}')
old=whole[start:end];new='\\src{203}\n'+old[:-len('\\src{203}')]
ch(old,new,'printed page break before the sheaf sequence','The sheaf exact sequence begins printed page 203. Move the existing marker there without altering its text.',kind='structure',full=True)
ch("$v:E\\longrightarrow E\\otimes L'$", "$v$ from $E$ to $E\\otimes L'$",'Proposition 2 corollary','Restore the source separation of the name v and the two sheaves in prose, rather than an added arrow formula.',kind='structure')
pairs=[(i,i) for i in range(16)]+[(i,i+1) for i in range(16,23)]+[(23,23)]+[(i,i) for i in range(24,49)]
align_math(rel,'en','182',202,pairs,(49,49))
ch('$\\symup{H^1\\bigl(X_y;\\mathop{\\text{\\uwave{Hom}}}\\nolimits_{O_X}(E_0,E_0)\\bigr)=0}$\nThen',
   '$\\symup{H^1\\bigl(X_y;\\mathop{\\text{\\uwave{Hom}}}\\nolimits_{O_X}(E_0,E_0)\\bigr)=0}$,\nthen',
   'Corollary 2','Restore the source comma and continuous conditional sentence after making the condition inline.',kind='structure')
ch("$\\symup{f^*(L')\\otimes O_X(n)}$\nwhere", "$\\symup{f^*(L')\\otimes O_X(n)}$,\nwhere",'Proposition 2 line-bundle form','Restore external comma after the inline formula.',kind='structure')
ch("$\\symup{P(E)\\xrightarrow{\\sim}P(E\\otimes L')=P(E)}$\nthe pair", "$\\symup{P(E)\\xrightarrow{\\sim}P(E\\otimes L')=P(E)}$;\nthe pair",'Proposition 2 corollary','Restore external semicolon after the inline isomorphism.',kind='structure')
for heading in [r'\result{COROLLARY}{2} ',r'\result{PROPOSITION}{2} ',r'\result{COROLLARY}{} ']:
    text,_,_=page_text(rel,202);body=text.split(heading,1)[1].split('\n\n',1)[0]
    ch(body,underline_prose(body).replace(r'\uline{where}', 'where'),'statements','Restore the printed prose emphasis, leaving the unaccented where outside the underline.')
text,_,_=page_text(rel,202);body=text.split(r'\result{COROLLARY}{3} ',1)[1].split('\n\n',1)[0]
aside="(i.e. sheaves locally isomorphic to $\\symup{O_X}$)";pre,post=body.split(aside,1)
ch(body,underline_prose(pre)+aside+underline_prose(post),'Corollary 3','Restore the main assertion’s emphasis while preserving its unaccented parenthetical definition.')
ch('an exact sequence of groups\n', 'an exact sequence of groups.\n','group exact sequence introduction','Restore the printed period before the displayed sequence.',kind='structure')
ch('following exact sequence of sheaves of groups','following exact sequence of \\uline{sheaves} of groups','sheaf exact sequence introduction','Restore emphasis distinguishing sheaves of groups.')
record_translation_page('en','182',202,rel,
    'Read Corollaries 2 and 3 of Theorem 7, Proposition 2, its automorphism corollary and the torsion/exact-sequence discussion. Approved all 49 target formula correspondences: the associated bundle refers implicitly to the preceding E, and the English repeats n in its uniqueness sentence, so the explicit pair list is not inferred from equal counts. The already-present local qualification in Corollary 3 and rank-at-least-two hypothesis in Proposition 2 agree with the corrected French. Removed the unprinted editorial footnote. Restored inline formulas, plain P, Hom typography, emphasis and the page-203 marker.',(432,494))
event('en-182-Theorem7-Corollaries2-3','targeted proof check',
    'Checked Corollary 2 by applying Theorem 7 to a chosen isomorphism between the common fiber restrictions and its isomorphism corollary. For an invertible E_0 the endomorphism sheaf is O_Xy, giving Corollary 3 only near the fiber. A nontrivial line bundle pulled back from the base has trivial restrictions to every fiber, so a global conclusion would be false; the existing English local qualification is retained.',
    '182, p. 202, Corollaries 2–3')
event('en-182-Proposition2','targeted proof check',
    'Checked the sketch using Pic(P^r_k)=Z and H^1(P^r_k,O)=0 as background inputs for r>=1. Corollary 3 makes each L locally O(n) over the base; n is locally constant and hence constant on connected Y. After twisting by O(-n), the transition units descend because f_*O_X=O_Y, producing L-prime. Fiber degree fixes n and pushforward fixes L-prime. Rank one would make n nonunique, so the corrected rank-at-least-two hypothesis is necessary.',
    '182, p. 202, Proposition 2 and proof sketch')
event('en-182-Proposition2-Corollary','targeted proof check',
    'Checked the relative-automorphism interpretation supplied by the preceding Y-morphism paragraph. Pullback of O(1) has degree one on fibers, hence differs from O(1) by a base line bundle; its degree-one sections provide v:E to E tensor L-prime with the stated projectivization. Scalar units are exactly the kernel. The determinant of E tensor L-prime gives (L-prime)^rank(E)=O_Y, and composition gives the stated group exact sequence with the twisting classes Gamma.',
    '182, p. 202, Proposition 2 corollary and group exact sequence')
update()
