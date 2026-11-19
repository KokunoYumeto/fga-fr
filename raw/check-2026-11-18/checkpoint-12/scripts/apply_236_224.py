from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'236-224',line,'1.1, 1.2',
                'Scan leaf 5 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    r('stables par la multiplication','stable par la multiplication','opening agreement','The print has singular stable.')
    r('$G$, ce qui\n', '$G$, de qui\n','opening conjunction','The printed letter is d in de qui, not c.')
    if tree=='fr':
        r('stable par la multiplication','stables par la multiplication','opening agreement','The adjective modifies the plural parties.','misprint of the original')
        r('$G$, de qui\n','$G$, ce qui\n','opening conjunction','The relative clause resumes the preceding assertion, requiring ce qui; de qui cannot be its grammatical subject.','misprint of the original')
    r("il n'existe pas en\ngénéral de sous-préschéma en groupes de $G$ dont l'ensemble sous-jacent soit\n$G^\\circ$", "\\uline{il n'existe pas en général de sous-préschéma en groupes de} $G$ \\uline{dont l'ensemble sous-jacent soit} $G^\\circ$",'nonrepresentability warning','The whole prose assertion is straight underlined, with the mathematical names outside the underline.')
    r('du point de vue « spécialisations »,\nl\'équivalence numérique se comporte de façon plus satisfaisante que\nl\'équivalence algébrique.', '\\uline{du point de vue ``spécialisations\'\', l\'équivalence numérique se comporte de façon plus satisfaisante que l\'équivalence algébrique}.','specialization comparison','The print uses ordinary double quotes and underlines this complete prose span.')
    r('sont\nlocalement constructibles.','\\uline{sont localement constructibles}.','1.1 opening assertion','These words alone have a straight underline.')
    r('$S$, donc\nfermé dans $G$.','$S$ donc\nfermé dans $G$.','1.1(i)','There is no comma before donc.')
    r('i.e.','i. e.','1.1(iii)','The abbreviation has an intervening space.')
    r('et que, pour tout entier','et que pour tout entier','1.1(iv)','The print has no comma after que.')
    r('Supposons que $S\\neq\\varnothing$,','Supposons que $S$ soit $\\neq\\varnothing$,','1.2 hypothesis','The printed word soit is present between S and the nonempty sign.')
    s,_,_=page_text(rel,224)
    a=s.index('Supposons que $S$ soit'); b=s.index("\n\nPour prouver le lemme",a)
    old=s[a:b]
    r(old,underline_prose(old),'1.2 statement','All statement prose is straight underlined, with symbols and punctuation outside the emphasis.')
    r(r'\mathcal O_{S,\eta}=A',r'\mathcal O_{S,s}=A','1.2 proof, second local ring','The second local-ring subscript is printed lowercase s, unlike the eta in the preceding base-change formula.')
    if tree=='fr':
        r(r'\mathcal O_{S,s}=A',r'\mathcal O_{S,\eta}=A','1.2 proof, second local ring','The ring A is the coordinate ring of S prime=Spec O_(S,eta) defined in the preceding clause. It is Artinian because eta is a generic point; a general local ring O_(S,s) need not be Artinian. The repeated ring therefore requires eta.','misprint of the original')
    r('sous-schéma en groupes ouvert\n$G\'{}^\\circ$ de type fini sur $A$', 'sous-schéma en groupes \\uline{ouvert}\n$G\'{}^\\circ$ \\uline{de type fini sur} $A$','1.2 proof, Artinian-base subgroup','Only ouvert and de type fini sur have straight underlines.')
    r("\\longrightarrow S$ ; on trouve", "\\longrightarrow S$, on trouve",'1.2 proof, base-change punctuation','The print has a comma after the base-change arrow.')
    r(r'\longrightarrow',r'\to','five arrows','The arrows are short.',count=5)
    upright_page(rel,layer,'236-224')
event('236-1-relative-subgroup-warning','carried as background without fault found','The author distinguishes fibrewise multiplication-stable subsets from actual subgroup subschemes and cautiously says that an arbitrary G zero need not admit such a scheme structure. The numerical-versus-algebraic comparison is motivational and depends on the following theorem and later Picard interpretations. No general counterexample or proof of that warning has yet been established in this reading.','236, p. 224, opening paragraph')
event('236-1.1','carried as background without fault found','Read the complete theorem and checked the assignment of all four loci and hypotheses: relative quasi-compactness for G zero; proper fibres plus separated ambient G for its properness; openness of G tau; the equal-characteristic qualification for closedness of G sigma; universal openness at G sigma for its projection; and the prime-to-p power-map openness criterion for G rho. These are statements at this point, with proof deferred to the subsequent pages. Properness here concerns the locus in the sense used by the text, not an unannounced representable subgroup structure.','236, p. 224, theorem 1.1(i)-(iv)')
event('236-1.2-generic-local-ring','targeted proof check','For a generic point eta of a locally Noetherian scheme, O_(S,eta) is a zero-dimensional Noetherian local ring and hence Artinian. Over this ring the underlying space of G prime equals that of its sole fibre; the identity component therefore gives an open subgroup whose underlying space is quasi-compact by the preceding field case. Local finite type then makes it finite type. The next spreading step requires finite-presentation limit arguments and is continued on p. 225. This also confirms that the second local ring is O_(S,eta), not the printed O_(S,s); for example the local ring of the affine line at a closed point is not Artinian.','236, p. 224, lemma 1.2 and opening proof')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='236-224')
record_page('236',224,'Compared both French layers, entry lines 140-193, with scan leaf 5 at 400 dpi, the full page and three enlarged bands. Read the introductory distinction between loci and subgroup schemes, all four parts of theorem 1.1, lemma 1.2 and its proof through the page-ending sentence fragment.\n\nRestored the printed singular stable and de qui, all prose emphasis, ordinary quotes, exact commas, spaced i. e., the missing word soit in the lemma statement, the printed s in the second local-ring subscript, short arrows and upright variables. Corrected French alone changes stable to stables, de qui to ce qui and the second ring subscript s to eta. Checked the Artinian generic-local-ring step and the finite-type open subgroup over it. The theorem and the remainder of the spreading proof are not counted as proved before their continuation is read.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
