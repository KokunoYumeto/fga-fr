from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1,full=False):
  replace(rel,a,b,layer,'182-214',line,statement,'400-dpi full scan and three enlarged bands. '+why,kind,count=count,full=full)
 r('\\src{215}\n','','page boundary','8-thm11-cor3','structure','The page ends at géométriquement, in the following observation.',full=True)
 r("géométriquement trivial sur $\\overline F$ (ce qui sera vrai", "géométriquement\n\\src{215}\ntrivial sur $\\overline F$ (ce qui sera vrai",'last line','8-thm11-cor3','structure','Move marker 215 before trivial sur F-bar.',full=True)
 txt,_,_=page_text(rel,214)
 for a,b,_ in list(footnotes(txt)):
  r(txt[a:b],'','Corollary 3 subject','8-thm11-cor3','structure','Remove supplied footnote absent from the printed page; its reason is recorded in the audit.')
 if tree=='fr_printed':
  r("pour que\n$X'$ soit image inverse", "pour que\n$X$ soit image inverse",'Corollary 3, second line','8-thm11-cor3',why='Printed subject is X. The criterion concerns the connected cover X-prime just introduced; corrected French retains X-prime.')
 r('fibre géométrique de $X$). Le','fibre générique de $X$). Le','proof after Corollary 2','8-thm11-cor2',why='The scan clearly reads générique; this is the generic-fiber function-field argument.')
 r('corollaire 1 : le\nnoyau','corollaire 1 : Le\nnoyau','equivalent group formulation','8-thm11-cor1',why='Capital L after the colon.')
 old=r'''\[
  \overline{f^{-1}(y)}
  =f^{-1}(y)\otimes_{\kappa(y)}\overline{\kappa(y)},
\]
$\overline{\kappa(y)}$ désignant une clôture algébrique de $\kappa(y)$.'''
 new=r'''$\overline{f^{-1}}(y)$ désigne le schéma
$f^{-1}(y)\otimes_{k(y)}\overline{\varkappa(y)}$,
($\overline{\varkappa(y)}$ désignant une clôture algébrique de $\varkappa(y)$).'''
 r(old,new,'definition in the kernel paragraph','8-thm11-cor1','structure','The printed definition is prose with inline formulas and a parenthesized explanation, not a displayed equality. Its tensor subscript is the ordinary k(y), while the following residue-field letters are crossed kappa. Preserve this printed notation variant in both layers.')
 r(r'des $\pi_1(\overline{f^{-1}(y)})$',r'des $\pi_1(\overline{f^{-1}}(y))$','kernel generators','8-thm11-cor1',why='The printed overbar extends over f-inverse, not the following (y).')
 r(r'$\pi_1(\overline{f^{-1}(y)})\longrightarrow\pi_1(X)$',r'$\pi_1(f^{-1}(y))\longrightarrow\pi_1(X)$','base-point discussion','8-thm11-cor1',why='The printed source in this later homomorphism has no bar. This is also a valid statement of the inner-conjugacy ambiguity for ordinary fibers, so the supplied added bar is withdrawn in both layers rather than treated as a necessary repair.')
 r('pouvoir choisir le même',r'pouvoir \uline{choisir} le même','base-point discussion','8-thm11-cor1',why='Only choisir is underlined in this clause.')
 r('un morphisme séparable. Alors',r'un morphisme \uline{séparable}. Alors','paragraph before Corollary 3','8-thm11-cor3',why='The first séparable is underlined.')
 for a in [r'\textit{(i)}',r'\textit{(ii)}',r'\textit{(iii)}']:
  txt,_,_=page_text(rel,214);n=txt.count(a)
  if n:r(a,a[8:-1],'condition references','8-thm11',why='Roman references.',count=n)
 txt,_,_=page_text(rel,214);a=txt.index('\n')+1;b=txt.index(' (mais',a);old=txt[a:b];new=underline_prose(old).replace(r'\uline{tel que (*) soit',r'\uline{tel que} (*) \uline{soit');r(old,new,'Theorem 11 continuation','8-thm11',why='All theorem prose is underlined, except the parenthetical warning; (*) itself is plain.')
 for n in [1,2,3]:
  txt,_,_=page_text(rel,214);marker='\\result{COROLLAIRE}{'+str(n)+'} ';a=txt.index(marker)+len(marker);b=txt.find('\n\n',a);old=txt[a:b]
  parts=re.split(r'(\(i\)|\(d\x27où .*?\))',old,flags=re.S)
  new=''.join(x if i%2 else underline_prose(x) for i,x in enumerate(parts))
  r(old,new,'Corollary '+str(n)+' prose','8-thm11-cor'+str(n),why='Restore printed underlining, keeping (i), formulas and the d’où parenthesis plain.')
 for a in ["Le\nnoyau de l'homomorphisme",'est le sous-groupe invariant fermé engendré\npar les images dans']:
  r(a,r'\uline{'+a+'}','kernel formulation','8-thm11-cor1',why='Printed emphasis in the equivalent group formulation.')
 r("$\\overline F'$ soit\ngéométriquement", "$\\overline F'$ soit\n\\uline{géométriquement}",'last line','8-thm11-cor3',why='The final word is underlined; continuation checked next page.')
 upright_page(rel,layer,'182-214')
