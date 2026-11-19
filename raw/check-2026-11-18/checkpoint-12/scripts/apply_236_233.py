from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'236-233',line,'2.5, 2.6, unnumbered corollary',
                'Scan leaf 14 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,233)
    for a,b,body in reversed(list(footnotes(s))):
        r(s[a:b],'','added theorem footnote','The page has no footnote or footnote call.','structure')
    r(r'x\in\operatorname{Pic}_{X/S}',r'x\in X','theorem 2.5','The print says x in X.')
    r(r'\longrightarrow',r'\to','three structure arrows','All three arrows are short.',count=3)
    s,_,_=page_text(rel,233)
    a=s.index('Soit $f:X');b=s.index('\n\nPar la caractérisation',a)
    r(s[a:b],underline_prose(s[a:b]),'theorem 2.5 emphasis','The statement prose is straight underlined, with the symbols outside the prose underline.')
    r('soit\n\\[\nA_{\\nu-1}=A/\\mathfrak m^\\nu,\n\\qquad X_{\\nu-1}=X\\otimes_A A_{\\nu-1},\n\\]\n',
      'soit $A_{m-1}=A/\\mathfrak m^\\nu$, $X_{\\nu-1}=X\\otimes_A A_{\\nu-1}$, ',
      'lemma 2.6 initial definitions','Both definitions are inline. The first A subscript is visibly m-1, while the next two are nu-1.','structure')
    r('isomorphe à\n\\[\n\\mathcal L_{\\nu-1}=\\mathcal L\\otimes_A A_{\\nu-1}.\n\\]\nAlors',
      'isomorphe à $\\mathcal L_{\\nu-1}=\\mathcal L\\otimes_A A_{\\nu-1}$. Alors',
      'lemma 2.6 reduction of L','The equality is inline.','structure')
    r('On pose\n\\[\nV=\\mathfrak m^\\nu=\\mathfrak m^\\nu/\\mathfrak m^{\\nu+1} ;\n\\]\nc\'est',
      "On pose $V=\\mathfrak m^\\nu=\\mathfrak m^\\nu/\\mathfrak m^{\\nu+1}$, c'est",
      'proof, small-extension ideal','The equality is inline and followed by a comma.','structure')
    r("en un Module inversible quelconque $\\mathcal L'$ sur $X$",
      "en un Module inversible quelconque sur $\\mathcal L'$ sur $X$",
      'proof, first lift','The print has the extra word sur before L prime as well as sur X.')
    for degree,nextword in [('2','mais'),('1','et')]:
        old='se trouve dans\n\\[\nH^'+degree+'(X_0,\\mathcal O_{X_0})\\otimes_k V,\n\\]\n'+nextword
        new='se trouve dans $H^'+degree+'(X_0,O_{X_0})\\otimes_k V$, '+nextword
        r(old,new,'proof, cohomology degree '+degree,'The cohomology expression is inline; the structure-sheaf O is ordinary upright, not script.','structure')
    r('puisque $n$ est premier','puisque $n$ premier','proof, vanishing obstruction','The printed clause omits est.')
    r(r'\mathfrak m',r'm','five maximal-ideal symbols','All five m letters are ordinary typed letters, not Gothic.',count=5)
    r('points de $\\operatorname{Pic}_{X/S}^\\circ$. Si',
      'points de $\\operatorname{Pic}_{X/S}^\\sigma$. Si',
      'unnumbered corollary, first conclusion','The superscript in this occurrence is sigma, not the circle used in the next sentence.')
    r('géométriquement normaux, cf. (2.3)), alors',
      'géométriquement normaux, cf. (2.3), alors',
      'unnumbered corollary, second parenthesis','Only the reference-closing parenthesis is printed; the outer one is missing.')
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}',
      'six Picard scheme names','All six names are straight underlined.',count=6)
    if tree=='fr':
        r(r'x\in X',r'x\in\underline{\operatorname{Pic}}_{X/S}',
          'theorem 2.5','The endomorphism phi_n acts on the Picard scheme, so its etale points are points of that scheme, not of X. This confirms the existing correction while removing its unprinted footnote.','misprint of the original')
        r(r'A_{m-1}=A/m^\nu',r'A_{\nu-1}=A/m^\nu',
          'lemma 2.6 initial quotient','The immediately following X and L reductions use A_(nu-1), the quotient by m^nu. The ideal m is not an integer index and cannot define m-1.','misprint of the original')
        r("quelconque sur $\\mathcal L'$ sur $X$","quelconque $\\mathcal L'$ sur $X$",
          'proof, first lift','L prime names the invertible Module being chosen on X; the extra sur before its name makes the syntax wrong.','misprint of the original')
        r('puisque $n$ premier','puisque $n$ est premier',
          'proof, vanishing obstruction','Restores the omitted finite verb in the clause whose subject is n.','misprint of the original')
        r('géométriquement normaux, cf. (2.3), alors',
          'géométriquement normaux, cf. (2.3)), alors',
          'unnumbered corollary, second parenthesis','Closes the parenthesis opened before par exemple.','misprint of the original')
    upright_page(rel,layer,'236-233')
