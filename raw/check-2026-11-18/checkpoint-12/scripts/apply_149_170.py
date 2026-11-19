from audit_utils import *
E='Exposé 149, p. 170, Numdam leaf 3, full page at 400 dpi and top/middle/bottom crops at 1.25x. '
for folder,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    base=f'sources/{folder}/tex/base.tex'
    replace(base,r'\usepackage{microtype}',r'\usepackage{microtype}'+'\n'+r'\usepackage[normalem]{ulem}',layer,'149-170','underlined propositions','','Printed prose emphasis uses underlining. ulem provides line-breaking underlining without converting existing emphasis commands.',kind='typesetting',full=True)
    replace(base,r'\textbf{#1%',r'\textnormal{#1%',layer,'149-170','proposition and corollary labels','','Printed result labels are roman typewriter capitals, without boldface distinction.',kind='typesetting',full=True)
    replace(base,r'\fi. ---}',r'\fi. -}',layer,'149-170','proposition and corollary labels','','Printed result separator is period plus short hyphen, rather than the supplied em dash.',kind='typesetting',full=True)
    rel=f'sources/{folder}/fr/149.tex'
    for old,new,line,statement,why in [
        (r'H^{p}\bigl(\Gamma(C(B))\bigr).',r'H^{p}\bigl(\Gamma(C(B))\bigr)','first display','(1.3)','No terminal period follows the display.'),
        (r'H^{p}\bigl(X,\Extsh_{\Osh}^{q}(A,B)\bigr).',r'H^{p}\bigl(X,\Extsh_{\Osh}^{q}(A,B)\bigr)','second display','(1.4)','No terminal period follows the display.'),
        (r'\fquote{edge-homomorphisms}',r'\fquote{\uline{edge-homomorphisms}}','after (1.4)','','The quoted phrase is underlined, excluding the quotation marks.'),
        (r'\operatorname{Ext}_{\Osh}^{p}(X;\Osh,B)=H^{p}(X,B).',r'\operatorname{Ext}_{\Osh}^{p}(X;\Osh,B)=H^{p}(X,B)','Corollary 1','(1.6)','No terminal period follows the display.'),
        (r'=\Extsh_{\Osh|U}^{p}(A|U,B|U),',r'=\Extsh_{\Osh|U}^{p}(A|U,B|U)','restriction display','','No terminal comma follows the display.'),
        (r'pour $x\in X$ fixé,',r'pour $x\in X$ fixé','before (1.7)','','No comma follows fixé.'),
        (r'\operatorname{Hom}_{\Osh_x}(A_x,B_x),',r'\operatorname{Hom}_{\Osh_x}(A_x,B_x)','Hom comparison display','(1.7)','No terminal comma follows the display.'),
        (r'\operatorname{Ext}_{\Osh_x}^{p}(A_x,B_x).',r'\operatorname{Ext}_{\Osh_x}^{p}(A_x,B_x)','Ext comparison display','(1.8)','No terminal period follows the display.')]:
        replace(rel,old,new,layer,'149-170',line,statement,E+why)
    old='''Il existe pour tout $\\Osh$-Module $A$ un foncteur
spectral cohomologique sur $\\Ccat^{\\Osh}$, aboutissant au foncteur gradué
$\\bigl(\\operatorname{Ext}_{\\Osh}^{*}(X;A,B)\\bigr)$, et dont le terme initial est'''
    new='''\\uline{Il existe pour tout} $\\Osh$-\\uline{Module} $A$ \\uline{un foncteur
spectral cohomologique sur} $\\Ccat^{\\Osh}$, \\uline{aboutissant au foncteur gradué}
$\\bigl(\\operatorname{Ext}_{\\Osh}^{*}(X;A,B)\\bigr)$, \\uline{et dont le terme initial est}'''
    replace(rel,old,new,layer,'149-170','Proposition 1, three text lines','1',E+'Underlining covers the prose of the proposition, excluding mathematical variables and the label.')
    old='''Si $A$ est localement isomorphe à $\\Osh^{n}$, alors on a
des isomorphismes canoniques'''
    new='''\\uline{Si} $A$ \\uline{est localement isomorphe à} $\\Osh^{n}$, \\uline{alors on a
des isomorphismes canoniques}'''
    replace(rel,old,new,layer,'149-170','Corollary 1, first sentence','Corollary 1',E+'Restore the printed prose underlining, excluding A and O^n.')
    replace(rel,'En particulier on a\nun isomorphisme canonique','\\uline{En particulier on a\nun isomorphisme canonique}',layer,'149-170','Corollary 1, second sentence','Corollary 1',E+'This sentence is underlined.')
    text,_,_=page_text(rel,170)
    old=text[text.index(r'\result{PROPOSITION}{2}'):].rstrip()
    new='''\\result{PROPOSITION}{2} \\uline{Si} $A$ \\uline{est, dans un voisinage de} $x$, \\uline{isomorphe au
conoyau d'un homomorphisme} $\\Osh^{m}\\longrightarrow\\Osh^{n}$, \\uline{alors} (1.7) \\uline{est un isomorphisme pour tout} $p$. \\uline{Il en est ainsi en
particulier si} $A$ \\uline{est un} $\\Osh$-\\uline{Module cohérent} [3].'''
    why='Restore the complete printed sentence, including (1.7) and pour tout p, and its underlining; the scan has no footnote or additional resolution hypothesis.'
    if folder=='fr':
        why+=' The supplied replacement by an all-degree Ext statement adds hypotheses and chooses an intended reference without sufficient evidence. The literal (1.7) Hom comparison is valid for a finite presentation: both stalk and local Hom are the same kernel of B_x^n -> B_x^m. Therefore restore the printed statement and reserve its redundant p for a note; no conjectural authorial intention is imposed.'
    replace(rel,old,new,layer,'149-170','last three text lines','2',E+why)
    upright_page(rel,layer,'149-170')
