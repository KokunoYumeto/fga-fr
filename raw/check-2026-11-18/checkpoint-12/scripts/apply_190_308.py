from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-308',line,statement,'400-dpi full scan, all three enlarged bands, and the tight conditions crop. '+why,kind,count=count)
 r('\\subsection*{3. Application aux étalements}\n\\addcontentsline{toc}{subsection}{3. Application aux étalements}\n\n', '\\addcontentsline{toc}{subsection}{3. Application aux étalements}\n\\result{3. \\uline{Application aux étalements}}{} ', 'section 3 run-in heading','3',kind='structure',why='Roman underlined heading, followed by period-dash and the first sentence on the same line.')
 for term in ['étalé','étale','étalement','revêtement étale','revêtements étales']:
  r('\\emph{'+term+'}','\\uline{'+term+'}','defining term '+term,'3',why='Printed underline.')
 for term in ['étale en $x\\in T$','étalé sur $S$ en $x$','étalé sur $S$']:
  r('\\emph{'+term+'}',underline_prose(term),'defining phrase '+term,'3',why='Underline only the prose, excluding the variables.')
 for term in ['non ramifié','main theorem','pleinement fidèle']:
  r('« '+term+' »',r'\fquote{'+term+'}','quoted phrase '+term,'3',why='Double quotation marks in the print.')
 r('$B$ est plat sur $A$ ;','$B$ est plat sur $A$','condition (i)','3',why='No semicolon is printed. The B has a broken lower bowl; it is not changed to E or P.')
 if tree=='fr_printed':
  r('(où $\\mathfrak m$','(ou $\\mathfrak m$','condition (ii) parenthesis','3',why='The print omits the accent on où.')
 r(r'\widehat A\longrightarrow\widehat B',r'\overline A\longrightarrow\overline B','completion comparison','3',why='Straight bars over A and B, not hats.')
 r(r'\mathcal O',r'\text{\uwave{O}}','two local rings','3',why='Ordinary O with wavy underline.',count=2)
 r('étale}, ou encore','étale} ou encore','étale terminology','3',why='No comma here in the print.')
 r("Remarquons d'ailleurs que, si $S$","Remarquons d'ailleurs que si $S$",'étale-locus condition','3',why='No comma after que.')
 r('au sens de Serre','au sens de SERRE','analytic-space attribution','3',why='Uppercase surname.')
 r('i.e.','i. e.','four explanatory abbreviations','3',why='Spaced abbreviation.',count=4)
 r("que, si $T,T'$", "que si $T,T'$",'analytic Hom comparison','3',why='No comma after que.')
 r("\\overline{T'}", "\\overline T'",'analytic Hom comparison target','3',why='The bar is above T only, with the prime outside it.')
 r(r'T\longmapsto\overline T',r'T\longrightarrow\overline T','analytic functor assignment','3',why='Ordinary arrow without mapsto bar.')
 r('Grauert--Remmert [2] implique que, si','GRAUERT-REMMERT [2] implique que si','normal-case theorem attribution','3',why='Uppercase names, short hyphen, no comma after que.')
 r('revêtements étales (finis)','revêtements étales (\\uline{finis})','analytic covering category','3',why='Finis is underlined.')
 if tree=='fr_printed':
  r('de $\\overline S$, i. e. que tout','de $S$, i. e. que tout','analytic covering category','3',why='This occurrence of S visibly lacks its bar. Corrected French retains the bar because the category is the analytic one.')
 old='théorème de Grauert--Remmert reste valable sans hypothèse de normalité sur\n$S$'
 new='théorème de Grauert-Remmert reste valable sans hypothèse de normalité sur\n$S$'
 r('\\emph{'+old+'}',underline_prose(new),'extension beyond the normal case','3',why='Underlined prose, mixed-case names with short hyphen, S outside underline.')
 upright_page(rel,layer,'190-308')
