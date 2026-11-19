from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'182-194',line,'1','400-dpi scan and all three enlarged page bands. '+why,kind,count=count)
 for a in ['schéma affine','préschéma','morphismes','séparé','schéma','noethériens']:
  r(r'\emph{'+a+'}',r'\uline{'+a+'}','definition of '+a,why='Definition emphasis is underlining.')
 r(r'\Osh', 'O','local-ring and structure-sheaf symbols',why='All four O symbols here are plain, not underlined.',count=4)
 r(r'\mathbf Z','Z','base ring in paragraphs 3–4',why='The printed Z is ordinary, not bold.',count=2)
 r('$A$-algèbres.',r'$A$\uline{-algèbres}.','paragraph 3, definition over an affine base',why='The hyphen and algèbres are underlined; the mathematical A is excluded.')
 r('forment une catégorie ; de plus','forment une catégorie, de plus','paragraph 3, product existence',why='The scan has a comma.')
 r(r'est dit \emph{de type fini sur} $S$ si, pour tout',r'est \uline{dit de type fini} sur $S$, si pour tout','paragraph 4, finite type definition',why='The underline includes dit and excludes sur; the comma follows S, not si.')
 for a in ['espaces algébriques','espace algébrique']:
  r('« '+a+' »',r'\fquote{'+a+'}','last paragraph, quoted expression',why='Ordinary double quotes are printed.')
 r('$f^{-1}(s)$, le paramètre','$f^{-1}(s)$ le paramètre','last paragraph, family description',why='There is no comma after the fiber.')
 r(r'\kappa',r'\varkappa','residue fields, last paragraph',why='The handwritten kappa is the crossed variant without the straight vertical left stem.',count=2)
 upright_page(rel,layer,'182-194')
event('182-1-relative','carried as background without fault found','Read the local-homomorphism qualification, definitions of affine schemes and preschemes, relative structures over S, existence of fiber products and base change. The Z and O alphabets were checked against the image. These foundational assertions were read as background, not independently proved.','182, p. 194, first three paragraphs')
event('182-1-separated-finite-type','carried as background without fault found','Read the historical convention that a scheme is a separated prescheme, the standing noetherian convention, the finite-type definition, and fibers over residue fields. The historical terminology is retained and not modernized in either French layer.','182, p. 194, last paragraph')
record_page('182',194,r'''Compared both French files sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 45–88 with scan leaf 3 at 400 dpi and three enlarged bands. The local rings, subscripts, fiber products, inverse images, residue-field symbols, primes and definition emphasis were inspected.

Restored underlines in the definitions, plain O and Z alphabets, the crossed kappa variant, the exact extent of dit de type fini and -algèbres emphasis, ordinary double quotes, the comma after catégorie, the comma position in the finite-type definition, and the absent comma after the family fiber. Typed mathematical variables are upright. Both layers agree; no original misprint was asserted. Historical scheme/prescheme terminology and the author's noetherian restriction remain unchanged.''')
from update_record_counts import update
update()
