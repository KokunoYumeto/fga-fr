from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1,full=False):
  replace(rel,a,b,layer,'182-210',line,statement,'400-dpi scan, full page and all three enlarged bands. '+why,kind,count=count,full=full)
 r('\\src{211}\n','','page boundary','8','structure','The printed page ends with par exemple au point générique de.',full=True)
 r('au point générique de\n$X$ supposé irréductible','au point générique de\n\\src{211}\n$X$ supposé irréductible','last line','8-def-pi1','structure','Move marker 211 before the irreducibility qualification and the later classification sentence.',full=True)
 r('\nde $X$ si','\n\\uline{de} $X$ si','first line','8-def-cover',why='The continuation de is underlined; X and si are not.')
 for n in ['i','ii','iii']:
  r('\\textit{'+n+'.}','\\textnormal{'+n+'.}','condition '+n+' marker','8-def-cover',why='The enumeration markers are upright.')
 txt,_,_=page_text(rel,210)
 r(r'\mathcal A',r'\text{\uwave{A}}','six algebra-sheaf symbols','8-def-cover',why='The algebra sheaf is ordinary wavy-underlined A, not script A.',count=txt.count(r'\mathcal A'))
 r(r'\Osh','O','tensor-product base ring','8-def-cover',why='O_x is plain.')
 r(r'\kappa',r'\varkappa','residue-field symbols','8-def-cover,8-def-point',why='The repeated residue-field symbol is crossed handwritten kappa, with the first formula exception separately restored in printed French.',count=txt.count(r'\kappa'))
 txt,_,_=page_text(rel,210);m=re.search(r'\\\[\s*(.*?)\s*\\\]',txt,re.S);old=m.group(0);expr=re.sub(r'\s*\n\s*',' ',m.group(1).strip())
 r(old,'$'+expr+'$','condition iii quotient formula','8-def-cover','structure','The entire quotient identity is inline, not a separate display.')
 r('sur $X$ ;','sur $X$','ends of conditions i and ii','8-def-cover',why='Neither condition has a semicolon in the scan.',count=2)
 if tree=='fr_printed':
  r(r'\otimes_{O_x}\varkappa(x)',r'\otimes_{O_x}\pi(x)','condition iii, tensor factor','8-def-cover',why='The scan clearly prints pi(x) here, contrasting with crossed kappa(x) immediately below. Corrected French retains the residue field kappa(x), required by the quotient identity.')
 r('due à Serre','due à SERRE','attribution','8',why='SERRE is uppercase in print.')
 r('à une théorie de Galois calquée','à une \\uline{théorie de Galois} calquée','Galois comparison','8',why='The first théorie de Galois is underlined.')
 r(r'\emph{point géométrique}',r'\uline{point géométrique}','definition of geometric point','8-def-point',why='The term is underlined, not italic.')
 r(r'\emph{localité}',r'\uline{localité}','underlying point','8-def-point',why='The term localité is underlined.')
 r("« points géométriques de $X'$ au-dessus de $a$ »",r"\fquote{points géométriques de $X'$ au-dessus de $a$}",'geometric fiber description','8-def-point',why='The print uses ordinary double quotation marks.')
 r(r'\varkappa(x)$-homomorphisme $\varkappa(x\prime)\longrightarrow\Omega$', '', 'unused') if False else None
 r("$\\varkappa(x)$-homomorphisme $\\varkappa(x')\\longrightarrow\\Omega$", "$\\varkappa(x)$-homomorphisme dans $\\Omega$",'geometric fiber homomorphism','8-def-point',why='The print says homomorphisme dans Omega, with the source field of the chosen point understood. The supplied explicit kappa(x-prime) arrow is an unnecessary expansion, so restore the original abbreviated wording in both layers.')
 r(r'\emph{groupe fondamental} du schéma connexe'+'\n$X$ en le point géométrique $a$',r'\uline{groupe fondamental du schéma connexe}'+'\n$X$ \\uline{en le point géométrique} $a$','fundamental-group definition','8-def-pi1',why='The underlining extends through du schéma connexe and en le point géométrique, excluding the two mathematical letters.')
 upright_page(rel,layer,'182-210')
event('182-8-def-cover','targeted proof check','For an O_x-module M, M/m_x M is canonically M tensor_{O_x} kappa(x), by right exactness of tensoring O_x -> kappa(x). Thus the printed pi(x) in condition iii is a symbol slip; corrected French retains the residue field. Conditions i–iii describe a finite locally free algebra with separable fibers, the finite étale covering condition in this setting; the general criterion is carried as background.','182, p. 210, conditions i–iii')
event('182-8-def-point','targeted proof check','A geometric point above a fixed base geometric point is equivalently a point x-prime above x plus an embedding of its residue field into Omega over kappa(x). This checks the fiber-set description. The original abbreviates the source field in homomorphisme dans Omega; restored that wording in both layers because its context already identifies the field, rather than treating the abbreviation as a mathematical misprint.','182, p. 210, geometric-point and fiber definitions')
event('182-8-def-pi1','carried as background without fault found','Read the Galois-category reconstruction, uniqueness of the profinite group with its fiber functor, and change-of-geometric-base-point statement up to inner automorphisms. These substantial categorical claims are not independently proved in this page check; the definition and all group indices were inspected. The last sentence continues on page 211.','182, p. 210, definition of the fundamental group')
record_page('182',210,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 824–878 with scan leaf 19 at 400 dpi, full page and enlarged top, middle and bottom bands. Read conditions i–iii, geometric points and fibers, and the Galois-category description through par exemple au point générique de. Moved marker 211 before X supposé irréductible; the supplied classification footnote now belongs to the next page and was not changed in this step.

Restored wavy-underlined A, plain O, crossed kappa, roman enumeration, the inline quotient identity with no semicolons at i–ii, uppercase SERRE, double quotes and exact term underlining. Printed French restores pi(x) in condition iii; corrected French retains kappa(x), justified by the elementary quotient/tensor identity and the residue field named immediately afterward. Removed the supplied explicit source-field arrow from the geometric-point description in both layers: the print's homomorphisme dans Omega has its source understood from the chosen point and does not require correction. The tiny stop at the following line start is retained as sentence punctuation. Galois-category reconstruction is honestly recorded as background.''')
p='CHECK_RECORD.md';t=read(p).replace('## Open reading questions','- 182-210, covering condition iii: retained kappa(x) rather than printed pi(x) in the residue tensor product; restored the valid abbreviated geometric-point homomorphism wording in both layers.\n\n## Open reading questions');write(p,t)
from update_record_counts import update
update()
