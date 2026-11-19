from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-194'
def ch(old,new,where,why,kind='terminology'):
    replace(rel,old,new,'English',page,where,'Section 1',
      'French 182-194 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands, with additional tight A-algebras crop: '+why,kind=kind)
align_math(rel,'en','182',194,[(i,i) for i in range(47)],(47,47))
for word in ['affine scheme','prescheme','separated','scheme','Noetherian']:
    ch('\\emph{'+word+'}','\\uline{'+word+'}','definitions','Restore printed underlined emphasis.')
ch('Morphisms of preschemes','\\uline{Morphisms} of preschemes','second paragraph','Restore missing emphasis on morphismes.')
ch('$\\symup{A}$-algebras.','$\\symup{A}$\\uline{-algebras}.','third paragraph','Restore emphasis on -algèbres; the tight crop confirms that A itself is excluded.')
ch('One says that $\\symup{X}$ is \\emph{of finite type over} $\\symup{S}$ if,',
   '$\\symup{X}$ is \\uline{said to be of finite type} over $\\symup{S}$ if,',
   'last paragraph definition','Match the passive est dit and the printed emphasis ending before sur.')
ch('“algebraic space,”','“algebraic space”,','last sentence','Restore punctuation outside the quoted expression.',kind='structure')
record_translation_page('en','182',194,rel,
    'Read the local-ring condition, affine scheme/prescheme definitions, relative products and base change, separated schemes, Noetherian and finite-type conventions, and fibers over residue fields. Approved 47 mathematical correspondences, including ordinary Z and the varkappa glyph. Restored all source emphasis; a separate tight crop confirms A is outside the underline in A-algebras. Historical conventions are retained without modernization.',(45,87))
event('en-182-1-preschemes','carried as background without fault found',
    'Read the construction and definitions paragraphwise. The local homomorphism condition, product/base-change notation and residue-field description agree with French. The historical definition of scheme as a separated prescheme is preserved; no modern terminology is substituted.',
    '182, p. 194, section 1')
update()
