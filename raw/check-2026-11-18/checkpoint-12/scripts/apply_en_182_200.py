from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-200'
def ch(old,new,where,why,kind='terminology',full=False,count=1):
    replace(rel,old,new,'English',page,where,'Theorem 5, Corollaries 1–2, Theorem 6 and section 5',
      'French 182-200 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands: '+why,kind=kind,full=full,count=count)
old='separated,\\footnote{The 1962 erratum replaces the printed hypothesis “$f$ is\nquasi-projective” by the weaker hypothesis “$f$ is separated,” by SGA VIII,\n6.2: every separated quasi-finite morphism is quasi-projective.}'
ch(old,'quasi-projective,','Theorem 6 hypothesis','The printed theorem assumes quasi-projectivity. The corrected French retains this original hypothesis because the later generalization belongs in the separate errata. Remove the unprinted explanatory footnote and undo its merged hypothesis.',kind='translation')
whole=read(rel);start=whole.index('assumed flat over $Y$');end=whole.index('\\src{201}',start)+len('\\src{201}')
old=whole[start:end];new='\\src{201}\n'+old[:-len('\\src{201}')]
ch(old,new,'printed page break in section 5','The printed page ends after the coherent sheaf on X is introduced. Move the existing page marker before the flatness assumption, keeping all intervening text.',kind='structure',full=True)
align_math(rel,'en','182',200,[(i,i) for i in range(53)],(53,53))
text,_,_=page_text(rel,200);body=text.split('that is, ',1)[1].split('\n\n',1)[0]
ch(body,underline_prose(body),'Theorem 5 continuation','Restore the printed statement emphasis, leaving the introductory that is unaccented.')
text,_,_=page_text(rel,200);body=text.split(r'\result{COROLLARY}{1} ',1)[1].split('\n\n',1)[0]
ch(body,underline_prose(body).replace(r'\uline{where}', 'where'),'Corollary 1','Restore statement emphasis while leaving the parenthetical definition of y-prime unaccented.')
ch("isomorphism $\\symup{O_{y'}\\longrightarrow O_x}$", "\\uline{isomorphism} $\\symup{O_{y'}\\longrightarrow O_x}$",'Corollary 1 proof','Restore emphasis on the asserted stalk isomorphism.')
ch('Chevalley','CHEVALLEY','attribution of Corollary 2','Restore printed capitalization.',kind='reading')
text,_,_=page_text(rel,200);body=text.split(r'\result{COROLLARY}{2} ',1)[1].split('\n\n',1)[0]
ch(body,underline_prose(body),'Corollary 2','Restore statement emphasis.')
ch("Zariski's Main Theorem", "Zariski's “Main Theorem”",'Theorem 6 introduction and heading','Restore the source quotation marks.',kind='structure',count=2)
text,_,_=page_text(rel,200);body=text.split(r"\result{THEOREM}{6 (Zariski's “Main Theorem”)} ",1)[1].split('\n\n',1)[0]
ch(body,underline_prose(body),'Theorem 6','Restore statement emphasis around the printed quasi-projectivity hypothesis.')
ch(r'\textit{a fortiori}',r'\uline{a fortiori}','local forms of Theorem 6','Restore underlining in place of italic emphasis.')
ch(r'\fsection{5}{Application to the cohomological study of proper flat morphisms}',
   r'\fsection{\normalfont5}{\normalfont\uline{Application to the cohomological study of proper and flat morphisms}.}',
   'section 5 heading','Restore the conjunction, underlined roman heading and final period.',kind='structure')
record_translation_page('en','182',200,rel,
    'Read the continuation of Theorem 5, its two corollaries and proofs, the compactification argument and Theorem 6, and the opening of section 5. Approved the 53 explicit formula correspondences after restoring the page-201 boundary. Replaced tilde notation by the source bars. The English already carries the corrected f-prime pushforward and the unbarred f in the quasi-projectivity example. Undid the merged later erratum in Theorem 6, restoring quasi-projective and removing its unprinted explanatory footnote. Restored source emphasis and quotation typography.',(330,406))
event('en-182-Theorem5-Corollary1','targeted proof check',
    'Checked the stated argument using properness and Theorem 5. A point isolated in a connected fiber makes that fiber a singleton. Properness makes images of closed complements closed; the singleton-fiber locus U maps homeomorphically onto an open V. The equality f-prime_*O_X=O_Y-prime and the cofinal inverse-image neighborhoods give the claimed stalk isomorphisms on U. Thus the restricted ringed-space map is an isomorphism. This check uses the connectedness theorem as its input.',
    '182, p. 200, Corollary 1 and following paragraph')
event('en-182-Theorem5-Corollary2','targeted proof check',
    'Checked the deduction from Corollary 1: finite fibers of a proper f make every connected fiber of f-prime a singleton, so f-prime is an isomorphism and f identifies with the finite Stein factor g. The converse is the usual properness and finite-fiber property of finite morphisms, carried as background.',
    '182, p. 200, Corollary 2')
event('en-182-Theorem6','carried as background without fault found',
    'Read the compactification sketch and original quasi-projective version of the Main Theorem. Restored that version in English; the later separated generalization remains in its erratum. No independent proof of the general theorem is claimed here.',
    '182, p. 200, Theorem 6 and preceding compactification paragraph')
update()
