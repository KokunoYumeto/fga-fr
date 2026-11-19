from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'182-193',line,'1','400-dpi scan and enlarged top, middle and bottom bands. '+why,kind,count=count)
 r(r'\fsection{1}{Schémas}',r'\fsection{\normalfont1}{\normalfont\uline{Schémas}.}','section heading',why='The title is roman and underlined, with a final period outside the underline.')
 r('de type fini et, dans','de type fini et dans','first paragraph, line 5',why='There is no comma after et.')
 for a in ['classique','absolument irréductibles']:
  r('« '+a+' »',r'\fquote{'+a+'}','first paragraph, quoted expression',why='The original uses ordinary double quotes.')
 r('« topologie de Zariski »',r'\fquote{\uline{topologie de Zariski}}','second paragraph, lines 2–3',why='The quoted term is underlined and uses double quotes.')
 for a in ['espace annelé','spectre premier']:
  r(r'\emph{'+a+'}',r'\uline{'+a+'}','second paragraph, definition',why='The original emphasizes this term by underlining, not italics.')
 r(r'\Osh_X','O_X','second paragraph, structure sheaf',why='Here the O has no underline; the new exposé uses a different notation from 149.')
 r(r'\mathfrak p\longmapsto',r'\mathfrak p\longrightarrow','last line, assignment',why='The printed arrow has no mapsto bar.')
 upright_page(rel,layer,'182-193')
 base=f'sources/{tree}/tex/base.tex'
 replace(base,r'\begin{flushleft}\sffamily Séminaire BOURBAKI',r'\begin{flushleft}\normalfont Séminaire BOURBAKI',layer,'182-193','seminar heading','header','Scans 149-169 and 182-193 show roman seminar headings; remove the supplied sans-serif style while retaining the macro and all wording.','reading',full=True)
 replace(base,r'{\Large\bfseries #1\par}',r'{\Large\normalfont #1\par}',layer,'182-193','paper title','header','Scans 149-169 and 182-193 show ordinary roman paper titles, not a separate bold alphabet. The common title macro retains its layout and wording.','reading',full=True)
event('182-1-spectrum','carried as background without fault found','Read the introductory affine dictionary, the prime spectrum, local stalks A_p, its global sections A and the contravariant map induced by a ring homomorphism. The assignment is printed with an ordinary arrow; the ringed-space qualification continues on the following page. No independent re-proof is claimed.','182, p. 193, section 1')
record_page('182',193,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 3–44 with scan leaf 2 at 400 dpi and three enlarged bands. Read every introductory sentence, the prime-spectrum definition, the localization indices and both contravariant arrows.

Restored the section-title underline and period, absence of a comma after et, double quotes, definition underlines, the plain ununderlined O_X, the ordinary assignment arrow and upright typed variables. The field k here is plain, unlike exposé 149. The common seminar and paper-title macros were also restored to roman typography, as visible on both already-read title pages. The p ideal glyphs are handwritten Gothic forms and retain mathfrak. Both French layers agree; no misprint of the original has been asserted on this page.''')
p=read('CHECK_RECORD.md')
p=p.replace('| Structure sheaf | `\\Osh` = `\\underline{O}` | Upright ordinary underlined O, confirmed from 149-169 onward |','| Structure sheaf | `\\Osh` = `\\underline{O}`; plain `O` where printed | Underlined throughout exposé 149 except recorded omissions; exposé 182 begins with plain upright O_X |')
p=p.replace('| Field | `\\underline{k}` | Underlined field k; integer indices k remain plain |','| Field | `\\underline{k}` or plain `k` | Underlined in exposé 149; plain upright in 182-193; integer indices remain plain |')
write('CHECK_RECORD.md',p)
from update_record_counts import update
update()
