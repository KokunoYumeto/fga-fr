from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-171'
def ch(old,new,where,why,kind='translation',full=False,count=1):
    replace(rel,old,new,'English',page,where,'Proposition 3 / section 2',
      'French 149-171 and the personally inspected full 400-dpi scan and three enlarged page bands: '+why,kind=kind,full=full,count=count)
note=r'''\footnote{The printed text reads “with $u$”; equation (2.1) requires
“with $d$.”}'''
ch(note,'','after (2.1)','This editorial note has no counterpart in the retained French text; the correction is explained separately in the audit.',kind='structure')
seq=r'''\[
  0\longrightarrow K'\longrightarrow K\longrightarrow K''\longrightarrow 0,
\]'''
ch(seq+'\n'+r'\src{172}',r'\src{172}'+'\n'+seq,'page boundary',
   'Printed p. 171 ends at complexes; the following exact sequence starts p. 172. Move only the page marker.',kind='structure',full=True)
align_math(rel,'en','149',171,[(i,i) for i in range(51)],(51,51),localized={34:[('où ','where ')]})
t=page_text(rel,171)[0];old=t.split(r'\result{PROPOSITION}{3} ',1)[1].split('\n\n',1)[0]
ch(old,underline_prose(old),'Proposition 3 prose','The assertion prose is underlined in the source; the two Ext signs have no added star exponents.',kind='terminology')
ch('cohomological\nbifunctors',r'\uline{cohomological bifunctors}','end of section 1','The phrase bifoncteurs cohomologiques is underlined.',kind='terminology')
ch(r'\fsection{2}{Composition law in Ext}',r'\fsection{\normalfont2}{\normalfont\uline{Composition law in} Ext.}',
   'section heading','Restore the printed underline span and terminal period.',kind='terminology')
ch('We denote by','One denotes by','graded Hom definition','On désigne is impersonal under the register standard.',kind='terminology')
ch('we equip','one equips','differential definition','On introduit is impersonal under the register standard.',kind='terminology')
ch('anticommute with','commute with','cycle condition',
   'Carry the corrected French commutent à d into English: delta(u)=0 gives du=(-1)^n ud, graded commutation. In degree zero the identity is a cycle, so graded anticommutation is wrong in characteristic different from two.')
ch('We may therefore consider','One may therefore consider','after cycle condition','On peut is impersonal under the register standard.',kind='terminology')
ch('respectively','resp.','module actions','The source uses resp. twice; preserve its abbreviation under the standard.',kind='terminology',count=2)
ch('composition of morphisms of complexes','composition of permitted homomorphisms of complexes','degree-zero composition',
   'The source explicitly says homomorphismes permis de complexes; retain the qualifier rather than silently dropping it. Its interpretation belongs in the notes.')
record_translation_page('en','149',171,rel,
    'Read all prose and approved all 51 math-span pairings after removing the editorial note and moving the next page marker before its exact sequence. Restored the ordinary underlined C in section 2, unindexed Ext in Proposition 3, inline Hom pairing, plain assignment arrow and exact tags. Propagated graded commutation with d, checked directly from (2.1); retained the source qualifier permitted in the degree-zero sentence. Applied the specified impersonal register, resp. and source emphasis. French grammar correction formée needs no separate English change.',(115,171))
event('en-149-2.1','used and rechecked in this run',
    'Rechecked the corrected cycle condition: delta(u)=du+(-1)^(n+1)ud=0 is equivalent to du=(-1)^n ud. For n=0, identity commutes with d and is a cycle; it does not anticommute in general. The corresponding English sentence now says commute with d as homogeneous operators. No new proof of the full Ext-composition theorem is claimed.',
    '149, p. 171, (2.1) and following sentence')
update()