event('182-8-thm11','targeted proof check','Checked the formal-to-open argument conditional on Lemma 3: after completion at y, isolate the connected component indexed by y-prime_1 in the finite Stein algebra. Lemma 3 identifies the corresponding étale covering on each Artinian thickening with a geometrically constant cover. Compatible finite étale algebras and Theorem 2 identify its limit with the completed local Stein algebra and the comparison map with an isomorphism. Étaleness and the isomorphism then hold on a neighborhood, using finite presentation, faithful flatness of completion and properness to exclude the closed bad locus. The infinitesimal invariance and algebra descent inputs are background, not newly proved.','182, pp. 213–214, Theorem 11')
event('182-8-thm11-cor1','targeted proof check','Applying Theorem 11 at every component over every fiber makes the global comparison map an isomorphism and the Stein factor finite étale; converse follows by base change. An open good locus containing every closed point is all of a noetherian base, since a nonempty closed complement has a closed point. For G=pi_1(X), quotienting by the closed normal subgroup generated by geometric-fiber images selects exactly finite G-sets trivial on every geometric fiber, hence the same finite sets as pi_1(Y); surjectivity is Lemma 4. The unnamed cover in the first clause is implicitly X-prime; no extra binder was inserted. The later ordinary-fiber map is valid as printed without a bar, so its supplied added bar is withdrawn.','182, p. 214, Corollary 1 and following paragraph')
event('182-8-thm11-cor2','targeted proof check','Use the nonempty neighborhood of y-prime_1 in Theorem 11 and integrality: its isomorphism passes to generic points. The function field K-prime of the integral Stein factor is finite separable over K (étale on that nonempty neighborhood); the generic comparison identifies L-prime with L tensor_K K-prime. Since this tensor product is a field, L and K-prime are linearly disjoint and its multiplication image is LK-prime. The printed proof says fibre générique, not the supplied fibre géométrique; restored in both French layers.','182, p. 214, Corollary 2')
event('182-8-thm11-cor3','targeted proof check','With f separable, Proposition 4 makes the Stein factor Y-prime finite étale. By Lemma 4 its pullback X times_Y Y-prime is connected when X-prime is connected: equivalently its Stein algebra has no nontrivial idempotent. The comparison between finite étale X-covers has image open and closed; a section on one geometric fiber gives a degree-one component there. Theorem 11 gives an isomorphism near that Stein point, and finite étale degree is constant on the connected target, so the comparison is globally an isomorphism. Conversely a base pullback splits on a geometric fiber. The printed subject X must be X-prime. The notation F-bar=f-inverse(y) is retained as the stated geometric-fiber convention.','182, p. 214, Corollary 3')
record_page('182',214,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 1012–1066 with scan leaf 23 at 400 dpi and all three enlarged bands. Read the completion of Theorem 11, its three corollaries, the kernel formulation and base-point discussion, and the first line of the final observation. Marker 215 now falls after géométriquement.

Restored the inline prose definition of the geometric fiber, the printed bar extents, ordinary tensor subscript k(y) alongside crossed kappa, capital Le, roman condition references and selective underlining. The proof after Corollary 2 reads fibre générique, not géométrique; corrected both layers. The later ordinary-fiber homomorphism is printed without a bar; because its inner-conjugacy assertion remains valid, withdrew the supplied added bar in both layers. Printed French retains X in Corollary 3; corrected French retains the necessary X-prime. Removed the unprinted footnote. Targeted checks of Theorem 11 and all three corollaries are recorded with their descent/formal-comparison dependencies explicit; no proof of those background inputs is claimed.''')
p='CHECK_RECORD.md';t=read(p).replace('## Open reading questions','- 182-214, Corollary 2 proof: restored fibre générique in both layers; withdrew the unnecessary added bar in the later ordinary-fiber map; confirmed X-prime as Corollary 3 subject.\n\n## Open reading questions');write(p,t)
from update_record_counts import update
update()
