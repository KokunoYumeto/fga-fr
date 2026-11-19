from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex'
for page,old,new,n,loc in [
 (172,'connecting','coboundary',6,'opening and composition paragraphs'),
 (182,'connecting\nhomomorphisms','coboundary\nhomomorphisms',1,'after (5.2)'),
 (184,'connecting homomorphisms','coboundary operators',1,'proof after Lemma 5')]:
    replace(rel,old,new,'English',f'149-{page}',loc,'cobord terminology',
       f'Corrected French 149-{page}; original 400-dpi enlarged crops reopened personally at the end of the unit. The source says cobord(s), rendered coboundary by the supplied GLOSSARY_SGA_EN_UNIFIED.tsv, cobord row. On page 184 the source noun is opérateurs. The separately printed bord on page 186 remains boundary.',kind='terminology',count=n)
with (ROOT/'CHECK_RECORD.md').open('a') as out:
    out.write('\n**Unit terminology follow-up.** '+utc()+'. Reopened enlarged crops for 149-172 (top/middle), 182 (top), 184 (middle/bottom) and 186 (top). Applied the supplied glossary cobord → coboundary in eight places on the first three pages, retaining the printed noun operators on p. 184. The p. 186 source reads bord, so boundary is retained. The two p. 190 cobord occurrences were already aligned during that page reading. This is part of the first translation reading, not the mandatory later correction-row review.\n')
finish_unit('en','149','All 25 printed pages 169–193, including the bibliography and April 1959 addendum, have been personally compared paragraph by paragraph with corrected French, with the full 400-dpi scan and all relevant enlarged bands inspected. All current page corrections are logged; mathematical decisions distinguish actual proof checks from background reading. The mandatory second correction-row reading and final PDF inspection remain pending.')
update()
