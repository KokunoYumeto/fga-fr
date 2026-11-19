from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1,full=False):
  replace(rel,a,b,layer,'182-212',line,statement,'400-dpi full page and enlarged top, middle and bottom crops. '+why,kind,count=count,full=full)
 r('\\src{213}\n','','page boundary','8-prop4','structure','The printed page ends at Alors le revêtement.',full=True)
 r("$Y'$ de $Y$ associé à $f_*(\\Osh_X)$ est non ramifié.","\\src{213}\n$Y'$ de $Y$ associé à $f_*(\\Osh_X)$ est non ramifié.",'last line','8-prop4','structure','Move marker 213 before the continuation Y-prime de Y.',full=True)
 txt,_,_=page_text(rel,212)
 r(r'\Osh','O','structure sheaves','',why='Plain upright O throughout.',count=txt.count(r'\Osh'))
 r(r'\mathcal A',r'\text{\uwave{A}}','Lemma 4 proof','8-lem4',why='Wavy-underlined ordinary A, not script A.',count=4)
 r(r'\kappa',r'\varkappa','Proposition 4 residue fields','8-prop4',why='Crossed handwritten kappa.',count=3)
 for a,b in [(r'\textit{i.}','i.'),(r'\textit{ii.}','ii.'),(r'\textit{i bis.}','i. bis'),(r'\textit{(i)}','(i)'),(r'\textit{(ii)}','(ii)')]:
  r(a,b,'Lemma 3 conditions','8-lem3',why='Roman labels and references; i. bis has the dot after i.')
 r(r'\emph{géométriquement trivial}',r'\uline{géométriquement trivial}','definition after Lemma 3','8-lem3',why='Printed underlining.')
 r("$Y'$ de $Y$\n(correspondant", "$Y'$ de $Y$,\n(correspondant",'Lemma 4 proof opening','8-lem4',why='The comma before the parenthesis is printed.')
 if tree=='fr_printed':
  r(r'$f_*(O_X)=O_Y$',r"$f_*(O_{X'})=O_Y$",'Lemma 4 first line','8-lem4',why='The printed structure-sheaf index has a prime. Corrected French uses O_X, the structure sheaf of the domain of f.')
  r(r'$f^*(\text{\uwave{A}})$',r'$f_*(\text{\uwave{A}})$','Lemma 4 proof, En effet','8-lem4',why='The star is printed below f. The sheaf A is on Y and must be pulled back to X; corrected French retains f-star superscript.')
  r(r'\result{PROPOSITION}{4} Soit $f:X\longrightarrow Y$',r'\result{PROPOSITION}{4} Soit $f:X\longrightarrow X$','Proposition 4 first line','8-prop4',why='The printed target is X; the base is Y throughout the statement, so corrected French retains Y.')
 # Selective underlining in the continuation of Lemma 3.
 for a in ['est complètement décomposé sur','Le morphisme naturel','est un isomorphisme','Sous ces conditions','est une extension','Enfin, si','est connexe, la condition','équivaut à la condition suivante\nplus faible en apparence','admet une section régulière\n    au-dessus de']:
  r(a,r'\uline{'+a+'}','Lemma 3 conclusion prose','8-lem3',why='Underline exactly the printed prose spans; non ramifiée remains plain.')
 r('non ramifiée de $A$',r'non ramifiée \uline{de} $A$','Lemma 3 first conclusion','8-lem3',why='Only de is underlined after non ramifiée.')
 # Lemma 4 leaves surjectif plain, and Lemma 5 leaves its connectedness aside plain.
 for n in [4,5]:
  txt,_,_=page_text(rel,212); marker='\\result{LEMME}{'+str(n)+'} ';a=txt.index(marker)+len(marker);b=txt.find('\n\n',a);old=txt[a:b]
  parts=re.split(r'(\(il est connexe\)|\\\[.*?\\\]|\(où .*?\)\.)',old,flags=re.S)
  new=''.join(x if i%2 else underline_prose(x) for i,x in enumerate(parts))
  if n==4:new=new.replace(r'\uline{est surjectif}',r'\uline{est} surjectif')
  r(old,new,'Lemma '+str(n)+' statement prose','8-lem'+str(n),why='Restore printed underlines, leaving mathematical spans and the indicated asides plain.')
 txt,_,_=page_text(rel,212);marker=r'\result{PROPOSITION}{4} ';a=txt.index(marker)+len(marker);old=txt[a:].rstrip()
 # Plain phrase inside an otherwise underlined parenthetical explanation.
 parts=re.split(r'(schéma séparable|i\.e\.)',old)
 new=''.join(x if i%2 else underline_prose(x) for i,x in enumerate(parts))
 r(old,new,'Proposition 4 statement prose','8-prop4',why='The parenthetical explanation is selectively underlined; schéma séparable and i. e. are plain.')
 upright_page(rel,layer,'182-212')
