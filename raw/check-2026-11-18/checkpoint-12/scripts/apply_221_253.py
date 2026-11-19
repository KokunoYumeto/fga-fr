from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-253',line,'1.3 / section 2',
                'Scan leaf 6 at 400 dpi and enlarged page bands: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,253)
    for a,b,body in list(footnotes(s)):
        r(s[a:b],'','Proposition 1.3 / footnote','There is no footnote in the print; the grammatical correction is documented separately.','structure')
    if tree=='fr':
        r('famille limitée de classes','famille limitée de classe','Proposition 1.3 first line','The printed noun is singular classe.')
        r('famille limitée de classe','famille limitée de classes','Proposition 1.3 first line','E is a family of equivalence classes, as defined in 1.1; the plural classes restores the noun phrase and is retained from the supplied corrected edition.','misprint of the original')
    s,_,_=page_text(rel,253)
    m=re.search(r'(\\result\{PROPOSITION\}\{1\.3\} )(.*?)(\n\n)',s,re.S)
    assert m
    r(m.group(2),underline_prose(m.group(2)),'Proposition 1.3, all four lines','The proposition prose is straight-underlined; its formulas are excluded.')
    r('induite, i.e.','induite, i. e.','explanation, line 2','There is a space between the two abbreviation letters.')
    for c in ['p','q']:
        r(r'\mathfrak '+c,r'\text{\uwave{'+c+'}}','primary-decomposition explanation',
          'The two '+c+' symbols are ordinary lowercase letters with a wavy underline, not Gothic.',count=2)
    r('$\\mathcal F$ (le corps','$\\mathcal F$, (le corps','primary-decomposition explanation, end','A comma precedes the final parenthesis.')
    r(r'\fsection{2}{Familles limitées et polynôme de Hilbert}',
      r'\fsection{2}{\normalfont\uline{Familles limitées et polynôme de Hilbert}.}',
      'section heading','The words are ordinary straight-underlined type, followed by a full stop.')
    r('À tout faisceau','A tout faisceau','Hilbert-polynomial paragraph opening','The initial capital A has no grave accent in the print.')
    old="\\[\nP_{\\mathcal F}(n)=\\text{caractéristique d'Euler--Poincaré de $\\mathcal F(n)$\nsur $X_K$},\n\\]"
    new="\\[\n\\symup{P_{\\mathcal F}(n)}=\\text{caractéristique d'Euler-Poincaré de $\\symup{F(n)}$\nsur $\\symup{X_K}$}\n\\]"
    r(old,new,'Hilbert-polynomial defining display','The display has a short hyphen, ordinary typed F(n) on the right, script F in the left subscript, upright variables, and no terminal comma.')
    r(r'\emph{polynôme de Hilbert}',r'\uline{polynôme de Hilbert}','sentence after the display','The defined term is straight-underlined.')
    r('plat par rapport','\\uline{plat} par rapport','final paragraph','The flatness hypothesis is straight-underlined.')
    upright_page(rel,layer,'221-253')
event('221-1.2','carried as background without fault found','Read the remaining condition that the cokernel be flat over T_0 after subdivision; this completes the printed proof reading, without an independent proof of the needed flattening results.','221, p. 253, opening three lines')
event('221-1.3','carried as background without fault found','Read boundedness of reduced supports and the primary-decomposition variants. Preserved the algebraically closed field hypothesis and the minimality qualification; only the supplied grammatical plural is retained as an emendation.','221, p. 253, Proposition 1.3 and following paragraph')
event('221-2-Hilbert-polynomial','carried as background without fault found','Read the Euler-characteristic definition, eventual H^0 formula, flat-family constancy on connected components and finiteness of the polynomial set without flatness. These are carried as background; no independent proof or external-reference verification is claimed.','221, p. 253, section 2')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-253')
record_page('221',253,'Compared both French 221.tex files, entry lines 191-238, with scan leaf 6 at 400 dpi and all three enlarged bands. Read the proof continuation, Proposition 1.3, the primary-decomposition paragraph, section heading and the three Hilbert-polynomial paragraphs, including the single displayed definition and all cohomology degrees and delimiters.\n\nRestored statement and term underlining, wavy ordinary p and q, the printed punctuation, the unaccented capital A, and the distinct ordinary F(n) in the display while retaining script F in its polynomial subscript. The looped handwritten O letters remain script O. The higher-cohomology expression has both closing parentheses and is unchanged. A close crop of the first support expression shows a faint short ink trace beside the full opening parenthesis, not a second full delimiter; one opening parenthesis is retained. The only printed/corrected difference on this page is the supplied singular classe versus justified plural classes; its unprinted note is removed.\n\nOperation counts: '+ '; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. All final row verdicts remain pending.')
from update_record_counts import update
update()
