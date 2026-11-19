from audit_utils import *
E='Exposé 149, p. 171, Numdam leaf 4, 400-dpi full image and enlarged top/middle/bottom crops. '
for folder,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{folder}/fr/149.tex'
    old='''Soit $L_{*}=(L_i)$ une résolution gauche du
$\\Osh$-Module $A$ par des $\\Osh$-Modules dont chacun est isomorphe localement à
un $\\Osh^{n}$. Alors $\\Extsh_{\\Osh}^{*}(A,B)$ s'identifie à
$H^{*}\\bigl(\\Homsh_{\\Osh}(L_{*},B)\\bigr)$, et
$\\operatorname{Ext}_{\\Osh}^{*}(X;A,B)$ s'identifie à l'hypercohomologie de $X$
par rapport au complexe $\\Homsh_{\\Osh}(L_{*},B)$.'''
    new='''\\uline{Soit} $L_{*}=(L_i)$ \\uline{une résolution gauche du}
$\\Osh$-\\uline{Module} $A$ \\uline{par des} $\\Osh$-\\uline{Modules dont chacun est isomorphe localement à
un} $\\Osh^{n}$. \\uline{Alors} $\\Extsh_{\\Osh}(A,B)$ \\uline{s'identifie à}
$H^{*}\\bigl(\\Homsh_{\\Osh}(L_{*},B)\\bigr)$, \\uline{et}
$\\operatorname{Ext}_{\\Osh}(X;A,B)$ \\uline{s'identifie à l'hypercohomologie de} $X$
\\uline{par rapport au complexe} $\\Homsh_{\\Osh}(L_{*},B)$.'''
    replace(rel,old,new,layer,'149-171','first four printed text lines','3',E+'The two Ext symbols have no star superscript; H carries the star. Restore the printed prose underlining. The unstarred Ext notation is intelligible as the graded functor, so no mathematical correction is imposed.')
    for old,new,line,statement,why,kind in [
        ('bifoncteurs cohomologiques,',r'\uline{bifoncteurs cohomologiques},','third paragraph','1','The two-word phrase is underlined.','reading'),
        (r'\fsection{2}{Loi de composition dans les Ext}',r'\fsection{\normalfont2}{\normalfont\uline{Loi de composition dans les} Ext.}','section heading','2','Underlining excludes Ext; the heading ends with a period.','reading'),
        (r'$\Ccat$',r'$\underline{C}$','first paragraph of section 2','2','Both category letters are ordinary underlined C, not script C.','reading'),
        (r'\text{où }n=\deg(u),',r'\text{où }n=\deg(u)','display (2.1)','(2.1)','No comma follows deg(u).','reading'),
        ('''définit un accouplement
\\[
  \\operatorname{Hom}(K,L)\\times\\operatorname{Hom}(L,M)
  \\longrightarrow\\operatorname{Hom}(K,M)
\\]
compatible''','''définit un accouplement
$\\operatorname{Hom}(K,L)\\times\\operatorname{Hom}(L,M)
\\longrightarrow\\operatorname{Hom}(K,M)$ compatible''','paragraph before (2.2)','2','This composition pairing is inline in the printed paragraph.','structure'),
        (r'H^{*}(K,M),',r'H^{*}(K,M)','display (2.2)','(2.2)','No terminal comma follows the display.','reading'),
        (r'$(u,v)\longmapsto vu$',r'$(u,v)\longrightarrow vu$','line after (2.2)','(2.2)','The printed arrow has no mapsto bar.','reading'),
        ("$K^{i}\\longrightarrow L^{i+n}$).\n\nSi", "$K^{i}\\longrightarrow L^{i+n}$).\nSi",'section 2 before (2.1)','2','No paragraph indentation or blank separation occurs before Si K et L.','structure'),
        ("$H^{*}(K,L)$.\n\nSi", "$H^{*}(K,L)$.\nSi",'section 2 after (2.1)','2','No paragraph indentation or blank separation occurs before Si on a un troisième complexe.','structure')]:
        replace(rel,old,new,layer,'149-171',line,statement,E+why,kind=kind,count=2 if old==r'$\Ccat$' else 1)
    # The last display is absent from the image of 171: marker belongs before it.
    old="complexes\n\\[\n  0\\longrightarrow K'\\longrightarrow K\\longrightarrow K''\\longrightarrow 0,\n\\]\n\\src{172}"
    new="complexes\n\\src{172}\n\\[\n  0\\longrightarrow K'\\longrightarrow K\\longrightarrow K''\\longrightarrow 0,\n\\]"
    replace(rel,old,new,layer,'149-171','page boundary after last word complexes','','The image ends with the word complexes; the following short exact sequence belongs after the source marker for p. 172.',kind='structure',full=True)
    if folder=='fr_printed':
        old="qu'opérateurs homogènes).\\footnote{Le texte imprimé porte « à $u$ » ; l'équation\n(2.1) impose « à $d$ ».}"
        replace(rel,old,"qu'opérateurs homogènes).",layer,'149-171','paragraph following (2.1)','(2.1)',E+'No editorial footnote appears in the print.',kind='structure')
        replace(rel,'qui anticommutent à $d$','qui anticommutent à $u$',layer,'149-171','paragraph following (2.1)','(2.1)',E+'The enlarged crop unambiguously reads anticommutent à u; preserve this in the printed layer.')
        replace(rel,'est formée des homomorphismes','est formé des homomorphismes',layer,'149-171','section 2, first paragraph','2',E+'The print has masculine formé. Corrected French retains formée to agree with composante.')
        replace(rel,r'$H^{*}\bigl(\operatorname{Hom}(K,L)\bigr)$',r'$H^{*}(\operatorname{Hom}(K,L)$',layer,'149-171','paragraph following (2.1)','(2.1)',E+'The outer H parenthesis is not closed in the print. Corrected French retains the necessary closing parenthesis.')
        replace(rel,'etc. En dimension','etc.. En dimension',layer,'149-171','penultimate paragraph','','The print has two consecutive periods after etc. Corrected French retains a single terminal period.')
    else:
        replace(rel,'qui anticommutent à $d$','qui commutent à $d$',layer,'149-171','paragraph following (2.1)','(2.1)',E+'The displayed equation gives delta(u)=0 iff du=(-1)^n ud: graded commutation with d. The prior u-to-d correction alone leaves the wrong graded sign terminology.',kind='misprint of the original')
        old="\\footnote{Le texte imprimé porte « à $u$ » ; l'équation\n(2.1) impose « à $d$ ».}"
        new="\\footnote{Le texte imprimé porte « anticommutent à $u$ ». Par (2.1), un cycle vérifie $du=(-1)^nud$ : il commute donc à $d$ au sens gradué.}"
        replace(rel,old,new,layer,'149-171','editorial note after corrected cycle condition','(2.1)',E+'Expand the existing correction note to give the exact relation forced by (2.1), recording both the wrong letter and the wrong graded commutation wording.',kind='misprint of the original')
    upright_page(rel,layer,'149-171')
