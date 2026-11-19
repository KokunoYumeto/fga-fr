from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/212.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'212-101',line,'1. Effective relations and epimorphisms','400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 r("couple d'équivalence: il", "couple d'équivalence : il",'opening colon',why='A space precedes the printed colon.')
 r(r'\longrightarrow',r'\to','four arrows',count=4,why='All four printed arrows have ordinary length.')
 r('« objet au-dessus de $Y$ »',r'\fquote{objet au-dessus de $Y$}','quoted description',why='Ordinary double quotation marks surround the description.')
 r('R(f)=',r'\text{\uwave{R}}(f)=','kernel-pair display',why='The R in R(f) has a wavy underline; the other relation objects on this page are plain R.')
 r("couple de morphismes $(p_1,p_2)$", "couple de morphismes $(p_1;p_2)$",'first pair in effective-pair definition',why='The enlarged middle band has a semicolon between the two projection names in this occurrence; the other pairs use commas.')
 for old in [r'\emph{associé}',r"\emph{couple d'équivalence effectif}","\\emph{relation d'équivalence\neffective}","\\emph{épimorphisme\neffectif}",r'\emph{quotient effectif}']:
  r(old,old.replace(r'\emph{',r'\uline{'),'defined term '+old,why='The printed emphasis is a straight underline.')
 r(r'le conoyau $X/(p_1,p_2)=Y$ existe;',r'le conoyau $X/(p_1,p_2)=Y$ existe','effective-pair condition (i)',why='There is no terminal semicolon in the printed first list.')
 r(r'le produit fibré $X\times_Y X$ existe;',r'le produit fibré $X\times_Y X$ existe','effective-pair condition (ii)',why='There is no terminal semicolon in this condition; the second list retains its printed semicolons.')
 r(r'\S~2.3',r'\S~2. 3','strict-epimorphism reference',why='The printed reference has a space after the internal period. Its number is retained: 190 A.2.2 defines strict epimorphisms, while adjacent A.2.3 discusses universally strict ones; the intended reference is not unambiguous enough to emend.')
 r('« correspondance galoisienne »',r'\fquote{\uline{correspondance galoisienne}}','last quoted term',why='Ordinary quotes surround straight-underlined words.')
 r('suivante:', 'suivante :','last colon',why='Space before the printed colon.')
 upright_page(rel,layer,'212-101')

event('212-1-kernel-pair','targeted proof check','Applying Hom(T,-) to R(f)=X times_Y X gives precisely the pairs of T-points with equal images under f. Equality of images is reflexive, symmetric and transitive, so the two projections form an equivalence pair. A pair isomorphic to this kernel pair has the same property. This verifies the implication built into the effective-pair definition without assuming the category itself is a category of sets.','212, p. 101, kernel-pair display and effective-pair definition')
event('212-1-effective-strict','targeted proof check','An effective epimorphism is a coequalizer of its kernel pair and hence an epimorphism. Any map compatible with every pair identified by f is in particular compatible with the kernel pair, and so factors uniquely through f: it is strict. Conversely, when the kernel pair exists, every pair beta1,beta2 with f beta1=f beta2 factors through it. A map equalizing its two projections therefore satisfies the strict-epimorphism factorization criterion, proving that a strict epimorphism with kernel pair is effective. The printed reference to 190 A.2.3 is retained conservatively; the exact definition and kernel-pair discussion are in A.2.2 on p. 304 and A.2.3 follows on p. 305.','212, p. 101, last two paragraphs; 190, pp. 304–305, definitions 2.2–2.3')
record_page('212',101,r'''Compared sources/fr_printed/fr/212.tex and sources/fr/fr/212.tex entry lines 91–138 against scan leaf 4 at 400 dpi, full page and top, middle and bottom enlarged bands. Read all subscripts, fibre-product bases, the two three-condition definitions, every arrow, the wavy underline on R(f), and the printed 2. 3 reference.

Both layers restore ordinary arrows and quotation marks, the local wavy R, straight underlines, the semicolon in the first pair of the effective-pair definition, the absence of semicolons in its first two conditions, and upright mathematical letters. The semicolons in the second list remain. The printed cross-reference 2.3 is retained with its typographic spacing: A.2.2 is the exact earlier definition, but A.2.3 immediately continues the subject, so an intended-number correction is not established. There is no mathematical difference between the two French layers on this page.

Verified that a kernel pair defines a pointwise equivalence relation and that effectiveness is equivalent to strict epimorphy when the kernel pair exists, by their universal properties.''')
from update_record_counts import update
update()
