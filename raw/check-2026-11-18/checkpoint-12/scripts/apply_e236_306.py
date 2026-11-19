from audit_utils import *
from collections import Counter
import csv
dq=chr(96)*2
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/e236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'e236-306',line,'Finiteness supplement (viii)-(ix) and proof comments',
                'Scan leaf 5 at 400 dpi, full page, three enlarged bands and tight damaged-letter crops: '+why,kind=kind,count=count)
    r('i.e.','i. e.','two abbreviations','The two initials are spaced.',count=2)
    r("d'équivalence numérique",r"d'\uline{équivalence numérique}",'numerical equivalence','The two words have a straight underline.','typesetting')
    r('Matsusaka','MATSUSAKA','attribution','The surname is all capitals.')
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}','three Picard labels','All three have straight underlines.',count=3)
    r('est ouvert et fermé dans',r'est ouvert \uline{et fermé} dans','assertion (ix)','Only et fermé is underlined within this phrase.','typesetting')
    r(r'\longrightarrow',r'\to ','structural morphism in (ix)','The arrow is short.')
    r('notamment TDTE I','notamment '+r'\uwave{TDTE} I','descent reference','TDTE has a wavy underline.')
    r("D'autre part, Mumford", "D'autre part, MUMFORD",'proof comments','This occurrence of the surname is all capitals.')
    r('par Mumford aux','par MUMFORD aux','ampleness attribution','This occurrence is all capitals; the named critère de Mumford occurrences retain their mixed case.')
    r('de Nakai','de NAKAI','ampleness attribution','The surname is all capitals.')
    r('intervenir tous les','intervenir '+r'\uline{tous} les','coefficient criterion','The word tous has a straight underline.','typesetting')
    r(r'la propriété $(S_2)$ de Serre,',r'(la propriété $(S_2)$ de SERRE),','extra fibre condition','The phrase is parenthesized, and SERRE is all capitals.')
    r(r'\geq2',r'\geqslant2','depth condition','The equality stroke is oblique.')
    r("« critères d'équivalence »",dq+"critères d'équivalence''",'equivalence criterion','Ordinary double quotation marks are printed.')
    r('dans SGA 1962','dans '+r'\uwave{SGA} 1962','seminar reference','SGA has a wavy underline.')
    upright_page(rel,layer,'e236-306')
event('e236-viii-e-continuation','used and rechecked in this run','Read the printed deduction e -> a: the Hilbert polynomials of all tensor powers agree, so criterion (iii) bounds the cyclic family. This matches the conditional argument recorded on p. 305. The opening parenthesis identifies b for F=L^m(n); taking all integers m makes the successive equalities equivalent, by telescoping, to equality with O(n). No exponent or additional tensor factor is missing.','Erratum 236, p. 306, opening paragraph after (viii)(e)')
event('e236-ix','targeted proof check','Checked the finite-condition step in deriving an open-and-closed tau locus from (viii)(e), conditional on Euler-polynomial theory and local universal line bundles. On each fixed relative-dimension piece of the projective flat family, the difference chi(L^m(n))-chi(O(n)) is a polynomial in m,n of uniformly bounded degree. Its vanishing for every integer pair is equivalent to vanishing on a finite interpolation grid. Each grid value is locally constant in a flat proper family, so their common zero set is open and closed. The construction is invariant under twisting L from the base and descends from local Picard charts. This avoids an unjustified claim that an infinite intersection of open subsets is open.','Erratum 236, p. 306, (ix)')
event('e236-proof-i-iv','carried as background without fault found','Read the proof sketch linking (i) to nonflat descent (TDTE I, p. 9) and (iv) to finite radicial surjections, specifically Frobenius. The relative Frobenius, rather than an arbitrary absolute Frobenius of a non-F-finite base, is the appropriate finite morphism for a relative finite-type scheme. The full descent-boundedness argument and the treatment of all nonzero integers are not supplied and remain background.','Erratum 236, p. 306, proof comments on (i) and (iv)')
event('e236-proof-ii-iii','carried as background without fault found','Read the sketch: first use a Mumford criterion bounding all Hilbert coefficients under an S_2 restriction, then reduce (ii) to flat geometrically integral normal fibres and apply SGA 1962, XII, equivalence criteria using depth at least two at closed points. Finally remove normality and strengthen to the two-coefficient criterion (iii). The normality-to-S_2 and dimension/depth implications are compatible with the stated fibre dimensions; the reduction, formal equivalence theorem and numerical strengthening require full proofs not given here. The attribution to Nakai and the historical status of the restriction are retained as reports.','Erratum 236, p. 306, final proof comments on (ii)-(iii)')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='e236-306')
record_page('e236',306,'Compared sources/fr_printed/fr/e236.tex and sources/fr/fr/e236.tex, entry lines 141-189, with scan leaf 5 at 400 dpi, full page, three enlarged bands and tight crops of condition and on. Retained these two words after examining damaged strokes; no lexical misprint is inferred from the ink defect. Read the continuation of (viii), assertion (ix) and all proof comments. Restored spaced i. e., numerical-equivalence and et fermé underlines, three straight-underlined Pic labels, short arrow, wavy TDTE/SGA, selected uppercase surnames, underlined tous, parentheses around the S_2 clause, ordinary quotes and the oblique depth inequality. Both French layers agree. Rechecked the finite interpolation argument for (ix), while retaining the descent, boundedness and formal-equivalence inputs as background.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
