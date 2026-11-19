from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'182-201',line,statement,'400-dpi scan, full page and all three enlarged bands. '+why,kind,count=count)
 txt,_,_=page_text(rel,201)
 r(r'\Osh','O','structure sheaves and local rings','5',why='The O letters are plain.',count=txt.count(r'\Osh'))
 r(r'\mathfrak m_y^nF$ (',r'\mathfrak m_y^nF$, (','opening paragraph, filtration','5',why='A comma follows the filtration term before its parenthesis.')
 txt,_,_=page_text(rel,201)
 r(r'\kappa',r'\varkappa','residue-field notation','5',why='The handwritten crossed kappa agrees with the residue-field sign on page 194.',count=txt.count(r'\kappa'))
 r(r'\widehat{R^qf_*(F)_y}',r'\overline{R^qf_*(F)}_y','formal comparison display','5',why='The completion mark is a straight bar; the y subscript lies outside it.')
 r(r'\varprojlim_n',r'\varprojlim\limits_n','formal comparison display','5',why='The n is beneath the inverse-limit arrow.')
 r('H^q(X_y,F/\\mathfrak m_y^nF).','H^q(X_y,F/\\mathfrak m_y^nF)','formal comparison display','5',why='No terminal period is printed after the display.')
 if tree=='fr_printed':
  r('H^q(X_y,F/\\mathfrak m_y^nF)','H^q(F_y,F/\\mathfrak m_y^nF)','formal comparison, first argument','5',why='The scan unmistakably prints F_y as the cohomology space. Corrected French retains X_y: F_y was defined as a sheaf on that space.')
  r('H^{q-1}(X_y,F/\\mathfrak m_y^nF)','H^{q-1}(X_y,F_y/\\mathfrak m_y^nF_y)','Proposition 1, target quotient','5-prop1',why='Both F letters in this quotient have a y subscript. Corrected French retains F/m_y^n F, the infinitesimal quotients used in the preceding comparison; the printed fiber quotient is independent of n for n at least 1.')
 txt,_,_=page_text(rel,201)
 old=re.search(r'\\\[\s*R\^\{q-1\}.*?\\\]',txt,re.S).group(0)
 expr=old[2:-2].strip().replace('\n  ',' ')
 r(old,'$'+expr+'$','Proposition 1, surjection','5-prop1','structure','The homomorphism is printed within the running statement.')
 r(r'\Homsh_{O_X}(F,G)',r'\mathop{\text{\uwave{Hom}}}\nolimits_{O_X}(F,G)','paragraph before Theorem 7','5-thm7',why='This occurrence of Hom has a wavy underline.')
 r(r'\Homsh_{O_{X_y}}',r'\Homsh_{O_X}','Theorem 7, Hom base','5-thm7',why='The printed subscript is O_X. Its action on the fiber sheaves factors through O_Xy, so the supplied expansion is unnecessary and is reverted in both layers.')
 r('\\[\n  H^1\\bigl(X_y,\\Homsh_{O_X}(F_y,G_y)\\bigr)=0,\n\\]','$H^1\\bigl(X_y,\\Homsh_{O_X}(F_y,G_y)\\bigr)=0$,','Theorem 7, vanishing','5-thm7','structure','The vanishing formula is inline; Hom has the straight underline printed here.')
 r('''homomorphisme
\\[
  u:F|V\\longrightarrow G|V,
  \\qquad V=f^{-1}(U),
\\]
où $U$ est un voisinage de $y$.''',r'''homomorphisme $u:F|V\longrightarrow G|V$, où $V=f^{-1}(U)$ est l'image inverse d'un voisinage $U$ de $y$.''','Theorem 7, final clause','5-thm7','structure','Restore the complete printed wording and the inline morphism and inverse-image equality; the supplied source paraphrased and displayed them.')
 for marker,sid in [(r'\result{PROPOSITION}{1} ','5-prop1'),(r'\result{THÉORÈME}{7} ','5-thm7')]:
  txt,_,_=page_text(rel,201);a=txt.index(marker)+len(marker);b=txt.index('\n\n',a);old=txt[a:b]
  if sid=='5-thm7':
   before,after=old.split(', où ',1);new=underline_prose(before)+', où '+underline_prose(after)
  else:new=underline_prose(old)
  r(old,new,'statement underlining',sid,why='The prose is roman and underlined, excluding the mathematical letters and the word où in Theorem 7.')
 txt,_,_=page_text(rel,201);marker=r'\result{COROLLAIRE}{} ';a=txt.index(marker)+len(marker);b=txt.index('\n\n',a);old=txt[a:b]
 parts=re.split(r'(\(resp\..*?\))',old,flags=re.S)
 new=''.join(x if i%2 else underline_prose(x) for i,x in enumerate(parts)).replace(r'\uline{assez petit}.',r'\uline{assez petit.}')
 r(old,new,'corollary underlining','5-thm7-cor',why='The parenthetical alternatives are not underlined; the final period is within the last underline.')
 upright_page(rel,layer,'182-201')
