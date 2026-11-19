from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/232.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'232-152',line,'4.1 and relative Abel map',
                'Scan leaf 11 at 400 dpi and three enlarged bands: '+why,kind=kind,count=count)
    notes=list(footnotes(page_text(rel,152)[0]))
    assert len(notes)==1
    r('\\footnote{'+notes[0][2]+'} ','','after duality display','There is no footnote in the print. The justified subscript correction is recorded separately.','structure')
    r(r'\operatorname{Hilb}',r'\underline{\operatorname{Hilb}}','three Hilbert scheme names','All three names are straight underlined.',count=3)
    r('\\operatorname{Div}_{X/S}=\n','\\underline{\\operatorname{Div}}_{X/S}=\n','decomposition left side','The left side denotes the scheme and has a straight underline.')
    r(r'\operatorname{Div}^{Q}',r'\underline{\operatorname{Div}}^{Q}','decomposition summand','The summand is straight underlined.')
    r(r'\operatorname{Div}_{X/S}',r'\text{\uwave{Div}}_{X/S}','three remaining divisor names','These are the functors, marked with a wavy underline.',count=3)
    r(r'\operatorname{Pic}_{X/S}',r'\text{\uwave{Pic}}_{X/S}','three Picard functor names','The three functor names are wavy underlined; the absolute group Pic(X/S) remains unmarked.',count=3)
    r(r'\mathbf Q',r'\text{\uwave{Q}}','two rational fields','The ground field Q is ordinary upright with a wavy underline.',count=2)
    r(r'\coprod_{',r'\coprod\limits_{','disjoint union index','The polynomial index is placed below the union sign.')
    r("d'ouverts disjoints quasi-projectifs sur","d'ouverts disjoints \\uline{quasi-projectifs} sur",'quasi-projectivity conclusion','Only quasi-projectifs is straight underlined.')
    r(r'\longmapsto',r'\rightsquigarrow','divisor-to-line-bundle assignment','The assignment arrow is wavy.')
    r(r'\longrightarrow',r'\to','three ordinary arrows','All ordinary arrows are short.',count=3)
    r(r'\xrightarrow{\sim}',r'\overset{\sim}{\to}','two isomorphism arrows','The tilde is over a short arrow.',count=2)
    r('i.e.','i. e.','reference to 2.4','The initials are spaced.')
    r('« Künneth »',"``Künneth''",'cohomology reference','The name is in ordinary double quotes.')
    r(r'\mathcal Q',r'\mathfrak Q','three coherent module signs','The handwritten coherent module is Gothic Q, distinct from ordinary polynomial Q and wavy field Q.',count=3)
    r(r'\operatorname{Hom}_{\mathcal O_S}',r'\underline{\operatorname{Hom}}_{\mathcal O_X}','duality display','The sheaf Hom is straight underlined and the printed coefficient subscript is O_X.')
    if tree=='fr':
        r(r'\underline{\operatorname{Hom}}_{\mathcal O_X}',r'\underline{\operatorname{Hom}}_{\mathcal O_S}','duality display','Both Q and O_S are modules on S; their sheaf Hom is over O_S. O_X is a sheaf on the wrong space. Retain this justified correction from the supplied edition, without its unprinted footnote.','misprint of the original')
    upright_page(rel,layer,'232-152')
event('232-4.1','used and rechecked in this run','The relative Cartier condition gives an open subfunctor of the Hilbert functor by the proper-image argument checked on p. 151. Expose 221 supplies the Hilbert scheme for projective X/S. Taking that open yields Div, and intersecting it with the projective fixed-Hilbert-polynomial loci yields disjoint quasi-projective opens. The two Div signs in the decomposition denote schemes, unlike the wavy functor signs.','232, p. 152, proposition 4.1 and following decomposition')
event('232-4-Abel-fibre-quotient','targeted proof check','Under the universal O_S to f_*O_X isomorphism, proposition 2.4 after any base change says that equality of the relative Picard classes of L(D) and L means equality up to a line bundle from the base. Such a line bundle is Zariski locally trivial. Locally a divisor is a fibrewise regular section of L modulo a base unit, and local divisor ideals glue uniquely. Thus the fibre sheaf is f_*L-star/O_S-star. Its compatibility with base change is interpreted as the same construction for the pulled-back family, not as a false assertion that ordinary f_*L always commutes with base change.','232, p. 152, paragraph after (+)')
event('232-4-cohomology-module','targeted proof check','With the finite locally free cohomology-complex theorem as background, represent H^0(X,L tensor M) locally by the kernel of K^0 tensor M to K^1 tensor M, choosing the complex in nonnegative degrees using flatness. Set Q=coker((K^1) dual to (K^0) dual); Hom(Q,M) is this kernel for every M. This identifies the correct base ring O_S, explains base-change compatibility of Q, and gives uniqueness and gluing through the represented functor. The printed O_X subscript is ill-typed and is corrected only in corrected French. Existence of the finite free complex itself is not independently reproved here.','232, p. 152, final display and its preceding paragraph')
event('232-4-universal-H0','carried as background without fault found','For proper flat X/S with geometrically integral fibres, O_S maps isomorphically to f_*O_X universally. This is the cohomology-and-base-change input cited in the text as [2], III, paragraph 7; no separate complete proof is claimed on this page.','232, p. 152, middle paragraph')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='232-152')
record_page('232',152,'Compared both French layers, entry lines 459-511, with scan leaf 11 at 400 dpi and all three enlarged bands. Read proposition 4.1, the polynomial decomposition, the Abel map (+), its fixed-class fibre and the coherent-module duality construction through the page-end fragment.\n\nRestored the straight scheme names, wavy functors and rational fields, Gothic coherent module Q, exact emphasis, arrow forms, underlined sheaf Hom and quotation marks. Removed the unprinted editorial footnote. Restored its printed O_X subscript in the diplomatic layer and retained the mathematically necessary O_S in corrected French. Rechecked 4.1 from the already examined open-locus argument, the quotient description and the algebra of the cohomology-module construction, with its existence theorem explicitly background.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
