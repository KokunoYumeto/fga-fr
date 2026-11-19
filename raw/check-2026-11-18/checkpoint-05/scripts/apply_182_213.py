from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1,full=False):
  replace(rel,a,b,layer,'182-213',line,statement,'400-dpi full scan and enlarged top, middle and bottom crops. '+why,kind,count=count,full=full)
 r('\\src{214}\n','','page boundary','8-thm11','structure','Theorem 11 continues on the next page after y-prime_1.',full=True)
 r("de $y'_1$ dans $Y'$, tel que", "de $y'_1$\n\\src{214}\ndans $Y'$, tel que",'last line','8-thm11','structure','Move marker 214 before dans Y-prime.',full=True)
 txt,_,_=page_text(rel,213)
 for a,b,_ in list(footnotes(txt)):
  r(txt[a:b],'','after second natural morphism','8-thm11','structure','This supplied editorial footnote is not printed; its mathematical reason is recorded outside the text.')
 if tree=='fr_printed':
  r("$X'\\longrightarrow Y'$ ;", "$X\\longrightarrow Y'$ ;",'after display (*)','8-thm11',why='The printed second arrow starts at X without its prime. The map to the Stein factor is from X-prime, retained in corrected French.')
  r("(non ramifié si $X'$ l'est)","(non ramifié si $X$ l'est)",'fiber F-prime paragraph','8-thm11',why='The print omits the prime on X in the parenthesis. The antecedent is the finite covering X-prime of X; corrected French retains the prime.')
 txt,_,_=page_text(rel,213)
 r(r'\Osh','O','structure sheaves','',why='Plain O, not underlined.',count=txt.count(r'\Osh'))
 r(r'\kappa',r'\varkappa','fiber F residue field','8-thm11',why='Crossed handwritten kappa.')
 r("$Y'$ de $Y$ associé à $f_*(O_X)$ est non ramifié.","$Y'$ \\uline{de} $Y$ \\uline{associé à} $f_*(O_X)$ est non ramifié.",'first line','8-prop4',why='Only de and associé à are underlined in this continuation.')
 r(r'\emph{séparable}',r'\uline{séparable}','Remark terminology','8-rem',why='Underlined séparable.')
 r(r'\emph{simple}','simple','Remark terminology','8-rem',why='The parenthetical simple is plain, without underline.')
 r('« absolument\nnormal »',r'\fquote{absolument normal}','Remark last sentence','8-rem',why='Ordinary double quotation marks.')
 r('« théorème de Bertini »',r'\uline{\fquote{théorème de Bertini}}','Remark last sentence','8-rem',why='Underlined quoted phrase, with ordinary double quotation marks.')
 r('f_*(O_X)=O_Y,\n', 'f_*(O_X)=O_Y\n','display (i)','8-thm11',why='No comma is printed after display (i).')
 r('(cf. théorème 5)','(cf théorème 5)','first Stein-factor reference','8-thm11',why='No period after this printed cf.')
 r('(cf. lemme 3).','(cf. lemme 3)','condition iii','8-thm11',why='No terminal period after the closing parenthesis.')
 for a,b in [(r'\textit{(ii)}','(ii)'),(r'\textit{(iii)}','(iii)')]:
  r(a,b,'conditions ii–iii','8-thm11',why='Printed roman condition labels.')
 txt,_,_=page_text(rel,213);marker=r'\result{THÉORÈME}{11} ';a=txt.index(marker)+len(marker);old=txt[a:].rstrip();r(old,underline_prose(old),'last line','8-thm11',why='The introductory prose and de are underlined; U-prime and y-prime_1 remain plain.')
 upright_page(rel,layer,'182-213')
event('182-8-prop4','targeted proof check','Work locally after completed strict henselization of the base, using faithful flat descent. The finite separable fiber-section algebra becomes a product k^r; its idempotents decompose every infinitesimal thickening into r open-and-closed pieces. On each piece H^0 of the closed fiber is k. Flatness gives the successive ideal sheaf (m^n/m^(n+1)) tensor O_F. Inductively constants identify H^0 of each thickening with A/m^(n+1): constants lift every section of the previous thickening, and the kernel is m^n/m^(n+1). Formal comparison (Theorem 2) identifies the completed Stein algebra with A^r. Thus it is finite étale locally and descends. Used as background: completed strict henselization, flat base change for H^0, and descent of finite étaleness.','182, pp. 212–213, Proposition 4')
event('182-8-separable-simple-open','carried as background without fault found','Read the historical definitions: flat finite-type morphisms with geometrically reduced fibers are called separable, and those with geometrically regular fibers simple. The asserted openness of the geometrically reduced, regular and normal fiber loci needs the corresponding finite-presentation openness theorems; no independent proof is claimed. Preserve the historical terminology rather than modernizing the text.','182, p. 213, Remark')
event('182-8-thm11-setup','targeted proof check','Checked the map (*) by its two components: X-prime -> X is given and X-prime -> Y-prime is the Stein factor map. The printed source X in the second arrow is a missing prime. If X-prime=X times_Y Y-double-prime with finite étale Y-double-prime, flat base change for the proper direct image and f_*O_X=O_Y identify its Stein factor with Y-double-prime, so (*) is the identity under this identification. The fiber-cover parenthesis likewise needs X-prime, not printed X. The theorem itself continues on page 214.','182, p. 213, display (*) and following paragraph')
record_page('182',213,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 963–1021 with scan leaf 22 at 400 dpi and its three enlarged bands. Read the conclusion and proof indication of Proposition 4, the terminology remark, the construction and hypotheses of Theorem 11, and its opening line. Marker 214 now precedes dans Y-prime in Theorem 11.

Restored selective underlining, plain O, crossed kappa, roman conditions, ordinary quotation marks, and the printed punctuation of (i), cf théorème 5 and condition (iii). Removed the unprinted explanatory footnote. Printed French retains X as the source of the second natural morphism and in the parenthesis non ramifié si X l'est; corrected French retains X-prime in both, justified by the Stein construction and the finite covering's domain. Checked Proposition 4 by the formal-thickening argument recorded in CHECK_EVENTS.tsv, with background dependencies explicit; checked the base-change identity for (*). The openness assertions in the remark are recorded as background. Theorem 11's conclusion has not yet been read.''')
p='CHECK_RECORD.md';t=read(p).replace('## Open reading questions','- 182-213, map to the Stein factor and fiber-cover parenthesis: confirmed X-prime in both places rather than printed X.\n\n## Open reading questions');write(p,t)
from update_record_counts import update
update()
