from audit_utils import *
omissions=[
 ("$\\text{\\uwave{A}}'$-\\uline{module", "$A'$-\\uline{module", 'basis statement'),
 ("des $\\text{\\uwave{A}}$-dérivations", "des $A$-dérivations", 'derivation base'),
 ("dérivations de $\\text{\\uwave{A}}'$", "dérivations de $A'$", 'derivation argument'),
 ("de $\\text{\\uwave{A}}'$-modules localement", "de $A'$-modules localement", 'locally free module'),
 ("sous-$\\text{\\uwave{A}}'$-module", "sous-$A'$-module", 'lemma submodule')]
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='B.3 example 2',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-321',line,statement,'400-dpi full scan and three enlarged bands. '+why,kind,count=count)
 r('« formel », i.e.',r'\fquote{formel}, i. e.','opening words','B.3 example 1',why='Double quotation marks and spaced abbreviation.')
 r(r'de $\mathcal U$ (muni',r'de $\mathcal U$, (muni','opening parenthesis','B.3 example 1',why='Printed comma before the parenthesis.')
 r("$\\mathcal U$ admet, en tant que\n$\\mathcal A'$-module à gauche, une base formée des sections de $\\mathcal U$ qui\ncorrespondent aux éléments de $\\Gamma$.","$\\mathcal U$ \\uline{admet, en tant que}\n$\\mathcal A'$-\\uline{module à gauche, une base formée des sections de} $\\mathcal U$ \\uline{qui correspondent aux éléments de} $\\Gamma$.",'basis assertion','B.3 example 1',why='Printed underlining excludes the mathematical identifiers.')
 r(r'\textsc{Exemple 2 (« Cartier »).} --',r'\result{EXEMPLE}{2 (\fquote{CARTIER})}','heading',why='Roman capitals, double quotation marks and short dash.')
 r('i.e.','i. e.','explanatory abbreviations',count=3,why='Printed spaced abbreviation.')
 r('est de caractéristique $p$','est de \\uline{caractéristique} $p$','characteristic hypothesis',why='Selective underline.')
 r(r"$(\mathcal A')^p\subset",r"$\mathcal A'^p\subset",'height-one hypothesis',why='No parentheses around A-prime.')
 r('est radiciel de\nhauteur 1','est \\uline{radiciel de hauteur} 1','height-one explanation',why='The word phrase is underlined; the numeral is not.')
 r('admet\nlocalement une $p$-base','\\uline{admet localement une} $p$-\\uline{base}','basis hypothesis',why='Selective prose underlining.')
 r(r'\mathfrak g',r'\mathfrak G','three derivation-sheaf identifiers',count=3,why='The handwritten Gothic identifier is the capital G form used for derivations earlier in the work.')
 r('[X,fY]=X(f)Y+f[X,Y].','[X,fY]=X(f)Y+f[X,Y]','formula end','(3.5)',why='No terminal period.')
 r(r'\textsc{Lemme.} --',r'\result{LEMME}{}','lemma heading',why='Roman capitals and single short dash.')
 r('relations supplémentaires\n','relations supplémentaires :\n','before relations','(3.6)',why='Printed colon.')
 r(r'Xf-fX&=X(f),',r'Xf-fX&=X(f)','first relation','(3.6)',why='No terminal comma.')
 r(r'XY-YX&=[X,Y],',r'XY-YX&=[X,Y]','second relation','(3.6)',why='No terminal comma.')
 r(r'X^p&=X^{(p)}.',r'X^p&=X^{(p)}','third relation','(3.6)',why='No terminal period.')
 for old,new,label in [(r'\overline{fX}&=f\overline X,',r'\symup{\overline{fX}}&\symup{=f\overline X}', '(3.7)'),(r'\overline X(fx)&=X(f)x+f\overline X(x),',r'\symup{\overline X(fx)}&\symup{=X(f)x+f\overline X(x)}','(3.8)'),(r'\overline{[X,Y]}&=[\overline X,\overline Y],',r'\symup{\overline{[X,Y]}}&\symup{=[\overline X,\overline Y]}','(3.9)'),(r'\overline{X^{(p)}}&=\overline X^p.',r'\symup{\overline{X^{(p)}}}&\symup{=\overline X^p}','(3.10)')]:
  r(old,new,'display',label,why='Upright variables; none of these four displays has terminal punctuation.')
 r('une connexion linéaire sur','une \\uline{connexion linéaire sur}','connection interpretation',why='Printed underline.')
 r('sans\ncourbure et compatible avec la puissance','\\uline{sans courbure} et \\uline{compatible avec la puissance}','connection qualifications',why='The conjunction is outside the two underlined spans.')
 r('$p$-ième.)','$p$-ième).','parenthesis end',why='Period outside the closing parenthesis.')
 r('sont des dérivations de','sont des \\uline{dérivations} de','scheme application',why='Printed underline.')
 for old,new,label in [(r'\mathcal U',r'\text{\uwave{U}}','endomorphism algebra'),(r'\mathcal O',r'\text{\uwave{O}}','structure ring'),(r'\mathcal A',r'\text{\uwave{A}}','coefficient algebra'),(r'\operatorname{Hom}',r'\mathop{\text{\uwave{Hom}}}\nolimits','internal Hom')]:
  s,_,_=page_text(rel,321)
  r(old,new,'all '+label+' identifiers',why='Ordinary printed letters with wavy underlines, subject to the separately recorded omissions.',count=s.count(old))
 if tree=='fr_printed':
  for old,new,label in omissions:
   r(old,new,label,why='The scan omits the wavy underline at this occurrence of the same algebra identifier.')
 upright_page(rel,layer,'190-321')
