from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-184'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'Lemma 5 / (D)',
      'French 149-184 and the personally inspected full 400-dpi page and enlarged top, middle and bottom bands: '+why,kind=kind,count=count)
ch('}^{1}', '}^{i}', 'Lemma 5, three Ext exponents',
   'The additional tight index crop and the corresponding small i on p. 183 show the round dot and shoulder of i. Both French layers correctly read i; the English numeral 1 improperly restricts the statement.',kind='translation',count=3)
align_math(rel,'en','149',184,[(i,i) for i in range(25)],(25,25))
ch('on $\\symup{X}$, and\nset', 'on $\\symup{X}$; let us\nset',
   'Lemma 5 setup','Retain the authorial posons and the whole source period.')
t=page_text(rel,184)[0];old=t.split(r'\result{LEMMA}{5} ',1)[1].split('\n\\[',1)[0]
ch(old,underline_prose(old),'Lemma 5 assertion','Restore the source assertion underlining, excluding mathematical spans.')
ch('\\]\nis an isomorphism.', '\\]\n\\uline{is an isomorphism}.',
   'Lemma 5 conclusion','Restore the source underlining.')
ch('We now prove (D)', 'Let us now prove (D)', 'proof of (D)','Restore the authorial Démontrons.')
ch('isomorphism for $\\symup{p=n}$. Both sides are then left-exact functors (since\n$\\symup{H^{r+1}(P,F)=0}$), so Lemma 3 shows',
   'isomorphism for $\\symup{p=n}$; since both sides are then left-exact functors (because\n$\\symup{H^{r+1}(P,F)=0}$), Lemma 3 shows',
   'projective-space proof','Keep the source period whole and its logical order.')
ch('The homomorphisms\n(5.2 bis) are functorial', 'Since the homomorphisms\n(5.2 bis) are functorial',
   'projective-space proof','Restore the opening subordinate cause of the source long period.')
ch('(Corollary to Lemma 4).\nA standard argument therefore shows',
   '(Corollary to Lemma 4),\na standard argument therefore shows',
   'projective-space proof','Keep the complete causal period whole.')
ch('projective space. Now let $\\symup{X}$ be\narbitrary but nonsingular.',
   'projective space.\n\nLet us now suppose $\\symup{X}$ arbitrary but nonsingular.',
   'transition to arbitrary X','Restore the printed paragraph break and the authorial Supposons.',kind='structure')
ch('duality theorem for $\\symup{P}$, there is an\nisomorphism',
   'duality theorem for $\\symup{P}$, one has an\nisomorphism,',
   'arbitrary X proof','Retain the source on a and the comma before the display.')
ch('Taking $\\symup{F=\\underline{\\Omega}_X^{n}}$ gives an isomorphism',
   'Taking $\\symup{F=\\underline{\\Omega}_X^{n}}$, one obtains an isomorphism',
   'before (5.7)','Restore the impersonal on trouve.')
record_translation_page('en','149',184,rel,
    'Read Lemma 5, its local-to-global spectral sequence, the proof of (D) on projective space, and the reduction for a nonsingular closed X through (5.7). Reopened a tight crop of the Lemma 5 index: restored i in all three Ext exponents, matching both French layers. Approved all 25 formula correspondences, including omega versus Omega, their underlines, the underlined field k, and formula punctuation. Restored the assertion emphasis, the two intact causal periods and the paragraph break before the case of arbitrary X.',(791,840))
event('en-149-lemma5','targeted proof check',
    'For each fixed degree i, twisting the first coherent argument by O(-m) twists each sheaf Ext by O(m). Serre vanishing kills the positive-p columns relevant to total degree i and to the differentials of the edge term for sufficiently large m; the edge morphism is then an isomorphism. This checks the general i reading and does not assert a single bound for all unbounded q on a singular X.',
    '149, p. 184, Lemma 5 and following spectral sequence')
event('en-149-D-projective-space','used and rechecked in this run',
    'Rechecked the reduction at p=n using left-exact contravariant functors and presentations by negative twists, then the extension to the other degrees by coeffaceability and compatibility with connecting maps. For a nonsingular closed X in P, the codimension r-n Ext and Lemma 1 identify the two Hom expressions; setting F=Omega_X^n gives (5.7) under the historical complete connected variety convention. The normalization of this isomorphism continues on the next page.',
    '149, p. 184, proof of (D), (5.6) and (5.7)')
update()
