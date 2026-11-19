from audit_utils import *
from collections import Counter
import csv
dq=chr(96)*2
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'236-242',line,'4; 4.1',
                'Scan leaf 23 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,242)
    for a,b,_ in list(footnotes(s)):
        r(s[a:b],'','two editorial footnotes','Neither footnote occurs in the print; their verdicts belong in the record.','structure')
    r('est séparable et à fibres\ngéométriques irréductibles',
      'est \\uline{séparable} et à \\uline{fibres\ngéométriques irréductibles}',
      'opening hypotheses','The two indicated phrases are underlined, with et à outside the underline.')
    for phrase in ['de torsion','identique à','limitées',"critères d'équivalence"]:
        r('« '+phrase+' »',dq+phrase+"''",'quotation marks','The print uses ordinary double quotation marks.')
    r('Matsusaka','MATSUSAKA','two attributions','The name is in capitals.',count=2)
    r('IV :\nconsidérons','IV :\nConsidérons','bounded family problem','Considérons begins with a capital after the colon.')
    r('$r,n,d,Q$ sont donnés) ; montrer','$r,n,d,Q$ sont donnés), montrer',
      'given parameters','A comma, not semicolon, follows the parenthesis.')
    r('est limitée, i.e.','est \\uline{limitée}, i.e.',
      'bounded family','Limitée has a straight underline here.')
    r("lorsque l'on se borne","lorsque on se borne",'smooth subvarieties','The literal phrase is lorsque on, without l apostrophe.')
    r(r'\result{THÉORÈME}{4.1} Soit $f:X\longrightarrow S$',
      r'\result{THÉORÈME}{4.1} Soient : $X\to S$',
      '4.1 opening list','The print says Soient : X to S, with no morphism letter f. Soient correctly introduces the list of several objects, and an unnamed displayed arrow is meaningful, so both layers retain the printed wording.')
    r('sur $\\overline X_{s_i}$ définissant $\\mathcal L_i$,\n\\[\na_n^{(i)}t^n+\\cdots+a_0^{(i)}\n\\]\nle polynôme',
      'sur $\\overline X_{s_i}$ définissant $\\mathcal L_i$, $a_n^{(i)}t^n+\\cdots+a_0^{(i)}$ le polynôme',
      'Hilbert polynomial','The polynomial is inline in the list of data.','structure')
    r(r'\noindent a. $E$',r'\noindent a. $Q$','4.1 condition a','The printed letter is Q, not E.')
    r('dimension $n$.)','dimension $n$).','4.1 condition b prime','The period is outside the parenthesis.')
    r('i.e.','i. e.','five abbreviations','The letters are separated by a space.',count=5)
    r(r'\mathbf P',r'\text{\uwave{P}}','three projective spaces','P is ordinary with a wavy underline.',count=3)
    r(r'\mathbf Z',r'\text{\uwave{Z}}','integer base','Z is ordinary with a wavy underline.')
    r(r'\mathbf Q',r'\text{\uwave{Q}}','rational coefficient field','Q is ordinary with a wavy underline.')
    r(r'f:X\longrightarrow S',r'f:X\to S','opening morphism','The arrow is short.')
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}','seven Picard names','All seven names are straight-underlined.',count=7)
    if tree=='fr':
        r(r'\noindent a. $Q$',r'\noindent a. $E$','4.1 condition a',
          'E is the subset of the Picard scheme introduced in the data and used again in b. Q denotes a polynomial, so its quasi-compactness cannot express the stated boundedness of the family. Restore E.','misprint of the original')
        r(r'$\underline{\operatorname{Pic}}_{X/S}^\tau$ est contenu dans un des',
          r'$\underline{\operatorname{Pic}}_{X/S}^\tau$ est contenu, localement sur $S$, dans un des',
          'torsion in a Hilbert polynomial locus','The polynomial of O on the fibres is only locally constant on S. For S consisting of two points, take P1 polarized by O(3) on one component and a smooth plane cubic on the other: the zero Picard classes have polynomials 3t+1 and 3t. Thus there is no single global Q. Locally on S the stated containment is correct, and finite type can then be checked locally on the base.','misprint of the original')
    upright_page(rel,layer,'236-242')
event('236-4-torsion-polynomial','targeted proof check',
      'A torsion-algebraically-trivial line bundle is numerically trivial; equality of Hilbert polynomials with O uses the numerical-invariance input. The resulting polynomial is locally constant on the base, not necessarily one fixed global polynomial. The disconnected example P1 with O(3) and a plane cubic gives 3t+1 versus 3t, even for smooth projective geometrically connected fibres. Corrected French inserts localement sur S. On an affine Noetherian base neighbourhood with constant polynomial, the open torsion locus inside a finite-type polynomial locus is quasi-compact, so the finite-type deduction remains valid locally and hence over S. Matsusaka\'s converse numerical criterion remains background.',
      '236, p. 242, opening paragraph')
event('236-4-boundedness-question','carried as background without fault found',
      'Read the boundedness formulation for line bundles with a fixed polynomial on integral projective subschemes of fixed ambient dimension, dimension and degree, over all algebraically closed fields, and the announced smooth-subvariety result using Matsusaka\'s method. These are the author\'s question and announced theorem, not a proof supplied on this page.',
      '236, p. 242, boundedness formulation and paragraph before 4.1')
event('236-4.1-a-b','targeted proof check',
      'The subset E, not the polynomial Q, is the object whose quasi-compactness is asserted in a. For a locally finite-type scheme over Noetherian S, a quasi-compact subset lies in a finite union of affine finite-type opens; conversely every subset of such a Noetherian open is quasi-compact. Since Hilbert-polynomial strata are open and closed, a quasi-compact E meets only finitely many, proving a implies b. A finite set of polynomials has a finite set of coefficients, proving b implies b prime where the indicated coefficients are defined. The substantive reverse boundedness implications and identification with a bounded family require the announced theorem and local universal families; they remain background pending the rest of the statement. For n below two, negative-index coefficients require the conventional value zero rather than a new coefficient.',
      '236, p. 242, theorem 4.1, data and conditions a, b, b prime')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='236-242')
record_page('236',242,'Compared sources/fr_printed/fr/236.tex and sources/fr/fr/236.tex, entry lines 966-1021, with scan leaf 23 at 400 dpi, full page and three enlarged bands. Read the boundedness discussion and theorem 4.1 through condition b prime.\n\nRemoved two unprinted editorial footnotes. Restored underlining, capitals, ordinary quotes, literal punctuation and words, the inline polynomial, wavy P/Q/Z, seven straight Picard names and short arrows. Restored Soient : X to S in both layers because its plural list and unnamed morphism are valid. Printed French has Q in condition a; corrected French retains E with the object-type justification. Corrected French adds the necessary local-on-S qualifier to the single-polynomial containment, checked by a disconnected smooth projective example. The easy quasi-compactness and coefficient implications were checked; the deep boundedness converse remains an announced result.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
