from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-178'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'Lemma 1 proof / cycle class',
      'French 149-178 and the personally inspected full 400-dpi page and enlarged top, middle and bottom bands: '+why,kind=kind,count=count)
align_math(rel,'en','149',178,[(i,i) for i in range(40)],(40,40))
ch('In particular, take $\\symup{F=\\Osh_Y}$ and $\\symup{L=\\underline{\\Omega}_X^{p}}$. Since',
   'Let us take, in particular, $\\symup{F=\\Osh_Y}$, $\\symup{L=\\underline{\\Omega}_X^{p}}$; taking into account that',
   'specialization before (4.2)','Restore the authorial Faisons and keep the source period whole.')
ch('Now suppose for simplicity that $\\symup{Y}$ is nonsingular, so that',
   'Let us now suppose $\\symup{Y}$ \\uline{nonsingular} for simplicity, so that',
   'after (4.2)','Restore the first-person Supposons, hypothesis order and emphasis on non singulière.')
ch('sheaf $\\symup{\\Extsh_{\\Osh_X}^{p}(\\Osh_Y,\\underline{\\Omega}_X^{p})}$. If all components of $\\symup{Y}$ have\ndimension $\\symup{n-p}$, we call it the \\emph{fundamental section} of the sheaf',
   'sheaf $\\symup{\\Extsh_{\\Osh_X}^{p}(\\Osh_Y,\\underline{\\Omega}_X^{p})}$, which we shall call, if all components of $\\symup{Y}$ have\ndimension $\\symup{n-p}$, the \\uline{fundamental section} of the sheaf',
   'fundamental section definition','Retain the single source sentence and its relative clause, conditional hypothesis and underlining.')
ch(r'\emph{cohomology class of $\symup{Y}$ in $\symup{X}$}',
   r'\uline{cohomology class of} $\symup{Y}$ \uline{in} $\symup{X}$',
   'definition after the natural homomorphism','Underline only the defining prose, not the mathematical variables.')
ch(r'Call a \emph{nonsingular cycle of dimension $\symup{n-p}$}',
   r'Let us call a \uline{nonsingular cycle} of dimension $\symup{n-p}$',
   'nonsingular cycle definition','The source Appelons is authorial and emphasizes only cycle non singulier.')
ch("$\\symup{n-p'}$. They are said to \\emph{intersect transversely} if every component of",
   "$\\symup{n-p'}$; they are said to \\uline{intersect transversely}, if every component of",
   'transversality definition','Keep the source period whole and restore its prose emphasis and comma.')
ch('we have the\n','one has the\n','page-ending continuation','The source on a is impersonal.')
record_translation_page('en','149',178,rel,
    'Read the proof of (4.1 bis), specialization (4.2), construction of the fundamental section and cohomology class, diagram (4.3), and the definitions of nonsingular cycles and transverse intersection. Approved all 40 mathematical correspondences. Preserved the corrected second Ext degree p in the opening equality, restored underlined Omega and omega and exact diagram/display punctuation, and used the printed ordinary arrow in the assignment Y to P(Y). Applied source emphasis, authorial Faisons/Appelons, impersonal on and the two long periods that the English had split.',(471,530))
event('en-149-4.2-4.3','used and rechecked in this run',
    'The locally free exterior-power duality gives Omega^n tensor (Omega^p) dual = Omega^(n-p), yielding (4.2) from (4.1 bis). The quotient O_X to O_Y acts contravariantly in the first Ext slot, so the global Ext map points from the O_Y argument toward the O_X argument as in (4.3). The section-to-global-Ext isomorphism is the degree-p edge isomorphism of Lemma 1. Checked the construction and the free-abelian extension to nonsingular cycles; no proof of the following intersection proposition is claimed here.',
    '149, p. 178, opening equality, (4.2), (4.3) and cycle definitions')
update()
