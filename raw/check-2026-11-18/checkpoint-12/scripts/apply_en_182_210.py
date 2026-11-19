from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-210'
def ch(old,new,where,why,kind='terminology',full=False,count=1):
    replace(rel,old,new,'English',page,where,'section 8: coverings and fundamental group',
      'French 182-210 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands: '+why,kind=kind,full=full,count=count)
whole=read(rel);start=whole.index('$X$, assumed irreducible.');end=whole.index('\\src{211}',start)+len('\\src{211}')
old=whole[start:end];new='\\src{211}\n'+old[:-len('\\src{211}')]
ch(old,new,'page break after generic point of','The printed page ends after point générique de. Move the existing marker before X assumed irreducible.',kind='structure',full=True)
ch("-homomorphism $\\kappa(x')\\longrightarrow\\Omega$",r'-homomorphism into $\Omega$',
   'fiber functor definition','Remove the added explicit source field and arrow; the French says a residue-field homomorphism into Omega.',kind='translation')
align_math(rel,'en','182',210,[(i,i) for i in range(54)],(54,54))
ch('of $\\symup{X}$ if','\\uline{of} $\\symup{X}$ if','definition continuation','Restore the continuation of the underlined defined term.')
for label in ['i.','ii.','iii.']:
    ch('\\textit{'+label+'}','\\textnormal{'+label+'}','definition labels','The printed labels are roman.',kind='structure')
ch("on $\\symup{X}$;","on $\\symup{X}$",'definition items i and ii','The printed first two items have no final semicolon.',kind='structure',count=2)
ch('due to Serre and the speaker','due to SERRE and the speaker','historical attribution','Restore the printed capitals.',kind='structure')
ch('gives rise to a Galois theory','gives rise to a \\uline{Galois theory}','Galois theory paragraph','Restore the printed emphasis.')
ch('More precisely, call','More precisely, let us call','geometric point definition','Restore the authors’ appelons register.')
for term in ['geometric point','locality']:
    ch('\\emph{'+term+'}','\\uline{'+term+'}','geometric point definition','Restore underlining of the defined term.')
ch('above $\\symup{a}$,”','above $\\symup{a}$”,','fiber functor definition','The comma follows the closing quotation mark.',kind='structure')
ch('an inverse limit of finite groups','a projective limit of finite groups','profinite group definition','Apply the standard rendering of limite projective.')
ch('\\emph{fundamental group} of the\nconnected scheme','\\uline{fundamental group of the\nconnected scheme}','fundamental group definition','Restore the full span of the first underlined phrase.')
ch('$\\symup{X}$ at the geometric point','$\\symup{X}$ \\uline{at the geometric point}','fundamental group definition','Restore the second underlined defining phrase.')
record_translation_page('en','182',210,rel,
    'Read all three conditions defining an unramified covering and the complete construction of the geometric-point fiber functor and its fundamental group through generic point of. Approved 54 formula pairings after removing an added explicit residue-field domain and moving the page-211 marker. Copied the corrected French varkappa in the fiber algebra, wavy A and plain O, and restored the inline quotient. Restored definition labels, underlining and punctuation; standardized projective limit. The English forgetful functor correctly expresses the French foncteur identique on underlying finite sets.',(812,864))
event('en-182-unramified-covering-definition','targeted proof check',
    'Checked the three conditions locally: a finite locally free algebra has finite flat morphism, and separability of every finite residue-field algebra gives zero relative differentials on each fiber. Nakayama for the finite module of differentials gives the unramified condition, hence finite etale. Conversely a finite etale morphism has these properties. This verifies the use of the historical unramified-covering terminology without changing the definition.',
    '182, p. 210, definition i–iii')
event('en-182-Galois-category-reconstruction','carried as background without fault found',
    'Read the claimed equivalence between finite unramified coverings with their geometric fiber functor and finite continuous sets for a profinite group. The required Galois-category axioms and reconstruction theorem are invoked, not proved independently in this page check.',
    '182, p. 210, Galois theory paragraph')
event('en-182-basepoint-inner-ambiguity','targeted proof check',
    'Conditional on the preceding reconstruction and existence of an isomorphism between the two fiber functors, checked the asserted ambiguity: transporting natural automorphisms along a chosen functor isomorphism gives a group isomorphism, and changing that choice by an automorphism of the fiber functor conjugates the result. Existence of the fiber-functor isomorphism remains part of the Galois-category background.',
    '182, p. 210, final paragraph')
update()
