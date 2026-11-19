from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1,full=False):
  replace(rel,a,b,layer,'182-200',line,statement,'400-dpi scan with all three enlarged bands. '+why,kind,count=count,full=full)
 r('\\src{201}\n\\result{PROPOSITION}{1}',r'\result{PROPOSITION}{1}','page boundary','5','structure','The marker is too late: page 200 ends after the introductory sur X, before F étant supposé Y-plat.',full=True)
 r('sur $X$, $F$ étant supposé','sur $X$,\n\\src{201}\n$F$ étant supposé','last line','5','structure','Insert page 201 at the true printed boundary; the following flatness argument is reserved for that page.',full=True)
 txt,_,_=page_text(rel,200)
 for a,b,body in list(footnotes(txt)):
  r(txt[a:b],'','Theorem 6 editorial footnote','4-thm6','structure','The printed exposé has no footnote here. The later erratum must remain in its separate section and is not merged into either exposé layer.')
 r('séparé, $U$ est','quasi-projectif, $U$ est','Theorem 6 hypothesis','4-thm6',why='The scan says quasi-projectif. The valid original theorem is restored in both layers; a later strengthening is not a correction of a misprint.')
 r('dû à Chevalley','dû à CHEVALLEY','attribution after Corollary 1','4-thm5-cor1',why='The surname is uppercase.')
 r(r'\textit{a fortiori}',r'\uline{a fortiori}','paragraph after Theorem 6','4-thm6',why='The phrase is roman and underlined.')
 txt,_,_=page_text(rel,200)
 for quoted in dict.fromkeys(re.findall('« (.*?) »',txt,re.S)):
  old='« '+quoted+' »'
  r(old,r'\fquote{'+quoted+'}','quoted phrase','4',why='The print uses ordinary double quotes.',count=txt.count(old))
 txt,_,_=page_text(rel,200)
 r(r'\Osh','O','structure sheaves and local rings','4',why='Every O here is plain, not underlined.',count=txt.count(r'\Osh'))
 if tree=='fr_printed':
  r(r"f'_*(O_X)=O_{Y'}",r"f'(O_X)=O_{Y'}",'proof of Corollary 1','4-thm5-cor1',why='The scan omits the direct-image star. Corrected French retains it, as required by the defining equality in Theorem 5.')
 r(r'un isomorphisme $O_{y\prime}',r'un isomorphisme $O_{y\prime}','proof','4-thm5-cor1') if False else None
 r("un isomorphisme $O_{y'}", "un \\uline{isomorphisme} $O_{y'}",'proof of Corollary 1, local rings','4-thm5-cor1',why='Only the word isomorphisme is underlined in this sentence.')
 r(r'\widetilde f',r'\overline f','compactification paragraph','4-thm6',why='The accents over the extended morphisms are straight bars, not tildes.',count=2)
 r(r'\widetilde X',r'\overline X','compactification paragraph','4-thm6',why='The compactification X has a straight bar, not a tilde.')
 if tree=='fr_printed':
  r('particulier si $f$ est quasi-projectif','particulier si $\\overline f$ est quasi-projectif','compactification parenthesis','4-thm6',why='A short bar is visible over f in the scan. Corrected French retains the supplied unbarred f: the parenthesis supplies a condition for existence of its proper extension, which is then used in Theorem 6.')
 txt,_,_=page_text(rel,200);a=txt.index("l'ensemble des composantes");b=txt.index('\n\n',a);old=txt[a:b]
 r(old,underline_prose(old),'Theorem 5 continuation','4-thm5',why='The continuation is underlined, including the second i.e.; the opening i.e. lies outside the underline.')
 for marker,sid in [(r'\result{COROLLAIRE}{1} ','4-thm5-cor1'),(r'\result{COROLLAIRE}{2} ','4-thm5-cor2'),(r'\result{THÉORÈME}{6 (\fquote{Main Theorem} de Zariski)} ','4-thm6')]:
  txt,_,_=page_text(rel,200);a=txt.index(marker)+len(marker);b=txt.index('\n\n',a);old=txt[a:b]
  parts=re.split(r'(\(où\s*\$[^$]*\$\))',old)
  new=''.join(x if i%2 else underline_prose(x) for i,x in enumerate(parts))
  r(old,new,'statement prose',sid,why='Restore the printed statement underlining, excluding mathematical letters and the parenthetical definition of y-prime.')
 r(r'''\fsection{5}{Application à l'étude cohomologique des morphismes propres et
plats}''',r'''\fsection{\normalfont5}{\normalfont\uline{Application à l'étude cohomologique des morphismes propres et
plats}.}''','section heading','5',why='The title is roman, underlined and ends with a period.')
 upright_page(rel,layer,'182-200')
event('182-4-thm5-cor1','targeted proof check','Checked the local argument: for a proper closed map with singleton fiber, inverse images of neighborhoods are cofinal among neighborhoods of that point; f-prime_*O_X=O_Y-prime then identifies the stalks. Finite presentation spreads the local inverse to neighborhoods. The printed equality in the proof drops the direct-image star; corrected French retains it.','182, p. 200, Corollary 1 and proof')
event('182-4-thm5-cor2','targeted proof check','If the proper map has finite fibers, every point is isolated in its fiber, so Corollary 1 makes f-prime an isomorphism and f the finite map g. Conversely a finite map is proper with finite fibers. This verifies the stated deduction under the preceding theorem.','182, p. 200, Corollary 2')
event('182-4-thm6','targeted proof check','The printed hypothesis is quasi-projectivity. Its projective closure supplies a proper extension, and the isolated-fiber open is an open subset of the finite Stein factor, as argued. The supplied replacement by separatedness is a later erratum, not an original misprint, so it and the inserted footnote are withdrawn from both exposé layers. The bar over f in the preceding parenthesis is restored only in printed French; its intended sufficient condition concerns f, which is the given morphism awaiting compactification.','182, p. 200, compactification paragraph and Theorem 6')
record_page('182',200,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 340–415 with scan leaf 9 at 400 dpi, full-page image and all enlarged bands. Read the end of Theorem 5, Corollaries 1–2 and their arguments, the compactification paragraph, Theorem 6, and the section-5 opening line. Moved the page-201 marker to before F étant supposé Y-plat, reserving the rest for the next scan.

Restored all statement and local-word underlining, uppercase CHEVALLEY, plain O, double quotes, straight completion/compactification bars and the section heading. The printed proof omits a direct-image star; corrected French retains it. The parenthesis prints barred f in the quasi-projective sufficient condition; corrected French retains unbarred f, with the contextual reason recorded for final recheck. Crucially, restored quasi-projectif in Theorem 6 in BOTH layers and removed the inserted footnote incorporating the 1962 erratum. The original theorem is valid as printed and the later strengthening belongs to the separate errata. The proper finite-fiber deduction and the quasi-projective compactification argument were checked.''')
from update_record_counts import update
update()
