from audit_utils import *
# Resolve the cross-page cocycle issue after reading the pointwise formula on 304.
replace('sources/fr/fr/190.tex',r'p_{31}^*(\varphi)=p_{32}^*(\varphi)\,p_{21}^*(\varphi)',r'p_{31}^*(\varphi)=p_{21}^*(\varphi)\,p_{32}^*(\varphi)','French corrected','190-302','condition (ii), product order','1(c)(ii)','The 400-dpi bottom crop on 302 prints 32 then 21. Page 303 defines p_ij by the ith and jth factors; with that ordered projection, p_ij-star(phi) maps the ith pullback to the jth. Thus the path 3 -> 2 -> 1 is p21-star(phi) p32-star(phi), consistent with the pointwise cocycle read on 304. The original order has mismatched domains in general. The exact matrix witness in scripts/check_190_cocycle_order.py also distinguishes the two orders.','misprint of the original')
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-304',line,statement,'400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 r(r"\varphi_{t,t''}=\varphi_{t,t'}\varphi_{t',t''}",r"\varphi_{t,t''}=\varphi_{t,t'}\varphi_{t',t''},",'ii bis formula punctuation','1(d)(ii bis)',why='A comma follows the formula before the quantifiers.')
 r(r"\qquad\text{pour tout $T$ et tous $t,t',t''\in S'(T)$}.",r"\qquad\text{pour tout $T$ et $t,t',t''\in S'(T)$}",'ii bis quantifiers','1(d)(ii bis)',why='No tous and no terminal period appear in the print.')
 r(r'$\varphi_{t,t}=\varphi_{t,t}^2$,',r'$\varphi_{t,t}^2=\varphi_{t,t}$','idempotence identity','1(d)',why='The square is on the left of the equality; no comma follows it.')
 if tree=='fr_printed':
  r('conséquence de (ii bis) (donc','conséquence de (i bis) (donc','deduction of normalization','1(d)',why='The print mistakenly repeats (i bis); corrected French keeps (ii bis), the cocycle condition actually used.')
 r('(i.e. que','(i. e. que','parenthetical explanation','1(d)',why='The abbreviation is spaced.')
 r('\\subsection*{2. Diagrammes exacts et épimorphismes stricts, morphismes de\ndescente. Exemples}',r'\subsection*{\normalfont 2. \uline{Diagrammes exacts et épimorphismes stricts}, \uline{morphismes de descente}. \uline{Exemples}.}','section 2 heading','2',kind='structure',why='Roman heading, underlined words excluding punctuation, terminal period.')
 r(r'\mathcal C',r'\text{\uwave{C}}','category C occurrences','2.1; 2.2',why='Ordinary C with wavy underline in all six occurrences.',count=6)
 for term in ['exact','noyau','conoyau','épimorphisme strict']:
  r('\\emph{'+term+'}','\\uline{'+term+'}','defining term '+term,'2.1; 2.2',why='Printed underline.')
 r('exact} si, pour tout','exact}, si pour tout','Definition 2.1 condition opening','2.1',why='Comma after exact, none after si.')
 r('(définition 1.2).','(définition 1.2.).','Definition 2.1 reference','2.1',why='Printed period inside the parenthesis, in addition to the sentence period.')
 r('(ou, par abus de','(ou par abus de','Definition 2.1 parenthesis','2.1',why='No comma after ou.')
 old=r'''S\xleftarrow{\alpha}S'
  \overset{\beta_1}{\underset{\beta_2}{\rightrightarrows}}S'''''
 new=old.replace(r'\rightrightarrows',r'\leftleftarrows')
 r(old,new,'dual exact diagram','2.1',why='Both beta arrows point left, unlike the earlier equalizer diagram on this page.')
 r(r'\overset{p_1}{\underset{p_2}{\rightrightarrows}}',r'\overset{p_1}{\underset{p_2}{\leftleftarrows}}','kernel-pair diagram at foot','2.2',why='Both projection arrows point left.')
 r("strict} si c'est", "strict}, si c'est",'Definition 2.2 after defining term','2.2',why='Comma follows strict.')
 r('et si, pour tout','et si pour tout','Definition 2.2 universal condition','2.2',why='No comma after si.')
 upright_page(rel,layer,'190-304')
