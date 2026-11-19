from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/195.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'195-388',line,'C.5','400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 s,_,_=page_text(rel,388)
 notes=list(footnotes(s)); assert len(notes)==1
 a,b,n=notes[0]
 r(s[a:b],'','editorial completed-stalk erratum footnote',kind='structure',why='The footnote is absent from the printed exposé. The author erratum remains in its own section.')
 r("(induisant l'identité sur $X'_0$), de", "(induisant l'identité sur $X'_0$) de",'opening parenthesis punctuation',why='There is no comma after the closing parenthesis.')
 r('forment un faisceau sur',r'forment un \uline{faisceau} sur','sheaf assertion emphasis',why='Only faisceau is underlined.')
 r('le faisceau constant dont',r'le faisceau \uline{constant} dont','constant-sheaf emphasis',why='Only constant is underlined.')
 old=r'''on a
\[
  G_x=G\bigl(\operatorname{Spec}(\mathcal O_{\mathfrak X,x})\bigr)
  \subset
  G\bigl(\operatorname{Spec}(\widehat{\mathcal O}_{\mathfrak X,x})\bigr),
\]
(= classes'''
 new=r'''on a $G_x=G(\operatorname{Spec}(\widehat{\mathcal O}_{\mathfrak X,x}))$ (= classes'''
 r(old,new,'part b completed-stalk formula',kind='structure',why='The scan has a direct equality with the completed local ring, inline, with no intermediate uncompleted term or inclusion. Those later amendments must not be merged into either exposé layer.')
 r(r"$\widehat{\mathcal O}'_{0x}$",r"$\mathcal O'_{0x}$",'part b marked algebra',why='No hat is printed on the marked algebra. The original tensor also has an uncompleted O_X_0,x; its substantive defect is retained for the notes and the separate erratum.')
 old=r'''un isomorphisme canonique
\[
  G_{\mathfrak X}=\varprojlim_nG_{X_n} ;
\]
en d'autres termes, pour tout ouvert $V$ de $\mathfrak X$, on a
\[
  G(V)=\varprojlim_nG(V_n).
\]'''
 new=r'''un isomorphisme canonique $G_{\mathfrak X}=\varprojlim G_{\mathfrak X_n}$, en d'autres termes, pour tout ouvert $V$ de $\mathfrak X$, on a $G(V)=\varprojlim G(V_n)$.'''
 r(old,new,'part c inverse-limit formulas',kind='structure',why='Both formulas are inline, the first followed by a comma. Neither limit has a printed n subscript. The first subscript X_n is handwritten Gothic in this local occurrence; the ordinary V_n remains typed.')
 r('propre $X$ sur',r'\uline{propre} $X$ sur','properness emphasis',why='propre is underlined.')
 r('du schéma ordinaire $X$',r'du schéma \uline{ordinaire} $X$','ordinary-scheme emphasis',why='The second occurrence of ordinaire is underlined.')
 r(r'$\mathcal J=\mathfrak m\mathcal O_X$',r'$\mathcal J=\mathfrak m.\mathcal O_X$','part d ideal product punctuation',why='A dot is printed between the maximal ideal and the structural sheaf in this occurrence.')
 if tree=='fr_printed':
  r('revêtements plats du schéma','revêtement plats du schéma','part d number of revêtement',why='The scan prints revêtement without a final s, followed by the plural plats.')
 else:
  # Log the correction explicitly from the restored print reading.
  r('revêtements plats du schéma','revêtement plats du schéma','part d number of revêtement: print restoration',why='Restore the exact printed singular before recording the grammatical correction.')
  r('revêtement plats du schéma','revêtements plats du schéma','part d number of revêtement',kind='misprint of the original',why='The phrase classes de revêtement plats requires the noun to agree with the printed plural adjective plats and the plural classes of covers.')
 for a,b in [('« se réduisent suivant $X\'_0$ »',r"\fquote{se réduisent suivant $X'_0$}"),('« fini »',r'\fquote{fini}'),('« infinitésimal »',r'\fquote{infinitésimal}'),('« formel »',r'\fquote{formel}'),('« algébrique »',r'\fquote{algébrique}')]:
  r(a,b,'quotation '+a,why='Ordinary double quotation marks.')
 r(r'F(A)=G(\mathfrak X\times_\Lambda A),',r'F(A)=G(\mathfrak X\times_\Lambda A).','definition of F punctuation',why='The displayed formula ends with a period.')
 r("où le marquage est pris après changement de base à l'algèbre réduite $A_{\\mathrm{red}}$, et non littéralement à $A/\\mathfrak mA$. C'est", "\nC'est",'unprinted clarification of the marking',kind='structure',why='The scan proceeds directly to a new paragraph beginning C’est. The sentence specifying A_red is an editorial addition and must not enter either exposé layer.')
 r('i.e. de la forme','i. e. de la forme','pro-representability abbreviation',why='Spaced i. e.')
 r(r'\operatorname{Hom}_{\Lambda\text{-algèbres top.}}(O,A),',r'\operatorname{Hom}_{\Lambda\text{-algèbres top.}}(\mathcal O,A)','last display letter and punctuation',why='The final ring letter is a handwritten cursive O, without an underline; no punctuation ends the formula. This local cursive shape is retained, provisionally for the second reading.')
 # Wavy underlines distinguish the sheaf G from the plain set-valued G.
 for a,b in [(r'G_{\mathfrak X}',r'\text{\uwave{G}}_{\mathfrak X}'),(r'=G$.',r'=\text{\uwave{G}}$.'),(r'G_x=',r'\text{\uwave{G}}_x='),(r'G_{\mathfrak X_n}',r'\text{\uwave{G}}_{\mathfrak X_n}')]:
  s,_,_=page_text(rel,388)
  r(a,b,'sheaf G letter '+a,count=s.count(a),why='The sheaf letter G has a short wavy underline; G applied to a scheme or open set does not.')
 s,_,_=page_text(rel,388)
 # The last cursive ring O is deliberately excluded from the structural-sheaf replacement.
 structural=s.count(r'\mathcal O')-1
 for a,b in [(r'\mathcal O}_{',r'\text{\uwave{O}}}_{'),(r'\mathcal O_',r'\text{\uwave{O}}_'),(r"\mathcal O'",r"\text{\uwave{O}}'")]:
  s,_,_=page_text(rel,388)
  if s.count(a): r(a,b,'structural O letter '+a,count=s.count(a),why='The structural sheaf has a wavy O underline; the last representing-ring letter does not.')
 s,_,_=page_text(rel,388)
 r(r'\mathcal J',r'\text{\uwave{J}}','ideal-of-definition letter',count=s.count(r'\mathcal J'),why='Unlike the preceding page, this page prints an upright J with a short wavy underline.')
 upright_page(rel,layer,'195-388')

