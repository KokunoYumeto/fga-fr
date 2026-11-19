from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-301',line,statement,'400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 r('de faisceaux de modules. On obtient',r'\uline{de faisceaux de modules}. On obtient','first line','Example 2',why='The underlining continues across the source-page boundary.')
 r(r'\mathcal C',r'\text{\uwave{C}}','category letter occurrences','1.2–1.4',why='Ordinary C with a wavy underline in each occurrence.',count=5)
 r(r'\emph{exact}',r'\uline{exact}','exactness defining terms','1.2; 1.3',why='Underlining rather than italics.',count=2)
 r('$\\text{\\uwave{C}}$ ; considérons','$\\text{\\uwave{C}}$, considérons','opening clauses','1.3; 1.4',why='Comma, not semicolon, after the category letter.',count=2)
 r(r'\overset{\beta_1}{\underset{\beta_2}{\rightrightarrows}}',r'\overset{\beta_1}{\underset{\beta_2}{\leftleftarrows}}','base diagram (+)','1.3',why='Both arrows point from S-double-prime to S-prime in the scan; the supplied pair was reversed.')
 r('exact} si, pour','exact} si pour','definition of F-exact','1.3',why='No comma after si.')
 r(r"\tag{+'}",r'\tag{+}','Hom diagram tag','1.3',why='The second diagram is also labeled (+); there is no prime. This repeated schematic label is retained in both layers.')
 r(r'\operatorname{Hom}(\alpha^*\xi,\alpha^*\eta)',r'\operatorname{Hom}(\alpha^*(\xi),\alpha^*(\eta))','middle Hom term','1.3',why='Parentheses around each pulled-back object are printed.')
 r(r'\operatorname{Hom}(\gamma^*\xi,\gamma^*\eta),',r'\operatorname{Hom}(\gamma^*(\xi),\gamma^*(\eta))','last Hom term','1.3',why='Parentheses are printed; no comma follows the display.')
 r('où $\\gamma=\\alpha\\beta_1=\\alpha\\beta_2$, est exact. Dans ce dernier', '(où $\\gamma=\\alpha\\beta_1=\\alpha\\beta_2$) est exact.\n\nDans ce dernier','after Hom diagram','1.3',kind='structure',why='The explanatory clause is parenthetical without a following comma; Dans begins a new paragraph.')
 if tree=='fr_printed':
  r('(où $','(ou $','parenthesis after Hom diagram','1.3',why='The printed ou has no grave accent; corrected French retains grammatical où.')
 r(r'$(\alpha\beta_i)^*=\gamma^*$',r'$(\alpha\beta_1)^*=\gamma^*$','identification explanation','1.3',why='The subscript in the parenthesized composite is numeral 1, although the preceding beta and coherence c have i. This is still the same composite gamma for both i, so no semantic correction is needed.')
 r("morphismes $\\beta_1,\\beta_2$ de $S''$ dans\n$S'$, dans", "morphismes $\\beta_1,\\beta_2:S''\\longrightarrow S'$ dans",'Definition 1.4 opening morphisms','1.4',why='The scan gives a colon and arrow, not an expanded prose description.')
 r(r'\emph{donnée de recollement}',r'\uline{donnée de recollement}','defining term','1.4',why='Underlined.')
 r(r'(relativement au couple $(\beta_1,\beta_2)$) un',r'(relativement au couple $(\beta_1,\beta_2)$), un','parenthesis before isomorphism','1.4',why='Comma after the parenthesis.')
 r(r'\emph{compatible avec les données de recollement}',r'\uline{compatible avec les données de recollement}','compatibility defining term','1.4',why='Underlined.')
 old=r'''\begin{array}{ccc}
  \beta_1^*(\xi') & \longrightarrow & \beta_2^*(\xi') \\
  \big\downarrow && \big\downarrow \\
  \beta_1^*(\eta') & \longrightarrow & \beta_2^*(\eta').
\end{array}'''
 new=r'''\begin{array}{ccc}
  \symup{\beta_1^*(\xi')} & \longrightarrow & \symup{\beta_2^*(\xi')} \\
  \big\downarrow && \big\downarrow \\
  \symup{\beta_1^*(\eta')} & \longrightarrow & \symup{\beta_2^*(\eta')}
\end{array}'''
 r(old,new,'compatibility square','1.4',why='No terminal period; all indices, primes and arrow directions agree with the print.')
 r('forment alors une catégorie.','forment alors une \\uline{catégorie}.','paragraph following square','1.4',why='The word catégorie is underlined.')
 if tree=='fr_printed':
  r(r'alors pour tout $\xi\in\mathcal F_S$',r"alors pour tout $\xi\in\mathcal F_{S'}$",'last line, object before pullback','1.4',why='The scan has S-prime. Corrected French keeps S because alpha-star has domain F_S.')
 upright_page(rel,layer,'190-301')
