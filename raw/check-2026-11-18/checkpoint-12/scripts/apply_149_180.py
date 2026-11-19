from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/149.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'149-180',line,statement,'400-dpi image and three enlarged page bands, including all formula indices and punctuation. '+why,kind,count=count)
 r(r"\Homsh_{\Osh_X}(L_{*}\otimes L'_{*},\Omega_X^{p+p'}),",r"\Homsh_{\Osh_X}(L_{*}\otimes L'_{*},\Omega_X^{p+p'})",'first display','4-thm1',why='No comma follows the pairing display.')
 old="  \\qquad(i>0),\n\\]\ndu fait"
 new="\\]\npour $i>0$, du fait"
 r(old,new,'Tor vanishing display and next line','4-thm1','structure','The condition is prose after the display: pour i>0, du fait.')
 r(r'$Z\longmapsto P_X(Z)$',r'$Z\longrightarrow P_X(Z)$','before 4.7','4.7',why='The printed assignment uses an ordinary arrow.')
 r('valable si $Z$, resp.', 'valable si $Z$ resp.','after 4.7','4.7',why='No comma occurs after the first Z.')
 r('« image inverse »',r'\fquote{image inverse}','before 4.8','4.8',why='Ordinary double quotes are printed.')
 r('« transversale »',r'\fquote{transversale}','after 4.8','4.8',why='Ordinary double quotes are printed.')
 r(r"=f^{*}\bigl(P_{X'}(Z')\bigr),",r"=f^{*}\bigl(P_{X'}(Z')\bigr)",'4.8','4.8',why='There is no terminal comma.')
 if tree=='fr_printed':
  r(r"H_i(L\otimes L')=",r"H_i(L\otimes L').=",'Tor vanishing display','4-thm1',why='The print has a stray dot immediately before the equality sign; corrected French omits it.')
  r('dans la proposition\n4','dans proposition\n4','after 4.6','4.6',why='The article la is absent; corrected French retains the grammatical repair.')
  r(r"P_{X'}(Z')\bigr)",r"P_{X'}(Z)\bigr)",'4.8','4.8',why='The right-hand class has Z without its prime. Corrected French keeps Z prime, the cycle on the target used on the left.')
  r("formule valable si $Z'$",'formule valable si $Z$','after 4.8','4.8',why='The first cycle name in the explanatory sentence lacks its prime; corrected French keeps Z prime.')
  r("à $Z'$, i.e.",'à $Z$, i.e.','after 4.8','4.8',why='The transversality clause also omits the prime. The final product X times Z prime confirms the intended cycle.')
 else:
  r("d'isomorphismes analogue à (4.3)","d'homomorphismes analogue à (4.3)",'7–8','4-thm1','misprint of the original','The left map of (4.3) need not be invertible: for X=A1, Y={0}, p=1 its source is k and target H1(X,Omega1)=0. Only the right edge map is an isomorphism.')
 txt,_,_=page_text(rel,180);r(r'\Omega',r'\underline{\Omega}','differential sheaf notation','4',why='The Greek sheaf letters are underlined.',count=txt.count(r'\Omega'))
 upright_page(rel,layer,'149-180')
event('149-4-thm1-diagram','refuted, with the refined statement\'s id','Refined statement 149-4-thm1-diagram-corrected: the bottom row identifies with the diagram of homomorphisms (4.3), whose right arrow is an isomorphism. Counterexample to all arrows being isomorphisms: X=Spec k[t], Y=V(t), p=1. The resolution A --t--> A gives Ext_A^1(A/(t),Omega_A^1)=k, whereas affine H^1(X,Omega_X^1)=0. Taking Y prime=X gives a transverse pair with this same bottom row.','149, p. 180, lines 7–8')
event('149-4.6','carried as background without fault found','Read the local compatibility of fundamental sections. Author delegates the calculation to the Koszul resolutions of Proposition 4; its details remain an item for the notes, not a claimed completed re-proof.','149, p. 180, formula (4.6) and following lines')
event('149-4.7','carried as background without fault found','Read the exterior-product compatibility and its hypotheses; proof is asserted to be similar and easier.','149, p. 180, formula (4.7)')
event('149-4.8','targeted proof check','Typed the domains in the pullback identity: f maps X to X prime, so the target cycle in P_Xprime and both transversality clauses must be Z prime, matching f inverse(Z prime) and X times Z prime. The supplied three prime repairs are confirmed; printed French restores their omissions.','149, p. 180, formula (4.8) and last three lines')
record_page('149',180,r'''Compared sources/fr_printed/fr/149.tex entry lines 587–635 and sources/fr/fr/149.tex entry lines 590–638 against scan leaf 13 at 400 dpi and three enlarged bands. Read the end of the intersection proof, the pairing and homology displays, (4.6), Cartesian-product compatibility (4.7) and transverse pullback (4.8), including every prime and the final graph criterion.

Both layers restore the external prose condition pour i>0, the ordinary assignment arrow, Greek sheaf underlines, quotes and literal display punctuation. Printed French restores a stray dot before the homology equality, the omitted article before proposition 4 and three missing primes in (4.8) and its explanation. Corrected French keeps the existing repairs. A new mathematical correction changes diagramme d'isomorphismes to diagramme d'homomorphismes in corrected French only: an explicit affine-line counterexample is recorded in CHECK_EVENTS.tsv. The local calculation for (4.6) and the omitted proof of (4.7) are flagged for the later notes without being represented as verified proofs.''')
from update_record_counts import update
update()
