from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'236-243',line,'4.1, 4.2; bibliography',
                'Scan leaf 24 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,243)
    tail=s[s.index('\\par\\smallskip\n\\begingroup\\footnotesize'):]
    r(tail,'','post-bibliography editorial material','The scan ends with a short horizontal rule and has none of these editorial comments. The omitted condition and earlier readings are adjudicated directly from the images.','structure')
    clause="\\noindent b''. (Si les fibres de $X/S$ ont toutes même dimension $n$). Les entiers\n$\\xi^{n-1}D_i$ et $\\xi^{n-2}D_i^2$ (degrés projectifs de $D_i$ et de $D_i^2$) restent majorés.\n\n"
    r('\\src{243}\n\n','\\src{243}\n\n'+clause,'4.1 condition b double prime',
      'The page begins with the missing condition b double prime, including both intersection exponents, the square on D, the explanatory parenthesis and the word majorés. Restore the complete condition before assessing it.','structure')
    r(r'f:X\longrightarrow S',r'f:X\to S','4.2 morphism','The arrow is short.')
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}','two Picard schemes','Both scheme names are straight-underlined.',count=2)
    r(r'\mathbf Q[t]',r'\text{\uwave{Q}}[t]','rational polynomial ring','The coefficient-field Q is ordinary with a wavy underline.')
    r(r'\section*{BIBLIOGRAPHIE}',r'\section*{\normalfont BIBLIOGRAPHIE}',
      'bibliography heading','The heading is upright ordinary capitals, not a bold section face.','typesetting')
    for n in range(1,9):
        r(r'\item[{['+str(n)+']}]',r'\item[{\normalfont ['+str(n)+']}]',
          'bibliographic labels','The bracketed numerals are upright ordinary text.','typesetting')
    for title in ['Amer. J. of Math.','Séminaire Bourbaki','Amer. J. Math.','Symposium internacional de topología algebraica']:
        r('\\emph{'+title+'}',title,'bibliographic titles','The printed title is upright, without emphasis.')
    r('Éléments de géométrie\nalgébrique, Chapitre I et suivants. -- Paris,',
      'Eléments de géométrie\nalgébrique, Chap. 1 et suivants.,- Paris,',
      'reference 2 opening','The initial E has no accent; Chap. and numeral 1 are printed, followed by period, comma and short dash.')
    r('1960--1961 (Institut des Hautes Études Scientifiques,',
      '1960--1961 Institut des hautes Etudes scientifiques,',
      'reference 2 collation','The opening parenthesis is absent in the print. The institution has lowercase hautes and scientifiques, and unaccented Etudes.')
    r('Institut des Hautes Études Scientifiques, 1961.',
      'Institut des hautes Études scientifiques, 1961.',
      'reference 4 institution','The initial letters of hautes and scientifiques are lowercase; Études is accented here.')
    r('Institut des Hautes Études\nScientifiques (à paraître).',
      'Institut des hautes Études\nscientifiques (à paraître).',
      'reference 5 institution','The initial letters of hautes and scientifiques are lowercase; Études is accented here.')
    r('[1956, Mexico], p.','[1956. Mexico] ; p.',
      'reference 8 proceedings','The print has a period after 1956 and a semicolon after the closing bracket.')
    r('autónoma','autonoma','reference 8 publisher','The printed publisher word has no accent.')
    s,_,_=page_text(rel,243)
    r('--','-','bibliographic dashes','The ranges and separating dashes are short.',count=s.count('--'))
    r('\\end{description}\n\n','\\end{description}\n\n\\begin{center}\\rule{2.5cm}{0.4pt}\\end{center}\n',
      'terminal rule','A short centred rule ends the printed item.','typesetting')
    if tree=='fr':
        r('dimension $n$). Les entiers','dimension $n\\geqslant 2$). Les entiers',
          '4.1 condition b double prime dimension','The intersection product with xi^(n-2) is defined in the stated form for n at least two. Unlike a negative polynomial coefficient, a negative power of an ample divisor has no implicit zero convention in intersection theory. Restrict this optional equivalent condition to n at least two.','misprint of the original')
        r('restent majorés.','restent bornés.',
          '4.1 condition b double prime bounds','Upper bounds on both intersection numbers are insufficient: on P1 times P1, xi=(1,1) and D_m=(m,-m) give xi.D_m=0 and D_m^2=-2m^2, both bounded above, but the polynomials (t+1)^2-m^2 form an infinite set. Two-sided bounds repair the criterion. Given the unchanged equivalence a-b prime, Hodge index bounds D.K from bounded H^(n-1)D and H^(n-2)D^2, and Riemann-Roch then bounds the two relevant polynomial coefficients with fixed denominators. Those index and Riemann-Roch inputs are recorded explicitly.','misprint of the original')
        r('suivants.,- Paris','suivants. - Paris','reference 2 punctuation',
          'The comma immediately after a sentence-ending period before the separator is duplicated punctuation; retain the period and dash.','misprint of the original')
        r('1960-1961 Institut des hautes Etudes scientifiques,',
          '1960-1961 (Institut des hautes Etudes scientifiques,',
          'reference 2 collation','The printed closing parenthesis after the series numbers has no matching opener. Supply the opener before the institutional series description.','misprint of the original')
    upright_page(rel,layer,'236-243')
