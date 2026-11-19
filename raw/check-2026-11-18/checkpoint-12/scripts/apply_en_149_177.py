from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-177'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'Corollary to Proposition 5 / Lemma 1',
      'French 149-177 and the personally inspected full 400-dpi page and enlarged top, middle and bottom bands: '+why,kind=kind,count=count)
ch('\\footnote{The printed text has $E(A)$. In the category under consideration the\nrepresenting object is $A/J$, and the equality needed for (3.7) is $E(A/J)$.}\n','',
   'after the representing-object formula','The explanation is an editorial addition absent from the corrected French. Preserve the corrected E(A/J) formula and keep its reason in the audit record.',kind='translation')
ch('\\footnote{The printed text uses\na union sign; the graded structure is the direct sum of the sheaves\n$\\Omega_X^p$.}','',
   'after the differential-forms definition','Remove the added editorial footnote while retaining the corrected direct-sum sign; its justification belongs in the notes.',kind='translation')
align_math(rel,'en','149',177,[(i,i) for i in range(42)],(42,42))
ch('“dimension”',r'\fquote{dimension}','opening continuation','Keep the printed quotation marks.')
ch('$\\symup{E(M)=\\operatorname{Hom}_{A}\\bigl(M,E(A/J)\\bigr)}$\nFinally,',
   '$\\symup{E(M)=\\operatorname{Hom}_{A}\\bigl(M,E(A/J)\\bigr)}$.\nFinally,',
   'representing-object formula','Restore the period after the formula, which runs in the line.',kind='structure')
ch('Then, for coherent algebraic sheaves\n$\\symup{F}$ on $\\symup{Y}$, there is a functorial isomorphism',
   'Then there is a functorial isomorphism for coherent algebraic sheaves\n$\\symup{F}$ on $\\symup{Y}$:',
   'Corollary assertion','Retain the source clause order and the colon introducing (3.8).',kind='structure')
ch(r'\fsection{4}{Cohomology class associated with a subvariety}',
   r'\fsection{4}{\uline{Cohomology class associated with a subvariety.}}',
   'section 4 heading','Restore the underlined heading and its final period.')
ch('We denote by','One denotes by','notation paragraph','The French On désigne is impersonal.')
for start,end in [(r'\result{COROLLARY}{} ','\n\\begin{equation}'),
                  (r'\result{LEMMA}{1} ','\n\\begin{equation}'),
                  ('If $\\symup{F}$ is a coherent algebraic sheaf','\n\\begin{equation}'),
                  ('where $\\symup{\\underline{\\omega}_Y^{n-p}}$','\n\n')]:
    t=page_text(rel,177)[0]
    if start.startswith('\\result'):old=t.split(start,1)[1].split(end,1)[0]
    else:old=start+t.split(start,1)[1].split(end,1)[0]
    ch(old,underline_prose(old),'assertion prose','Restore the source prose underlining while preserving each mathematical alphabet.')
record_translation_page('en','149',177,rel,
    'Read the end of Proposition 5, its corollary, the opening of section 4 and Lemma 1. Approved all 42 math correspondences after removing the two added editorial footnotes. Retained the justified E(A/J), direct sum and Y corrections; restored inline status for the representing-object formula and the graded forms, underlined Omega and omega, the unsubscripted O bases of (4.1), exact tags and punctuation, assertion emphasis and impersonal On. The reasons for corrected readings remain in the record, separate from the translated text.',(420,478))
event('en-149-3.7-representing-object','used and rechecked in this run',
    'The representing module for a left exact contravariant functor on A/J-modules taking direct sums to products is E(A/J): use a presentation by direct sums of A/J and identify both functors with the same kernel. Thus the existing corrected E(A/J) is retained; E(A) in the print is not the value on the unit object of this module category. The added explanatory footnote is removed from the translation.',
    '149, p. 177, first paragraph, inline representing-object formula')
event('en-149-4.1','carried as background without fault found',
    'Read the corollary (3.8), the dimension and locally free hypotheses of Lemma 1, (4.1) and (4.1 bis), and the references to Propositions 1 and 5. Matched all formula bases, primes, underlined differential sheaves and degree n-p against the corrected French and scan. The proof continues on p. 178.',
    '149, p. 177, corollary to Proposition 5 and Lemma 1')
update()
