from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-183'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'Lemmas 2–4 / Corollary',
      'French 149-183 and the personally inspected full 400-dpi page and enlarged top, middle and bottom bands: '+why,kind=kind,count=count)
ch('\\footnote{The printed text gives a second\nformula ``(5.3)\'\' on page 182 and refers to it here; the identifier\n``(5.3 bis)\'\' distinguishes this formula from the first (5.3).}', '',
   'opening sentence','The editorial note is absent from the printed and corrected French text; the corrected reference and its justification remain in the ledger.',kind='translation')
ch("\\footnote{The printed text has $\\Osh_P(r+r')$; the two factors\n$\\Osh_P(m)$ and $\\Osh_P(m')$ require $\\Osh_P(m+m')$.}", '',
   'Lemma 2 proof','The editorial note is absent from the French text; retain the corrected m+m-prime twist and its separately recorded justification.',kind='translation')
align_math(rel,'en','149',183,[(i,i) for i in range(35)],(35,35))
ch('We use', 'One uses', 'notation paragraph','The source On utilise is impersonal.')
ch(r'Assertion (D) is true if $\symup{X=P}$ and $\symup{F=\Osh_P(m)}$.',
   r'\uline{Assertion} (D) \uline{is true if} $\symup{X=P}$ \uline{and} $\symup{F=\Osh_P(m)}$',
   'Lemma 2','Restore the printed assertion underlining, exclude (D), and remove the added terminal period.')
ch('mentioned above.\nFor the second, note that there is an isomorphism',
   'mentioned above;\nfor the second, one notes that one has an isomorphism',
   'Lemma 4 proof','Keep the source period whole and its impersonal on note and on a.')
ch('we obtain the', 'one obtains the', 'before Corollary','The source on trouve is impersonal.')
for start in [r'\result{LEMMA}{3} ',r'\result{LEMMA}{4} ',r'\result{COROLLARY}{} ']:
    t=page_text(rel,183)[0];old=t.split(start,1)[1].split('\n\n',1)[0]
    ch(old,underline_prose(old),'assertion prose','Restore underlined assertion prose while preserving the mathematical spans.')
record_translation_page('en','149',183,rel,
    'Read the end of the deduction of Theorem 2, the projective-space setup, Lemmas 2, 3 and 4, their explanations and the coeffaceability corollary. Removed two unprinted editorial footnotes while retaining the corrected 5.3 bis reference and m+m-prime twist. Approved all 35 formula correspondences, including the inline cup product and inline Ext vanishing; restored the source O(m) without an added X subscript in the displayed identification. Restored underlining and the impersonal register; kept the source long period in the proof of Lemma 4.',(742,798))
event('en-149-D-implies-theorem2','used and rechecked in this run',
    'Using the point-sheaf local Ext calculation already read in (4.2), assertion (D) for F=k_x first gives a one-dimensional nonzero L. Hence tensoring by L-prime is faithful, and the transpose of the evaluation isomorphism (5.3 bis) identifies with (5.4); (5.5) is therefore an isomorphism and sends the local fundamental generator to a basis of L. This rechecks the deduction from (D), not an independent proof of (D).',
    '149, pp. 182–183, (5.3 bis)–(5.5) and opening paragraph of p. 183')
event('en-149-lemma2','used and rechecked in this run',
    'Rechecked the twist m+m-prime in the cup product by O(m) tensor O(m-prime)=O(m+m-prime). For the projective-space case the usual homogeneous-monomial description pairs H^0(O(m)) with H^r(O(-m-r-1)) by the coefficient of the monomial having all exponents -1; the intermediate groups vanish. This checks the pairing mechanism used by the lemma; a full independent Cech calculation is not claimed.',
    '149, p. 183, Lemma 2 and its proof')
for sid,result in [
 ('lemma3','Read the large-positive-twist global generation statement and its deduction of a quotient of O_X(-m)^k; the cited global generation theorem is carried as background.'),
 ('lemma4','Read H^(r-i)(P,O_P(-m))=0 and Ext^i(O_X(-m),B)=H^i(B tensor O(m))=0 for i>0 and large m. The locally free Hom identification was rechecked; the projective-space computation and Serre vanishing are carried as background.'),
 ('corollary-p183','Read coeffaceability in the coherent-sheaf categories, using a surjection from a sufficiently negative finite sum and the preceding vanishings; no independent proof of the underlying vanishing theorem is claimed.')]:
    event('en-149-'+sid,'carried as background without fault found',result,'149, p. 183, '+sid)
update()
