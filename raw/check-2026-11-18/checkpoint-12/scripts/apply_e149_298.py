from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/e149.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'e149-298',line,'Remarque sur la page 14',
                'Scan leaf 2 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    r('\\noindent\\textbf{1. Théorème de dualité pour les faisceaux algébriques\ncohérents.}',
      '\\noindent 1. \\uwave{Théorème de dualité pour les faisceaux algébriques\ncohérents}.',
      'title','The title is ordinary upright with wavy underline, excluding its number and final period.','typesetting')
    r(r'\textbf{Remarque sur la page 14.}',r'\uline{Remarque sur la page 14}.',
      'remark heading','The heading is straight-underlined ordinary text, with the final period outside the underline.','typesetting')
    r(' --- ',' - ','three separators','The dash is short.',count=3)
    r('1958,\\footnote{','1958 \\footnote{','first note call','The call precedes the comma, with a space before it.')
    r('Press, 1960.}\nles questions','Press, 1960.},\nles questions','first note call','The sentence comma follows the parenthesized note call.')
    r('Grothendieck (Alexander)','GROTHENDIECK (Alexander)','footnote author','The surname is uppercase.')
    r('varieties, \\emph{Proceedings of the International Congress of Mathematicians}',
      'varieties, Proceedings of the international Congress of Mathematicians',
      'footnote title','The title is ordinary upright, with lowercase international.','typesetting')
    r('[1958, Edinburgh],','[1958. Edinburgh] ;','footnote venue','The date is followed by a period and the closing bracket by a semicolon.')
    r('103--118','103-118','footnote page range','The range dash is short.')
    r(r'\emph{loco citato}\footnotemark[1]',r'loco citato \footnotemark[1]',
      'second note call','Loco citato is upright and separated from its parenthesized call.','typesetting')
    r('112--115','112-115','body page range','The range dash is short.')
    r('EGA',r'\uwave{EGA}','two EGA references','The abbreviation has a wavy underline.',count=2)
    r('SGA 1962',r'\uwave{SGA} 1962','SGA reference','Only the abbreviation has a wavy underline.')
    r(r'2\textsuperscript{e} partie','2e partie','EGA part number','The e is on the baseline.')
    r('\\src{298}\n','\\src{298}\n\\begingroup\n\\makeatletter\n\\renewcommand\\@makefnmark{\\hbox{\\normalfont(\\textsuperscript{\\@thefnmark})}}\n\\makeatother\n',
      'note-call formatting','Both body calls and the footnote label have baseline parentheses around a raised numeral. The override is local to this erratum.','typesetting')
    r('(chapitre IX dans le plan prévu).\n','(chapitre IX dans le plan prévu).\n\\endgroup\n',
      'end of local note formatting','Close the local footnote-marker group, without changing text.','typesetting')
event('e149-p14','carried as background without fault found',
      'The erratum reports that the duality questions on original exposé page 14 have been resolved and directs the reader to the 1958 congress address, EGA III part 2 and SGA 1962. It supplies no proof or refined theorem on this page. The resolution and projected chapter IX are retained as dated authorial assertions; detailed later-source identification is reserved for the notes.',
      'Erratum 149, p. 298, Remarque sur la page 14 and note 1')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='e149-298')
record_page('e149',298,'Compared sources/fr_printed/fr/e149.tex and sources/fr/fr/e149.tex, entry lines 5-25, with scan leaf 2 at 400 dpi, full page and three enlarged bands. Read the title, bibliographic bracket, both paragraphs and the complete bottom footnote. Restored wavy and straight underlines, upright type, literal capital/lowercase lettering, baseline e, short dashes, bibliography punctuation and parenthesized note calls with raised numerals. No correction of the original is justified here, so both French layers agree. The notice of resolved duality questions is carried as background, without treating its citation as a proof checked in this run.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
