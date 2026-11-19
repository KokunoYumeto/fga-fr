from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/149.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'149-190',line,statement,'400-dpi scan, enlarged bands and tight crop of the (8.3) target. '+why,kind,count=count)
 txt,_,_=page_text(rel,190)
 r('L(',r'\underline{L}(','resolution symbols','8.1',why='Every resolution L on this page is underlined, unlike the plain complexes named on p. 189.',count=txt.count('L('))
 r(r'\mathbf R',r'\underline{\underline{R}}','hypercohomology operator','8.1',why='The hyperderived R has a double underline, not boldface.',count=2)
 r(r'\right)\right),\\[3pt]',r'\right)\right)\\[3pt]','8.1, first row','8.1',why='The first row has no terminal comma.')
 r(r'\right)\right).',r'\right)\right)','8.1, second row','8.1',why='The second row has no terminal period.')
 old=r'''\[
  K=\Homsh_{\Osh_X}\bigl(\underline{L}(A_1)\otimes\cdots,
      \underline{L}(B_1)\otimes\cdots\bigr),
\]
aboutissant'''
 new=r'''$K=\Homsh_{\Osh_X}\bigl(\underline{L}(A_1)\otimes\cdots,
      \underline{L}(B_1)\otimes\cdots\bigr)$, aboutissant'''
 r(old,new,'hypercohomology paragraph, complex K','8.2','structure','The definition of K is inline, followed immediately by the continuing clause.')
 r(r'(A_1,\ldots,A_r;B_1,\ldots,B_s)\right).',r'(A_1,\ldots,A_r;B_1,\ldots,B_s)\right)','formula 8.2','8.2',why='There is no full stop after (8.2).')
 r('une composition (généralisant','une \\uline{composition} (généralisant','before 8.3','8.3',why='The operation name composition is underlined.')
 r('opération de contraction chaque','opération de \\uline{contraction} chaque','last paragraph','8',why='The operation name contraction is underlined.')
 r('les homomorphismes fonctoriels, les homomorphismes cobords et les suites','les homomorphismes fonctoriels et les homomorphismes cobords, les suites','after 8.3','8.3',why='Restore the printed placement of et and the comma.')
 if tree=='fr_printed':
  r('celle envisagée',"celle 'envisagée",'before 8.3','8.3',why='The print has a stray apostrophe immediately before envisagée. Corrected French retains the word without this accidental mark.')
 old=r'''\begin{aligned}
&T_{r}^{s*}(A_1,\ldots,A_r;B_1,\ldots,B_s)
\times T_{r'}^{s'*}(A'_1,\ldots,A'_{r'};B'_1,\ldots,B'_{s'})\\
&\qquad\longrightarrow
T_{r+r'}^{s+s'*}
(A_1,\ldots,A_r,A'_1,\ldots,A'_{r'};
 B_1,\ldots,B_s,B'_1,\ldots,B'_{s'}),
\end{aligned}'''
 new=r'''T_{r}^{s*}(A_1,\ldots,A_r;B_1,\ldots,B_s)
\times T_{r'}^{s'*}(A'_1,\ldots,A'_{r'};B'_1,\ldots,B'_{s'})
\longrightarrow T_{r+r'}^{s+s'*}
(A_1,\ldots,A'_{r'};B_1,\ldots,B'_{s'})'''
 r(old,new,'formula 8.3','8.3','structure','The original is one unbroken display and abbreviates each concatenated target list to its first and last arguments. No terminal comma is printed.')
 if tree=='fr_printed':
  r(r"(A_1,\ldots,A'_{r'};B_1,\ldots,B'_{s'})",r"(A_1,\ldots,A'_{r'};B_1,\ldots,B'_{s})",'formula 8.3, final subscript','8.3',why='The target prints s without a prime below B-prime. Corrected French retains s-prime, the last index of the second input list.')
 txt,_,_=page_text(rel,190)
 m=re.search(r'(\\begin\{aligned\})(.*?)(\\end\{aligned\})',txt,re.S);old=m.group(2)
 parts=re.split(r'(&|\\\\\[3pt\])',old)
 new=''.join(s if s=='&' or s==r'\\[3pt]' or not s.strip() else '\n'+r'\symup{'+s.strip()+'}\n' for s in parts)
 r(old,new,'formula 8.1, upright cell letters','8.1',why='Preserve upright typed letters separately in each alignment cell.')
 upright_page(rel,layer,'149-190')
event('149-8.1','targeted proof check','Checked the two definitions and zero-argument convention. Empty tensor products are O_X; the sheaf-valued zero-argument functor is O_X in degree zero, while its global version is H^*(X,O_X). Bounded locally free resolutions preserve quasi-isomorphisms under these tensor and Hom constructions. Hypercohomology is correctly distinguished by double-underlined R.','149, p. 190, (8.1) and first explanatory paragraph')
event('149-8.2','carried as background without fault found','Read the local-to-global hypercohomology spectral sequence, with p the sheaf-cohomology degree and q the cohomology-sheaf degree. The expression premier membre of (8.1) is read as the left side of its global row, not as a claim that the abutment is the sheaf-valued first row. No unsupported change of this wording is made.','149, p. 190, (8.2) and following paragraph')
event('149-8.3','targeted proof check','The two source argument lists concatenate, giving r+r-prime contravariant and s+s-prime covariant arguments. The printed last target index s lacks its prime; the corrected s-prime is forced by the second source list. The shorter printed ellipses are valid and were restored without expanding them. Signs in the omitted symmetry and contraction laws remain to be spelled out in the notes, not inserted into this text.','149, p. 190, (8.3) and following paragraph')
record_page('149',190,r'''Compared sources/fr_printed/fr/149.tex entry lines 1123–1199 and sources/fr/fr/149.tex entry lines 1133–1209 against scan leaf 23 at 400 dpi, all three enlarged bands and a tight crop of the final target of (8.3). Read the multifunctor definitions, zero-argument convention, spectral sequence and composition law.

Restored underlined resolution L, double-underlined hyperderived R, inline K, printed equation punctuation, underlined operation names, the original conjunction/comma order, upright mathematical letters and the one-line composition with its abbreviated argument lists. Printed French restores a stray apostrophe before envisagée and the unprimed final target index s; corrected French retains the supplied clean word and s-prime. Concatenation of the two input lists verifies the latter correction. The phrase premier membre was retained as referring to the left-hand side of the global equation, not normalized into a different claim.''')
from update_record_counts import update
update()
