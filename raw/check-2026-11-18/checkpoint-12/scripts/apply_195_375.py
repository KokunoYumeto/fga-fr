from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/195.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'195-375',line,'A.5','400-dpi full scan and three enlarged bands. '+why,kind,count=count)
 r(r'des $\Lambda$-algèbres artiniennes)',r'des $\Lambda$-\uline{algèbres artiniennes})','opening defined class',why='The words after Lambda are underlined.')
 r('proposition 3.1.','proposition 3, 1.','opening reference',why='Printed comma-numbered reference.')
 r('catégorie des algèbres topologiques','catégorie des \\uline{algèbres topologiques}','topological algebra description',why='Printed selective underline.')
 r(r'O=\varprojlim_i O_i',r'O=\varprojlim O_i','first limit display',why='No index is printed beneath this limit arrow; retain the implicit index in both layers.')
 r('i.e. dont','i. e. dont','topology characterization',why='Printed abbreviation spacing.')
 r('est linéaire, séparée et\ncomplète','est \\uline{linéaire}, \\uline{séparée} et \\uline{complète}','topology properties',why='The three adjectives are individually underlined.')
 r('algèbre artinienne sur $\\Lambda$','algèbre \\uline{artinienne} sur $\\Lambda$','open quotient condition',why='Printed selective underline.')
 s,_,_=page_text(rel,375)
 m=re.search(r'\\begin\{align\*\}.*?\\end\{align\*\}',s,re.S)
 if not m: raise ValueError('Expected continuous-Hom display')
 display=r'''\begin{align*}
  \symup{F(A)=h'_O(A)}
  &=\text{ensemble des homomorphismes \uline{continus} de }\symup{\Lambda}\text{-algèbres}\\
  &\phantom{=}\text{topologiques }\symup{O\longrightarrow A}\\
  &=\symup{\varinjlim\limits_i\operatorname{Hom}_{\Lambda\text{-algèbres}}(O_i,A)}
\end{align*}'''
 r(m.group(0),display,'continuous-Hom display',kind='structure',why='The scan writes ensemble des homomorphismes, with continus underlined, rather than set braces. Restore the printed three-line arrangement, direct-limit index and absence of a terminal period; letters are upright.')
 for a,b,line in [('composants locaux',r'\uline{composants locaux}','local components'),('schéma formel [2]',r'\uline{schéma formel} [2]','formal scheme'),('est un corps (',r'est un \uline{corps} (','field-valued point'),('soit un anneau noethérien.',r'soit un anneau \uline{noethérien}.','noetherian question')]:
  r(a,b,line,why='Printed selective underline.')
 r('« points »',r'\fquote{points}','point terminology',why='The print uses ordinary double quotation marks.')
 r("si et seulement s'ils sont dominés","si et seulement si ils sont dominés",'same-point criterion',why='The print has unelided si ils.')
 r(r'\mathfrak m)$.)',r'\mathfrak m)$).','algebraically closed residue fields parenthesis',why='The final period follows the closing parenthesis.')
 r("un anneau quotient d'un anneau de\nséries formelles", "un \\uline{anneau quotient d'un anneau de séries formelles}",'power-series quotient assertion',why='Printed underline on the quoted phrase.')
 r('« nombres\nduaux »',r'\fquote{nombres duaux}','dual-number terminology',why='The print uses ordinary double quotation marks.')
 r("l'homomorphisme d'augmentation ; il", "l'homomorphisme d'augmentation, il",'augmentation punctuation',why='Printed comma, not semicolon.')
 r(r'F(\varepsilon):F(I_A)\longrightarrow F(A),',r'F(\varepsilon):F(I_A)\longrightarrow F(A)','last display punctuation',why='No terminal comma is printed.')
 if tree=='fr_printed':
  r('cas où $\\Lambda$ est un\ntel anneau local complet','cas où $A$ est un tel anneau local complet','reduction of the base ring',why='The printed letter is A, whereas the discussion is reducing the base Lambda.')
 s,_,_=page_text(rel,375)
 r(r'\mathcal C',r'\text{\uwave{C}}','category letters',count=s.count(r'\mathcal C'),why='The category is an upright C with a wavy underline.')
 upright_page(rel,layer,'195-375')

