from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-185'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'(D) / section 6',
      'French 149-185 and the personally inspected full 400-dpi page and enlarged top, middle and bottom bands: '+why,kind=kind,count=count)
ch("\\footnote{The printed text also numbers this formula ``(6.2)''; the suffix\n``bis'' distinguishes the two occurrences.} ", '',
   'after (6.2 bis)','The editorial explanation is absent from the French text. Retain the corrected identifier and its separately recorded justification.',kind='translation')
align_math(rel,'en','149',185,[(i,{13:14,14:13}.get(i,i)) for i in range(31)],(31,31),localized={17:[('pour ','for ')]})
ch('on $\\symup{P}$, we write','on $\\symup{P}$, one writes:',
   'first paragraph','The source on écrit is impersonal and ends with a colon before the display.')
ch(r'\fsection{6}{The duality theorem for singular varieties}',r'\fsection{\normalfont6}{\normalfont\uline{The duality theorem for singular varieties}.}',
   'section 6 heading','Restore the source heading font, underlining and period.')
ch('where we have set','where one has set','before (6.2)','The source on a posé is impersonal.')
ch('the chosen embedding','the chosen immersion','after (6.2)','Use immersion for the printed immersion, as required by the English terminology standard.')
ch('in (6.1), we obtain','in (6.1), one obtains','before (6.2 bis)','The source on trouve is impersonal.')
ch('$\\symup{\\underline{\\omega}_X^{n}}$:\n', '$\\symup{\\underline{\\omega}_X^{n}}$ into itself:\n',
   'identity homomorphism','Retain the explicit source dans lui-même.',kind='translation')
record_translation_page('en','149',185,rel,
    'Read the completion of (D), the projective-space vanishing argument, the section 6 opening, the dualizing sheaf and its trace through (6.3). Approved all 31 mathematical pairings, explicitly crossing the reordered P and O_X occurrences in the prose; translated pour within the vanishing display. Preserved the corrected 6.2 bis label while removing its unprinted footnote. Restored Omega and omega underlines, the field underline, source punctuation, the heading, immersion, and impersonal on forms.',(842,892))
event('en-149-D-completion','used and rechecked in this run',
    'Read the normalization through (5.6)–(5.7) and the reduction to negative twists. For p<n one has r-p>r-n; the regular closed immersion of nonsingular X in nonsingular P gives projective dimension r-n for O_X locally, so the sheaf Ext in degree r-p vanishes. Lemma 5 then gives the global Ext vanishing after a large twist. Together with Lemma 4 this supplies the required coeffaceability. No new independent construction of the trace normalization is claimed.',
    '149, p. 185, completion of the proof of (D)')
event('en-149-6.1-through-6.3','carried as background without fault found',
    'Read the top-degree duality for a possibly singular closed X, omega_X^n as the sheaf Ext in codimension r-n, independence of the chosen immersion as referred to Proposition 5, and the functional corresponding to the identity of omega_X^n. Kept a plain arrow for the trace in (6.3); the text does not assert it is an isomorphism in this generality.',
    '149, p. 185, section 6, (6.1), (6.2), (6.2 bis), (6.3)')
update()
