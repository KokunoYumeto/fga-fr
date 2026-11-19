from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-180'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'Theorem 1 proof / (4.6)–(4.8)',
      'French 149-180 and the personally inspected full 400-dpi page and enlarged top, middle and bottom bands: '+why,kind=kind,count=count)
ch('  \\qquad(i>0),\n\\]\nbecause','\\]\nfor $i>0$, because',
   'Tor vanishing','The condition i>0 belongs to the prose after the display in the source.',kind='structure')
ch('provided $Z\'$ is a nonsingular cycle on $X\'$ to which $f$ is “transverse,” that\nis, the graph of $f$',
   'a formula valid if $Z\'$ is a nonsingular cycle on $X\'$ such that $f$ is \\fquote{transverse} to $Z\'$, i.e. such that the graph of $f$',
   'hypothesis of (4.8)','Restore the explicit repeated corrected Z-prime, the quoted word and i.e.; retain the order of the source hypothesis.',kind='translation')
align_math(rel,'en','149',180,[(i,i) for i in range(34)],(34,34))
ch('diagram of\nisomorphisms analogous','diagram of\nhomomorphisms analogous',
   'identification with (4.3)','Carry the corrected French homomorphismes into English. The left map in (4.3) need not be an isomorphism: for A^1 and its origin, Ext^1(O_0,Omega^1) is k whereas H^1(A^1,Omega^1) is zero.',kind='translation')
ch('now follows from the formula\n','now follows from the formula:\n','before (4.6)','Restore the printed colon.',kind='structure')
ch('respectively','resp.','hypotheses of (4.7)','Retain the source abbreviation.',count=2)
ch('Cartesian\nproducts:','cartesian\nproduct:','compatibility before (4.7)','Apply lowercase cartesian and preserve the source singular product.')
ch('compatible with inverse image under a morphism',r'compatible with the operation \fquote{inverse image} under a morphism',
   'compatibility before (4.8)','Restore the source operation noun and quotation marks without introducing pullback terminology.')
record_translation_page('en','149',180,rel,
    'Read the completion of Theorem 1 and formulas (4.6), (4.7) and (4.8). Restored the inline i>0 condition and explicit repeated Z-prime before approving all 34 math correspondences. Carried the corrected homomorphisms into the diagram description; the printed isomorphisms is false for its left arrow. Retained the corrected Z-primes throughout inverse-image compatibility, restored the source formula punctuation, resp., cartesian, quoted inverse image and transverse, and i.e. The first-person Je dis remains I claim.',(582,628))
event('en-149-4.3-left-arrow','used and rechecked in this run',
    'Rechecked the corrected word homomorphisms: take X=A^1, Y the origin and p=1. The length-one resolution by multiplication by the coordinate gives Ext^1_X(O_Y,Omega_X^1)=k, whereas H^1(X,Omega_X^1)=0. Thus the left arrow of (4.3) cannot generally be called an isomorphism. Its right edge arrow remains an isomorphism.',
    '149, p. 180, first paragraph referring to (4.3) and (4.5)')
event('en-149-4.6-4.8','carried as background without fault found',
    'Read the tensor-resolution argument, Tor vanishing under transverse intersection, local product of fundamental sections, cartesian-product compatibility and the graph-transversality formulation of inverse-image compatibility. Checked the corrected Z-primes and every degree, tensor, product and arrow. No separate sign-convention proof of the Koszul product is asserted in this translation event.',
    '149, p. 180, Tor displays and (4.6)–(4.8)')
update()
