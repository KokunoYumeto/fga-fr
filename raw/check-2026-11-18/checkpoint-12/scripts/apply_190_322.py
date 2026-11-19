from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='B.4',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-322',line,statement,'400-dpi full scan and three enlarged bands. '+why,kind,count=count)
 old='\\subsection*{4. Application à des critères de rationalité}\n\\addcontentsline{toc}{subsection}{4. Application à des critères de rationalité}\n\n'
 new='\\addcontentsline{toc}{subsection}{4. Application à des critères de rationalité}\n\\result{4. \\uline{Application à des critères de rationalité}}{} '
 r(old,new,'heading',kind='structure',why='The heading is roman, selectively underlined and run in with the opening sentence.')
 r('un faisceau inversible\n(i.e.','un \\uline{faisceau inversible}\n(i. e.','definition',why='Underlined term and spaced abbreviation.')
 r('façon imagée, section de\n$F$ au-dessus de $s$','façon imagée, \\uline{section de}\n$F$ \\uline{au-dessus de} $s$','marked-section terminology',why='Underlining excludes the letters.')
 old='si $F_1$ et $F_2$ sont\nisomorphes, il existe un isomorphisme et un seul de $F_1$ sur $F_2$ compatible\navec les sections en question'
 r(old,underline_prose(old),'uniqueness assertion',why='Prose underlined, mathematical identifiers excluded.')
 r('(i.e. transformant','(i. e. transformant','uniqueness explanation',why='Spaced abbreviation.')
 r('comme\néquivalents deux','comme\n\\uline{équivalents} deux','equivalence definition',why='Underlined defined word.')
 r('sur $X$ tels que tout','sur $X$ tel que tout','equivalence definition',why='The scan has singular tel. The nearby X permits a literal syntactic reading; no compulsory grammatical correction is asserted.')
 old="tout faisceau inversible $F$ sur $X$ est\néquivalent à un faisceau inversible $F_1$ muni d'une section marquée au-dessus\nde $s$"
 r(old,underline_prose(old),'normalization assertion',why='Selective prose underlining.')
 old='et $F_1$ est déterminé à un\nisomorphisme près'
 r(old,underline_prose(old),'normalization uniqueness',why='Selective prose underlining.')
 r('sur $X$ à une équivalence près','sur $X$ à une \\uline{équivalence} près','classification sentence',why='Only équivalence is underlined here.')
 r('de la base (en remplaçant','de la base, (en remplaçant','base-change sentence',why='Printed comma before the parenthesis.')
 s,_,_=page_text(rel,322)
 match=re.search(r'\\emph\{(Le pré-schéma .*?près\.)\}',s,re.S)
 if not match: raise ValueError('Missing theorem-like paragraph')
 r(match.group(0),underline_prose(match.group(1)),'rationality criterion',kind='reading',why='The printed assertion is roman with underlined prose, not italic; formulas remain outside the underlining.')
 r('rationnel sur $S$.)','\\uline{rationnel} sur $S$).','rationality terminology',why='Underlined word and period outside the parenthesis.')
 r('les critères de rationalité de Weil ou de Cartier.','les \\uline{critères de rationalité de} Weil \\uline{ou de} Cartier.','closing attribution',why='Underlined prose excludes the two names.')
 if tree=='fr_printed':
  r('section de $X$ au-dessus de $S$','section de $X$ au-dessus de $s$','base of section',why='The print uses lower-case s here; corrected French retains the scheme S.')
  r('que ces auteurs','que ses auteurs','last parenthesis',why='The printed possessive ses is retained in the printed layer.')
 else:
  r('une section du faisceau inversible $s^*(F)$','une section génératrice du faisceau inversible $s^*(F)$','definition of section above s',kind='misprint of the original',why='The immediately following existence and uniqueness claim is false for an arbitrary section: over a field, no automorphism takes zero to one and every scalar fixes zero. A generator (a trivialization) is necessary, and is precisely the canonical section of the normalized line bundle used next.')
 s,_,_=page_text(rel,322)
 r(r'\mathcal O',r'\text{\uwave{O}}','four structure sheaf identifiers',why='Ordinary O with wavy underline.',count=s.count(r'\mathcal O'))
 upright_page(rel,layer,'190-322')
