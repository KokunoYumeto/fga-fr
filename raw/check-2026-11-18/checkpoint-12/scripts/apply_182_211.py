from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1,full=False):
  replace(rel,a,b,layer,'182-211',line,statement,'400-dpi scan, full page and all three enlarged bands. '+why,kind,count=count,full=full)
 r('\\src{212}\n','','page boundary','8-lem3','structure','The page ends after the introduction of the two equivalent conditions.',full=True)
 r('Alors les deux conditions suivantes sont équivalentes :\n\\begin{enumerate}','Alors les deux conditions suivantes sont équivalentes :\n\\src{212}\n\\begin{enumerate}','last line','8-lem3','structure','Move marker 212 before condition i; the remainder of Lemma 3 belongs to the next page.',full=True)
 txt,_,_=page_text(rel,211)
 for a,b,_ in list(footnotes(txt)):
  r(txt[a:b],'','opening classification sentence','8-def-pi1','structure','This supplied explanatory footnote is absent from the printed page. Its justification is retained in the audit record, outside both text layers.')
 if tree=='fr_printed':
  r('revêtements non ramifiés peut se traduire','revêtements inséparables peut se traduire','opening classification sentence','8-def-pi1',why='The original prints inséparables. Corrected French retains non ramifiés, the category R(X) just defined; inseparable covers cannot be classified by these finite continuous group actions.')
  r(r'\result{LEMME}{3} Soit $X$',r'\result{LEMME}{3} Soit $Z$','Lemma 3 first line','8-lem3',why='The printed opening letter is Z. Corrected French retains X, used in H^0(X,O_X)=A and throughout all remaining hypotheses.')
 txt,_,_=page_text(rel,211)
 r(r'\Osh','O','Lemma 3 structure sheaves','8-lem3',why='All structure-sheaf O letters are plain.',count=txt.count(r'\Osh'))
 r(r'\textit{a priori}','a priori','Lemma 3 parenthesis','8-lem3',why='The parenthetical a priori is ordinary roman and ununderlined.')
 r('Évidemment','Evidemment','homotopy-sequence introduction','8',why='The capital E is unaccented in print.')
 r('foncteur covariant\nen le schéma pointé',r'\uline{foncteur covariant en le schéma pointé}','first two lines','8-def-pi1',why='The entire qualifying phrase is underlined.')
 r('des groupes topologiques).','des \\uline{groupes topologiques}).','end of first paragraph','8-def-pi1',why='The phrase groupes topologiques is underlined.')
 r('pour toute extension\nalgébrique','pour \\uline{toute} extension\nalgébrique','consequence of Lemmas 1–2','8-lem12-cor',why='Only toute is underlined in this assertion.')
 for n in [1,2,3]:
  txt,_,_=page_text(rel,211);marker='\\result{LEMME}{'+str(n)+'} ';a=txt.index(marker)+len(marker);b=txt.find('\n\n',a);b=len(txt) if b<0 else b;old=txt[a:b].rstrip()
  parts=re.split(r'(\([^)]*\)|\bsoit fini\b)',old,flags=re.S)
  # Parentheses inside inline formulas must not be treated as prose parentheses.
  parts=re.split(r'(\(muni du.*?\)|\(et est par suite injectif\)|\(i\.e\..*?\)|\(pouvant.*?\)|\(obtenus.*?\)|\(ainsi.*?\)|\bsoit fini\b)',old,flags=re.S)
  new=''.join(x if i%2 else underline_prose(x) for i,x in enumerate(parts))
  if n==1:new=new.replace('(et est par suite injectif)',r'(et est par suite \uline{injectif})')
  if n==3:new=new.replace(r'\uline{de} $X_0\otimes_k\Omega$',r'de $X_0\otimes_k\Omega$')
  r(old,new,'Lemma '+str(n)+' statement prose','8-lem'+str(n),why='Restore the selective underlining: explanatory parentheses are plain; Lemma 1 nevertheless underlines injectif, and Lemma 3 leaves soit fini and the final de plain.')
 upright_page(rel,layer,'182-211')
event('182-8-classification-slip','targeted proof check','The finite continuous pi_1-sets classify the nonramified coverings R(X) of the preceding page. Purely inseparable morphisms are not these coverings: e.g. in characteristic p the degree-p map of affine lines t -> t^p has one geometric point in every fiber and is not finite étale. Thus inséparables is incompatible with the asserted dictionary; confirmed the supplied non ramifiés repair only in corrected French. Removed its unprinted footnote from both layers.','182, p. 211, opening paragraph')
event('182-8-lem1','targeted proof check','For G=pi_1(X,a), the pointed component of a finite G-set E is the orbit G/H with H=Stab(e). Finite G-sets over that orbit correspond to finite H-sets by taking the fiber at e, with inverse G times_H (-). Under the covering/fiber equivalence this identifies pi_1 of the pointed covering component with H and its canonical map with the inclusion H -> G. This proves the assertion conditional on the Galois-category equivalence on page 210.','182, p. 211, Lemma 1')
event('182-8-lem2','carried as background without fault found','Read the unique descent of finite étale coverings under a purely inseparable field extension. A proof requires topological invariance of finite étale algebras under a radicial base change (or relative Frobenius for finite exponent) and passage to filtered limits for arbitrary algebraic extensions. These ingredients were identified but not independently proved in this page check.','182, p. 211, Lemma 2')
event('182-8-lem12-cor','targeted proof check','For a finite algebraic extension, separate the separable part, where base change is a finite étale covering and Lemma 1 applies, from the purely inseparable part, where Lemma 2 preserves the covering category. For an infinite algebraic extension use finite-presentation descent of finite étale covers and morphisms along its finite subextensions; the resulting fundamental group maps inject into the original one. The finite-presentation limit fact is used as background.','182, p. 211, consequence after Lemma 2')
event('182-8-lem3-premises','targeted proof check','The opening Z must be X: every subsequent structure sheaf, global-section condition and covering is attached to X. Corrected French retains X. Properness over Artinian A makes global sections of the finite covering algebra a finite A-module, giving the stated finiteness of A-prime. The equivalence and extra conclusions are deferred until their text on page 212.','182, p. 211, Lemma 3 hypotheses')
record_page('182',211,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 867–928 with scan leaf 20 at 400 dpi, full page and enlarged top, middle and bottom bands. Read the fundamental-group continuation, the homotopy-sequence programme, Lemmas 1–2 and their consequence, and the hypotheses of Lemma 3. Moved marker 212 before its first equivalent condition.

Printed French restores inséparables in the classification sentence and Z at the start of Lemma 3; corrected French retains the justified non ramifiés and X repairs. Removed the unprinted explanatory footnote while preserving its reason in this record and the check events. Restored plain structure O, ordinary a priori, unaccented Evidemment and the exact selective underlining, including Lemma 1's isolated injectif emphasis. Checked the stabilizer lemma and the algebraic-extension consequence conditional on the stated Galois and descent background. Lemma 2's deeper radicial invariance is explicitly marked as background; Lemma 3's conclusion has not yet been checked.''')
p='CHECK_RECORD.md';t=read(p).replace('## Open reading questions','- 182-211, fundamental-group dictionary: confirmed non ramifiés rather than printed inséparables; Lemma 3 retains X rather than its printed initial Z.\n\n## Open reading questions');write(p,t)
from update_record_counts import update
update()
