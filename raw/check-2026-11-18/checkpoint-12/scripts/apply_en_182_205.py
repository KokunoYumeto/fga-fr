from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-205'
def ch(old,new,where,why,kind='terminology',full=False,count=1):
    replace(rel,old,new,'English',page,where,'deformation corollaries and Theorem 9',
      'French 182-205 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands: '+why,kind=kind,full=full,count=count)
whole=read(rel);start=whole.index('of formal schemes $\\mathfrak X$');end=whole.index('\\src{206}',start)+len('\\src{206}')
old=whole[start:end];new='\\src{206}\n'+old[:-len('\\src{206}')]
ch(old,new,'printed page break in Theorem 9','The printed page ends after the parenthetical condition on isomorphisms. Move the existing page marker before the formal schemes being classified.',kind='structure',full=True)
ch('$\\underline{\\operatorname{Aut}}(X_n)$','$\\underline{\\operatorname{Aut}}(X_{n-1})$',
   'quotient of the automorphism filtration','Carry the corrected French index into English. The nth subgroup is the kernel of reduction modulo m^n, hence the quotient concerns X_(n-1), as the last-step description immediately below also shows.',kind='translation')
ch('$\\Theta_{X_0/k}\\otimes_k\\operatorname{gr}(A)$',
   '$\\Theta_{X_0/k}\\otimes_k\\bigoplus_{i>0}\\operatorname{gr}^i(A)$',
   'associated graded automorphism sheaf','Carry the corrected French positive-degree restriction into English. Augmentation-compatible automorphisms induce the identity on the closed fiber, so the filtration starts with degree one and has no degree-zero tangent summand.',kind='translation')
pairs=[(i,i) for i in range(5)]+[(5,3)]+[(i,i-1) for i in range(6,64)]
align_math(rel,'en','182',205,pairs,(64,63))
ch('$\\symup{H^1\\bigl(X_0,\\mathop{\\text{\\uwave{Aut}}}\\nolimits(X)\\bigr)}$\nwhere',
   '$\\symup{H^1\\bigl(X_0,\\mathop{\\text{\\uwave{Aut}}}\\nolimits(X)\\bigr)}$,\nwhere',
   'classification by nonabelian cohomology','Restore the external comma after the inline formula.',kind='structure')
ch('$\\symup{H^1(X_0,\\mathfrak G_{X_0/k})\\otimes_k\\mathfrak m^n}$\n\n',
   '$\\symup{H^1(X_0,\\mathfrak G_{X_0/k})\\otimes_k\\mathfrak m^n}$.\n\n',
   'Corollary 2 final formula','Restore the external period after the inline formula.',kind='structure')
ch('found an $\\symup{X}$','found \\uline{an} $\\symup{X}$','choice of a reference lifting','Restore the emphasis on un.')
ch('compatible with the augmentation.', '\\uline{compatible with the augmentation}.',
   'automorphism sheaf definition','Restore the defining phrase’s printed emphasis.')
ch('following statements.','following statements:','before Corollary 2','Restore the introductory colon.',kind='structure')
ch('to $\\symup{X_n}$.)','to $\\symup{X_n}$).','note after Corollary 2','Restore the period outside the closing parenthesis.',kind='structure')
ch('a complete Noetherian local ring with\nresidue field',
   'a \\uline{complete Noetherian local ring with\nresidue field}',
   'passage to formal schemes','Restore the source emphasis on the base-ring hypothesis.')
text,_,_=page_text(rel,205);body=text.split('\\src{205}\n',1)[1].split('\n\n',1)[0]
ch(body,underline_prose(body),'Corollary 1 continuation','Restore statement emphasis while retaining the existing English placement of flat over A.')
text,_,_=page_text(rel,205);body=text.split(r'\result{COROLLARY}{2} ',1)[1].split('\n\n',1)[0]
ch(body,underline_prose(body),'Corollary 2','Restore emphasis on the complete assertion, including its isomorphism qualification.')
text,_,_=page_text(rel,205);body=text.split(r'\result{COROLLARY}{3} ',1)[1].split('\n\n',1)[0]
parts=re.split(r'(nonsingular|\(up to\nisomorphism\))',body)
new=''.join(x if i%2 else underline_prose(x) for i,x in enumerate(parts))
ch(body,new,'Corollary 3','Restore printed emphasis while leaving simple and the parenthetical up to isomorphism unaccented.')
text,_,_=page_text(rel,205);body=text.split(r'\result{THEOREM}{9} ',1)[1]
parts=re.split(r'(nonsingular|\(up to isomorphism\ninducing the identity on \$\\symup\{X_0\}\$\))',body)
new=''.join(x if i%2 else underline_prose(x) for i,x in enumerate(parts))
ch(body,new,'Theorem 9 opening','Restore the printed statement emphasis, leaving simple and the parenthetical isomorphism condition unaccented.')
record_translation_page('en','182',205,rel,
    'Read the conclusion of Corollary 1, the nonabelian cohomology description and automorphism filtration, Corollaries 2 and 3, and the opening of Theorem 9. Approved 64 English formula correspondences with 63 French expressions; the English repeats A in flat over A, which does not add a hypothesis. Propagated the corrected quotient index X_(n-1) and the positive-degree associated graded. The English already has X rather than Y in Corollary 1 and X_n in Corollary 2. Restored Gothic G, wavy Aut, inline formulas, statement emphasis and the precise page-206 boundary.',(575,640))
event('en-182-Theorem8-Corollary1','targeted proof check',
    'Checked existence by successive Artinian quotients conditional on Theorem 8 and the obstruction calculation on page 204. At each square-zero step the obstruction belongs to H^2(T_X0/k) tensor the relevant graded piece of the maximal ideal. Its vanishing permits a lift; Artinian nilpotence makes the sequence finite. This proves existence, without selecting a canonical lift.',
    '182, pp. 204–205, Corollary 1 to Theorem 8')
event('en-182-automorphism-filtration','targeted proof check',
    'Checked the corrected indices and grading. For augmentation-compatible automorphisms, F^n is the kernel of reduction to X_(n-1)=X tensor A/m^n. The successive quotient is the tangent sheaf tensor m^n/m^(n+1), for n at least one. Commutators raise filtration degree, so the associated graded is commutative and the final nonzero step is central. The degree-zero summand of gr(A) must be omitted.',
    '182, p. 205, paragraph preceding Corollary 2')
event('en-182-Theorem8-Corollary2','targeted proof check',
    'Checked the torsor assertion conditional on the local lifting input. For the last square-zero ideal m^n, differences between gluing data of two liftings form tangent-sheaf 1-cocycles modulo changes of local identifications. Thus, if nonempty, the set of lifts with fixed reduction is a principal homogeneous space under H^1(T_X0/k) tensor m^n. It has no preferred zero before a reference lift is chosen.',
    '182, p. 205, Corollary 2 and parenthetical note')
event('en-182-Theorem8-Corollary3','targeted proof check',
    'Checked uniqueness up to isomorphism by induction on the Artinian quotients using Corollary 2. Vanishing of H^1 makes each nonempty lifting torsor a singleton and allows compatible comparisons of the given lifts. The assertion is at most one isomorphism class; it asserts neither existence nor uniqueness of the isomorphism.',
    '182, p. 205, Corollary 3')
update()
