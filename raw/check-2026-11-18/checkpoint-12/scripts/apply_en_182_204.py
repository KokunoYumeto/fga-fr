from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-204'
def ch(old,new,where,why,kind='terminology',full=False,count=1):
    replace(rel,old,new,'English',page,where,'Theorem 8 and deformation obstruction',
      'French 182-204 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands: '+why,kind=kind,full=full,count=count)
whole=read(rel);start=whole.index('$H^2(X_0,\\Theta_{X_0/k})=0$');end=whole.index('\\src{205}',start)+len('\\src{205}')
old=whole[start:end];new='\\src{205}\n'+old[:-len('\\src{205}')]
ch(old,new,'printed page break in Corollary 1','The print breaks after supposons, before the H^2 condition. Move the existing page marker to that point.',kind='structure',full=True)
ch('let $n>0$ be\nan integer','let $n$ be\nan integer $>0$','successive lifting setup','Restore the source’s two separate inline expressions and their placement around integer.',kind='structure')
align_math(rel,'en','182',204,[(i,i) for i in range(61)],(61,61))
for roman in ['i','ii']:
    ch('\\textit{'+roman+'.}', '\\textnormal{'+roman+'.}','augmentation structure list','Restore roman item labels.',kind='structure')
ch('$\\symup{\\mathfrak m^nO_X/\\mathfrak m^{n+1}O_X =O_{X_0}\\otimes_k(\\mathfrak m^n/\\mathfrak m^{n+1})}$\n\\end{enumerate}\nThe fundamental fact is the following.',
   '$\\symup{\\mathfrak m^nO_X/\\mathfrak m^{n+1}O_X =O_{X_0}\\otimes_k(\\mathfrak m^n/\\mathfrak m^{n+1})}$.\nThe fundamental fact is the following:\n\\end{enumerate}',
   'end of augmentation structure list','The print continues the paragraph after the inline graded-piece formula and introduces Theorem 8 with a colon. Match that paragraph structure.',kind='structure')
ch('The isomorphism in question is not canonical','Let us note that the isomorphism in question is not canonical','after Theorem 8','Restore the authors’ Notons register.')
ch('the equal-characteristic case','the \\uline{equal-characteristic} case','coefficient-field case','Restore source emphasis on égales caractéristiques.')
ch('we seek to lift','one seeks to lift','successive lifting setup','Restore impersonal on se propose under the register standard.')
ch('an obstruction to constructing','an \\uline{obstruction to constructing}','obstruction conclusion','Restore the printed emphasis.')
ch('$\\symup{X_n}$ lifting\n$\\symup{X_{n-1}}$', '$\\symup{X_n}$ \\uline{lifting}\n$\\symup{X_{n-1}}$',
   'obstruction conclusion','Restore the separate emphasis on remontant.')
ch('$\\symup{H^2(X_0,\\mathfrak G_{X_0/k})\\otimes \\mathfrak m^n/\\mathfrak m^{n+1}}$\nConsequently:',
   '$\\symup{H^2(X_0,\\mathfrak G_{X_0/k})\\otimes \\mathfrak m^n/\\mathfrak m^{n+1}}$.\nConsequently:',
   'obstruction group','Restore the external period after the inline formula.',kind='structure')
for heading in [r'\result{THEOREM}{8} ',r'\result{COROLLARY}{1} ']:
    text,_,_=page_text(rel,204);body=text.split(heading,1)[1].split('\n\n',1)[0]
    ch(body,underline_prose(body),'Theorem 8 and Corollary 1 opening','Restore the printed statement emphasis.')
record_translation_page('en','182',204,rel,
    'Read the augmented-algebra description of flat liftings, Theorem 8, the noncanonical-choice discussion, and the automorphism and obstruction sheaves through the opening of Corollary 1. Approved 61 formula correspondences after splitting n and >0 and restoring the page-205 marker. The English already has the corrected base A in the sentence about a mixed-characteristic lifting. Replaced Theta by the source Gothic G for derivations and restored inline formulas, roman labels, source emphasis and the Notons/on register. The author’s historical first-person uncertainty is preserved.',(526,608))
event('en-182-Theorem8','carried as background without fault found',
    'Read the existence and uniqueness up to noncanonical isomorphism of a flat lifting of a smooth affine scheme to a local Artinian ring. The text gives no proof here. It requires the infinitesimal lifting property for smooth affine algebras; no independent proof of that input is claimed in this page check.',
    '182, p. 204, Theorem 8 and following qualification')
event('en-182-deformation-obstruction','targeted proof check',
    'Checked the local automorphism and gluing calculation conditional on Theorem 8. Over the square-zero last ideal I=m^n/m^(n+1), an automorphism inducing the identity is 1+d with d a k-derivation into O_X0 tensor I; products add derivations because I^2=0. Differences of gluing maps therefore form an abelian tangent-sheaf cocycle. Its triple-overlap obstruction lies in H^2(T_X0/k) tensor I, and vanishing permits the adjustment needed to glue.',
    '182, p. 204, paragraphs after Theorem 8, automorphism sheaf and obstruction')
update()
