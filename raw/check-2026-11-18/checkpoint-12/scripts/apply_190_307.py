from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-307',line,statement,'400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 r("l'effectivité d'une donnée de recollement", "l'\\uline{effectivité} d'une donnée de recollement",'opening question','2(c)',why='Only effectivité is underlined.')
 r("(et plus particulièrement d'une", "(et plus particulièrement, d'une",'opening parenthesis','2(c)',why='Comma after particulièrement.')
 r("$S'$ est délicate (et", "$S'$, est délicate, (et",'opening sentence continuation','2(c)',why='Commas occur before est and before the parenthesis.')
 r('Plus généralement, soient $A$','Plus généralement, soit $A$','ring formulation opening','2(c)',why='The print uses singular soit; retained as the author’s elliptical formulation.')
 r('i.e.','i. e.','definition of module descent data','2(c)',why='Spaced abbreviation.')
 r('de 1.c (que','de 1.(c) (que','cocycle reference','2(c)',why='Printed parentheses enclose c.')
 s,_,_=page_text(rel,307)
 span=re.search(r"L'effectivité de \$\\varphi\$ signifie alors.*?isomorphisme\.",s,re.S).group()
 r(span,underline_prose(span),'effectivity criterion emphasis','2(c)',why='The prose of the criterion is underlined; math letters and terminal punctuation are excluded.')
 if tree=='fr_printed':
  r('une technique de descente, à faire','une technique de descente, de faire','remark first sentence','2(c), remarque',why='The print has de faire after obligeait; corrected French retains grammatical à faire.')
 r('corps de base','\\uline{corps} de base','remark last sentence','2(c), remarque',why='Corps is underlined.')
 upright_page(rel,layer,'190-307')
with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 csv.writer(f,delimiter='\t').writerow(['sources/fr/fr/190.tex','French corrected','190-307','remark first sentence','2(c), remarque','une technique de descente, de faire','une technique de descente, à faire','Confirmed supplied à against printed de in the lower enlarged band: the governing verb is obligeait, whose complement is à faire.','misprint of the original','low'])
event('190-2c-flat-module-descent','targeted proof check','Verified equivalence between the algebra equalizer A -> B => B tensor_A B and full faithfulness on flat modules. For a flat target module N, tensoring gives N as the equalizer of N tensor B => N tensor B tensor B; a compatible B-linear map from M tensor B therefore restricts uniquely to M -> N. Conversely take M=N=A and identify its compatible endomorphisms with the ring equalizer. The displayed phi has the two correct tensor-factor placements and the invariant equation lies in B tensor_A M-prime.','190, p. 307, ring and module reformulation')
event('190-2c-effectivity-criterion','targeted proof check','The invariant elements form an A-submodule because both maps in the defining equality are A-linear. Its inclusion induces the canonical B-linear map M tensor_A B -> M-prime. If this is an isomorphism and M is flat, the invariant equation ensures compatibility with the canonical descent datum. Conversely any effective flat N is recovered as its invariant module by the flat-module equalizer just checked, so N=M and the canonical map is an isomorphism.','190, p. 307, underlined effectivity criterion')
event('190-2c-effectivity-question','carried as background without fault found','Read the historical question for flat quasi-coherent modules, including the Artinian local, rank-one special case. No answer or later result is inserted into either text layer. The remark explains the shift from flat objects to flat covering morphisms; its forward reference to paragraph 2 is retained pending the later section structure. Over a field all modules are vector spaces and hence flat.','190, p. 307, opening question and closing remark')
record_page('190',307,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 438–485 with scan leaf 10 at 400 dpi, full page and all three enlarged bands. Read the entire effectivity question, all three displayed formulas, the tensor-unit subscripts and the closing remark. The marker for 308 follows the completed remark.

Restored the selective effectivity/corps underlines, three opening commas, singular soit, spaced i. e., parenthesized c in the reference, and the prose underlining of the effectivity criterion. In printed French restored the visible de faire after obligeait; confirmed and explicitly recorded the grammatical à faire only in corrected French. All formulas, primes, arrow directions and displayed/inline positions agree after upright-letter restoration.

Checked full faithfulness for flat modules from the ring equalizer, its converse from endomorphisms of A, the A-submodule of invariants, and the two implications of the stated effectivity criterion. The question about arbitrary flat descent data remains a historical question. The forward reference to paragraph 2 is left for inspection of the later section structure, rather than guessed from the current numbering.''')
from update_record_counts import update
update()
