from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-179'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'Theorem 1 / (4.5)',
      'French 149-179 and the personally inspected full 400-dpi page and enlarged top, middle and bottom bands: '+why,kind=kind,count=count)
align_math(rel,'en','149',179,[(i,i) for i in range(32)],(32,32))
ch('intersect transversely, then\n','intersect transversely, then one has\n','Theorem 1 assertion','Restore the source on a.')
ch('(We assume that','(One assumes that','parenthetical hypothesis','The source On suppose is impersonal.')
ch('space.)','space)','parenthetical hypothesis','The source parenthesis has no terminal period.',kind='structure')
ch('This last hypothesis is used only to conclude that','We use this last hypothesis only to be able to conclude that',
   'opening proof','Keep the explicit authorial nous sert.')
ch('we may suppose that','one may suppose that','reduction to irreducible subvarieties','The source on peut supposer is impersonal.')
ch('locally free sheaves. By Proposition 3, the diagram of homomorphisms (4.3) then\nidentifies with',
   'locally free sheaves; then, by Proposition 3, the diagram of homomorphisms (4.3)\nidentifies with the diagram',
   'resolution paragraph','Keep the source period whole, including its repeated diagram noun.')
ch('Here $\\symup{\\Gamma}$ is the “group of sections” functor',
   'where $\\symup{\\Gamma}$ is the \\fquote{group of sections} functor',
   'after the hypercohomology diagram','Retain the continuing relative clause and the quoted functor label.')
ch('For simplicity, we\nmay suppose that','For simplicity, one\nwill suppose that','normalization of the resolution','The source On supposera is impersonal.')
ch('(which is permissible).\nThen $\\symup{\\alpha}$','(which is permissible);\nthen $\\symup{\\alpha}$',
   'normalization of the resolution','Retain the source period whole through the consequence for alpha.')
ch('is the familiar edge\nhomomorphism. Consider the analogous diagram for a locally free resolution',
   'is a familiar \\fquote{edge-homomorphism}. Let us consider an analogous diagram for a locally free resolution',
   'edge homomorphism and second resolution','Restore un, the printed quoted hyphenated label and authorial Considérons.')
ch('and then the following commutative diagram of pairings:',
   'and let us consider the commutative diagram of pairings:',
   'introduction to (4.5)','Retain the repeated authorial considérons and avoid an added then.')
for start,end in [(r'\result{THEOREM}{1} ','\n\\begin{equation}'),
                  ('where the product on the right is the cup product','\n\\[')]:
    t=page_text(rel,179)[0]
    old=t.split(start,1)[1].split(end,1)[0] if start.startswith('\\result') else start+t.split(start,1)[1].split(end,1)[0]
    ch(old,underline_prose(old),'Theorem 1 assertion prose','Restore the source underlining without changing mathematical alphabets.')
record_translation_page('en','149',179,rel,
    'Read Theorem 1, its projective-space hypothesis, the use of locally free resolutions, the hypercohomology comparison and the whole pairing diagram (4.5). Approved all 32 mathematical correspondences. Restored double-underlined R in place of blackboard R, all underlined differential sheaves, the left brace and full parentheses in (4.5), the beta-over-sim symbol, the ordinary L without a star in the complex map, and exact punctuation. Restored theorem emphasis, source quotation marks, impersonal on, authorial nous/Considérons and the source long periods. The theorem proof continues on p. 180.',(529,596))
event('en-149-theorem1','carried as background without fault found',
    'Read the transverse nonsingular-cycle multiplicativity assertion (4.4), its locally closed projective-space hypothesis and the resolution argument through (4.5). Inspected all nine diagram entries, three pairings, primes, degrees and arrows. Preserved the distinction between ordinary R and double-underlined hypercohomology R. The next page completes the argument; this event does not claim a new independent proof.',
    '149, p. 179, Theorem 1 and diagram (4.5)')
update()
