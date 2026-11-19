from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='4(c)',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-312',line,statement,'400-dpi full image and all three enlarged bands. '+why,kind,count=count)
 r(r'G_\xi',r'G','three coefficient functors in first paragraph',why='The print abbreviates the fixed coefficient functor to G without the xi index; restored in both layers.',count=3)
 text,_,_=page_text(rel,312)
 spans=[]
 for m in re.finditer(r'\\emph\{',text):
  i=m.end();depth=1
  while depth:
   if text[i]=='{':depth+=1
   if text[i]=='}':depth-=1
   i+=1
  spans.append((text[m.start():i],text[m.end():i-1]))
 for index,(old,plain) in enumerate(spans):
  formatted=underline_prose(plain)
  formatted=formatted.replace("$\\mathcal F_{S'}$ \\uline{à} $\\xi\\times_SS'$","$\\mathcal F_{S'}$ à $\\xi\\times_SS'$")
  r(old,formatted,f'first paragraph emphasis {index+1}',why='Prose underlined, mathematical variables and outer punctuation excluded; the isolated à before the final pullback is not underlined.')
 r("et $H^1(S'/S,G)$","\\uline{et} $H^1(S'/S,G)$",'line 3',why='The conjunction et is underlined.')
 r("$\\xi'=\\xi\\times_SS'$. Si donc", "$\\xi'=\\xi\\times_SS'$ Si donc",'line 5',why='No sentence period is visible after the fiber product.')
 r("$\\mathcal F_{S'}$, \\uline{sont isomorphes", "$\\mathcal F_{S'}$ \\uline{sont isomorphes",'line 5',why='No comma after the category letter.')
 old="Si donc\n$\\alpha:S'\\longrightarrow S$ est un morphisme de $\\mathcal F$-descente\n(cf. (b)), alors"
 new=underline_prose("Si donc $\\alpha:S'\\longrightarrow S$ est un morphisme de $\\mathcal F$-descente")+" (cf. (b)), \\uline{alors}"
 r(old,new,'line 6',why='This hypothesis and alors are also underlined, except the parenthetical reference.')
 if tree=='fr_printed':
  r(r'$\mathcal F$-descente strict.)',r'$S$-descente strict).','last parenthetical line',why='The print has ordinary S-descente, not script F-descente; the period follows the closing parenthesis.')
 else:
  r(r'$\mathcal F$-descente strict.)',r'$\mathcal F$-descente strict).','last parenthetical line',why='The period follows the closing parenthesis.')
 r('géométrie algébrique, notamment dans la « cohomologie de Weil » des préschémas.','géométrie algébrique, (notamment dans la \\fquote{cohomologie de Weil} des préschémas).','remark final line','4 remark',why='Printed parenthesis and double quotes. Here préschémas is unhyphenated.')
 for letter,num in [('d',1),('e',2)]:
  r('\\medskip\\noindent\n'+letter+'. \\result{EXEMPLE}{'+str(num)+'}', '\\result{'+letter+'. EXEMPLE}{'+str(num)+'}',f'example {num} heading',f'4({letter})',kind='structure',why='Letter and example title run together in the same paragraph.')
 r('« formellement principal sur $S$, de groupe $\\Gamma$ »',r'\fquote{formellement principal sur $S$, de groupe $\Gamma$}','Example 1 terminology','4(d)',why='Double quotes.')
 r('i.e.','i. e.','Example 1 explanatory abbreviation','4(d)',why='Printed spacing.')
 r('interviennent ici existent.)','interviennent ici existent).','Example 1 parenthesis','4(d)',why='Period outside the closing parenthesis.')
 old="est canoniquement\nisomorphe au groupe simplicial de cochaînes standard homogènes\n$C^*(\\Gamma,F(S'))$, donc $H^*(S'/S,F)$ est canoniquement isomorphe à\n$H^*(\\Gamma,F(S'))$."
 r(old,underline_prose(old),'Example 1 concluding assertion','4(d)',why='The prose is underlined; mathematical expressions and final period are not.')
 if tree=='fr':
  r('groupe simplicial de cochaînes','groupe cosimplicial de cochaînes','Example 1 concluding assertion','4(d)',kind='misprint of the original',why='As in 4(a), F is contravariant and sends the simplicial nerve to a cosimplicial abelian group. The cofaces increase degree.')
 r('la catégorie des préschémas. On désigne','la catégorie des pré-schémas. On désigne','Example 2 first line','4(e)',why='Here pré-schémas has a printed hyphen.')
 r('« groupe additif »',r'\fquote{groupe additif}','Example 2 additive term','4(e)',why='Double quotes.')
 r('« groupe multiplicatif »',r'\fquote{groupe multiplicatif}','Example 2 multiplicative term','4(e)',why='Double quotes.')
 r("« groupe linéaire d'ordre\n$n$ »",r"\fquote{groupe linéaire d'ordre $n$}",'Example 2 last term','4(e)',why='Double quotes.')
 r('(groupe des éléments inversibles',r'($=$ groupe des éléments inversibles','Example 2 units explanation','4(e)',why='An equals sign is printed at the start of the parenthesis.')
 if tree=='fr_printed':
  r("par $G_a$ (\\fquote{groupe additif}) le foncteur contravariant de $\\mathcal C$","par $G_a$ (\\fquote{groupe additif}) le foncteur contravariant de $G$",'Example 2 domain category','4(e)',why='The printed domain letter is ordinary G. Corrected French keeps the prescheme category C.')
 r(r'\mathcal O',r'\text{\uwave{O}}','three structure-sheaf letters','4(e)',why='Ordinary wavy-underlined O.',count=3)
 page,_,_=page_text(rel,312)
 r(r'\mathcal C',r'\text{\uwave{C}}','category letters','4',why='Ordinary wavy-underlined C.',count=page.count(r'\mathcal C'))
 upright_page(rel,layer,'190-312')
