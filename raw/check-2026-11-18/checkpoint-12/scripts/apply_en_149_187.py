from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-187'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'Corollary to Proposition 6 / section 7',
      'French 149-187 and the personally inspected full 400-dpi page and enlarged top, middle and bottom bands: '+why,kind=kind,count=count)
ch('\\footnote{The printed text says here\n``$S$ is normal\'\'; the paragraph involves only the variety $X$.}', '',
   'normality example','Remove the unprinted editorial footnote; the justified X reading remains in the corrected text and in the correction record.',kind='structure')
align_math(rel,'en','149',187,[(i,i) for i in range(44)],(44,44))
ch('One has $\\symup{H^{i}(X,F(-m))=0}$ for $\\symup{m}$ large if and only if\n$\\symup{E^{n-i}(F)=0}$.',
   'For $\\symup{H^{i}(X,F(-m))=0}$ to hold for $\\symup{m}$ large, it is necessary and sufficient that\n$\\symup{E^{n-i}(F)=0}$.',
   'corollary','Apply the standard necessary-and-sufficient rendering of il faut et il suffit, retaining the order of its two conditions.')
ch('Recall that','Let us recall that','second paragraph','Restore authorial Rappelons.')
ch('projective embedding','projective immersion','second paragraph','Apply the standard rendering of immersion.')
ch('purely local.\nConsequently, if','purely local;\nconsequently, if','second paragraph','Keep the source causal period whole.',kind='structure')
ch('$\\symup{\\geq k}$ (see\n[4]','$\\symup{\\geq k}$ (cf.\n[4]','homological codimension','Apply the standard cf. for cf, rather than see.')
ch('(Nagata)','(NAGATA)','local ring criteria','Restore the source name capitalization.',kind='reading')
ch('Cohen--Macaulay','Cohen-Macaulay','local ring criteria','The printed compound uses a single hyphen.',kind='reading')
ch(r'\fsection{7}{Poincaré duality}',r'\fsection{\normalfont7}{\normalfont\uline{Poincaré duality}.}',
   'section heading','Restore normal weight, title underlining and final period.',kind='structure')
ch('dimension $\\symup{2n}$: that is,','dimension $\\symup{2n}$, i.e.',
   'Poincaré algebra','Restore the printed comma and the standard i.e. abbreviation.')
ch('as a commutative algebra, $\\symup{H^{*}(X)}$ is a contravariant functor of $\\symup{X}$: a\nmorphism $\\symup{f:Y\\longrightarrow X}$ defines in the evident way a homomorphism of',
   '$\\symup{H^{*}(X)}$ is, as a commutative algebra, a contravariant functor of $\\symup{X}$, a\nmorphism $\\symup{f:Y\\longrightarrow X}$ defining in the evident way a homomorphism of',
   'last paragraph','Preserve the source appositive construction and comma within the continuing sentence.',kind='structure')
t=page_text(rel,187)[0];start=r'\result{COROLLARY}{} ';old=t.split(start,1)[1].split('\n\n',1)[0]
ch(old,underline_prose(old),'corollary','Restore the printed underlined assertion prose.')
record_translation_page('en','149',187,rel,
    'Read the corollary, local vanishing examples, homological codimension discussion, and the opening of section 7 paragraph by paragraph. Approved all 44 formula correspondences, including the underlined Omega and k, the two inline identities, and (7.1) without an added comma. The existing corrected X in the normality example and H^m in the duality pair are retained; removed only the unprinted explanatory footnote. Restored assertion emphasis, section heading, cf., authorial form and source sentence boundaries.',(944,991))
event('en-149-proposition6-corollary','used and rechecked in this run',
    'For fixed i, Proposition 6 identifies the dual of H^i(F(-m)) with H^0(E^(n-i)(F)(m)) for sufficiently large m. A coherent sheaf has zero H^0 in all sufficiently large twists exactly when it is zero, since such twists are globally generated. This verifies the necessary-and-sufficient wording and the n-i exponent.',
    '149, p. 187, opening corollary')
event('en-149-section6-local-examples','carried as background without fault found',
    'Read and aligned the local vanishing, historical homological-codimension and complete-intersection claims, with the earlier justified X-for-S correction. No independent proof of all the local-ring characterizations was made in this translation pass.',
    '149, p. 187, paragraph following the corollary')
event('en-149-section7-poincare','used and rechecked in this run',
    'Checked the total degree p+q and complementary degree 2n-m in the Serre-duality pairing. The corrected H^m partner agrees with the product displayed in the same sentence; the printed H^n there is retained only in the printed French layer. The Kunneth and trace-compatibility assertions are carried from the earlier results, without a new independent proof here.',
    '149, p. 187, section 7 through (7.1)')
update()
