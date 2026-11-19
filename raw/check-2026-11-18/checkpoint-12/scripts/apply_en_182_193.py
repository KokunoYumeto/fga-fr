from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-193'
def ch(old,new,where,why,kind='terminology'):
    replace(rel,old,new,'English',page,where,'Section 1',
      'French 182-193 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands: '+why,kind=kind)
align_math(rel,'en','182',193,[(i,i) for i in range(21)],(21,21))
ch('\\fsection{1}{Schemes}','\\fsection{\\normalfont1}{\\normalfont\\uline{Schemes}.}',
   'section heading','Restore the printed normal number, underlined heading and final period.',kind='structure')
ch('“Zariski topology”','“\\uline{Zariski topology}”','spectrum paragraph','Restore printed emphasis within the quotation.')
for word in ['ringed space','prime spectrum']:
    ch('\\emph{'+word+'}','\\uline{'+word+'}','spectrum paragraph','Restore underlined rather than italic emphasis.')
record_translation_page('en','182',193,rel,
    'Compared both paragraphs and the title/date. Approved all 21 mathematical correspondences, retaining the printed ordinary O_X, Gothic prime ideal and plain arrow for the element assignment. Restored section and definition emphasis. The historical discussion of nilpotents and the distinction between the affine algebra and its spectrum are faithfully retained; stalk is already the standard rendering of fibre at a point.',(3,44))
event('en-182-1-spectrum','carried as background without fault found',
    'Read the affine algebra/spectrum correspondence, stalk localization and inverse-image prime-ideal map. These standard constructions are carried as background in this paragraphwise translation check; no independent proof is claimed.',
    '182, p. 193, section 1')
update()
