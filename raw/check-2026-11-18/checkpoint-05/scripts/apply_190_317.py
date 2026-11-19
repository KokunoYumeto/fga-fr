from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='B.1 theorem 2',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-317',line,statement,'400-dpi full image and three enlarged bands. '+why,kind,count=count)
 r('« équivaut »',r'\fquote{équivaut}','first line',why='Double quotes.')
 r('sur $S$ et des préschémas','sur $S$, et des préschémas','opening correspondence',why='Printed comma after S.')
 r('préschémas','pré-schémas','three plural occurrences',why='Printed hyphens.',count=3)
 r("$S'$-préschéma","$S'$-pré-schéma",'effectivity paragraph',why='Printed hyphen.')
 for word in ['morphisme de descente','morphisme de descente strict','radiciel']:
  r('\\emph{'+word+'}','\\uline{'+word+'}','underlined '+word,why='Underlining.')
 r('(A, définition 2.4)','(A définition 2.4)','first theorem reference',why='No comma after A in this reference.')
 r('des schémas affines au-dessus de pré-schémas\n(A, définition 1.7).','des schémas; affines au-dessus de pré-schémas,\n(A, définition 1.7).','theorem last two lines',why='The image shows a semicolon after schémas and a comma before the final reference; both are retained.')
 r('est exact,','est \\uline{exact},','below Hom diagram',why='Exact is underlined.')
 r('i.e.','i. e.','four abbreviations',why='Printed spacing.',count=4)
 r('\\emph{espace topologique\nquotient}',r'\uline{espace topologique quotient}','lemma conclusion','B.1 lemma 1.2',why='Underlined phrase.')
 r('soit ouverte est ouverte.','soit ouverte, est ouverte.','lemma final line','B.1 lemma 1.2',why='Comma after the inverse-image condition.')
 r('\\emph{une telle donnée de\ndescente n\'est pas nécessairement effective}',"\\uline{une telle donnée de descente n'est pas nécessairement effective}",'effectivity warning',why='Underlined prose.')
 r("d'après Serre","d'après SERRE",'surface attribution',why='Capitals.')
 r('de Nagata','de NAGATA','surface attribution',why='Capitals.')
 old="Pour\nqu'une donnée de descente sur $X'/S'$ relativement à\n$\\alpha:S'\\longrightarrow S$ (fidèlement plat et quasi-compact) soit effective,\nil faut et il suffit que $X'$ soit réunion d'ouverts $X'_i$, affines sur $S'$,\nqui soient « stables » par la donnée de descente sur $X'$."
 new=underline_prose(old.replace('\n',' ').replace('« stables »',r'\fquote{stables}'))
 new=new.replace("sur} $X'$.","sur} $\\underline{X'}$.")
 r('\\emph{'+old+'}',new,'underlined effectivity criterion',why='Selective prose underline excludes the earlier variables; the final X-prime is visibly included in the underline.')
 if tree=='fr_printed':
  r('formée des homomorphismes','formé des homomorphismes','below Hom diagram',why='Printed formé lacks the feminine ending.')
  r("et\n$X'$ un schéma algébrique","et\n$S'$ un schéma algébrique",'surface example',why='The image prints S-prime here, although the intended surface is X-prime.')
  r('quels que soient','quel que soit','last parenthesis',why='Printed singular wording.')
 upright_page(rel,layer,'190-317')
with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 for line,old,new,why in [
  ('below Hom diagram','formé des homomorphismes','formée des homomorphismes','The participle modifies the feminine noun partie.'),
  ('surface example',"$S'$ un schéma algébrique","$X'$ un schéma algébrique",'S-prime was just specified as the spectrum of a field, hence has dimension zero. The proper surface carrying the descent datum is X-prime.'),
  ('last parenthesis','quel que soit','quels que soient','The following coordinated subjects are X-prime/S-prime and the descent datum; plural agreement is required.')]:
  w.writerow(['sources/fr/fr/190.tex','French corrected','190-317',line,'B.1 theorem 2',old,new,'The enlarged scan shows the old reading. '+why,'misprint of the original','low'])
