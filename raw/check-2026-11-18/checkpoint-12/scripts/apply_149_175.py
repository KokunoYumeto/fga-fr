from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/149.tex'
    def r(a,b,line,statement='',kind='reading',why=''):
        replace(rel,a,b,layer,'149-175',line,statement,'400-dpi full scan, three enlarged bands and 3x parenthesis crops. '+why,kind)
    for label,end,sid in [(r'\result{PROPOSITION}{4} ','\n\n(Le point','4'),(r'\result{COROLLAIRE}{1} ','\n\\begin{equation}','4-cor1'),(r'\result{COROLLAIRE}{2} ','\n\n','4-cor2')]:
        txt,_,_=page_text(rel,175)
        start=txt.index(label)+len(label); stop=txt.index(end,start)
        old=txt[start:stop]
        r(old,underline_prose(old),'statement prose',sid,why='The prose of this statement is underlined; mathematical expressions and numbered references are not, apart from the separately recorded emphasis on k.')
    r('conditions indiquées.)','conditions indiquées).','10','4',why='The period follows the closing parenthesis.')
    r(r'\bigr)=A/J.',r'\bigr)=A/J','display (3.5)','3.5',why='No terminal period appears after the display.')
    r('« $\'$ »',r'\fquote{$\prime$}','dual explanation','4-cor1',why='The print uses double quotation marks around the prime sign, not guillemets.')
    old='''s'identifie à
\\[
  \\operatorname{Ext}_{A}^{p}\\!\\left(A/J,\\bigwedge^{p}(J/J^{2})\\right),
\\]
donc, en vertu'''
    new='''s'identifie à
$\\operatorname{Ext}_{A}^{p}\\!\\left(A/J,\\bigwedge^{p}(J/J^{2})\\right)$,
donc, en vertu'''
    r(old,new,'line before the Hom display','4-cor1','structure','The Ext expression runs in the paragraph; only the following Hom expression is displayed.')
    r(r"\emph{classe fondamentale de l'idéal $J$ dans $A$}",r"\uline{classe fondamentale} de l'idéal $J$ dans $A$",'fundamental-class definition','4-cor1',why='Only classe fondamentale is emphasized, by underlining rather than italics.')
    r('sensiblement plus larges.)','sensiblement plus larges).','following parenthesis','4-cor1',why='The period follows the closing parenthesis.')
    # Two k glyphs are visibly underlined as emphasis in the corollaries.
    txt,_,_=page_text(rel,175)
    replace(rel,'$k$',r'$\underline{k}$',layer,'149-175','Corollaries 1 and 2','4-cor1;4-cor2','The two field symbols k are underlined in the statement emphasis; no change of the named field is intended.',count=2)
    if tree=='fr_printed':
        r('$(A/J)$-module projectif de rang $1$', '$(A/J)$-module libre de rang $1$','first line after 3.5','4-cor1',why='The print says libre, not projectif. The corrected layer retains the locally free/projective repair.')
        r('$A$-module projectif de rang $1$', '$A$-module libre de rang $n$','second line after 3.5','4-cor1',why='The print says libre de rang n. Corrected French retains projectif de rang 1: the top exterior power has rank one; global freeness is not implied.')
        txt,_,_=page_text(rel,175)
        note=next(m for m in footnotes(txt) if 'rang $n$' in m[2])
        r(txt[note[0]:note[1]],'','editorial footnote','4-cor1','structure','No editorial note is present in the scan.')
        r('le $(A/J)$-module dual','le $(A/J$-module dual','dual explanation','4-cor1',why='The tighter crop shows the missing close after A/J; the printed layer preserves it.')
        r(r'$\operatorname{Ext}_{A}^{p}\bigl(\Omega^{n-p}(A/J),\Omega^{n}(A)\bigr)$',r'$\operatorname{Ext}_{A}^{p}\bigl(\Omega^{n-p}(A/J)\bigr),\Omega^{n}(A)$','fundamental-class definition','4-cor1',why='The 3x crop shows the Ext closing parenthesis before the comma, after Omega^(n-p)(A/J); corrected French places it after the second argument.')
    else:
        old='''\\footnote{Le texte imprimé
porte « rang $n$ » ; les deux modules de formes de degré maximal sont de rang
$1$, comme l'exige aussi l'identification à $\\bigwedge^{p}(J/J^{2})$ ci-dessous.}'''
        new='''\\footnote{Le texte imprimé dit « libre » pour les deux modules et « rang $n$ » pour $\\Omega^{n}(A)$. Les modules de formes de degré maximal sont projectifs de rang $1$ ; leur liberté globale ne découle pas des hypothèses. L'identification ci-dessous résulte de la suite conormale en prenant les déterminants.}'''
        r(old,new,'editorial note after the rank assertion','4-cor1','misprint of the original','Confirm the rank correction and record the previously unmarked two replacements of libre by projectif. Localizing the smooth differential modules gives ranks n and n-p; their top exterior powers have rank one. The determinant of the conormal exact sequence supplies the cancellation used in (3.5).')
    upright_page(rel,layer,'149-175')
event('149-4','carried as background without fault found','Read the regular-sequence assertion and cited Koszul acyclicity. No full induction proof has yet been reconstructed.','149, p. 175, Proposition 4')
event('149-4-cor1','targeted proof check','Under the stated smooth regular affine setting, top differentials are projective of rank one, not generally globally free. Localizing a rank-n differential module makes its nth exterior power rank one; the printed rank n is wrong. Taking determinants in 0 -> J/J^2 -> Omega_A tensor B -> Omega_B -> 0, B=A/J, gives omega_B dual tensor omega_A|B = det(J/J^2), which cancels the dual determinant in Ext_A^p(B,A). This justifies both projective replacements and rank 1 in the existing corrected text. The parenthesis in the later Ext group must enclose both arguments.','149, p. 175, Corollary 1, (3.5), and its proof')
record_page('149',175,r'''Read both French intervals `\src{175}` to before `\src{176}` (entry lines 320–374) against leaf 8 at 400 dpi, with all three enlarged bands and additional 3x crops of the dual-module phrase and the later Ext expression. Compared Proposition 4, Corollary 1 with its proof, and the beginning of Corollary 2, including every rank, exponent, parenthesis and emphasis span.

Restored statement underlining (including the separately underlined k glyphs), the period outside two prose parentheses, absent terminal punctuation in (3.5), double quotes around the dual prime, the inline Ext expression, and underlining only of classe fondamentale. Upright variables are explicit.

The printed layer now restores libre in both top-form modules and rank n for the second, removes the editorial note, preserves the missing close in (A/J-module dual, and places the later Ext close before its comma as printed. The corrected layer keeps projectif in both places, rank 1, and correctly scoped parentheses; the existing footnote now records both the rank error and previously silent projectivity repairs. The determinant calculation supporting these decisions is recorded as a targeted proof check. Source comparison completed; second reading, propagation to translations and build verification pending.''')
