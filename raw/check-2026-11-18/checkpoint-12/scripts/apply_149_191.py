from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/149.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'149-191',line,statement,'400-dpi scan, enlarged page bands and tight crop of the start of (8.5). '+why,kind,count=count)
 r("est égal à l'un des arguments $B_j$ :","est égal à l'un des arguments $B_j$ ;",'line 1','8.4',why='The print has a semicolon.')
 r("le cas où l'un des arguments $B_i$ est localement libre", "le cas où l'un des arguments $B_j$ est localement libre",'first paragraph, line 4','8.5',why='This occurrence has subscript j; the following exceptional argument is printed B_i and remains so.')
 r('où cela est immédiat ; on peut','où cela est immédiat : on peut','after 8.5','8.5',why='The original has a colon.')
 txt,_,_=page_text(rel,191)
 for a,b,body in list(footnotes(txt)):
  r(txt[a:b],'','last paragraph','8-thm6','structure','The editorial note wrongly treats the other standard hypercohomology spectral sequence as a misprint. The note is withdrawn in both layers.')
 r(r'$H^{p}(X,H^{q}(K))$',r'$H^{p}(H^{q}(X,K))$','last paragraph, spectral-sequence term','8-thm6',why='Restore the printed and valid term: take the complex q-th sheaf cohomology of the terms K^a, then its p-th cohomology. This termwise-cohomology spectral sequence is the one suited to termwise Serre duality; replacing it by (8.2) was unjustified.')
 old=r'''\begin{aligned}
&T_{r}^{s*}(A_1,\ldots,A_{i-1},C,A_{i+1},\ldots,A_r;
 B_1,\ldots,B_{j-1},C,B_{j+1},\ldots,B_s)\\
&\qquad\longrightarrow
T_{r-1}^{s-1*}(A_1,\ldots,\widehat{A_i},\ldots,A_r;
 B_1,\ldots,\widehat{B_j},\ldots,B_s).
\end{aligned}'''
 new=r'''\begin{aligned}
&T_{r}^{s*}(A_1,\ldots,A_{i-1},C,A_{i+1},\ldots,A_r;
 B_1,\ldots,B_{j-1},C,B_{j+1},\ldots,B_s)\longrightarrow\\
&\qquad\relbar\quad
T_{r-1}^{s-1*}(A_1,\ldots,\widehat{A}_i,\ldots,A_r;
 B_1,\ldots,\widehat{B}_j\ldots,B_s)
\end{aligned}'''
 r(old,new,'formula 8.4','8.4','structure','Restore the two-line arrow continuation, hats on the letters rather than indices, no comma after the omitted B_j, and no terminal period.')
 if tree=='fr_printed':
  r(r'T_{r}^{s*}(A_1,\ldots,A_r;B_1,\ldots,B_s)',r'T_{r}^{s*}(.A_1,\ldots,A_r;B_1,\ldots,B_s)','formula 8.5, opening argument','8.5',why='The scan has a stray baseline dot before A_1. The corrected layer retains the argument list without it.')
 r(r'H^{n}(X,\Omega_X^{n}).',r'H^{n}(X,\Omega_X^{n})','formulae 8.6 and 8.7','8.6;8.7',why='Neither display has terminal punctuation.',count=2)
 txt,_,_=page_text(rel,191);label=r'\result{THÉORÈME}{6} ';a=txt.index(label)+len(label);b=txt.index('\n\n',a);old=txt[a:b]
 r(old,underline_prose(old),'Theorem 6','8-thm6',why='The theorem prose is underlined, excluding X and reference (8.6).')
 r('algébriques cohérents localement libres, alors',r'algébriques cohérents \uline{localement libres}, alors','Theorem 6 proof','8-thm6',why='The hypothesis localement libres is underlined.')
 r(r'\mathbf R',r'\underline{\underline{R}}','formula 8.7','8.7',why='The hyperderived R is double-underlined, not boldface.',count=3)
 txt,_,_=page_text(rel,191)
 r(r'\Omega',r'\underline{\Omega}','differential-sheaf symbols','8',why='All these sheaf symbols are underlined except the last inline occurrence, restored separately below.',count=txt.count(r'\Omega'))
 if tree=='fr_printed':
  r("et la suite spectrale analogue pour\n$K'\\otimes\\underline{\\Omega}_X^{n}$","et la suite spectrale analogue pour\n$K'\\otimes\\Omega_X^{n}$",'last paragraph, final inline Omega','8-thm6',why='The last inline Omega lacks an underline in print; corrected French retains the canonical-sheaf underline.')
 txt,_,_=page_text(rel,191);m=re.search(r'(\\begin\{aligned\})(.*?)(\\end\{aligned\})',txt,re.S);old=m.group(2)
 parts=re.split(r'(&|\\\\)',old)
 new=''.join(s if s in ('&',r'\\') or not s.strip() else '\n'+r'\symup{'+s.strip()+'}\n' for s in parts)
 r(old,new,'formula 8.4, upright variables','8.4',why='Typed mathematical variables are upright in each line of the continued display.')
 upright_page(rel,layer,'149-191')
event('149-8.4','targeted proof check','With the finite locally free resolution of the repeated coherent argument C, contraction is evaluation of its perfect complex against the dual. The counts fall from (r,s) to (r-1,s-1), with the repeated argument omitted. The arrow is continued over two printed lines; the isolated bar begins that continuation, not a negative sign on the target.','149, p. 191, (8.4)')
event('149-8.5','targeted proof check','If every contravariant argument is locally free and at most one covariant argument is not, all tensor factors except possibly one are flat. Thus the derived tensor expression is the ordinary tensor product shown, whose hypercohomology is ordinary sheaf cohomology. The dot before A_1 is an accidental printed mark, not part of the argument.','149, p. 191, paragraph and (8.5)')
event('149-8-thm6','targeted proof check','Withdrawn existing correction: the printed H^p(H^q(X,K)) is meaningful. For a bounded complex K of vector bundles, H^q(X,K) denotes the complex with terms H^q(X,K^a); its p-th cohomology is E2 of the termwise-cohomology hypercohomology spectral sequence. Serre duality pairs E1^{a,b}=H^b(X,K^a) with the corresponding term in the dual complex at (-a,n-b), giving complementary total degrees n. This is precisely the formal argument indicated. Substitution of H^p(X,H^q(K)) had selected a different spectral sequence without justification. The bounded-complex scope is supplied by the finite resolutions used in (8.1).','149, p. 191, Theorem 6, (8.7) and last paragraph')
record_page('149',191,r'''Compared sources/fr_printed/fr/149.tex entry lines 1196–1261 and sources/fr/fr/149.tex entry lines 1206–1271 with scan leaf 24 at 400 dpi, three enlarged bands and a tight crop showing the baseline dot before A_1 in (8.5). Read the contraction, locally-free reductions, duality pairing and proof of Theorem 6.

Restored punctuation, the first B_j index, the continued two-line arrow, hats confined to letters, prose underlines, double-underlined R, upright variables and differential-sheaf underlines. Printed French keeps the stray dot at the start of (8.5) and the omitted final Omega underline; corrected French omits the dot and supplies the underline.

**Existing mathematical correction reverted in both layers:** the printed term H^p(H^q(X,K)) is the valid termwise-cohomology spectral sequence, appropriate to this proof by termwise Serre duality. The supplied replacement H^p(X,H^q(K)) and its editorial footnote are withdrawn. The degree pairing (a,b) with (-a,n-b) confirms total degrees p and n-p. This substantive restoration must be propagated to all translations when reached.''')
from update_record_counts import update
update()
