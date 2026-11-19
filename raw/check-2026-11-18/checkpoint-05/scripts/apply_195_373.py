from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/195.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'195-373',line,'A.2–3','400-dpi full scan and three enlarged bands. '+why,kind,count=count)
 r('un isomorphisme unique près (au sens usuel',r'\uline{un isomorphisme unique près} (au sens usuel','strict-system uniqueness',why='Printed selective underline.')
 r("Il en résulte que dans\n$\\operatorname{Pro}(\\mathcal C)$ la limite projective d'un système projectif de\npro-objets stricts $\\widetilde X^{(\\alpha)}$ existe toujours", "Il en résulte que \\uline{dans}\n$\\operatorname{Pro}(\\mathcal C)$ \\uline{la limite projective d'un système projectif de pro-objets stricts} $\\widetilde X^{(\\alpha)}$ \\uline{existe toujours}",'inverse-limit existence emphasis',why='Restore the printed underlined prose spans, leaving the mathematical symbols separate.')
 r('$F$, $\\overline F$, on aura','$F$, $\\overline F$ on aura','formula introduction',why='The second comma is absent from the print.')
 r(r'\overline F\left(\varprojlim_\alpha\widetilde X^{(\alpha)}\right)',r'\overline F(\varprojlim_\alpha\widetilde X^{(\alpha)})','first limit formula parentheses',why='The print uses ordinary-sized parentheses.')
 r(r'\overline F\left(\widetilde X^{(\alpha)}\right).',r'\overline F(\widetilde X^{(\alpha)})','second limit formula punctuation',why='Ordinary parentheses and no terminal period.')
 r("\\varprojlim_{\\alpha,\\mathcal C'}", "\\underset{\\alpha}{\\varprojlim}\\nolimits_{\\mathcal C'}",'right-hand limit indices',why='Alpha is beneath the arrow; the category label is separately to its right.')
 r('est strict (cf.','est strict, (cf.','strictness parenthesis',why='Restore the printed comma before the parenthesis.')
 r(r'\subsection*{3. Caractérisation des foncteurs pro-représentables}',r'\subsection*{\normalfont 3. \uline{Caractérisation des foncteurs pro-représentables}.}','section heading',why='Roman underlined heading with a period.')
 r('(i.e. relatives','(i. e. relatives','finite-limit parenthesis',why='Printed abbreviation spacing.')
 r("en particulier l'existence", "en particulier, l'existence",'terminal-object parenthesis',why='Restore the printed comma.')
 r('« objet unité à droite »',r'\fquote{objet unité à droite}','terminal-object phrase',why='The print uses ordinary double quotation marks.')
 for number in ['i','ii','iii']:
  r(r'\item[('+number+r')]',r'\item['+number+r'.]','equivalence item '+number,why='Printed roman item number followed by a period, without parentheses.')
 r('([3], A, définition 2.1),','([3], A, définition 2, 1)','exact-diagram reference',why='The reference has a comma between 2 and 1, and no comma after the parenthesis.')
 r(r'\emph{exact à gauche}',r'\uline{exact à gauche}','defined term',why='Printed underline, not italic.')
 r('dans $\\mathcal C$ les limites projectives finies\nexistent.','dans $\\mathcal C$, les limites projectives finies existent.','standing assumption punctuation',why='Restore the printed comma after the category.')
 r("qu'un foncteur\npro-représentable est exact à gauche.","qu'\\uline{un foncteur pro-représentable est exact à gauche}.",'pro-representability implication',why='The entire concluding claim is underlined.')
 if tree=='fr_printed':
  r(r'\overline F(\varprojlim_\alpha\widetilde X^{(\alpha)})',r'\overline F(\varprojlim_\alpha\widetilde X^{(\alpha)}','left side closing parenthesis',why='The print omits the closing parenthesis of the outer F-bar application.')
  r(r'\overline F(\widetilde X^{(\alpha)})',r'F(\widetilde X^{(\alpha)})','right-side functor bar',why='The print has an unbarred F here.')
  r(r'F(\widetilde X^{(\alpha)})',r'F(X^{(\alpha)})','right-side pro-object underline',why='This printed X lacks the wavy underline present in the argument on the left.')
  r("X\\longrightarrow X'\\rightrightarrows X''", "X'\\longrightarrow X'\\rightrightarrows X''",'first exact diagram initial object',why='The first printed object is X-prime, duplicating the middle object; the transformed diagram below begins F(X).')
  r(r'soient $X\in\mathcal C$',r'soient $X\in C$','last-line category identifier',why='The last printed C lacks its wavy underline.')
 for token,new,line in [(r'\mathcal C',r'\text{\uwave{C}}','category letters'),(r'\widetilde X',r'\text{\uwave{X}}','pro-object letters'),(r'\varprojlim_\alpha',r'\varprojlim\limits_\alpha','left-hand inverse-limit index')]:
  s,_,_=page_text(rel,373)
  r(token,new,line,count=s.count(token),why='Restore wavy category/pro-object letters and the index beneath the limit arrow.')
 upright_page(rel,layer,'195-373')

