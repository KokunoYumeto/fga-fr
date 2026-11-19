from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/195.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'195-385',line,'C.3–4','400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 r('« schémas de modules »',r'\fquote{schémas de modules}','opening quotation',why='Ordinary double quotation marks.')
 r("par l'introduction, si besoin est, de structures auxiliaires","par l'introduction si besoin est de structures auxiliaires",'opening rule punctuation',why='Neither comma around si besoin est occurs in the scan.')
 span="numéro et des suivants, et chaque fois qu'on cherche des \\fquote{schémas de modules}\npour des classes d'objets qui ne sont définis qu'à un isomorphisme près, reste\ntoujours la suivante"
 r(span,r'\uline{'+span+'}','opening rule first emphasis span',why='Underline continues from page 384 through suivante.')
 span="éventuels des objets qu'on\nveut classifier, par l'introduction si besoin est de structures auxiliaires"
 r(span,r'\uline{'+span+'}','opening rule second emphasis span',why='The scan leaves éliminer les automorphismes without an underline, then underlines éventuels through auxiliaires.')
 r(r"\subsection*{4. Modules formels d'une variété}",r"\subsection*{\textnormal{4. \uline{Modules formels d'une variété}.}}",'section heading',kind='typesetting',why='Roman heading, words underlined, final period.')
 r('un anneau local noethérien','un anneau \\uline{local} noethérien','coefficient ring emphasis',why='Only local is underlined.')
 r('de Cohen), $X_0$','de Cohen) $X_0$','coefficient ring parenthesis punctuation',why='No comma after the closing parenthesis.')
 r('des classes, à un isomorphisme près, de','des classes à un isomorphisme près de','deformation classes punctuation',why='No commas surround à un isomorphisme près.')
 r('$X$ plats sur $A$','$X$ \\uline{plats} sur $A$','deformation flatness emphasis',why='Only plats is underlined.')
 old=r'''\[
  (*)\qquad
  X\otimes_A\kappa(A)\xleftarrow{\sim}
  X_0\otimes_k\kappa(A),
\]'''
 new=r'''\begin{equation}\tag{*}
  X\otimes_A\varkappa(A)\xleftarrow{\sim}
  X_0\otimes_k\varkappa(A)
\end{equation}'''
 r(old,new,'marked special-fibre isomorphism',kind='structure',why='The star label is at the left margin; the isomorphism points left; the handwritten residue symbol is varkappa, and there is no terminal comma.')
 r(r'\kappa(A)',r'\varkappa(A)','residue field in explanation',why='Same handwritten varkappa as in the display.')
 r('le foncteur des modules pour',r'le \uline{foncteur des modules} pour','functor definition emphasis',why='These three words are underlined.')
 r('appelé schéma formel des modules pour',r'appelé \uline{schéma formel des modules} pour','formal moduli definition emphasis',why='These five words are underlined.')
 r('« finis »',r'\fquote{finis}','finite automorphisms quotation',why='Ordinary double quotation marks.')
 s,_,_=page_text(rel,385)
 r(r'\Theta',r'\mathfrak G','derivation sheaf letter',count=s.count(r'\Theta'),why='The handwritten letter is the same Gothic G used for the derivation sheaf earlier in exposé 182, not a typed Greek theta. All three occurrences are checked here.')
 r(r'H^0(X_0,\mathfrak G_{X_0/k})=0,',r'H^0(X_0,\mathfrak G_{X_0/k})=0','automorphism criterion display',why='No terminal comma.')
 r('tangent) de $X_0$. On trouve', 'tangent) de $X_0$.\nOn trouve','line break before tangent discussion',kind='structure',why='The printed discussion starts a new line, without an indented paragraph.')
 r('simple sur $k$)\n','simple sur $k$),\n','smooth-case parenthesis punctuation',why='A comma follows the closing parenthesis.')
 r(r'F(I_A,\xi)=H^1(X_A,\mathfrak G_{X_A/A}).',r'F(I_A,\xi)=H^1(X_A,\mathfrak G_{X_A/A})','deformation tangent display',why='No terminal period; degree 1 and the nested A subscript are printed and retained.')
 upright_page(rel,layer,'195-385')

