from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-268',line,'4c representability and polarizations',
                'Scan leaf 21 at 400 dpi, all three enlarged bands and a 3x arrow-target crop: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,268)
    for a,b,body in list(footnotes(s)):
        r(s[a:b],'','agreement note','The print has no footnote.','structure')
    if tree=='fr':
        r(r'Soit $\mathcal L$',r'Soient $\mathcal L$','introduction of two line bundles','Withdraw the supplied singular normalization: the printed plural introduces the paired objects L and M via resp.; this harmless compressed construction does not force a substantive correction.')
    r(r'\Pi_{X/S}',r'\prod\limits_{X/S}','restriction of scalars','The product-shaped sign has its X/S limit beneath it.')
    for name,n in [('Hilb',3),('Hom',7),('Isom',1),('Imm',1)]:
        r(r'\operatorname{'+name+'}',r'\underline{\operatorname{'+name+'}}','scheme signs '+name,'The scheme signs are straight-underlined.',count=n)
    s,_,_=page_text(rel,268)
    start=s.index('lorsque ')
    end=s.index(' Lorsque $X$ et $Y$')
    r(s[start:end],underline_prose(s[start:end]),'first two representability conclusions','All prose in the first two sentences is straight-underlined. The next Lorsque sentence is not emphasized.')
    r(r'\longrightarrow',r'\to','two morphism arrows','Both arrows are short. The tight crop confirms the prime attached to the upper right arm of Y in X-prime to Y-prime; that prime is retained.',count=2)
    for a,b in [('« polarisée »','"polarisée"'),('« vrai »','"vrai"'),('« défini sur $k$ »','"défini sur $k$"')]:
        r(a,b,'quotation marks','The print uses ordinary double quotation marks.')
    old="\\fsection{5}{Étude différentielle des schémas de Hilbert}\n\nElle découle du résultat suivant :\n\n\\src{269}"
    new="\\src{269}\n\\fsection{5}{Étude différentielle des schémas de Hilbert}\n\nElle découle du résultat suivant :"
    replace(rel,old,new,layer,'221-268','boundary after ancien style','page boundary','Scan leaf 21 at 400 dpi and enlarged bottom band: the page ends after ancien style. The section-5 heading and its introductory sentence must follow the next page marker. Their detailed reading is reserved for page 269.',kind='structure',full=True)
    upright_page(rel,layer,'221-268')
event('221-4c-representability','carried as background without fault found','Read the section, Hom, Isom and immersion representability assertions and their open embeddings into Hilbert or Hom schemes. The first two underlined conclusions retain their distinct hypotheses: proper flat X for sections with quasi-projective Z, and projective flat X for Hom with quasi-projective Y. The subsequent Isom sentence continues with the standing flatness of X. The relevant openness theorem for isomorphisms in proper flat-source families is a background input, not independently re-proved here.','221, p. 268, first paragraph')
event('221-4c-Hilbert-polynomial','targeted consequence check','On the graph of g, the exterior product L tensor M restricts to L tensor g-star M. Thus the Hilbert polynomial of the graph is exactly the Euler characteristic in the displayed formula, interpreted fiberwise over each point of S. For a general base the displayed chi must be the relative, fiberwise Euler characteristic; no absolute Euler characteristic over an arbitrary base is being inferred. The open-and-closed fixed-polynomial decomposition then restricts from Hilbert to Hom.','221, p. 268, second paragraph and display')
event('221-4c-Matsusaka','carried as background without fault found','Read the historical comparison with polarized automorphism groups and the distinction between the representing scheme and its reduced classical group over an algebraically closed field. No detailed reconstruction of Matsusaka theorem is claimed.','221, p. 268, final paragraph')
event('221-4c-nilpotent-base-change','targeted algebraic check','The indicated obstruction over imperfect fields is real: for k=F_p(t), A=k[u]/(u^p-t) is a field and has zero nilradical, but over K=k(t^(1/p)) it becomes K[v]/(v^p), with nonzero nilradical (v). That nilradical cannot descend to an ideal of the field A. This directly checks the stated failure of nilpotent reduction to descend under arbitrary field extension; it is an illustrative algebra calculation, not a claim that this specific A is an automorphism group.','221, p. 268, final paragraph')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-268')
record_page('221',268,'Compared printed French entry lines 920-968 and corrected French entry lines 921-969 with scan leaf 21 at 400 dpi and all three enlarged bands. A 3x arrow-target crop confirms the overinked Y-prime. Read all representability, fixed-polynomial and automorphism-group paragraphs; the page ends after ancien style, before section 5.\n\nRestored the product operator with its lower limit, all straight scheme underlines, the emphasis of the first two conclusions, two short arrows and ordinary double quotes. Moved the page-269 marker before the section-5 heading and introductory sentence, whose content is to be read next. Removed the unprinted agreement note and withdrew the supplied Soient-to-Soit normalization: the paired introduction is harmless mathematical prose. The graph-polarization formula was checked fiberwise, and an explicit purely inseparable extension verifies the stated nilradical obstruction. The representability and historical inputs remain identified as background.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