with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 for line,old,new,why in [('base of section','au-dessus de $s$','au-dessus de $S$','The section s is a map from the base scheme S into X; lower-case s cannot name its base.'),('last parenthesis','que ses auteurs','que ces auteurs','The phrase points to the two authors just named, Weil and Cartier, so the demonstrative ces is required.')]:
  w.writerow(['sources/fr/fr/190.tex','French corrected','190-322',line,'B.4',old,new,'The enlarged scan shows the old reading. '+why,'misprint of the original','low'])
event('190-B3-example2-effectivity','carried as background without fault found','The opening sentence invokes theorem 3 for radicial descent and imposes no flatness, smoothness or finiteness on the object being descended. The representation calculation on 321 did not use such hypotheses on the module. The general scheme effectivity still depends on the background theorem.','190, p. 322, first two paragraphs')
event('190-B4-arbitrary-marked-sections','refuted, with the refined statement\'s id','Take X=S=Spec Q, s the identity and F1=F2=O. For marked sections zero and one there is no compatible isomorphism; for two zero sections there are many scalar automorphisms. The printed assertion therefore requires a generating section of s-star(F), not an arbitrary section. Refined statement id: 190-B4-rigidified-line-bundles. Correct the defining phrase by adding generatrice, leaving every later use governed by that definition.','190, p. 322, definition and first underlined uniqueness assertion')
event('190-B4-rigidified-line-bundles','targeted proof check','Let f:X to S satisfy O_S isom f-star(O_X). Then automorphisms of any invertible F are exactly global units of O_X, hence units of O_S. Two chosen generators of s-star(F) differ by a unique base unit, giving a unique compatible isomorphism whenever the line bundles are isomorphic. Normalize F by tensoring with f-star(s-star(F) inverse); its restriction along s has the canonical generator one. Locally equivalent normalized bundles have unique compatible local isomorphisms, which agree on overlaps and glue. Thus equivalence classes of unmarked bundles identify with isomorphism classes of these rigidified bundles. The suppressed pullback in the printed normalization formula is retained as notation, not classified as a misprint.','190, p. 322, normalization and classification assertions')
event('190-B4-flat-base-change','carried as background without fault found','Flat base change for the direct image of the structure sheaf is the input used here. The standard proof with finite affine covers and finite affine refinements of intersections applies when f is quasi-compact and quasi-separated: tensor by a flat algebra preserves the finite equalizer computing sections. This run has not established the opening assertion for completely arbitrary pre-schemes without those hypotheses. Preserve the statement and flag that scope for the notes; do not silently add a finiteness hypothesis.','190, p. 322, opening sentence of section 4')
event('190-B4-rationality-criterion','targeted proof check','Conditional on O_S isom f-star(O_X) persisting over the flat bases in question, normalize F-prime along the base-changed section. Equivalence of its two pullbacks then gives their unique rigidification-preserving isomorphism. On the triple product both composites preserve the rigidification, hence uniqueness gives the cocycle condition. Theorem 1 descends the invertible sheaf, and faithful flatness detects local rank one. Uniqueness of the rigidified descent gives uniqueness up to the stated equivalence. Necessity follows by pullback. This proof explicitly uses generating marked sections and the base-change input recorded separately.','190, p. 322, final underlined criterion')
record_page('190',322,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 1199–1247 with scan leaf 25 at 400 dpi, full page and all three enlarged bands. Read the completion of the Cartier example, section 4, all starred inverse images, subscripts and fiber products, and the rationality criterion through the page break.

Restored the run-in underlined heading, selective roman underlines throughout, wavy O identifiers, spaced abbreviations and printed punctuation. Restored singular tel in both layers; its nearby singular X allows the literal construction, so no grammatical modernization was retained. Printed French restores lower-case s as the erroneous base of the section and ses auteurs; corrected French retains S and ces, with explicit rows. Corrected French adds génératrice in the definition of a marked section: zero sections give immediate counterexamples to the next existence and uniqueness assertion.

Checked the normalization of an invertible sheaf along a section and the resulting uniqueness and classification. The descent criterion follows by the unique rigidification-preserving isomorphism, whose cocycle identity is automatic by uniqueness. This proof is conditional on the flat-base-change assertion at the start of the section. Its standard quasi-compact, quasi-separated scope is recorded, while the full arbitrary-pre-scheme scope has not been proved here and is reserved for the notes. The implicit pullback in F times s-star(F) inverse is left as printed notation.''')
from update_record_counts import update
update()
