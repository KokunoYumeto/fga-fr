from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/com.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'com-298',line,'Sigles employés',
                'Scan leaf 3 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    for abbr in ['SHG','SHMT','EGA','TDTE']:
        r(r'\item['+abbr+' :]',r'\item[{\normalfont\uwave{'+abbr+'} :}]',
          abbr+' label','The upright abbreviation is wavy-underlined; the colon is outside the underline.','typesetting')
    r('MUMFORD--TATE','MUMFORD-TATE','SHMT','The joining dash is short.')
    r(' --- ',' - ','bibliographic separators','The bibliographic dash is short.',count=3)
    r('Éléments de géométrie','Eléments de géométrie','EGA title','The initial capital E has no acute accent.')
    r('Hautes Études Scientifiques','Hautes Etudes Scientifiques','EGA institution','The capital E of Etudes is unaccented.')
    r('I--VI','I-VI','TDTE range','The range dash is short.')
    r(r'\emph{Séminaire Bourbaki}','Séminaire Bourbaki','TDTE periodical','The periodical name is upright, not italic.','typesetting')
event('com-sigles','carried as background without fault found',
      'Read all four remaining abbreviation entries, including dates, volume numbers and exposé numbers. The printed TDTE sequence is 190/195, 212/221, 232/236. These are bibliographic descriptions, with no mathematical assertion or change of a theorem.',
      'Commentaires, p. 298, SHG, SHMT, EGA and TDTE')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='com-298')
record_page('com',298,'Compared sources/fr_printed/fr/com.tex and sources/fr/fr/com.tex, entry lines 44-66, with scan leaf 3 at 400 dpi, full page and three enlarged bands. Read SHG, SHMT, EGA and TDTE, including all accents, dates, volume/exposé numbers and the terminal punctuation. Restored wavy abbreviation underlines, upright periodical title, short dashes and literal unaccented initial capitals. The comma before the first ellipsis and singular n° before each pair are retained as printed. No new difference between the French layers is warranted on this page.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