event('149-eq2.1','targeted proof check','From delta(u)=du+(-1)^(n+1)ud, delta(u)=0 is equivalent to du=(-1)^n ud. Corrected text must say graded commutation with d; the printed text says anticommutation with u. The existing letter correction is confirmed and the remaining sign terminology is corrected.','Exposé 149, p. 171, (2.1) and the following two text lines')
event('149-3','carried as background without fault found','Read the bicomplex argument and proposition; no independent proof claimed. The scan uses unstarred Ext and starred H.','Exposé 149, p. 171, Proposition 3')
record_page('149',171,'''Compared both French sources, `\\src{171}` through the printed ending complexes, against the 400-dpi image and three enlarged crops. Supplied source range was lines 125-183; the page marker was one display late. Read Proposition 3, its bicomplex explanation, section 2, (2.1), the inline Hom pairing, (2.2), and every index/sign.

Restored unstarred Ext in Proposition 3, underlined ordinary C in section 2, all printed emphasis, punctuation, the inline pairing and paragraph continuity. Moved `\\src{172}` before the short exact sequence that is absent from p. 171. Upright printed letterforms are represented explicitly.

Printed-only restorations: formé (corrected formée agrees with composante), the missing outer closing parenthesis after Hom(K,L), the duplicated period after etc., and anticommutent à u. Corrected French retains the grammatical/punctuation repairs. Existing u-to-d correction is confirmed by (2.1); the corrected sentence now also uses commutent, since the displayed sign gives graded commutation. The exact calculation is recorded as a targeted check, not a proof of surrounding claims. This new meaning correction is pending propagation to the translations in their required turn.

Source comparison completed; final second reading and PDF inspection are pending. The 17 later release dispositions do not occur here.''')
