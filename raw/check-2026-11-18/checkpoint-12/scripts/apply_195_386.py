from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/195.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'195-386',line,'C.4','400-dpi full scan and all three enlarged bands, with an additional threefold product-base crop. '+why,kind,count=count)
 r(r'\result{PROPOSITION}{4.1}',r'\result{PROPOSITION}{4, 1}','proposition number',why='Printed comma numbering.')
 r('proposition 4.1','proposition 4, 1','two proposition references',count=2,why='Printed comma numbering.')
 r(r'\Theta',r'\mathfrak G','derivation sheaf letter',why='Same handwritten Gothic G as on page 385.')
 r(r'\result{REMARQUES}{} 1\textsuperscript{o}',r'\result[.]{REMARQUES}{}'+'\n\n'+r'1\textsuperscript{o}','remarks heading and first paragraph',kind='structure',why='REMARQUES has a period and no dash, then the first numbered remark begins a separate paragraph.')
 old=r'''\[
  \operatorname{Ext}^1_{\mathcal O_{P_A}}
  \bigl(P_A;\mathcal I_{X_A},\mathcal O_{X_A}\bigr),
\]'''
 new=r'''\[
  \operatorname{Ext}^1_{\mathcal O_{P_A}}(P_A;\mathcal I_{X_A},\mathcal O_{X_A})
\]'''
 r(old,new,'Ext display',kind='typesetting',why='One-line formula with ordinary-size parentheses and no terminal comma.')
 r(r'X_A\times_\Lambda X_A',r'X_A\times_A X_A','diagonal product base',why='The enlarged subscript is a typed A with a visible crossbar, not Lambda; this is the relative diagonal over A.')
 old="munies d'un isomorphisme d'augmentation\n\\[\n  \\mathcal O\\otimes_{I_A}A\\longrightarrow\\mathcal O_{X_A}\n\\]\n(on rappelle"
 new="munies d'un isomorphisme d'augmentation $\\mathcal O\\otimes_{I_A}A\\longrightarrow\\mathcal O_{X_A}$ (on rappelle"
 r(old,new,'augmentation formula',kind='structure',why='This is an inline formula in the scan, with an ordinary right arrow.')
 r(r'I_A=A[t]/(t^2)',r'I_A=At/(t^2)','dual-number notation',why='The scan prints At without square brackets; retain its polynomial-ring abbreviation in both layers.')
 r("aux faisceaux d'algèbres commutatives.","aux faisceaux d'algèbres \\uline{commutatives}.",'commutative submodule emphasis',why='Only commutatives is underlined.')
 r("qu'en particulier toute courbe\nalgébrique $X_0$ simple et propre sur", "qu'en particulier, toute \\uline{courbe\nalgébrique} $X_0$ \\uline{simple} et \\uline{propre} sur",'curve remark punctuation and emphasis',why='Printed comma after particulier; separate underlined spans courbe algébrique, simple and propre.')
 r(r'\geq2',r'\geqslant2','genus bound',why='The printed greater-than-or-equal sign has a slanted lower stroke.')
 r("s'y ramener, dans","s'y ramener; dans",'curve remark semicolon',why='The enlarged scan has a semicolon after ramener.')
 r('($g=1$), grâce','($g=1$) grâce','elliptic parenthesis punctuation',why='No comma follows this parenthesis.')
 r('On peut, bien entendu,','On peut bien entendu,','last paragraph introduction punctuation',why='No comma follows peut.')
 r('Supposons, par\nexemple,','Supposons par\nexemple,','example introduction punctuation',why='No comma follows Supposons.')
 r('un schéma abélien sur $k$','un \\uline{schéma abélien} sur $k$','abelian scheme emphasis',why='Both words are underlined.')
 r('comme un schéma en groupes sur $k$','comme un schéma en \\uline{groupes} sur $k$','group structure emphasis',why='Only groupes is underlined.')
 r("l'ensemble des classes, à un isomorphisme près, de schémas abéliens sur $A$", "l'ensemble des classes à un isomorphisme près, de schémas \\uline{abéliens} sur $A$",'abelian deformation classes',why='No comma after classes; the comma after près is printed; only abéliens is underlined.')
 r('i.e.','i. e.','two explanatory abbreviations',count=2,why='Spaced i. e. in both printed parentheses.')
 r("et même seulement d'une « section unité »","et même seulement, d'une \\fquote{section unité}",'unit-section parenthesis',why='Printed comma after seulement and ordinary double quotation marks.')
 r('« absolument connexes »',r'\fquote{absolument connexes}','geometric connectedness quotation',why='Ordinary double quotation marks.')
 r('le soit sur\nune fibre','le soit sur\n\\uline{une} fibre','single-fibre emphasis',why='Only une is underlined.')
 s,_,_=page_text(rel,386)
 r(r'\mathcal O',r'\text{\uwave{O}}','structural algebra sheaf letters',count=s.count(r'\mathcal O'),why='All the indicated sheaf O letters have short wavy underlines; the complete topological ring O is plain.')
 s,_,_=page_text(rel,386)
 r(r'\mathcal I',r'\text{\uwave{I}}','diagonal ideal sheaf letters',count=s.count(r'\mathcal I'),why='The scan has upright I with a wavy underline.')
 if tree=='fr_printed':
  r(r'P_A=X_A\times_A X_A',r'P_A=X_A.\times_A X_A','dot before fibre-product sign',why='The additional enlarged crop shows a separate baseline dot after the first X_A. It is retained in the printed layer.')
 upright_page(rel,layer,'195-386')

