from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-199'
def ch(old,new,where,why,kind='terminology',full=False,count=1):
    replace(rel,old,new,'English',page,where,'Theorems 4 and 5',
      'French 182-199 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands: '+why,kind=kind,full=full,count=count)
whole=read(rel);start=whole.index('that is, the\nset of connected components');end=whole.index('\\src{200}',start)+len('\\src{200}')
old=whole[start:end];new='\\src{200}\n'+old[:-len('\\src{200}')]
ch(old,new,'printed page break in Theorem 5','The print ends page 199 after the connectedness assertion and continues its explanation on page 200. Move the existing marker to this point.',kind='structure',full=True)
align_math(rel,'en','182',199,[(i,i) for i in range(47)],(47,47))
ch('$\\symup{H^2(\\mathfrak X_0,O_{\\mathfrak X_0})=0}$\n', '$\\symup{H^2(\\mathfrak X_0,O_{\\mathfrak X_0})=0}$.\n','Theorem 4(ii) continuation','Restore the external period after changing the formula to its printed inline form.',kind='structure')
ch(r'\textit{iii.}',r'\textnormal{iii.}','Theorem 4(iii)','Restore roman item label.',kind='structure')
ch('$\\symup{\\mathfrak X_0}$ is projective.', '$\\symup{\\mathfrak X_0}$ \\uline{is projective}.','Theorem 4(iii)','Restore printed emphasis.')
text,_,_=page_text(rel,199);body=text.split('\\end{enumerate}\n',1)[1].split('\n\n',1)[0]
newbody=underline_prose(body).replace('\\uline{is a projective}', '\\uline{is a} projective')
ch(body,newbody,'Theorem 4 conclusion','Restore statement emphasis while leaving projective unaccented, as in the source.')
for roman,count in [('i',1),('ii',2),('iii',2)]:
    ch('\\textit{('+roman+')}','('+roman+')','Theorem 4 proof references','Restore roman reference typography.',kind='structure',count=count)
ch('nonsingular curve','\\uline{nonsingular curve}','curve example','Restore the source emphasis on courbe simple.')
ch('(of\n“projective type” and dimension', '(the\n“standard projective space” of dimension','projective space in Theorem 4 proof','Projectif type denotes the standard projective space P_A^r; the former wording made it an unspecified type of projective scheme.',kind='translation')
ch('\\fsection{4}{Application to the connectedness theorem and Zariski\'s Main\nTheorem}',
   '\\fsection{\\normalfont4}{\\normalfont\\uline{Application to the connectedness theorem and Zariski\'s “Main\ntheorem”}.}',
   'section 4 heading','Restore heading underlining, the quoted Main theorem, and the final period.',kind='structure')
ch('the \\emph{Stein factorization}','\\uline{the Stein factorization}','Stein factorization definition','Restore source underlining including the article.')
text,_,_=page_text(rel,199);body=text.split(r"\result{THEOREM}{5 (Zariski's “connectedness theorem”)} ",1)[1]
pre,post=body.split('(up to\nisomorphism)',1)
newbody=underline_prose(pre)+'(up to\nisomorphism)'+underline_prose(post)
newbody=newbody.replace('\\uline{whence}', 'whence')
ch(body,newbody,'Theorem 5 first part','Restore the underlined statement while preserving the two unaccented parenthetical qualifications.')
record_translation_page('en','182',199,rel,
    'Read the conclusion and proof sketch of Theorem 4, the Stein factorization construction, and the first part of Theorem 5. Approved all 47 formula correspondences after restoring the page-200 break. The English already uses Gothic X for the formal scheme in the immersion, agreeing with the corrected French rather than the ordinary X misprint. Restored source emphasis and the inline H^2 condition. Corrected the rendering of projectif type to standard projective space.',(286,339))
event('en-182-Theorem4','targeted proof check',
    'Checked the stated proof sketch with Theorems 1 and 3 as inputs. Flatness identifies the successive ideal quotients with O_X0 tensor the finite vector spaces m^n/m^(n+1), so H^2(O_X0)=0 removes each line-bundle lifting obstruction. Lift an ample bundle and take a high power; H^1 vanishing on the closed fiber permits compatible lifting of sections, and Nakayama gives a formal projective immersion. Apply coherent-ideal algebraization on projective space to obtain a projective A-scheme. This expands the sketch conditional on the earlier finiteness/algebraization inputs.',
    '182, pp. 198–199, Theorem 4 and proof sketch')
event('en-182-Theorem5-connectedness','targeted proof check',
    'Checked the local connectedness argument. Localize at y-prime. Formal functions identifies sections of the completed fiber neighborhood with the completion of O_y-prime, a local ring. A disconnected fiber would split the underlying formal space into two nonempty open-and-closed pieces and give a nontrivial 0/1 idempotent in those sections, impossible in a local ring. The relative Spec of f_*O_X gives the finite factor; its affine pushforward is faithful, yielding f-prime_*O_X=O_Y-prime and uniqueness of that factorization.',
    '182, p. 199, section 4, Theorem 5')
update()
