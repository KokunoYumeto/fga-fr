from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/212.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'212-103',line,'2. Finite equivalence relations; 2.1 opening','400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 s,_,_=page_text(rel,103)
 for start,end,body in list(footnotes(s)):
  r(s[start:end],'','editorial footnote after stricts',kind='structure',why='There is no footnote or footnote mark at this place in the print. Its mathematical reason is retained in the audit record.')
 r('effectifs (ou non stricts,','effectifs (ou stricts,','opening parenthesis: printed reading',why='The print has stricts without non.')
 if tree=='fr':
  r('effectifs (ou stricts,','effectifs (ou non stricts,','opening parenthesis: corrected reading',kind='misprint of the original',why='The category has fibre products, and p. 101 proves effective if and only if strict. Therefore non-effective is equivalent to non-strict, not strict. The existing correction is confirmed independently.')
 r('il y a dans $\\mathcal C$ des épimorphismes non\neffectifs',r'\uline{il y a dans} $\text{\uwave{C}}$ \uline{des épimorphismes non effectifs}','first sentence emphasis',why='Straight underlines mark the prose on either side of the wavy-underlined category letter.')
 s,_,_=page_text(rel,103)
 for m in list(re.finditer(r'\\emph\{([^{}]*)\}',s,re.S)):
  r(m.group(0),underline_prose(m.group(1)),'emphasis '+m.group(1)[:45],why='The printed prose is straight-underlined; intervening formulas are outside that underline.')
 r(r'\longrightarrow',r'\to','three arrows',count=3,why='The scan uses ordinary-length arrows.')
 r('i.e. la droite affine','i. e. la droite affine','affine-line abbreviation',why='A space separates the two abbreviated words.')
 r('« recollement »',r'\fquote{recollement}','quoted word',why='The scan has ordinary double quotation marks.')
 r('de diverses variantes sera','de diverses variantes, sera','last long paragraph punctuation',why='The printed comma precedes sera.')
 r('le suivant:', 'le suivant :','proposition introduction',why='A space precedes the colon.')
 upright_page(rel,layer,'212-103')

event('212-2-non-strict-misprint','targeted proof check','Confirmed the existing insertion of non in non effectifs (ou non stricts): p. 101 proves the equivalence of effective and strict epimorphisms when the kernel pair exists, and finite schemes over a noetherian base have it. For an explicit finite example, let B=k[t]/(t^8) and A=k+kt^5+kt^6 inside B. Both are finite local k-algebras and A injects into B, so Spec(B) to Spec(A) is an epimorphism; the one-point underlying spaces reduce the arbitrary-target uniqueness test to the injective local-ring map. In B tensor_A B, put x=t tensor 1 and y=1 tensor t. Then x^5=y^5 and x^6=y^6, whence x^7-y^7=(x+y)(x^6-y^6)-xy(x^5-y^5)=0. Thus the map to the affine line defined by t^7 equalizes the kernel pair, but cannot factor through Spec(A), since t^7 is not in A. The epimorphism is not strict/effective.','212, p. 103, opening parenthesis; compare 190, p. 306, discussion of epimorphisms')
event('212-2-artinian-reduction','carried as background without fault found','The asserted reduction of effectiveness for finite equivalence relations to artinian local bases with algebraically closed residue field is stated without proof. A complete argument must control the kernel-pair comparison under the chosen flat local extensions, completion and artinian truncations, rather than assuming that equalizer subalgebras commute with arbitrary base change. The printed historical statements of what the author did not know are retained and are not interpreted as assertions about present knowledge.','212, p. 103, first paragraph after the opening parenthesis')
event('212-2-finite-relation-questions','carried as background without fault found','The quotient-existence and finite-projection questions, their extension to pregraphs and the reduction of effectiveness after a finite quotient are retained as the author presents them. The noetherian and finiteness conditions required to pass from the finite-over-base case to this setting must be supplied in a proof; no modern solution is inserted into either French layer. The pointed reference to formal moduli is to the already read 195 B, Theorem 1.','212, p. 103, second paragraph')
event('212-2-closed-gluing','targeted proof check','For a finite collection of pieces and compatible closed identifications R_ij in X_i times X_j, the disjoint union of the R_ij has finite projections to the disjoint union of the X_i: each projection is a closed immersion on its piece and each target piece meets only finitely many such pieces. The identity, symmetry and cocycle conditions give the equivalence relation. This checks the stated mechanism for finite closed gluing; without the finite incidence condition an arbitrary infinite family need not give a finite relation. The broader programme of nonprojective constructions is an announcement, not a theorem proved here.','212, p. 103, recollement paragraph')
record_page('212',103,r'''Compared sources/fr_printed/fr/212.tex and sources/fr/fr/212.tex entry lines 183–227 against scan leaf 6 at 400 dpi, full page and all three enlarged bands. Examined the missing non in the opening parenthesis, all straight/wavy underlines, the three arrows, t in k[t], the indices on X_i and p_1, the Ω and k(s) in the beginning of Proposition 2.1, and the references.

Removed the unprinted editorial footnote from both layers. Restored stricts in the as-printed parenthesis and confirmed non stricts in the corrected layer, with an explicit misprint row and independent reason. Both layers restore selective underlines, ordinary arrows and quotation marks, the i. e. spacing, the comma before sera and upright letters. No authorial erratum is merged here.

Checked the strict/effective equivalence and a concrete finite-algebra epimorphism that is not strict. Recorded the artinian reduction and finite quotient questions as unproved background and checked the finite closed-gluing mechanism with its finite incidence qualification. Proposition 2.1 begins here; its conclusion and assessment continue on the next printed page.''')
from update_record_counts import update
update()