event('236-4.1-b-double-prime','refuted, with the refined statement\'s id',
      'The printed upper-bound criterion is false. On X=P1_k times P1_k with polarization H=(1,1), take L_m=O(m,-m), m positive. The corresponding divisors satisfy H.D_m=0 and D_m^2=-2m^2, hence both numbers are bounded above. Their Hilbert polynomials are (t+m+1)(t-m+1)=(t+1)^2-m^2, so condition b fails. This is an independent calculation from the printed statement, not reliance on the deleted editorial reference. Refined statement: 236-4.1-b-double-prime-bounded.',
      '236, p. 243, condition b double prime')
event('236-4.1-b-double-prime-bounded','targeted proof check',
      'Refinement: for common fibre dimension n at least two, both displayed intersection integers remain bounded on both sides. This is necessary for a bounded family. For sufficiency, write D along H plus its H-primitive part. Bounded H^(n-1)D and H^(n-2)D^2 bound the negative norm of the primitive part. Hodge index and Cauchy-Schwarz then bound H^(n-2)D.K, since the relative canonical intersection numbers have finitely many values on the Noetherian base. Riemann-Roch gives a_(n-1)=(H^(n-1)D-H^(n-1)K/2)/(n-1)! and a_(n-2) from H^(n-2)(D^2-D.K)/2 plus the fixed Todd contribution. Their denominators are fixed, so boundedness gives finite coefficient sets and the unchanged b-prime criterion applies. The Hodge-index, Riemann-Roch and relative characteristic-number invariance inputs, and the substantive b-prime-to-a theorem, are background; the numerical implication was checked conditional on them.',
      '236, p. 243, corrected condition b double prime')
event('236-4.2','targeted proof check',
      'Given the unchanged a-b boundedness theorem in 4.1, each fixed-polynomial stratum is of finite type; the torsion locus is so locally on the base by the qualification checked on p. 242. The relevant loci are open and closed in the Picard scheme. Applying the projectivity criterion 2.4 to these finite-type unions of connected components gives the claimed projectivity. This deduction does not use the refuted printed upper-bound clause. The representability and projectivity inputs remain background.',
      '236, p. 243, corollary 4.2 and proof')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='236-243')
record_page('236',243,'Compared sources/fr_printed/fr/236.tex and sources/fr/fr/236.tex, entry lines 1014-1063, with scan leaf 24 at 400 dpi, full page and three enlarged bands, including all eight bibliographic entries and the terminal rule.\n\nRestored the omitted condition b double prime in both layers, then corrected its upper bounds to two-sided bounds and its meaningful dimension range in corrected French only. An explicit P1 times P1 family refutes the printed condition; the refined numerical implication is checked with the named Hodge-index and Riemann-Roch inputs. Removed unprinted end comments. Restored straight Picard names, wavy Q, short arrow and dashes, ordinary bibliography fonts, literal institutional case and accents, chapter abbreviation, proceedings punctuation and rule. Corrected French repairs the unmatched bibliographic parenthesis and duplicated punctuation. Checked the corollary from the unchanged boundedness criterion without using the false printed clause.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