with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 for line,statement,old,new,reason in [
  ('last parenthetical line','4(c)','$S$-descente strict','$\\mathcal F$-descente strict','S is the base object, whereas the effectiveness condition is strict descent for the fibered category F.'),
  ('Example 2 domain category','4(e)','contravariant de $G$','contravariant de $\\text{\\uwave{C}}$','The just-defined domain is the category C of preschemes; G is not a category here.')]:
  w.writerow(['sources/fr/fr/190.tex','French corrected','190-312',line,statement,old,new,'Confirmed the supplied corrected identifier against the clearly different printed letter in the enlarged band. '+reason,'misprint of the original','low'])
event('190-4c-forms-classification','targeted proof check','Using the canonical descent datum on the pullback of xi, an arbitrary descent isomorphism is encoded by an automorphism-valued cocycle; the corrected order from 311 is exactly its composition identity. Changing the identification with xi-prime acts by the printed gauge formula. Thus H¹ parametrizes descent objects whose underlying pullback is isomorphic to xi-prime. Full faithfulness makes objects over S inject into these isomorphism classes; equality is equivalent to effectiveness for this fixed pullback. This proves the stated classification and the strict-descent sufficient condition.','190, p. 312, 4(c)')
event('190-4d-group-cochains','refuted, with the refined statement\'s id','The unconditional comparison for an arbitrary contravariant F is false. Refined statement 190-4d-group-cochains-with-coproduct-condition: require the iterated torsor fiber powers to identify with the relevant coproducts and F to send those coproducts to products. Counterexample: finite sets, S a point, S-prime the regular two-point C2-torsor, and the constant functor F=Z with every map the identity. The Čech degree-one group is Z, whereas the standard group-cochain degree-one group is Z². In fact the former complex alternates zero and identity and has no positive cohomology; H²(C2,Z)=Z/2 via the exact two-periodic resolution, whose maps on Z[C2] are gamma−1 and 1+gamma. Their kernels/images are checked directly on a+b gamma. The omitted hypotheses are a substantive gap, retained for the notes rather than silently inserted into the historical exposition.','190, p. 312, 4(d), Example 1')
event('190-4d-group-cochains-refinement','targeted proof check','Under the stated refinement, degree n is Map(Gamma^n,F(S-prime)); the face maps are the usual inhomogeneous group differential after the torsor identification. Homogenization identifies this with equivariant homogeneous cochains. F(K) is cosimplicial, consistent with 4(a), so corrected French changes simplicial to cosimplicial in this one description. No blanket claim that arbitrary F preserves coproducts is made.','190, p. 312, 4(d), Example 1')
event('190-4e-standard-group-functors','targeted proof check','Global functions pull back contravariantly and define the additive functor; ring homomorphisms preserve units, giving the multiplicative functor. The units star is on the entire H⁰ ring. The general linear group definition continues on 313.','190, p. 312, 4(e), Example 2')
record_page('190',312,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 689–742 with scan leaf 15 at 400 dpi, full page and all three enlarged bands. Read the full forms classification and both examples, including every Greek index, star, parenthesis, font and inline/display choice.

Restored the printed abbreviation G for fixed G_xi in both layers, detailed prose underlines, parenthesis punctuation, the parenthesized Weil-cohomology remark, double quotes, spaced i. e., run-in example headings, the equals sign in the units explanation, and wavy-underlined C/O. The remark's préschémas is unhyphenated; Example 2 has pré-schémas. Restored S-descente and the ordinary G domain letter in printed French, explicitly confirming the supplied corrected F and C. Corrected simplicial to cosimplicial only in corrected French.

Checked the H¹ classification using the cocycle/gauge formulas and full faithfulness. Found a substantive missing hypothesis in Example 1: arbitrary F need not take coproducts to products. A constant-Z functor on finite sets gives a degree-one rank counterexample and different H² for C2. The historical assertion remains in the exposition; the event records the counterexample and an explicit refined statement for the later notes, without merging author errata or silently adding hypotheses.''')
from update_record_counts import update
update()
