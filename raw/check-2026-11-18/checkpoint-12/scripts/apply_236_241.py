from audit_utils import *
from collections import Counter
import csv
dq=chr(96)*2
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'236-241',line,'3.8-3.10; section 4',
                'Scan leaf 22 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    r('Serre ([8]','SERRE ([8]','mixed characteristic example','The name is in capitals.')
    for phrase in ['$R^1f_*(\\mathcal O_X)$\nlocalement libre','polynômes de\nHilbert','une conique dégénérant en\ndeux droites']:
        r('« '+phrase+' »',dq+phrase+"''",'quotation marks','The print has ordinary double quotation marks.')
    r('Sous les conditions de (3.5),\n','Sous les conditions de (3.5)\n',
      'corollary 3.8','There is no comma after the reference.')
    r(r'\result{REMARQUE}{3.10}',r'\noindent\uline{Remarque} 3.10. -',
      'remark heading','Mixed-case Remarque is straight-underlined.')
    r(r'si $\operatorname{Pic}_{X/S}^\tau$ est propre sur $S$, que',
      r'si $\operatorname{Pic}_{X/S}$ est aussi \uline{propre} sur $S$, que',
      '3.10 first properness assumption','The first Picard name has no tau; aussi is printed and propre is underlined. The stronger full-Picard properness hypothesis is mathematically valid and retained in both layers.')
    r('(par exemple si $f:X\\longrightarrow S$ est simple et projectif)',
      '(par exemple $f:X\\to S$ simple et projectif)',
      '3.10 projective example','Neither si nor est is printed in this parenthesis, and the arrow is short.')
    r('Néron--Severi','Néron-Severi','two group names','The joining dash is short.',count=2)
    r('de\n\\[\n\\operatorname{Pic}_{X_s/k(s)}^\\tau/\n\\operatorname{Pic}_{X_s/k(s)}^{\\circ\\circ}=T_{X_s/k(s)}\n\\]\nreste',
      'de $\\operatorname{Pic}_{X_s/k(s)}/\\operatorname{Pic}_{X_s/k(s)}^{\\circ\\circ}=T_{X_s/k(s)}$ reste',
      '3.10 quotient','The formula is inline and the numerator has no printed tau.','structure')
    r(r'si $\operatorname{Pic}_{X/S}^\tau$ est propre sur $S$ (par exemple',
      r'si $\operatorname{Pic}_{X/S}$ est propre sur $S$ (par exemple',
      '3.10 second properness assumption','This Picard name has no tau in the print.')
    r(r'$\operatorname{Pic}_{X/S}^\tau$ est plat sur $S$',
      r'$\operatorname{Pic}_{X/S}$ est \uline{plat} sur $S$',
      '3.10 flatness clause','No tau is printed; plat is underlined. The literal verb is est.')
    r(r'\fsection{4}{Le théorème de finitude pour le schéma de Picard}',
      r'\fsection{4}{\uwave{Le théorème de finitude pour le schéma de Picard}.}',
      'section 4 heading','The title has a wavy underline and a final period.')
    r(r'f:X\longrightarrow S',r'f:X\to S','section 4 morphism','The arrow is short.')
    r(r'\mathbf Q[t]',r'\text{\uwave{Q}}[t]','Hilbert polynomial coefficients','The coefficient-field Q is ordinary with a wavy underline, not bold.')
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}','all Picard names',
      'Each Picard name on this page has a straight underline.',count=13)
    if tree=='fr':
        r(r'si $\underline{\operatorname{Pic}}_{X/S}$ est propre sur $S$ (par exemple',
          r'si $\underline{\operatorname{Pic}}_{X/S}^\tau$ est propre sur $S$ (par exemple',
          '3.10 second properness assumption','This is the torsion subgroup discussed after 3.9. The asserted projective smooth example is false for the whole Picard scheme: Pic(P1) is the infinite discrete degree group Z and is not proper. Pic(P1)^tau is trivial and proper. Supply tau here to make the explicit example and the subsequent finite torsion quotient agree.','misprint of the original')
        r(r'$\underline{\operatorname{Pic}}_{X_s/k(s)}/\underline{\operatorname{Pic}}_{X_s/k(s)}^{\circ\circ}=T_{X_s/k(s)}$',
          r'$\underline{\operatorname{Pic}}_{X_s/k(s)}^\tau/\underline{\operatorname{Pic}}_{X_s/k(s)}^{\circ\circ}=T_{X_s/k(s)}$',
          '3.10 finite torsion quotient','The finite group whose field rank is discussed is the torsion quotient. For P1 the unqualified quotient is Z, with no finite field rank, whereas the torsion quotient is the trivial finite scheme. Supply the omitted tau in the numerator.','misprint of the original')
        r(r'$\underline{\operatorname{Pic}}_{X/S}$ est \uline{plat} sur $S$',
          r'$\underline{\operatorname{Pic}}_{X/S}^\tau$ soit \uline{plat} sur $S$',
          '3.10 flatness clause','The clause concerns the proper torsion subgroup and its finite quotient by the abelian subscheme; a finite locally free torsion quotient only controls that subgroup, not the other Neron-Severi components of the whole Picard scheme. Supply the omitted tau consistently with the immediately preceding finite quotient. The subordinate phrase il revient au même que requires soit.','misprint of the original')
    upright_page(rel,layer,'236-241')
