from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-189'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'Diagram (7.6) / Theorem 5 / section 8',
      'French 149-189 and the personally inspected full 400-dpi page and enlarged top, middle and bottom bands: '+why,kind=kind,count=count)
ch('canonical endomorphisms:','canonical homomorphisms:',
   'opening continuation','Carry the justified corrected French homomorphismes: the diagram connects different groups, so its arrows are not endomorphisms.',kind='reading')
ch('variety $X$ whose fixed points all have multiplicity 1.',
   'variety $X$, such that the fixed points of $f$ have multiplicity $1$.',
   'Theorem 5 hypothesis','Restore the explicitly named f and the mathematical numeral before aligning the source formulas.',kind='reading')
ch('multiplicity 1.','multiplicity $1$.','homotopy remark','Preserve the source mathematical numeral.')
ch('modulo the characteristic',r'$\operatorname{mod}$ the characteristic',
   'Theorem 5 conclusion','Preserve the printed abbreviation as mathematical text.')
align_math(rel,'en','149',189,[(i,i) for i in range(31)],(31,31))
ch('This gives an exact analogue','One thus obtains an exact analogue',
   'after (7.6)','Restore on obtient ainsi.')
ch('oriented varieties.','oriented manifolds.',
   'topological comparison','Here variétés orientées compactes denotes topological manifolds in the comparison with classical Poincaré duality, not algebraic varieties.',kind='reading')
ch('A well-known argument then gives,\nfor example, a Lefschetz formula.',
   'By a well-known argument, one deduces from this,\nfor example, a \\uline{Lefschetz formula}:',
   'before Theorem 5','Retain on en déduit, the source underlining, and the introducing colon.')
ch('of $\\symup{\\underline{k}}$, to the','of $\\symup{\\underline{k}}$ to the',
   'Theorem 5 conclusion','Remove the added second comma in the source sentence.',kind='structure')
ch('remark in Section 4. Note, however,','remark in no. 4. One will note, however,',
   'homotopy remark','Retain the reference abbreviation and impersonal future on notera.')
ch(r'\fsection{8}{Generalization of the duality theorem}',
   r'\fsection{\normalfont8}{\normalfont\uline{Generalization of the duality theorem}.}',
   'section heading','Restore the source normal weight, underlining and final period.',kind='structure')
ch('$\\symup{B_1,\\ldots,B_s}$,','$\\symup{B_1,\\ldots,B_s}$',
   'last line','Remove the added comma before the continuation on p. 190.',kind='structure')
t=page_text(rel,189)[0];start=r'\result{THEOREM}{5} ';old=t.split(start,1)[1].split('\n\n',1)[0]
ch(old,underline_prose(old),'Theorem 5 assertion','Restore printed underlined prose, keeping formulas and mod outside the underlining.')
record_translation_page('en','149',189,rel,
    'Read the continuation of the compatibility argument, all six objects and arrows of (7.6), the Lefschetz theorem and homotopy remark, and the finite-resolution construction opening section 8. Corrected endomorphisms to homomorphisms and the topological contextual use of oriented manifolds; restored the named f in the fixed-point hypothesis. Approved all 31 formula correspondences after restoring two mathematical 1s and mod. Restored underlining, heading, impersonal register, references and punctuation; retained the existing removal of the duplicated opening the second across pp. 188–189.',(1045,1099))
event('en-149-7.6','carried as background without fault found',
    'Checked the six group expressions, the two downward arrows, leftward Ext maps and rightward isomorphisms against the corrected French and scan. These are homomorphisms between generally different groups. Commutativity is retained as the stated compatibility; no independent chain-level sign proof was made here.',
    '149, p. 189, opening and (7.6)')
event('en-149-theorem5','used and rechecked in this run',
    'Rechecked the stated scope: the diagonal/graph pairing gives the alternating trace in the base field, and transverse fixed points have local multiplicity one, hence contribute one. This yields the printed congruence modulo the characteristic, not an asserted integer equality in positive characteristic. The remark about a homotopic endomorphism remains background; the page does not specify a separate formal definition of that quoted word.',
    '149, p. 189, Theorem 5 and following remark')
event('en-149-section8-resolutions','targeted proof check',
    'Checked existence of a finite locally free resolution under the stated quotient property: take successive locally free covers of coherent kernels, then use the finite regular local dimensions to make a sufficiently high kernel locally free. For a comparison into a prescribed resolution, cover the successive fiber products; if the sheaf map is surjective, these can be chosen surjective onto the prescribed terms. This also supplies a common refinement, with finite truncation above both original lengths.',
    '149, p. 189, section 8 opening paragraph')
update()
