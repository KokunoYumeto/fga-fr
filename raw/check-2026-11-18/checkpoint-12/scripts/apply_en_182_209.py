from audit_utils import *
from translation_edits import *
from update_record_counts import update
rel='sources/en/en/182.tex';page='182-209'
def ch(old,new,where,why,kind='terminology',full=False,count=1):
    replace(rel,old,new,'English',page,where,'Theorem 10 and section 8',
      'French 182-209 and personally inspected full 400-dpi scan and enlarged top, middle and bottom bands: '+why,kind=kind,full=full,count=count)
whole=read(rel);start=whole.index('of $X$ if\n\\begin{enumerate}');end=whole.index('\\src{210}',start)+len('\\src{210}')
old=whole[start:end];new='\\src{210}\n'+old[:-len('\\src{210}')]
ch(old,new,'page break in covering definition','The print ends immediately after revêtement non ramifié. Move the existing marker before of X if.',kind='structure',full=True)
align_math(rel,'en','182',209,[(i,i) for i in range(22)],(22,22))
ch('is a sufficient condition','is a \\uline{sufficient} condition','representability discussion','Restore emphasis on sufficient.')
ch('Kodaira--Spencer','KODAIRA-SPENCER','analytical analogue reference','Restore the printed capitals and hyphen.',kind='structure')
ch('preceding section.','preceding section:','introduction to Theorem 10','Restore the introductory colon.',kind='structure')
ch('As already noted,','As we have already noted,','algebraization paragraph','Restore the authors’ nous register.')
ch('Methods such as those presented','Let us also note that methods such as those presented','Picard paragraph','Restore the authors’ Remarquons aussi register.')
ch(r'\fsection{8}{Application to the fundamental group}',
   r'\fsection{\normalfont8}{\normalfont\uline{Application to the fundamental group}.}',
   'section 8 heading','Restore the roman underlined heading and final period.',kind='structure')
ch('Lang--Serre','LANG-SERRE','section 8 introduction','Restore the printed capitals and hyphen.',kind='structure')
ch('called an unramified covering','called an \\uline{unramified covering}','covering definition opening','Restore emphasis on the defined term.')
text,_,_=page_text(rel,209);body=text.split(r'\result{THEOREM}{10} ',1)[1].split('\n\n',1)[0]
before,rest=body.split('\\[',1);formula,after=rest.split('\\]',1)
main,aside=after.split(' (i.e.',1)
new=underline_prose(before)+'\\['+formula+'\\]'+underline_prose(main)+' (i.e.'+aside
ch(body,new,'Theorem 10','Restore the statement’s printed emphasis, leaving the explanation of the regular ring unaccented.')
record_translation_page('en','182',209,rel,
    'Read the representability discussion, Theorem 10, the algebraization and Picard observations, and the opening of section 8 through unramified covering. Approved all 22 formula correspondences after restoring the page-210 boundary. The English already has the corrected X_0 in the opening properness hypothesis. Restored the source arrow in A to F(A), Gothic G, statement and definition emphasis, normal section typography, author-name capitals and the authors’ register. The sufficient H^0 criterion before Theorem 10 is retained as the author’s plausible claim, distinct from the theorem with both vanishing hypotheses.',(768,824))
event('en-182-Theorem10','targeted proof check',
    'Checked the formal construction conditional on the preceding deformation and gluing calculations. Properness makes H^1(T_X0/k) finite-dimensional. Choose a basis and a first-order family with identity Kodaira–Spencer map over the square-zero quotient of R=k[[t_1,...,t_d]]. H^2=0 permits compatible extensions to every power of the maximal ideal of R. For a small extension of Artinian test algebras with kernel I, lifts of a map from R form a torsor under H^1(T) tensor I, as do lifts of the deformation; the tangent isomorphism identifies these torsors. H^0(T)=0 removes infinitesimal automorphisms reducing to the identity, so comparison introduces no orbit quotient. Induction on length gives the natural bijection Hom(R,A)=F(A), establishing a regular representing ring in this setting.',
    '182, p. 209, Theorem 10')
event('en-182-representability-H0-suggestion','carried as background without fault found',
    'Read the suggestion that H^0(T)=0 alone is sufficient for formal moduli and is not necessary. The preceding general necessary-and-sufficient criterion is explicitly not stated here. This suggestion was not independently proved in this page check and is not conflated with the stronger hypotheses of Theorem 10.',
    '182, p. 209, paragraph preceding Theorem 10')
event('en-182-Theorem10-algebraization','used and rechecked in this run',
    'Rechecked the reference to Theorem 4: projectivity of X_0 and H^2(O_X0)=0 lift an ample line bundle and allow algebraization of the proper formal family. The dimension-one case uses the same coherent H^2 vanishing as Corollary 4 of Theorem 9. The page asserts no general algebraization without these extra hypotheses.',
    '182, p. 209, paragraph after Theorem 10')
update()