event('149-2','targeted proof check','The printed reference is (1.7), a Hom comparison. For a local finite presentation O^m -> O^n -> A -> 0, applying Hom(-,B) gives the kernel of B^n -> B^m; stalks preserve that finite kernel, so (1.7) is an isomorphism. The unused phrase pour tout p is redundant. The supplied all-degree Ext rewrite is not forced by this reading and is reverted. This does not prove an all-degree Ext comparison from finite presentation.','Exposé 149, p. 170, Proposition 2, final three text lines')
for sid,loc in [('149-1','Proposition 1'),('149-cor1','Corollary 1')]:
    event(sid,'carried as background without fault found','Read formulae and prose against the scan; no independent proof claimed.',f'Exposé 149, p. 170, {loc}')
record_page('149',170,'''Compared both `sources/fr/fr/149.tex` and `sources/fr_printed/fr/149.tex`, `\\src{170}` through before `\\src{171}` (supplied lines 65-123), against Numdam leaf 3 at 400 dpi; enlarged top, middle and bottom crops cover every displayed formula and the final proposition. Read all prose and indices in (1.3)-(1.8), the unnumbered restriction formula, Proposition 1, Corollary 1 and Proposition 2.

Restored missing prose underlining and absent terminal punctuation, the comma-free fixé, upright mathematical variables, and ordinary result-label typography. The standard left-tag option added for p. 169 also applies here. Source-page comparison is complete; PDF inspection and the mandated second reading remain pending.

**Existing correction reverted in corrected French:** the expanded Proposition 2 was not a transcription of the printed sentence. The print reads (1.7), not (1.8), and has no added partial-free-resolution or pseudo-coherence clauses. With its literal Hom reference the finite-presentation assertion is true, by the finite-kernel argument recorded in CHECK_EVENTS.tsv. The words pour tout p are redundant but do not force the stronger Ext assertion. Both French layers now preserve this printed sentence. This changed meaning must be propagated when each translation is reached; none is yet claimed checked or updated. No numbered release disposition among 0001-0017 occurs on this page.''')
