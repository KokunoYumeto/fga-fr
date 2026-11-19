from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1,full=False):
  replace(rel,a,b,layer,'182-207',line,statement,'400-dpi scan, full page and all three enlarged bands. '+why,kind,count=count,full=full)
 r('\\src{208}\n','','page boundary','7','structure','The printed page ends after des schémas de modules, earlier than this marker.',full=True)
 r('des schémas de modules véritables','des schémas de modules\n\\src{208}\nvéritables','last line','7','structure','Move marker 208 to the actual continuation before véritables.',full=True)
 txt,_,_=page_text(rel,207)
 additions=list(re.finditer(r'\\emph\{Complément de 1962\.\}.*?\n\n',txt,re.S))
 if len(additions)!=2:raise ValueError('Expected two unprinted inserted complements on page 207')
 for i,m in enumerate(additions,1):
  r(m.group(0),'','after Remark '+str(1 if i==1 else 3),'6-rem'+str(1 if i==1 else 3),'structure','This supplied 1962 complement is absent from the printed exposé page. Remove the merged insertion from both layers; the separate errata text remains for its scheduled check.')
 txt,_,_=page_text(rel,207)
 r(r'\Theta',r'\mathfrak G','two derivation sheaves','6-rem1,6-rem3',why='The two handwritten derivation symbols repeat the Gothic G of pages 204–206.',count=txt.count(r'\Theta'))
 r(r'\mathbf P',r'\mathfrak P','three projective-space symbols','6-rem3',why='The projective-space letter is handwritten Gothic, not bold roman; the pen forms vary.',count=txt.count(r'\mathbf P'))
 r(r'\kappa',r'\varkappa','residue field in Remark 3','6-rem3',why='The handwritten crossed kappa is the same variant as on pages 194 and 201.')
 r('Kodaira--Spencer','Kodaira-Spencer','two names in Remark 3','6-rem3',why='The printed names are joined by one short hyphen.',count=2)
 r("$A'$-isomorphes ($X,X'$", "$A'$-isomorphes, ($X,X'$",'isomorphism parenthesis','6-rem3',why='The scan has a comma before the parenthesis.')
 for old,new in [('« théorème fondamental »',r'\fquote{théorème fondamental}'),('« variations de\nstructure »',r'\fquote{variations de structure}'),('« formel »',r'\fquote{formel}')]:
  r(old,new,'quoted expressions','6,7',why='The original uses ordinary double quotation marks.')
 r('les idées) complet.','les idées) \\uline{complet}.','Remark 2 emphasis','6-rem2',why='The word complet is underlined.')
 r(r'\fsection{7}{Application à la « Théorie des modules »}',r'\fsection{\normalfont7}{\normalfont\uline{Application à la \fquote{Théorie des modules}}.}','section 7 heading','7',why='The number and heading are roman; the title is underlined, with double quotes and a final period outside the underline.')
 r('sur un corps $k$, i.e. nous travaillons en égale caractéristique,','sur un \\uline{corps} $k$, i.e. nous travaillons en \\uline{égale caractéristique},','section 7 opening emphasis','7',why='The print underlines corps and égale caractéristique.')
 upright_page(rel,layer,'182-207')
event('182-6-rem2','carried as background without fault found','Read the dependence of Theorem 3 on completeness and the stated desire for a fourth fundamental theorem. The passage is a historical open problem, not an asserted theorem; no modern result was substituted.','182, p. 207, Remark 2')
event('182-6-rem3','carried as background without fault found','Read the proposed finite unramified descent of isomorphisms, the asserted geometric-fiber rigidity under H^1(G)=0, and the degeneration questions. These are distinguished as conjecture, assertion without proof, and questions respectively. No independent proof of the unproved geometric-fiber assertion was supplied. Removed the absent 1962 insertion from the exposé in both French layers.','182, p. 207, Remark 3')
event('182-6-rem3-projective-question','targeted proof check','The question as literally stated assumes only properness and flatness. The family xy=t z^2 in projective 2-space over k[[t]] has a smooth generic conic with rational point, hence generic fiber P^1, but special fiber the union of two lines. It is flat because t is a nonzerodivisor in its homogeneous coordinate ring. Thus the literal question has a negative example unless further smoothness hypotheses are intended. The text is a question and is retained; any later erratum is to be assessed separately, not merged.','182, p. 207, Remark 3, projective-space degeneration question')
event('182-7-introduction','carried as background without fault found','Read the equal-characteristic restriction and the author\u2019s stated intention to construct moduli schemes. This opening continues on page 208; no historical completion has been merged into the exposé.','182, p. 207, section 7 opening')
record_page('182',207,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 685–748 with scan leaf 16 at 400 dpi, full page and enlarged top, middle and bottom bands. Read the end of Remark 1, Remarks 2–3 and section 7 through des schémas de modules. Moved marker 208 before véritables.

Removed two supplied paragraphs headed Complément de 1962: neither appears on this printed exposé page. They must remain in the separate supplementary text, to be read later, and this removal must be propagated through the translations. Restored Gothic G/P, crossed kappa, the short Kodaira-Spencer hyphens, the comma before the isomorphism parenthesis, double quotation marks, and the printed emphasis and section heading. Read the unproved rigidity assertion as background and retained the historical conjectures and questions. Recorded the flat conic degeneration xy=t z^2 as a countercheck to an affirmative answer under the literal proper-flat hypotheses of the projective-space question; no question wording was changed.''')
p='CHECK_RECORD.md';t=read(p)
t=t.replace('and Corollary 2 on 202 |','Corollary 2 on 202, and all Hom sheaves on 203 |')
t=t.replace('| Ext sheaf |', '| Automorphism sheaf | `\\mathop{\\text{\\uwave{Aut}}}\\nolimits` | Wavy-underlined Aut in 182-203 and 205 |\n| Derivation sheaf | `\\mathfrak G` | Handwritten Gothic G in 182-204 onward; supplied Greek theta replaced after enlarged glyph comparison |\n| Projective space | `\\mathfrak P` or plain `P` | Handwritten Gothic P in 182-206–207; pen forms vary and case is provisional; plain typed P on 199 |\n| Ext sheaf |')
t=t.replace('Crossed handwritten kappa in 182-194 and 201','Crossed handwritten kappa in 182-194, 201 and 207')
t=t.replace('## Open reading questions', '''- 182-203, projective-bundle automorphism sequence: retained O_Y rather than printed O_X; the bundle is on Y.
- 182-204, deformation setup: retained A rather than printed X as the base of the lifted scheme; restored the Gothic derivation symbol G in both layers.
- 182-205, filtration: corrected the quotient index to X_{n-1} and removed degree zero from the associated graded, with explicit affine-line counterchecks.
- 182-205, Corollaries 1–2: retained X rather than printed Y and X_n rather than unindexed X in the respective lift equations.
- 182-206, Theorem 9: retained the formal Gothic X in its reduction equation; printed French restores ordinary X.
- 182-207, Remarks 1 and 3: removed two merged 1962 complements from both layers; no modern replacement is inserted into the historical statements.

## Open reading questions''')
write(p,t)
from update_record_counts import update
update()
