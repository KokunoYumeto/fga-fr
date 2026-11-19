from audit_utils import *
from collections import Counter
import csv
dq=chr(96)*2
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'236-231',line,'1.12, 2.1, 2.2',
                'Scan leaf 12 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,231)
    for a,b,body in reversed(list(footnotes(s))):
        r(s[a:b],'','two added footnotes','Neither footnote nor call is printed on this page.','structure')
    r('Si de plus, pour tout entier','Si de plus pour tout entier','corollary 1.12','The print has no comma after plus.')
    r(r'\longrightarrow',r'\to','two arrows','Both arrows are short.',count=2)
    r(r'\fsection{2}{Application aux propriétés locales des schémas de Picard}',
      r'\fsection{2}{\normalfont\uwave{Application aux propriétés locales des schémas de Picard}.}',
      'section heading','The heading text is upright with a wavy underline and a final period.')
    r(r'\operatorname{Pic}_{X/k}^\circ',r'\operatorname{Pic}_{X/S}^\circ',
      '2.1(ii)','The printed denominator is S; the deleted editorial footnote had silently corrected it.')
    r('tout diviseur sur\n$X$ est','tout diviseur sur\n$S$ est',
      '2.1(i) proof, divisor ambient space','The printed letter is S.')
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}','six Picard scheme names','All six names have straight underlines.',count=6)
    r('et, pour toute','et pour toute','2.1(i)','No comma follows et.')
    r(r'\result{THÉORÈME}{2.1}',r'\result[.]{THÉORÈME}{2.1}','theorem heading','The heading ends in a period and is followed by a separate paragraph, with no dash.')
    for a,b in [
        ('Soit $f:X\\to S$ un morphisme',r'\begin{proof}'),
    ]:
        s,_,_=page_text(rel,231)
        start=s.index(a)
        end=s.index(b,start)
        old=s[start:end]
        new=underline_prose(old)
        # The parenthetical example is not underlined in the image.
        new=new.replace(r'(\uline{par exemple} $f$ \uline{un morphisme projectif})',
                        '(par exemple $f$ un morphisme projectif)')
        r(old,new,'2.1(i)-(ii) statement emphasis','Both theorem statements have straight prose underlines, with formulas and the parenthetical projective example outside the prose emphasis.')
    r(r'\begin{proof}',r'\result[.]{\uline{Démonstration}}{}'+'\n',
      'proof heading','Démonstration is upright and straight underlined on its own line.','structure')
    r(r'\end{proof}','','end of proof (i)','The print has no end-of-proof symbol here.','structure')
    r('i.e.','i. e.','valuative proof','The abbreviation has an intervening space.')
    r('resp. $X$, en termes','resp. $X$ en termes','divisor classes','No comma follows X.')
    r('« de Cartier »',dq+"de Cartier''",'divisor classes','The print uses ordinary double quotation marks.')
    r('« adhérence »',dq+"adhérence''",'closure of divisor','The print uses ordinary double quotation marks.')
    r('Auslander','AUSLANDER','factoriality reference','The name is printed in capitals.')
    r('En effet,\ntout','En effet tout','divisor extension','There is no comma after effet.')
    r(r'\result{REMARQUE}{2.2}',r'\result{\normalfont\uline{Remarque}}{2.2}',
      'remark heading','Only mixed-case Remarque is straight underlined.')
    r('intersections\ncomplètes et simples','intersections\ncomplètes, et simples',
      'remark 2.2','A comma is printed after complètes.')
    r('« conjecture de Samuel »',dq+"conjecture de Samuel''",
      'factoriality theorem','The quoted phrase uses ordinary double quotation marks.')
    if tree=='fr':
        r("unité, elle l'est","unité, il l'est",'corollary 1.12',
          'The grammatical subject is the masculine group scheme G; elle has no feminine subject here.','misprint of the original')
        r(r'\underline{\operatorname{Pic}}_{X/S}^\circ',r'\underline{\operatorname{Pic}}_{X/k}^\circ',
          '2.1(ii)','The stated base is Spec k and there is no S in this assertion. The identity component is Pic_(X/k). This confirms the existing correction while removing its unprinted footnote.','misprint of the original')
        r('tout diviseur sur\n$S$ est','tout diviseur sur\n$X$ est',
          '2.1(i) proof, divisor ambient space','Factoriality is asserted for the local rings of X, so the Weil divisors made Cartier by this argument are on X; it is also on X that the closure of a divisor from V is taken. This confirms the existing correction.','misprint of the original')
    upright_page(rel,layer,'236-231')