with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 csv.writer(f,delimiter='\t').writerow(['sources/fr/fr/190.tex','French corrected','190-304','deduction of normalization','1(d)','conséquence de (i bis)','conséquence de (ii bis)','Confirmed the supplied corrected reference: the 400-dpi top band prints i bis, but the proof specializes the cocycle ii bis to equal points and then cancels an invertible idempotent.','misprint of the original','low'])
event('190-1c-cocycle-order','refuted, with the refined statement\'s id','With p_ij=(p_i,p_j) as read in the continuation, p_ij-star(phi) goes from factor i to factor j. The p. 302 right-hand product has reversed composability. Corrected formula: p31-star(phi)=p21-star(phi) p32-star(phi), refined id 190-1c-cocycle-order-corrected. The p. 304 pointwise identity confirms right-to-left composition and this correction. The printed projection convention/order interpretation remains explicit for final review.','190, pp. 302–304, (ii), projection definition, and (ii bis)')
event('190-1c-cocycle-order','computation or formal certificate','Executed an exact integer-matrix witness, now preserved in scripts/check_190_cocycle_order.py: g1=I, g2=((1,1),(0,1)), g3=((1,0),(1,1)); phi(i,j)=g_j g_i^-1. p31=((1,0),(-1,1)); printed p32*p21=((0,1),(-1,2)); corrected p21*p32=p31. This is a concrete witness for the order issue under the stated ordered projection, not a certificate of a general descent theorem.','190, p. 302, (ii)')
event('190-1d-normalization','targeted proof check','Verified that an invertible idempotent is identity by composing e^2=e with e^-1. Thus ii bis implies i bis for isomorphisms; confirmed corrected reference ii bis rather than printed i bis. Without invertibility a nonidentity idempotent supplies a counterexample. With both normalization and the cocycle, phi(t,t-prime) and phi(t-prime,t) are mutual inverses, by applying the cocycle in both orders.','190, p. 304, paragraph after (ii bis)')
event('190-2.1','targeted proof check','The Hom equalizer condition is the universal property of an equalizer. Two such pairs map uniquely to one another and the composites are identities by uniqueness. In sets evaluation at a singleton recovers the set equalizer and conversely the universal property works for all test sets. The dual assertion is the coequalizer universal property; restored the scan’s leftward arrows.','190, p. 304, Definition 2.1')
event('190-2.2','targeted proof check','Checked strict epimorphism definition and the start of the kernel-pair formulation: a pair beta1,beta2 equalized by alpha factors uniquely through S-prime times_S S-prime, so equality on its projections is equivalent to equality for all such pairs. Epimorphy supplies uniqueness of the factorization. The concluding exactness phrase continues on p. 305.','190, p. 304, Definition 2.2')
record_page('190',304,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 271–332 with scan leaf 7 at 400 dpi and all three enlarged bands. Read (ii bis), every prime and composition in the following argument, the full section 2 heading, Definitions 2.1–2.2 and all four diagrams. The marker correctly follows the final kernel-pair display.

Restored the comma before the quantifiers in (ii bis), absence of tous and final period, the order e^2=e, omission of its following comma, spaced i. e., underlined roman heading and terms, wavy C, printed comma positions, period inside the 1.2 reference parenthesis, and leftward arrows in the two coequalizer diagrams. The forward arrows in the equalizer diagrams are retained. Confirmed corrected reference (ii bis) in the normalization argument; the scan’s mistaken (i bis) is restored only in printed French.

Resolved the p. 302 cocycle issue using the ordered projection definition on 303 and the pointwise equation on this page. Corrected French now has p31-star(phi)=p21-star(phi) p32-star(phi); printed French retains the reversed product. Recorded domain/codomain reasoning and an exact 2-by-2 integer-matrix witness. This is explicitly conditional on the ordered projection (p_i,p_j) given by the prose, and is subject to the final correction reread. Rechecked normalization, mutual inverses, equalizer uniqueness and the kernel-pair universal-property argument; no modern terminology replaces the author’s noyau/conoyau/strict usage.''')
from update_record_counts import update
update()
