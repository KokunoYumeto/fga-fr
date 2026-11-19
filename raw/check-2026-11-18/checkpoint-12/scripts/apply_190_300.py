from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-300',line,statement,'400-dpi full scan, all three enlarged bands, and completion-sign crop. '+why,kind,count=count)
 r(r'\widehat A',r'\overline A','opening completion notation','A',why='Completion is indicated by a straight bar, not a hat.',count=3)
 r(r'$\overline A\otimes_A\overline A$',r'$\overline{\overline A}\otimes_A\overline A$','opening tensor product, first factor','A',why='The first factor visibly carries two separated horizontal strokes above A. Retain the visible doubled bar provisionally rather than silently removing the upper stroke; completion is idempotent here.')
 r(r'\fsection{A}{Préliminaires sur les catégories}',r'\section*{\normalfont A. \uline{Préliminaires sur les catégories}.}','section A heading','A',kind='structure',why='The heading is ordinary type with the words underlined and a terminal period.')
 r('\\subsection*{1. Catégories fibrées, données de descente, morphismes de\n$\\mathcal F$-descente}',r'\subsection*{\normalfont 1. \uline{Catégories fibrées}, \uline{données de descente}, \uline{morphismes de} $\mathcal F$-\uline{descente}.}','section 1 heading','1',kind='structure',why='The prose is underlined, excluding commas, the script letter, and the terminal period.')
 r(r'\emph{catégorie fibrée}',r'\uline{catégorie fibrée}','definition opening','1.1',why='The defining term is underlined.')
 r(r'\mathcal C',r'\text{\uwave{C}}','category C occurrences','1.1; Examples 1–2',why='All ten category letters on this page are ordinary C with a wavy underline.',count=10)
 r('un « objet de\n$\\text{\\uwave{C}}$ au-dessus de $Y$ »',r'un \fquote{objet de $\text{\uwave{C}}$ au-dessus de $Y$}','definition parenthesis','1.1',why='Ordinary double quotation marks.')
 r('i.e. comme','i. e. comme','definition parenthesis','1.1',why='The abbreviation is visibly spaced i. e.')
 r('et enfin,\npour deux','et enfin pour deux','definition composition clause','1.1',why='No comma after enfin.')
 r(r'c_{f,g}:(gf)^*\longrightarrow f^*g^*,',r'c_{f,g}:(gf)^*\longrightarrow f^*g^*','composition-isomorphism display','1.1',why='No punctuation follows this display.')
 r(r'\item[(i)] $\operatorname{id}_X^*=\operatorname{id}$ ;',r'\item[\textnormal{(i)}] $\operatorname{id}^*=\operatorname{id}$','identity axiom','1.1(i)',why='The printed id has no X subscript; no terminal semicolon.')
 r(r'\item[(ii)]',r'\item[\textnormal{(ii)}]','identity coherence item label','1.1(ii)',why='Ordinary roman item label.')
 r('isomorphisme identique ;','isomorphisme identique','end of axiom ii','1.1(ii)',why='No terminal punctuation.')
 r(r'\item[(iii)] étant',r'\item[\textnormal{(iii)}] Etant','associativity axiom opening','1.1(iii)',why='Initial unaccented capital E and roman item label.')
 old=r'''\begin{array}{ccc}
  (h(gf))^*=((hg)f)^* & \longrightarrow & f^*(hg)^* \\
  \big\downarrow && \big\downarrow \\
  (gf)^*h^* & \longrightarrow & (f^*g^*)h^*=f^*(g^*h^*).
\end{array}'''
 new=r'''\begin{array}{ccc}
  \symup{(h(gf))^*=((hg)f)^*} & \longrightarrow & \symup{f^*(hg)^*} \\
  \big\downarrow && \big\downarrow \\
  \symup{(gf)^*h^*} & \longrightarrow & \symup{(f^*g^*)h^*=f^*(g^*h^*)}
\end{array}'''
 r(old,new,'associativity square','1.1(iii)',why='Upright typed variables; no terminal period. Both factorizations and both compositions agree with the scan.')
 r('existent. On définit','existent, on définit','Example 1 opening','Example 1',why='Comma followed by lowercase on.')
 r('par le produit fibré','par le \\uline{produit fibré}','Example 1 pullback','Example 1',why='The words produit fibré are underlined.')
 r(r'Z\longmapsto Z\times_YX',r'Z\rightsquigarrow Z\times_YX','Example 1 object assignment','Example 1',why='The source uses a wavy right arrow without a mapsto bar.')
 r('préschémas','pré-schémas','Example 2 scheme occurrences','Example 2',why='Internal hyphen printed in both occurrences.',count=2)
 r('image inverse\n','\\uline{image inverse}\n','Example 2 last words','Example 2',why='The phrase at the page foot is underlined.')
 if tree=='fr':
  r("l'anneau non\nnoethérien", "l'anneau non nécessairement\nnoethérien",'opening tensor-product assertion','190-A-completion-tensor',kind='misprint of the original',why='The absolute claim fails for a complete noetherian local A, for which A-bar tensor_A A-bar is A. For example A is a field. The context only needs the tensor product not to be assumed noetherian; inserting nécessairement gives that qualified assertion.')
 upright_page(rel,layer,'190-300')
