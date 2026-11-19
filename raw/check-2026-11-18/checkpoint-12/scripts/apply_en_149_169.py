from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-169'
start_unit('en','149',rel)
align_math(rel,'en','149',169,[(i,i) for i in range(33)],(33,33))
def change(old,new,where,evidence,kind='translation'):
    replace(rel,old,new,'English',page,where,'section 1',
        'French 149-169 and the personally inspected 400-dpi scan with three enlarged page bands: '+evidence,kind=kind)
change('Cartan--Eilenberg','Cartan-Eilenberg','opening paragraph','The compound name has the same short hyphen as in the source.',kind='typesetting')
change(r"\fsection{1}{The Ext's of sheaves of modules ({[2]}, Chapters 3 and 4)}",
       r"\fsection{\normalfont1}{\normalfont\underline{The} Ext's \underline{of sheaves of modules} ({[2]}, Chapters 3 and 4).}",
       'section heading','The heading underlines the words around Ext and ends with a period; source emphasis is required by the all/register standard.',kind='terminology')
change('We consider the abelian category','One considers the abelian category','first definition paragraph',
       'On considère is impersonal. Apply DECISIONS all/register and the English register standard.',kind='terminology')
change('the\nabelian group of','the\nabelian '+r'\underline{group}'+' of','Hom group definition',
       'The source emphasizes groupe, distinct from the following sheaf.',kind='terminology')
change('will denote the sheaf of germs','will denote the '+r'\underline{sheaf}'+' of germs','Hom sheaf definition',
       'The source emphasizes faisceau, distinct from the preceding group.',kind='terminology')
change('we define functors','one defines functors','definition of h and underlined h',
       'On définit is impersonal, not an authors’ nous. Apply the all/register standard.',kind='terminology')
change('are covariant left-exact functors. We consider\ntheir right derived functors, denoted respectively by',
       'are covariant left-exact functors; one considers\ntheir right derived functors, denoted respectively by',
       'paragraph before (1.2)','The French gives one sentence with impersonal on. Apply the register standard without changing its content.',kind='terminology')
change(r'$\symup{B\longrightarrow H^{p}(X,B)}$',r'$\symup{B\longrightarrow H^{p}(X,B)}$:',
       'last line','The inline notation leads into (1.3) with a colon; the source has a plain right arrow and no separate display.',kind='structure')
record_translation_page('en','149',169,rel,
    'Read every prose paragraph against the French, retaining the existing translation except for the prescribed impersonal register and source emphasis. Approved all 33 outer math-span pairings: plain Z in the category exponent, straight Hom/Ext and h underlines, upright typed letters, exact (1.1) and (1.2) punctuation, and the final two formulas inline with a plain right arrow. Dates, references [2]/[3], chapter numbers, title and author were checked in the image. No mathematical change to the French was needed. The assertions about injective resolutions and derived functors are carried as background here.',(3,63))
event('en-149-section1-definitions','carried as background without fault found',
    'Paragraphwise English comparison completed for p. 169 with the scan open. Formula alphabets, tags and the distinction between the Hom group and Hom sheaf were rechecked; existence of injective resolutions and the general derived-functor formalism were not independently reproved in this translation reading.',
    '149, p. 169, section 1, definitions and (1.1)–(1.2)')
update()
