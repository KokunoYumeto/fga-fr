from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/195.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'195-382',line,'C.2','400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 r(r'\result{PROPOSITION}{2.1}',r'\result{PROPOSITION}{2, 1}','proposition number',why='Printed comma-numbered proposition.')
 old=r'''\[
  F(I_A,\xi)=H^0\!\left(
    X_A,
    \underline{\operatorname{Hom}}_{\mathcal O_{X_A}}
    \bigl(\xi^*(\Omega^1_{Y_A/A}),\mathcal O_{X_A}\bigr)
  \right),
\]'''
 new=r'''\[
  F(I_A,\xi)=H^0(X_A,\text{\uwave{Hom}}_{\text{\uwave{O}}_{X_A}}(\xi^*(\mathord{\underset{\sim}{\Omega}}^1_{Y_A/A}),\text{\uwave{O}}_{X_A}))
\]'''
 r(old,new,'tangent display typography and punctuation',kind='structure',why='The scan has one line, wavy Hom/O/Omega, ordinary-size parentheses and no terminal comma. The corrected degree and closing parenthesis are retained here before separately restoring the printed defects.')
 r(r'\Omega^1_{Y_A/A}',r'\mathord{\underset{\sim}{\Omega}}^1_{Y_A/A}','differential sheaf in explanation',why='The Omega has a short wavy underline matching its displayed occurrence; retain for recurrent-letter review.')
 r('A.5.1 et','A. 5, 1. et','reference to tangent criterion',why='Printed comma-numbered reference with its final period.')
 r('finitude de [2], le','finitude de [2] le','finiteness reference punctuation',why='No comma follows [2].')
 r('des anneaux noethériens.','des anneaux \\uline{noethériens}.','corollary emphasis',why='Only noethériens is underlined.')
 r('« coordonnées de Chow »',r'\fquote{coordonnées de Chow}','Chow-coordinate quotation',why='Ordinary double quotation marks.')
 r('et en particulier ne se','et en particulier, ne se','remarks punctuation',why='Printed comma after particulier.')
 r('qui sont plats sur $T$','qui sont \\uline{plats} sur $T$','flat subschemes condition',why='Only plats is underlined.')
 r('un faisceau quasi cohérent','un faisceau quasi-cohérent','last paragraph sheaf adjective',why='The printed adjective has a hyphen.')
 s,_,_=page_text(rel,382)
 r(r'\mathcal C',r'\text{\uwave{C}}','category letters',count=s.count(r'\mathcal C'),why='Upright C with a wavy underline.')
 if tree=='fr_printed':
  r('=H^0(X_A,','=H^1(X_A,','tangent cohomology degree',why='The scan unambiguously prints exponent 1.')
  r(r'\text{\uwave{O}}_{X_A}))',r'\text{\uwave{O}}_{X_A})','tangent display missing outer parenthesis',why='Only the inner Hom is closed in print; the outer H parenthesis is missing.')
 upright_page(rel,layer,'195-382')

with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 w.writerow(['sources/fr/fr/195.tex','French corrected','195-382','tangent cohomology degree','C.2 tangent formula','H^1','H^0','The enlarged scan prints 1. A first-order change of a fixed map is a global derivation, hence H^0 of the Hom sheaf. With X=Y=A1 over k and xi the identity, H^1 of that quasi-coherent sheaf is zero but the tangent space k[t] is nonzero. Existing corrected reading confirmed.','misprint of the original','low'])
 w.writerow(['sources/fr/fr/195.tex','French corrected','195-382','tangent display missing outer parenthesis','C.2 tangent formula','...O_X_A)','...O_X_A))','The scan has three opening parentheses (H, Hom, xi-star argument) and only two closings. A second final parenthesis is necessary to close H. Existing corrected reading confirmed.','misprint of the original','low'])
