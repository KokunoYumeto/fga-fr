from audit_utils import *
from collections import Counter
import csv
dq=chr(96)*2
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/com.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'com-297',line,'Avertissement; Sigles employés',
                'Scan leaf 2 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    r(r'14\textsuperscript{e}',r'14e','seminar year','The e is on the baseline, not raised.')
    for title in ['Avertissement','Sigles employés']:
        r(r'\section*{'+title+'}',r'\section*{\normalfont\uwave{'+title+'}.}',
          'two headings','The mixed-case heading is ordinary upright text with a wavy underline and final period.','typesetting')
    r("géométrie algébrique. À l'exception", "géométrie algébriques. A l'exception",
      'opening subject','The print has algébriques with a final s and unaccented capital A.')
    r('dans le cadre des schémas.','dans le cadre des \\uline{schémas}.',
      'framework','Only schémas is straight-underlined.')
    r('« Éléments de géométrie algébrique »',dq+"Eléments de géométrie algébrique''",
      'treatise title','The title has ordinary double quotes and unaccented initial E.')
    r('MUMFORD--TATE','MUMFORD-TATE','Harvard seminar','The joining dash is short.')
    r(r'\item[SGA :]',r'\item[{\normalfont\uwave{SGA} :}]',
      'SGA abbreviation','The abbreviation is ordinary upright capitals with a wavy underline; the colon is not underlined.','typesetting')
    r('1960--1962','1960-1962','SGA years','The date range has a short dash.')
    if tree=='fr':
        r('Fondements de la géométrie algébriques.',
          'Fondements de la géométrie algébrique.',
          'opening subject','The adjective qualifies singular géométrie and repeats the work\'s singular title printed at the top of the same page. Remove the erroneous final s.','misprint of the original')
event('com-avertissement','carried as background without fault found',
      'Read the author\'s May 1962 account of the eight exposés, their intended inclusion in EGA, the purpose of the collected comments and errata, and the IHES/Harvard seminar notes. These are dated authorial descriptions and expectations, not present-day publication claims or independently verified historical findings. No mathematical theorem is asserted on this page.',
      'Commentaires, p. 297, Avertissement and SGA abbreviation')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='com-297')
record_page('com',297,'Compared sources/fr_printed/fr/com.tex and sources/fr/fr/com.tex, entry lines 3-43, with scan leaf 2 at 400 dpi, full page and three enlarged bands. Read the full heading, three preface paragraphs and first abbreviation.\n\nRestored baseline 14e, wavy heading and SGA underlines, straight schémas emphasis, ordinary quotes, literal initial accents and short dashes. Printed French preserves algébriques; corrected French repairs agreement with singular géométrie, confirmed by the title on the same page. All names and attributions are retained. The dated historical account is recorded as background, without a mathematical proof claim.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
