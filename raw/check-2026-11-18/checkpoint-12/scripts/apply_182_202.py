from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1,full=False):
  replace(rel,a,b,layer,'182-202',line,statement,'400-dpi scan with all three enlarged bands. '+why,kind,count=count,full=full)
 r('\\src{203}\n\\fsection{6}',r'\fsection{6}','page boundary','5','structure','Page 203 begins with the sheaf-of-groups sequence, before section 6.',full=True)
 r('exacte suivante de faisceaux de groupes\n\\[','exacte suivante de \\uline{faisceaux} de groupes\n\\src{203}\n\\[','last two lines','5-prop2-cor','structure','Restore underlining of faisceaux and place the page marker before the continuation display.',full=True)
 txt,_,_=page_text(rel,202)
 for a,b,body in list(footnotes(txt)):
  r(txt[a:b],'','Corollary 3 editorial note','5-thm7-cor3','structure','No footnote is printed. The retained corrected qualification is justified in the audit record instead.')
 if tree=='fr_printed':
  r('restrictions à $X_y$ sont isomorphes, sont isomorphes dans un voisinage de $X_y$.','restrictions à $X_y$ sont isomorphes, sont isomorphes.','Corollary 3 conclusion','5-thm7-cor3',why='The print omits the neighborhood qualification. It is retained in corrected French because pullbacks of different base line bundles give a counterexample to a global conclusion.')
  r('localement libre de rang au moins $2$ sur $Y$','localement libre sur $Y$','Proposition 2 hypothesis','5-prop2',why='The print has no rank restriction. Corrected French retains rank at least two: in rank one, P(E)=Y and the integer n is not unique.')
 else:
  r('dont des restrictions','dont les restrictions','Corollary 2, relative clause','5-thm7-cor2','misprint of the original','The scan prints des, but the clause refers to the two sheaves\u2019 restrictions to the specified fiber, as in the following corollary; les repairs the article.')
 txt,_,_=page_text(rel,202)
 r(r'\Osh','O','structure sheaves','5',why='The O letters are plain.',count=txt.count(r'\Osh'))
 r(r'\mathbf P','P','projective bundle notation','5-prop2',why='P is an ordinary upright letter, not bold.',count=txt.count(r'\mathbf P'))
 r(r'\Homsh_{O_{X_y}}',r'\mathop{\text{\uwave{Hom}}}\nolimits_{O_X}','Corollary 2 hypothesis','5-thm7-cor2',why='The Hom has a wavy underline and its subscript is O_X, acting through the fiber structure sheaf; the expanded base is unnecessary.')
 txt,_,_=page_text(rel,202)
 for expr in list(re.finditer(r'\\\[\s*(.*?)\s*\\\]',txt,re.S))[:3]:
  old=expr.group(0);body=expr.group(1).strip().replace('\n  ',' ');punct=''
  if body[-1:] in ',;':punct=body[-1];body=body[:-1]
  r(old,'$'+body+'$'+punct,'statement formula','5','structure','This formula is inline in the scan, with punctuation outside it.')
 r('suite exacte de groupes\n','suite exacte de groupes.\n','sentence before group sequence','5-prop2-cor',why='The sentence ends with a period before the displayed sequence.')
 for marker,sid in [(r'\result{COROLLAIRE}{2} ','5-thm7-cor2'),(r'\result{COROLLAIRE}{3} ','5-thm7-cor3'),(r'\result{PROPOSITION}{2} ','5-prop2'),(r'\result{COROLLAIRE}{} ','5-prop2-cor')]:
  txt,_,_=page_text(rel,202);a=txt.index(marker)+len(marker);b=txt.index('\n\n',a);old=txt[a:b]
  parts=re.split(r'(\(i\.e\..*?\)|,\s*où\s+)',old,flags=re.S)
  new=''.join(x if i%2 else underline_prose(x) for i,x in enumerate(parts))
  r(old,new,'statement prose',sid,why='Restore roman underlining, excluding mathematical letters, the i.e. parenthesis and où in Proposition 2.')
 upright_page(rel,layer,'182-202')
# Record the mathematical correction already present in the supplied corrected text.
with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 for old,new,line,sid,why in [
 ('sont isomorphes.','sont isomorphes dans un voisinage de X_y.','Corollary 3 conclusion','5-thm7-cor3','The printed conclusion lacks locality. Distinct pullbacks of line bundles on the base agree on the fixed fiber but need not agree globally; Corollary 2 proves precisely the retained local conclusion.'),
 ('localement libre sur Y','localement libre de rang au moins 2 sur Y','Proposition 2 hypothesis','5-prop2','No rank condition is printed. For rank one, P(E)=Y and twisting the base line bundle absorbs any n, so its asserted uniqueness fails; rank at least two makes the fiber degree unique.')]:
  w.writerow(['sources/fr/fr/182.tex','French corrected','182-202',line,sid,old,new,'Supplied corrected reading confirmed against 400-dpi page 202 and enlarged bands. '+why,'misprint of the original','low'])
event('182-5-thm7-cor2','targeted proof check','The fiber isomorphism between the two bundles lifts by Theorem 7; its corollary makes the lift an isomorphism after shrinking the base. The printed O_X subscript is valid for the fiber sheaves and is restored; the faulty article des is repaired to les only in corrected French.','182, p. 202, Corollary 2')
event('182-5-thm7-cor3','targeted proof check','For an invertible fiber sheaf its endomorphism sheaf is O_Xy, so Corollary 2 yields the neighborhood conclusion. A global interpretation is false: on X=P^1 x P^1 over Y=P^1, O_X and f^*O_Y(1) restrict identically to each fiber but differ globally (restrict along a section). Retained the supplied neighborhood correction; removed its explanatory footnote from the edition text.','182, p. 202, Corollary 3')
event('182-5-prop2','targeted proof check','On a projective-space fiber of positive dimension the degree n of an invertible sheaf is unique. Corollary 3 makes this degree locally constant; connectedness fixes n. L(-n) is fiberwise trivial and locally trivial over base neighborhoods; f_*O_X=O_Y identifies its transition units with base units, yielding L-prime and uniqueness. Rank one gives P(E)=Y and no unique n; retained the supplied rank-at-least-two qualification only in corrected French.','182, p. 202, Proposition 2 and proof')
event('182-5-prop2-cor','targeted proof check','A Y-automorphism preserves O(1) fiber degree and thus changes it by a base invertible sheaf; pushing forward gives the described E twist and its isomorphism class. Determinants of E tensor L-prime give (L-prime)^rank(E)=O_Y. The displayed group sequence follows from the scalar kernel and those twists admitting an isomorphism. The sheaf sequence continues on the next printed page.','182, p. 202, corollary to Proposition 2 and group sequence')
record_page('182',202,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 439–501 with scan leaf 11 at 400 dpi, full page and all enlarged bands. The actual page ends after the introductory phrase for the sheaf-of-groups sequence; moved marker 203 before that continuation and reserved it for the next page.

Restored plain P and O, wavy-underlined Hom with the valid O_X subscript, the three inline statement formulas, statement and final-word underlining and the period before the group sequence. Corrected the printed article des to les only in corrected French. Confirmed the existing local qualification of Corollary 3 by a product-projective-space counterexample to its global reading, and the rank restriction of Proposition 2 by the rank-one failure of uniqueness. Both qualifications are removed only from printed French; the unprinted explanatory footnote is removed from both. The Picard-group and automorphism deductions and determinant torsion argument were checked as recorded.''')
from update_record_counts import update
update()