# Explicitly record confirmed original corrections even where the supplied corrected source already has the right reading.
for line,old,new,why in [('parenthesis after Hom diagram','(ou gamma...)','(où gamma...)','The scan prints unaccented ou; the relative adverb in this parenthetical identification is où.'),('last line, object before pullback',r'\xi\in\mathcal F_{S\prime}',r'\xi\in\mathcal F_S',r'For alpha:S-prime -> S, alpha-star has domain F_S and codomain F_S-prime. The input xi must be in F_S. The printed extra prime is visible in the bottom band.')]:
 with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
  csv.writer(f,delimiter='\t').writerow(['sources/fr/fr/190.tex','French corrected','190-301',line,'1.3' if line.startswith('parenthesis') else '1.4',old,new,'Confirmed supplied corrected reading against the 400-dpi scan. '+why,'misprint of the original','low'])
event('190-1.2','targeted proof check','The definition identifies E by u with the equalizer of v1 and v2. It imposes both injectivity and surjectivity onto the equalizing subset, exactly as needed for unique descent of morphisms.','190, p. 301, Definition 1.2')
event('190-1.3','targeted proof check','Checked variance and domains: beta_i:S-double-prime -> S-prime, alpha:S-prime -> S, so pullbacks on Hom go to the right. Both composites alpha beta_i equal gamma. The coherence c(beta_i,alpha) identifies the pullbacks; writing alpha beta_1 in the explanatory equality is valid for both i. Restored the leftward base arrows in both French layers.','190, p. 301, Definition 1.3')
event('190-1.4','targeted proof check','Checked the compatibility square and closure of compatible maps under composition and identities. At the page foot the print assigns xi to F_S-prime although alpha-star takes F_S to F_S-prime; retain the supplied correction F_S only in corrected French. The canonical gluing construction continues on p. 302.','190, p. 301, Definition 1.4')
record_page('190',301,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 100–158 with scan leaf 4 at 400 dpi and the three enlarged bands. Read the continuation of Example 2, Definitions 1.2–1.4, every symbol of the three linear diagrams and the compatibility square, and the last-line object and pullback. The next-page marker is correct.

Restored underlined terminology, ordinary wavy-underlined C, printed commas and parentheses, the two leftward beta arrows in the base diagram, the repeated (+) tag without the added prime, parentheses around pulled-back objects in the Hom diagram, the new paragraph before Dans, the numeral 1 in the explanatory composite alpha beta_1 (valid since both composites equal gamma), the arrow notation in Definition 1.4, and the omitted category underline. Removed the unprinted period after the square. Typed Latin letters are upright.

Confirmed two supplied corrected readings against the print: où rather than the printed ou, and xi in F_S rather than the printed F_S-prime on the final line. The latter is forced by the domain of alpha-star; the printed prime is restored only in the as-printed layer. Exactness as an equalizer, variance of the induced Hom arrows, and composition of compatible gluing maps were explicitly checked. No cocycle condition has yet been imposed at this stage of the author's definition.''')
from update_record_counts import update
update()