event('195-C5-a','targeted proof check','Under the actual levelwise density condition of 195-C5-levelwise-density, an isomorphism of marked covers is unique by the preceding Hom injectivity. Local isomorphism classes that agree on overlaps therefore have unique transition isomorphisms, automatically satisfying the cocycle condition. Locally finite free algebras glue with multiplication and unit, proving the sheaf assertion. On U, equivalence of finite etale covers across a nilpotent thickening, and then inverse limit, gives the unique lift of the prescribed closed cover. The etale equivalence is retained as a named background input.','195, p. 388, part a')
event('195-C5-b','refuted, with the refined statement\'s id','Refined statement id: 195-C5-b-local-versus-complete. The printed tensor B tensor over the completed local ring with the uncompleted special-fibre local ring has no specified canonical algebra map in that direction. For example Q[t]_(t) has no canonical Q[t]_(t)-algebra structure over Q[[t]]. Even after completing the marked special fibre, equality of the germ set with all completed deformations is false in general; the explicit rank-two example in 195-C5-b-local-versus-complete verifies failure of surjectivity. This is substantive author-erratum material, not a silent typo correction.','195, p. 388, part b')
event('195-C5-b-local-versus-complete','targeted proof check','Let R0=Q[x,y]_(x,y), R=R0[epsilon]/(epsilon^2), with ideal of definition (epsilon), and prescribed rank-two cover B0=R0[z]/(z^2-x^2), etale on D(x). The function x is a non-zero-divisor on both levels. Over the maximal-adic completion Rhat=Q[[x,y]][epsilon]/(epsilon^2), take Bhat=Rhat[z]/(z^2-x^2-epsilon h(y)), where h(y)=sum over n>=1 of y^(n!), with the duplicate small exponent counted once if necessary. Every marked rank-two deformation over R has basis 1,z by Nakayama; completing the square expresses its relation as z^2=x^2+epsilon f(x,y), f in R0. A marked isomorphism changes z by epsilon(a+bz), so it changes f by a multiple of x^2 (the z coefficient forces a=0 in characteristic zero). Thus algebraization of Bhat would imply h(y) modulo x^2 lies in R0/(x^2), and in particular h(y) is a rational germ in y. Its arbitrarily long zero gaps followed by nonzero coefficients preclude the eventual fixed linear recurrence of a rational series. Hence it is not a germ. This checks non-surjectivity for the meaningful comparison with a completed marked fibre; it does not repair the ill-typed printed tensor by inference.','195, p. 388, part b, explicit comparison example')
event('195-C5-c','targeted proof check','Under uniqueness of marked isomorphisms, compatible isomorphism classes on successive X_n have unique compatible transition identifications. The inverse limit of the corresponding locally finite free algebras gives a formal finite locally free algebra, with multiplication and unit obtained by inverse limit. Conversely reduction recovers every level. Locally the rank is fixed by the closed fibre and a lifted basis gives the complete free module. This checks the asserted limit of class sets and sheaves under the density/rigidity assumptions; completeness and coherent formal-module equivalence are the named structural inputs.','195, p. 388, part c')
event('195-C5-d','carried as background without fault found','The asserted algebraization uses proper formal existence for coherent sheaves over a complete noetherian local base. Its fully faithful tensor-compatible form algebraizes multiplication, unit and their equations. Local freeness follows near the closed fibre and then everywhere: the non-free locus is closed and its proper image cannot be a nonempty closed subset of a local base missing its closed point. The proper formal-existence theorem is not independently proved in this run; this event records the required input rather than claiming a new proof.','195, p. 388, part d')
event('195-C5-functor-marking','used and rechecked in this run','Removed the unprinted sentence that specifies marking over A_red. The preceding definition only says that G(Y) is defined similarly for Y over the formal base; the choice of its closed subspace matters. If it is taken to be the pullback by mA, then for Lambda a field m=0 the marking fixes the cover on all Y, leaving a singleton. If instead the marking is over A_red, nilpotent deformations remain: for A=Q[epsilon]/epsilon^2 the two marked covers z^2=x^2 and z^2=x^2+epsilon over A[x] are not isomorphic, since a marked change z to z+epsilon(a+bz) changes the constant term only by a multiple of x^2. Thus the removed clarification is mathematically consequential. Its correct historical placement must be checked in the separate erratum; no interpretation is silently inserted into the exposé.','195, p. 388, definition of F and removed editorial clarification')
event('195-C5-finite-algebras-continuity','targeted proof check','Conditional on a coherent definition of the marking and the inverse-limit assertion (c), a finite algebra A over the complete noetherian local Lambda is complete for mA and equals the inverse limit of its Artinian quotients A/m^(n+1)A. Thus the functor is determined by its values there. Compatible continuous maps from a pro-Artinian representing algebra to those quotients give a unique continuous map into A, which checks the displayed extension of a pro-representing description. This does not settle the separate marking ambiguity.','195, p. 388, last paragraph and display')
record_page('195',388,r'''Compared sources/fr_printed/fr/195.tex entry lines 935–1003 and sources/fr/fr/195.tex entry lines 936–1004 with scan leaf 21 at 400 dpi, full page and all three enlarged bands. Read the hats and absent hats in part b, both inverse-limit arrows, all sheaf underlines, the handwritten Gothic X_n, the two different ideal products, and the last cursive ring letter.

Both layers restore the original inline equality with the completed local ring, remove the inserted intermediate inclusion and erratum footnote, and remove the unprinted A_red clarification. They retain the original uncompleted marked algebra and tensor factor, recording the mathematical defect separately. Both inverse-limit formulas are inline and have no printed n under the limit. Restored punctuation, ordinary quotation marks, selective emphasis, wavy G/O/J, the local Gothic X_n, the locally cursive representing O, and upright typed letters. The only new difference between French layers is the grammatical revêtement plats to revêtements plats in part d.

Checked sheaf gluing and inverse limits conditional on the preceding density/rigidity input. A rank-two marked cover with a nonrational formal coefficient gives an explicit obstruction to the completed-stalk equality, even after making its marking well-typed. Proper algebraization remains a named background theorem. Recorded why the removed A_red sentence is substantive and checked the finite-algebra continuity argument only under a coherent marking convention.''')
from update_record_counts import update
update()
