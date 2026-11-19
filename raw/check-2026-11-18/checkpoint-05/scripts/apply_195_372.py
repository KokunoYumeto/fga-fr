from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/195.tex'
 def r(a,b,line,kind='reading',why='',count=1,full=False):
  replace(rel,a,b,layer,'195-372',line,'A.2','400-dpi full scan and three enlarged bands. '+why,kind,count=count,full=full)
 r("$X_i\\longrightarrow X'$ soit équivalent à un épimorphisme\n\n\\src{373}\n", "\\src{373}\n$X_i\\longrightarrow X'$ soit équivalent à un épimorphisme\n",'last line / next page boundary',kind='structure',why='Page 372 ends after tout épimorphisme; the formula and following words start page 373.',full=True)
 r('est équivalente à une sous-catégorie\npleine de',r'\uline{est équivalente à une sous-catégorie pleine de}','opening emphasis',why='The printed phrase is underlined.')
 r('$\\mathcal C$, on\naura','$\\mathcal C$, alors on aura','opening sentence',why='Restore the second printed alors.')
 r(r'\widetilde X=\varprojlim_i X_i,',r'\widetilde X=\varprojlim_i X_i','first display punctuation',why='No terminal comma is printed.')
 r('étant prise dans','étant \\uline{prise dans}','limit category emphasis',why='Printed selective underline.')
 r("$). On fera attention que,\nlors", "$).\n\nOn fera attention que, lors",'paragraph before warning',kind='structure',why='A new indented paragraph begins On fera attention.')
 r('existe dans $\\mathcal C$','\\uline{existe dans} $\\mathcal C$','warning emphasis',why='Printed selective underline.')
 r("représentable à l'aide de $L$,\ni.e.","représentable à l'aide de $\\text{\\uwave{L}}$, i. e.",'representing object notation',why='This L has a wavy underline, unlike the earlier defining L; retain the local printed notation.')
 r(r'\operatorname{Hom}_{\mathcal C}(Y,L)',r'\operatorname{Hom}_{\mathcal C}(Y,\text{\uwave{L}})','representing Hom notation',why='The printed L again has a wavy underline. Both layers retain this local notation.')
 r('$\\varprojlim_{\\mathcal C}X_i$ est défini déjà en termes du',r'$\lim_{\mathcal C}X_i$ \uline{est défini déjà en termes du}','dependence on pro-object',why='This particular printed lim lacks its arrow. Its direction is specified by the surrounding text; retain the abbreviation in both layers. The following prose is underlined.')
 r('$\\operatorname{Pro}(\\mathcal C)$ dans $\\mathcal C$, et il y a un','$\\operatorname{Pro}(\\mathcal C)$ dans $\\mathcal C$ ; et il y a un','functor punctuation',why='Printed semicolon.')
 r(r'$\varprojlim_{\mathcal C}(\widetilde X)\longrightarrow\widetilde X$',r'$\lim_{\mathcal C}(\widetilde X)\longrightarrow\widetilde X$','canonical morphism notation',why='The printed lim has no arrow in this occurrence; retain its locally unambiguous abbreviation.')
 r('covariant pour fixer les idées,','covariant pour fixer les idées','functor introduction',why='No final comma is printed.')
 r(r"\longrightarrow\operatorname{Pro}(\mathcal C'),",r"\longrightarrow\operatorname{Pro}(\mathcal C')",'Pro(F) display punctuation',why='No terminal comma is printed.')
 r("un foncteur composé\n\\[\n  \\overline F:\\operatorname{Pro}(\\mathcal C)\\longrightarrow\\mathcal C',\n  \\qquad\n  \\overline F=\\varprojlim_{\\mathcal C'}\\circ\\operatorname{Pro}(F),\n\\]", "un foncteur composé $\\varprojlim_{\\mathcal C'}\\circ\\operatorname{Pro}(F)$ :\n\\[\n  \\overline F:\\operatorname{Pro}(\\mathcal C)\\longrightarrow\\mathcal C'\n\\]",'extended functor formula',kind='structure',why='The composite is inline before the colon; only the named functor and its source/target are displayed. The added equality and commas are absent from the print.')
 r(r'\emph{pro-objet strict}',r'\uline{pro-objet strict}','strict pro-object definition',why='The defined term is underlined, not italic.')
 r(r'\emph{strictement pro-représentable}',r'\uline{strictement pro-représentable}','strict functor definition',why='The defined term is underlined, not italic.')
 r('sont des épimorphismes ;','sont des \\uline{épimorphismes} ;','transition morphisms',why='Printed selective underline.')
 r('$I$ soit ordonné filtrant','$I$ soit \\uline{ordonné} filtrant','index set emphasis',why='Only ordonné is underlined.')
 r(r'$(X_i)_{i\in I}$ où les morphismes',r'$(X_i)_{i\in I}$, où les morphismes','strict system punctuation',why='Restore the printed comma.')
 if tree=='fr_printed':
  r("h'_{\\widetilde X}=\\varinjlim_i h'_{X_i}","h_{\\widetilde X}=\\varinjlim_i h'_{X_i}",'parenthetical limit first functor',why='The first printed h has no prime.')
  r("h_{\\widetilde X}=\\varinjlim_i h'_{X_i}","h_{\\widetilde X}=\\varinjlim_i h_{X_i}",'parenthetical limit second functor',why='The second printed h also has no prime.')
  r(r'$(X_i)_{i\in I}$, où les morphismes',r'$(X_i)_{i\in I}$, ou les morphismes','strict system relative clause',why='The print has ou without the grave accent; corrected French retains où.')
 for token,new,line in [(r'\mathcal C',r'\text{\uwave{C}}','category letters'),(r'\widetilde X',r'\text{\uwave{X}}','pro-object letters'),(r'\varinjlim_i',r'\varinjlim\limits_i','direct-limit indices'),(r'\varprojlim_i',r'\varprojlim\limits_i','inverse-limit indices')]:
  s,_,_=page_text(rel,372)
  r(token,new,line,count=s.count(token),why='Restore wavy category/pro-object letters and the indices beneath the limit arrows.')
 upright_page(rel,layer,'195-372')

