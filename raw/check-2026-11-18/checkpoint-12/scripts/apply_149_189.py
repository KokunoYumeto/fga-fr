from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/149.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'149-189',line,statement,'400-dpi scan and enlarged page bands. '+why,kind,count=count)
 if tree=='fr_printed':
  r('\\src{189}\npar exemple','\\src{189}\nla deuxième par exemple','line 1','7.6',why='The print repeats la deuxième across the page break. Corrected French retains only the p. 188 occurrence, avoiding the duplicated subject phrase.')
 else:
  r("diagramme suivant d'endomorphismes","diagramme suivant d'homomorphismes",'lines 1–2','7.6','misprint of the original','The maps displayed in (7.6) have different source and target groups; they are homomorphisms, not endomorphisms.')
 r(r'&\simeq&',r'&\xrightarrow{\sim}&','diagram 7.6, both rows','7.6',why='Both isomorphisms are right-pointing arrows with tildes.',count=2)
 r('une formule de Lefschetz :','une \\uline{formule de Lefschetz} :','line before Theorem 5','7-thm5',why='The words formule de Lefschetz are underlined.')
 r('congru, modulo la caractéristique de\n$k$, à','congru, $\\operatorname{mod}$ la caractéristique de\n$\\underline{k}$ à','Theorem 5, lines 2–3','7-thm5',why='The print abbreviates mod without underlining; the field k is underlined and has no following comma.')
 r('de multiplicité 1.','de multiplicité $1$.','Theorem 5 and following paragraph','7-thm5',why='The numerical multiplicity is ordinary upright type, excluded from the statement underline.',count=2)
 txt,_,_=page_text(rel,189);lab=r'\result{THÉORÈME}{5} ';a=txt.index(lab)+len(lab);b=txt.index('\n\n',a);old=txt[a:b]
 r(old,underline_prose(old),'Theorem 5','7-thm5',why='All statement prose is underlined; the symbols and abbreviation mod are not.')
 r('« homotope »',r'\fquote{homotope}','paragraph after Theorem 5','7-thm5',why='The print uses ordinary double quotation marks.')
 r(r'\fsection{8}{Généralisation du théorème de dualité}',r'\fsection{\normalfont8}{\normalfont\uline{Généralisation du théorème de dualité}.}','heading','8',why='The section title is underlined and ends with a period.')
 r(r'$B_1,\ldots,B_s$,',r'$B_1,\ldots,B_s$','last line','8',why='The printed page ends without a comma after the list of arguments.')
 txt,_,_=page_text(rel,189)
 r(r'\Omega',r'\underline{\Omega}','diagram differential sheaves','7.6',why='All differential-sheaf letters in the diagram are underlined.',count=txt.count(r'\Omega'))
 txt,_,_=page_text(rel,189);m=re.search(r'(\\begin\{array\}\{ccccc\})(.*?)(\\end\{array\})',txt,re.S);old=m.group(2)
 parts=re.split(r'(&|\\\\\[3pt\])',old)
 new=''.join(s if s=='&' or s==r'\\[3pt]' or not s.strip() else '\n'+r'\symup{'+s.strip()+'}\n' for s in parts)
 r(old,new,'diagram 7.6, cell letterforms','7.6',why='The typed variables in each diagram cell are upright; cell boundaries and arrows are preserved.')
 upright_page(rel,layer,'149-189')
event('149-7.6-print','refuted, with the refined statement\'s id','The printed label endomorphismes is incorrect for this diagram: its restriction-induced maps run between distinct Ext and Hom groups. The corrected wording is homomorphismes, id 149-7.6. The repeated la deuxieme at the page break is an independent compositorial duplication.','149, pp. 188–189, page break and introduction to (7.6)')
event('149-7.6','targeted proof check','Checked the six objects and arrow directions. The left vertical identification uses the perfect wedge pairing Omega_X^m tensor Omega_X^{n-m} to Omega_X^n. The right vertical map precomposes with restriction Omega_X^m to Omega_Y^m. Naturality yields the displayed compatibility; the two horizontal isomorphisms point right.','149, p. 189, (7.6)')
event('149-7-thm5','carried as background without fault found','Read the fixed-point trace congruence with multiplicity-one hypothesis and the following homotopy caveat. The author invokes the usual diagonal/graph argument without displaying it; no complete independent proof or extension to nontransverse intersections is claimed in this reading.','149, p. 189, Theorem 5 and following paragraph')
event('149-8-resolutions','carried as background without fault found','Read the finite locally free resolution and common-refinement claims under nonsingularity and the stated resolution property, including the surjective refinement for a surjection F-prime to F. These are prerequisites for the next-page multifunctor definitions, not a new proved result of this audit.','149, p. 189, section 8, opening paragraph')
record_page('149',189,r'''Compared sources/fr_printed/fr/149.tex entry lines 1055–1110 and sources/fr/fr/149.tex entry lines 1065–1120 against scan leaf 22 at 400 dpi and the enlarged top/middle/bottom bands. Read every cell and arrow of (7.6), Theorem 5, its caveat and the opening of section 8.

Both layers restore the two right-facing isomorphism arrows, differential-sheaf underlines, upright mathematics, the underlined Lefschetz phrase and theorem prose, literal mod, the field underline, missing final-comma omission, and the section heading. Printed French restores the second la deuxième at the page break; corrected French keeps the supplied nonduplicated sentence. A new corrected-layer repair changes endomorphismes to homomorphismes because the displayed maps do not have identical source and target. The actual diagram was checked using wedge duality and restriction; the fixed-point theorem and resolution claims were read as background, with the author's omitted proofs explicitly not certified here.''')
from update_record_counts import update
update()
