from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-190'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'Multifunctors (8.1)–(8.3)',
      'French 149-190 and the personally inspected full 400-dpi page and enlarged top, middle and bottom bands: '+why,kind=kind,count=count)
ch('$A_i,B_j$','$A_i$, $B_j$','coboundary operators','Keep the two source arguments separate before aligning formulas.')
align_math(rel,'en','149',190,[(i,i) for i in range(32)],(32,32))
ch('values, respectively, in the category of coherent algebraic sheaves on $\\symup{X}$ and\nin the category of modules over $\\symup{H^{0}(X,\\Osh_X)}$, by the formulas',
   'values in the category of coherent algebraic sheaves on $\\symup{X}$, resp.\nin the category of modules over $\\symup{H^{0}(X,\\Osh_X)}$, by the formulas:',
   'opening','Restore the source resp. and the colon introducing (8.1).')
ch('respectively','resp.','resolution convention and operations','Apply the standard preservation of resp.',count=2)
ch('arguments: $\\symup{\\underline{T}_{0}^{0}}$','arguments, $\\symup{\\underline{T}_{0}^{0}}$',
   'zero-argument convention','The source continues with a comma.',kind='structure')
ch('\\bigr)}$\nwhich abuts','\\bigr)}$,\nwhich abuts',
   'definition of K','Restore the source comma outside the restored inline formula.',kind='structure')
ch('with respect to $\\symup{K}$. Its initial term\nis','with respect to $\\symup{K}$, and whose initial term\nis',
   'before (8.2)','Keep the source long period whole.',kind='structure')
ch('It follows that this spectral sequence itself','One then sees that this spectral sequence itself',
   'after (8.2)','Restore on voit alors.')
ch('The connecting\noperators in the various arguments $\\symup{A_i}$, $\\symup{B_j}$ are readily defined, since every',
   'One readily defines the coboundary\noperators in the various arguments $\\symup{A_i}$, $\\symup{B_j}$, noting that every',
   'coboundary operators','Apply the glossary cobord → coboundary and retain on définit and en notant que.')
ch('Thus there is a composition (generalizing the\none considered in Section 2)',
   'Thus one has a \\uline{composition} (generalizing the\none considered in no. 2):',
   'before (8.3)','Restore on a, source emphasis, reference form and colon.')
ch('connecting homomorphisms','coboundary homomorphisms',
   'after (8.3)','Use the glossary cobord → coboundary consistently.')
ch('There are likewise symmetry operations','Likewise, one has symmetry operations',
   'last paragraph','Restore on a.')
ch('In addition, there is a contraction operation',
   'In addition, one has a \\uline{contraction} operation',
   'last paragraph','Restore on a and source emphasis.')
record_translation_page('en','149',190,rel,
    'Read the two definitions (8.1), zero-argument conventions, independence argument, (8.2), coboundaries, composition (8.3), and the beginning of contraction. Approved all 32 mathematical correspondences after separating A_i and B_j. Restored underlined resolutions, double-underlined R, the inline K identity, compact source argument lists and no added display punctuation. Retained corrected s-prime in (8.3). Applied resp., coboundary, source emphasis, impersonal register and whole-period structure.',(1112,1187))
event('en-149-8.1-8.2','used and rechecked in this run',
    'Checked the zero-argument specialization Hom(O_X,O_X)=O_X and its hypercohomology H^*(X,O_X). For independence, bounded complexes of locally free sheaves preserve quasi-isomorphisms under the finite tensor and internal-Hom constructions; locally this follows from contracting bounded acyclic complexes of finite free modules. The hypercohomology spectral sequence has the displayed E_2=H^p(X,H^q(K)) and compares the global values. The printed phrase first member of (8.1) is retained as its left-hand global expression, not changed to the sheaf-valued first line.',
    '149, p. 190, (8.1)–(8.2) and explanation')
event('en-149-8.3','carried as background without fault found',
    'Checked the r+r-prime, s+s-prime indices and the primed last B argument against the corrected French; the shorter printed ellipses are retained without expansion. Associativity, symmetry, spectral-sequence compatibility and contraction are read as stated constructions; no fresh full Koszul-sign computation was made here.',
    '149, p. 190, (8.3) and following paragraph')
update()
