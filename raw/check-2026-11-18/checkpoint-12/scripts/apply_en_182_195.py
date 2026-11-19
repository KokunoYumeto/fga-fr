from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-195'
def ch(old,new,where,why,kind='terminology'):
    replace(rel,old,new,'English',page,where,'Section 2',
      'French 182-195 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands: '+why,kind=kind)
ch('inverse system of sheaves of rings on $X\'$', 'projective system of sheaves of rings on $X$',
   'formal completion construction', 'The scan and both French layers say sur X. These sheaves on X are supported on the closed subset X-prime; restore the ambient space and apply the standard projective system term.',kind='translation')
align_math(rel,'en','182',195,[(i,i) for i in range(53)],(53,53))
for word in ['projective morphism','proper morphism','coherent sheaf of rings','formal scheme']:
    ch('\\emph{'+word+'}','\\uline{'+word+'}','definitions','Restore source underlined emphasis.')
ch('\\fsection{2}{Formal schemes}',r'\fsection{\normalfont2}{\normalfont\uline{Formal schemes}.}','section heading','Match printed heading emphasis and final period.',kind='structure')
ch('“closed subscheme of $\\symup{X}$.”','“\\uline{closed subscheme of} $\\symup{X}$”.','definition of closed subscheme','Restore missing emphasis, with X excluded, and punctuation outside the quotation.',kind='structure')
ch('inverse limit','projective limit','completion construction','Apply the standard projective limit terminology.')
ch('inverse\nsystem','projective\nsystem','formal scheme definition','Apply the standard projective system terminology.')
ch('\\emph{formal completion of\n$\\symup{O_X}$ along $\\symup{X\'}$}',
   '\\uline{formal completion of}\n$\\symup{O_X}$ \\uline{along} $\\symup{X\'}$',
   'formal completion of the structure sheaf','Match the source emphasis, excluding the mathematical symbols.')
ch('$\\symup{X\'}$ is called the\n\\emph{formal completion of $\\symup{X}$ along $\\symup{X\'}$}',
   '$\\symup{X\'}$ is \\uline{called the\nformal completion of} $\\symup{X}$ \\uline{along} $\\symup{X\'}$',
   'formal completion of the space','Include called in the printed emphasis and exclude the mathematical symbols.')
ch("Zariski's sense", "ZARISKI's sense",'historical terminology','Preserve the printed author typography.',kind='structure')
record_translation_page('en','182',195,rel,
    'Read every paragraph on proper morphisms, coherent sheaves, closed subschemes, formal completion and the start of the formal-scheme definition. Approved all 53 formula correspondences individually. Restored the ambient X in the projective system of sheaves, the standard projective terminology and the exact source emphasis. Checked n+1, the transition map for m greater than or equal to n, and the kernel J_m to the power n+1. The final definition continues on page 196.',(88,132))
event('en-182-2-formal-completion','carried as background without fault found',
    'Read the completion construction against the corrected French and print. The ambient space is X, while the completed ringed space has underlying closed subset X-prime. Preserved the historical Noetherian convention and Zariski terminology discussion. The assertions are carried as background, not recorded as independently proved.',
    '182, p. 195, section 2')
update()
