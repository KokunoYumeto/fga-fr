from audit_utils import *
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
 prior_operations={(x['file'],x['printed_page'],x['old'],x['new']) for x in csv.DictReader(f,delimiter='\t')}
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/195.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  if (rel,'195-371',a,b) in prior_operations: return
  replace(rel,a,b,layer,'195-371',line,'A.2','400-dpi full scan and three enlarged bands. '+why,kind,count=count)
 r('de $\\mathcal C$ dans la catégorie des ensembles.',r'\uline{de} $\mathcal C$ \uline{dans la catégorie des ensembles}.','opening continuation',why='The underline continues from the previous page.')
 r('aussi les foncteurs covariants','aussi les foncteurs \\uline{covariants}','dual functors',why='Printed selective underline.')
 r('représentables, i.e. de la\nforme','\\uline{représentables}, i. e. de la forme','dual definition',why='Printed underline and spaced abbreviation.')
 r("\\[\n  Y\\longmapsto\\operatorname{Hom}(X,Y)=h'_X(Y).\n\\]","$Y\\rightsquigarrow\\operatorname{Hom}(X,Y)=h'_X(Y)$.",'dual representable formula',kind='structure',why='Inline formula with a wavy assignment arrow.')
 r(r'\subsection*{2. Foncteurs pro-représentables, pro-objets}',r'\subsection*{\normalfont 2. \uline{Foncteurs proreprésentables, pro-objets}.}','section heading',why='The heading has no hyphen in proreprésentables, ordinary roman lettering, an underline and a period.')
 r('$\\mathcal C$ ; il lui correspond','$\\mathcal C$, il lui correspond','system definition',why='Printed comma, not semicolon.')
 r("h'_{\\widetilde X}=\\varinjlim_i h'_{X_i},","h'_{\\widetilde X}=\\varinjlim_i h'_{X_i}",'first limit display',why='No terminal comma.')
 r(r'=\varinjlim_i\operatorname{Hom}(X_i,Y),',r'=\varinjlim_i\operatorname{Hom}(X_i,Y)','explicit limit display',why='No terminal comma.')
 r('filtrant est dit \\emph{pro-représentable}',r'\uline{filtrant}, est dit \uline{pro-représentable}','definition emphasis',why='Underline on filtrant and the defined term, with the printed intervening comma.')
 r('limites inductives filtrantes\nde foncteurs représentables.',r'\uline{limites inductives filtrantes de foncteurs représentables}.','characterization',why='The entire characterization phrase is underlined.')
 r('$J$) ; on vérifie','$J$), on vérifie','second system punctuation',why='Printed comma.')
 r('proposition 1.1)','proposition 1, 1)','reference to Yoneda',why='The printed statement number uses a comma.')
 if tree=='fr_printed':
  r("\\operatorname{Hom}(h'_{\\widetilde X'},h'_{\\widetilde X})","\\operatorname{Hom}(h_{\\widetilde X'},h'_{\\widetilde X})",'Hom comparison first functor',why='The printed h has no prime; corrected French retains the necessary prime.')
  r("\\operatorname{Hom}(h_{\\widetilde X'},h'_{\\widetilde X})","\\operatorname{Hom}(h_{\\widetilde X'},h_{\\widetilde X})",'Hom comparison second functor',why='The second printed h also has no prime.')
  r("$\\widetilde X'=(X'_j)_{j\\in J}$ sont deux tels objets","$\\widetilde X'=(X'_j)_{j\\in I}$ sont deux tels objets",'last second-system index set',why='The printed set is I, although this system is indexed by J.')
  r(r'catégorie duale de la catégorie $\operatorname{Pro}(\mathcal C)$',r'catégorie duale de la catégorie $\operatorname{Pro}(C)$','last Pro category identifier',why='The print omits the wavy underline in this one occurrence.')
 r('introduire la catégorie $','introduire la \\uline{catégorie} $','category definition',why='Printed selective underline.')
 r('des\npro-objets de $\\mathcal C$ ;',r'\uline{des pro-objets de} $\mathcal C$ ;','category definition continuation',why='Printed selective underline.')
 r(r'\operatorname{ProHom}',r'\operatorname{Pro\ Hom}','pro-morphism name',why='The printed operator has a space between Pro and Hom.')
 r(r"=\varprojlim_j\varinjlim_i\operatorname{Hom}(X_i,X'_j),",r"=\varprojlim_j\varinjlim_i\operatorname{Hom}(X_i,X'_j)",'pro-Hom display punctuation',why='No terminal comma.')
 r(r'\widetilde X\longmapsto',r'\widetilde X\rightsquigarrow','pro-object assignment',why='Printed wavy arrow.')
 s,_,_=page_text(rel,371)
 m=re.search(r'équivalence de la\ncatégorie duale.*?dans \$\(\\operatorname\{Ens\}\)\$\.',s,re.S)
 if not m: raise ValueError('Expected final equivalence span')
 r(m.group(0),underline_prose(m.group(0)),'final equivalence emphasis',why='The prose is underlined, while mathematical expressions retain their own typography.')
 for token,new,line in [(r'\mathcal C',r'\text{\uwave{C}}','category letters'),(r'\widetilde X',r'\text{\uwave{X}}','pro-object letters'),(r'\varinjlim_i',r'\varinjlim\limits_i','direct-limit indices'),(r'\varprojlim_j',r'\varprojlim\limits_j','inverse-limit indices')]:
  s,_,_=page_text(rel,371)
  r(token,new,line,count=s.count(token),why='Restore wavy underlines rather than script or tilde, and indices beneath the limit arrows.')
 upright_page(rel,layer,'195-371')
