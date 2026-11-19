from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-181'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'Corollary 1 / Theorem 2',
      'French 149-181 and the personally inspected full 400-dpi page and enlarged top, middle and bottom bands: '+why,kind=kind,count=count)
ch("\\[\n  Z\\times(a)=(X\\times(a)).U,\n  \\qquad\n  Z'\\times(b)=(X\\times(b)).U.\n\\]",
   "$Z\\times(a)=(X\\times(a)).U$, $Z'\\times(b)=(X\\times(b)).U$.",
   'two cycle identities in Corollary 1','These are two separate inline expressions in the source; preserve the corrected prime and uppercase U.',kind='structure')
align_math(rel,'en','149',181,[(i,i) for i in range(48)],(48,48))
ch("projective space, with $\\symup{X'}$ complete.","projective space; let us suppose $\\symup{X'}$ complete.",
   'Corollary 1 hypotheses','Retain the authorial supposons and the order of hypotheses.')
ch('transversely. Let $\\symup{Z}$','transversely; let $\\symup{Z}$',
   'Corollary 1 hypotheses','Keep the source period whole.')
ch('Then\n\\[','Then one has\n\\[','Corollary 1 conclusion','Restore on a.')
ch('$\\symup{f_a(x)=(x,a)}$. Formula (4.8) gives',
   '$\\symup{f_a(x)=(x,a)}$; one then has, by (4.8), the formula',
   'Corollary 1 proof','Keep the source period whole and retain its impersonal on a.')
ch('the point $\\symup{(x)}$','$\\symup{(x)}$',
   'point-class paragraph','The source directly uses the notation (x) without an added noun.',kind='translation')
ch(r'\emph{fundamental class}',r'\uline{fundamental class}',
   'point-class definition','Restore the printed prose underlining.')
ch('(At the time this exposé was written, this had not yet been done in\nfull generality.)',
   '(At the time of writing this exposé, this has not yet been done in\nfull generality).',
   'historical remark','Preserve the source present perspective and the period outside the closing parenthesis.')
ch(r'\fsection{5}{The duality theorem}',r'\fsection{\normalfont5}{\normalfont\uline{The duality theorem}.}',
   'section 5 heading','Restore the source heading type, underlining and final period.')
ch('(The proof will be given below.)','(The proof will be given below).',
   'after Theorem 2','The period follows the closing parenthesis.',kind='structure')
ch('we may therefore\nidentify','one may therefore\nidentify','after Theorem 2','The source on peut is impersonal.')
ch('Now consider the pairings','Let us now consider the pairings','page-ending paragraph','Restore the authorial Considérons.')
for start,end in [(r'\result{COROLLARY}{1} ','\n\\['),(r'\result{THEOREM}{2} ','\n\n')]:
    t=page_text(rel,181)[0];old=t.split(start,1)[1].split(end,1)[0]
    ch(old,underline_prose(old),'statement prose','Restore the underlined assertion prose, excluding mathematical variables.')
record_translation_page('en','149',181,rel,
    'Read Corollary 1 and its Künneth proof, the point-class definition, the historical remark, section 5 and Theorem 2. Restored the two inline cycle identities, then approved all 48 mathematical correspondences. Kept corrected Z-prime and U in the second identity; all differential-sheaf underlines and the underlined field k now match French. Restored statement emphasis, the heading, authorial and impersonal forms, intact source periods, and the historical remark in its original present perspective. Reopened the literal French par/pas locus: fr_printed already correctly retains par and the corrected French pas is separately justified in the ledger.',(627,678))
event('en-149-corollary1-p181','used and rechecked in this run',
    'Read the stated complete nonsingular parameter variety and transverse-fiber hypotheses. Under the historical variety convention giving H^0(X\u2032,O)=k, evaluation at a and b agrees on scalars; positive cohomology or positive differential degree from X\u2032 pulls back to zero at a point, so the Künneth expression gives f_a^*=f_b^*. Rechecked the corrected second fiber identity Z\u2032 times (b)=(X times (b)).U. This does not remove the historical remark\u2019s caveat about arbitrary algebraic equivalence.',
    '149, p. 181, Corollary 1, its proof and following remark')
event('en-149-theorem2','carried as background without fault found',
    'Read that the fundamental point class is a basis of H^n(X,Omega_X^n) for a nonsingular projective variety and the resulting scalar identification. The text explicitly postpones its proof; no independent proof is claimed at this page.',
    '149, p. 181, Theorem 2 and final paragraph')
update()