with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 csv.writer(f,delimiter='\t').writerow(['sources/fr/fr/195.tex','French corrected','195-386','dot before fibre-product sign','C.4 remark 1',r'X_A.\times_A X_A',r'X_A\times_A X_A','The enlarged product-base crop shows a stray baseline dot. The expression defines the fibre product of X_A with itself over A; the dot is neither a factor nor an operator in that construction and interrupts the single expression. Corrected layer omits it.','misprint of the original','low'])
event('195-4.1','carried as background without fault found','The existence conclusion applies the general pro-representability/descent criterion with the automorphism vanishing established on page 385. An independent proof for arbitrary preschemes, including all effectiveness and size issues, is not claimed here. In the proper finite-type case, the singular tangent space is a subspace of an Ext group of coherent sheaves on the proper product, hence is finite-dimensional by coherent Ext finiteness. Together with existence and A.5,1 this explains the noetherian conclusion; the general descent and coherent-finiteness theorems are explicit inputs.','195, p. 386, Proposition 4,1')
event('195-C4-Hochschild-affine','targeted proof check','For an A-projective algebra B, write a first-order flat deformation on B plus epsilon B with multiplication b*c=bc+epsilon h(b,c). Associativity is exactly b h(c,d)-h(bc,d)+h(b,cd)-h(b,c)d=0; changing a splitting by epsilon u changes h by the corresponding Hochschild coboundary. The bar resolution identifies the resulting classes with HH^2(B/A,B), and the exact sequence 0 to I to B tensor_A B to B to 0 identifies this with Ext^1 over B tensor_A B of I into B. Commutativity is the additional linear symmetry h(b,c)=h(c,b), yielding a submodule of classes. The scan uses the product over A, correctly restored from the sources\' Lambda. This establishes the affine calculation under its stated projectivity condition, not the full sheaf-globalization claim.','195, p. 386, remark 1, relative diagonal and Hochschild explanation')
event('195-C4-Hochschild-global','carried as background without fault found','The global Ext classification requires a descent/gluing argument for algebra sheaves and the hypotheses ensuring that the diagonal ideal and direct-image structural sheaf are coherent. The displayed coherent-ideal interpretation applies to separated finite-type X_A, in particular the proper case used for finiteness; it is not an automatic coherent closed-diagonal description for arbitrary nonseparated preschemes. The phrase globalisation facile is retained but is not substituted for a completed proof. The bracketless At notation is preserved as a printed polynomial-ring abbreviation.','195, p. 386, remark 1')
event('195-C4-curve-dimensions','targeted proof check','For a smooth proper geometrically connected curve, the tangent bundle has degree 2-2g. Riemann-Roch gives chi(T)=3-3g. For g at least two, negative degree forces h^0(T)=0, hence h^1(T)=3g-3. For genus zero, T becomes O(2) after a splitting field and h^1=0; for genus one, T becomes trivial and h^1=1. H^2(T)=0 on a curve removes the usual small-extension gluing obstruction, explaining formal smoothness once the deformation/obstruction construction is supplied. For an elliptic curve with origin, a lift of that origin exists by smoothness, and any two choices are related by translation, so passing between unpointed and pointed deformation classes does not add a parameter. The general genus-one form and full mixed-characteristic existence construction are named background, not independently proved here.','195, p. 386, remark 2')
event('195-C4-abelian-rigidification','targeted proof check','On an abelian variety, translation identifies T with O tensor Lie(X_0). Proper geometric connectedness gives H^0(O)=k, so evaluation of a global vector field at the origin is an isomorphism onto Lie(X_0). An infinitesimal automorphism preserving the origin therefore has zero vector field. The Artinian filtration argument of page 385 then removes every marked infinitesimal automorphism. Coherent tangent finiteness explains the noetherian conclusion conditional on effective descent. The ensuing assertion about a global multiplication and its uniqueness continues on page 387 and is not yet treated as proved.','195, p. 386, final paragraph')
record_page('195',386,r'''Compared sources/fr_printed/fr/195.tex entry lines 834–886 and sources/fr/fr/195.tex entry lines 835–887 with scan leaf 19 at 400 dpi, full page, all three enlarged bands, and an extra threefold crop of the product base. The crop resolves a typed subscript A, not Lambda, and a separate dot before the product sign. Checked the Ext degree and all nested indices, the inline augmentation arrow, the bracketless At notation, genus inequality, and emphasis.

Both layers restore comma numbering, the separate REMARQUES. heading, literal punctuation, upright variables, Gothic G, wavy O/I, the product over A, inline augmentation formula, unpunctuated Ext display, slanted inequality and selective prose underlines. Both retain At/(t^2) as printed. The printed layer additionally retains the dot after X_A; the corrected layer omits it with a separate misprint justification. The two ordinary quotation spans and spaced i. e. abbreviations are restored.

Checked the affine Hochschild cocycle/coboundary calculation and the linear commutativity condition, while keeping the sheaf-globalization/coherent-diagonal hypotheses explicit. Derived the curve tangent dimensions from Riemann-Roch and explained the H^2 obstruction input. Verified that an origin kills infinitesimal automorphisms of an abelian variety. The general existence theorem, global Ext classification and the multiplication statement continuing on page 387 are not represented as fully independently proved.''')
from update_record_counts import update
update()