event('195-C2-Prop21','targeted proof check','The Hom functor preserves finite products of Artinian algebras because their spectra are finite disjoint unions. For an exact A to B double-arrow B tensor_A B with A,B finite-length Lambda-algebras, Spec(B) to Spec(A) is finite surjective. After base change to the flat X_A, the equalizer of structure sheaves remains exact by flatness. The finite surjective map is a topological quotient after every base change. A map from X_B to Y agreeing on the two pullbacks therefore gives a continuous underlying map on X_A; the exact sheaf equalizer descends its maps on functions. Locality is checked at a point above each point, using the local maps on stalks and residue fields. Thus the Hom diagram is an equalizer. Applying the announced criterion B.1 gives pro-representability. This is a proof of the application conditional on B.1, whose independent sufficiency proof remains background.','195, p. 382, Proposition 2, 1')
event('195-C2-map-tangent','targeted proof check','The split dual-number extension gives a distinguished zero lift of xi:X_A to Y_A. Any other lift differs on functions by epsilon times an A-derivation from O_Y_A to xi_*O_X_A; the Leibniz identity is exactly the condition that the perturbed map preserve multiplication. These local derivations glue precisely to global sections of Hom_O_X_A(xi-star Omega^1_Y_A/A,O_X_A). Hence the cohomology degree is zero. For X=Y=A1_k and xi=id, the sections form k[t], while H^1 of this quasi-coherent sheaf on the affine line vanishes, independently refuting the printed degree one.','195, p. 382, tangent display and following definition')
event('195-C2-noetherian-corollary','targeted proof check','For a finite residue-field test K, local finite type of Y makes Omega^1_Y_K/K coherent, and its pullback and Hom into O_X_K remain coherent on the noetherian proper X_K. Proper coherent-cohomology finiteness gives finite-dimensional H^0. Together with Proposition 2,1 and the finite-tangent/noetherian criterion A.5,1, this yields the stated noetherian local components. The cohomology finiteness theorem and the general complete-local finite-tangent criterion are named inputs, not newly reproved here. S in the corollary is read with the affine-base convention S=Spec(Lambda) of this discussion.','195, p. 382, corollary')
event('195-C2-cycle-versus-subscheme','targeted proof check','The flat closed-subscheme assignment is a contravariant functor: closed immersions and flatness are preserved by arbitrary base change, and pullback is associative. Cycle data alone need not recover the subscheme: in A2_k the ideals (x^2,y) and (x,y^2) define distinct length-two subschemes with the same fundamental cycle 2[0]. This illustrates loss of embedded infinitesimal directions. It does not assert that every modern scheme-theoretic cycle construction erases all tangent information. The sweeping assessment of classical Chow-coordinate practice is retained as the author\'s historical judgment. The quotient-sheaf generalization continues on page 383.','195, p. 382, remarks and last paragraph')
record_page('195',382,r'''Compared sources/fr_printed/fr/195.tex entry lines 645–692 and sources/fr/fr/195.tex entry lines 646–693 with scan leaf 15 at 400 dpi, full page and all three enlarged bands. Checked the printed H^1, all three pairs of nested parentheses, the star on xi, nested X_A/Y_A/A subscripts, short Omega underlines, proposition/reference numbering and final flatness condition.

Both layers restore comma numbering, literal reference punctuation, selective underlines, ordinary quotes, the quasi-cohérent hyphen, wavy C/Hom/O/Omega and upright variables. The tangent display is restored as one unpunctuated line. Printed French retains H^1 and the absent outer closing parenthesis; corrected French retains H^0 and the necessary second final parenthesis, with explicit justifications. The short wavy Omega form is marked for recurrent-letter review.

Checked Proposition 2,1 by product preservation and descent of maps along the exact finite Artinian relation after flat base change, conditional on the announced B.1 criterion. Derived the tangent formula directly from derivations and checked the affine-line counterexample to H^1. Verified the corollary from coherent H^0 finiteness and the earlier criterion, naming those inputs. Checked the flat-subscheme functor and an explicit example of equal cycles with different infinitesimal subschemes.''')
from update_record_counts import update
update()
