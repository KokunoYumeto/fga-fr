from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/212.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'212-99',line,'Introduction','400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 r(r'13\textsuperscript{e} année','13e année','seminar year',why='The e is on the baseline.')
 r(r'\\Février 1961',r'\\\hfill Février 1961','seminar date',why='The date is right aligned on its own line.')
 r('III. PRÉSCHÉMAS QUOTIENTS','III : PRÉSCHEMAS QUOTIENTS','title punctuation and accents',why='The subtitle has a colon and only the first capital E is accented in PRÉSCHEMAS.')
 r(r'\subsection*{Introduction}',r'\subsection*{\textnormal{\uline{Introduction}.}}','introduction heading',why='Roman text with an underline and a final period outside the underline.')
 r(r"\emph{l'effectivité d'une donnée de descente}",r"\uline{l'effectivité d'une donnée de descente}",'effectivity emphasis',why='The phrase is underlined, not italic.')
 r(r'\longrightarrow',r'\to','faithfully flat base arrow',why='The printed arrow is ordinary length.')
 r('donnée de descente;','donnée de descente ;','descent sentence punctuation spacing',why='The printed semicolon is separated from the preceding word.')
 r(r'\emph{schéma de Picard}',r'\uline{schéma de Picard}','Picard emphasis',why='The phrase is underlined.')
 r('simple: ce sont','simple : ce sont','construction sentence colon',why='The printed colon is separated.')
 old=r'''\emph{schémas de modules sur les entiers pour les courbes de genre arbitraire,
les variétés abéliennes polarisées}'''
 new=r'''\uline{schémas de modules sur les entiers pour les courbes de genre arbitraire},
les \uline{variétés abéliennes polarisées}'''
 r(old,new,'last paragraph selective emphasis',why='The first underline ends after arbitraire; comma and les are outside it; a new underline begins at variétés and continues through polarisées.')
 upright_page(rel,layer,'212-99')
event('212-intro-covariance','targeted proof check','For a fixed relation R with two maps to X, the functor sending Y to the set of maps X to Y equalizing the two R maps is covariant in Y. A representing object in the covariant Hom(Q,Y) convention is precisely a categorical coequalizer Q. This checks the opening variance distinction from the contravariant point functors of the preceding exposés.','212, p. 99, opening sentences')
event('212-intro-effective-descent','targeted proof check','A descent datum on X over T for an fpqc map T to S gives the relation R=X times_S T with the second map to X supplied by the datum. The cocycle identity gives composition, and the two projections are fpqc by base change. If X descends to Q over S, this relation is X times_Q X and X to Q is its fpqc sheaf quotient. Conversely, a representable fpqc sheaf quotient with the stated cartesian effectiveness property recovers X as Q times_S T after the fpqc check over T. Thus the advertised equivalence holds with the reasonable quotient properties explicitly reserved by the text; existence of an arbitrary categorical quotient alone would not suffice.','212, p. 99, effectivity of descent paragraph')
event('212-intro-Picard-and-moduli','carried as background without fault found','The introduction announces constructions of Picard schemes from parameter schemes and flat equivalence relations under suitable projectivity hypotheses, and identifies a later quotient question as an obstacle to moduli of curves and polarized abelian varieties over the integers. The preceding definitions in 195 C.2 and C.3 match the Hom and Picard references. These are programmatic statements here; exact construction hypotheses and later developments remain to be checked at their own statements and in the notes. No unconditional fine-moduli claim is inferred.','212, p. 99, Picard and final moduli paragraphs')
record_page('212',99,r'''Compared sources/fr_printed/fr/212.tex and sources/fr/fr/212.tex entry lines 3–42 with scan leaf 2 at 400 dpi, full page and all three enlarged bands. Read the seminar date and number, all title accents, every internal reference, the ordinary base arrow, the straight-underlined Hom with its S subscript, and the exact extent of the prose underlines.

Both layers restore the baseline e and right-aligned date, colon in the subtitle, the locally unaccented second E of PRÉSCHEMAS, roman underlined Introduction with its period, the ordinary arrow, punctuation spacing and selective prose underlines. The printed simple and the straight Hom underline are retained. No mathematical or semantic difference is introduced between the two French layers on this page.

Checked the covariance of the quotient universal-property functor and the effectivity/quotient equivalence with its reserved fpqc/cartesian properties. The Picard construction and moduli discussion are recorded as conditional announcements, with their preceding internal reference targets identified; no later proof or stronger fine-moduli claim is attributed to this introductory page.''')
from update_record_counts import update
update()
