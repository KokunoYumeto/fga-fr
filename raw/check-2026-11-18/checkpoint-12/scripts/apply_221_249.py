from audit_utils import *
import csv
from collections import Counter

for tree, layer in [('fr_printed', 'French as printed'), ('fr', 'French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(old,new,line,why,kind='reading',count=1):
        replace(rel,old,new,layer,'221-249',line,'Introduction / section 1',
                'Scan leaf 2 at 400 dpi, full page and enlarged top, middle and bottom crops: '+why,
                kind=kind,count=count)
    r(r'13\textsuperscript{e} année','13e année','seminar header','The e of 13e is on the baseline.')
    r('IV. LES SCHÉMAS DE HILBERT','IV : LES SCHÉMAS DE HILBERT','title','The part number is followed by a colon.')
    r('\\subsection*{Introduction}\n\\addcontentsline{toc}{subsection}{Introduction}\n\n',
      '\\phantomsection\\addcontentsline{toc}{subsection}{Introduction}\n\\noindent INTRODUCTION. - ',
      'introduction heading','INTRODUCTION. - is an ordinary upright run-in heading, not a separate mixed-case subsection.','structure')
    r('« schémas de Hilbert »','"schémas de Hilbert"','introduction paragraph 1','The quoted name has ordinary double quotation marks.')
    r('« sans points\nfixes »','"sans points\nfixes",','introduction paragraph 2','Ordinary quotation marks and a comma before (cf.) are printed.')
    r('« projectifs »','"projectifs"','introduction paragraph 2','The word is enclosed in ordinary double quotation marks.')
    r(r"\footnote{Voir l'additif à la fin de l'exposé.}",
      r"\textnormal{(*)}\begingroup\renewcommand{\thefootnote}{(*)}\stepcounter{footnote}\footnotetext{Voir l'additif à la fin de l'exposé.}\endgroup",
      'introduction paragraph 2 and footnote','The note is present, with a baseline parenthesized asterisk in the text and (*) as its label; its wording is retained.','structure')
    r(r'\fsection{1}{Familles limitées de faisceaux : propriétés de permanence}',
      r'\fsection{1}{\normalfont\uline{Familles limitées de faisceaux : propriétés de permanence}.}',
      'section 1 heading','The words are straight-underlined in ordinary type, with a final period outside the underline.')
    if tree=='fr_printed':
        r(r"\mathcal F\otimes_K K'=\mathcal F_{K'}",
          r"\mathcal F\otimes_K K'={}_{K'}",
          'section 1, line 3','The enlarged formula has no sheaf letter between the equals sign and the subscript K-prime. Restore the visible omission in the printed layer.')
    else:
        r(r"\mathcal F\otimes_K K'=\mathcal F_{K'}",
          r"\mathcal F\otimes_K K'={\mathcal F}_{K'}",
          'section 1, line 3','The print omits the sheaf letter before subscript K-prime. The corrected layer supplies F: this is the defined scalar extension of the previously introduced sheaf F. The braces make that documented existing emendation explicit in the source.',
          'misprint of the original')
    upright_page(rel,layer,'221-249')

event('221-1-base-change-notation','carried as background without fault found',
      'The scalar-extension notation is read, not independently proved. The print omits F before the subscript K-prime in its defining equality; the corrected layer retains the mathematically forced sheaf symbol and the printed layer reproduces the omission.',
      '221, p. 249, section 1 opening paragraph, third line')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    counts=Counter((r['layer'],r['kind']) for r in csv.DictReader(f,delimiter='\t') if r['printed_page']=='221-249')
record_page('221',249,
    'Compared sources/fr_printed/fr/221.tex and sources/fr/fr/221.tex, entry lines 3-47, with scan leaf 2 at 400 dpi and all three enlarged bands. Read the header, title, both introductory paragraphs, all references, the section heading, the opening base-change paragraph and its footnote. All small indices and primes are in the enlarged bottom band.\n\n'
    'Restored baseline 13e, title colon, the run-in introduction heading, ordinary quotation marks, the comma after the fixed-point quotation, the parenthesized asterisk note marker, straight-underlined section title and upright mathematical letters. The printed equality genuinely lacks F before its final subscript K-prime; that omission is restored only in the printed layer and the existing correction is explicitly recorded in the corrected layer. No later erratum is merged. The claims in the introduction remain historical background, with no proof claimed.\n\n'
    'Operation counts: '+ '; '.join(f'{layer}, {kind}: {n}' for (layer,kind),n in sorted(counts.items()))+
    '. All verdicts remain provisional until the final row-by-row second reading.')
from update_record_counts import update
update()