event('190-B1-theorem2','targeted proof check','Full faithfulness of quasi-coherent descent transports the multiplication, unit and their identities, giving descent of commutative algebras and hence relative affine schemes by relative Spec. For morphisms of arbitrary schemes, apply the quotient-topology lemma after base change to X: inverse images of affine opens of Y under a compatible map X-prime to Y-prime are saturated opens and descend to opens of X. On these opens the affine-target assertion follows from descent of functions; uniqueness glues the morphisms. The statement is full faithfulness in general, not effectivity for all schemes.','190, p. 317, theorem 2')
event('190-B1-lemma1.2','targeted proof check','Reduce locally on S and by a finite affine cover of S-prime to a faithfully flat ring map A to B. For a saturated closed set C in Spec B, its image is proconstructible: maps of affine spectra are continuous for the compact constructible topologies. Its image is specialization-stable: for p contained in p-prime choose q-prime over p-prime, and use flat going-down to find q contained in q-prime above p; saturation puts q in C and closedness then puts q-prime in C. A proconstructible specialization-stable subset of an affine spectrum is closed. Thus the image of C is closed and the surjection is a quotient map. The elementary constructible-topology criterion and flat going-down are the stated background inputs.','190, p. 317, lemma 1.2')
event('190-B1-theorem2-surface-letter','targeted proof check','The printed S-prime in the surface example cannot have dimension two: S-prime is Spec k-prime by the immediately preceding clause. Replacing it by X-prime restores the declared subject of the descent problem.','190, p. 317, last paragraph, surface example')
event('190-B1-theorem2-noneffective-surface','carried as background without fault found','Read the claim of a noneffective datum for a proper algebraic surface over a quadratic field extension and its SERRE/NAGATA attribution. The concrete surface and semilinear action are not constructed here; the claim is not recorded as independently proved.','190, p. 317, last paragraph, noneffectivity assertion')
event('190-B1-theorem2-affine-cover-global','refuted, with the refined statement\'s id','Literal global necessity of a cover by opens affine over S-prime fails for unrestricted non-semi-separated bases. Take alpha=id_S, with S obtained by gluing two affine planes along the punctured plane, and X the first plane. Its identity descent datum is effective. If an open W in X containing its origin were affine over S, then W is affine by base change to the first plane, and a principal open D(f) containing the origin can be chosen inside W. Since D(f) is principal also in W, its map to S would be affine. Base change to the second plane would make D(f) minus the origin affine. But its functions are k[x,y]_f (intersect the localizations at x and y in the fraction field, with f(0) nonzero); its canonical map to Spec k[x,y]_f omits the origin, contradicting affineness. Refined statement id: 190-B1-theorem2-affine-cover-local. The criterion is valid after restricting S to affine opens; this may be the implicit intended reduction. Preserve the printed criterion in both text layers and explain the scope in the notes.','190, p. 317, underlined effectivity criterion')
event('190-B1-theorem2-affine-cover-local','targeted proof check','Over an affine base S, an effective datum is covered by pullbacks of affine opens of its descended scheme; these are affine over S-prime and stable. Conversely a stable relative affine cover descends by the affine part of theorem 2. Its intersections are stable opens; lemma 1.2 after base change descends those opens, and full faithfulness descends and glues the overlap isomorphisms and their cocycles. Over an arbitrary base apply this criterion separately over an affine open cover of S, then glue.','190, p. 317, underlined effectivity criterion, refined local formulation')
record_page('190',317,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 948–999 with scan leaf 20 at 400 dpi, full page and all three enlarged bands. Read the Hom diagram and all its base indices, pullback labels, the inverse-image sign, primes and effectivity criterion.

Restored hyphenated pré-schémas, selective underlining (including the final X-prime of the criterion), double quotes, abbreviation spacing, SERRE/NAGATA capitals and printed punctuation. The theorem's unusual semicolon after schémas is retained. Printed French restores formé, the erroneous S-prime naming the proper surface, and singular quel que soit; corrected French retains the justified feminine agreement, X-prime and plural agreement, with explicit correction rows.

Checked algebra/affine-scheme descent, the morphism assertion using quotient topology, and lemma 1.2 with its two elementary background inputs stated. The specific noneffective surface is carried as background. A literal global reading of the stable relative-affine-cover criterion has a counterexample over a plane with doubled origin; the criterion works locally over affine opens of the base. This scope issue is reserved for the notes and does not alter the historical assertion. The radicial case continues on 318.''')
from update_record_counts import update
update()