event('182-8-lem3','carried as background without fault found','Read both equivalent conditions, finite unramified A-prime, and the connected-cover section criterion. A proof needs invariance of finite étale covers under nilpotent thickenings, descent of geometrically constant covers, and the decomposition of the global finite algebra over an algebraic closure. These are identified as background, not independently established here. The weaker section criterion uses transitivity for a connected cover after arithmetic descent.','182, pp. 211–212, Lemma 3')
event('182-8-lem4','targeted proof check','For a finite locally free algebra A on Y, projection formula gives f_*f^*A = A tensor f_*O_X = A. A nontrivial open-and-closed splitting of the pullback cover gives two nonzero algebra summands, whose units give nonzero direct-image summands. Thus a connected finite étale Y-cover stays connected on X, the criterion for surjectivity on pi_1. Printed O_X-prime has the wrong domain and printed f_*A the wrong variance; corrected O_X and f^*A are confirmed. The Galois-category criterion is used as background.','182, p. 212, Lemma 4 and proof')
event('182-8-lem5','targeted proof check','Checked the cited assembly: injectivity is the algebraic-field-extension consequence of Lemmas 1–2; Lemma 3 characterizes covers trivialized over the algebraic closure and supplies middle exactness; factor X -> Spec A -> Spec k, apply Lemma 4 to the first morphism and radicial invariance to the second for surjectivity. Nilpotent invariance is needed to replace A by its residue field. The displayed b is the image base point on Spec k; leaving this implicit is not a misprint. Dependencies on Lemmas 2–3 are retained as background.','182, p. 212, Lemma 5 and proof')
event('182-8-prop4-target','targeted proof check','The morphism target must be Y, not the printed X: y ranges over Y, the fibers are f-inverse(y), and the Stein algebra defines a covering of Y. The conclusion and proof continue on page 213 and remain to be checked there.','182, p. 212, Proposition 4 first line')
record_page('182',212,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 909–966 with scan leaf 21, rendered at 400 dpi, and all three enlarged bands. Read the conclusion of Lemma 3, Lemmas 4–5 and their proofs, and the opening of Proposition 4. Moved marker 213 before Y-prime de Y, where the printed continuation begins.

Restored plain O, wavy-underlined A, crossed kappa, roman condition labels, the printed i. bis punctuation, the comma in the proof of Lemma 4, and selective prose underlines. Printed French now retains the prime in Lemma 4's O_X-prime, the subscript star in f_*A, and Proposition 4's target X. Corrected French retains O_X, f^*A and target Y, each justified by the objects and variance of the morphisms. Checked Lemma 4 by projection formula and connected-cover criterion, and the logical assembly of Lemma 5 using the stated background; Lemma 3's deeper descent ingredients are explicitly recorded as background. Proposition 4's conclusion awaits the next printed page.''')
p='CHECK_RECORD.md';t=read(p).replace('## Open reading questions','- 182-212, Lemma 4: confirmed O_X and pullback f^*A instead of printed O_X-prime and f_*A; Proposition 4 target Y instead of X.\n\n## Open reading questions');write(p,t)
from update_record_counts import update
update()
