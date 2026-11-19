from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='4(e)',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-313',line,statement,'400-dpi full scan and enlarged top, middle and bottom bands. '+why,kind,count=count)
 r(r'\operatorname{Gl}\bigl(n,H^0(X,\mathcal O_X)\bigr),',r'\operatorname{Gl}\bigl(n,H^0(X,\mathcal O_X)\bigr)','first display',why='No comma follows the printed display.')
 r('telle que, pour','telle que pour','fiber category description',why='No comma after que.')
 r("on a en effet\n\\[\n  \\operatorname{Gl}(n)(X)=\n  \\operatorname{Aut}_{\\mathcal F_X}(\\mathcal O_X^n).\n\\]", "on a en effet $\\operatorname{Gl}(n)(X)=\\operatorname{Aut}_{\\mathcal F_X}(\\mathcal O_X^n)$.",'automorphism identity',kind='structure',why='The identity is inline, followed by a period.')
 r("D'après (b), il s'ensuit que, si","D'après (b) il s'ensuit que si",'classification reference',why='Neither comma appears in the print.')
 if tree=='fr':
  r("D'après (b)","D'après (c)",'classification reference',kind='misprint of the original',why='The H¹ classification and its effectiveness criterion are established in 4(c), on 312; 4(b) on 311 discusses only H⁰ and full faithfulness.')
 r('paragraphe 2.c','paragraphe 2.(c)','three references to flat descent',why='Printed parentheses around c.',count=3)
 r(r'(cf. paragraphe 2.(c)), $H^1',r'(cf. paragraphe 2.(c)) $H^1','first flat-descent reference',why='No comma after the reference.')
 for label in ['i','ii','iii']:
  r('\\item[('+label+')]',r'\item[\textnormal{('+label+').}]','condition '+label,why='Roman label with period after the closing parenthesis.')
 r("l'homomorphisme d'augmentation\n\\[\n  H^0(S,\\mathcal O_S)=G_a(S)\\longrightarrow H^0(S'/S,G_a)\n\\]\nest un isomorphisme ;","L'homomorphisme d'augmentation $H^0(S,\\mathcal O_S)=G_a(S)\\longrightarrow H^0(S'/S,G_a)$ est un isomorphisme",'condition (i)',kind='structure',why='Capital L, inline formula and no final semicolon.')
 r('conditions équivalent aussi à :','conditions équivalent aussi à','condition (iii) introduction',why='No colon in the print.')
 r("\\bigotimes_A^{n+1}A',","\\bigotimes\\limits_A^{n+1}A'",'additive cochain display',why='The tensor exponent is over the operator and the display has no final comma.')
 r(r'x_i\otimes\cdots\otimes x_n.',r'x_i\otimes\cdots\otimes x_n','coface display',why='No final period.')
 old="De même,\n\\[\n  C^n(S'/S,G_m)=C^n(A'/A,G_m)\n  \\simeq\\left(\\bigotimes_A^{n+1}A'\\right)^*,\n\\]\nles opérations"
 new="De même, $C^n(S'/S,G_m)=C^n(A'/A,G_m)$ s'identifie à $(\\bigotimes\\limits_A^{n+1}A')^*$, les opérations"
 r(old,new,'multiplicative cochain identification',kind='structure',why='The entire identification runs inline with the words s’identifie à; there is no isomorphism symbol.')
 old="\\emph{Dans tous les cas à la connaissance du\nconférencier, on a}\n\\[\n  H^i(A'/A,G_a)=0\\qquad\\text{pour $i>0$},\n\\]\n\\emph{et si $A$ est local, on a}\n\\[\n  H^1(A'/A,G_m)=0\n  \\quad\\text{et plus généralement}\\quad\n  H^1(A'/A,\\operatorname{Gl}(n))=(e)\n\\]"
 plain="Dans tous les cas à la connaissance du conférencier, on a $H^i(A'/A,G_a)=0$ pour $i>0$, et si $A$ est local, on a $H^1(A'/A,G_m)=0$ et plus généralement $H^1(A'/A,\\operatorname{Gl}(n))=(e)$"
 r(old,underline_prose(plain),'vanishing assertions',kind='structure',why='All these formulas run inline; the surrounding prose, including pour and et plus généralement, is underlined, excluding variables.')
 r('i.e.','i. e.','last explanatory abbreviation',why='Spaced abbreviation.')
 old="\\emph{le « théorème 90 » de Hilbert n'est\nautre que la relation}"
 new="\\uline{le} \\fquote{\\uline{théorème} 90} \\uline{de Hilbert n'est autre que la relation}"
 r(old,new,'last line',why='Double quotes; prose underlined except the numeral 90.')
 page,_,_=page_text(rel,313)
 r(r'\mathcal C',r'\text{\uwave{C}}','four category letters',why='Ordinary wavy-underlined C.',count=page.count(r'\mathcal C'))
 r(r'\mathcal O',r'\text{\uwave{O}}','five structure-sheaf letters',why='Ordinary wavy-underlined O.',count=5)
 upright_page(rel,layer,'190-313')
