from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'182-195',line,statement,'400-dpi scan and three enlarged bands, including every power and limit index. '+why,kind,count=count)
 for a in ['morphisme projectif','morphisme propre',"faisceau cohérent d'anneaux",'schéma formel']:
  r(r'\emph{'+a+'}',r'\uline{'+a+'}','definition of '+a,why='The definition is underlined, not italic.')
 r('de type fini ; de plus','de type fini, de plus','paragraph 1, line 3','1',why='The scan has a comma.')
 r('(noethérien, comme toujours), le','(noethérien, comme toujours) le','paragraph 2, first line','1',why='There is no comma after the parenthesis.')
 r(r'\fsection{2}{Schémas formels}',r'\fsection{\normalfont2}{\normalfont\uline{Schémas formels}.}','section heading','2',why='Roman underlined title and final period.')
 txt,_,_=page_text(rel,195)
 r(r'\Osh','O','all structure sheaves and rings','1;2',why='The O symbols are plain, without underlines.',count=txt.count(r'\Osh'))
 r(r'\operatorname{Supp}(O_X/J)',r'\operatorname{supp}O_X/J','section 2, support formula','2',why='Lowercase supp is printed without enclosing parentheses.')
 r('« sous-schéma fermé de $X$ »',r'\fquote{\uline{sous-schéma fermé de} $X$}','section 2, first definition','2',why='Double quotes and underlined prose, with X excluded.')
 r("noté $X_n$ ; c'est", "noté $X_n$, c'est",'section 2, thickened closed scheme','2',why='The print has a comma.')
 r('Évidemment les','Evidemment les','section 2, projective system','2',why='The printed capital E has no accent.')
 r("projectif de faisceaux d'anneaux sur $X'$, dont", "projectif de faisceaux d'anneaux sur $X$, dont",'section 2, projective system','2',why='The print has unprimed X. This is meaningful for the quotient sheaves on X, supported on X-prime; no mathematical need justifies the supplied prime.')
 r(r'''\emph{complété formel de $O_X$ le
long de $X'$}''',r'''\uline{complété formel de} $O_X$ \uline{le
long de} $X'$''','section 2, completed ring sheaf','2',why='Only the prose is underlined.')
 r(r'''appelé
\emph{complété formel de $X$ le long de $X'$}''',r'''\uline{appelé
complété formel de} $X$ \uline{le long de} $X'$''','section 2, completed space','2',why='The underline includes appelé and excludes X and X-prime.')
 r(r'\varprojlim_n',r'\varprojlim\limits_n','three inverse limits','2',why='The n is beneath the left arrow, even in the running text.',count=3)
 r(r"O_X/J^{n+1}$) ; c'est",r"O_X/J^{n+1}$), c'est",'section 2, completed module','2',why='The parenthesis is followed by a comma.')
 r("« sections formelles de $F$ le long\nde $X'$ »",r"\fquote{sections formelles de $F$ le long"+"\n"+r"de $X'$}",'section 2, formal sections','2',why='The print uses ordinary double quotes.')
 r('« fonctions\nholomorphes »',r'\fquote{fonctions'+"\n"+'holomorphes}','section 2, Zariski terminology','2',why='The print uses ordinary double quotes.')
 r('au sens de Zariski (dont','au sens de ZARISKI, (dont','section 2, Zariski terminology','2',why='The surname is uppercase and followed by a comma.')
 r('à cause de ses interférences','à cause de ces interférences','section 2, final parenthesis','2',why='The printed demonstrative is ces.')
 r(r'm\geq n',r'm\geqslant n','last paragraph, transition index','2',why='The handwritten inequality has a slanted lower bar.')
 upright_page(rel,layer,'182-195')
event('182-1-proper-coherence','carried as background without fault found','Read the projective/proper morphism terminology and the coherence of the structure sheaf on a noetherian scheme. Properness is stated through finite type and universal closedness under the earlier separated convention. No independent proof is claimed.','182, p. 195, first two paragraphs')
event('182-2-completion','targeted proof check','Restored the printed unprimed X in the projective system of quotient sheaves: O_X/J^{n+1} is a sheaf on X supported on X-prime, equivalently the direct image of the sheaf on the closed subspace. Taking the inverse limit in either description gives the stated completion. The inserted prime was unnecessary. The n+1 power gives X_0 the quotient by J.','182, p. 195, first paragraph of section 2')
event('182-2-formal-scheme-definition','carried as background without fault found','Read the topological inverse-limit definition and the transition-kernel power J_m^{n+1}; the definition continues on the next page. No completeness or equivalence theorem has yet been proved in this pass.','182, p. 195, final paragraph')
record_page('182',195,r'''Compared both French files sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 89–134 with scan leaf 4 at 400 dpi and three enlarged bands. Read the properness/coherence paragraphs, closed subscheme and completion definitions, and the beginning of the formal-scheme definition. All powers n+1, n and m indices, primes, bars and inverse-limit arrows were enlarged.

Restored definition underlining, plain structure-sheaf O, lowercase supp without added parentheses, precise punctuation and quotation marks, unaccented Evidemment, uppercase ZARISKI, ces interférences, and indices below limit arrows. The second completion definition underlines appelé as well as its defining prose. The printed unprimed X in the projective system is retained in both layers: the quotient sheaves on X have support X-prime, so the supplied prime was an unnecessary change. No new original misprint is asserted; the formal-scheme definition continues.''')
from update_record_counts import update
update()