with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 for new,old,label in omissions:
  w.writerow(['sources/fr/fr/190.tex','French corrected','190-321',label,'B.3',old,new,'The enlarged scan omits the wavy underline here. This denotes the same algebra A or A-prime explicitly defined and wavy-underlined on this page, so the corrected layer supplies its identifying typography.','misprint of the original','low'])
event('190-B3-example1-basis','targeted proof check','The Galois-torsor basis assertion follows after the faithfully flat base change trivializing the torsor: B becomes a product of copies of the base ring indexed by Gamma. Multiplication by the primitive idempotents followed by the permutation operators for Gamma gives all matrix units in End_A(B). Thus the group operators form a left B-basis, and the isomorphism descends by faithful flatness.','190, p. 321, opening assertion')
event('190-B3-example2-hypothesis','targeted proof check','The enlarged print really says x_i^p=0. Taken literally, this assumes locally B=A[x_1,...,x_n]/(x_1^p,...,x_n^p), a finite free height-one radicial extension of rank p^n. This stronger hypothesis is internally consistent and is retained in both French layers. It should not silently be replaced with the more general p-basis relations x_i^p=a_i in A.','190, p. 321, example 2 definition of p-base')
event('190-3.5','targeted proof check','For A-derivations X,Y of B, applying both sides to b gives X(fY(b))-fY(X(b))=X(f)Y(b)+f[X,Y](b). In characteristic p, the intermediate binomial coefficients in the iterated Leibniz rule vanish, so X^p is again a derivation. Thus the derivations form a restricted Lie algebra over A; the displayed extra term explains why the bracket is not B-bilinear.','190, p. 321, (3.5)')
event('190-3.6','targeted proof check','Locally choose the printed p-basis and coordinate derivations partial_i. They commute and partial_i^p=0. The relations move coefficients to the left and reduce every word to a B-linear combination of partial^alpha with 0<=alpha_i<p. These operators form a B-basis of End_A(B): evaluate successively on the basis monomials x^beta, in increasing total degree. Previously determined coefficients account for all alpha<beta, while the coefficient of partial^beta is multiplied by beta!, a unit because each beta_i<p. This constructs a unique expansion of any A-linear endomorphism. It proves both generation and absence of additional relations.','190, p. 321, lemma and (3.6)')
event('190-3.7-3.10','targeted proof check','Under the restricted Lie-module interpretation, B-linearity in X is (3.7), commuting the coefficient multiplication with X gives the Leibniz condition (3.8), and the bracket and restricted-power relations give (3.9) and (3.10). The lemma therefore identifies such a representation with an End_A(B)-module extending its given B-module, hence with the descent datum checked on 319. Zero curvature is (3.9), and compatibility with restricted p-th power is (3.10). Additivity of the Lie action is part of that representation interpretation; the displayed identities are not being claimed here as a separate proof of additivity.','190, p. 321, (3.7)–(3.10)')
event('190-B3-example2-schemes','used and rechecked in this run','For the height-one radicial map the two projections of the descent groupoid induce the same map on underlying spaces, so the moving-open obstruction recorded for general schemes on 320 is absent here. On affine opens, compatibility with the algebra multiplication is exactly the derivation rule for each X-bar, since X(bc)=X(b)c+bX(c). The local algebra data glue. Effectivity invokes theorem 3; the full proof of that theorem remains background, not a new proof claimed here.','190, p. 321, final paragraph')
record_page('190',321,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 1149–1206 with scan leaf 24, rendered at 400 dpi and read as a full page and in all three enlarged bands. Read the Galois basis assertion, every p-th power, the Gothic derivation identifier, all commutators, bars and tagged relations, and the final scheme application.

Restored the wavy algebra and Hom identifiers, capital Gothic G, selective prose underlining, double quotation marks, capitals and short heading dashes, the comma before the opening parenthesis, the absence of parentheses around A-prime in its p-th power, the colon before (3.6), display punctuation and the final parenthesis punctuation. The printed layer records five omitted algebra underlines; the corrected layer retains the consistent identifiers, with five explicit correction rows. Both layers preserve the literal hypothesis x_i^p=0, which defines a valid stronger special case.

Checked the Galois basis after trivializing the torsor. Proved the restricted derivation presentation using coordinate derivations and triangular evaluation on the monomial basis, including why the factorial coefficients are units. Checked (3.5) and the interpretation of (3.7)–(3.10) as a restricted Lie-module action. The general scheme application is compatible with fixed opens in this radicial case; its effectivity still uses theorem 3 as background. No broader p-basis hypothesis or full proof of theorem 3 has been inserted into the text.''')
from update_record_counts import update
update()
