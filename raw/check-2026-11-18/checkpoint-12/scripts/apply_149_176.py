from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/149.tex'
    def r(a,b,line,statement='',kind='reading',why='',count=1):
        replace(rel,a,b,layer,'149-176',line,statement,'400-dpi image, three enlarged bands and the 3x comma crop. '+why,kind,count=count)
    old='''Soit $\\Omega_X$ (resp. $\\Omega_Y$) le faisceau des germes de formes
différentielles régulières sur $X$ (resp. $Y$). Alors on a des isomorphismes
canoniques :'''
    new='''\\uline{Soit} $\\Omega_X$ (resp. $\\Omega_Y$) \\uline{le faisceau des germes de formes
différentielles régulières sur} $X$ (resp. $Y$). \\uline{Alors on a des isomorphismes
canoniques} :'''
    r(old,new,'1–2','4-cor2',why='Printed prose underlining excludes the two resp. parentheticals.')
    r('\nou encore\n',r'\n\uline{ou encore}\n'.replace(r'\n','\n'),'between 3.6 and 3.6 bis','4-cor2',why='The linking phrase is underlined.')
    r('servir de définition de',r'servir de \uline{définition} de','after 3.6 bis','5',why='définition is underlined.')
    r(r'\bigr)=\Osh_Y,',r'\bigr)=\Osh_Y','3.6','3.6',why='No comma follows this display.')
    r(r'\bigr)=\Omega_Y^{n-p}.',r'\bigr)=\Omega_Y^{n-p}','3.6 bis','3.6 bis',why='No period follows this display.')
    r(r'$i<p$, tandis',r'$i<p$ ; tandis','Proposition 5','5',why='The print has a semicolon after i<p.')
    r(r'\Extsh_{\Osh_X}^{p}(\Osh_X/J,L)\right),',r'\Extsh^{p}(\Osh_X/J,L)\right)','3.7','3.7',why='The inner Ext has no base-ring subscript and the display has no terminal comma.')
    r(r'\Extsh_{\Osh_X}^{p}(\Osh_Y,L)\right).',r'\Extsh^{p}(\Osh_Y,L)\right).','3.7 bis','3.7 bis',why='The inner Ext has no base-ring subscript; the terminal period is present and retained.')
    old='''les faisceaux
\\[
  E^{i}(F)=\\Extsh_{\\Osh_X}^{p+i}(F,\\Omega_X^{n})
\\]
ne dépendent'''
    new='''les faisceaux
$E^{i}(F)=\\Extsh_{\\Osh_X}^{p+i}(F,\\Omega_X^{n})$ ne dépendent'''
    r(old,new,'last paragraph of Proposition 5','5','structure','The E^i formula runs in the paragraph.')
    for startmark,endmark in [(r'\result{PROPOSITION}{5} ','\n\\begin{equation}'),('où $J$','\n\\begin{equation}'),('Enfin, $F$','\n\nLa question')]:
        txt,_,_=page_text(rel,176)
        start=txt.index(startmark)+(len(startmark) if startmark.startswith('\\result') else 0)
        end=txt.index(endmark,start); old=txt[start:end]
        r(old,underline_prose(old),'Proposition 5 prose','5',why='All statement prose in this span is underlined, while its mathematical formulas remain outside prose emphasis.')
    r("d'algèbre locale : si $A$","d'algèbre locale : Si $A$",'proof, second line','5',why='The scan uses capital Si.')
    r(r'$\leq q=n-p$, prouver',r'$\leq q=n-p$ prouver','proof, third line','5',why='There is no comma after n-p.')
    old='''et
\\[
  \\operatorname{Ext}_{A}^{p}(M,A)
  =\\operatorname{Hom}_{A}\\!\\left(M,\\operatorname{Ext}_{A}^{p}(A/J,A)\\right),
\\]
où'''
    new='''et
$\\operatorname{Ext}_{A}^{p}(M,A)
=\\operatorname{Hom}_{A}\\!\\left(M,\\operatorname{Ext}^{p}(A/J,A)\\right)$,
où'''
    r(old,new,'proof, fourth line','5','structure','This equality is inline, and its inner Ext omits the A subscript.')
    r('« dimension »',r'\fquote{dimension}','proof','5',why='The scan uses double quotes, not guillemets.')
    r('« système de paramètres »',r'\fquote{système de paramètres}','proof','5',why='The scan uses double quotes, not guillemets.')
    txt,_,_=page_text(rel,176)
    r(r'\Omega',r'\underline{\Omega}','all differential-sheaf symbols','3.6–3.7',why='Every Omega denoting a sheaf on this page is underlined; the supplied source dropped these underlines.',count=txt.count(r'\Omega'))
    if tree=='fr_printed':
        r(r'$\operatorname{Ext}$, au cas où',r'$\operatorname{Ext}$, au,cas où','third line from bottom','5',why='A clear printed comma occurs between au and cas. Corrected French keeps the grammatical phrase without it.')
    upright_page(rel,layer,'149-176')
event('149-4-cor2','carried as background without fault found','Read the geometric reformulation and equations (3.6), (3.6 bis). Underlines on all differential sheaves restored; no change to the mathematical statement.','149, p. 175–176, Corollary 2')
event('149-5','carried as background without fault found','Read the vanishing assertion, change-of-rings identification and independence of embedding, together with the beginning of the local proof. The reduction to a cyclic module and parameter ideal remains a proof detail for the notes.','149, p. 176, Proposition 5 and the proof continuing on p. 177')
record_page('149',176,r'''Compared both French source intervals for `\src{176}` (entry lines 371–425) against leaf 9 at 400 dpi. Three enlarged bands cover all mathematical signs; a 3x crop establishes the stray comma in au,cas. Read the continuation of Corollary 2, (3.6), (3.6 bis), Proposition 5, (3.7), (3.7 bis), the embedding-independence clause, and the local proof through its page break.

Restored all underlined Omega symbols, statement emphasis, the underlined word définition, omitted-base shorthand for three inner Ext occurrences, the two inline formulas, double quotation marks, capital Si, the semicolon in the vanishing clause, and literal punctuation of the displays. The terminal period of (3.7 bis) was retained. The printed layer alone restores au,cas; the corrected layer keeps au cas. The handwritten repair in the word proposition is not treated as a new italic-emphasis instruction. No further mathematical correction was imposed. Second reading, translations, proof-gap notes and PDF checks remain pending.''')
from update_record_counts import update
update()
