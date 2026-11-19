from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/149.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'149-185',line,statement,'400-dpi scan and three enlarged page bands. '+why,kind,count=count)
 for old,new,loc in [('de prouver que, pour','de prouver que pour','line 4'),('Or, pour le premier\nmembre, cela','Or pour le premier\nmembre cela','lines 6–7'),('est, en tant que','est en tant que','line 11'),('$\\leq r-n$ (car','$\\leq r-n$, (car','line 12'),("singulière), d'où","singulière) d'où",'line 12')]:r(old,new,loc,'5-D',why='Restore the printed comma placement.')
 r(r'$L=k$',r'$L=\underline{k}$','line 2','5.7',why='The field k is underlined.')
 r(r'\fsection{6}{Le théorème de dualité pour les variétés singulières}',r'\fsection{\normalfont6}{\normalfont\uline{Le théorème de dualité pour les variétés singulières}.}','heading','6',why='The title is underlined, in ordinary type, with a final full stop.')
 for old,new,loc in [(r'=\operatorname{Ext}_{\Osh_X}^{0}(X;F,\omega_X^{n}),',r'=\operatorname{Ext}_{\Osh_X}^{0}(X;F,\omega_X^{n})','6.1'),(r'=\Extsh_{\Osh_P}^{r-n}(\Osh_X,\Omega_P^{r}).',r'=\Extsh_{\Osh_P}^{r-n}(\Osh_X,\Omega_P^{r})','6.2'),(r'\simeq\operatorname{Hom}_{\Osh_X}(X;\omega_X^{n},\omega_X^{n}),',r'\simeq\operatorname{Hom}_{\Osh_X}(X;\omega_X^{n},\omega_X^{n})','second 6.2')]:r(old,new,'formula '+loc,loc,why='The formula has no terminal punctuation in print.')
 r(r'\longrightarrow k.',r'\longrightarrow\underline{k}','formula 6.3','6.3',why='The field k is underlined and the display has no final full stop.')
 if tree=='fr_printed':
  txt,_,_=page_text(rel,185)
  for a,b,body in list(footnotes(txt)):r(txt[a:b],'','after second 6.2','6.2-bis','structure','The explanation of the numbering repair is an editorial footnote absent from the original.')
  r(r'\tag{6.2 bis}',r'\tag{6.2}','second 6.2','6.2-bis',why='The print repeats 6.2. Corrected French retains the existing unique label 6.2 bis.')
 txt,_,_=page_text(rel,185)
 for m in list(re.finditer(r'\$[^$]+\$|\\begin\{equation\}.*?\\end\{equation\}|\\\[.*?\\\]',txt,re.S)):
  old=m.group(0);new=old.replace(r'\Omega',r'\underline{\Omega}').replace(r'\omega',r'\underline{\omega}')
  omitted=old==r"$H^{n}(X,\omega_X^{n})'$"
  if omitted and tree=='fr_printed':new=old
  if new!=old:r(old,new,'Greek sheaf symbols','5;6','misprint of the original' if omitted else 'reading',why=('The inline omega in the privileged-element sentence lacks the underline in print; corrected French supplies the same sheaf notation as the adjoining formulas.' if omitted else 'The printed differential-sheaf letters are underlined.'))
 upright_page(rel,layer,'149-185')
event('149-5-D-general','targeted proof check','With the printed arbitrary degree i of Lemma 5 restored, its use at i=r-p is valid. A smooth closed X in smooth P is a regular immersion of codimension r-n, so the local Koszul resolution makes the sheaf Ext vanish for r-p>r-n, equivalently p<n. After twisting, Lemma 5 transfers that vanishing to global Ext; the coeffaceability argument then completes D on the coherent category.','149, p. 185, conclusion of section 5')
event('149-6.1','carried as background without fault found','Read the top-degree duality with the canonical sheaf for a possibly singular closed projective variety; its derivation and embedding independence are referred to the preceding results.','149, p. 185, (6.1)–first (6.2)')
event('149-6.3','targeted proof check','Substitution F=omega in (6.1) identifies the dual of top cohomology with endomorphisms of omega. The identity endomorphism selects a linear functional gamma; no isomorphism to k is claimed for a singular X. The omitted underline in the intervening inline omega is a notation slip.','149, p. 185, second (6.2), intervening sentence and (6.3)')
record_page('149',185,r'''Compared sources/fr_printed/fr/149.tex entry lines 850–901 and sources/fr/fr/149.tex entry lines 856–907 against scan leaf 18 at 400 dpi and the three enlarged page crops. Read the completion of the proof of D and the opening of section 6 through the definition of gamma.

Both layers restore the exact commas, heading emphasis, underlined field and differential-sheaf symbols, display punctuation and upright mathematics. Printed French restores the duplicate label (6.2), removes its editorial footnote, and retains the missing underline on the inline omega in the privileged-element sentence. Corrected French retains the disambiguation (6.2 bis) and repairs that one omitted sheaf underline. The arbitrary-degree version of Lemma 5, visually resolved before this page was completed, is the version needed in its first paragraph. The trace in (6.3) is an ordinary arrow, as distinct from the isomorphism arrow in (5.7).''')
from update_record_counts import update
update()
