from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-305',line,statement,'400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 r('i.e.','i. e.','three explanatory abbreviations','2.2; 2(b)',why='The print spaces the abbreviation.',count=3)
 r('En tout cas','En tous cas','opening paragraph','2.2',why='The print has tous.')
 r('le soin de développer','de développer','opening paragraph','2.2',why='No le soin occurs in the scan.')
 for term in ['monomorphisme strict','épimorphisme universel','épimorphisme strict universel','morphisme de descente','morphisme de descente strict']:
  r('\\emph{'+term+'}','\\uline{'+term+'}','defining term '+term,'2.2–2.4',why='The terms are underlined.')
 r('$\\mathcal F$-descente et la notion', '$\\mathcal F$-descente, et la notion','transition paragraph','2.3',why='Comma before et.')
 r('si, pour tout $T$','si pour tout $T$','Definition 2.3 condition','2.3',why='No comma after si.')
 r('les quatre notions','les 4 notions','paragraph after 2.3','2.3',why='A numeral 4 is printed.')
 r('préschéma','pré-schéma','prescheme spelling','2.3; 2(b)',why='The print retains the hyphen, including the overprinted paragraph.',count=5)
 if tree=='fr_printed':
  r('pré-schémas, ou la catégorie','pré-schémas, où la catégorie','paragraph after 2.3','2.3',why='The scan visibly accents où; the intended disjunction is retained unaccented only in corrected French.')
 r('(cf. définition 1.7),','(cf. définition 1.7.),','Definition 2.4 reference','2.4',why='A period appears inside the parenthesis.')
 r(r'\mathcal C',r'\text{\uwave{C}}','eight category-letter occurrences','2.4; 2.1; 2(b)',why='Ordinary C with a wavy underline.',count=8)
 r('morphismes de descente et épimorphismes','morphismes de descente, et épimorphismes','Proposition 2.1 conclusion','2.1',why='Comma follows descente; the body is not underlined.')
 r("deux pré-schémas finis sur $S$","deux pré-schémas \\uline{finis} sur $S$",'start of examples','2(b)',why='Only finis is underlined.')
 r(r'\mathcal A',r'\text{\uwave{A}}','four algebra-letter occurrences','2(b)',why='Ordinary A with a wavy underline.',count=4)
 r('qui, en tant que faisceaux de modules, sont','qui en tant que faisceaux de modules sont','finite algebra description','2(b)',why='Neither comma appears in the print.')
 r('Cohen--Seidenberg),','Cohen-Seidenberg)','finite-morphism theorem reference','2(b)',why='Short hyphen and no following comma.')
 r(r'\overset{\beta_1}{\underset{\beta_2}{\rightrightarrows}}',r'\overset{\beta_1}{\underset{\beta_2}{\leftleftarrows}}','final coequalizer diagram','2(b)',why='Both beta arrows point from S-double-prime to S-prime.')
 upright_page(rel,layer,'190-305')
with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 csv.writer(f,delimiter='\t').writerow(['sources/fr/fr/190.tex','French corrected','190-305','paragraph after 2.3','2.3','pré-schémas, où la catégorie','pré-schémas, ou la catégorie','Confirmed the supplied unaccented disjunction against the visible accented où in the middle crop. The sentence lists the category of preschemes or the category over a fixed base; a relative adverb cannot connect these noun phrases.','misprint of the original','low'])
event('190-2.2','targeted proof check','Completed the kernel-pair criterion: equality on the two projections is equivalent to equality on every pair equalized by alpha. Any coequalizer is therefore strict. If a strict epimorphism is also monic, every equalized pair is equal, so the identity of its source factors through alpha; epimorphy gives the other inverse identity.','190, pp. 304–305, Definition 2.2 and its continuation')
event('190-2.3','carried as background without fault found','Read the two universal definitions. In sets, sheaves of sets and abelian categories the usual surjectivity/local-surjectivity/cokernel descriptions supply the asserted coincidence. The claim that all four notions differ even for finite preschemes is awaiting the examples that continue on subsequent pages; no proof is certified here.','190, p. 305, Definition 2.3 and following paragraph')
event('190-2.1-proposition','targeted proof check','Verified both implications assuming the finite products and fiber products stated. For universally strict alpha, a compatible map X-prime to Y-prime gives X-prime to Y constant on the kernel pair of X-prime to X, hence a unique map X to Y; epimorphy verifies it lies over S. Conversely, for any T over S and u:T times_S S-prime to Z equalizing its kernel pair, view u as an S-prime map to (S times Z) times_S S-prime. Descent full faithfulness produces the unique map T to S times Z and thus T to Z. This makes each base change a coequalizer of its kernel pair, hence strict.','190, p. 305, Proposition 2.1')
event('190-2b-finite-exactness','carried as background without fault found','Read the finite-scheme setup and checked variance: beta_i:S-double-prime to S-prime induces algebra maps A-prime to A-double-prime. The coequalizer/equalizer assertion continues on p. 306, and is not yet counted as a completed proof. The closedness input is the integral-morphism closed-map theorem.','190, p. 305, beginning of examples')
record_page('190',305,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 332–383 with scan leaf 8 at 400 dpi, the full page and all three enlarged bands. Read the continuation of 2.2, Definitions 2.3–2.4, Proposition 2.1, the finite-scheme setup and all symbols in its final diagram. The next marker follows the unfinished phrase diagramme de faisceaux, as printed.

Restored tous, the absence of le soin, numeral 4, spaced i. e., hyphenated pré-schéma, the printed commas and reference period, underlined defining terms and finis, ordinary wavy-underlined C and A, the short Cohen-Seidenberg hyphen, and the leftward beta arrows. The partly overprinted paragraph remains legible; its visible accented où is restored in printed French, while the grammatical disjunction ou is confirmed and explicitly recorded in corrected French. Proposition 2.1 has no underlined body.

Completed the strict-epimorphism/coequalizer argument and the strict-epi-plus-mono inverse argument. Reconstructed both implications of Proposition 2.1 using Hom descent and kernel-pair coequalizers after arbitrary base change, with the finite product S times Z used in the converse. The four-notions distinction and the finite-scheme equalizer test await their continuation; they are carried as background here without a claim of proof.''')
from update_record_counts import update
update()
