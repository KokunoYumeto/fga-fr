from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/149.tex'
    def r(a,b,line,statement='',kind='reading',why='',count=1):
        replace(rel,a,b,layer,'149-177',line,statement,'400-dpi image, three enlarged bands and 3x overprint/last-line crops. '+why,kind,count=count)
    r('« dimension »',r'\fquote{dimension}','1','5',why='The print uses ordinary double quotes.')
    old='''d'où résulte facilement que
\\[
  E(M)=\\operatorname{Hom}_{A}\\bigl(M,E(A/J)\\bigr).
\\]
'''
    new='''d'où résulte facilement que
$E(M)=\\operatorname{Hom}_{A}\\bigl(M,E(A/J)\\bigr)$.
'''
    r(old,new,'3','5','structure','The representability equality is inline.')
    r(r'\fsection{4}{Classe de cohomologie associée à une sous-variété}',r'\fsection{\normalfont4}{\normalfont\uline{Classe de cohomologie associée à une sous-variété}.}','section heading','4',why='The title is underlined and followed by a period.')
    r(r'\Homsh_{\Osh_X}(F,\omega_Y^{q}).',r'\Homsh_{\Osh_X}(F,\omega_Y^{q})','3.8','3.8',why='No terminal period follows this display.')
    r('$k$',r'$\underline{k}$','first paragraph of section 4','4',why='The base-field letter is underlined even outside statement emphasis.')
    old='''par
\\[
  \\Omega_X^{*}=\\bigoplus_p\\Omega_X^{p}
\\]
le faisceau'''
    new='''par
$\\Omega_X^{*}=\\bigoplus\\limits_p\\Omega_X^{p}$ le faisceau'''
    r(old,new,'fourth line of section 4','4','structure','The graded-form expression is inline, with p set below the large operator. The operator itself is adjudicated separately.')
    old='''\\operatorname{Ext}_{\\Osh_X}^{p}(X;F,L)
  =H^{0}\\bigl(X,\\Extsh_{\\Osh_X}^{p}(F,L)\\bigr).'''
    new='''\\operatorname{Ext}_{\\Osh}^{p}(X;F,L)
  =H^{0}\\bigl(X,\\Extsh_{\\Osh}^{p}(F,L)\\bigr)'''
    r(old,new,'4.1','4.1',why='Both base sheaves are written O without subscript X in this display; there is no terminal period.')
    r('  \\right),\n\\end{equation}','  \\right)\n\\end{equation}','4.1 bis','4.1 bis',why='The display has no terminal comma.')
    r('proposition 5 (qui', 'proposition 5, (qui','after 4.1 bis','4-lem1',why='The print has a comma before the explanatory parenthesis.')
    for startmark,endmark in [(r'\result{COROLLAIRE}{} ','\n\\begin{equation}'),(r'\result{LEMME}{1} ','\n\\begin{equation}'),('Si $F$','\n\\begin{equation}'),('où $\\omega_Y^{n-p}$','\n\nLa formule')]:
        txt,_,_=page_text(rel,177); start=txt.index(startmark)+(len(startmark) if startmark.startswith('\\result') else 0)
        stop=txt.index(endmark,start); old=txt[start:stop]
        r(old,underline_prose(old),'Corollary / Lemma 1 prose','5-cor;4-lem1',why='Restore the underlining of the selected statement prose.')
    if tree=='fr_printed':
        r(r'E(M)=\operatorname{Hom}_{A}\bigl(M,E(A/J)\bigr)',r'E(M)=\operatorname{Hom}_{A}\bigl(M,E(A)\bigr)','3','5',why='The print unambiguously has E(A). Corrected French keeps E(A/J), the value at the free rank-one A/J-module.')
        for fragment in ['objet\nreprésentant','signe de réunion']:
            txt,_,_=page_text(rel,177); note=next(m for m in footnotes(txt) if fragment in m[2])
            r(txt[note[0]:note[1]],'','editorial footnote','5' if fragment.startswith('objet') else '4','structure','The editorial footnote is absent from the scan.')
        r(r'\bigoplus\limits_p',r'\bigcup\limits_p','fourth line of section 4','4',why='The printed operator is a union sign, not a direct-sum sign. Corrected French retains direct sum for the graded module.')
        r(r'fermée} $Y$',r'fermée} $\text{\rlap{M}Y}$','Lemma 1, second clause','4-lem1',why='The 3x crop shows a composite M/Y overprint. The printed layer reproduces both superposed glyphs; corrected French reads the Y used in the displayed target and subsequent definition. The order of the strikes is not claimed certain.')
        r('corollaire à la\nproposition 5','corollaire à\nproposition 5','after 4.1 bis','4-lem1',why='The article la is absent in the print; the corrected sentence retains it.')
        r('formule (3.8) on peut','formule (3.8) pn peut','last line','4-lem1',why='The enlarged final line has pn, with a visible descender on p. Corrected French retains on.')
    # All Omega/omega occurrences here denote sheaves, with visible underlines.
    for symbol in [r'\Omega',r'\omega']:
        txt,_,_=page_text(rel,177)
        r(symbol,r'\underline{'+symbol+'}','differential and dualizing sheaves','3.8;4',why='The scan underlines this Greek sheaf symbol.',count=txt.count(symbol))
    upright_page(rel,layer,'149-177')
event('149-5-representability','targeted proof check','For an A/J-linear contravariant left exact functor sending direct sums to products, a presentation by free A/J-modules identifies its value with Hom_A(M,E(A/J)). The printed E(A) is the wrong evaluation; for p>0 Ext_A^p(A,A)=0 and A need not be an object of the A/J-module category. Existing correction confirmed.','149, p. 177, first paragraph')
event('149-4-graded-forms','targeted proof check','The stated sheaf of all differential forms is graded additively. A set union of separate homogeneous pieces is not closed under addition of different degrees; their direct sum is the required graded module. Existing union-to-direct-sum correction retained in corrected French and reversed only in printed French.','149, p. 177, section 4 first paragraph')
event('149-5-cor','carried as background without fault found','Read the definition of the dualizing sheaf and the displayed consequence (3.8).','149, p. 177, Corollary to Proposition 5')
event('149-4-lem1','carried as background without fault found','Read Lemma 1 and both displays (4.1), (4.1 bis); proof continues on the next page. The overprinted closed-subset letter is consistent with Y in the displayed and subsequent formulas.','149, p. 177, Lemma 1')
record_page('149',177,r'''Compared both French intervals for p. 177 (entry lines 421–480) with leaf 10 at 400 dpi, all three enlarged bands, and tight 3x crops of the closed-subset overprint and pn. Read the end of Proposition 5's proof, its unnumbered corollary and (3.8), section 4, Lemma 1 and (4.1)/(4.1 bis), and the two final proof lines.

Both layers restore inline placement of the representability and graded-form formulas, Greek sheaf underlines, underlined k, statement and heading emphasis, the heading period, equation shorthand O without X in (4.1), literal quotes and punctuation. Confirmed existing original corrections E(A) to E(A/J) and union to direct sum, with targeted arguments in CHECK_EVENTS.tsv. Printed French restores the original readings and removes their editorial footnotes.

Other printed-only restorations are the absent article la after corollaire à and pn in the final line. The closed-subset glyph is visibly overstruck: the printed layer represents superposed M and Y rather than asserting a clean M; corrected French retains Y, as used throughout the clause. This ambiguous overprint requires particular attention in the second reading. All changes remain pending that mandated pass and translation propagation.''')
from update_record_counts import update
update()
