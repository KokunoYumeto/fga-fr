from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-203'
def ch(old,new,where,why,kind='terminology',full=False,count=1):
    replace(rel,old,new,'English',page,where,'section 6 and Proposition 3',
      'French 182-203 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands: '+why,kind=kind,full=full,count=count)
whole=read(rel);start=whole.index('structure” of $X_0$');end=whole.index('\\src{204}',start)+len('\\src{204}')
old=whole[start:end];new='\\src{204}\n'+old[:-len('\\src{204}')]
ch(old,new,'printed page break inside variations of structure','The print ends after variations de and continues the quoted phrase on page 204. Move the existing marker to the corresponding point in English.',kind='structure',full=True)
align_math(rel,'en','182',203,[(i,i) for i in range(40)],(40,40))
ch('\\fsection{6}{Application to existence and uniqueness theorems for sheaves and\nschemes over a complete $\\symup{J}$-adic ring}',
   '\\fsection{\\normalfont6}{\\normalfont\\uline{Application to existence and uniqueness theorems for sheaves and\nschemes over a complete} $\\symup{J}$\\uline{-adic ring}.}',
   'section 6 heading','Restore the underlined roman heading, with J unaccented, and its final period.',kind='structure')
ch('we shall now deduce existence theorems','we now deduce \\uline{existence} theorems','section 6 introduction','Use the source present tense nous déduisons and restore emphasis on existence.')
ch('separated and complete.', 'separated and \\uline{complete}.','base-ring hypothesis','Restore source emphasis on completeness.')
ch('carrying out formal constructions','carrying out \\uline{formal} constructions','general method','Restore source emphasis on formal.')
ch('algebraic geometry over an Artinian ring','\\uline{algebraic geometry over an Artinian ring}','general method','Restore the printed emphasis on this entire phrase.')
ch('$\\symup{H^2\\bigl(X_0,\\mathop{\\text{\\uwave{Hom}}}\\nolimits_{O_{X_0}}(F_0,F_0)\\bigr)=0}$\nThen',
   '$\\symup{H^2\\bigl(X_0,\\mathop{\\text{\\uwave{Hom}}}\\nolimits_{O_{X_0}}(F_0,F_0)\\bigr)=0}$.\nThen',
   'Proposition 3 hypothesis','Restore the external period after the inline vanishing formula.',kind='structure')
ch('$\\symup{H^2\\bigl(X_0,\\mathop{\\text{\\uwave{Hom}}}\\nolimits_{O_{X_0}}(F_0,F_0)\\bigr) \\otimes_{A/J}(J^n/J^{n+1})}$\nwhich',
   '$\\symup{H^2\\bigl(X_0,\\mathop{\\text{\\uwave{Hom}}}\\nolimits_{O_{X_0}}(F_0,F_0)\\bigr) \\otimes_{A/J}(J^n/J^{n+1})}$,\nwhich',
   'Proposition 3 proof','Restore external comma after the inline obstruction group.',kind='structure')
ch('$\\symup{H^1(X_0,\\mathop{\\text{\\uwave{Hom}}}\\nolimits_{O_{X_0}}(F_0,F_0))=0}$.)',
   '$\\symup{H^1(X_0,\\mathop{\\text{\\uwave{Hom}}}\\nolimits_{O_{X_0}}(F_0,F_0))=0}$).',
   'Proposition 3 parenthetical uniqueness','Restore the printed placement of the period outside the parenthesis.',kind='structure')
text,_,_=page_text(rel,203);body=text.split(r'\result{PROPOSITION}{3} ',1)[1].split(' (Moreover,',1)[0]
ch(body,underline_prose(body),'Proposition 3','Restore emphasis on the main assertion, leaving the parenthetical uniqueness statement unaccented.')
text,_,_=page_text(rel,203);body=text.split(r'\result{COROLLARY}{1} ',1)[1].split('\n\n',1)[0]
ch(body,underline_prose(body),'Proposition 3 corollary','Restore the full statement’s printed emphasis.')
ch('nonsingular (by which we mean absolutely nonsingular)', '\\uline{nonsingular} (by which we mean \\uline{absolutely} nonsingular)',
   'deformation setup','Restore emphasis on simple and on absolument only in its parenthetical qualification.')
ch('“theory of moduli,”', '“\\uline{theory of moduli}”','deformation setup','Restore the printed emphasis and remove the comma inserted before the alternative quoted expression.')
record_translation_page('en','182',203,rel,
    'Read the sheaf automorphism sequence, the section-6 method, Proposition 3 and its algebraization corollary, and the opening deformation setup. Approved all 40 formula correspondences after restoring the page break inside the final quotation. The English already uses O_Y and O_Y-units in the opening sequence and explanation, agreeing with the corrected French. Restored wavy Aut and Hom, inline obstruction formulas, source emphasis and the present tense of nous déduisons. The page-extraction helper now obtains complete formula ranges from a strict whole-file parse because the printed break bisects a prose quotation.',(480,551))
event('en-182-Proposition3','targeted proof check',
    'Checked the obstruction sketch for finite-rank locally free sheaves. Lift transition matrices over each square-zero step J^n/J^(n+1); their failure of the cocycle equation gives a class in H^2(End(F_0)) tensor J^n/J^(n+1), using flatness. Vanishing allows adjustment by a 1-cochain and successive compatible lifts. The H^1 group controls differences of lifts; its vanishing gives uniqueness up to isomorphism, not uniqueness of the isomorphism. Compatible local bases give a locally free formal inverse limit.',
    '182, p. 203, Proposition 3 and proof sketch')
event('en-182-Proposition3-Corollary1','targeted proof check',
    'Checked the deduction conditional on Theorem 3: algebraize the compatible formal locally free sheaf and use full faithfulness for isomorphisms. Local freeness holds near the closed fiber by faithful local completion and then on all of X, because a nonempty closed nonfree locus in a proper scheme over a local base would meet the closed fiber.',
    '182, p. 203, Corollary 1 to Proposition 3')
update()
