from audit_utils import replace,read,write,record_page,page_text
E='Exposé 149, printed p. 169, Numdam PDF leaf 2; rendered at 400 dpi; notation/formula/tail crops enlarged 1.3x. '
changes=[
('Cartan--Eilenberg','Cartan-Eilenberg','introductory paragraph, line 4','', 'The printed author pair has a single hyphen, not an en dash.'),
(r'\fsection{1}{Les Ext de faisceaux de modules ({[2]}, chap. 3 et 4)}',r'\fsection{\normalfont1}{\normalfont\underline{Les} Ext \underline{de faisceaux de modules} ({[2]}, chap. 3 et 4).}','section heading','1','Underlining covers Les and de faisceaux de modules, excludes Ext and the reference; the heading ends with a period.'),
('le groupe abélien','le \\underline{groupe} abélien','paragraph 2, line 7','1','The word groupe is underlined.'),
('désignera le faisceau des germes',r'désignera le \underline{faisceau} des germes','paragraph 2, line 8','1','The word faisceau is underlined.'),
(r'\Ccat^{\Zsh}',r'\Ccat^{\mathrm Z}','paragraph 2 and final paragraph','1','The superscript Z is an ununderlined roman Z in both occurrences; the supplied sheaf macro adds an underline and boldface.',2),
(r'h_A(B)=\operatorname{Hom}_{\Osh}(X;A,B),',r'h_A(B)=\operatorname{Hom}_{\Osh}(X;A,B)','formula (1.1), left half','(1.1)','There is no comma after the first equality.'),
(r'\hsh_A(B)=\Homsh_{\Osh}(A,B).',r'\hsh_A(B)=\Homsh_{\Osh}(A,B)','formula (1.1), right half','(1.1)','There is no terminal period in the displayed formula.'),
(r'= H^{p}\bigl(\operatorname{Hom}_{\Osh}(X;A,C(B))\bigr),',r'= H^{p}\bigl(\operatorname{Hom}_{\Osh}(X;A,C(B))\bigr)','formula (1.2), first line','(1.2)','The first equality line has no terminal comma.'),
(r'= H^{p}\bigl(\Homsh_{\Osh}(A,C(B))\bigr),',r'= H^{p}\bigl(\Homsh_{\Osh}(A,C(B))\bigr)','formula (1.2), second line','(1.2)','The second equality line has no terminal comma.'),
('Désignons par\n\\[\n  \\Gamma:\\Ccat^{\\mathrm Z}\\longrightarrow\\Ccat\n\\]\nle foncteur', 'Désignons par\n$\\Gamma:\\Ccat^{\\mathrm Z}\\longrightarrow\\Ccat$ le foncteur','last paragraph, lines 2-3','1','The functor Gamma expression is inline, continuing Désignons par; there is no display.','structure'),
('notés par\n\\[\n  B\\longmapsto H^{p}(X,B).\n\\]', 'notés par $B\\longrightarrow H^{p}(X,B)$ :','last paragraph, last line','1','The functor assignment is inline, has an ordinary arrow without a mapsto bar, and ends with a colon.','structure'),
]
for folder,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{folder}/fr/149.tex'
    for c in changes:
        old,new,line,statement,why,*opts=c
        count=opts[0] if opts and isinstance(opts[0],int) else 1
        kind=opts[0] if opts and isinstance(opts[0],str) else 'reading'
        replace(rel,old,new,layer,'149-169',line,statement,E+why,kind=kind,count=count)
record_page('149',169,'''Both French layers were read against the full 400-dpi image and enlarged notation, formula and final-paragraph crops. Source: `sources/fr/fr/149.tex` and `sources/fr_printed/fr/149.tex`, from `\\src{169}` to before `\\src{170}` (supplied lines 3-63). The compared text runs from the seminar heading through the definition of the section functor. Formulae (1.1) and (1.2), all sheaf underlines, superscripts and indices were inspected.

Eleven replacement operations in each layer: nine reading operations (one covers the two occurrences of the same Z notation) and two structure operations. These restore omitted underlining, plain Z, printed punctuation, the hyphen, the ordinary arrow and two inline formulae. The mathematics of the definitions is unchanged. Neither layer has a recorded original-misprint correction on this page.

The typography of the modern book wrappers and mathematical font policy still needs resolution and PDF inspection. In particular, printed equation tags are on the left, and the supplied common macros and fonts are modern reconstructions. This page is therefore **not counted as fully completed** under the requested typography standard. The required final second reading is also pending.''',done=False)
