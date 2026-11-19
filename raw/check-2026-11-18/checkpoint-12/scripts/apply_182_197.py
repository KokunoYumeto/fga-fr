from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'182-197',line,statement,'400-dpi scan and enlarged top/middle/bottom bands. '+why,kind,count=count)
 r('de Serre [4]','de SERRE [4]','opening paragraph','3',why='The surname is uppercase.')
 txt,_,_=page_text(rel,197)
 for m in list(re.finditer('« (.*?) »',txt,re.S)):
  r(m.group(0),r'\fquote{'+m.group(1)+'}','quotation in section 3','3',why='The print has ordinary double quotation marks.')
 r(r'\varprojlim_n',r'\varprojlim\limits_n','Theorem 2 limit','3-thm2',why='The n is beneath the left arrow.')
 r(r'''\result{THÉORÈME}{2 (Premier théorème de comparaison)} Les
$R^{q}f_{*}(F)$ sont des faisceaux cohérents sur $Y$ (ce qui est un cas
particulier du théorème 1), et les homomorphismes naturels''',r'''\result{THÉORÈME}{2 (Premier théorème de comparaison)} \uline{Les}
$R^{q}f_{*}(F)$ \uline{sont des faisceaux cohérents sur} $Y$ (ce qui est un cas
particulier du théorème 1), \uline{et les homomorphismes naturels}''','Theorem 2 introduction','3-thm2',why='Statement prose is underlined; the parenthetical aside and mathematical letters are not.')
 r('\nsont des isomorphismes.','\n\\uline{sont des isomorphismes}.','Theorem 2 conclusion','3-thm2',why='The prose is underlined; the final period lies outside the line.')
 r(r'''\result{COROLLAIRE}{1} On a des isomorphismes canoniques :
\[
  \overline{R^{q}f_{*}(F)}=R^{q}\overline f_{*}(\overline F).
\]''',r'''\result{COROLLAIRE}{1} \uline{On a des isomorphismes canoniques} :
$\overline{R^{q}f_{*}(F)}=R^{q}\overline f_{*}(\overline F)$.''','Corollary 1','3-cor1','structure','The equation is in the running line after the underlined introduction, not in a separate display.')
 r(r'(\textit{ii})','(ii)','paragraph following Corollary 1','3-thm1-ii',why='The reference marker is upright.')
 r('triviale pour $q$ grand','trivial pour $q$ grand','descending induction paragraph','3-thm2',why='The print has trivial; its masculine reference to the theorem makes an emendation unnecessary.')
 r('Alors, pour tout','Alors pour tout','Corollary 2','3-cor2',why='There is no comma after Alors.')
 for n in [2,3]:
  txt,_,_=page_text(rel,197); marker='\\result{COROLLAIRE}{'+str(n)+'} '; a=txt.index(marker)+len(marker); b=txt.index('\n\n',a); old=txt[a:b]
  r(old,underline_prose(old),'Corollary '+str(n),'3-cor'+str(n),why='The full statement prose is underlined; variables and the initial letters in A-modules/J-adiques remain outside the underlines.')
 r(r'\Osh_X','O_X','sentence introducing Corollary 3','3-cor3',why='The structure-sheaf O is plain and ununderlined.')
 r(r'\Homsh_{O_X}',r'\mathop{\text{\uwave{Hom}}}\nolimits_{O_X}','sentence introducing Corollary 3','3-cor3',why='The printed sheaf Hom has a wavy underline, distinct from the straight underline of the earlier exposé.')
 upright_page(rel,layer,'182-197')
event('182-3-thm2','carried as background without fault found','Read the coherence and comparison isomorphism with its completed left side and inverse limit. The descending induction is described but not supplied on this page; no independent proof is claimed here.','182, p. 197, Theorem 2 and following discussion')
event('182-3-cor1','targeted proof check','The canonical comparison follows by composing the isomorphisms of Theorem 2 and Theorem 1(ii) through the same inverse limit. The q=0 case of Theorem 1(ii) follows from limits of sheaves and sections commuting, whereas completion of algebraic cohomology in Theorem 2 is additional content.','182, p. 197, Corollary 1 and following paragraph')
event('182-3-cor2','targeted proof check','Over affine noetherian Y, the coherent higher direct image corresponds to the finite A-module H^q(X,F). Its J-adic completion and Theorem 1(ii) identify with cohomology on the formal completion. This checks the stated deduction from the preceding theorems, without independently proving those theorems.','182, p. 197, Corollary 2')
event('182-3-cor3','targeted proof check','The Hom-sheaf is coherent for coherent F,G on noetherian X. Finite presentation and flat adic completion identify its completion with the Hom-sheaf of the completed modules, reducing the statement to Corollary 2 in degree zero. If A is complete, finite A-modules are complete, giving the two last displayed identifications.','182, p. 197, Corollary 3 and final display')
record_page('182',197,r'''Compared both French sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 186–244 against scan leaf 6 at 400 dpi and all three enlarged bands. Read Theorem 2, Corollaries 1–3, the descending-induction discussion, functoriality and both final identifications. Every completion bar, q, n, star, prime and reference was enlarged.

Restored uppercase SERRE, literal double quotes, theorem/corollary underlining, the inline placement of Corollary 1, upright ii, printed trivial, the absence of a comma after Alors, and the wavy underline of the sheaf Hom over plain O_X. The ordinary Hom groups remain ununderlined. No original misprint is newly asserted. The deductions of the corollaries were checked using the explicitly identified standard completion facts; the comparison theorem itself is only carried as background on this page.''')
from update_record_counts import update
update()
