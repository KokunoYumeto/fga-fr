from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1,full=False):
  replace(rel,a,b,layer,'182-198',line,statement,'400-dpi scan and enlarged three bands; tight maximal-ideal crop where specified. '+why,kind,count=count,full=full)
 r('\\src{199}\n\\fsection{4}',r'\fsection{4}','printed page boundary','3-thm4','structure','Page 198 ends after on a in clause ii. Remove the late marker before section 4, then put it at the true boundary.',full=True)
 r('    on a\n    \\[\n      H^2','    on a\n\\src{199}\n    \\[\n      H^2','last line','3-thm4-ii','structure','The next printed page starts with the H^2 formula, not with section 4.')
 r(r'\emph{sous-catégorie}',r'\uline{sous-catégorie}','first paragraph','3-thm3',why='The term is underlined.',count=2)
 r('séparé et complet.]','séparé et complet].','end of bracketed reminder','3-thm3',why='The final period follows the square bracket.')
 r(r'$\Osh_X$, resp.',r'$\Osh_X$ resp.','proof of Corollary 1','3-thm3-cor1',why='No comma precedes resp.')
 txt,_,_=page_text(rel,198)
 r(r'\Osh','O','structure-sheaf letters','3',why='The O symbols are plain, not underlined.',count=txt.count(r'\Osh'))
 if tree=='fr_printed':
  r(r'\overline{O}_X','O_X','proof of Corollary 1, second structure sheaf','3-thm3-cor1',why='The scan omits the completion bar on the second O_X. Corrected French retains it: the second category is on the completed space.')
 r(r'propres au-dessus de $A$'+'\n(anneau',r'propres au-dessus de $A$,'+'\n(anneau','Corollary 2, first line','3-thm3-cor2',why='A comma precedes the parenthesis.')
 r(r'g\longmapsto\overline g',r'g\longrightarrow\overline g','Corollary 2 map','3-thm3-cor2',why='The print uses an ordinary arrow without a starting bar.')
 r(r'\mathfrak m(A)',r'\mathfrak r(A)','Theorem 4, adic topology','3-thm4',why='The tight crop shows a single Gothic r-shaped stem, not m. This is the radical/maximal-ideal notation of the local ring.')
 r('On suppose :','On suppose','Theorem 4 introduction','3-thm4',why='No colon follows suppose.')
 # The theorem and corollary prose is underlined, except their parenthetical reminders.
 txt,_,_=page_text(rel,198)
 for marker,ending,sid in [(r'\result{THÉORÈME}{3} ',' (déterminé','3-thm3'),(r'\result{COROLLAIRE}{1} ','\n\n','3-thm3-cor1'),(r'\result{COROLLAIRE}{2} ','\n(anneau','3-thm3-cor2'),(r'\result{THÉORÈME}{4} ',' (muni','3-thm4')]:
  txt,_,_=page_text(rel,198);a=txt.index(marker)+len(marker);b=txt.index(ending,a);old=txt[a:b]
  r(old,underline_prose(old),'statement prose',sid,why='The scan underlines the prose and leaves mathematical symbols outside the underline.')
 old=r'''Alors l'application
$g\longrightarrow\overline g$ définit une correspondance biunivoque entre les
$Y$-morphismes de $X$ dans $Z$, et les $\overline Y$-morphismes de
$\overline X$ dans $\overline Z$.'''
 r(old,underline_prose(old),'Corollary 2, assertion','3-thm3-cor2',why='The assertion after the parenthesis is underlined.')
 r(r'''les schémas algébriques propres sur $A$ apparaissent comme
une \uline{sous-catégorie}''',r'''\uline{les schémas algébriques propres sur} $A$ \uline{apparaissent comme
une sous-catégorie}''','paragraph after Corollary 2','3-thm3-cor2',why='The underline covers the entire categorical assertion before its parenthesis.')
 old=r'''qu'il existe des schémas formels propres sur $\overline Y$ qui ne
sont pas « algébrisables »'''
 r(old,r'''\uline{qu'il existe des schémas formels propres sur} $\overline Y$ \uline{qui ne
sont pas \fquote{algébrisables}}''','nonalgebraizability paragraph','3-nonalgebraizable',why='This whole assertion is underlined, including the ordinary double quotes around algébrisables.')
 r('« théorie des\nmodules »',r'\uline{\fquote{théorie des'+'\n'+r'modules}}','same paragraph, moduli','3-nonalgebraizable',why='The quoted phrase is underlined.')
 for numeral in ['i','ii']:
  r(r'\item[\textit{'+numeral+'.}]',r'\item[\textnormal{'+numeral+'.}]','Theorem 4 clause '+numeral,'3-thm4-'+numeral,why='The list marker is roman.')
 txt,_,_=page_text(rel,198);a=txt.index(r'\item[\textnormal{i.}]')+len(r'\item[\textnormal{i.}]');b=txt.index(r'\[',a);old=txt[a:b]
 new=underline_prose(old).replace('modules plats sur','modules} plats \\uline{sur}')
 r(old,new,'Theorem 4(i), prose','3-thm4-i',why='All the defining prose is underlined except the word plats and the mathematical letters.')
 r(r'''\[
      \operatorname{gr}(O_{\mathfrak X})
      \simeq
      \operatorname{gr}^{0}(O_{\mathfrak X})
      \otimes_k\operatorname{gr}(A).
    \]''',r'''$\operatorname{gr}(O_{\mathfrak X})\simeq
      \operatorname{gr}^{0}(O_{\mathfrak X})\otimes_k\operatorname{gr}(A)$.''','Theorem 4(i), graded relation','3-thm4-i','structure','The relation is in the running sentence at its next line, not a centered display.')
 txt,_,_=page_text(rel,198);a=txt.index(r'\item[\textnormal{ii.}]')+len(r'\item[\textnormal{ii.}]');old=txt[a:]
 r(old,underline_prose(old),'last line, Theorem 4(ii)','3-thm4-ii',why='The clause introduction is underlined, excluding the formula and k.')
 upright_page(rel,layer,'182-198')
