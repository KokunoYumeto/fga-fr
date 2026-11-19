from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/149.tex'
    def r(a,b,line,statement='',kind='reading'):
        replace(rel,a,b,layer,'149-173',line,statement,'400-dpi scan and enlarged top/middle/bottom crops show the replacement reading.',kind)
    r('structures multiplicatives ; de façon','structures multiplicatives, de façon','3')
    r("qui, pour l'aboutissement,","qui, pour l'aboutissement",'5')
    r(r'H^{0}\bigl(X,\Extsh',r'H^{0}\bigl(X;\Extsh','10','2.6')
    r('\\end{equation}\net\n\\begin{equation}\\tag{2.7}','\\end{equation}\n\\begin{equation}\\tag{2.7}','10–11','2.6–2.7','structure')
    r(r'\fsection{3}{Résultats de cohomologie locale}',r'\fsection{\normalfont3}{\normalfont\uline{Résultats de cohomologie locale}.}','section heading','3')
    r(r'M\otimes A/J\right),\\',r'M\otimes A/J\right)\\','3.1 first display line','3.1')
    r(r'\otimes\operatorname{Hom}_{A}(A/J,M),',r'\otimes\operatorname{Hom}_{A}(A/J,M)','3.1 second display line','3.1')
    r("de points de $J$, d'homomorphismes","de points de $J$ d'homomorphismes",'paragraph before 3.2','3')
    r(r'&\longrightarrow M\otimes A/J,\\',r'&\longrightarrow M\otimes A/J\\','3.2 first display line','3.2')
    r(r'\operatorname{Tor}_{p}^{A}(A/J,M),',r'\operatorname{Tor}_{p}^{A}(A/J,M)','3.2 second display line','3.2')
    upright_page(rel,layer,'149-173')
event('149-eq2.6–2.7','carried as background without fault found','Read the two edge homomorphisms and the multiplicative-compatibility assertion; no proof reconstruction claimed. The semicolon in H^0(X; Ext) is retained literally.','149, printed p. 173, displays (2.6) and (2.7)')
event('149-eq3.1–3.2','carried as background without fault found','Read all arrows, tensor/exterior powers and degrees; the constructions are continued on the following page.','149, printed p. 173, displays (3.1) and (3.2)')
record_page('149',173,r'''Compared both French files, `sources/fr/fr/149.tex` and `sources/fr_printed/fr/149.tex`, the interval `\src{173}` to before `\src{174}`, against PDF leaf 6 at 400 dpi and three enlarged bands. Read every sentence, both edge homomorphisms, the local-cohomology heading, both paired displays (3.1)–(3.2), and all degrees, subscripts, arrows and underlines.

Restored the comma after multiplicatives, absence of a comma after aboutissement, the semicolon in H^0(X; Ext), the absence of an added et between (2.6) and (2.7), the underlined heading and its period, and the absence of commas after both lines of (3.1), after J in the following paragraph, and after both lines of (3.2). Typed mathematical variables are upright. No correction of the original's mathematics was made on this page. Both French layers have the same readings. The final second reading, translations and PDF inspection remain pending.''')
