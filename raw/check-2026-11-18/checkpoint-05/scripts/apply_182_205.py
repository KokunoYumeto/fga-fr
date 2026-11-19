from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1,full=False):
  replace(rel,a,b,layer,'182-205',line,statement,'400-dpi scan with full-page image and all three enlarged bands. '+why,kind,count=count,full=full)
 r('\\src{206}\n', '', 'page boundary','6','structure','The printed page ends in the opening definition of Theorem 9, earlier than this marker.',full=True)
 r('sur $X_0$) de schémas formels','sur $X_0$)\n\\src{206}\nde schémas formels','Theorem 9, last line','6-thm9','structure','Move marker 206 after the parenthesis ending sur X_0; its following definition and conclusions remain for the next page.',full=True)
 txt,_,_=page_text(rel,205)
 r(r'\Osh','O','structure sheaves','6',why='The structure sheaf O is plain.',count=txt.count(r'\Osh'))
 r(r'\Theta',r'\mathfrak G','derivation sheaf','6',why='All five occurrences repeat the Gothic G shape enlarged on page 204; they are not Greek theta.',count=txt.count(r'\Theta'))
 r(r'\underline{\operatorname{Aut}}',r'\mathop{\text{\uwave{Aut}}}\nolimits','automorphism sheaves','6-thm8-filtration',why='Every Aut sheaf has wavy underlining.',count=txt.count(r'\underline{\operatorname{Aut}}'))
 if tree=='fr_printed':
  r('il existe un $A$-schéma plat $X$ tel que','il existe un $A$-schéma plat $Y$ tel que','Corollary 1 continuation','6-thm8-cor1',why='The print names the lifted scheme Y and immediately uses X in its equation. Corrected French retains X.')
  r('$X_n$ tels que $X_n\\otimes_A A_{n-1}=X_{n-1}$','$X_n$ tels que $X\\otimes_A A_{n-1}=X_{n-1}$','Corollary 2, reduction equation','6-thm8-cor2',why='The n subscript is missing on X in the printed reduction equation. Corrected French retains it to refer to the X_n just quantified.')
  r('dans ce\ndernier espace','dans de\ndernier espace','parenthesis after Corollary 2','6-thm8-cor2',why='The enlarged line prints de dernier, an ungrammatical article; corrected French retains ce dernier.')
 else:
  r(r'\nolimits(X_n)$ ; le gradué',r'\nolimits(X_{n-1})$ ; le gradué','filtration quotient','6-thm8-filtration','misprint of the original','The later explicit F^n is the kernel of reduction to X_{n-1}; hence the quotient is Aut(X_{n-1}), not Aut(X_n). For A=k[epsilon]/epsilon^2, F^1 is the whole augmented group, so its quotient is trivial, whereas Aut(X_1) need not be.')
  r(r'\mathfrak G_{X_0/k}\otimes_k\operatorname{gr}(A)',r'\mathfrak G_{X_0/k}\otimes_k\bigoplus_{i>0}\operatorname{gr}^i(A)','associated graded of augmented automorphisms','6-thm8-filtration','misprint of the original','Only positive filtration degrees occur: all automorphisms induce the identity on X_0. The printed gr(A) includes degree zero, as explicitly used on page 204. For A=k and X_0 affine line the group is trivial but the printed right side has a nonzero degree-zero derivation sheaf.')
 r('et est\nisomorphe à','et\nisomorphe à','last filtration step','6-thm8-filtration',why='The print has et isomorphe, with est supplied by the earlier clause; the extra est is removed from both layers.')
 r('(Noter que, en général','(Noter que en général','parenthetical remark','6-thm8-cor2',why='No comma follows que in the original.')
 r('sur $k$. Pour tout anneau','sur $k$, Pour tout anneau','Theorem 9 first sentence','6-thm9',why='The scan has a comma after k, followed by capital Pour.')
 txt,_,_=page_text(rel,205)
 for m in list(re.finditer(r'\\\[\s*(.*?)\s*\\\]',txt,re.S)):
  old=m.group(0);expr=re.sub(r'\s*\n\s*',' ',m.group(1).strip());punct=expr[-1];expr=expr[:-1]
  r(old,'$'+expr+'$'+punct,'cohomology classification formulas','6-thm8','structure','Both formulas are inline with punctuation outside mathematics.')
 r('pu trouver un $X$','pu trouver \\uline{un} $X$','classification paragraph','6-thm8',why='Only un is underlined in this phrase.')
 r("compatibles avec\nl'augmentation",r"\uline{compatibles avec l'augmentation}",'definition of augmented Aut','6-thm8-filtration',why='This qualifying phrase is underlined.')
 r('anneau local\nnoethérien complet de corps résiduel $k$, pourvu',r'\uline{anneau local noethérien complet de corps résiduel} $k$, pourvu','paragraph before Theorem 9','6-thm9',why='The ring condition, excluding k, is underlined.')
 txt,_,_=page_text(rel,205);a=txt.index('\n')+1;b=txt.index('\n\n',a);old=txt[a:b]
 r(old,underline_prose(old),'Corollary 1 continuation','6-thm8-cor1',why='The continuation statement prose is underlined.')
 for marker,sid in [(r'\result{COROLLAIRE}{2} ','6-thm8-cor2'),(r'\result{COROLLAIRE}{3} ','6-thm8-cor3'),(r'\result{THÉORÈME}{9} ','6-thm9')]:
  txt,_,_=page_text(rel,205);a=txt.index(marker)+len(marker);b=txt.find('\n\n',a);b=len(txt) if b<0 else b;old=txt[a:b].rstrip()
  if sid=='6-thm8-cor2':new=underline_prose(old)
  else:
   parts=re.split(r'(\bsimple\b|\(à un\s+isomorphisme.*?\))',old,flags=re.S)
   new=''.join(x if i%2 else underline_prose(x) for i,x in enumerate(parts))
  r(old,new,'statement prose',sid,why='Restore the exact statement underlining; simple and the isomorphism parenthesis are ununderlined in Corollary 3 and Theorem 9, unlike Corollary 2.')
 upright_page(rel,layer,'182-205')