with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 writer=csv.writer(f,delimiter='\t')
 writer.writerow(['sources/fr/fr/190.tex','French corrected','190-308','condition (ii) parenthesis','3','(ou $\\mathfrak m$','(où $\\mathfrak m$','Confirmed the supplied accent against the unaccented ou visible in the tight conditions crop; this introduces the explanation of the maximal-ideal symbol, not an alternative.','misprint of the original','low'])
 writer.writerow(['sources/fr/fr/190.tex','French corrected','190-308','analytic covering category','3','de $S$, i. e. que tout','de $\\overline S$, i. e. que tout','Confirmed the supplied bar against its visible omission in the bottom crop. The sentence compares algebraic covers of S with analytic covers of S-bar, and its next clause explicitly describes a cover of S-bar.','misprint of the original','low'])
event('190-3-local-etale-completion','targeted proof check','For noetherian local A,B with algebraically closed residue field k, (ii) gives B/mB=k and hence n=mB. Flatness identifies the associated gradeds of A and B, so induction on the powers identifies their completions. Conversely an isomorphism of the completions identifies the maximal ideal with m in the completed B; faithful flatness of B -> B-hat descends n=mB and the common residue k. Flatness of A -> B-hat=A-hat, together with faithful flatness over B, descends flatness to A -> B. This uses the noetherian completion flatness theorem as background.','190, p. 308, conditions (i)–(ii) and completion paragraph')
event('190-3-etale-local-structure','carried as background without fault found','Read the local-ring and finite-type definitions, openness of the étale locus, and the stated use of Zariski main theorem to obtain a local standard equation. These require finite-presentation/flatness and unramified local-structure results. No complete new proof of Zariski main theorem or analytic local comparison was attempted.','190, p. 308, first paragraph')
event('190-3-analytic-full-faithfulness','targeted proof check','Checked the reduction of full faithfulness to connected-component comparison. A map between analytic spaces étale over S-bar has graph open and closed in the analytic fiber product because the algebraic schemes are separated and the relative diagonal is open and closed. Using the background fact that connected components of finite-type complex schemes and their analytifications agree, that graph comes from an algebraic open-and-closed subscheme. Its projection is étale and analytically an isomorphism, hence an isomorphism by the degree-one étale criterion. This gives the unique algebraic map. The connectedness comparison and analytification criterion are background inputs, not re-proved here.','190, p. 308, Hom comparison')
event('190-3-grauert-remmert','carried as background without fault found','Read the quoted normal-case finite-cover equivalence and the proposed removal of normality. The reduction begins at the page foot and continues on 309. Restored the missing analytic-base bar only in corrected French. The cited external theorem is an input of the printed argument; its paper has not been consulted during this text check.','190, p. 308, final paragraph')
record_page('190',308,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 486–539 with scan leaf 11 at 400 dpi, full page, all three enlarged bands and an additional tight crop of conditions (i)–(ii). Read every completion/analytification bar, local-ring subscript, prime and arrow. The thin/broken B in (i) is retained as B; the clearer B forms nearby and the lower-bowl trace support that reading.

Restored the run-in roman underlined heading, selective term/prose underlines, double quotes, no semicolon after (i), straight completion bars rather than hats, wavy-underlined local O, printed comma omissions, uppercase SERRE and GRAUERT-REMMERT, short hyphens, spaced i. e., prime outside the Hom target bar, ordinary functor-assignment arrow and underlined finis. Printed French restores ou without its accent and S without its analytic bar at the two visible omissions; corrected French retains the supplied où and S-bar, now with explicit correction rows.

Checked the completion characterization using noetherian completion flatness as background, and the graph reduction for analytic full faithfulness using connected-component comparison. The openness/local-equation assertions and normal Grauert-Remmert theorem remain stated background inputs. The nonnormal reduction is not certified before its continuation. The marker for 309 correctly falls after supposons le.''')
from update_record_counts import update
update()