event('190-A-completion-tensor','refuted, with the refined statement\'s id','The unqualified assertion that the completed tensor product is nonnoetherian fails for A=k, a field: completion and the tensor product both equal k. Corrected French qualifies it as non nécessairement noethérien; refined statement id 190-A-completion-tensor-qualified. The doubled first completion bar visible in the print is retained provisionally; completion of a complete noetherian local ring changes nothing.','190, p. 300, opening paragraph')
event('190-1.1','targeted proof check','Checked the normalized contravariant pseudofunctor data: c(f,g) maps (gf)* to f*g*, identity axioms have matching domains, and the square compares (c(f,g) h*) c(gf,h) with (f* c(g,h)) c(f,hg). Both paths run from (hgf)* to f*g*h*. The old terminology catégorie fibrée is preserved; no modern reformulation is inserted.','190, p. 300, Definition 1.1')
event('190-1-example1','targeted proof check','For objects over Y, the fiber product with X defines pullback. The comparison from the pullback along gf to iterated pullback is the unique map with the same three projections; the two triple-pullback comparison paths therefore agree by the universal property. Choose identity pullbacks identically for the normalized units.','190, p. 300, Example 1')
event('190-1-example2','carried as background without fault found','Read the beginning of the quasi-coherent-module pullback example; it continues on p. 301. Pullback preservation and the canonical tensor associativity constraints are standard background, not independently reproved here.','190, p. 300, Example 2')
s=read('CHECK_RECORD.md')
anchor='| Completion |'
i=s.index(anchor)
s=s[:i]+'| Descent base category and fibred category | `\\text{\\uwave{C}}`, `\\mathcal F` | Ordinary wavy-underlined C and script F in 190-300; not interchangeable script letters |\n'+s[i:]
anchor='## Mathematical decisions so far'
i=s.index('\n### ',s.index(anchor)) if '\n### ' in s[s.index(anchor):] else len(s)
s=s[:i]+'\n- 190-300, introductory tensor product: qualified non noethérien as non nécessairement noethérien in corrected French; the original universal claim fails for A already complete.\n'+s[i:]
write('CHECK_RECORD.md',s)
record_page('190',300,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 43–102 with scan leaf 3 at 400 dpi, all three enlarged bands, and a tight crop of the completion bars. Read every word, all category letters and subscripts, the pullback/composition formulas, three axioms, the associativity square, Example 1 and the beginning of Example 2. The next marker correctly follows image inverse.

Restored straight completion bars, the visible doubled bar on the first tensor factor (provisional pending the mandated second reading), wavy-underlined ordinary C versus script F, underlined headings/definition/pullback terminology, ordinary double quotes, i. e. spacing, printed punctuation, identity without the added X subscript, unaccented Etant, the wavy object-assignment arrow, pré-schémas, and upright typed mathematical letters. The square has been checked arrow by arrow, including both expressions for each corner. Definition 1.1 is the author's normalized pullback-functor description; it is not modernized.

New correction of the original: the tensor product is not invariably nonnoetherian, since A complete gives A tensor_A A=A. Corrected French inserts nécessairement after non; printed French retains the absolute assertion. The doubled bar is not removed merely for consistency: its visible two strokes are recorded, and a second completion here is idempotent. The categorical coherence and fiber-product example received explicit universal-property checks; the sheaf example remains background at this page boundary.''')
from update_record_counts import update
update()