event('236-1.11-no-proof','carried as background without fault found',
      'Following the page turn, the print proceeds directly to corollary 1.12 and section 2: there is no supplied proof of 1.11. The earlier page record saying its proof continues was anticipatory and is corrected by this observation. Its smooth/flat-locus subgroup assertion remains background; a proof needs openness of these loci, faithful-flat locality and translation.',
      '236, pp. 230-231, proposition 1.11 and following transition')
event('236-1.12','targeted proof check',
      'Conditionally on 1.11, smoothness or flatness at every unit gives U=S and an open subgroup containing every identity component. Translation by a section gives the assertion along that section. If x has prime-to-residue-characteristic torsion component class, choose n killing that class, so phi_n(x) lies in G zero; the assumed etaleness at x pulls back smoothness or flatness from this target neighbourhood. Thus the deduction to G sigma is valid. Proposition 1.11 itself remains an unproved background input here.',
      '236, p. 231, corollary 1.12')
event('236-2.1-i','targeted proof check',
      'Checked the divisor-extension mechanism: a line bundle on the generic open V has a Cartier divisor, whose Weil closure in regular X is Cartier by regular-local factoriality, yielding an extension. The printed S in that factoriality conclusion must be X. For uniqueness one also needs that vertical divisors are sums of whole connected special-fibre components, principal on their corresponding components over the complete trait. Passing from Picard-scheme sections to actual line bundles requires an fpqc splitting and descent argument; it is not supplied just by naming the definition. These component, descent and valuative-criterion inputs are recorded as background rather than treated as proved by the one paragraph. The properness conclusion for finite-type closed parts uses that a generic section lying in a closed part has its entire extension there.',
      '236, p. 231, theorem 2.1(i) and proof')
event('236-2.1-ii','carried as background without fault found',
      'Read proper geometric normality over k and properness of the identity component of the Picard scheme. The printed denominator S has no defined referent; corrected French retains the existing k correction. The proof is not on this page and no proof is claimed yet.',
      '236, p. 231, theorem 2.1(ii)')
event('236-2.2','carried as background without fault found',
      'Read the weakening to flat families with local-complete-intersection fibres smooth in codimension at most 2, and the stated local-complete-intersection factoriality theorem under regularity in codimension at most 3. The reference [5] and the continuation beginning On notera que le are retained. The parafactorial theorem is a substantial background input, not independently reproved.',
      '236, p. 231, remark 2.2')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='236-231')
record_page('236',231,'Compared sources/fr_printed/fr/236.tex and sources/fr/fr/236.tex, entry lines 461-510, with scan leaf 12 at 400 dpi, full page and three enlarged bands. Read corollary 1.12, section 2, both parts of 2.1, proof (i) and the beginning of 2.2. There is no proof of 1.11 after the page turn; the anticipatory wording on p. 230 is corrected by the explicit event here.\n\nRestored the heading and statement emphasis, six straight Picard underlines, the exact punctuation, quotes and capitalization, short arrows, and the printed S readings. Removed two editorial footnotes and the unprinted proof end symbol. Corrected French confirms Pic_(X/k) and divisors on X, and changes grammatical elle to il. Checked the deduction of 1.12 and the divisor-extension part of 2.1(i), with the required descent, vertical-divisor and valuative inputs explicitly recorded as background. The substantial factoriality theorem in 2.2 is background; its sentence continues on the next page.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
