from audit_utils import *
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
 prior_lines={(x['file'],x['printed_page'],x['line']) for x in csv.DictReader(f,delimiter='\t')}

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/195.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  if (rel,'195-379',line) in prior_lines: return
  replace(rel,a,b,layer,'195-379',line,'C.1','400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 s,_,_=page_text(rel,379)
 fs=list(footnotes(s))
 if (rel,'195-379','opening editorial footnote') not in prior_lines:
  if len(fs)!=1: raise ValueError('Expected one unprinted editorial footnote')
  a,b,_=fs[0]
  r(s[a:b],'','opening editorial footnote',kind='structure',why='This footnote is absent from the scan; its two suggested corrections are separately recorded, together with additional visible omissions.')
 r(r'\src{379}localement de type fini',r'\src{379}\uline{localement de type fini}','definition continuation',why='Printed underline on the defined phrase.')
 r('sur $S$ si, pour tout $x\\in X$ se projetant','sur $S$ si pour tout $x\\in X$, se projetant','definition punctuation',why='The comma follows x in X, not si.')
 r("voisinage affine de $y$, d'anneau", "voisinage affine de $y$ d'anneau",'first affine neighborhood punctuation',why='No comma follows y.')
 r("connexes (qu'il", "connexes, (qu'il",'Picard components parenthesis',why='Printed comma before the parenthesis.')
 r('i.e.', 'i. e.', 'abbreviation spacing',count=2,why='Both abbreviations are spaced in the scan.')
 r('« variété de Picard »',r'\fquote{variété de Picard}','Picard variety quotation',why='Ordinary double quotation marks.')
 r('« pré-schémas de Picard »',r'\fquote{pré-schémas de Picard}','Picard prescheme quotation',why='Ordinary double quotation marks.')
 s,_,_=page_text(rel,379)
 if (rel,'195-379','purpose of the lectures emphasis') not in prior_lines:
  start=s.index('Le but principal');end=s.index("Signalons en passant",start)
  span=s[start:end].rstrip()
  r(span,underline_prose(span),'purpose of the lectures emphasis',why='The full prose statement is underlined, with the mathematical letters left outside the underline.')
 r('en passant que, dans cette étude','en passant que dans cette étude','aside punctuation',why='No comma after que in the scan.')
 r('sont pas des schémas.','sont pas des schémas','end of first paragraph',why='No terminal period is visible in the print; retain this punctuation in both layers.')
 r('sur $S$, et soit\n\\[','sur $S$, et soit $F$ :\n\\[','associated functor introduction',why='The print explicitly names F followed by a colon before the display.')
 r('un anneau local artinien','un anneau \\uline{local} artinien','Artinian test ring',why='Only local is underlined.')
 r(r'\mathcal O_{s,S}',r'\text{\uwave{O}}_s','base local ring notation',why='The scan has wavy O with the sole subscript s; the added ambient S is absent.')
 r(r'\mathcal O_{x,X}',r'\text{\uwave{O}}_x','local ring notation',why='The scan has wavy O with the sole subscript x; the added ambient X is absent.')
 r(r'\widehat{\mathcal O}_{x,X}',r'\widehat{\text{\uwave{O}}}_x','completed local ring notation',why='The hat covers the wavy O and the sole subscript is x.')
 r('« $\\Lambda$-algèbres artiniennes »',r'\fquote{$\Lambda$-algèbres artiniennes}','Artinian algebra quotation',why='Ordinary double quotation marks.')
 r('la\nrestriction $F_0$ de $F$ aux',r'\uline{la restriction} $F_0$ \uline{de} $F$ \uline{aux}','pro-representability conclusion introduction',why='Selective prose underline excludes the two functor symbols and the following quotation.')
 s,_,_=page_text(rel,379)
 if (rel,'195-379','completed-local-ring conclusion emphasis') not in prior_lines:
  start=s.index('pro-représentable, et est représentée')
  start=s.rfind('est\n',0,start) if 'est\n' in s[:start] else -1
  if start<0: raise ValueError('Expected conclusion emphasis start')
  end=s.index('Cela montre\nque la seule connaissance',start)
  span=s[start:end].rstrip()
  r(span,underline_prose(span),'completed-local-ring conclusion emphasis',why='The prose from est pro-représentable through points fermés de S is underlined; letters and completed local ring are excluded.')
 r('On notera que, même','On notera que même','last sentence punctuation',why='No comma after que.')
 if tree=='fr_printed':
  r(r'$y\in S$',r'$y\in Y$','point on the base',why='The printed base letter is Y.')
  r('de $Y$ dans $X$ (i. e.','de $Y$ dans (i. e.','target of an S-homomorphism',why='The scan leaves the target blank before the parenthesis.')
  r('un élément de $F(Y)$) est défini','un élément de $F(Y)$ est défini','missing parenthesis after F(Y)',why='There is no closing prose parenthesis after F(Y).')
  r(r'\fquote{$\Lambda$-algèbres artiniennes}',r'\fquote{$Y$-algèbres artiniennes}','quoted base algebra letter',why='The scan types Y, not the earlier handwritten Lambda.')
  r(r'la} $\Lambda$\uline{-algèbre topologique',r'la} $Y$\uline{-algèbre topologique','representing topological algebra base letter',why='The scan again types Y.')
  r(r'points fermés de} $S$.',r'points fermés de} $Y$.','last base scheme letter',why='The scan ends the underlined assertion with Y.')
 s,_,_=page_text(rel,379)
 r(r'\mathcal C',r'\text{\uwave{C}}','category letters',count=s.count(r'\mathcal C'),why='The category is upright C with a wavy underline.')
 upright_page(rel,layer,'195-379')

with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 for line,old,new,why in [
 ('point on the base','y in Y','y in S','The immediately preceding morphism is X over S, and y denotes its image.'),
 ('target of an S-homomorphism','de Y dans (','de Y dans X (','The associated functor is F(Y)=Hom_S(Y,X); the target omitted in print is X.'),
 ('missing parenthesis after F(Y)','un élément de F(Y) est','un élément de F(Y)) est','The explanatory parenthesis opened at i. e. has no closing parenthesis in print.'),
 ('quoted base algebra letter','Y-algèbres artiniennes',r'\Lambda-algèbres artiniennes','The base is S=Spec(Lambda); Y denotes the varying test spectrum, not a ring.'),
 ('representing topological algebra base letter','Y-algèbre topologique',r'\Lambda-algèbre topologique','The representing inverse-limit algebra is over Lambda, the ring of the affine base.'),
 ('last base scheme letter','points fermés de Y','points fermés de S','The closed points x of X are being restricted to points above closed points of the base S.')]:
  w.writerow([rel,layer,'195-379',line,'C.1',old,new,'Enlarged scan bands confirm the printed defect. '+why+' Existing corrected reading confirmed.','misprint of the original','low'])
event('195-C1-Artinian-tests','targeted proof check','For a local Artinian Y finite over S, its unique point has closed image s, because a finite morphism is closed, and its residue field is finite over kappa(s). An S-map to a locally finite-type X has image x with kappa(x) embedded in that finite extension; hence x is a closed point of the finite-type fiber and therefore of X. The map is given by the compatible local-ring homomorphism O_X,x to A. In this finite-residue setting even an O_S,s-algebra homomorphism is forced to be local: the preimage of the maximal ideal gives a closed point of the finite-type fiber specializing to x, so it equals x. The nilpotent maximal ideal of A makes the map factor through O_X,x/m_x^n and extend uniquely to the completion. Conversely such a continuous map gives the scheme map. Each quotient has finite Lambda-length. Finite Artinian targets split into local factors, so the product of these completed local rings with the product topology represents the full restriction; continuity selects only finitely many components. This verifies the stated recovery of the completed local rings, with the affine-base convention in the paragraph.','195, p. 379, second paragraph and completed-local-ring assertion')
event('195-C1-Picard-prospect','carried as background without fault found','The Picard discussion motivates allowing infinitely many components and nonseparated preschemes. For the projective line over an algebraically closed field, the degrees of O(n), n in Z, already illustrate infinitely many components, while degree zero is the neutral component. The text gives no individual nonseparated Picard example here, so that existence claim remains background for the later Picard discussion. The adjective excellents is not assigned the later technical definition of excellent rings from this sentence alone.','195, p. 379, first paragraph')
record_page('195',379,r'''Compared sources/fr_printed/fr/195.tex entry lines 501–548 and sources/fr/fr/195.tex entry lines 502–549 with scan leaf 12 at 400 dpi, full page and all three enlarged bands. Checked the four inconsistent base letters, the blank target and unclosed parenthesis, F_0 and C_0, the sole local-ring subscripts s and x, completion hat, quotation marks and all underlines.

Removed the unprinted editorial footnote. Both layers restore the printed local-ring notation without added ambient subscripts, explicit F and colon before its display, punctuation, ordinary quotes, selective emphasis, wavy C/O and upright letters. Printed French restores y in Y, the omitted X, the missing closing parenthesis, both Y-algebra expressions and the final base Y. Corrected French retains the six justified repairs, each explicitly recorded. The first paragraph has no added final period.

Checked the closed-image and residue-field arguments for finite Artinian test schemes, locality of the ring maps in this setting, their factorization through finite local quotients and unique extension to completions. The product topology and finite decomposition of the target give the full pro-representation. Picard existence examples not supplied here remain identified background; the elementary projective-line degree example explains the infinitely many components.''')
from update_record_counts import update
update()
