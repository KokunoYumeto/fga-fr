from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1,full=False):
  replace(rel,a,b,layer,'182-206',line,statement,'400-dpi scan, full page and three enlarged bands. '+why,kind,count=count,full=full)
 r('\\src{207}\n','','page boundary','6','structure','The printed page ends with Il faudrait commencer.',full=True)
 r('Il faudrait commencer\npar regarder','Il faudrait commencer\n\\src{207}\npar regarder','last line','6-rem1','structure','Move marker 207 before par regarder; the 1962 complement belongs to the next printed page.',full=True)
 txt,_,_=page_text(rel,206)
 r(r'\Theta',r'\mathfrak G','Theorem 9 and Corollary 3 derivation sheaves','6-thm9',why='Three handwritten Gothic G symbols, as on pages 204–205, not Greek theta.',count=txt.count(r'\Theta'))
 r(r'\Osh','O','Corollary 3 display','6-thm9-cor3',why='The structure sheaf O is plain.')
 r(r'\mathbf P',r'\mathfrak P','Corollary 2 projective spaces','6-thm9-cor2',why='Both projective-space symbols are handwritten Gothic P, with slightly differing pen forms; not bold roman P. The enlarged forms were compared with a local Gothic P/p specimen; no other edition was consulted.',count=2)
 r(r'\textit{i.}',r'\textnormal{i.}','Theorem 9 condition i','6-thm9',why='The condition marker is upright.')
 r(r'\textit{ii.}',r'\textnormal{ii.}','Theorem 9 condition ii','6-thm9',why='The condition marker is upright.')
 r(r'\textit{(i)}','(i)','Corollary 1 condition','6-thm9-cor1',why='The condition reference is upright and included in the statement underline.')
 r(r'9\textit{(ii)}','9(ii)','deduction after Corollary 3','6-thm9-cor3',why='The printed reference 9(ii) is upright.')
 r(r'\result{REMARQUES}{}',r'\result[.]{REMARQUES}{}','remarks heading','6-rem1',why='The heading has a period, no dash.')
 if tree=='fr_printed':
  r(r'tels que $\mathfrak X\otimes_A k=X_0$',r'tels que $X\otimes_A k=X_0$','Theorem 9 reduction equation','6-thm9',why='The print uses an ordinary X in this equation although the preceding formal scheme is Gothic X. Corrected French retains the consistent formal-scheme symbol.')
  old="induisant l'identité sur $X_0$) un schéma $X$ propre et plat sur $A$, tel que\n$X\\otimes_A k=X_0$."
  new=old.replace('$X\\otimes_A', '$.X\\otimes_A')
  r(old,new,'Corollary 1 final equation','6-thm9-cor1',why='The enlarged scan shows a small stray baseline period immediately before X. Corrected French omits this extraneous punctuation.')
 txt,_,_=page_text(rel,206);a=txt.index('\n')+1;b=txt.index('\n\\begin{enumerate}',a);old=txt[a:b]
 r(old,underline_prose(old),'Theorem 9 continuation','6-thm9',why='Statement prose is underlined, excluding mathematical letters and punctuation.')
 for n in ['i','ii']:
  txt,_,_=page_text(rel,206);marker='\\item[\\textnormal{'+n+'.}] ';a=txt.index(marker)+len(marker);b=txt.find('\n  \\item',a)
  if b<0:b=txt.index('\n\\end{enumerate}',a)
  old=txt[a:b];r(old,underline_prose(old),'Theorem 9 condition '+n,'6-thm9',why='The condition prose is underlined; mathematics and final periods are outside the underline.')
 for n in [1,2,3,4]:
  txt,_,_=page_text(rel,206);marker='\\result{COROLLAIRE}{'+str(n)+'} ';a=txt.index(marker)+len(marker);b=txt.index('\n\n',a);old=txt[a:b]
  if n==1:
   parts=re.split(r'(\(à un\s+isomorphisme.*?\))',old,flags=re.S)
   new=''.join(x if i%2 else underline_prose(x) for i,x in enumerate(parts))
  elif n==3:
   parts=re.split(r'(\\\[.*?\\\])',old,flags=re.S)
   new=''.join(x if i%2 else underline_prose(x) for i,x in enumerate(parts))
  else:new=underline_prose(old)
  r(old,new,'Corollary '+str(n)+' statement','6-thm9-cor'+str(n),why='Restore statement underlining; Corollary 1 excludes its isomorphism parenthesis, and Corollary 3 retains its displayed formula.')
 r('« schéma de courbe simple »',r'\fquote{schéma de courbe simple}','Corollary 4 quotation','6-thm9-cor4',why='The print uses ordinary double quotation marks.')
 r('« plus petit $A$\npossible »',r'\fquote{plus petit $A$ possible}','Remark 1 quotation','6-rem1',why='The print uses ordinary double quotation marks.')
 r('caractéristique $0$,',r'\uline{caractéristique} $0$,','Remark 1 characteristic-zero phrase','6-rem1',why='Only caractéristique in the characteristic-zero phrase is underlined.')
 upright_page(rel,layer,'182-206')