event('182-3-thm3','carried as background without fault found','Read the existence theorem with its properness and complete noetherian affine-base hypotheses carried from the preceding paragraphs. Canonical uniqueness is understood relative to the chosen identification of the completion; no textual strengthening is inserted. The proof is not on this page.','182, p. 198, Theorem 3')
event('182-3-thm3-cor1','targeted proof check','Closed subschemes correspond to coherent ideal submodules of O_X. The completed ideal submodules live in completed O_X, so the scan’s second unbarred O_X is a missing completion mark. The equivalence of coherent categories is exact and fully faithful and sends O_X to its completion, yielding the correspondence of subobjects.','182, p. 198, Corollary 1 and its proof')
event('182-3-thm3-cor2','carried as background without fault found','Read the stated graph deduction and full-faithfulness assertion for proper schemes over the complete base. Completing graphs gives the indicated direction; algebraizing a formal graph and proving its projection is an isomorphism requires the effectivity argument, not supplied in full here.','182, p. 198, Corollary 2')
event('182-3-nonalgebraizable','carried as background without fault found','Read the assertion that proper formal schemes need not algebraize and its moduli motivation. No example or independent proof is given here.','182, p. 198, paragraph after Corollary 2')
event('182-3-thm4','carried as background without fault found','Read the complete-local-base hypotheses and clause (i), with its canonical graded-flatness criterion. The handwritten maximal-ideal notation is Gothic r(A). Clause (ii) and the conclusion continue on page 199; no theorem verdict is claimed yet.','182, p. 198, Theorem 4 through start of clause ii')
record_page('182',198,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 243–320 with scan leaf 7 at 400 dpi and all enlarged bands. The source’s page-199 marker was too late; moved it to immediately before condition (ii)’s H^2 formula, which is not on page 198. Only the text actually on this scan page is adjudicated here. Inspected every completion bar, formal Gothic X, exponent, tensor index and the maximal-ideal symbol; the correctly placed tight crop confirms Gothic r(A), replacing supplied m(A).

Restored all printed underlining, two punctuation readings, the ordinary arrow g→barred g, the inline graded relation, roman i/ii and the ununderlined word plats. The printed proof of Corollary 1 omits the completion bar on its second O_X; restored that omission in printed French, retaining the needed bar in corrected French. Theorems 3 and 4 are not claimed independently proved. The subobject deduction of Corollary 1 was checked from the stated exact equivalence; the graph argument and nonalgebraizability assertion remain background at this point.''')
from update_record_counts import update
update()
