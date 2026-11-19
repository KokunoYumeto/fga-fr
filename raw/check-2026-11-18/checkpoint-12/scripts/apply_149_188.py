from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/149.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'149-188',line,statement,'400-dpi scan and enlarged top/middle/bottom crops. '+why,kind,count=count)
 r('non-singularité convenables','non singularité convenables','line before Theorem 4','7-thm4',why='The printed noun phrase has no hyphen.')
 if tree=='fr_printed':
  txt,_,_=page_text(rel,188)
  for a,b,body in list(footnotes(txt)):r(txt[a:b],'','after 7.4 bis','7.4-bis','structure','The explanatory correction note is absent from print.')
  r('non singularité convenables','non singularité convenable','line before Theorem 4','7-thm4',why='The scan has singular convenable. Corrected French retains the plural agreement with conditions; this disposition will receive the final second reading.')
  r(r'=f^{*}(\xi^{m,m})',r'=f_{*}(\xi^{m,m})','formula 7.4 bis','7.4-bis',why='The scan places the star below f. The supplied corrected pullback f^* is required by its input on X and output on Y.')
 for a,b,loc in [(r'f^{*}:H^{*}(X)\longrightarrow H^{*}(Y).',r'f^{*}:H^{*}(X)\longrightarrow H^{*}(Y)','7.2'),(r'f_{*}:H^{*}(Y)\longrightarrow H^{*}(X).',r'f_{*}:H^{*}(Y)\longrightarrow H^{*}(X)','7.3'),(r'f_{*}(1_Y)=P_X(Y),',r'f_{*}(1_Y)=P_X(Y)','7.4'),(r'\bigl(\xi^{m,m}\in H^{m}(X,\Omega_X^{m})\bigr),',r'\bigl(\xi^{m,m}\in H^{m}(X,\Omega_X^{m})\bigr)','7.4-bis')]:r(a,b,'formula '+loc,loc,why='The printed display has no terminal punctuation.')
 r(r"l'élément unité de $H(Y)$, on a",r"l'élément unité de $H(Y)$ on a",'Theorem 4, second line','7-thm4',why='There is no comma after H(Y).')
 txt,_,_=page_text(rel,188);label=r'\result{THÉORÈME}{4} ';a=txt.index(label)+len(label);b=txt.index(r'\begin{',a);old=txt[a:b]
 r(old,underline_prose(old),'Theorem 4 introduction','7-thm4',why='The statement prose is underlined, with variables outside the underline.')
 old='où le deuxième membre est la classe de cohomologie dans $X$ associée à $Y$.'
 r(old,underline_prose(old),'line after 7.4','7-thm4',why='The concluding prose of the theorem is underlined.')
 r('valables en fait, pour','valables en fait, pour','last paragraph','7-thm4',why='The printed comma is present; retained unchanged.') if False else None
 old=r'''\begin{split}
  H^{n-m}(X,\Omega_X^{n-m})
  &\simeq
  \operatorname{Ext}_{\Osh_X}^{n-m}(X;\Omega_X^{m},\Omega_X^{n})\\
  &\longleftarrow
  \operatorname{Ext}_{\Osh_X}^{n-m}(X;\Omega_Y^{m},\Omega_X^{n})
  \simeq
  \operatorname{Hom}_{\Osh_X}(X;\Omega_Y^{m},\Omega_Y^{m}).
\end{split}'''
 new=r'''H^{n-m}(X,\Omega_X^{n-m})
  \xrightarrow{\sim}
  \operatorname{Ext}_{\Osh_X}^{n-m}(X;\Omega_X^{m},\Omega_X^{n})
  \longleftarrow
  \operatorname{Ext}_{\Osh_X}^{n-m}(X;\Omega_Y^{m},\Omega_X^{n})
  \xrightarrow{\sim}
  \operatorname{Hom}_{\Osh_X}(X;\Omega_Y^{m},\Omega_Y^{m})'''
 r(old,new,'formula 7.5','7.5','structure','The original is one unbroken display; both isomorphisms have right-facing arrows with tildes, and no final period.')
 txt,_,_=page_text(rel,188)
 for m in list(re.finditer('« (.*?) »',txt,re.S)):
  r(m.group(0),r'\fquote{'+m.group(1)+'}','quoted expression','7',why='Restore ordinary double quotation marks.')
 txt,_,_=page_text(rel,188)
 r(r'\Omega',r'\underline{\Omega}','all differential-sheaf symbols','7',why='The sheaf symbols are underlined apart from the one inline omission separately restored below.',count=txt.count(r'\Omega'))
 if tree=='fr_printed':
  r(r"$\varepsilon_Y$ est l'élément fondamental dans $H^{m}(Y,\underline{\Omega}_Y^{m})$",r"$\varepsilon_Y$ est l'élément fondamental dans $H^{m}(Y,\Omega_Y^{m})$",'line immediately after 7.4 bis','7.4-bis',why='This inline capital Omega has no underline in print. Corrected French keeps the sheaf underline, consistently with the adjoining formulas.')
 upright_page(rel,layer,'149-188')
event('149-7.4-bis','targeted proof check','The printed f_* is a domain/codomain slip: xi belongs to cohomology of X, whereas f_* was just defined from Y to X. The left side lies in H^m(Y,Omega_Y^m), so the correct right side is the pullback f^*(xi). This confirms the existing supplied correction. The adjacent inline Omega is an omitted sheaf underline.','149, p. 188, (7.4 bis) and following line')
event('149-7-thm4','targeted proof check','Checked the displayed transposition: duality identifies the dual of H^m(X,Omega_X^m) with Ext^{n-m}(Omega_X^m,Omega_X^n), and the dual of H^m(Y,Omega_Y^m) with End(Omega_Y^m). The map is induced contravariantly by restriction of forms. The assertion that the identity maps to the class P_X(Y) is a compatibility with the fundamental class; read here, with the detailed verification left implicit by the author.','149, p. 188, Theorem 4 and (7.5)')
record_page('149',188,r'''Compared sources/fr_printed/fr/149.tex entry lines 997–1058 and sources/fr/fr/149.tex entry lines 1005–1066 with scan leaf 21 at 400 dpi and enlarged crops covering every formula and all prose. Read Theorem 4, (7.2)–(7.5), and the beginning of the compatibility discussion.

Restored display punctuation, the non-hyphenated phrase non singularité, quotation marks, statement underlining, upright variables and underlined differential sheaves. Formula (7.5) is restored as a single display with two explicit right-facing isomorphism arrows. Printed French restores the printed subscript star in (7.4 bis), singular convenable and the omitted underline on the following inline Omega, and removes the editorial footnote. Corrected French retains the supplied pullback (confirmed by its domain and codomain) and plural agreement, and supplies the omitted underline. The singular adjective is recorded as a grammatical disposition for the final second reading. The duality identifications and arrow directions were checked; the author's full implicit fundamental-class compatibility was not claimed independently proved.''')
from update_record_counts import update
update()
