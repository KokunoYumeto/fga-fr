from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-267',line,'4a-c',
                'Scan leaf 20 at 400 dpi and all three enlarged bands: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,267)
    for a,b,body in list(footnotes(s)):
        r(s[a:b],'','editorial notes','No footnotes occur in the printed page.','structure')
    if tree=='fr':
        restorations=[
            (r"$\mathcal G_{s'}$ ($s'\in S'$)",r"$\mathcal G_s$ ($s'\in S'$)",'1-degree fiber index'),
            ("([3], IV) sur $S'$","([3], IV) sur $S$",'smooth base'),
            ("normal sur $S'$","normal sur $S$",'normal base'),
            ("$k(s')$","$k(s)$",'residue field'),
            ("des $S'$-intersections","des $k$-intersections",'relative intersection prefix'),
            ("locales dans $X'$ relativement à $S'$","locales dans $X$ relativement à $S$",'ambient space and base'),
            ("locales dans les $X'_{s'}$","locales dans les $X_{s'}$",'fiber shorthand'),
            (r'le cas de $\operatorname{Hom}_S(X,Y)$',r'le cas de $\operatorname{Hom}_S(X,X)$','Hom reduction'),
            (r"des sous-préschémas $\Gamma$ de $Z'$",r"des sous-préschémas $\Gamma$ de $Z$",'graph ambient space')
        ]
        for a,b,line in restorations:
            r(a,b,line,'Restore the exact printed wording before deciding each supplied correction. In the final fiber shorthand X_s-prime is already the fiber over the S-point s-prime, so its additional prime is unnecessary.')
    r('est quasi-projectif sur','est \\\\uline{quasi-projectif} sur','4a hypothesis','Only quasi-projectif is straight-underlined.')
    r('conclusions le mot','conclusions les mots','4a wording','The print has the plural les mots.')
    r('« projectif » par « quasi-projectif »','"projectif" par "quasi-projectif"','4a quotation marks','The print uses ordinary double quotation marks; the handwritten insertion is retained as the same words.')
    r("dont le\nsupport est propre sur $S'$",r"\uline{dont le support est propre sur} $S'$",'proper support condition','The prose from dont through sur is straight-underlined.')
    r(r'\underline{\operatorname{Quot}}',r'\mathop{\text{\uwave{Quot}}}\nolimits','two functor signs','Both functor signs have wavy underlines.',count=2)
    r(r'\operatorname{Quot}',r'\underline{\operatorname{Quot}}','two scheme signs','Both representing-scheme signs have straight underlines.',count=2)
    r(r'aux quotients $\mathcal G$ de',r'aux quotients $G$ de','4b first quotient','The first G in 4b is ordinary, unlike the script G in 4a and 2 degrees.')
    r("plats sur $S'$,\ntoutes sortes","plats sur $S'$\ntoutes sortes",'4b punctuation','There is no comma between S-prime and toutes.')
    r(r"$\mathcal G_s$ ($s'\in S'$)",r"$G_s$, ($s'\in S'$)",'1-degree module and punctuation','The G is ordinary and followed by a comma before the parenthesis.')
    r('un préschéma simple\n','un préschéma \\\\uline{simple}\n','2-degree smoothness','Only simple is straight-underlined.')
    r('resp. normal sur','resp. \\\\uline{normal} sur','2-degree normality','Only normal is straight-underlined.')
    r('i.e.','i. e.','three explanatory abbreviations','Each printed abbreviation is spaced.',count=3)
    r('« sur $k(s)$ »','"sur $k(s)$"','geometric normality quotes','The printed quotation marks are ordinary double quotes.')
    r('de nature\ncohomologique sur','de nature\ncohomologiques sur','cohomological conditions','The print has the plural cohomologiques.')
    r(r"sur les Modules $\mathcal G_{s'}$ induits",r"sur les Modules $G_{s'}$ induits",'cohomological fiber module','The G is ordinary, with its printed prime retained.')
    r(r'de $\underline{\operatorname{Quot}}_{\mathcal F/X/S}$ est',r'de $\underline{\operatorname{Quot}}_{\mathcal F/X/S}$, est','intersection sentence','The print has a comma before est.')
    r(r'\operatorname{Hom}',r'\underline{\operatorname{Hom}}','three Hom schemes','The three Hom signs have straight underlines.',count=3)
    r(r'\operatorname{Isom}',r'\underline{\operatorname{Isom}}','Isom scheme','The Isom sign has a straight underline.')
    r(r'\Pi_{X/S}',r'\prod\limits_{X/S}','three restriction-of-scalars signs','The product-shaped operator has X/S directly beneath it.',count=3)
    r("Comme on a\n\\[\n\\underline{\\operatorname{Hom}}_S(X,Y)=\\prod\\limits_{X/S}((X\\times_SY)/X),\n\\]\nle cas",
      r'Comme on a $\underline{\operatorname{Hom}}_S(X,Y)=\prod\limits_{X/S}((X\times Y)/X)$, le cas',
      'Hom identity','The identity runs inline. The product X times Y has no base subscript in the print; the ambient S context makes this harmless shorthand.','structure')
    r(r'\longrightarrow',r'\to','two final arrows','Both arrows are short.',count=2)
    if tree=='fr':
        repairs=[
            (r"$G_s$, ($s'\in S'$)",r"$G_{s'}$, ($s'\in S'$)",'1-degree fiber index','The point quantified in this family is s-prime in S-prime; its fiber module needs that same index.'),
            ("([3], IV) sur $S$","([3], IV) sur $S'$",'smooth base','The parameterized closed subscheme Y is a family over the test base S-prime, not just over S.'),
            (r"\uline{normal} sur $S$",r"\uline{normal} sur $S'$",'normal base','The geometric normality condition belongs to the test family Y over S-prime.'),
            ("$k(s)$","$k(s')$",'residue field','The geometric fiber criterion is over the residue field of the explicitly quantified point s-prime.'),
            ("des $k$-intersections","des $S'$-intersections",'relative intersection prefix','There is no field k specified in this relative family; the intended relative base in this condition is S-prime.'),
            ("locales dans $X$ relativement à $S$","locales dans $X'$ relativement à $S'$",'ambient space and base','The closed immersion being tested is Y into X-prime over S-prime; Y need not be a closed subscheme of X itself.'),
            ('de nature\ncohomologiques sur','de nature\ncohomologique sur','adjective agreement','The adjective in de nature cohomologique agrees with singular nature.'),
            (r'le cas de $\underline{\operatorname{Hom}}_S(X,X)$',r'le cas de $\underline{\operatorname{Hom}}_S(X,Y)$','Hom reduction','The reduction is for the general Hom scheme just introduced and expressed by the preceding identity; its second argument is Y.'),
            (r"des sous-préschémas $\Gamma$ de $Z$",r"des sous-préschémas $\Gamma$ de $Z'$",'graph ambient space','A section of Z-prime over X-prime has its graph inside Z-prime. Its projection to Z need not be an immersion.')
        ]
        for a,b,line,why in repairs:
            r(a,b,line,why,'misprint of the original')
    upright_page(rel,layer,'221-267')