event('182-6-thm8-cor1','targeted proof check','The H^2 obstruction computed on page 204 vanishes at every Artinian extension, so successive local lifts glue to a global lift. Corrected French retains X where the printed conclusion first calls it Y and then uses X.','182, pp. 204–205, Corollary 1')
event('182-6-thm8-filtration','targeted proof check','Write F^n=ker(Aut_aug(X)->Aut_aug(X_{n-1})), as the final sentence specifies. Smooth local lifting makes the quotient sheaf Aut_aug(X_{n-1}); each positive graded piece is G tensor m^n/m^(n+1). Corrected Aut(X_n) to Aut(X_{n-1}) and gr(A) to its strictly positive part. Counterchecks: for the affine line over dual numbers, x maps to x+epsilon f(x), F^1 is the entire nontrivial augmented group, and its quotient is trivial. For A=k the augmented group is trivial, whereas G tensor gr^0(k) is nonzero. These explicitly exhibit both indexing defects under the paragraph\u2019s own convention.','182, p. 205, filtration paragraph')
event('182-6-thm8-cor2','targeted proof check','After one lift is chosen, differences of overlap gluing maps are 1-cocycles in G tensor m^n; change of local identifications is a coboundary. Thus the classes form a torsor under H^1(G) tensor m^n; without a lift the set is empty. Isomorphisms must fix X_{n-1}, as stated. Corrected French retains the missing n in the reduction equation.','182, p. 205, Corollary 2')
event('182-6-thm8-cor3','targeted proof check','Induct on the nilpotence length. Having identified the previous reductions, Corollary 2 with zero H^1 makes their lifts isomorphic compatibly with that identification. This proves at-most-one isomorphism class.','182, p. 205, Corollary 3')
record_page('182',205,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 585–649 with scan leaf 14 at 400 dpi, full page and all three enlarged bands. Read Corollary 1's continuation, the augmented-automorphism classification and filtration, Corollaries 2–3, and the opening of Theorem 9. Moved marker 206 after the final parenthesis on this page, reserving the rest of that theorem for its actual scan.

Restored the repeated Gothic G derivation symbol, wavy-underlined Aut, plain O, inline cohomology formulas, precise selective underlining, and the printed punctuation and unexpanded wording. Printed French restores Y in the first conclusion, the missing n in Corollary 2's equation and de dernier in the following parenthesis; corrected French retains the supplied repairs. Two new mathematical corrections are made only in corrected French: the quotient by F^n is Aut(X_{n-1}), and the graded derivation formula uses only strictly positive degrees of gr(A). Explicit affine-line/dual-number and residue-field counterchecks are recorded. The obstruction-existence, torsor and uniqueness deductions were checked conditional on Theorem 8.''')
from update_record_counts import update
update()
