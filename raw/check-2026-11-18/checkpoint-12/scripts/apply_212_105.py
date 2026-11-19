from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/212.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'212-105',line,'3. Free actions; 4. Groupoids','400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 r(r'p_1=\operatorname{pr}_2',r'p_1=\operatorname{pr}_1','opening projection: printed',why='The enlarged top band clearly has subscript 1 after pr.')
 if tree=='fr':
  r(r'p_1=\operatorname{pr}_1',r'p_1=\operatorname{pr}_2','opening projection: corrected',kind='misprint of the original',why='The displayed domain on p. 104 is G times X and the target is X. Its first projection lands in G, whereas the second lands in X. The subsequent pair is (x,gx), requiring pr_2. The existing unmarked correction is confirmed.')
 r(r'\simeq',r'\sim','point-product identification',why='The print has a single tilde, without an equality bar underneath.')
 r(r'\longrightarrow',r'\to','two arrows',count=2,why='The arrows have ordinary length in the scan.')
 r('i.e.', 'i. e.','three abbreviations',count=3,why='The abbreviated words are separated by spaces in print.')
 r(r'i. e. si $g\in G(T)$',r'i. e. $g\in G(T)$','stabilizer condition introduction',why='There is no si before g in this occurrence.')
 r("implique que $g$ est l'élément unité", 'implique $g=$ élément unité','stabilizer conclusion wording',why='The printed conclusion is the compressed formula g = élément unité, not an expanded prose sentence. Both layers retain it.')
 r(r'\emph{opère librement sur $X$} (ou',r'\uline{opère librement} sur $X$, (ou','free-action emphasis',why='The underline ends before sur X, and a comma precedes the parenthesis.')
 r(r'\emph{$\mathcal C$-espace principal sous $G$}',r'$\mathcal C$\uline{-espace principal sous} $G$','principal-space emphasis',why='The category has a wavy underline, the prose beginning with the hyphen is straight-underlined, and G is outside it.')
 old="\\emph{relation\nd'équivalence définie par le groupe $G$ opérant librement sur $X$}"
 new="\\uline{relation\nd'équivalence définie par le groupe} $G$ opérant librement sur $X$"
 r(old,new,'relation-name emphasis',why='The underline ends at groupe; the following words opérant librement sur are not underlined.')
 for term in ['librement','monomorphisme','groupoïde','objets','flèches']:
  r(r'\emph{'+term+'}',r'\uline{'+term+'}','defined '+term,why='The printed emphasis is a straight underline.')
 r("« l'image »",r"\fquote{l'image}",'quoted image',why='Ordinary double quotes surround this word.')
 r('ou plus précisément par','ou plus précisément, par','image-relation parenthesis',why='A printed comma follows précisément.')
 r(r'$\operatorname{pr}_i$), on',r'$\operatorname{pr}_i$) on','end of image-relation parenthesis',why='The scan has no comma after the closing parenthesis.')
 r(r"\subsection*{4. Pré-relations d'équivalence}",r"\subsection*{\textnormal{4. \uline{Pré-relations d'équivalence}.}}",'section 4 heading',why='Roman underlined title with a final period outside the underline.')
 r('structures suivantes:', 'structures suivantes :','last colon',why='A space precedes the colon.')
 s,_,_=page_text(rel,105)
 r(r'\mathcal C',r'\text{\uwave{C}}','category letters',count=s.count(r'\mathcal C'),why='Each category C has a wavy underline.')
 upright_page(rel,layer,'212-105')

event('212-3-projection-index','targeted proof check','The action pair has common domain G times X and common target X. Thus p1 is the second projection, while p2 is the action. The printed pr_1 instead has target G and is ill-typed for arbitrary G and X. Corrected only in the corrected French layer to pr_2; the supplied unmarked correction is independently confirmed.','212, p. 105, first display; p. 104, final display')
event('212-3-free-action','targeted proof check','The point map is (g,x) to (x,gx). Its image is always the orbit equivalence relation on X(T). It is injective exactly when stabilizers are trivial: equality of (x,gx) and (x,hx) is equivalent to h inverse g fixing x. Therefore the original pair represents the equivalence graph bijectively exactly for a free action. Yoneda equates injectivity for every T with p being a monomorphism. The term espace principal here asserts freeness only; no nonemptiness, transitivity or covering condition is added to the historical definition.','212, p. 105, first paragraph')
event('212-3-image-not-equivalence','targeted proof check','Concrete example verifying the warning in the category of finite k-schemes, char(k) not 2: let G be the constant group of order two acting on X=Spec(k[t]/t^2) by t to -t. The map G times X to X times X has scheme-theoretic image R=Spec(k[x,y]/(x^2,y^2,xy)), because evaluation at y=x and y=-x has kernel (xy). In this finite category every subobject is a finite monomorphism, hence a closed immersion, so R is the smallest subobject through which the map factors. But R times_X R has ring k[x,y,z]/(x^2,y^2,z^2,xy,yz), where xz is nonzero. The pair of outer projections does not factor through R, whose defining equation would require xz=0. Thus the image fails transitivity even though the group action is genuine. This is a hand-checked polynomial calculation, not a claim of an executed formal certificate.','212, p. 105, image paragraph')
event('212-3-lost-isotropy','targeted proof check','Replacing the action groupoid by its image forgets stabilizers even when that image is an equivalence relation: a nontrivial group acting trivially on a one-point object has diagonal image, the same image as the trivial group, but different automorphism groups in its action groupoid. This explains the need to retain the original pair and composition structure in section 4. The discussion is a structural motivation, not an assertion that the categorical coequalizer alone remembers isotropy.','212, p. 105, final paragraph of section 3')
record_page('212',105,r'''Compared sources/fr_printed/fr/212.tex and sources/fr/fr/212.tex entry lines 268–315 against scan leaf 8 at 400 dpi, full page and all three enlarged bands. Inspected the printed pr_1, every p and pr index, the single-tilde identification, all G(T) and X(T) arguments, the scalar action dot, both quotient slash directions, and the precise underline endpoints.

The printed layer restores pr_1; the corrected layer keeps pr_2 with an explicit misprint row, since the projection must land in X. Both layers restore the single tilde, ordinary arrows, i. e. spacing, the abbreviated stabilizer condition, selective underlines, ordinary quotes, two parenthetical comma details, the roman section heading and its period, and upright variables.

Verified the free-action criterion and its Yoneda reformulation. Checked an explicit finite-scheme example in which the image of a group action fails transitivity, and the trivial-action example showing loss of isotropy. The groupoid definition continues on p. 106.''')
from update_record_counts import update
update()
