from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='B.3',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-320',line,statement,'400-dpi full image and three enlarged bands. '+why,kind,count=count)
 seg,_,_=page_text(rel,320)
 for a,b,body in footnotes(seg):
  if body.startswith('Le texte imprimé porte'):
   r(seg[a:b],'','after (3.4)','(3.4)',kind='structure',why='The supplied explanatory footnote is absent from the printed page; its justification is retained in the correction record.')
 old="\\[\n  T_i:\\mathcal U\\longrightarrow\n  \\operatorname{Hom}_{\\mathcal O_S}(F'_i,F'_i)\n  \\qquad (i=1,2,3),\n\\]"
 new="$T_i$ $(i=1,2,3)$ $\\mathcal U\\longrightarrow\\operatorname{Hom}_{\\mathcal O_S}(F'_i,F'_i)$,"
 r(old,new,'opening homomorphisms',kind='structure',why='The maps are inline; the index range precedes the arrow expression and no colon follows T_i.')
 r("compatibles avec l'accouplement donné","\\uline{compatibles avec l'accouplement donné}",'first compatibility clause',why='Underlined phrase.')
 r('la condition suivante est vérifiée.','la condition suivante est vérifiée :','end of first paragraph',why='Printed colon.')
 r("\\[\n  \\Delta\\xi=\\sum_i\\xi'_i\\otimes_{\\mathcal A'}\\xi''_i\n\\]","$\\Delta\\xi=\\sum\\xi'_i\\otimes_{\\mathcal A'}\\xi''_i$",'diagonal definition',kind='structure',why='Inline formula; the summation sign has no printed index at this occurrence.')
 r("compatibles avec\nl'application diagonale","\\uline{compatibles avec l'application diagonale}",'parenthetical explanation',why='Underlined phrase.')
 r("l'accouplement donné.)","l'accouplement donné).",'parenthesis end',why='The period follows the closing parenthesis.')
 r("représentations d'algèbres à applications diagonales les données","représentations d'algèbres à applications diagonales, les données",'interpretation sentence',why='Printed comma after diagonales.')
 r("un faisceau quasi-cohérent d'algèbres sur","un faisceau quasi-cohérent d'\\uline{algèbres} sur",'algebra consequence',why='Algèbres is underlined.')
 r("d'un pré-schéma $X'$ sur $S$","d'un pré-schéma $X'$ \\uline{sur} $S$",'general-scheme paragraph',why='Sur is underlined.')
 r("\\mathcal A'\\longrightarrow\\mathcal O_{X'},","\\mathcal A'\\longrightarrow\\mathcal O_{X'}",'structure-algebra display',why='No terminal comma.')
 r("$h:X'\\longrightarrow S'$)\n\\[","$h:X'\\longrightarrow S'$) :\n\\[",'before last display',why='The printed parenthesis is followed by a colon.')
 r("(\\mathcal O_{X'},\\mathcal O_{X'}),","(\\mathcal O_{X'},\\mathcal O_{X'})",'last display end',why='No terminal comma.')
 r(r'\textsc{Exemple 1 (« Weil »).} --',r'\result{EXEMPLE}{1 (\fquote{WEIL})}','example heading','B.3 example 1',why='Roman capitals, double quotes and a single short dash.')
 r('un revêtement étale\ngaloisien','un \\uline{revêtement étale galoisien}','example hypothesis','B.3 example 1',why='Underlined phrase.')
 r('paragraphes 3 et 4.d','paragraphes 3, et 4,(d)','example reference','B.3 example 1',why='Printed comma and parenthesized letter.')
 if tree=='fr_printed':
  r("de $F'_1,F'_2$ respectivement sur un ouvert","de $\\mathcal A'$ sur un ouvert",'domains below (3.4)','(3.4)',why='The print says A-prime; the corrected module domains remain in corrected French.')
  r('gauche) définie par','gauche) défini par','diagonal definition',why='Printed masculine défini.')
 else:
  r("$h:X'\\longrightarrow S'$","$h:X'\\longrightarrow S$",'base map in last paragraph',kind='misprint of the original',why='The displayed coefficient sheaf is h-inverse(O_S), and U is on S; h must therefore denote the structure map to S. The printed target S-prime gives a mismatched sheaf base.')
 for old,new,label in [(r'\mathcal U',r'\text{\uwave{U}}','endomorphism algebra U'),(r'\mathcal O',r'\text{\uwave{O}}','structure ring O'),(r'\mathcal A',r'\text{\uwave{A}}','algebra A'),(r'\operatorname{Hom}',r'\mathop{\text{\uwave{Hom}}}\nolimits','internal Hom')]:
  s,_,_=page_text(rel,320)
  r(old,new,'all '+label+' identifiers',why='The scanned identifiers are ordinary letters with wavy underlines.',count=s.count(old))
 if tree=='fr_printed':
  r("\\sum\\xi'_i\\otimes_{\\text{\\uwave{A}}'}\\xi''_i","\\sum\\xi'_i\\otimes_{A'}\\xi''_i",'first tensor base','diagonal definition',why='The wavy underline is omitted from A-prime in this inline tensor subscript.')
 upright_page(rel,layer,'190-320')
