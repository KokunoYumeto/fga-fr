from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-196'
def ch(old,new,where,why,kind='terminology'):
    replace(rel,old,new,'English',page,where,'Theorem 1',
      'French 182-196 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands: '+why,kind=kind)
align_math(rel,'en','182',196,[(i,i) for i in range(34)],(34,34))
ch(r'\emph{coherent sheaf of Noetherian local rings}',r'\uline{coherent} sheaf of \uline{Noetherian local} rings','opening sentence','Limit the underlining to the source adjectives.')
for word in ['locally','affine']:
    ch('\\emph{'+word+'}','\\uline{'+word+'}','formal scheme description','Restore underlined source emphasis.')
ch(r'\fsection{3}{The three fundamental theorems}',r'\fsection{\normalfont3}{\normalfont\uline{The three fundamental theorems}.}','section heading','Match the source heading and final period.',kind='structure')
ch(r'\result{THEOREM}{1 (finiteness theorem)}',r'\result[.]{THEOREM}{1 (finiteness theorem)}','theorem heading','Restore the printed heading separator.',kind='structure')
ch('\\item[\\textit{i.}] The $\\symup{R^{q}\\overline f_{*}(\\overline F)}$ are coherent\n    sheaves on $\\symup{\\overline Y}$.',
   '\\item[\\textnormal{i.}] \\uline{The} $\\symup{R^{q}\\overline f_{*}(\\overline F)}$ \\uline{are coherent\n    sheaves on} $\\symup{\\overline Y}$.','Theorem 1 i','Restore the roman item marker and underlined prose, excluding mathematical expressions.')
ch(r'\item[\textit{ii.}] The natural homomorphisms',r'\item[\textnormal{ii.}] \uline{The natural homomorphisms}','Theorem 1 ii','Restore the roman item marker and underlined prose.')
ch('    are isomorphisms.','    \\uline{are isomorphisms.}','Theorem 1 ii conclusion','Restore source underlining.')
ch('“formal cohomology.”','“formal cohomology”.','last sentence','Restore punctuation outside the quoted expression.',kind='structure')
record_translation_page('en','182',196,rel,
    'Read the continuation of the formal-scheme definition, the affine description, the setup of the three fundamental theorems and Theorem 1 with both clauses. Approved 34 exact mathematical correspondences. The English already has the corrected target Y-bar in the induced formal morphism, where the print repeats X-bar. Preserved the author\'s explicit qualification about the extent of his written proof. Restored emphasis, theorem punctuation and roman item markers.',(133,181))
event('en-182-Theorem1','carried as background without fault found',
    'Compared both finiteness assertions and their notation with the corrected French and scan: coherence of R^q f-bar_* F-bar and its comparison with the projective limit of R^q f_n* F_n. The English already carries the corrected target Y-bar in the preceding morphism. This reading does not supply an independent proof of the formal finiteness theorem.',
    '182, p. 196, section 3, Theorem 1')
update()
