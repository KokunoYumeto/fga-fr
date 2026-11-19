from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/149.tex';page='149-176'
def ch(old,new,where,why,kind='terminology',count=1):
    replace(rel,old,new,'English',page,where,'Corollary 2 / Proposition 5',
      'French 149-176 and the personally inspected full 400-dpi page and enlarged top, middle and bottom bands: '+why,kind=kind,count=count)
ch('the case $M=A/J$;','the case where $M$ is of the form $A/J$;',
   'local algebra reduction','The source separates M and A/J by est de la forme; retain its formula boundaries.')
align_math(rel,'en','149',176,[(i,i) for i in range(52)],(52,52))
ch('respectively','resp.','opening of Corollary 2','Keep the printed abbreviation.',count=2)
ch('isomorphisms\n\\begin{equation}\\tag{3.6}',
   'isomorphisms:\n\\begin{equation}\\tag{3.6}','opening of Corollary 2','Restore the printed colon.')
ch('the definition of',r'the \uline{definition} of','after (3.6 bis)','The source emphasizes definition.')
ch('we may suppose','one may suppose','local proof','The source on peut is impersonal.')
ch('first assertion, argue by induction','first assertion, one proceeds by induction','local proof','The source on procède is an impersonal assertion, not an imperative.')
ch('choice of embedding of the algebraic space','way of immersing the algebraic space','independence assertion','Translate immerger by the immersion terminology without imposing an extra closed-embedding interpretation.')
ch('“dimension”',r'\fquote{dimension}','local ideal','Keep the source quotation marks.')
ch('“system of parameters,” as in',r'\fquote{system of parameters} as in','local reduction','Keep the source quoted technical phrase and punctuation.')
ch('$\\symup{\\operatorname{Ext}}$ groups','$\\symup{\\operatorname{Ext}}$','exact sequence','Retain the source Ext notation without an added noun.',kind='translation')
ch('$\\symup{\\operatorname{Ext}_{A}^{p}(M,A)\n=\\operatorname{Hom}_{A}\\!\\left(M,\\operatorname{Ext}^{p}(A/J,A)\\right)}$\nwhere',
   '$\\symup{\\operatorname{Ext}_{A}^{p}(M,A)\n=\\operatorname{Hom}_{A}\\!\\left(M,\\operatorname{Ext}^{p}(A/J,A)\\right)}$,\nwhere',
   'local comparison formula','The expression is inline in the source and followed by a comma.',kind='structure')
old=page_text(rel,176)[0].split('\n',1)[1].split('\\begin{equation}',1)[0].rstrip()
new=r'''\uline{Let} $\symup{\underline{\Omega}_X}$ (resp. $\symup{\underline{\Omega}_Y}$) \uline{be the sheaf of germs of regular
differential forms on} $\symup{X}$ (resp. $\symup{Y}$). \uline{Then there are canonical
isomorphisms}:'''
ch(old,new,'opening assertion','Restore exactly the source prose emphasis, leaving both parenthetical resp. phrases ununderlined.')
ch('or equivalently\n',r'\uline{or equivalently}'+'\n','between (3.6) and (3.6 bis)','The connecting phrase is underlined.')
for start,end in [(r'\result{PROPOSITION}{5} ','\n\\begin{equation}'),('where $\\symup{J}$ denotes','\n\\begin{equation}'),('Finally, still taking','\n\n')]:
    t=page_text(rel,176)[0]
    if start.startswith('\\result'):old=t.split(start,1)[1].split(end,1)[0]
    else:old=start+t.split(start,1)[1].split(end,1)[0]
    ch(old,underline_prose(old),'Proposition 5 assertion prose','Restore the underlined assertion prose; formulas remain outside prose underlining.')
record_translation_page('en','149',176,rel,
    'Read the continuation of Corollary 2, the full statement of Proposition 5 and the first proof paragraph. Approved all 52 math correspondences after restoring the two source expressions M and A/J. Restored underlined Omega throughout, the printed omitted inner Ext base subscripts, the inline E^i definition and local Ext comparison, exact tags and punctuation. Applied resp., impersonal on, immersion terminology and the source emphasis. Kept the historical phrase algebraic space without an inserted modern interpretation. The vanishing, canonical comparison and embedding-independence claims remain background in this language pass.',(368,423))
event('en-149-proposition5','carried as background without fault found',
    'Read the dimension q=n-p, support and locally free hypotheses, vanishing for i<p, comparison in degree p, the annihilator ideal conditions, the Y-module specialization and immersion independence of the E^i sheaves. Checked (3.6), (3.6 bis), (3.7), (3.7 bis), their base-ring subscripts and the proof references against the printed image. The proof continues on p. 177; no independent proof of the full proposition is claimed here.',
    '149, p. 176, Corollary 2 and Proposition 5')
update()