with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 csv.writer(f,delimiter='\t').writerow(['sources/fr/fr/195.tex','French corrected','195-375','reduction of the base ring','A.5','A',r'\Lambda','Enlarged middle band prints A. The category is being decomposed according to maximal ideals of the base Lambda; the preceding words refer to its completed local rings. It is Lambda, not the variable object A, that is reduced to a complete local base. Existing corrected reading confirmed.','misprint of the original','low'])
event('195-A5-profinite-algebras','targeted proof check','Finite-length Lambda-algebras have finite limits and descending chains of subobjects stabilize as chains of finite-length Lambda-submodules, so the artinian corollary applies. Given a complete separated linearly topologized algebra O with finite-length open quotients, O is the inverse limit of those quotients by completeness. A continuous map to a discrete finite-length algebra kills an open ideal and hence factors through one quotient. Two such factorizations agree after a common refinement, proving the displayed continuous-Hom formula. Recovering this quotient presentation from an arbitrary pro-system additionally uses strictification and the linearly compact finite-length-module inverse-limit theorem; that theorem is identified background rather than re-proved here.','195, p. 375, first paragraph and continuous-Hom display')
event('195-A5-base-product','refuted, with refined statement 195-A5-finite-support-product','Taken as a full categorical product over all maximal ideals, the statement about C is too broad: every finite-length Lambda-module has support at finitely many maximal ideals. For Lambda=Z, the tuple consisting of F_p for every prime p lies in the full product of the local categories but comes from no finite-length Z-algebra. The precise statement is the finite-support product (allowing zero components). The canonical finite decomposition of an artinian algebra gives that restricted equivalence. This clarification is reserved for the notes; the historical wording essentiellement le produit is retained.','195, p. 375, On notera d ailleurs paragraph')
event('195-A5-local-components-and-points','targeted proof check','Each finite-length quotient of O decomposes into finitely many local artinian factors, and a surjective transition map respects the associated central idempotents. Taking limits gives the product of the local components, indexed by the union of the finite quotient spectra; this uses the quotient presentation. A continuous O-to-K map into a field factors through an artinian quotient, so its image is the finite residue field kappa at its kernel. Two such maps have the same kernel exactly when they both factor from that common residue-field point, giving a common dominating pair. They also admit a common finite extension: a field quotient of K tensor over kappa K-prime. Conversely either kind of common comparison forces equal kernels because field maps are injective. If the base residue fields are algebraically closed, these finite residue extensions are trivial, giving the stated disjoint union of F(Lambda/m).','195, p. 375, local-component and field-valued point paragraph')
event('195-A5-power-series-quotient','refuted, with refined statement 195-A5-power-series-same-residue','The noetherian-to-power-series-quotient assertion lacks a residue-field condition. Take Lambda=R and O_xi=C with the discrete topology; this is a finite artinian Lambda-algebra and is noetherian. Every proper quotient of R[[t_1,...,t_n]] has residue field R, so it cannot be C as an R-algebra. With equal residue fields, finite generators of the maximal ideal modulo its square and the base maximal ideal give the usual continuous surjection from a power-series ring, using completeness; with a residue extension, an appropriate coefficient/base extension is needed. The earlier parenthetical statement beginning Si les Lambda/m sont algebriquement clos is a conditional point-counting observation, not a global hypothesis. The broad original assertion remains in both layers and is qualified in the notes.','195, p. 375, noetherian local component and power-series quotient assertion')
event('195-A5-dual-numbers','targeted proof check','The algebra I_A=A[t]/(t^2) has underlying A-module A plus At, so it remains a finite-length Lambda-algebra when A does. Evaluation at t=0 is the stated augmentation, and covariance gives F(I_A) to F(A) in the printed direction. The tangent construction continues on page 376.','195, p. 375, final two displays')
record_page('195',375,r'''Compared sources/fr_printed/fr/195.tex and sources/fr/fr/195.tex entry lines 309–359 with scan leaf 8 at 400 dpi, full page and all three enlarged bands. Inspected the two different limit notations, h-prime, every subscript and repeated point prime, the local-base letter, power-series brackets, t-squared and both augmentation arrows.

Restored the printed prose of the continuous-Hom display instead of set braces, its three lines and selective underline, the unindexed first limit, comma-numbered 3, 1, spaced abbreviation, exact punctuation, unelided si ils, double quotes, all selected underlines, wavy C and upright variables. The handwritten maximal-ideal m is retained with the supplied Gothic encoding provisionally for the final recurrent-letter review. Printed French restores A in the reduction of the base; corrected French keeps the justified Lambda, with an explicit row.

Checked the continuous-Hom factorization, local decomposition and same-point tests, and the dual-number augmentation. The inverse-limit theorem for linearly compact finite-length modules is identified background. Two substantive qualifications are recorded for the notes: the product of local categories needs finite support, and a quotient of a power-series ring over the given complete local base requires the corresponding residue-field condition. Counterexamples are Z with all residue-prime components and R-to-C, respectively. Neither broad historical assertion has been silently rewritten.''')
from update_record_counts import update
update()
