from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'236-221',line,'0(a)',
                'Scan leaf 2 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    r(r'14\textsuperscript{e} année','14e année','seminar heading','The e is on the baseline.')
    r(r"\fsection{0}{Compléments à l'exposé précédent ([3], V)\textsuperscript{(1)}}",r"\fsection{\normalfont 0}{\normalfont\uwave{Compléments à l'exposé précédent} ([3], V) (\textsuperscript{1}).}",'section heading','Only the title words have a wavy underline; the reference is outside it. The footnote numeral alone is raised inside baseline parentheses, and a full stop follows.')
    r('Mumford','MUMFORD','two attributions','The surname is uppercase.',count=2)
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}','four scheme names','All four Pic names have straight scheme underlines.',count=4)
    for letter,n in [('R',3),('C',1),('Z',2),('P',1)]:
        r(r'\mathbf '+letter,r'\text{\uwave{'+letter+'}}','field, integer and projective-space signs','The ordinary letter has a wavy underline, rather than bold weight.',count=n)
    r('homogènes)\n\\[\nx^2+y^2=tz^2,\n\\]', 'homogènes) $x^2+y^2=tz^2$,','conic equation','The equation runs in the sentence.','structure')
    r(r"\widetilde S'",r'\widetilde S','two doubled-origin names','Both newly named copies are printed as S with a tilde and without a prime.',count=2)
    r("$S'$ en dédoublant",'$S$ en dédoublant','base of doubled-origin construction','The print has unprimed S here.')
    if tree=='fr':
        r('$S$ en dédoublant',"$S'$ en dédoublant",'base of doubled-origin construction','The preceding scheme is Pic of X prime over S prime, after extension from R[[t]] to C[[t]]. Its degree components have generic point over C((t)) and origins with residue C. They are constructed from S prime, not S=Spec R[[t]]. The newly defined name tilde S needs no prime and is retained.','misprint of the original')
    r(r'\longrightarrow',r'\to','four morphisms','All arrows are short.',count=4)
    upright_page(rel,layer,'236-221')
event('236-0a-conic','targeted proof check','Checked the stated family: its primitive homogeneous equation gives a t-torsion-free quotient over the DVR R[[t]], hence flatness; the generic conic is smooth and the geometric special fibre is two distinct lines, so the fibres are geometrically reduced. The special equation x squared plus y squared is irreducible over R. Adjoining i gives the finite étale cover C[[t]] and splits the two components. In a fixed total degree d, their multidegrees (a,d-a) are exchanged by conjugation; for odd d some origins are interchanged. Conditional on the stated doubled-origin description of the Picard scheme, two such origins cannot lie in an affine open: the two maps from Spec C[[t]] coincide generically and differ at the closed point, contrary to separatedness of an affine scheme. An effective descended scheme would have an affine neighborhood of the image point whose base change contains the entire orbit, a contradiction. This verifies the descent obstruction and the required base S prime; the full relative Picard-functor classification behind the doubled-origin model is retained as a background input.','236, p. 221, 0(a), example and descent obstruction')
event('236-0a-existence','carried as background without fault found','The reported existence theorem for projective separable morphisms with geometrically irreducible fibre components requires the refined quotient theorem attributed to Mumford. It is not reproved here. The possible existence of Pic tau without the component hypothesis is explicitly left open in the print and is preserved as such.','236, p. 221, 0(a), final sentences')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='236-221')
record_page('236',221,'Compared both French layers, entry lines 3-47, with scan leaf 2 at 400 dpi, the full page and three enlarged bands. Read the seminar and title block, section 0 heading and the complete paragraph 0(a), including all fields, subscripts, primes, exponents and references.\n\nRestored the baseline e, wavy title emphasis and exact footnote-call position, uppercase MUMFORD, four straight-underlined Picard schemes, wavy R/C/Z/P signs, inline conic equation, the two unprimed names tilde S, short arrows and upright variables. The printed base of the doubled-origin construction is S; the corrected layer changes that base alone to S prime, as required by the preceding complex extension. Checked the geometric fibres and the non-effective-descent obstruction conditional on the announced Picard model, and kept the general quotient-based existence result and Pic-tau possibility as background.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