with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 for line,statement,old,new,why in [
  ('domains below (3.4)','(3.4)',"de $\\text{\\uwave{A}}'$ sur un ouvert","de $F'_1,F'_2$ respectivement sur un ouvert",'The variables are inputs to the pairing F1-prime times F2-prime to F3-prime and to the indicated T operators. They are not generally sections of the coefficient algebra.'),
  ('diagonal definition','B.3','gauche) défini par','gauche) définie par','The participle qualifies la section and requires feminine agreement.'),
  ('first tensor base','B.3',"\\otimes_{A'}","\\otimes_{\\text{\\uwave{A}}'}",'The tensor product is over the same wavy-underlined algebra A-prime explicitly specified in the following sentence.')]:
  w.writerow(['sources/fr/fr/190.tex','French corrected','190-320',line,statement,old,new,'The enlarged scan shows the old reading. '+why,'misprint of the original','low'])
event('190-3.4','targeted proof check','For B finite locally free over A, U=Hom_A(B,B) identifies with B tensor B-dual, and U tensor_B U (using the left B-structures) identifies with Hom_A(B tensor_A B,B). Under this identification Delta(xi) is xi composed with multiplication B tensor B to B, so it exists uniquely and has the printed formula. Compatibility of a pairing N1 times N2 to N3 with the descent coactions is delta3(xy)=delta1(x)delta2(y); evaluating its coefficients by a dual basis gives (3.4), and conversely the identities for every xi recover that coaction equality. Thus x and y belong to N1 and N2, confirming the existing correction of the printed coefficient-algebra domains.','190, p. 320, diagonal formula and (3.4)')
event('190-B3-base-map','targeted proof check','In the last display O_S is a sheaf on S and U is likewise on S. Hence the map used in h-inverse(O_S) must have target S. Correct h:X-prime to S-prime to h:X-prime to S, the structure morphism already named in the previous sentence. This typing repair does not establish the broader arbitrary-scheme operator claim.','190, p. 320, last paragraph before example 1')
event('190-B3-arbitrary-scheme-operators','refuted, with the refined statement\'s id','With internal Hom interpreted as ordinary sheaf endomorphisms on the fixed space X-prime, the displayed operator description cannot encode every scheme descent datum. Let L/K be quadratic Galois with involution sigma and X-prime=Spec(L times L). The semilinear action (a,b) maps to (sigma(b),sigma(a)); it is an effective datum descending to Spec L over K, since L tensor_K L is L times L. It exchanges the two points. Any endomorphism of the sheaf O_X-prime on its fixed space acts componentwise on global sections, because it commutes with restriction to the two singleton opens. It cannot induce that swapping operator T_sigma, although sigma is in End_K(L). Refined statement id: 190-B3-algebra-operators-and-moving-opens. Preserve the historical assertion; its interpretation and required topology are for the notes.','190, p. 320, arbitrary pre-scheme paragraph and last display')
event('190-B3-algebra-operators-and-moving-opens','targeted proof check','The checked operator formulation applies to quasi-coherent algebras over the base S, and therefore to relative affine schemes via their pushed-forward algebras. For a general scheme a descent datum must also specify how opens or points move under the groupoid; ordinary internal endomorphisms of its structure sheaf do not contain that information. In the Galois case the semilinear scheme automorphisms stated in example 1 supply it explicitly. No claim of a full replacement formalism for every arbitrary scheme is made here.','190, p. 320, refinement of the arbitrary-scheme paragraph')
event('190-B3-example1','targeted proof check','For a finite etale Galois torsor S-prime/S, S-prime times_S S-prime is the disjoint union of the graphs of the group elements. A descent isomorphism therefore gives one semilinear automorphism for each element. Restriction of the cocycle to each component of the triple fiber product is exactly the group action law, and restriction to the diagonal is the identity law. The same argument works for quasi-coherent sheaves and schemes and does not require the fixed-space internal-Hom interpretation criticized above. The example continues on 321.','190, p. 320, example 1')
record_page('190',320,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 1098–1159 with scan leaf 23 at 400 dpi, full page and all three enlarged bands. Read the coproduct and both sums, tensor bases, all three operator superscripts in (3.4), both algebra maps, the inverse-image coefficient sheaf and the Galois example.

Removed the unprinted explanatory footnote. Printed French restores A-prime as the erroneous domain below (3.4), masculine défini and the missing wavy underline in the first tensor base; corrected French retains the justified module domains and feminine agreement and supplies the same algebra identifier. Corrected French also repairs the target of h to S so h-inverse(O_S) is well typed. Restored the opening maps and coproduct inline, the unindexed summation sign in the inline formula, selective underlines, wavy mathematical identifiers, printed punctuation, EXEMPLE/WEIL capitals and the exact reference form.

Checked the coproduct through finite duality and the pairing law, confirming the existing mathematical correction below (3.4). A Galois datum exchanging two components shows why ordinary fixed-space structure-sheaf endomorphisms cannot describe all the arbitrary-scheme data claimed in the next paragraph. That broader issue is retained for the notes, separate from the small typing correction. Checked the semilinear group-action description in example 1 directly on the components of the torsor's double and triple fiber products.''')
from update_record_counts import update
update()
