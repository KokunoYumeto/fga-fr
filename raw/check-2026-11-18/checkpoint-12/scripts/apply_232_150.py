from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/232.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'232-150',line,'3.3, 4',
                'Scan leaf 9 at 400 dpi and all three enlarged bands: '+why,kind=kind,count=count)
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}','six scheme names','Each Pic sign denotes a scheme and is straight underlined, including both abbreviated names in the parenthesis.',count=6)
    r('contient des composantes\nconnexes qui ne sont pas de type fini sur', '\\uline{contient des composantes\nconnexes qui ne sont pas de type fini sur}', 'opening continuation','This entire prose span, ending before S, is straight underlined.')
    r('Néron--Severi','Néron-Severi','Néron-Severi group','The compound uses a short hyphen.')
    r('pour $u$ l\'automorphisme\n\\[\n(x,y)\\longmapsto(x,y+x)\n\\]\nde', 'pour $u$ l\'automorphisme\n$(x,y)\\rightsquigarrow(x,y+x)$ de','shear automorphism','The assignment is inline, with a wavy arrow.','structure')
    r(r'\mathbf Z',r'\text{\uwave{Z}}','three group signs','The integer group is typed Z with a wavy underline.',count=3)
    r('un schéma abélien sur','un schéma \\uline{abélien} sur','associated family','Only abélien is straight underlined.')
    r('une composante connexe isomorphe à\n\\[\nP\\times\\underline{\\operatorname{Pic}}^{0}_{X_0/k},\n\\]\n(où','une composante connexe isomorphe à\n$P\\times\\underline{\\operatorname{Pic}}^{0}_{X_0/k}$ (où','connected component','The product is inline and has no comma before the parenthesis.','structure')
    r('comme envisagés dans 3.2.]','comme envisagés dans 3.3.]','bracketed reference','The print refers to 3.3 here.')
    r(r'\fsection{4}{Diviseurs de Cartier relatifs et fibrés projectifs}',r'\fsection{4}{\normalfont\uwave{Diviseurs de Cartier relatifs et fibrés projectifs}.}','section 4 heading','The upright title has a wavy underline and final period.')
    r(r'\emph{diviseur de Cartier}',r'\uline{diviseur de Cartier}','definition','The term is straight underlined.')
    r(r'\mathcal J',r'\mathfrak J','four ideal signs','The handwritten ideal letter is Gothic J.',count=4)
    r('qui est un Module inversible,','qui est un Module \\uline{inversible},','definition of ideal','Only inversible is straight underlined.')
    r('par une section non diviseur de zéro de','par une section \\uline{non diviseur de zéro} de','regular generator','This phrase is straight underlined.')
    r('i.e.','i. e.','two abbreviations','The initials are spaced.',count=2)
    r(r'\longrightarrow',r'\to','two canonical maps','Both arrows are short.',count=2)
    r('essentiellement équivalente à','essentiellement \\uline{équivalente} à','classification of divisors','Only équivalente is straight underlined.')
    r('« diviseur »',"``diviseur''",'inverse construction','The print uses ordinary double quotation marks.')
    if tree=='fr':
        r('comme envisagés dans 3.3.]','comme envisagés dans 3.2.]','bracketed reference','The nonseparated Picard schemes are discussed in remarque 3.2; 3.3 is the present finite-type question. Correct the cross-reference only in corrected French.','misprint of the original')
    upright_page(rel,layer,'232-150')
event('232-3.3-monodromy-example','independent re-proof','For X-zero=E times E and u(x,y)=(x,y+x), take the class of the divisor y=0. Its successive pullbacks are y+n x=0. Intersections with y=0 and y+x=0 give n^2 and (n-1)^2, distinguishing all integer n, including in positive characteristic by the degree formula for multiplication on an elliptic curve. Glue copies indexed by Z of the two opens S-a and S-b, using identity on one connected overlap and a one-step shift on the other. The resulting Z-torsor P is connected and has an infinite discrete geometric fibre. Gluing X-zero by u gives a locally projective abelian scheme. The orbit of the chosen Picard component has trivial stabilizer; identifying each translate with the chosen component gives its associated component as P times Pic-zero. A line bundle over the algebraically closed ground field identifies that chosen component with Pic-zero. The component is connected and not of finite type because its fibre has infinitely many connected components. The standard representability of the Picard scheme of E times E is the background input.','232, p. 150, continuation of remarque 3.3')
event('232-3.3-bracketed-reference','targeted proof check','The bracketed sentence discusses nonseparated Picard schemes, the subject of 3.2 on p. 149. The printed 3.3 points to the present finite-type discussion. Restored 3.3 in the diplomatic layer and retained the justified correction to 3.2 in corrected French. The analogous additional nonseparated examples are not constructed in this paragraph.','232, p. 150, bracketed sentence before section 4')
event('232-4-effective-Cartier-definition','independent re-proof','An invertible ideal J included in O_X is locally generated by one regular element, since a chosen basis of J maps injectively into O_X. Dualizing the inclusion gives the canonical section of J inverse. Conversely, a line bundle L with a regular section s gives an injective dual map L inverse to O_X; its image is an invertible ideal and defines the effective Cartier divisor. In a local trivialization this is the ideal (s), so the two constructions are inverse and glue. The printed restriction to positive divisors is retained and makes the stated definition precise.','232, p. 150, section 4 definition and two displays')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='232-150')
record_page('232',150,'Compared both French layers, entry lines 365-417, with scan leaf 9 at 400 dpi and three enlarged bands. Read the entire monodromy example finishing 3.3, its bracketed qualification, the section 4 heading, effective-Cartier definition and the two canonical-section displays through the final sentence fragment.\n\nRestored straight scheme names and prose emphasis, wavy integer-group signs and assignment, the two inline formulas, Gothic ideal J, spaced abbreviations, short arrows and quotation marks. The printed reference 3.3 is restored in the diplomatic layer; corrected French points to 3.2, where nonseparated examples occur. Reconstructed the infinite-orbit monodromy example and the equivalence between effective Cartier divisors and invertible sheaves with regular sections.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
