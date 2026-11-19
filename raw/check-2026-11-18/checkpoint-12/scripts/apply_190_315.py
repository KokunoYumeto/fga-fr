from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='B.1',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-315',line,statement,'400-dpi full image and three enlarged bands. '+why,kind,count=count)
 r(r'\emph{quasi-compact}',r'\uline{quasi-compact}','definition 1.2','B.1.2',why='Underlining in print.')
 r("réunion finie d'ouverts affines","réunion \\uline{finie} d'ouverts affines",'definition parenthesis','B.1.2',why='Finie is underlined.')
 r('pour les ouverts affines de','pour les ouverts \\uline{affines} de','affine-open test','B.1.2',why='Affines is underlined.')
 r('i.e.','i. e.','three explanatory abbreviations',why='Printed spacing.',count=3)
 r('« extension de la base »',r'\fquote{extension de la base}','stability assertion',why='Double quotes.')
 r('préschémas, fidèlement plat et quasi-compact.','pré-schémas, \\uline{fidèlement plat} et \\uline{quasi-compact}.','theorem hypothesis','B.1 theorem 1',why='Printed hyphen and selective underlines.')
 r(r'\emph{morphisme de descente strict}',r'\uline{morphisme de descente strict}','theorem conclusion','B.1 theorem 1',why='Underlining.')
 for n in ['i','ii']:
  r('\\item[('+n+')]',r'\item[\textnormal{('+n+')} ]','clause '+n,'B.1 theorem 1',why='Roman labels without a final period.')
 r(r'\mathcal O_S',r'\text{\uwave{O}}_S','specialization F = O','B.1 theorem 1',why='Wavy underline beneath ordinary O.')
 r(r'\result{COROLLAIRE}{1}',r'\result[, -]{COROLLAIRE}{1}','corollary heading','B.1 corollary 1',why='The enlarged heading shows a comma after 1.')
 upright_page(rel,layer,'190-315')
event('190-B1.1-sequence-criterion','targeted proof check','For a surjective flat map, at each point of the base choose a point above it; the resulting flat local ring map is faithfully flat, so tensor detects exactness of the localized sequence. Conversely, on each affine open the asserted exact and faithful pullback tests flatness by finite relations and detects every nonzero residue module. Together with localization this yields the stated local characterization. The three morphism tests follow by testing kernels and cokernels.','190, p. 315, opening paragraph')
event('190-B1.2-quasicompactness','targeted proof check','A quasi-compact open in a scheme admits a finite affine cover, so testing inverse images of affine opens suffices. An affine morphism passes this test. Composition and base change of quasi-compact morphisms reduce to finite affine coverings. Flatness is stable under tensor base change and composition; faithful flatness is stable as well, using nonzero residue-field fibers (or faithfulness of the composite tensor functors).','190, p. 315, definition 1.2 and stability paragraph')
event('190-B1-theorem1-statement','carried as background without fault found','Read the faithfully flat quasi-compact hypothesis, the reference to A.1.7, full faithfulness expressed by compatible Hom maps, and effectivity of every quasi-coherent descent datum. These two clauses exactly unpack strict descent in the preceding definition. This page states the theorem; a proof is not claimed here, and its subsequent proof remains to be read. Hom(O,G) identifies with global sections, giving the announced corollary whose diagram begins on 316.','190, p. 315, theorem 1 and corollary 1')
record_page('190',315,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 845–894 with scan leaf 18 at 400 dpi, including the full page and the top, middle and bottom enlarged bands. Read the opening exactness criterion, every hypothesis of theorem 1, its displayed Hom map, both clauses, the specialization F = O_S and the corollary opening.

Restored selective underlines in definition 1.2 and the theorem, spaced i. e., double quotes, hyphenated pré-schémas, Roman clause labels, wavy-underlined O_S and the comma visible in the corollary heading. The Hom map is correctly displayed in the supplied source. No mathematical correction was identified on this page. The blemish at the opening parenthesis before en particulier does not obscure the reading.

Checked the local exactness characterization, the affine-open quasi-compactness test and stability assertions. The strict-descent theorem is recorded at this point as a statement awaiting its later proof; its two explanatory clauses match full faithfulness and effectivity. The corollary follows formally from the Hom statement and continues on 316.''')
from update_record_counts import update
update()
