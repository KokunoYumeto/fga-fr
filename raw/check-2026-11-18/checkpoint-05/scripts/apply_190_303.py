from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-303',line,statement,'400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 txt,_,_=page_text(rel,303)
 for a,b,body in list(footnotes(txt)):
  r(txt[a:b],'','split morphism paragraph','1.7',kind='structure',why='No footnote is printed. This supplied footnote merges the 1962 erratum; the erratum must remain in its separate section.')
 r(r'\emph{donnée de descente}',r'\uline{donnée de descente}','Definition 1.6 defining term','1.6',why='Underlined rather than italic.')
 r(r'\emph{morphisme de $\mathcal F$-descente}',r'\uline{morphisme de} $\mathcal F$-\uline{descente}','Definition 1.7 first defining term','1.7',why='Underlined prose with the script letter excluded.')
 r(r'\emph{morphisme de $\mathcal F$-descente strict}',r'\uline{morphisme de} $\mathcal F$-\uline{descente strict}','Definition 1.7 second defining term','1.7',why='Underlined prose with the script letter excluded.')
 r(r'\overset{p_1}{\underset{p_2}{\rightrightarrows}}',r'\overset{p_1}{\underset{p_2}{\leftleftarrows}}','Definition 1.7 base diagram','1.7',why='Both projection arrows point left in the scan, from the fiber square to S-prime.')
 r('(définition 1.3)','(définition 1.3.)','Definition 1.7 first reference','1.7',why='The reference has a period inside the closing parenthesis.')
 r('(définition 1.6)','(définition 1.6.)','Definition 1.7 second reference','1.7',why='The reference has a period inside the closing parenthesis.')
 r('peut aussi, de façon plus imagée,','peut aussi de façon plus imagée','equivalence paraphrase opening','1.7',why='No paired commas around the phrase.')
 old="« Il revient au même » de se donner un objet de $\\mathcal F_S$, ou un objet de\n$\\mathcal F_{S'}$ muni d'une donnée de descente."
 new="\\fquote{\\uline{Il revient au même}} \\uline{de se donner un objet de} $\\mathcal F_S$, \\uline{ou un objet de}\n$\\mathcal F_{S'}$ \\uline{muni d'une donnée de descente}."
 r(old,new,'equivalence paraphrase','1.7',why='Ordinary double quotes around Il revient au même; the whole prose assertion is underlined except punctuation and math.')
 r(r"Notons que si un morphisme $\alpha:S'\longrightarrow S$",r"Notons que si un morphisme de $\mathcal F$-descente $\alpha:S'\longrightarrow S$",'split morphism hypothesis','1.7',kind='structure',why='The original explicitly assumes a morphism of F-descent. Removing that hypothesis implements the later erratum and is therefore reverted in both exposé layers.')
 r('« section »',r'\fquote{\uline{section}}','split morphism section term','1.7',why='The quoted word is underlined and uses ordinary double quotes.')
 r('(i.e. un morphisme','(i. e. un morphisme','split morphism parenthesis','1.7',why='Spaced abbreviation.')
 r(r'$\alpha s=\operatorname{id}_S$), alors',r'$\alpha s=\operatorname{id}_S$) alors','end of section parenthesis','1.7',why='No comma after the parenthesis.')
 r('descente strict. Si','descente strict : si','split morphism conclusion','1.7',why='Colon followed by lowercase si.')
 r('il « provient »',r'\fquote{il provient}','split morphism explanation','1.7',why='Both il and provient are within the printed double quotation marks.')
 r(r'\mathcal C',r'\text{\uwave{C}}','object-parameter base category','1(d)',why='Wavy-underlined ordinary C.')
 r('de 1.c s’écrivent','de 1.(c) s’écrivent','reference before i bis','1(d)',why='The scan encloses c in parentheses.') if 'de 1.c s’écrivent' in page_text(rel,303)[0] else None
 r("de 1.c s'écrivent","de 1.(c) s'écrivent",'reference before i bis','1(d)',why='The scan encloses c in parentheses.')
 r(r"\qquad\text{pour tout $T$ et tout $t\in S'(T)$},",r"\qquad\text{pour tout $T$ et tout $t\in S'(T)$}",'i bis display ending','1(d)(i bis)',why='No terminal comma.')
 upright_page(rel,layer,'190-303')
event('190-1.6','carried as background without fault found','Read the definition of descent data with the two printed normalization/cocycle conditions. The opening line defines p_ij by the ith and jth factors. There is a potential order conflict with the product in p. 302(ii), now explicitly flagged for resolution against the pointwise cocycle on p. 304; no projection convention has been silently substituted.','190, p. 303, opening line and Definition 1.6')
event('190-1.7','targeted proof check','The definition is full faithfulness of the canonical functor, and strictness adds essential surjectivity onto descent data. Restored the printed prior F-descent hypothesis in the split-morphism observation, rather than merging the later erratum. With a section s, the candidate descent is s-star xi-prime; pullback along (s alpha,id) of the gluing datum gives alpha-star s-star xi-prime -> xi-prime, and compatibility follows from the cocycle. The printed projection-order issue remains tracked separately.','190, p. 303, Definition 1.7 and split-morphism observation')
event('190-1d-points','targeted proof check','The pointwise gluing maps come from pullback by (t,t-prime):T -> S-prime times_S S-prime. Conversely, evaluate a natural family on the universal pair of projections to recover the original map; functoriality recovers every other pair. The diagonal condition becomes phi(t,t)=identity. The pointwise cocycle continues on p. 304.','190, p. 303, paragraph d and (i bis)')
record_page('190',303,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 214–272 with scan leaf 6 at 400 dpi and all three enlarged bands. Read the p_ij explanation, Definitions 1.6–1.7, the split-morphism observation and its parenthesis, all object/arrow primes, the T-point description and (i bis). The marker is correctly after (i bis).

Restored underlined definitions and the equivalence paraphrase; both leftward projection arrows; periods inside the 1.3 and 1.6 reference parentheses; omission of two editorial commas; the quoted/underlined section, spaced i. e., colon and lowercase si, quotes including il provient, wavy-underlined C, the reference 1.(c), and no final comma in (i bis). Restored the original F-descent hypothesis in the split-morphism observation and removed the unprinted footnote that merged the later erratum, in both French layers.

Checked the equivalence interpretation, the section pullback construction subject to the cocycle, and the universal-pair argument for the functor-of-points description. The opening definition of p_ij makes the order in p. 302(ii) suspect when read as the ordered pair (p_i,p_j); the immediately following pointwise cocycle is still to be read before deciding how to correct this. No claim of a completed proof with that unresolved order is made.''')
from update_record_counts import update
update()
