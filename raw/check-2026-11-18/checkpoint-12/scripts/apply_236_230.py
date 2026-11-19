from audit_utils import *
from collections import Counter
import csv
dq=chr(96)*2
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'236-230',line,'1.9, 1.10, 1.11',
                'Scan leaf 11 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    r('« groupe additif »',dq+"groupe additif''",'opening parenthesis','The print uses ordinary double quotation marks.')
    r('« droites »',dq+"droites''",'additive example','The word droites has ordinary double quotation marks.')
    r('« schéma en groupes constant »',dq+"schéma en groupes constant''",'constant group','The print uses ordinary double quotation marks.')
    r(r'\mathbf G_a',r'\text{\uwave{G}}_a','opening functor','G has a wavy underline with the a outside.')
    r(r'\mathbf G_m',r'\text{\uwave{G}}_m','multiplicative functor','G has a wavy underline with the m outside.')
    r(r"S'\longmapsto\Gamma(S',\mathcal O_{S'})",r"S'\rightsquigarrow\Gamma(S',O_{S'})",'opening assignment','The inline assignment has a wavy arrow and an ordinary upright O, not a script O.')
    r('tant que $S$-schéma,\n\\[\nG=\\operatorname{Spec}V[x]/(x^p-tx)\n\\]\nest',
      'tant que $S$-schéma, $G=\\operatorname{Spec}V[x]/(x^p-tx)$ est',
      'first coordinate algebra','The coordinate algebra is inline, with no added grouping parentheses around the algebra.','structure')
    r("Dans le cas d'inégale caractéristique, de\ncaractéristique résiduelle",
      "Dans le cas d'inégale caractéristique, caractéristique résiduelle",
      'mixed characteristic','There is no de before the second caractéristique.')
    r(r'H=\boldsymbol\mu_p$,',r'H=\mu_p$','multiplicative kernel','The Greek mu is not bold, and no comma follows its subscript p.')
    r('donc\n\\[\nH=\\operatorname{Spec}V[x]/(x^p-1) ;\n\\]\nc\'est',
      "donc $H=\\operatorname{Spec}V[x]/(x^p-1)$, c'est",
      'second coordinate algebra','This coordinate algebra is inline and is followed by a comma, not a semicolon.','structure')
    r(r'\mathbf Z',r'\text{\uwave{Z}}','seven cyclic-group expressions','Every Z in these seven expressions has a wavy underline.',count=14)
    r(r'sur $S$, donc fermé',r'sur $S$ donc fermé','corollary 1.10','No comma is printed between S and donc.')
    r(r'G^\tau\longrightarrow S',r'G^\tau\to S','corollary 1.10 final map','The structure arrow is short.')
    r(r'de $S$, telle que',r'de $S$, telles que','proposition 1.11','The printed agreement is plural telles.')
    r(r'au-dessus de $S$ soit',r'au-dessus de $S$, soit','proposition 1.11','A comma is printed after S.')
    if tree=='fr':
        r('est réunion de $p$', 'est réunion, après une extension finie ramifiée de $V$, de $p$',
          'additive example, branch description',
          'The p-branch description requires splitting the generic fibre: for V=k[[t]] and p>2, x^p-tx=x(x^(p-1)-t), with the second factor Eisenstein, has only two irreducible components. Adjoining u with u^(p-1)=t gives the p factors x-au for a in F_p. The qualifier makes the following split cyclic-group description apply after that extension.','misprint of the original')
        r("c'est encore la réunion de $p$ droites",
          "après une extension de $V$ contenant les racines $p$-ièmes de l'unité, c'est encore la réunion de $p$ droites",
          'multiplicative example, branch description',
          'The p sections and the generic constant cyclic group require p-th roots of unity in the fraction field. Over Z_p with p>2, x^p-1=(x-1)Phi_p(x), and Phi_p(y+1) is Eisenstein, giving two components before extension. After adjoining the roots it splits into p sections; the subsequent product description is then understood over this extended trait.','misprint of the original')
        r('telles que','telle que','proposition 1.11',
          'The antecedent is the singular une partie ouverte U; telle is the required singular agreement.','misprint of the original')
    upright_page(rel,layer,'236-230')
event('236-1.9-branches','refuted, with the refined statement\'s id',
      'Refined statement 236-1.9-split-branches. The unqualified p-branch descriptions fail already for p>2 over k[[t]] and Z_p respectively: the factorizations are x times the Eisenstein polynomial x^(p-1)-t, and (x-1) times Phi_p(x), with Phi_p(y+1) Eisenstein. Thus each has two irreducible components. The split generic group descriptions likewise require a splitting extension. Added the respective extensions only to corrected French.',
      '236, p. 230, remark 1.9 opening examples')
event('236-1.9-split-branches','independent re-proof',
      'In equal characteristic p, the finite ramified extension u^(p-1)=t splits x^p-tx as the product of x-au over a in F_p. In mixed characteristic, adjoining the p-th roots of unity splits x^p-1 into its p linear factors. Each resulting section specializes to the unique point of the connected special fibre. The identity-component locus is the unit section, not open because it contains the common special point but excludes other generic points. For mu_p times constant Z/p, rho is the unit section plus the special fibre and sigma is the unit section plus the generic fibre; the former is not open and the latter is not closed. These set-theoretic statements follow by computing the component groups in each characteristic.',
      '236, p. 230, remark 1.9')
event('236-1.10','targeted proof check',
      'In characteristic zero, prime-to-characteristic torsion is all torsion and the characteristic-primary subgroup is trivial, yielding tau=sigma and zero=rho. The assertions then follow from the corresponding parts of 1.1, 1.5 and 1.8; the added invertibility restriction in refined 1.5 is automatic here. This checks the deduction conditional on those component, openness and smoothness inputs, rather than independently reproving the inputs.',
      '236, p. 230, corollary 1.10')
event('236-1.11','carried as background without fault found',
      'Read the existence of an open U, the entire smooth (respectively flat) locus G prime as an open subgroup of G restricted to U, and the assertion about all sections over U. Only the singular agreement telle is corrected. The proof continues on p. 231 and is not yet counted as checked.',
      '236, p. 230, proposition 1.11')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='236-230')
record_page('236',230,'Compared sources/fr_printed/fr/236.tex and sources/fr/fr/236.tex, entry lines 419-469, with scan leaf 11 at 400 dpi, full page and three enlarged bands. Read the completion of 1.9, all of 1.10 and the statement of 1.11. Restored ordinary quotation marks, the wavy functor and integer letters, the plain O and mu, the wavy assignment, inline coordinate algebras and exact punctuation. Enlarged image confirms the closing parenthesis in (iv); no correction there.\n\nThe p-branch and split-group descriptions in 1.9 need splitting extensions. Explicit Eisenstein factorizations refute the unqualified readings; corrected French supplies the extensions while the printed layer keeps the original. The mixed-characteristic component-locus counterexamples are verified directly. Corollary 1.10 is checked as a deduction conditional on its preceding results. Proposition 1.11 continues on the next page; printed telles is retained only in the printed layer.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
