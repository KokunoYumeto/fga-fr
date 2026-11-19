from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-302',line,statement,'400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 r('un foncteur canonique de','un \\uline{foncteur canonique} de','paragraph after second display','1.4',why='The defining phrase is underlined.')
 r('la définition 1.3 en disant','la définition 3 en disant','full-faithfulness reformulation','1.3',why='The print abbreviates the reference to définition 3. The local context identifies 1.3; no normalization is justified.')
 r('diagramme (+) de ladite\ndéfinition est','diagramme (+) de ladite est dit','full-faithfulness reformulation','1.3',why='The scan reads de ladite est dit, without the repeated noun définition.')
 r('« pleinement\nfidèle », i.e.',r'\fquote{pleinement fidèle}, i. e.','quoted category terminology','1.3',why='Ordinary double quotes and spaced abbreviation.')
 if tree=='fr':
  r('sous-catégorie de la catégorie','sous-catégorie pleine de la catégorie','full-faithfulness reformulation','1.3',kind='misprint of the original',why='For the stated equivalence to full faithfulness, the target subcategory must be full. A proper subgroup H of G gives an equivalence BH onto the non-full subcategory BH of BG but not a fully faithful functor BH -> BG. The preceding Hom equalizer condition requires all compatible morphisms.')
 r(r'\emph{effective}',r'\uline{effective}','Definition 1.5 defining term','1.5',why='Underlined.')
 r("$\\xi'$, muni de cette donnée, est", "$\\xi'$ muni de cette donnée est",'Definition 1.5 object clause','1.5',why='No commas around muni de cette donnée.')
 old="la\ncatégorie $\\mathcal F_S$ est équivalente à la catégorie des objets de\n$\\mathcal F_{S'}$ munis d'une donnée de recollement effective."
 new="\\uline{la catégorie} $\\mathcal F_S$ \\uline{est équivalente à la catégorie des objets de}\n$\\mathcal F_{S'}$ \\uline{munis d'une donnée de recollement effective}."
 r(old,new,'equivalence following Definition 1.5','1.5',why='The conclusion is underlined except the category symbols and terminal period.')
 r(r"S''=S'\times_S S',",r"S''=S'\times_S S'",'fiber-square display','1(c)',why='No terminal comma.')
 r('sur ses deux facteurs','sur ces deux facteurs','projection explanation','1(c)',why='The print reads ces, not ses.')
 r(r'$\mathcal C$ les produits',r'$\text{\uwave{C}}$, les produits','fiber-product parenthesis','1(c)',why='Ordinary wavy-underlined C followed by a comma.')
 r('soit effective. On a','soit effective.\n\nOn a','before condition i','1(c)',kind='structure',why='On a starts a separate paragraph.')
 r(r"\Delta^*(\varphi)=\operatorname{id}_{\xi'},",r"\Delta^*(\varphi)=\operatorname{id}_{\xi'}",'condition i display','1(c)(i)',why='No terminal comma.')
 r("$(p_i\\Delta)^*(\\xi')=\\xi'$. On a", "$(p_i\\Delta)^*(\\xi')=\\xi'$.\n\nOn a",'before condition ii','1(c)',kind='structure',why='On a starts a separate paragraph.')
 r(r'p_{31}^*(\varphi)=p_{32}^*(\varphi)\,p_{21}^*(\varphi),',r'p_{31}^*(\varphi)=p_{32}^*(\varphi)\,p_{21}^*(\varphi)','condition ii display','1(c)(ii)',why='No terminal comma. The indices and composition order are retained exactly; the projection convention continues on the next page.')
 upright_page(rel,layer,'190-302')
event('190-1.3-full-subcategory','refuted, with the refined statement\'s id','The explanatory i. e. needs a full subcategory. Counterexample: inclusion of the one-object category of a proper subgroup H into that of G is an equivalence onto its non-full image subcategory but is not full. Corrected French inserts pleine; refined statement id 190-1.3-full-subcategory-qualified. Under the Hom equalizer condition the essential image is full, so the qualified reformulation follows.','190, p. 302, reformulation of Definition 1.3')
event('190-1.4-canonical-gluing','targeted proof check','The two beta-pullbacks of alpha-star xi identify naturally with gamma-star xi; transporting identity gives the canonical gluing isomorphism. Naturality of c(beta_i,alpha) makes alpha-star u compatible, yielding the asserted canonical functor.','190, p. 302, first two displays and following paragraph')
event('190-1.5','targeted proof check','Effective data are exactly the essential image of the canonical functor. If the diagram is F-exact, that functor is fully faithful, hence an equivalence onto effective data. The unique isomorphism of descents is the one compatible with the chosen identifications with the fixed glued object; the assertion is not read as excluding all automorphisms of the underlying object.','190, p. 302, Definition 1.5 and following paragraph')
event('190-1c-normalization','targeted proof check','For canonical data, pullback along the diagonal identifies both projections with the identity, so the comparison is identity by coherence. This proves condition (i). The written indices 31, 32, 21 in (ii) have been visually checked; their projection convention continues on p. 303 and is not silently replaced by another convention.','190, p. 302, conditions (i)–(ii)')
record_page('190',302,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 160–212 with scan leaf 5 at 400 dpi and all three enlarged bands. Read the canonical gluing and map displays, full-faithfulness paragraph, Definition 1.5 and its equivalence conclusion, the fiber-square setup, diagonal identification and cocycle formula. The next marker is correctly after condition (ii).

Restored underlining of foncteur canonique, effective and the equivalence conclusion; the printed abbreviated reference définition 3; de ladite est dit; ordinary quotes and i. e.; omission of two editorial commas in Definition 1.5; ces deux facteurs; the wavy C and following comma; separate On a paragraphs; and no punctuation after the fiber-square, diagonal or cocycle displays. All displayed indices and primes were enlarged and read.

New corrected-only qualification: sous-catégorie pleine in the reformulation of full faithfulness. Without pleine the reverse implication fails for a proper subgroup's one-object category included in the ambient group category; the Hom exactness condition explicitly supplies fullness. Canonical gluing, functoriality, the equivalence with effective data, and diagonal normalization were checked using naturality/coherence and full faithfulness. Unique isomorphism is interpreted compatibly with the chosen descent identification. The cocycle index convention will be read on its continuation page before judging its composition order.''')
from update_record_counts import update
update()