with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 for line,old,new,why in [
  ('Hom comparison first functor',"h_{\\text{\\uwave{X}}'}","h'_{\\text{\\uwave{X}}'}",'The pro-object functor just defined is covariant h-prime. The first h in the printed comparison omits its prime.'),
  ('Hom comparison second functor',r'h_{\text{\uwave{X}}}',r"h'_{\text{\uwave{X}}}",'The same omission affects the second h; the Yoneda evaluation proving this formula applies to the two covariant functors.'),
  ('last second-system index set',r"(X'_j)_{j\in I}",r"(X'_j)_{j\in J}",'The second system was explicitly indexed by J and the following inverse limit is over j; I belongs to the first system.'),
  ('last Pro category identifier',r'\operatorname{Pro}(C)',r'\operatorname{Pro}(\text{\uwave{C}})','This is the same category C with a wavy underline as in its definition and all adjacent occurrences.')]:
  w.writerow(['sources/fr/fr/195.tex','French corrected','195-371',line,'A.2',old,new,'Enlarged scan: '+why+' Existing corrected reading confirmed.','misprint of the original','low'])
event('195-A2-pro-Hom','targeted proof check','Let H_X=colim_i Hom(X_i,-). By the universal property of the source colimit, Nat(colim_j h_Xj-prime, H_X)=lim_j Nat(h_Xj-prime,H_X). Covariant Yoneda identifies each inner natural-transformation set with H_X(X_j-prime)=colim_i Hom(X_i,X_j-prime). This proves precisely the displayed inverse-j/direct-i formula, with no interchange of the two limits. It also confirms the two missing primes on h and the final erroneous I in the second system. Composition can be defined through composition of these natural transformations, so it is well defined and associative; identities are inherited. Full faithfulness follows from the same bijection and essential surjectivity onto the pro-representable functors follows from their definition.','195, p. 371, pro-object definition, Hom comparison and concluding equivalence')
record_page('195',371,r'''Compared sources/fr_printed/fr/195.tex and sources/fr/fr/195.tex entry lines 105–160 with scan leaf 4 at 400 dpi, full page and all three enlarged bands. Read every prime on h and X, the two index sets, all direct/inverse limit arrows and their order, the two Pro(C) occurrences and the final equivalence.

Restored the opening continuation underline, inline dual-representable formula, wavy assignment arrows, local unhyphenated heading spelling, roman headings, selective underlining, exact commas and display punctuation, the space in Pro Hom, wavy C and pro-object X, upright variables and limit indices beneath the arrows. Printed French restores two missing primes on h, the final erroneous I in the J-indexed system and the missing underline in the last Pro(C); corrected French retains the justified readings, with four explicit rows.

Checked the pro-Hom formula using the universal property of a colimit in the source followed by covariant Yoneda evaluation. This confirms the inverse-j/direct-i order. Transporting natural-transformation composition proves associativity and gives the stated equivalence with the opposite pro-category. No exchange of limits or finite-presentation hypothesis was used.''')
from update_record_counts import update
update()
