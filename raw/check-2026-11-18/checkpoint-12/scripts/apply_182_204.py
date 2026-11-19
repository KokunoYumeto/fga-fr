from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1,full=False):
  replace(rel,a,b,layer,'182-204',line,statement,'400-dpi scan with all three enlarged bands and a tight derivation-letter crop. '+why,kind,count=count,full=full)
 r('\\src{205}\n', '', 'page boundary','6','structure','The existing marker lies after material printed on page 205; relocate it to the continuation of Corollary 1.',full=True)
 r('supposons $H^2(X_0,\\Theta_{X_0/k})=0$.','supposons\n\\src{205}\n$H^2(X_0,\\Theta_{X_0/k})=0$.','last line','6-thm8-cor1','structure','The printed page ends after supposons; the vanishing formula begins page 205.',full=True)
 txt,_,_=page_text(rel,204)
 r(r'\Osh','O','structure sheaves','6',why='The structure sheaf letters are plain O.',count=txt.count(r'\Osh'))
 for i in ['i','ii']:
  r(r'\textit{'+i+'.}',r'\textnormal{'+i+'.}','enumerated structures','6',why='The item labels are upright roman.')
 r(r'\Theta',r'\mathfrak G','derivation sheaf','6-thm8',why='The enlarged handwritten glyph is Gothic G, with a rounded lower bowl and internal descending stroke, not capital Greek theta; a local glyph specimen was used only to compare alphabets, not as textual evidence.',count=3)
 r('« canonique »',r'\fquote{canonique}','paragraph after Theorem 8','6-thm8',why='The word has ordinary double quotes.')
 r('« remonter »',r'\fquote{remonter}','mixed-characteristic paragraph','6-thm8',why='The word has ordinary double quotes.')
 r("$k$-algèbre (cas d'égales caractéristiques)","$k$-algèbre, (cas d'\\uline{égales caractéristiques})",'equal-characteristic parenthesis','6-thm8',why='Restore the comma before the parenthesis and underline égales caractéristiques only.')
 r('$X_{n-1}$ ; on se propose','$X_{n-1}$, on se propose','lifting induction','6-thm8',why='The punctuation is a comma, not a semicolon.')
 r("localement ; d'autre part", "localement, d'autre part",'lifting induction','6-thm8',why='The punctuation is a comma.')
 if tree=='fr_printed':
  r('défini sur $A$. Cependant','défini sur $X$. Cependant','mixed-characteristic sentence','6-thm8',why='The scan says défini sur X. Corrected French retains A, the Artinian base over which X is being lifted.')
 r(r'\mathfrak G_{X_0/k}\otimes_k(\mathfrak m^n/\mathfrak m^{n+1})',r'\mathfrak G_{X_0/k}\otimes_k\mathfrak m^n/\mathfrak m^{n+1}','automorphism-kernel formula','6-thm8',why='The quotient has no surrounding parentheses in the print.')
 r('H^2(X_0,\\mathfrak G_{X_0/k})\\otimes_k\n','H^2(X_0,\\mathfrak G_{X_0/k})\\otimes\n','obstruction formula','6-thm8',why='The tensor-product base k is omitted in this occurrence; the unambiguous implicit base is retained in both layers.')
 txt,_,_=page_text(rel,204)
 for m in list(re.finditer(r'\\\[\s*(.*?)\s*\\\]',txt,re.S)):
  old=m.group(0);expr=re.sub(r'\s*\n\s*',' ',m.group(1).strip());punct=''
  if expr.endswith('.'):punct='.';expr=expr[:-1]
  r(old,'$'+expr+'$'+punct,'flatness, automorphism and obstruction formulas','6','structure','All three formulas run within the prose in the printed page.')
 r('    \\end{enumerate}',r'\end{enumerate}','list end','6') if False else None
 r('\\end{enumerate}\nLe fait fondamental','Le fait fondamental','after flatness formula','6','structure','Le fait fondamental continues the same paragraph in item ii.')
 r('Le fait fondamental est le suivant :','Le fait fondamental est le suivant :\n\\end{enumerate}','end of item ii','6','structure','Close the list only after the introductory sentence, matching the continuous paragraph.')
 r('une obstruction à construire $X_n$\nremontant','une \\uline{obstruction à construire} $X_n$\n\\uline{remontant}','obstruction argument','6-thm8',why='The two prose spans are underlined.')
 txt,_,_=page_text(rel,204);marker=r'\result{THÉORÈME}{8} ';a=txt.index(marker)+len(marker);b=txt.index('\n\n',a);old=txt[a:b]
 r(old,underline_prose(old),'Theorem 8 statement','6-thm8',why='The theorem prose is roman and underlined, excluding mathematical letters.')
 txt,_,_=page_text(rel,204);marker=r'\result{COROLLAIRE}{1} ';a=txt.index(marker)+len(marker);old=txt[a:].rstrip()
 r(old,underline_prose(old),'Corollary 1 opening line','6-thm8-cor1',why='The statement opening is underlined; its continuation is reserved for page 205.')
 upright_page(rel,layer,'182-204')
event('182-6-flatness-criterion','used and rechecked in this run','Over an Artinian local base the displayed natural graded isomorphisms express flatness: lift a residue-field basis and compare each finite filtration quotient; nilpotence then identifies the module with the corresponding free A-module. Read the sheaf formulation stalkwise.','182, p. 204, item ii')
event('182-6-thm8','carried as background without fault found','Read the affine smooth lifting and uniqueness theorem; no proof is printed. Its proof requires infinitesimal deformation/lifting theory for smooth affine algebras (projective differentials and vanishing higher affine obstruction groups), which is carried as background here. Restored the Gothic derivation letter G in subsequent prose; corrected French retains the Artinian base A where the print says X.','182, p. 204, Theorem 8 and following paragraph')
event('182-6-thm8-obstruction','targeted proof check','For a square-zero final kernel, an augmented automorphism is 1+D with D a derivation into the kernel; composition is addition. Flatness identifies the kernel with O_X0 tensor m^n/m^(n+1), giving the stated derivation sheaf. Lifting local schemes and overlap isomorphisms produces a triple-overlap 2-cocycle; its vanishing is the obstruction to gluing. This checks the deduction conditional on Theorem 8.','182, p. 204, automorphism identification and obstruction paragraph')
record_page('182',204,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 536–617 with scan leaf 13 at 400 dpi, full page and all enlarged bands. Inspected an additional tight crop of the handwritten derivation symbol and a local font specimen: the glyph is provisionally read as Gothic G, not the supplied Greek Theta. The scan itself decides this reading; the specimen only distinguishes candidate alphabet shapes. Moved marker 205 to before the vanishing formula in Corollary 1, whose first line ends this page.

Restored plain O, roman item labels, three inline formulas and their punctuation, the continuing paragraph in item ii, ordinary double quotes, local and statement underlining, the comma before the equal-characteristic parenthesis and two commas in the induction. Removed unprinted quotient parentheses and the expanded tensor base in the obstruction term. Printed French restores défini sur X; corrected French retains the necessary Artinian base A. The flatness criterion and square-zero automorphism/gluing deduction were checked; Theorem 8 itself remains an explicitly identified background theorem without a printed proof.''')
from update_record_counts import update
update()
