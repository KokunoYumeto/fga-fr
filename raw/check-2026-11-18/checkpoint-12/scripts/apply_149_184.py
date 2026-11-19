from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/149.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'149-184',line,statement,'400-dpi scan, enlarged bands and tight exponent crops. '+why,kind,count=count)
 r('Alors, pour $m$','Alors pour $m$','Lemma 5, line 2','5-lem5',why='There is no comma after Alors.')
 txt,_,_=page_text(rel,184);start=txt.index(r'\result{LEMME}{5} ')+len(r'\result{LEMME}{5} ');stop=txt.index(r'\[',start);old=txt[start:stop]
 r(old,underline_prose(old),'Lemma 5 prose','5-lem5',why='The statement prose is underlined, excluding variables.')
 r('\nest un isomorphisme.','\n\\uline{est un isomorphisme}.','Lemma 5 conclusion','5-lem5',why='The concluding words are underlined.')
 r("pour l'espace projectif.\nSupposons", "pour l'espace projectif.\n\nSupposons",'before general X case','5-D','structure','Supposons begins a new paragraph in the print.')
 r('dualité pour $P$, on a un isomorphisme\n', 'dualité pour $P$, on a un isomorphisme,\n','general X introduction','5.6',why='A comma follows isomorphisme before the displayed formula.')
 r(r'=\operatorname{Ext}_{\Osh_P}^{r-n}(P;F,\Omega_P^{r}).',r'=\operatorname{Ext}_{\Osh_P}^{r-n}(P;F,\Omega_P^{r})','ambient duality formula','5.6',why='The display has no terminal full stop.')
 r(r'(n\textsuperscript{o} 4), le dernier',r'(n\textsuperscript{o} 4) le dernier','Lemma 1 reference','5.6',why='The reference is not followed by a comma.')
 r(r'=\operatorname{Ext}_{\Osh_X}^{0}(X;F,\Omega_X^{n}),',r'=\operatorname{Ext}_{\Osh_X}^{0}(X;F,\Omega_X^{n})','Hom identification display','5.6',why='The display has no terminal comma.')
 r(r'=\operatorname{Ext}_{\Osh_X}^{0}(X;F,\Omega_X^{n}).',r'=\operatorname{Ext}_{\Osh_X}^{0}(X;F,\Omega_X^{n})','formula 5.6','5.6',why='The numbered display has no terminal full stop.')
 r(r'\xrightarrow{\sim}k.',r'\xrightarrow{\sim}\underline{k}','formula 5.7','5.7',why='The base field k is underlined and there is no terminal full stop.')
 for symbol in [r'\Omega',r'\omega']:
  txt,_,_=page_text(rel,184);r(symbol,r'\underline{'+symbol+'}','differential sheaf symbols','5.6;5.7',why='Each Greek differential-sheaf symbol is visibly underlined.',count=txt.count(symbol))
 upright_page(rel,layer,'149-184')
event('149-5-lem5','targeted proof check','The exponent in the statement is 1, confirmed by enlargement. For total degree 1, vanishing of positive cohomology of the coherent Hom and Ext sheaves after a large positive twist gives the edge isomorphism. Only finitely many relevant spectral-sequence terms are needed; no uniform vanishing over every q is asserted by this check.','149, p. 184, Lemma 5 and proof')
event('149-5-D-projective','targeted proof check','For X=P, n=r. At p=n both sides are contravariant left-exact functors; two finite presentations by negative twists reduce their comparison to Lemma 2. For p<n, the coeffaceability proved on p. 183 yields the universal delta-functor comparison. This argument applies to the coherent category used by those lemmas.','149, p. 184, proof of D for projective space')
event('149-5.6','carried as background without fault found','Read the ambient-projective-space duality and the change-of-ring identification through Lemma 1. Indices r-n, r and n agree with codimension and dimensions; no new correction of mathematics was found here.','149, p. 184, general X case and (5.6)')
event('149-5.7','carried as background without fault found','Read the trace isomorphism obtained by setting F to the top differential sheaf in (5.6). A small mark next to its exponent was enlarged; it was not confidently identified as a second mathematical index and the reading n was retained.','149, p. 184, final sentence and (5.7)')
record_page('149',184,r'''Compared sources/fr_printed/fr/149.tex entry lines 798–848 and sources/fr/fr/149.tex entry lines 804–854 against scan leaf 17 at 400 dpi, the three enlarged bands, and tight crops of the degree-one Ext and the exponent in “F = Omega”. Read Lemma 5, the projective-space proof of D, and the reduction to (5.6) and (5.7).

Both layers restore the underlining of Lemma 5, a paragraph break, the printed punctuation, underlined Greek sheaf symbols and field k, and upright mathematical letters. The first Ext exponent is the numeral 1. The faint extra mark beside the final inline exponent n remains an explicit uncertainty for the second reading, not a newly asserted prime. No existing mathematical repair was introduced or reverted on this page. The scope and finite-term use of the spectral sequence were recorded in the check events.''')
from update_record_counts import update
update()