event('236-3.8-remark-end','carried as background without fault found',
      'Read the mixed-characteristic counterexample attributed to Serre, reference [8] p. 50, and the historical uncertainty in equal characteristic. The cited example is not reconstructed here and the statement about known counterexamples is retained as the author\'s historical assessment.',
      '236, p. 241, first paragraph')
event('236-3.8-corollary','targeted proof check',
      'Conditional on 3.5 and 2.10(i), smoothness near each fibre identity extends by translations to the prime-to-characteristic torsion components, giving the stated sigma locus over U. The duplicated number 3.8, already used for the preceding remark, is the print\'s numbering and is retained.',
      '236, p. 241, corollary 3.8')
event('236-3.9','targeted proof check',
      'In characteristic zero the geometric Picard groups are smooth by the Cartier input cited in 2.10(iii), so 3.5 applies locally at every base point. All torsion orders are prime to the residue characteristic exponent 1; thus sigma equals tau, and corollary 3.8 gives the stated smoothness. The Cartier theorem itself remains background.',
      '236, p. 241, corollary 3.9')
event('236-3.10-torsion','targeted proof check',
      'Conditional on properness of the torsion subgroup and 2.5, each kernel of multiplication by q^n is finite etale over S when q is invertible. Its rank is constant on a connected base. On a geometric fibre the size is q^(2gn) times the size of the q^n-torsion of the finite Neron-Severi torsion group, since q-multiplication on the abelian part is surjective. The ranks for all n determine g by their eventual growth and then determine the elementary divisors of the finite q-primary group. This checks the claimed constancy conditional on the geometric abelian/finite-quotient structure and etaleness inputs. The p-primary warning and proposed rank constancy are retained as warning and conjectural possibility.',
      '236, p. 241, remark 3.10')
event('236-3.10-omitted-tau','targeted proof check',
      'The first full-Picard properness assumption is stronger but valid, so its unprinted tau is withdrawn in both layers. Three later omitted taus have a different role: smooth projective P1 has Pic equal to the infinite discrete Z, disproving the second properness example for full Pic and the finite-rank quotient interpretation. Corrected French uses Pic^tau in that example, its finite fibre quotient, and the matching flatness condition. The asserted equivalence over reduced bases and reduction to discrete valuation rings are not independently established here.',
      '236, p. 241, remark 3.10, second properness assumption, quotient and flatness clause')
event('236-4-conic-example','targeted proof check',
      'For the projective flat conic xy=t z^2, the special fibre is two projective lines meeting in one node. Line bundles of multidegree (a,d-a) exist for every integer a and have the same Hilbert polynomial 2n+d+1 for the plane polarization. Their Picard identity component is trivial, so they give infinitely many discrete special-fibre points with that fixed polynomial. Hence the corresponding fixed-polynomial locus is not quasi-compact and cannot be of finite type over the base. The general Hilbert-polynomial open-and-closed decomposition uses the already stated flat-family invariance.',
      '236, p. 241, opening of section 4')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='236-241')
record_page('236',241,'Compared sources/fr_printed/fr/236.tex and sources/fr/fr/236.tex, entry lines 924-970, with scan leaf 22 at 400 dpi, the full page and three enlarged bands. Read both numbered corollaries, remark 3.10 and the opening of section 4.\n\nRestored ordinary quotations, capitals, punctuation, the mixed-case remark, thirteen straight Picard names, the omitted aussi, short arrows and name hyphens, inline quotient, wavy coefficient-field Q and section title, and the emphasis on propre and plat. Restored four missing-in-print tau superscripts before adjudication: the first remains absent in corrected French because its stronger hypothesis is valid; three later ones are justified in the torsion example, finite quotient and corresponding flatness condition. Corrected French also repairs est to soit in the subordinate clause. Kept duplicate number 3.8. Checked the two corollary deductions, the prime-to-characteristic torsion rank argument and the explicit conic multidegree counterexample, with the deeper extension/flatness claims identified as background.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
