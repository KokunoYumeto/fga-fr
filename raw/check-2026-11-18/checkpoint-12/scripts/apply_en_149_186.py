from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-186'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'Theorem 3 bis / Proposition 6',
      'French 149-186 and the personally inspected full 400-dpi page and enlarged top, middle and bottom bands: '+why,kind=kind,count=count)
align_math(rel,'en','149',186,[(i,i) for i in range(29)],(29,29))
ch('Now consider', 'Let us now consider','opening','Restore the authorial Considérons.')
ch('and compose them', 'and let us compose them','after (6.4)','Restore the authorial composons-les.')
ch('of (6.3). This gives functorial\nhomomorphisms, compatible with the boundary operators,',
   'of (6.3); one obtains functorial\nhomomorphisms, compatible with the boundary operators:',
   'after (6.4)','Keep the source period whole, retain on obtient, and restore the colon.')
ch('(6.1). With this understood, we have the following result.',
   '(6.1). With this understood, one has the',
   'before Theorem 3 bis','Retain impersonal on a and the source continuation directly into the theorem.')
ch(r'\textit{',r'\textnormal{','enumeration and proof labels','The source labels are roman, not italic.',count=12)
ch(r'\noindent\textbf{PROOF.} ---',r'\noindent PROOF. --',
   'proof label','Restore the source normal label and separator.')
ch('next proposition.', 'next proposition:', 'end of theorem proof','The source introduces the proposition with a colon.',kind='structure')
ch('sufficiently large, there is an isomorphism\n', 'sufficiently large, one has an isomorphism:\n',
   'Proposition 6','Restore on a and the colon before (6.6).')
ch('where we set (compare no. 3, Proposition 5)',r'\uline{where one sets} (compare no. 3, Proposition 5):',
   'before (6.7)','The source underlines only où on pose; restore its impersonal form and the final colon.')
for start,end in [(r'\result{THEOREM}{3 bis} ','\n\\begin{enumerate}'),(r'\result{PROPOSITION}{6} ','\n\\begin{equation}')]:
    t=page_text(rel,186)[0];old=t.split(start,1)[1].split(end,1)[0]
    ch(old,underline_prose(old),'statement introduction','Restore the source underlined prose.')
for label in ['i','ii','iii','iv']:
    start='\\item[\\textnormal{'+label+'.}] '
    t=page_text(rel,186)[0];rest=t.split(start,1)[1]
    old=rest.split('\n  \\item',1)[0].split('\n\\end{enumerate}',1)[0]
    ch(old,underline_prose(old),'Theorem 3 bis condition '+label,'Restore underlined condition prose, excluding formulas and the equation reference.')
record_translation_page('en','149',186,rel,
    'Read the trace pairings (6.4)–(6.5), all four conditions of Theorem 3 bis, each indicated implication, and Proposition 6 with its proof. Approved all 29 mathematical correspondences; in particular the source uses omega_P in condition iv and Omega_P in (6.7), which is harmless on nonsingular P and is retained literally. Restored the assertion underlining, twelve roman condition labels, the proof label, source periods and colons, and the authorial/impersonal forms.',(892,943))
event('en-149-theorem3bis','targeted proof check',
    'Rechecked the finite range n-k<=p<n: i implies ii by the Ext vanishing for sufficiently negative line bundles; ii implies iii by coherent quotients of finite sums of these line bundles. For iii implies i, use the common degree-zero identification at p=n and dimension shifting through the coeffaceable delta functors. For ii iff iv, Proposition 6 identifies the dual groups with H^0 of the corresponding E^(n-p) twist; global generation of large twists detects vanishing of each coherent sheaf. Only finitely many degrees are involved for a fixed k.',
    '149, p. 186, Theorem 3 bis, conditions i–iv and proof')
event('en-149-proposition6','used and rechecked in this run',
    'Rechecked r-i=(r-n)+(n-i): projective-space duality identifies H^i(F(-m)) dual with global Ext in degree r-i, and Lemma 5 identifies that Ext with H^0 of E^(n-i)(F)(m) for sufficiently large m. The source printed indices, signs and the comma in (6.6) are retained.',
    '149, p. 186, Proposition 6 and formulas (6.6)–(6.7)')
update()