event('182-5-formal-comparison','used and rechecked in this run','Theorem 2 applied to the flat filtration gives completion of R^q f_*F at y as the limit of H^q(X_y,F/m_y^nF). The printed first argument F_y is a sheaf and is replaced by X_y only in corrected French. The bar placement is transcribed in both layers.','182, p. 201, formal comparison display')
event('182-5-prop1','targeted proof check','Flatness identifies each graded kernel with a direct sum of copies of F_y. Vanishing of H^q(F_y) therefore gives vanishing for all infinitesimal quotients and surjective transition maps on H^(q-1). Formal comparison and faithful completion yield stalk vanishing; coherence gives neighborhood vanishing. The inverse limit surjects onto each finite quotient; since the target is annihilated by m_y^n, surjectivity descends from completion to the actual stalk. The printed F_y/m_y^nF_y is constant for n>=1; the preceding argument requires F/m_y^nF. The corrected target is retained, without claiming the weaker printed assertion itself is false.','182, p. 201, Proposition 1')
event('182-5-thm7','targeted proof check','The Hom sheaf of two locally free sheaves is locally free and is Y-flat when f is flat. Proposition 1 with q=1 and n=1 lifts a fiber homomorphism to the stalk of f_*Hom, hence over a neighborhood. O_X in the printed Hom subscript acts through O_Xy and is restored in both French layers.','182, p. 201, Theorem 7')
event('182-5-thm7-cor','targeted proof check','For a map of vector bundles, isomorphism, surjectivity and fiberwise injectivity hold on open rank loci (locally controlled by minors); a bad locus missing the fiber has closed image under proper f. Shrinking the base thus supplies the stated conclusion.','182, p. 201, corollary to Theorem 7')
record_page('182',201,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 391–448 with scan leaf 10 at 400 dpi, full page and separately viewed enlarged top, middle and bottom bands. Read the flatness discussion, both comparison formulas, Proposition 1, the Hom application, Theorem 7 and its corollary through En particulier.

Restored plain O, the crossed residue-field kappa, the filtration comma, straight completion bar with external y, lower inverse-limit index, display punctuation, inline proposition and theorem formulas, the complete final wording of Theorem 7, and selective roman underlining. The Hom before Theorem 7 is wavy-underlined; the Hom in its hypothesis is straight-underlined and has the printed base O_X in both layers. Printed French restores F_y as the space in formal comparison and both fiber subscripts in Proposition 1's quotient; corrected French retains X_y and the infinitesimal quotient of F, for the reasons in the events. These existing supplied corrections remain provisional until the final crop recheck. The flat-filtration vanishing/surjectivity deduction, Hom lifting and rank-locus corollary were checked as recorded.''')
from update_record_counts import update
update()
