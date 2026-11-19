from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1,full=False):
  replace(rel,a,b,layer,'182-199',line,statement,'400-dpi scan and all three enlarged page bands. '+why,kind,count=count,full=full)
 r('\\src{200}\n\\result{COROLLAIRE}{1}',r'\result{COROLLAIRE}{1}','next page boundary','4-thm5','structure','The printed page ends after sont connexes, before the explanatory i.e.; remove the late marker before Corollary 1.',full=True)
 r('sont connexes, i.e.','sont connexes,\n\\src{200}\ni.e.','last line','4-thm5','structure','Place the page-200 marker at the actual boundary inside Theorem 5.')
 r(r'''\[
      H^2(\mathfrak X_0,\Osh_{\mathfrak X_0})=0.
    \]''',r'$H^2(\mathfrak X_0,\Osh_{\mathfrak X_0})=0$.','first line','3-thm4-ii','structure','The formula continues the running clause from the preceding page; it is not centered.')
 r(r'\item[\textit{iii.}] $\mathfrak X_0$ est projectif.',r'\item[\textnormal{iii.}] $\mathfrak X_0$ \uline{est projectif}.','condition iii','3-thm4-iii',why='Roman marker and underlined words.')
 txt,_,_=page_text(rel,199);a=txt.index('Sous ces conditions');b=txt.index('\n\n',a);old=txt[a:b]
 new=underline_prose(old).replace(r'\uline{-schéma projectif}',r'\uline{-schéma} projectif')
 r(old,new,'Theorem 4 conclusion','3-thm4',why='The prose is underlined except the final word projectif and mathematical symbols.')
 for n in ['i','ii','iii']:
  txt,_,_=page_text(rel,199);old=r'\textit{('+n+')}'
  r(old,'('+n+')','references to Theorem 4 conditions','3-thm4',why='The condition references are upright.',count=txt.count(old))
 r('une courbe simple sur','une \\uline{courbe simple} sur','application to curves','3-thm4',why='Courbe simple is underlined.')
 if tree=='fr_printed':
  r(r'immersion de $\mathfrak X$ dans',r'immersion de $X$ dans','proof sketch, projective embedding','3-thm4',why='The scan prints ordinary X here. Corrected French retains Gothic X, the formal scheme being embedded before an algebraization X is constructed.')
 r(r'\mathbf P_A^r','P_A^r','projective-space formula','3-thm4',why='P is ordinary, not bold.')
 r('de dimension $r$','de dim $r$','projective-space parenthesis','3-thm4',why='The printed abbreviation is dim.')
 txt,_,_=page_text(rel,199)
 for m in list(re.finditer('« (.*?) »',txt,re.S)):
  r(m.group(0),r'\fquote{'+m.group(1)+'}','quoted phrase','3;4',why='The print uses ordinary double quotation marks.')
 r(r'''\fsection{4}{Application au théorème de connexion et au \fquote{Main theorem} de
Zariski}''',r'''\fsection{\normalfont4}{\normalfont\uline{Application au théorème de connexion et au \fquote{Main theorem} de
Zariski}.}''','section heading','4',why='The heading is roman, underlined and ends with a period.')
 txt,_,_=page_text(rel,199)
 r(r'\Osh','O','structure-sheaf symbols','3;4',why='The O symbols are plain, without underlines.',count=txt.count(r'\Osh'))
 r(r'\mathcal A',r'\text{\uwave{A}}','two occurrences of the direct-image algebra','4',why='The algebra is an ordinary upright A with a wavy underline, not a script A.',count=2)
 r(r'la \emph{factorisation de Stein}',r'\uline{la factorisation de Stein}','definition of Stein factorization','4',why='The underline includes la.')
 r("$y'$, on trouve", "$y'$ on trouve",'connectedness argument','4-thm5',why='No comma follows y-prime.')
 r(r"O_{Y',y'}",r"O_{y'}",'local-ring equality in the connectedness argument','4-thm5',why='The printed local ring has only the point y-prime as subscript. This is unambiguous, so the supplied expanded index is withdrawn in both layers.')
 r('est local !).','est local !).','connectedness argument','4-thm5') if False else None
 txt,_,_=page_text(rel,199);marker=r'\result{THÉORÈME}{5 (\fquote{Théorème de connexion} de Zariski)} ';a=txt.index(marker)+len(marker);old=txt[a:]
 parts=re.split(r"(\(à un isomorphisme près\)|\(d'où\s*\$[^$]*\$\))",old)
 new=''.join(x if i%2 else underline_prose(x) for i,x in enumerate(parts))
 r(old,new,'Theorem 5, beginning through sont connexes','4-thm5',why='The assertion is underlined, excluding both parenthetical asides and the mathematical letters.')
 upright_page(rel,layer,'182-199')
event('182-3-thm4','targeted proof check','Checked the proof sketch’s object types: the projective immersion is of the formal scheme Gothic X, before its algebraization X exists; the printed ordinary X is a font/notation slip. The obstruction argument needs flatness to identify each infinitesimal kernel with O_{X_0} tensor a finite k-vector space, then H^2=0 to lift an invertible sheaf. A high ample power, lifting sections and formal Nakayama yield a closed formal immersion; algebraization of its ideal uses Theorem 3, Corollary 1. These are the dependencies of the sketch, not an independent proof of Theorems 1–3.','182, p. 199, Theorem 4 conclusion and proof sketch')
event('182-4-thm5','targeted proof check','Checked the connectedness contradiction: a disconnected proper fiber gives a nontrivial idempotent in the ring of formal sections, while formal comparison identifies that ring with the completed local ring at y-prime, which is local. For a nonclosed point y-prime one first works over Spec(O_{Y-prime,y-prime}); this localization step is implicit in the printed argument. Construction uses the finite algebra f_*O_X and its relative spectrum. The theorem’s remaining interpretation continues on page 200.','182, p. 199, Stein factorization construction and Theorem 5')
record_page('182',199,r'''Compared both French sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 293–348 with scan leaf 8 at 400 dpi and enlarged top/middle/bottom bands. Read the continuation of Theorem 4, its proof sketch, the section-4 heading, Stein construction and Theorem 5 through sont connexes. Moved the late page-200 marker from before Corollary 1 to the actual boundary before i.e.; the continuation is reserved for the next page.

Restored the first formula to the running clause, underlining (including its exclusions), roman condition references, ordinary P, printed dim, literal quotes, the wavy-underlined algebra A, la in the underlined definition, and the printed abbreviated local-ring index O_{y'}. Printed French restores ordinary X in the projective immersion sentence; corrected French retains Gothic X, because the object embedded is the formal scheme being algebraized. Recorded the obstruction/embedding dependencies and the implicit localization needed in the connectedness argument. No external proof of the comparison or existence theorem was consulted.''')
from update_record_counts import update
update()