event('182-6-thm9','targeted proof check','Existence follows by applying the H^2 obstruction vanishing to successive Artinian quotients and taking the compatible formal limit; uniqueness follows by choosing the isomorphisms successively using the H^1 torsor statement. The finite-type flat formal-limit construction is carried as background. The first reduction equation is ordinary X in print; corrected French retains formal Gothic X.','182, pp. 205–206, Theorem 9')
event('182-6-thm9-cor1','targeted proof check','For proper schemes, the formal isomorphism from Theorem 9(i) algebraizes by Theorem 3, Corollary 2. Thus at most one proper flat algebraic lift with the specified special-fiber identification exists.','182, p. 206, Corollary 1')
event('182-6-thm9-cor2','targeted proof check','For projective r-space, the Euler sequence 0 -> O -> O(1)^(r+1) -> T -> 0 and H^1(O(1))=H^2(O)=0 give H^1(T)=0; r=0 is immediate. Compare X with projective r-space over A and apply Corollary 1. These elementary projective-space cohomology values are used as background.','182, p. 206, Corollary 2')
event('182-6-thm9-cor3','targeted proof check','Theorem 9(ii) supplies a formal lift. Vanishing H^2(O) lifts an ample line bundle, and Theorem 4 algebraizes the proper formal lift projectively. Flatness descends from its completions. This is a deduction conditional on those earlier formal-algebraization results.','182, p. 206, Corollary 3')
event('182-6-thm9-cor4','targeted proof check','On a proper smooth curve, coherent H^2 vanishes for O and the derivation sheaf, so Corollary 3 applies. Projectivity of a proper smooth curve is used as background. The nonsmooth locus of the resulting proper flat family is closed and misses the closed fiber; its proper image in the local base is empty, so the family is smooth throughout.','182, p. 206, Corollary 4')
event('182-6-rem1','carried as background without fault found','Read the historical positive-to-zero-characteristic lifting discussion and the Cohen-ring reduction. No independent proof of Cohen structure theory or of the historical open-question claim was attempted; its historical wording is retained. The paragraph continues on page 207.','182, p. 206, Remark 1')
record_page('182',206,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 636–702 with scan leaf 15 at 400 dpi, full page and enlarged top, middle and bottom bands. Read Theorem 9's continuation, Corollaries 1–4, and Remark 1 through Il faudrait commencer. Moved marker 207 to that actual boundary; material following it was reserved for the next page.

Restored Gothic derivation G and projective-space P, plain O, upright condition references, selective statement underlining, ordinary double quotes, the characteristic-zero emphasis, and the REMARQUES period. The projective P pen forms vary; their Gothic family is clear, while the case interpretation remains provisional for the final reread. Printed French restores ordinary X in the formal reduction equation and a stray period before X in Corollary 1's equation; corrected French retains the consistent formal symbol and omits the stray punctuation. Checked the corollaries as deductions from the formal existence, uniqueness and algebraization results, with projective-space and curve cohomology explicitly identified as background. The historical remark is retained as historical text.''')
from update_record_counts import update
update()
