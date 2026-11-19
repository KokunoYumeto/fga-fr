from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-211'
def ch(old,new,where,why,kind='terminology',full=False,count=1):
    replace(rel,old,new,'English',page,where,'section 8: Lemmas 1–3',
      'French 182-211 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands: '+why,kind=kind,full=full,count=count)
whole=read(rel);start=whole.index('\\begin{enumerate}',whole.index('\\result{LEMMA}{3}'));end=whole.index('\\src{212}',start)+len('\\src{212}')
old=whole[start:end];new='\\src{212}\n'+old[:-len('\\src{212}')]
ch(old,new,'Lemma 3 page boundary','The printed page ends with the introduction to the two equivalent conditions; move the marker before their list.',kind='structure',full=True)
ch('\\footnote{The printed text says “inseparable coverings.”\nThe paragraph concerns the category $R(X)$ of unramified coverings and its\nequivalence with finite sets carrying a continuous $\\pi_1(X,a)$-action.}',
   '', 'opening classification paragraph','The explanatory editorial footnote is absent from the print and corrected French. The corrected unramified reading remains; its reason belongs to the records.',kind='translation')
align_math(rel,'en','182',211,[(i,i) for i in range(45)],(45,45))
ch('covariant functor of the\npointed scheme','\\uline{covariant functor of the\npointed scheme}','opening paragraph','Restore the underlined phrase.')
ch('the groups\nare topological','one has \\uline{topological groups}','opening paragraph','Preserve the source’s on a register and its emphasis on topological groups.')
ch('Since we do not\nknow what the higher homotopy groups should be,','Clearly, for lack of\nknowing what the higher homotopy groups are,','aim of section 8','Restore Evidemment and the impersonal faute de savoir register.')
ch('for every algebraic\nextension','for \\uline{every} algebraic\nextension','consequence of Lemmas 1 and 2','Restore the emphasis on toute.')
ch(r'\textit{a priori}','a priori','Lemma 3 parenthesis','The printed a priori is unaccented.')
ch('consider the unramified covering','let us consider the unramified covering','Lemma 3','Restore the authors’ considérons register.')
text,_,_=page_text(rel,211)
body=text.split(r'\result{LEMMA}{1} ',1)[1].split('\n\n',1)[0]
before,rest=body.split(' (with marked\npoint ',1);aside,after=rest.split('). ',1)
main,last=after.split(' (and is therefore ',1)
new=underline_prose(before)+' (with marked\npoint '+aside+'). '+underline_prose(main)+' (and is therefore \\uline{injective}).'
ch(body,new,'Lemma 1','Restore statement underlining, leaving the marked-point parenthesis and the words and is therefore unaccented.')
text,_,_=page_text(rel,211);body=text.split(r'\result{LEMMA}{2} ',1)[1].split('\n\n',1)[0]
before,after=body.split(' (i.e. extension of scalars) ',1)
ch(body,underline_prose(before)+' (i.e. extension of scalars) '+underline_prose(after),'Lemma 2','Restore statement underlining, excluding the explanatory parenthesis.')
text,_,_=page_text(rel,211);body=text.split(r'\result{LEMMA}{3} ',1)[1].rstrip()
parts=body.split(' (and may\na priori be ramified over ',1);before=parts[0];aside,rest=parts[1].split('). ',1)
main,rest2=rest.split(' (obtained by quotienting by the sheaves of\nnilpotent elements in ',1)
aside2,rest3=rest2.split('), ',1)
main2,rest4=rest3.split(' is finite (so ',1)
aside3,tail=rest4.split('it). ',1)
new=(underline_prose(before)+' (and may\na priori be ramified over '+aside+'). '+underline_prose(main)
     +' (obtained by quotienting by the sheaves of\nnilpotent elements in '+aside2+'), '+underline_prose(main2)
     +' is finite (so '+aside3+'it). '+underline_prose(tail))
ch(body,new,'Lemma 3 hypotheses','Restore the source’s individual emphasis spans, excluding all three explanatory parentheses and the unaccented words is finite.')
record_translation_page('en','182',211,rel,
    'Read the functoriality and classification paragraph, section aim, Lemmas 1 and 2 and their consequence, and all hypotheses of Lemma 3. Approved 45 formula pairs after removing the editorial footnote and moving the page-212 boundary before the conditions. English already has unramified coverings and the corrected initial X in Lemma 3. Restored plain O, the statement underlining with its unaccented asides, every in the algebraic-extension consequence, and the authors’ register.',(853,913))
event('en-182-Lemma1','targeted proof check',
    'Using the preceding Galois equivalence, restrict to the orbit of the marked point e in the finite pi-set E. That orbit is pi/H for H the open stabilizer of e, and finite covers of its pointed connected component correspond to finite continuous H-sets. The induced fundamental-group map is H into pi, hence injective with the stated image. This checks the reduction to the Galois-category statement, not a new proof of reconstruction.',
    '182, p. 211, Lemma 1')
event('en-182-Lemma2','carried as background without fault found',
    'Read invariance of finite unramified coverings under a radicial field extension. It is the purely inseparable invariance theorem for finite etale covers; a proof requires finite-height Frobenius descent and passage to a filtered union for a general extension. That descent theorem was not independently proved on this page.',
    '182, p. 211, Lemma 2')
event('en-182-algebraic-base-extension-injection','targeted proof check',
    'Conditional on Lemma 2, the finite algebraic case factors through a finite separable extension, where Lemma 1 gives an open-subgroup inclusion, and a purely inseparable extension, which preserves covers. A general algebraic extension is the union of its finite subextensions; finite etale covers and their morphisms descend to a finite stage, so the inverse-limit group map remains injective.',
    '182, p. 211, consequence of Lemmas 1 and 2')
update()
