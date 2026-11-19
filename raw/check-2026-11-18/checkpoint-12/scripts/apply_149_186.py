from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/149.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'149-186',line,statement,'400-dpi scan, enlarged bands and tight Greek-symbol crops. '+why,kind,count=count)
 r(r'\longrightarrow H^{n}(X,\omega_X^{n}),',r'\longrightarrow H^{n}(X,\omega_X^{n})','formula 6.4','6.4',why='No terminal comma follows the displayed pairing.')
 r('Alors, pour $m$','Alors pour $m$','Proposition 6','6-prop6',why='There is no comma after Alors.')
 r(r'\Extsh_{\Osh_P}^{r-n+i}(\Osh_X,\Omega_P^{r})',r'\Extsh_{\Osh_P}^{r-n+i}(\Osh_X,\omega_P^{r})','Theorem 3 bis, iv','6-thm3bis',why='The printed letter is lowercase omega. On nonsingular P it denotes the same canonical sheaf, so this valid notation is restored in both layers.')
 for label in [r'\result{THÉORÈME}{3 bis} ',r'\result{PROPOSITION}{6} ']:
  txt,_,_=page_text(rel,186);start=txt.index(label)+len(label);stop=txt.index(r'\begin{',start);old=txt[start:stop]
  r(old,underline_prose(old),'statement introduction','6',why='Restore the printed prose underlining, excluding variables.')
 txt,_,_=page_text(rel,186)
 for m in list(re.finditer(r'(\\item\[\\textit\{[iv]+\.\}\] )(.*?)(?=\n  \\item|\n\\end\{enumerate\})',txt,re.S)):
  old=m.group(2);r(old,underline_prose(old),'Theorem 3 bis condition','6-thm3bis',why='Each condition has underlined prose, with the mathematical formulas left outside the underline.')
 for numeral in ['i.','ii.','iii.','iv.']:
  txt,_,_=page_text(rel,186);a=r'\textit{'+numeral+'}';r(a,r'\textnormal{'+numeral+'}','condition labels and proof','6-thm3bis',why='The condition labels are upright roman numerals.',count=txt.count(a))
 r(r'\noindent\textbf{DÉMONSTRATION.} ---',r'\noindent DÉMONSTRATION. --','proof heading','6-thm3bis',why='The proof label is ordinary type followed by a short dash.')
 r(r'où on pose (comparer',r'\uline{où on pose} (comparer','before 6.7','6-prop6',why='Only the words où on pose are underlined.')
 r(r'E^{j}(F)=\Extsh_{\Osh_P}^{r-n+j}(F,\Omega_P^{r}).',r'E^{j}(F)=\Extsh_{\Osh_P}^{r-n+j}(F,\Omega_P^{r})','formula 6.7','6.7',why='The display has no terminal period.')
 txt,_,_=page_text(rel,186)
 for m in list(re.finditer(r'\$[^$]+\$|\\begin\{equation\}.*?\\end\{equation\}',txt,re.S)):
  old=m.group(0);new=old.replace(r'\Omega',r'\underline{\Omega}').replace(r'\omega',r'\underline{\omega}')
  omitted=old==r'$\operatorname{Ext}_{\Osh_P}^{r-i}(P;F(-m),\Omega_P^{r})$'
  if omitted and tree=='fr_printed':new=old
  if new!=old:r(old,new,'Greek differential-sheaf symbols','6','misprint of the original' if omitted else 'reading',why=('The final inline capital Omega lacks an underline in print; corrected French restores the sheaf notation fixed by (6.7).' if omitted else 'The Greek sheaf letters are underlined in print.'))
 upright_page(rel,layer,'149-186')
event('149-6-thm3bis','targeted proof check','Checked the interval endpoints and degree change: p from n-k through n-1 corresponds to i=n-p from 1 through k. The top case p=n is supplied by (6.1). The first three conditions are related by Lemmas 3 and 4 and the delta-functor comparison. The remaining implication uses the next Corollary and is still to be read. Lowercase omega_P in iv is valid since P is nonsingular.','149, p. 186, Theorem 3 bis and proof')
event('149-6-prop6','targeted proof check','Ambient duality gives Ext degree r-i. Definition E^{n-i} has degree r-n+(n-i)=r-i, and twisting the first argument by -m produces the +m twist on the sheaf Ext. Lemma 5 therefore gives (6.6). The ununderlined final Omega is a notation omission, not a different sheaf.','149, p. 186, Proposition 6, (6.6)–(6.7) and proof')
record_page('149',186,r'''Compared sources/fr_printed/fr/149.tex entry lines 901–953 and sources/fr/fr/149.tex entry lines 908–960 against scan leaf 19 at 400 dpi, three enlarged page bands and tight crops of omega in condition iv and Omega in the last line. Read (6.4)–(6.7), Theorem 3 bis and Proposition 6 with their proofs.

Both layers restore underlining of statement prose, upright condition labels, the ordinary proof heading, exact punctuation and Greek sheaf typography. Condition iv prints lowercase omega_P, a valid canonical-sheaf notation on nonsingular P, retained in both layers rather than normalized to capital Omega. The final inline capital Omega is ununderlined in print and kept so in the printed layer; corrected French supplies its omitted sheaf underline. The ranges in Theorem 3 bis and the degree arithmetic in Proposition 6 were checked explicitly; the cited next-page Corollary remains pending.''')
from update_record_counts import update
update()
