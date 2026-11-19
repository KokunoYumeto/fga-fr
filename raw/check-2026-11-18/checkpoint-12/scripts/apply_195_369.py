from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/195.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'195-369',line,'A.1','400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 r(r'12\textsuperscript{e} année','12e année','seminar year',why='The e is on the baseline.')
 r(r'\\Février 1960',r'\\\hfill Février 1960','seminar date',why='The date is right aligned on its own line.')
 r(r'\paperhead{TECHNIQUE',r'\paperhead{\sffamily\bfseries TECHNIQUE','title font',why='The title is in heavier sans-serif display lettering, unlike the typed body.')
 r('{par Alexander GROTHENDIECK}',r'{\sffamily\bfseries par Alexander GROTHENDIECK}','author font',why='The author line uses the same heavier sans-serif lettering.')
 if tree=='fr':
  r('EN GÉOMÉTRIE ALGÉBRIQUES','EN GÉOMÉTRIE ALGÉBRIQUE','title agreement',kind='misprint of the original',why='The scan has the final S, but the adjective qualifies singular géométrie. The corrected layer removes that grammatical misprint.')
 r(r'\fsection{A}{Foncteurs représentables et pro-représentables}',r'\fsection{\normalfont A}{\normalfont\uline{Foncteurs représentables et pro-représentables}.}','section heading',why='Ordinary roman letters, underlined title and final period.')
 r(r'\subsection*{1. Foncteurs représentables}',r'\subsection*{\normalfont 1. \uline{Foncteurs représentables}.}','subsection heading',why='Ordinary roman heading with an underline and period.')
 r(r'(\operatorname{Ens}),'+ '\n'+r'\]',r'(\operatorname{Ens})'+'\n'+r'\]','first display punctuation',why='The printed display has no terminal comma.')
 r(r'h_X(Y)=\operatorname{Hom}(Y,X).',r'h_X(Y)=\operatorname{Hom}(Y,X)','second display punctuation',why='The printed display has no terminal period.')
 r('i.e. on a défini un foncteur covariant\ncanonique','i. e. on a défini un \\uline{foncteur covariant canonique}','canonical functor',why='Spaced abbreviation and selective underline.')
 r(r'\operatorname{Hom}\bigl(\mathcal C^o,(\operatorname{Ens})\bigr)',r'\operatorname{Hom}(\mathcal C^o,(\operatorname{Ens}))','functor-category parentheses',why='Ordinary-size printed parentheses.')
 r(r'\result{PROPOSITION}{1.1}',r'\result{PROPOSITION}{1, 1}','proposition number',why='The printed number uses a comma between its two components.')
 r(r'\emph{pleinement fidèle}',r'\uline{pleinement fidèle}','proposition emphasis',why='Printed underline, not italics.')
 r('est bijective.','est \\uline{bijective}.','proposition conclusion',why='Printed underline.')
 r('est déterminé à un isomorphisme unique près.','est \\uline{déterminé à un isomorphisme unique près}.','representing-object uniqueness',why='Printed underline.')
 r(r'\emph{représentable}',r'\uline{représentable}','defined term',why='Printed underline.')
 r('définit une équivalence\nde','définit une \\uline{équivalence}\nde','categorical equivalence',why='Printed selective underline.')
 r("notion de « solution\nd'un Problème Universel »",r"\uline{notion de \fquote{solution d'un Problème Universel}}",'universal problem',why='The entire phrase beginning notion is underlined, with ordinary double quotes.')
 s,_,_=page_text(rel,369)
 r(r'\mathcal C^o',r'\mathcal C^0','four opposite-category exponents',count=s.count(r'\mathcal C^o'),why='The printed raised sign has the tall numeral-zero form; no op notation is substituted.')
 s,_,_=page_text(rel,369)
 r(r'\mathcal C',r'\text{\uwave{C}}','category identifiers throughout the page',count=s.count(r'\mathcal C'),why='The category letter is ordinary C with a wavy underline, not script C.')
 upright_page(rel,layer,'195-369')
event('195-1.1','targeted proof check','For a natural transformation alpha:h_X to h_X-prime, put f=alpha_X(id_X). Naturality for u:Y to X gives alpha_Y(u)=f composed with u. Conversely composition with any f defines a natural transformation, and evaluation at id_X recovers f. These operations are inverse and preserve composition, proving full faithfulness. A chosen isomorphism h_X to F and another h_X-prime to F determine a unique compatible isomorphism X to X-prime. The uniqueness phrase is read with these representing identifications, not as a denial of automorphisms of the underlying object. The equivalence with the full subcategory of representables follows by essential surjectivity from its definition.','195, p. 369, Proposition 1, 1 and following paragraph')
record_page('195',369,r'''Compared sources/fr_printed/fr/195.tex and sources/fr/fr/195.tex entry lines 3–56 with scan leaf 2 at 400 dpi, full page and all three enlarged bands. Read the headings, all category symbols and raised opposite-category signs, each h subscript and Hom argument, every arrow, Proposition 1, 1 and the final universal-property paragraph.

Restored the baseline e, right-aligned date, heavier sans-serif title and author lettering, roman underlined headings with their periods, selective prose underlines, double quotes, spaced abbreviation, display punctuation, comma in the proposition number, upright variables and wavy-underlined C. The opposite-category exponent has the printed numeral-zero form. Corrected French removes the erroneous final S in ALGÉBRIQUES in the title; printed French retains it.

Checked Proposition 1, 1 by evaluation of a natural transformation at the identity and the converse composition construction. The uniqueness statement is valid with the chosen representing identifications, as usual; no stronger assertion about absence of automorphisms was inserted. The definition of representability and the resulting equivalence were checked with the same construction.''')
rec=read('CHECK_RECORD.md')
rec=rec.replace('| Descent base category and fibred category |', '| Opposite category | `\\text{\\uwave{C}}^0` | Raised numeral-zero form on 195-369; retain the local printed sign instead of normalizing to op |\n| Descent base category and fibred category |')
rec=rec.replace('Ordinary wavy-underlined C and script F in 190-300;', 'Ordinary wavy-underlined C and script F in 190-300; wavy C continues in 195-369;')
pos=rec.index('\n## Page records') if '\n## Page records' in rec else -1
addition='\n- 195-369, title: corrected ALGÉBRIQUES to singular ALGÉBRIQUE to agree with géométrie; the printed layer retains the final S.\n'
if pos<0: raise ValueError('Page-record heading not found')
rec=rec[:pos]+addition+rec[pos:]
write('CHECK_RECORD.md',rec)
from update_record_counts import update
update()
