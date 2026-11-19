from audit_utils import *
E='Exposé 149, p. 172, Numdam leaf 5: 400-dpi image, three enlarged bands, and 3x crops of the closing parentheses and X1. '
for folder,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{folder}/fr/149.tex'
    old="\\[\n  0\\longrightarrow K'\\longrightarrow K\\longrightarrow K''\\longrightarrow 0,\n\\]\ntelle que"
    new="$0\\longrightarrow K'\\longrightarrow K\\longrightarrow K''\\longrightarrow 0$, telle que"
    replace(rel,old,new,layer,'149-172','first text line','2',E+'The short exact sequence is inline and followed by a comma.',kind='structure')
    old="cobord\n\\[\n  H^{i}(K',L)\\longrightarrow H^{i+1}(K'',L).\n\\]"
    new="cobord\n$H^{i}(K',L)\\longrightarrow H^{i+1}(K'',L)$."
    replace(rel,old,new,layer,'149-172','third text line','2',E+'The connecting map is inline, ending its sentence.',kind='structure')
    replace(rel,r'$\Ccat$',r'$C$',layer,'149-172','second paragraph, first two lines','2',E+'The two category letters are ordinary upright C, without an underline; preserve this printed variant.',count=2)
    for old,new,stmt in [(r'\operatorname{Ext}^{*}(A,C).',r'\operatorname{Ext}^{*}(A,C)','(2.3)'),(r'\operatorname{Ext}_{\Osh}^{p+q}(X;A,C),',r'\operatorname{Ext}_{\Osh}^{p+q}(X;A,C)','(2.4)'),(r'\Extsh_{\Osh}^{p+q}(A,C).',r'\Extsh_{\Osh}^{p+q}(A,C)','(2.5)')]:
        replace(rel,old,new,layer,'149-172','display '+stmt,stmt,E+'The numbered display has no terminal punctuation.')
    if folder=='fr_printed':
        replace(rel,r'$\Osh$-Modules sur $X$,',r'$\Osh$-Modules sur $X1$,',layer,'149-172','paragraph before (2.4), second line','(2.4)',E+'The print has a baseline digit 1 immediately after the overstruck X, not a subscript or a footnote. Preserve X1 in the printed layer. Corrected French retains X, the defined base space; no X1 is introduced.')
    upright_page(rel,layer,'149-172')
event('149-eq2.4','used and rechecked in this run','Checked the base-space symbol in the paragraph defining the products: the scan reads baseline X1, while the standing space is X and each adjacent displayed product uses X. Retain corrected X; no proof of the product construction is claimed.','Exposé 149, p. 172, paragraph immediately before (2.4), second line')
record_page('149',172,'''Compared both French sources for `\\src{172}` through before `\\src{173}` (supplied lines 184-228, plus the initial sequence moved from the preceding marker interval) against the 400-dpi image. Three enlarged bands cover all signs and formulas; separate 3x crops resolve the three closing parentheses in the first bicomplex equality (source correct there) and the printed baseline X1.

Restored the two inline formulas at the top of the page; ordinary ununderlined C in the second paragraph; and absent punctuation after (2.3)-(2.5). Upright variables are explicit. Retained the period after the second unnumbered bicomplex equality because the scan shows it.

An unrecorded supplied correction is now identified: the print has X1 before (2.4). The printed layer restores that literal reading; corrected French retains X because the only defined base space and all neighbouring products use X. The glyph is a baseline digit, not a footnote or subscript. No additional proof check is claimed for the product constructions. Source comparison completed; final second reading and build/PDF verification pending.''')
