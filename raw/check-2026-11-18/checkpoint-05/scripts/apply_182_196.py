from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'182-196',line,statement,'400-dpi scan and three enlarged bands. '+why,kind,count=count)
 r("\\emph{faisceau cohérent d'anneaux locaux\nnoethériens}","faisceau \\uline{cohérent} d'anneaux \\uline{locaux\nnoethériens}",'first paragraph','2',why='Only cohérent and locaux noethériens are underlined.')
 for word in ['localement','affine']:
  r('\\emph{'+word+'}','\\uline{'+word+'}','second paragraph','2',why='The word is underlined, not italic.')
 txt,_,_=page_text(rel,196)
 r(r'\Osh','O','structure sheaf symbols','2;3',why='Each O is plain and ununderlined.',count=txt.count(r'\Osh'))
 r(r'\fsection{3}{Les trois théorèmes fondamentaux}',r'\fsection{\normalfont3}{\normalfont\uline{Les trois théorèmes fondamentaux}.}','section heading','3',why='Roman underlined heading with a final period.')
 r("toujours), soit $Y'$","toujours), soient $Y'$",'section 3, first paragraph','3',why='The scan has the plural soient.')
 r("dans $X$ ;\nconsidérons","dans $X$,\nconsidérons",'section 3, first paragraph','3',why='A comma follows X.')
 if tree=='fr_printed':
  r(r'\overline f:\overline X\longrightarrow\overline Y',r'\overline f:\overline X\longrightarrow\overline X','section 3, completed morphism','3-completed-morphism',why='The enlarged image clearly prints a barred X as target. Corrected French retains barred Y, required by f:X→Y and all following target sheaves.')
 r('de $X,Y,f,F$.)','de $X,Y,f,F$).','end of parenthetical proof limitation','3',why='The period is outside the closing parenthesis.')
 # Keep the existing result macro and add an optional punctuation argument.
 base=f'sources/{tree}/tex/base.tex'
 replace(base,r'''\newcommand{\result}[2]{%
  \par\medskip\noindent\textnormal{#1%
  \if\relax\detokenize{#2}\relax\else\space#2\fi. -}\enspace
}''',r'''\newcommand{\result}[3][. -]{%
  \par\medskip\noindent\textnormal{#2%
  \if\relax\detokenize{#3}\relax\else\space#3\fi#1}\enspace
}''',layer,'182-196','Theorem 1 heading','3-thm1','The scan has a period without a dash. An optional punctuation argument preserves the existing macro and all earlier default punctuation.','typesetting',full=True)
 r(r'\result{THÉORÈME}{1 (théorème de finitude)}',r'\result[.]{THÉORÈME}{1 (théorème de finitude)}','Theorem 1 heading','3-thm1',why='The printed heading ends with a period only.')
 r(r'\item[\textit{i.}] Les',r'\item[\textnormal{i.}] \uline{Les}','Theorem 1(i)','3-thm1-i',why='Roman list marker and underlined prose.')
 r('sont des faisceaux\n    cohérents sur $\\overline Y$.','\\uline{sont des faisceaux\n    cohérents sur} $\\overline Y$.','Theorem 1(i)','3-thm1-i',why='The prose is underlined, not the formula or final punctuation.')
 r(r'\item[\textit{ii.}] Les homomorphismes naturels',r'\item[\textnormal{ii.}] \uline{Les homomorphismes naturels}','Theorem 1(ii)','3-thm1-ii',why='Roman list marker and underlined prose.')
 r('    sont des isomorphismes.','    \\uline{sont des isomorphismes.}','Theorem 1(ii), conclusion','3-thm1-ii',why='The concluding sentence including its period is underlined.')
 r(r'\varprojlim_n',r'\varprojlim\limits_n','Theorem 1(ii), displayed limit','3-thm1-ii',why='The n is below the inverse-limit arrow.')
 r('« cohomologie formelle »',r'\fquote{cohomologie formelle}','last line','3',why='Ordinary double quotes appear in print.')
 upright_page(rel,layer,'182-196')
event('182-3-completed-morphism','targeted proof check','The scan prints barred f:barred X→barred X. Completion of f:X→Y along X-prime=f^{-1}(Y-prime) has target barred Y, also the base of the following direct-image sheaves. Retain the existing supplied Y only in corrected French; restore printed X in the as-printed layer.','182, p. 196, section 3, first paragraph')
event('182-2-affine-formal','carried as background without fault found','Read coherence, local noetherianity, local completion form and the equivalence of affine formal schemes with separated complete noetherian adic rings. These claims are stated without proof here; no independent proof is claimed.','182, p. 196, first two paragraphs')
event('182-3-thm1','carried as background without fault found','Read both finiteness and inverse-limit assertions, with bars and transition indices checked in the scan. The author explicitly says that a complete proof had only been written for the case induced from X,Y,f,F. The general formal-scheme assertion is not certified by this reading.','182, p. 196, Theorem 1 and preceding parenthesis')
record_page('182',196,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 135–185 with scan leaf 5 at 400 dpi, then all three enlarged bands. Read every line, the completed morphism, both clauses of Theorem 1 and its limit formula; all bars, primes, exponents and subscripts were enlarged.

Restored the precise underlining, plain structure-sheaf O, roman theorem markers, heading punctuation, plural soient, two punctuation readings and ordinary double quotation marks. The result macro now accepts optional punctuation, preserving its prior default; Theorem 1 uses the printed period without a dash. The printed morphism target is barred X, restored in the printed layer. Corrected French retains barred Y, justified by completion of f:X→Y. The author’s proof limitation is preserved and explicitly recorded; the formal finiteness theorem is carried as background pending the later argument, not claimed independently proved.''')
from update_record_counts import update
update()