event('195-C3-golden-rule','carried as background without fault found','The auxiliary-structure rule is a methodological proposal: choose markings that remove automorphisms while controlling how they alter the classification problem. It is not read as a theorem that every moduli functor becomes a scheme after an arbitrary marking. The proof burden is to verify vanishing of the marked automorphism group and effective descent for the particular added structure.','195, p. 385, opening continuation of C.3')
event('195-C4-deformation-functor','targeted proof check','An Artinian local algebra A carries a deformation together with an identified special fibre X_0 over its residue field. Pullback along a local algebra map transports that identification by the induced residue-field map. A general finite-length algebra is a finite product of its local factors; spectra are disjoint unions, which proves the stated product rule. Over a field extension K of k there is exactly one isomorphism class with the specified marking, so a pro-representing topological algebra, if it exists in the previously defined category, has one local component and residue field k. The printed word représentable is retained in its surrounding topological/pro-representable usage.','195, p. 385, section 4 definition')
event('195-C4-infinitesimal-automorphisms','targeted proof check','For a local Artinian A with nonzero maximal ideal m, let X be a flat deformation with its special-fibre identification. Automorphisms in this category reduce to the identity. Filtering by powers of m, the difference from identity at the first nonzero level is a derivation of X_0 over the residue field with values in O_X_0 tensor (m^r/m^{r+1}). If H^0 of the tangent sheaf vanishes, induction forces the automorphism to be identity. Conversely choose a nonzero socle element a in m and a nonzero global derivation delta of the special fibre. Flatness identifies a O_X with O_X_0 tensor (a); the composite O_X to O_X_0 followed by a delta is a square-zero derivation D. Then 1+D is a nontrivial automorphism with inverse 1-D. Finite residue-field extension preserves the existence/vanishing of these derivations. This proves the criterion for local nonfield A. A product of fields is not a field but has no infinitesimal ideal; the wording is therefore read within the local discussion, not as a criterion for every nonlocal nonfield A.','195, p. 385, vanishing H^0 criterion')
event('195-C4-tangent-H1','targeted proof check','For a smooth deformation X_A, a deformation over A[epsilon]/epsilon^2 with identified reduction is locally trivial on affine opens by formal smoothness. Two local trivializations differ by 1+epsilon delta with delta a relative derivation; their transition maps satisfy the additive one-cocycle relation. Changing trivializations adds a coboundary, giving H^1(X_A,G_X_A/A). At A=k the special-fibre marking already fixes the reduction; for general A the preceding no-automorphism condition identifies this framed calculation with the stated fibre of isomorphism classes. Without that condition one must account for the action of automorphisms of the reduction. Smoothness is essential for this elementary local-triviality calculation.','195, p. 385, final tangent display')
record_page('195',385,r'''Compared sources/fr_printed/fr/195.tex entry lines 786–833 and sources/fr/fr/195.tex entry lines 787–834 with scan leaf 18 at 400 dpi, full page and all three enlarged bands. Read the deliberate gap in the opening underlining, the left-pointing marked special-fibre isomorphism, all A/k/0 subscripts, the handwritten residue symbol and three Gothic derivation letters.

Both layers restore the literal punctuation and ordinary quotation marks, selective emphasis, roman underlined heading, left-margin star label, varkappa, Gothic G and upright variables. The two cohomology displays are unpunctuated; H^0 controls infinitesimal automorphisms and H^1 controls smooth first-order deformations. No mathematical difference is introduced between the two French layers on this page.

Checked functorial pullback, finite-product behaviour and the implication for the residue field of a representing local algebra. Proved the no-infinitesimal-automorphism criterion using the maximal-ideal filtration and a socle derivation for the converse, explicitly limiting the nonfield assertion to local Artinian algebras. Derived the smooth deformation tangent description by local trivializations and derivation cocycles, distinguishing a fixed reduction from unframed isomorphism classes when automorphisms remain. The opening rigidification rule is retained as a method, not a blanket existence theorem.''')
from update_record_counts import update
update()
