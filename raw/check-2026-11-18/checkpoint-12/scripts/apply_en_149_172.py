from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-172'
def ch(old,new,where,why,kind='translation',count=1):
    replace(rel,old,new,'English',page,where,'section 2 / (2.3)–(2.5)',
      'French 149-172 and the personally inspected full 400-dpi scan and enlarged top, middle and bottom crops: '+why,kind=kind,count=count)
ch('a category in which every object $A$ admits','a category such that every object $A$ of $C$ admits',
   'injective resolutions','Retain the explicit of C in the source and its repeated category symbol; the hypotheses are unchanged.',kind='terminology')
align_math(rel,'en','149',172,[(i,i) for i in range(26)],(26,26))
ch("$\\symup{0\\longrightarrow K'\\longrightarrow K\\longrightarrow K''\\longrightarrow 0}$\nsuch that",
   "$\\symup{0\\longrightarrow K'\\longrightarrow K\\longrightarrow K''\\longrightarrow 0}$, such that",
   'opening exact sequence','The sequence is inline in the scan, followed by a comma.',kind='structure')
ch("$\\symup{H^{i}(K',L)\\longrightarrow H^{i+1}(K'',L)}$\nThe connecting",
   "$\\symup{H^{i}(K',L)\\longrightarrow H^{i+1}(K'',L)}$.\nThe connecting",
   'connecting operator','The coboundary map runs inline and ends the sentence.',kind='structure')
ch('$\\symup{\\operatorname{Ext}}$ groups.','$\\symup{\\operatorname{Ext}}$.',
   'last sentence','The French says between the Ext, without an added noun groups; retain its functor notation.')
record_translation_page('en','149',172,rel,
    'Compared every paragraph, including the termwise split exact sequence, both bicomplex identifications, the associative composition pairing, its ring case and the sheaf pairings. Approved all 26 math correspondences after restoring the explicit category symbol in the hypothesis. Restored the opening sequence and connecting map to inline form, ordinary C in the general category, the printed category alphabet in the sheaf case, underlined sheaf Hom/Ext and the exact absence of terminal punctuation in (2.3)–(2.5). The compatibility and bicomplex claims were read as background; no additional proof is claimed.',(165,221))
event('en-149-2.3-2.5','carried as background without fault found',
    'Read the composition and sheaf pairings paragraph by paragraph against corrected French and checked the full printed image and enlarged crops. The exact sequence is termwise split, and the connecting map has source H^i(K prime,L) and target H^(i+1)(K double-prime,L). Formula degrees p,q,p+q and the reference (1.8) agree. No independent proof of the bicomplex or compatibility statements was performed here.',
    '149, p. 172, section 2 and (2.3)–(2.5)')
update()
