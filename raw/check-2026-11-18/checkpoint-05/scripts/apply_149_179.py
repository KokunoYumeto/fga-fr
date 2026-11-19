from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/149.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'149-179',line,statement,'400-dpi image, three enlarged bands and tight cup-product/diagram crops. '+why,kind,count=count)
 txt,_,_=page_text(rel,179);start=txt.index(r'\result{THÉORÈME}{1} ')+len(r'\result{THÉORÈME}{1} ');end=txt.index(r'\begin{equation}',start);old=txt[start:end]
 r(old,underline_prose(old),'1–2','4-thm1',why='The theorem prose is underlined, excluding its variables.')
 r("P_X(Z.Z')=P_X(Z).P_X(Z'),", "P_X(Z.Z')=P_X(Z).P_X(Z')",'4.4','4.4',why='No terminal comma is printed.')
 old='où le produit du deuxième membre est le cup-produit';r(old,r'\uline{'+old+'}','after 4.4','4-thm1',why='This continuation of the statement is underlined.')
 r('projectif.)','projectif)','hypothesis parenthesis','4-thm1',why='There is no full stop inside the closing parenthesis.')
 r('localement libres ; alors','localement libres, alors','proof paragraph','4-thm1',why='The print uses a comma.')
 r(r'\Osh_X\longrightarrow L_{*}',r'\Osh_X\longrightarrow L','proof paragraph, complex map','4-thm1',why='The print uses the unindexed L as the name of the same complex; adding a star is unnecessary normalization.')
 r('« groupe des sections »',r'\fquote{groupe des sections}','after unnumbered diagram','4-thm1',why='The scan has ordinary double quotes.')
 r('« edge-homomorphism »',r'\fquote{edge-homomorphism}','before 4.5','4-thm1',why='The scan has ordinary double quotes.')
 r(r'\xrightarrow[\sim]{\beta}',r'\xrightarrow{\overset{\beta}{\sim}}','unnumbered diagram','4-thm1',why='Beta is above the tilde, both above the right arrow.')
 r(r'\mathbb R^{p}\Gamma\!\left(\Homsh_{\Osh_X}(L_{*},\Omega_X^{p})\right)',r'(\mathbb R^{p}\Gamma)\!\left(\Homsh_{\Osh_X}(L_{*},\Omega_X^{p})\right)','unnumbered diagram','4-thm1',why='The functor R^p Gamma is parenthesized in the first diagram.',count=2)
 # In (4.5) the functor itself is not parenthesized: undo only that occurrence.
 txt,_,_=page_text(rel,179);a=txt.index(r'\begin{equation}\tag{4.5}');old=txt[a:];new=old.replace(r'(\mathbb R^{p}\Gamma)\!',r'\mathbb R^{p}\!\Gamma')
 r(old,new,'4.5','4.5',why='The extra functor parentheses belong only to the preceding diagram; the (4.5) cell retains the printed unparenthesized functor.')
 r(r'\bigr)\right),',r'\bigr)\right)','unnumbered diagram','4-thm1',why='No comma follows the diagram.')
 for deg,args in [('p',r'L_{*},\Omega_X^{p}'),("p'",r"L'_{*},\Omega_X^{p'}"),("p+p'",r"L_{*}\otimes L'_{*},\Omega_X^{p+p'}")]:
  old='\\Gamma H^{'+deg+'}\\!\\left('+ ('\n' if deg=="p+p'" else '')+r'\Homsh_{\Osh_X}('+args+r')\right)'
  new='\\Gamma\\bigl(H^{'+deg+'}\\!\\left('+ ('\n' if deg=="p+p'" else '')+r'\Homsh_{\Osh_X}('+args+r')\right)\bigr)'
  r(old,new,'4.5, right column','4.5',why='Gamma encloses the H expression in parentheses.')
 r('\\bigr).\n\\end{array}','\\bigr)\n\\end{array}','4.5, final cell','4.5',why='The array has no terminal full stop.')
 r(r'\begin{array}{ccc}',r'\left\{\begin{array}{ccc}','4.5','4.5','structure','Restore the tall left grouping brace.')
 r(r'\end{array}',r'\end{array}\right.','4.5','4.5','structure','The grouping brace has no right counterpart.')
 if tree=='fr_printed':
  r(r"\times H^{p'}(X,\Omega_X^{p'})",r"\times H^{p'}(X,\Omega_X^{p'}.)",'cup-product display','4-thm1',why='A stray full stop is printed inside the second cohomology argument; corrected French omits it.')
  r('en vertu de la proposition 3','en vertu de proposition 3','proof paragraph','4-thm1',why='The print omits la; corrected French retains the grammatical repair.')
  r(r"l'augmentation $L_0\longrightarrow\Osh_Y$",r"l'augmentation $L_0\longrightarrow O_Y$",'augmentation clause','4-thm1',why='O_Y in this clause has no underline in the print; corrected French keeps structure-sheaf notation.')
  r(r"\Homsh_{\Osh_X}(L_{*}\otimes L'_{*},\Omega_X^{p+p'})\right)\n&",r"\Homsh_{\Osh_X}(L_{*}\otimes L'_{*},\Omega_X^{p+p'})\right.\n&",'4.5, bottom middle','4.5',why='The tight crop confirms only one closing parenthesis for Gamma(Hom(...); the missing outer close is restored in corrected French.') if False else None
  old="\\Homsh_{\\Osh_X}(L_{*}\\otimes L'_{*},\\Omega_X^{p+p'})\\right)\n&"
  new="\\Homsh_{\\Osh_X}(L_{*}\\otimes L'_{*},\\Omega_X^{p+p'})\\right.\n&"
  r(old,new,'4.5, bottom middle','4.5',why='The tight crop confirms only one closing parenthesis for Gamma(Hom(...); corrected French retains the missing outer close.')
 for old,new,why in [(r'\mathbb R',r'\underline{\underline{R}}','Hyperderived R is a double-underlined ordinary R, not a blackboard character.'),(r'\Omega',r'\underline{\Omega}','The differential sheaf symbols are underlined.')]:
  txt,_,_=page_text(rel,179);r(old,new,'throughout page','4-thm1;4.5',why=why,count=txt.count(old))
 # Array cells require separate alphabet scopes, since TeX groups cannot span &.
 txt,_,_=page_text(rel,179);m=re.search(r'(\\begin\{array\}\{ccc\})(.*?)(\\end\{array\})',txt,re.S)
 parts=re.split(r'(\\\\(?:\[[^\]]*\])?|&)',m.group(2));parts=[x if x=='&' or x.startswith('\\\\') or not x.strip() else r'\symup{'+x.strip()+'}' for x in parts]
 r(m.group(0),m.group(1)+''.join(parts)+m.group(3),'4.5','4.5',why='Upright typewritten variables in each array cell; printed alphabets and underlines retained.')
 upright_page(rel,layer,'149-179')
