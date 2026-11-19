from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-212'
def ch(old,new,where,why,kind='terminology',full=False,count=1):
    replace(rel,old,new,'English',page,where,'section 8: Lemmas 3–5 and Proposition 4',
      'French 182-212 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands: '+why,kind=kind,full=full,count=count)
whole=read(rel);start=whole.index("$Y'$ of $Y$ associated with");end=whole.index('\\src{213}',start)+len('\\src{213}')
old=whole[start:end];new='\\src{213}\n'+old[:-len('\\src{213}')]
ch(old,new,'Proposition 4 page boundary','The printed page ends after Then the covering; move the marker before Y prime.',kind='structure',full=True)
align_math(rel,'en','182',212,[(i,i) for i in range(49)],(49,49))
for old,new in [(r'\textit{i.}','i.'),(r'\textit{ii.}','ii.'),(r'\textit{i bis.}','i. bis'),(r'\textit{(i)}','(i)'),(r'\textit{(ii)}','(ii)')]:
    ch(old,new,'Lemma 3 conditions','Restore the printed roman labels and references.',kind='structure')
for term in ['is completely split over','The natural morphism','is an isomorphism','Under these conditions','Finally, if','is connected, condition','is equivalent to the following\napparently weaker condition','admits a regular section over']:
    ch(term,'\\uline{'+term+'}','Lemma 3 conditions','Restore the corresponding printed emphasis span.')
ch('is an unramified extension of','\\uline{is an} unramified \\uline{extension of}','Lemma 3 conclusion','Restore emphasis while leaving the adjective unramified unaccented, as in the French.')
ch(r'\emph{geometrically trivial}',r'\uline{geometrically trivial}','definition after Lemma 3','Restore the printed definition underlining.')
ch('Choose a geometric point','Let us choose a geometric point','Lemma 5','Restore the authors’ choisissons register.')
text,_,_=page_text(rel,212);body=text.split(r'\result{LEMMA}{4} ',1)[1].split('\n\n',1)[0]
main,last=body.rsplit(' surjective.',1)
ch(body,underline_prose(main)+' surjective.','Lemma 4','Restore statement underlining with surjective unaccented.')
text,_,_=page_text(rel,212);body=text.split(r'\result{LEMMA}{5} ',1)[1].split('\n\\[',1)[0]
before,after=body.split(' (which is connected). ',1)
ch(body,underline_prose(before)+' (which is connected). '+underline_prose(after),'Lemma 5','Restore statement underlining except the connectedness parenthesis.')
text,_,_=page_text(rel,212);body=text.split(r'\result{PROPOSITION}{4} ',1)[1].rstrip()
before,rest=body.split(' a separable scheme\nover ',1)
middle,after=rest.split(', i.e. ',1)
new=underline_prose(before)+' a separable scheme\n\\uline{over} '+middle+', i.e. '+underline_prose(after)
ch(body,new,'Proposition 4 hypotheses','Restore statement emphasis while leaving separable scheme and i.e. unaccented.')
record_translation_page('en','182',212,rel,
    'Read the equivalent conditions and geometric-triviality definition in Lemma 3, Lemmas 4 and 5 with their arguments, and the hypotheses of Proposition 4. Approved 49 formula pairs after moving the page-213 marker. English already has the three substantive corrected readings O_X in Lemma 4, f-star pullback in its proof, and Y as the target of Proposition 4. Restored the wavy algebra sheaf, plain O, bars and residue-field letter, plus roman labels and the exact selective emphasis.',(895,952))
event('en-182-Lemma3','targeted proof check',
    'Checked the reduction behind geometric triviality, conditional on invariance of finite etale covers under nilpotent thickenings and finite etale descent. After a separably closed Artinian base extension, each geometric connected component of X has only constant covers satisfying (i); their descent is a finite etale algebra B over A. Properness and H^0(X,O_X)=A identify H^0(X tensor_A B,O)=B, hence B=A-prime and yield (ii). Conversely a finite etale algebra splits geometrically. In the connected-cover case, a section gives one degree-one geometric component; conjugacy of geometric components forces all such components to have degree one, giving (i). The invoked descent and nilpotent-invariance theorems are background, not independently re-proved here.',
    '182, pp. 211–212, Lemma 3')
event('en-182-Lemma4','targeted proof check',
    'Rechecked the printed proof with the corrected O_X and pullback f-star(A). For a finite locally free algebra A on Y, projection gives f_*f^*A=A tensor f_*O_X=A. A nontrivial idempotent splitting of the pullback algebra therefore descends to a nontrivial splitting of A. Thus pullback preserves connected finite covers, the Galois-category criterion for surjectivity of the fundamental-group map.',
    '182, p. 212, Lemma 4 and proof')
event('en-182-Lemma5','used and rechecked in this run',
    'Rechecked the three steps identified by the author: injection follows from Lemmas 1–2, the middle kernel consists of geometrically trivial covers and is identified through Lemma 3, and the final surjection follows from Lemma 4 applied to the Stein factor together with purely inseparable and nilpotent invariance. The radicial residue-field hypothesis identifies the fundamental group of the Artinian Stein factor with that of k and ensures geometric connectedness.',
    '182, p. 212, Lemma 5 and following paragraph')
update()
