from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/149.tex'
    def r(a,b,line,statement='',kind='reading',why='',count=1):
        replace(rel,a,b,layer,'149-178',line,statement,'400-dpi page, three enlarged bands and tight formula crops. '+why,kind,count=count)
    txt,_,_=page_text(rel,178)
    m=re.search(r'\\begin\{align\*\}(.*?)\\end\{align\*\}',txt,re.S)
    old=m.group(0);body=m.group(1).replace('&','').replace('\\\\','').rstrip().removesuffix(',')
    r(old,'\\['+body+'\n\\]','1','4-lem1','structure','The proof equality is a single display, without a terminal comma or forced alignment breaks.')
    r(r'(X;\Omega_X^{n-p},\omega_Y^{n-p}).',r'(X;\Omega_X^{n-p},\omega_Y^{n-p})','4.2','4.2',why='There is no terminal period.')
    r('$Y$ non singulière',r'$Y$ \uline{non singulière}','after 4.2','4',why='Non singulière is underlined.')
    r('\\emph{section\nfondamentale}','\\uline{section\nfondamentale}','fundamental section definition','4',why='The defined term is underlined, not italic.')
    r(r'\emph{classe de cohomologie de $Y$ dans $X$}',r'\uline{classe de cohomologie de} $Y$ \uline{dans} $X$','cycle class definition','4',why='Prose only is underlined; the variables are not.')
    txt,_,_=page_text(rel,178)
    m=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',txt,re.S)
    old=m.group(0);body=m.group(1).replace('&','').replace('\\\\','').rstrip().removesuffix('.')
    r(old,body,'4.3','4.3','structure','The diagram is printed on one line with no terminal period.')
    r(r'\emph{cycle non singulier de dimension $n-p$}',r'\uline{cycle non singulier} de dimension $n-p$','cycle definition','4',why='Only cycle non singulier is underlined.')
    r(r'$Y\longmapsto P(Y)$',r'$Y\longrightarrow P(Y)$','cycle definition','4',why='The printed arrow has no vertical mapsto bar.')
    r('sur $X$\ndans','sur $X$,\ndans','cycle definition','4',why='The print has a comma after X.')
    r("$n-p'$ ;", "$n-p'$,",'last paragraph','4',why='The print uses a comma, not a semicolon.')
    r(r'\emph{coupent transversalement}',r'\uline{coupent transversalement}','last paragraph','4',why='The phrase is underlined.')
    if tree=='fr_printed':
        r(r'\Extsh_{\Osh_X}^{p}(F,\Omega_X^{n})',r'\Extsh_{\Osh_X}(F,\Omega_X^{n})','1','4-lem1',why='The second Ext has no superscript p. Corrected French retains p: twisting by an invertible module preserves the Ext degree.')
        r(r'\Extsh_{\Osh_X}^{p}(\Osh_Y,\Omega_X^{p})$. Cette',r'\Extsh_{\Osh_X}^{p}(\Osh_Y,\Omega_X^{p})$ Cette','fundamental section definition','4',why='No period is printed after the displayed-in-line sheaf before Cette; corrected French retains sentence punctuation.')
        r(r'H^{0}\!\left(X,\Extsh_{\Osh_X}^{p}(\Osh_Y,\Omega_X^{p})\right)',r'H^{0}\!\left(X,\Extsh_{\Osh_X}^{p}(O_Y,\Omega_X^{p})\right)','4.3','4.3',why='The last O_Y is visibly not underlined. Corrected French keeps the underline identifying the structure sheaf already used in the same diagram.')
    for symbol in [r'\Omega',r'\omega']:
        txt,_,_=page_text(rel,178)
        r(symbol,r'\underline{'+symbol+'}','differential and dualizing sheaf symbols','4',why='Restore the printed underlined Greek sheaf notation.',count=txt.count(symbol))
    upright_page(rel,layer,'149-178')
event('149-4-lem1-twist','targeted proof check','Locally trivializing the invertible sheaf L tensor omega_X dual reduces the first equality to Ext^p(F,omega_X) in the same degree p. The missing p on the second Ext is therefore a typographical omission; the supplied correction is retained.','149, p. 178, line 1')
event('149-4.2','carried as background without fault found','Read the specialization F=O_Y, L=Omega_X^p and the induced fundamental section; formula indices checked visually.','149, p. 178, formula (4.2) and following paragraph')
event('149-4.3','carried as background without fault found','Read the maps defining the cycle class and checked their directions, the isomorphism marker, and both closing parentheses. The final O_Y loses its underline in print; corrected notation refers to the same structure sheaf as elsewhere in the diagram.','149, p. 178, formula (4.3)')
record_page('149',178,r'''Compared sources/fr_printed/fr/149.tex entry lines 473–532 and sources/fr/fr/149.tex entry lines 476–535 against scan leaf 11, rendered at 400 dpi, three enlarged bands and tight crops of the first Ext chain, the natural-map punctuation and the end of (4.3). Read the conclusion of Lemma 1, (4.2), the construction of the fundamental section and cycle class, (4.3), and the two cycle-definition paragraphs.

Both layers restore the single-line display structures, literal punctuation and ordinary assignment arrow, upright letters, sheaf underlines and the exact spans of definition emphasis. Printed French additionally restores the second Ext's absent p, the omitted sentence period after the fundamental-section sheaf, and the ununderlined final O_Y in (4.3). Corrected French retains the existing repairs, with the Ext-degree check recorded separately. The small mark after the natural-map target is punctuation, not an added variety name. Changes await the required second reading and propagation to translations.''')
from update_record_counts import update
update()