event('149-4-thm1','carried as background without fault found','Read the transverse intersection statement and first part of its proof, including the resolution assumption and the hypercohomology pairing diagram. The proof continues on the next page. No independent proof claimed.','149, p. 179, Theorem 1 and (4.4)')
event('149-4.5','targeted proof check','Checked pairing degrees p,p prime,p+p prime and corresponding L,L prime,tensor-product entries against the defining terms. The bottom-middle Gamma(Hom(...)) needs two closing parentheses; the print has one. The supplied balanced expression is retained in corrected French.','149, p. 179, diagram (4.5)')
record_page('149',179,r'''Compared sources/fr_printed/fr/149.tex entry lines 532–600 and sources/fr/fr/149.tex entry lines 535–603 with scan leaf 12 at 400 dpi, all three enlarged bands, and tight crops of the cup-product dot, first diagram and bottom-middle closing parenthesis. Read Theorem 1, (4.4), the resolution and hypercohomology discussion and every cell, prime, exponent and arrow of (4.5).

Restored both layers' statement underlining, double-underlined R, Greek sheaf underlines, left grouping brace, Gamma parentheses, beta/tilde placement, quotes and punctuation. The printed shorthand complex L is kept in both layers; the added star was not needed to repair the mathematics. Printed French alone restores the stray dot inside the cup-product argument, absent article la, one omitted structure-sheaf underline and the absent outer closing parenthesis in the bottom-middle entry. The corrected layer retains those existing repairs. The pairing degrees and parenthesis repair have a targeted event; the theorem is otherwise recorded as read, with proof continuing.''')
p=read('CHECK_RECORD.md');needle='| Underlined functor |';i=p.index(needle);p=p[:i]+'| Hyperderived functor | `\\underline{\\underline{R}}` | Double-underlined ordinary R in 149-179, distinguished from ordinary derived R |\n'+p[i:];write('CHECK_RECORD.md',p)
from update_record_counts import update
update()