event('236-2.5','targeted proof check',
      'The multiplication map acts on Pic_(X/S), confirming the correction of x in X. For an infinitesimal square-zero extension, n acts invertibly on the additive kernel 1+I of the units sheaf whenever n is invertible in the residue field. The cohomological lifting calculation in 2.6 therefore gives formal etaleness of the power map, including uniqueness on the relative Picard functor. Local finite presentation then gives etaleness. Passage from line bundles to the fpqc Picard sheaf and the formal criterion are background inputs explicitly needed by the argument.',
      '236, p. 233, theorem 2.5 and its reduction')
event('236-2.6','targeted proof check',
      'For the intended positive index nu, I=m^nu O_X is square-zero and, by flatness inherited from 2.5, is O_(X_0) tensor_k V. The unit exact sequence places the lifting obstruction in H2(I). Tensoring n times multiplies that obstruction by n; the given nth power extends, so it vanishes because n is invertible. A lift can then be adjusted by a class in H1(I), solving n eta=xi. The same invertibility supplies uniqueness for the infinitesimal Picard-functor lifting problem. The printed first quotient index m-1 is therefore nu-1. The statement does not explicitly say that the chosen root extends the prescribed root or state uniqueness; these stronger facts are what its proof uses. Index nu is taken positive, as required for this infinitesimal step; if one permitted nu=0, the purported assertion would fail for O(1) on P1 and n=2. This boundary convention is noted rather than silently rewriting the true intended lifting lemma.',
      '236, p. 233, lemma 2.6 and proof')
event('236-2.6-corollary','targeted proof check',
      'The first printed conclusion is universal openness of the ambient Picard morphism at Pic sigma, not merely Pic zero. Locally on S choose an integer n>1 invertible near the point; 2.5 makes its power map etale and hence universally open. Refined 1.5 and 1.1 then give the stated conclusions under absence of additive components. The added invertibility qualification in refined 1.5 causes no problem because n can be chosen locally. The distinction between openness of the ambient morphism at sigma and universal openness of the sigma locus itself when the identity locus is closed is retained, as is the equal-characteristic rho conclusion. The cited group-locus theorems remain the background inputs.',
      '236, p. 233, unnumbered corollary')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='236-233')
record_page('236',233,'Compared sources/fr_printed/fr/236.tex and sources/fr/fr/236.tex, entry lines 553-618, with scan leaf 14 at 400 dpi, full page and all three enlarged bands. Read 2.5, 2.6 with its proof, and the unnumbered corollary.\n\nRestored the statement emphasis, inline definitions and cohomology, plain m and O, straight Picard names, short arrows, the original x in X, first index m-1, extra sur and omitted est. The corollary first has sigma, not zero, in both layers; the missing outer parenthesis is restored only in corrected French. Corrected French alone also retains the existing Picard-domain correction and fixes the quotient index and the two grammatical slips. Checked the square-zero obstruction and adjustment calculation, distinguishing formal lifting from its sheaf and finite-presentation inputs; documented the implicit positive nu and the unstated stronger lifting/uniqueness conclusions. The unnamed corollary remains unnamed.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