event('190-4e-vector-bundle-forms','targeted proof check','An automorphism of O_X^n is an invertible matrix of global functions, identifying the functor with Aut of the fixed free object. The H¹ classification is therefore the application of 4(c), not merely 4(b), so the reference is corrected. On Spec of a local ring every locally free sheaf is free: a trivializing neighborhood of the closed point is the entire spectrum. Thus effectiveness for the fixed free pullback is equivalent to H¹ being a singleton under the preceding descent assumption. This is a criterion, not an assertion that arbitrary descent data are effective.','190, p. 313, first paragraph')
event('190-4e-global-functions-equivalence','refuted, with the refined statement\'s id','As stated for arbitrary S, (i) does not imply (ii) or, for finite maps, (iii). Counterexample: S=P¹_k and S-prime a k-rational point. Global functions and the equalizer in (i) are k, but pullback Hom(O,O(1))=k²→k has nonzero kernel, so full faithfulness fails. The point immersion is finite and is not an epimorphism, since two distinct morphisms P¹→P¹ can agree at that point. Refined statement 190-4e-affine-equivalence: for affine S and affine S-prime the equalizer criterion implies the Hom criterion for finite locally free modules by tensoring and taking direct summands; for a finite morphism it also matches the strict-epimorphism equalizer criterion of 2(b). The original general wording is preserved; this is a substantive scope gap for the notes.','190, p. 313, conditions (i)–(iii)')
event('190-4e-amitsur-formulas','targeted proof check','For affine S=Spec A and S-prime=Spec A-prime, the n-fold nerve term has n+1 tensor factors. Pulling back along deletion of coordinate i inserts the unit in position i, giving the displayed coface formula. Inserting two units in opposite orders gives the cosimplicial identity and cancellation in d². Passing to units and invertible matrices preserves the ring cofaces and yields the stated multiplicative and general-linear constructions. The generic historical phrase opérations simpliciales is retained.','190, p. 313, tensor and coface formulas')
event('190-4e-vanishing-known-cases','carried as background without fault found','The author explicitly limits the assertion to cases known to the speaker; it is retained with that qualifier. In the faithfully flat case, additive acyclicity follows by tensoring with A-prime, using the split Čech contraction and detecting exactness by faithful flatness. The nonabelian vanishing over a local base additionally uses effective descent of finite locally free modules. That general theorem is not independently proved on this page. Hilbert 90 continues on 314.','190, p. 313, final paragraph')
record_page('190',313,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 738–817 with scan leaf 16 at 400 dpi, full page and all three enlarged bands. Checked each tensor factor count, insertion position, exponent, prime, augmentation arrow and cross-reference.

Restored the automorphism identity and condition (i) inline, the multiplicative cochain identification as inline prose s'identifie à, and all vanishing formulas inline. Restored Roman labels with final periods, capital L, printed punctuation and absence of display punctuation, parenthesized section letters, detailed underlining, double quotes, spaced i. e. and wavy C/O. Newly corrected the H¹ classification reference (b) to (c) only in corrected French. The two uses of the generic phrase opérations simpliciales are retained.

Checked the matrix/automorphism identification, local-spectrum triviality, effectiveness criterion and tensor/coface formulas. Found the missing affine scope in conditions (i)–(iii), with the rational-point immersion into P¹ as a counterexample; recorded the affine refinement for the notes while preserving the historical statement. The final vanishing assertion is explicitly limited to the author's known cases and has not been promoted to an unrestricted theorem.''')
from update_record_counts import update
update()
