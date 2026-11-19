from audit_utils import *
from collections import Counter
import csv
dq=chr(96)*2
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/e190.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'e190-300',line,'Errata to TDTE I',
                'Scan leaf 2 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    old="\\noindent\\textbf{3. Technique de descente et théorèmes d'existence en\ngéométrie algébrique [TDTE I]. I : Généralités. Descente par morphismes\nfidèlement plats.}"
    new="\\noindent 3. \\uwave{Technique de descente et théorèmes d'existence en\ngéométrie algébrique} [TDTE I].\n\\par\\noindent I : \\uwave{Généralités. Descente par morphismes\nfidèlement plats}."
    r(old,new,'title and subtitle','The two title lines are ordinary text with wavy underlines; the numbering, brackets and final periods are outside the title-word underlines.','typesetting')
    for title in ['Page 1, ligne 10','Page 5, ligne 16','Page 20, remarque','Page 26, ligne 9']:
        r(r'\textbf{'+title+'.}',r'\uline{'+title+'}.','four entry headings',
          'The ordinary entry heading has a straight underline.','typesetting')
    r(' --- ',' - ','entry separators','The dashes are short.',count=4)
    r('TDTE',r'\uwave{TDTE}','three series abbreviations','The abbreviation alone has a wavy underline.',count=3)
    r('SGA VI',r'\uwave{SGA} VI','final reference','The abbreviation has a wavy underline.')
    r('« ',dq,'three quotations','The print has ordinary double quotation marks.',count=3)
    r(' »',"''",'three quotations','The print has ordinary double quotation marks.',count=3)
    r(r'\mathcal F',r'\mathfrak F','descent category','The F is Gothic, not script.')
    r(r'\widehat A',r'\overline A','completion','The completion sign is a horizontal overbar, not a hat.')
    r(r'\longrightarrow',r'\to','four morphisms','The arrows are short.',count=4)
    r('non isotrivial',r'\uline{non isotrivial}','torsor conclusion','Both words have a straight underline.')
    r('Chow--Lang','CHOW-LANG','correct attribution','Uppercase surnames and a short joining dash are printed.')
    r('Igusa--Lang','IGUSA-LANG','replaced attribution','Uppercase surnames and a short joining dash are printed.')
    upright_page(rel,layer,'e190-300')
event('e190-p1','carried as background without fault found',
      'Read the authorial qualification of the role of descent in projective versus non-projective existence techniques. It is a methodological comment, not a new theorem.',
      'Erratum 190, p. 300, Page 1, ligne 10')
event('e190-split-descent','targeted proof check',
      'Checked that a split morphism alpha with section s gives effective descent in any fibred category with the stated pullbacks, without a separate descent hypothesis. For an object xi prime with descent datum, take xi=s star xi prime. Pulling the descent isomorphism along the pair (s alpha,id) gives alpha star xi isomorphic to xi prime; the cocycle identity gives compatibility. For an invariant morphism u prime, take u=s star u prime; the same pair proves alpha star u=u prime, and s star alpha star=id proves uniqueness. Thus both full faithfulness and effectiveness follow from the section. The original passage remains unchanged, with this weakening only in the erratum.',
      'Erratum 190, p. 300, Page 5, ligne 16; exposé 190, p. 303, after definition 1.7')
event('e190-p20','carried as background without fault found',
      'Read the announced non-projective elliptic torsor over a local algebraic curve, becoming projective after the indicated étale cover or completion. No construction is supplied here. This directly concerns failure of descent in the projective subcategory; by itself the already existing scheme X does not exhibit ineffective descent in the category of all schemes. The unqualified non-strict-descent assertion and the non-isotrivial conclusion are retained as background claims requiring the category and finite-cover convention to be made explicit in the notes.',
      'Erratum 190, p. 300, Page 20, remarque')
event('e190-p26','carried as background without fault found',
      'Read the correction CHOW-LANG in place of IGUSA-LANG and the references SGA VI, VII, VIII. Preserve the attribution instruction in the erratum without merging it into the exposé.',
      'Erratum 190, p. 300, Page 26, ligne 9 and final sentence')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='e190-300')
record_page('e190',300,'Compared sources/fr_printed/fr/e190.tex and sources/fr/fr/e190.tex, entry lines 5-44, with scan leaf 2 at 400 dpi, full page and three enlarged bands. Read the two title lines, bibliography, all four errata and final reference. Restored wavy titles/abbreviations, straight headings and non isotrivial, Gothic F, completion overbar, ordinary quotes, uppercase paired attributions, short dashes/arrows and upright variables. Both layers agree; the printed participial wording mais f n’étant pas projectif is retained. Proved the split-morphism weakening directly using the section and cocycle. The non-projective torsor existence report remains background, with the distinction between projective descent and descent of all schemes recorded explicitly.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