with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 for line,old,new,why in [
  ('left side closing parenthesis',r'\overline F(\varprojlim\limits_\alpha\text{\uwave{X}}^{(\alpha)}',r'\overline F(\varprojlim\limits_\alpha\text{\uwave{X}}^{(\alpha)})','The outer application of F-bar is unclosed in the print; the displayed equality requires the closing parenthesis.'),
  ('right-side functor bar',r'F(\text{\uwave{X}}^{(\alpha)})',r'\overline F(\text{\uwave{X}}^{(\alpha)})','F has domain C, whereas the argument is a pro-object. Its extension F-bar is required by the immediately preceding definition and the assertion of commutation.'),
  ('right-side pro-object underline',r'X^{(\alpha)}',r'\text{\uwave{X}}^{(\alpha)}','These are the same pro-objects indexed by alpha as on the left and in the preceding sentence; the local underline was dropped.'),
  ('first exact diagram initial object',r"X'\longrightarrow X'\rightrightarrows X''",r"X\longrightarrow X'\rightrightarrows X''",'The equalizer object is X, as explicitly shown by F(X) in the transformed diagram. A duplicated X-prime would not express preservation of general equalizers.'),
  ('last-line category identifier',r'X\in C',r'X\in\text{\uwave{C}}','This is the same category C with a wavy underline as throughout the definition; the underline is locally omitted.')]:
  w.writerow(['sources/fr/fr/195.tex','French corrected','195-373',line,'A.2–3',old,new,'Enlarged scan: '+why+' Existing corrected reading confirmed.','misprint of the original','low'])
event('195-A2-strict-normal-form','targeted proof check','For a strict system, each represented functor Hom(X_i,-) injects into H=colim Hom(X_i,-), since transition maps are epimorphisms. Every represented subfunctor Hom(Q,-) of H factors through some stage by Yoneda evaluation, and that factorization corresponds to an epimorphism X_i to Q. Thus the represented subfunctors, ordered by inclusion, give the saturated canonical system; cancellation of epimorphisms gives uniqueness of compatible transition maps. This argument assumes the required quotient collection is a set (for example C essentially small or the relevant co-well-poweredness condition). The source does not discuss that size issue; no hypothesis is silently inserted. Uniqueness is relative to the identification of the represented functor, not a denial of automorphisms.','195, pp. 372–373, strict-system normal form and uniqueness')
event('195-A2-iterated-pro-limits','carried as background without fault found','Read the claim for projective systems in the preceding filtered sense. Its proof needs the reindexing result that a filtered colimit of filtered colimits of representables is again a filtered colimit of representables. Under this small-diagram construction the two iterated inverse limits in C-prime identify, giving commutation by F-bar. The displayed missing parenthesis, missing bar on F and missing wavy underline on X have been checked by their domains; a complete reindexing proof is not claimed in this page check. Arbitrary nonfiltered diagrams are not inferred here.','195, p. 373, first displayed formula and its concluding sentence')
event('195-A3-left-exactness','targeted proof check','Finite limits are constructed from finite products (including the empty product) and equalizers. A fiber product is the equalizer of the two maps from X times Y to Z; an equalizer is the fiber product of (f,g):X to Y times Y with the diagonal of Y. These constructions prove equivalence of (i), (ii), and (iii), with exact diagram meaning equalizer. They confirm the first diagram begins with X rather than X-prime. A covariant representable Hom(A,-) preserves limits by their universal property. A filtered colimit of these preserves finite limits in Sets: representatives for finitely many coordinates and finitely many equalities can be chosen at one common later stage. This proves pro-representable implies left exact.','195, p. 373, A.3 equivalences and pro-representable implication')
record_page('195',373,r'''Compared sources/fr_printed/fr/195.tex and sources/fr/fr/195.tex entry lines 208–261 with scan leaf 6 at 400 dpi, full page and all three enlarged bands. Inspected every prime, bar, parenthesis, alpha and category subscript in the limit formula, both equalizer diagrams, and the final category identifier.

Restored the printed underlines, roman heading and item labels, ordinary quotation marks and parentheses, exact comma placement, comma-numbered reference 2, 1, wavy category/pro-object letters, upright variables and limit-index placement. The printed layer restores five omissions/slips: the missing closing parenthesis, unbarred right-side F, plain right-side X, initial X-prime in the equalizer diagram and plain final C. Five existing corrected readings are confirmed with explicit reasons.

Checked the strict-system normal form through represented subfunctors and epimorphic quotients, recording the necessary set-size qualification separately. The general reindexing result used by the iterated-limit claim remains identified background. Proved the finite-limit equivalences by products, equalizers and fiber products, and the pro-representable implication by the finite-coordinate description of filtered colimits of sets. The next definition continues on page 374.''')
from update_record_counts import update
update()