event('221-4a-quasi-projective','targeted consequence check','Embed X as an open subscheme in a projective closure and extend the coherent ambient sheaf across that closure. A quotient supported properly over the base extends by zero coherently and is exactly a quotient with support disjoint from the boundary. The open condition checked on p. 266 therefore gives the quasi-projective variant, with proper support retained as an essential hypothesis. Coherent extension and the projective theorem are used as recorded background inputs.','221, p. 267, first paragraph')
event('221-4b-1','carried as background without fault found','Read the openness assertion for allowed dimensions of associated prime cycles in a proper flat family. Corrected French uses the actual test point s-prime. No independent proof of the associated-cycle semicontinuity theorem is claimed.','221, p. 267, item 1 degree')
event('221-4b-2','carried as background without fault found','Read the smooth, geometrically normal and relative local-complete-intersection loci. The test family is Y inside X-prime over S-prime, which justifies the base and ambient-space corrections. The final X_s-prime already denotes X fibered with the residue field of the S-point s-prime, so the supplied additional prime is withdrawn as unnecessary notation normalization. Openness theorems and their proper-family use are carried as background, not re-proved.','221, p. 267, item 2 degrees')
event('221-4b-conjunction','targeted consequence check','For a finite conjunction, the intersection of its representing opens is open and has the required functor of points. The unqualified word conjunction is read in this finite sense; arbitrary infinite intersections would not be open in general. The finite-etale rank-r example combines the zero-dimensional proper flat locus, smoothness and the locally constant rank. No arbitrary infinite-conjunction theorem is asserted.','221, p. 267, paragraph after item 2 degrees')
event('221-4c-graph','targeted correspondence check','A section of Z-prime -> X-prime gives a graph in Z-prime isomorphic to X-prime; conversely the inverse of an isomorphic projection from such a subscheme gives exactly one section. Separatedness of Z over X is preserved by base change and makes the section a closed immersion. Hom_S(X,Y) is the section functor for X times_S Y -> X. This checks the correspondence and identifies the printed Hom(X,X) and ambient Z slips. Representability continues on the next page.','221, p. 267, section 4c')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-267')
record_page('221',267,'Compared printed French entry lines 868-924 and corrected French entry lines 869-925 with scan leaf 20 at 400 dpi and all three enlarged bands. Read the quasi-projective extension, the entire list of open conditions and the beginning of the Hom/section construction.\n\nRestored les mots, the printed commas and absent comma, ordinary double quotes, the proper-support and smooth/normal underlines, ordinary versus script G, wavy functor signs and straight scheme signs, product operators with limits beneath them, the inline Hom identity and both short arrows. Removed all editorial footnotes. Adjudicated every supplied correction against the enlarged image and the test-base types: retain the necessary point/base/ambient-space and Hom argument repairs; withdraw the needless prime in the final X_s-prime, which is valid fiber shorthand. Printed French retains cohomologiques; corrected French repairs its agreement with nature. The graph correspondence and finite-conjunction consequence have explicit checks; the geometric openness theorems are recorded as background.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