with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 for line,old,new,why in [
  ('parenthetical limit first functor',r'h_{\text{\uwave{X}}}',r"h'_{\text{\uwave{X}}}",'The functor associated with this pro-object on page 371 is covariant h-prime; the first printed h omits the prime.'),
  ('parenthetical limit second functor',r'h_{X_i}',r"h'_{X_i}",'The stage functors in the direct limit must be the covariant represented functors Hom(X_i,-), denoted h-prime.'),
  ('strict system relative clause','ou les morphismes','où les morphismes','This is a relative clause specifying the system, requiring où; ou would mean or and break its syntax.')]:
  w.writerow(['sources/fr/fr/195.tex','French corrected','195-372',line,'A.2',old,new,'Enlarged scan: '+why+' Existing corrected reading confirmed.','misprint of the original','low'])
event('195-A2-pro-limits','targeted proof check','The constant embedding is fully faithful by Yoneda. The pro-Hom formula gives Hom_Pro(Z,(X_i))=lim_i Hom_Pro(Z,X_i), so the pro-object is the inverse limit of its stages in Pro(C). If L=lim_C X_i exists, Hom_C(Y,L)=lim_i Hom_C(Y,X_i)=Hom_Pro(cY,X), giving the right adjoint to the constant embedding and its canonical counit cL to X. The two missing primes in the covariant-functor formula are confirmed. The two printed plain lim abbreviations and local wavy L notation are retained because their interpretation is specified by context.','195, p. 372, constant embedding, first display and comparison with limits in C')
event('195-A2-pro-limit-not-constant','independent re-proof','For C=Sets take X_n={0,1}^n with truncation maps and L={0,1}^N. If the pro-system were isomorphic to constant L, a morphism from the system to L would be represented by a map from one finite X_n. Composing with an inverse from L would express id_L as a map factoring through that finite set, impossible because L is infinite. This proves the printed warning even in Sets without an appeal to another edition.','195, p. 372, warning that the two limits need not be isomorphic')
event('195-A2-extension-of-functors','targeted proof check','Applying F to stages and representative transition maps defines Pro(F); equality after refinement and composition are preserved because F is a functor. When inverse limits in C-prime exist, composition with their limit functor gives the displayed bar-F, taking (X_i) to lim F(X_i). Its restriction to constants is canonically F. The strict pro-object definition is read here; the ensuing normal-form assertion continues on page 373 and is deferred until that page.','195, p. 372, functor extension and strict pro-object definition')
record_page('195',372,r'''Compared sources/fr_printed/fr/195.tex and sources/fr/fr/195.tex entry lines 156–213 with scan leaf 5 at 400 dpi, full page and all three enlarged bands. Read every limit direction, prime, subscript, wavy underline, and the page boundary. Page 372 ends after “tout épimorphisme”; moved the next formula to page 373 in both layers.

Restored the missing second alors, paragraph break, underlined phrases, upright letters, wavy category and pro-object symbols, exact punctuation and the inline composite preceding the displayed extended functor. Retained the two local plain lim abbreviations and the two wavy L occurrences in both layers; their intended objects are fixed by the surrounding definitions, so no normalization was made. The printed layer restores two missing h-primes and ou; the corrected layer retains the three justified readings, each explicitly recorded.

Checked the formal inverse-limit property, the adjunction between constant objects and limits in C, the canonical comparison, and extension of a functor. Proved the warning in Sets using finite binary prefixes: an isomorphism with the constant infinite limit would force its identity through one finite stage. The final strict-system assertion continues on the next page.''')
from update_record_counts import update
update()
