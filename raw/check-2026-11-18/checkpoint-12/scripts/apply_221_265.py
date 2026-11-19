from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-265',line,'3.7 proof / 3.8 / Hilbert definition',
                'Scan leaf 18 at 400 dpi and all three enlarged bands: '+why,kind=kind,count=count)
    r('9.4.2, et','9.4.2 et','opening reference','No comma follows the section number.')
    r('(3.1), est','(3.1) est','proof conclusion','No closing comma follows (3.1).')
    r(r'Q=\operatorname{Quot}^P',r'Q=\underline{\operatorname{Quot}}^P','definition of Q','The scheme sign has a straight underline.')
    r(r'$\mathcal F_Q=\mathcal F\otimes',r'$F_Q=\mathcal F\otimes','definition of base-changed F','The left F is an ordinary capital, while the right sheaf F is script; preserve the printed font variation.')
    r(r'$\underline{\operatorname{Quot}}^P',r'$\mathop{\text{\uwave{Quot}}}\nolimits^P','represented functor','The functor sign has a wavy underline.')
    r(r'\operatorname{Grass}_{P(n)}',r'\underline{\operatorname{Grass}}_{P(n)}','Grassmannian','The scheme sign is straight-underlined.')
    r('i.e.','i. e.','very ample interpretation','The abbreviation is spaced.')
    r("faisceau\n\\[\n\\bigwedge^{P(n)}(f_Q)_*(\\mathcal G(n))\n\\]\nsur",
      r'faisceau $\mathop{\bigwedge}\limits^{P(n)}(f_Q)_*(\mathcal G(n))$ sur',
      'determinant sheaf','The exterior power is inline with its degree placed above the wedge, not a separate display.','structure')
    s,_,_=page_text(rel,265)
    m=re.search(r'(\\result\{PROPOSITION\}\{3\.8\} )(.*?)(?=\n\nOn peut)',s,re.S)
    new=underline_prose(m.group(2)).replace('(3.2)',r'\uline{(3.2)}')
    r(m.group(2),new,'Proposition 3.8','All statement prose, including the reference (3.2), is straight-underlined; mathematical symbols retain their explicit alphabets.')
    r(r'au cas où $\mathcal F$ est plat',r'au cas où $F$ est plat','proof of 3.8','The print uses an ordinary F in this sentence.')
    r(r'\operatorname{Quot}_{\mathcal O_X',r'\underline{\operatorname{Quot}}_{\mathcal O_X','Hilbert identity','The scheme Quot sign has a straight underline.')
    r(r'\operatorname{Quot}^P_{\mathcal O_X',r'\underline{\operatorname{Quot}}^P_{\mathcal O_X','Hilbert identity with P','The scheme Quot sign has a straight underline.')
    r(r'\operatorname{Hilb}_{X/S}',r'\underline{\operatorname{Hilb}}_{X/S}','three Hilbert scheme signs','The three plain scheme signs are straight-underlined.',count=3)
    r(r'\operatorname{Hilb}^P_{X/S}',r'\underline{\operatorname{Hilb}}^P_{X/S}','three Hilbert scheme signs with P','All three scheme signs with superscript P have straight underlines.',count=3)
    r(r"$\underline{\operatorname{Hilb}}_{X/S}(S')$, ensemble",
      r"$\mathop{\text{\uwave{Hilb}}}\nolimits_{X/S}(S')$ = ensemble",
      'Hilbert functor definition','The functor sign has a wavy underline and is followed by an equality sign, not a comma.')
    r("plats sur $S'$ ; et","plats sur $S$ ; et",'flat base in Hilbert definition','The scan prints S without a prime.')
    if tree=='fr':
        r("plats sur $S$ ; et","plats sur $S'$ ; et",'flat base in Hilbert definition','An S-prime-valued Hilbert point is a closed subscheme of X base-changed to S-prime which is flat over S-prime. Flatness only over S would not give this functor; restore the missing prime.','misprint of the original')
    r(r'\emph{préschéma de Hilbert}',r'\uline{préschéma de Hilbert}','Hilbert terminology','The term is straight-underlined, not italic.')
    r(r"\emph{préschéma de Hilbert d'indice $P$}",r"\uline{préschéma de Hilbert d'indice} $P$",'indexed Hilbert terminology','The prose is straight-underlined and P remains outside the underline.')
    upright_page(rel,layer,'221-265')
event('221-3.7','targeted proof check','Let j be the principal open generic fiber over the DVR and take K as the kernel of F -> j_*G_s. The image G is quasi-coherent because j is affine locally (inverting the uniformizer), and G restricts to G_s. It embeds in a module on which the uniformizer is invertible, hence is torsion-free over the DVR and therefore flat. Any base-flat quotient with that generic fiber injects into its localization, so its kernel is exactly this same contraction. This proves both existence and uniqueness under the stated quasi-coherence hypotheses.','221, p. 265, opening paragraph')
event('221-3.8','targeted consequence check','The constructed Grassmannian immersion for sufficiently large n identifies the universal direct image with the tautological locally free quotient of rank P(n). Its top exterior power pulls back the Plucker very ample invertible sheaf; the properness conclusion upgrades the immersion to a closed immersion. This checks the claimed consequence conditional on the previously recorded construction and its cited cohomology and boundedness inputs, without claiming to re-prove those inputs.','221, p. 265, Proposition 3.8 and proof')
event('221-Hilbert-definition','targeted definition check','A quotient of O_X-prime as an O_X-prime-module has an ideal kernel and therefore determines exactly one closed subscheme, with the quotient its structure sheaf. The Quot flatness condition is over the test base S-prime, so the printed flatness over S is a dropped-prime misprint. The fixed-polynomial decomposition is read using the locally constant Hilbert polynomial in flat projective families.','221, p. 265, Hilbert definition and displays')
event('221-Chow-comparison','carried as background without fault found','Read the beginning of the explanatory contrast between families of subschemes and cycles; its sentence continues on the next page.','221, p. 265, final paragraph')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-265')
record_page('221',265,'Compared printed French entry lines 771-822 and corrected French entry lines 772-823 with scan leaf 18 at 400 dpi, then read all three enlarged bands. Read the complete proof of 3.7, all of 3.8 and its explanation, the Hilbert scheme identities and functor definition, and the opening of the Chow comparison.\n\nRestored the two absent commas, the straight scheme underlines and wavy functor underlines, ordinary F in two printed occurrences, all proposition emphasis, inline exterior power with its upper degree, the equality sign in the Hilbert definition and the two underlined prose terms. Printed French retains flatness over S; corrected French repairs the omitted prime to S-prime. The DVR contraction proof was checked explicitly, and the Grassmannian/Plucker consequence and Hilbert ideal-kernel construction were checked with their dependencies stated.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
