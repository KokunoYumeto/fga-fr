from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-206'
def ch(old,new,where,why,kind='terminology',full=False,count=1):
    replace(rel,old,new,'English',page,where,'Theorem 9 and corollaries',
      'French 182-206 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands: '+why,kind=kind,full=full,count=count)
whole=read(rel);start=whole.index('by examining whether the first obstruction');end=whole.index('\\src{207}',start)+len('\\src{207}')
old=whole[start:end];new='\\src{207}\n'+old[:-len('\\src{207}')]
ch(old,new,'page break in Remark 1','The printed page ends after commencer. Move the existing marker to the corresponding position before by examining.',kind='structure',full=True)
align_math(rel,'en','182',206,[(i,i) for i in range(50)],(50,50))
for roman in ['i','ii']:
    ch('\\textit{'+roman+'.}', '\\textnormal{'+roman+'.}','Theorem 9 list','Restore roman item labels.',kind='structure')
ch(r'\textit{(i)}','(i)','Corollary 1 reference','Restore the roman reference.',kind='structure')
ch(r'9\textit{(ii)}','9(ii)','Corollary 3 explanation','Restore the roman reference.',kind='structure')
ch('standard projective scheme','standard projective space','Corollary 2','Use the established English rendering of schéma projectif type, as elsewhere in this exposé.')
ch('a “smooth-curve scheme”','a “scheme of a nonsingular curve”','Corollary 4','Translate the quoted phrase schéma de courbe simple with the same nonsingular rendering of simple used in its hypothesis and the preceding corollaries.')
ch('Proposition 3, Corollary 1.)','Proposition 3, Corollary 1).','note after Corollary 2','Restore the period outside the parenthesis.',kind='structure')
ch(r'\result{REMARKS}{}',r'\result[.]{REMARKS}{}','remarks heading','Restore the printed heading’s period.',kind='structure')
ch('ring of characteristic $\\symup{0}$','ring of \\uline{characteristic} $\\symup{0}$','Remark 1','Restore the emphasis on characteristic.')
ch('“smallest possible $\\symup{A}$,”','“smallest possible $\\symup{A}$”,','Remark 1','Place the comma outside the quotation as in the source.',kind='structure')
ch('such ring $\\symup{A}$.) It\nmay be noted in this connection',
   'such ring $\\symup{A}$). Let\nus note in this connection',
   'Remark 1','Restore the external period and the authors’ Signalons register.')
text,_,_=page_text(rel,206);body=text.split('\\src{206}\n',1)[1].split('\\begin{enumerate}',1)[0]
ch(body,underline_prose(body),'Theorem 9 continuation','Restore statement emphasis.')
for roman in ['i','ii']:
    text,_,_=page_text(rel,206);marker='\\item[\\textnormal{'+roman+'.}] '
    body=text.split(marker,1)[1].split('\\item',1)[0].split('\\end{enumerate}',1)[0]
    ch(body,underline_prose(body),'Theorem 9 '+roman,'Restore the statement’s printed emphasis.')
text,_,_=page_text(rel,206);body=text.split(r'\result{COROLLARY}{1} ',1)[1].split('\n\n',1)[0]
parts=re.split(r'(\(up to isomorphism\ninducing the identity on \$\\symup\{X_0\}\$\))',body)
ch(body,''.join(x if i%2 else underline_prose(x) for i,x in enumerate(parts)),
   'Corollary 1','Restore statement emphasis, leaving the parenthetical isomorphism condition unaccented.')
for heading in [r'\result{COROLLARY}{2} ',r'\result{COROLLARY}{4} ']:
    text,_,_=page_text(rel,206);body=text.split(heading,1)[1].split('\n\n',1)[0]
    ch(body,underline_prose(body),heading,'Restore the full statement’s printed emphasis.')
text,_,_=page_text(rel,206);body=text.split(r'\result{COROLLARY}{3} ',1)[1].split('\n\n',1)[0]
before,rest=body.split('\\[',1);formula,after=rest.split('\\]',1)
ch(body,underline_prose(before)+'\\['+formula+'\\]'+underline_prose(after),
   'Corollary 3','Restore the prose emphasis on both sides of the displayed vanishing hypothesis.')
record_translation_page('en','182',206,rel,
    'Read the continuation and both parts of Theorem 9, its four corollaries and their short explanations, and the first part of Remark 1 through the printed page boundary. Approved all 50 formula correspondences. The English already has Gothic X in the reduction formula, agreeing with the corrected French. Restored source alphabets, statement emphasis, roman references, the quoted curve phrase and the authors’ register. The historical uncertainty in Remark 1 is preserved; the inserted later supplement now lies after the restored page-207 boundary for examination with that page.',(627,695))
event('en-182-Theorem9','targeted proof check',
    'Checked the formal passage from the Artinian lifting corollaries. Vanishing of H^2 allows compatible lifts over all A/m^(n+1); their compatible local affine algebras give the adic formal scheme. Vanishing of H^1 lets comparisons of two lifts extend successively with a fixed reduction, yielding an isomorphism of inverse systems and formal schemes. The argument gives existence and uniqueness of classes separately, without asserting that a formal lift is algebraic.',
    '182, pp. 205–206, Theorem 9(i) and (ii)')
event('en-182-Theorem9-Corollary1','targeted proof check',
    'Checked the deduction from Theorem 9(i) and the full faithfulness of completion for proper schemes in Theorem 3, Corollary 2. A formal isomorphism respecting the chosen closed fiber algebraizes uniquely as a morphism; algebraizing its inverse gives an algebraic isomorphism. Existence is not asserted.',
    '182, p. 206, Corollary 1')
event('en-182-Theorem9-Corollary2','targeted proof check',
    'Checked the rigidity deduction using the Euler sequence for projective space: H^1(O(1)) and H^2(O) vanish, so H^1(T_P^r)=0 (and r=0 is immediate). The standard projective space over A supplies one proper flat lift; Corollary 1 identifies every other such lift with it. Cohomology of line bundles on projective space is the background input.',
    '182, p. 206, Corollary 2')
event('en-182-Theorem9-Corollary3','targeted proof check',
    'Checked the stated combination of Theorem 9(ii) and Theorem 4. H^2 of the tangent sheaf gives a formal flat lifting; H^2(O) removes the successive obstructions to lifting an ample line bundle. The algebraization theorem then gives a projective flat scheme with the prescribed closed fiber.',
    '182, p. 206, Corollary 3')
event('en-182-Theorem9-Corollary4','targeted proof check',
    'Checked the curve deduction conditional on the standard facts that a complete nonsingular algebraic curve is projective and its coherent cohomology vanishes in degree two. Corollary 3 supplies the projective flat lift. Smoothness holds near the smooth closed fiber; properness over the local base forces the closed nonsmooth locus to be empty. These inputs give the asserted scheme of a nonsingular curve.',
    '182, p. 206, Corollary 4')
update()
