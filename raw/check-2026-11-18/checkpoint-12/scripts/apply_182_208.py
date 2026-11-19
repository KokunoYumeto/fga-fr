from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='7',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'182-208',line,statement,'400-dpi scan, full page and all three enlarged bands. '+why,kind,count=count)
 txt,_,_=page_text(rel,208);m=re.search(r'\\emph\{Complément de 1962\.\}.*?\n\n',txt,re.S)
 if not m:raise ValueError('Expected unprinted merged complement')
 r(m.group(0),'','after opening paragraph','7','structure','The 1962 paragraph about Mumford and Jacobi schemes is absent from the printed exposé page. Remove the merged insertion from both layers; leave separate supplementary text for its scheduled check.')
 txt,_,_=page_text(rel,208)
 r(r'\mathcal O_n','O_n','Artinian quotient rings','7-star',why='The scan distinguishes the handwritten script ring O from its typed plain O_n quotients; the latter are not script.',count=txt.count(r'\mathcal O_n'))
 r(r'\mathcal O_0','O_0','residue quotient','7-star',why='The displayed-in-line residue quotient is typed plain O_0.')
 r("$Y'=\\operatorname{Spec}(A)","$\\mathfrak Y'=\\operatorname{Spec}(A)",'base-change explanation','7-star',why='The prime-bearing Y is handwritten Gothic even though this Artinian spectrum is also a scheme.')
 r("$Y'$-schéma", "$\\mathfrak Y'$-schéma",'base-change explanation','7-star',why='The prime-bearing base symbol is Gothic.')
 r("\\mathfrak Y}Y'$", "\\mathfrak Y}\\mathfrak Y'$",'base-change tensor product','7-star',why='Both base symbols in this formula are Gothic.')
 r('Supposons qu\'on puisse',r"\uline{Supposons} qu'on puisse",'representability hypothesis','7-star',why='Only Supposons is underlined in this sentence.')
 r(r'\emph{schéma formel des modules} pour',r'\uline{schéma formel des modules pour}','definition after (*)','7-star',why='The definition is underlined through pour; le and X_0 are outside the underline.')
 r(r'fort bien \textit{a priori}',r'fort bien \uline{à priori}','penultimate paragraph','7',why='The first phrase is underlined and prints accented à.')
 r(r'inadéquat \textit{a priori}',r'inadéquat \uline{a priori}','last line','7',why='The second phrase is underlined and prints unaccented a.')
 r('des anneaux réguliers)','des anneaux \\uline{réguliers})','last line','7',why='The word réguliers is underlined, excluding the closing parenthesis.')
 r('Kodaira--Spencer','Kodaira-Spencer','penultimate line','7',why='A single short hyphen is printed.')
 upright_page(rel,layer,'182-208')
event('182-7-star','targeted proof check','The base-change assignment is covariant by associativity of tensor products and preservation of flatness. Given the natural representing isomorphism (*), its values at the Artinian quotients produce universal classes compatible with reduction. The representing complete ring, together with its natural isomorphism, is unique: apply naturality to the canonical maps to each finite quotient and pass to the inverse limit, giving inverse maps between two representing rings. The formal-scheme existence and extension from finite Artinian to arbitrary complete Noetherian bases are carried as background, not independently reproved here.','182, p. 208, (*) and surrounding paragraphs')
record_page('182',208,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 728–781 with scan leaf 17 at 400 dpi, full page and enlarged top, middle and bottom bands. Read the complete page, from the moduli-programme continuation through the criticism of restricting bases to regular rings; marker 209 already matches the end.

Removed the unprinted merged 1962 complement about Mumford and Jacobi schemes from both layers. Preserved the script complete ring but restored the plain typed quotient symbols O_n and O_0, Gothic Y-prime in all three base-change occurrences, the exact underlining, the first accented à priori and second unaccented a priori, and the short Kodaira-Spencer hyphen. The (*) display, its isomorphism direction, n+1 quotient exponent and all inline tensor products were compared enlarged. Checked functoriality and uniqueness of the representing ring conditional on (*); the formal-limit construction and extension assertion are explicitly carried as background.''')
p='CHECK_RECORD.md';t=read(p).replace('| Source pagination |','| Moduli ring and quotients | `\\mathcal O`, plain `O_n` and `O_0` | Script complete ring and typed plain Artinian quotients in 182-208; retain this distinction |\n| Source pagination |')
t=t.replace('- 182-207, Remarks 1 and 3: removed two merged 1962 complements from both layers; no modern replacement is inserted into the historical statements.','- 182-207, Remarks 1 and 3: removed two merged 1962 complements from both layers; no modern replacement is inserted into the historical statements.\n- 182-208, section 7: removed the merged 1962 complement about Mumford and Jacobi schemes from both layers.')
write(p,t)
from update_record_counts import update
update()
