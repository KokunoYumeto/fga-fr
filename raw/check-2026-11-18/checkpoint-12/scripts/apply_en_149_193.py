from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-193'
def ch(old,new,where,why,kind='terminology'):
    replace(rel,old,new,'English',page,where,'Addendum',
        'French 149-193 and the personally inspected full 400-dpi image and enlarged complete text crop: '+why,kind=kind)
ch('\\section*{ADDENDUM}','\\section*{\\centering\\normalfont ADDENDUM}',
   'heading','Restore centered normal face.',kind='structure')
ch('“theory of schemes,”','“theory of schemes”,','first paragraph','Keep the comma outside the quoted expression, as in the source.',kind='structure')
ch('“Éléments de Géométrie algébrique” of J. Dieudonné and A. Grothendieck',
   '“Eléments de Géométrie algébrique” of J. DIEUDONNÉ and A. GROTHENDIECK',
   'first paragraph','Restore the exact printed title and author capitalization.')
ch('Some indications may be found in:','One will find some indications in:',
   'first paragraph last sentence','Retain impersonal on and the future trouvera.')
ch('Grothendieck (A.). ---','GROTHENDIECK (A.). -','bibliographic entry','Restore printed capitalization and separator.')
ch('\\emph{International Congress of Mathematicians}',
   'Int. Congress of Mathematicians','bibliographic entry','Restore the abbreviated int. and normal face of Congrès int. des Mathématiciens.')
record_translation_page('en','149',193,rel,
    'Read the entire April 1959 addendum, its original page-13 reference, the EGA title, conference entry and date. No formulas occur. Preserved the announcement as historical text, including currently in preparation and to appear. Restored heading and bibliographic typography, the exact cited title and impersonal future.',(1303,1326))
event('en-149-addendum','carried as background without fault found',
    'Compared the announcement of extension of duality to arbitrary singularities and the two references. This is read as the historical April 1959 announcement; the cited future work has not been used as proof in this translation pass.',
    '149, p. 193, Addendum')
update()
