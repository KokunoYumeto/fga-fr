from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/236.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'236-229',line,'1.7, 1.8, 1.9',
                'Scan leaf 10 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count)
    r('Cartier','CARTIER','corollary 1.7','The name is printed in capitals.')
    r('(en particulier plat)','(en particulier, plat)','corollary 1.7','The print includes a comma after particulier.')
    r('composante connexe, est','composante {\\addfontfeatures{LetterSpace=12}connexe}, est','flatness discussion','This occurrence of connexe is visibly letterspaced in the print.')
    r('donné dans [2], IV, paragraphe 5','donné dans [IV], paragraphe 5','flatness reference','The print puts only IV inside square brackets.')
    r(r'\result{REMARQUES}{1.9}',r'\result{\normalfont\uline{Remarques}}{1.9}','remark heading','Mixed-case Remarques alone has a straight underline.')
    r(r'\mathbf Z',r'\text{\uwave{Z}}','infinite-origin special fibre','The Z has a wavy underline.')
    r('en groupes fini et plat $G$ sur le','en groupes fini et plat, $G$, sur le','finite flat example','The print places commas before and after G.')
    r(r'\mathbf G_a',r'\text{\uwave{G}}_a','additive-group functors','Both G names have wavy underlines; the subscript a is outside.',count=2)
    r(r'G\longrightarrow S',r'G\to S','three structure morphisms','These three arrows are short; the longer additive-functor arrow is retained.',count=3)
    r('foncteurs\n\\[\nf\\longmapsto f^p-tf,\n\\]\noù', 'foncteurs $f\\rightsquigarrow f^p-tf$ où','final assignment','The assignment is inline, with a wavy arrow and no comma before où.','structure')
    if tree=='fr':
        r('donné dans [IV], paragraphe 5','donné dans [2], IV, paragraphe 5','flatness reference','IV is the chapter of the EGA reference [2], explicitly cited in the immediately preceding sentence. There is no bibliography item IV; restoring [2], IV makes the citation usable without changing the historical paragraph number.','misprint of the original')
    upright_page(rel,layer,'236-229')
event('236-1.7','carried as background without fault found','Read the universal-openness and separable-fibre hypotheses, Cartier characteristic-zero parenthesis, openness of the identity-component locus, and smoothness over a reduced base. The stronger pointwise neighbourhood formulation and the EGA IV paragraph-7 citation are also read. They depend on the cited geometric-reducedness/component theorem and Cartier theorem, neither independently proved here.','236, p. 229, corollary 1.7 and following paragraph')
event('236-1.8','carried as background without fault found','Read the fibre-open U, universal openness there, separability of the fibre and reducedness of S at s. The asserted flatness, hence smoothness for these group fibres, invokes the announced EGA IV paragraph-5 criterion. Restored the malformed printed [IV] in the printed layer and recorded [2], IV in corrected French. This identifies the intended book and chapter, not a claim that the later published EGA paragraph numbering has already been verified.','236, p. 229, corollary 1.8 and preceding citation')
event('236-1.9-infinite-origins','independent re-proof','Glue copies of the affine line indexed by Z along their common complement of the origin; addition of the indices defines the special-fibre group law and all other fibres are the unit group. The identity-component locus is the copy with index zero, and the torsion-component locus is the same because Z is torsion-free. This copy is open but not closed: its common punctured line specializes to every other origin. Thus dropping separatedness indeed invalidates closedness of both loci. The realization as the closure of the identity in a degenerating-conic Picard scheme is additional background.','236, p. 229, remark 1.9 first example')
event('236-1.9-additive-kernel','targeted proof check','The displayed map on the additive-group functor is f to f^p minus tf. Its kernel has coordinate algebra V[z]/(z^p-tz), free of rank p with basis 1 through z^(p-1), so is finite flat. The generic derivative is minus t, a unit, giving an etale generic fibre; the special fibre is alpha_p. As an underlying fibrewise locus G zero is precisely the image of the unit section and is closed. No claim that the full connected special fibre equals the unit section as a scheme is made. The consequences continue on p. 230.','236, p. 229, remark 1.9 final example')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='236-229')
record_page('236',229,'Compared sources/fr_printed/fr/236.tex and sources/fr/fr/236.tex, entry lines 372-422, with scan leaf 10 at 400 dpi, full page and three enlarged bands. Read 1.7, its pointwise refinement and both EGA references, 1.8, and both examples beginning 1.9.\n\nRestored CARTIER, punctuation, the letterspaced connexe, mixed-case underlined Remarques, wavy Z and additive-functor G, short structure arrows and the inline wavy assignment. The malformed printed [IV] is restored in the printed layer and resolved to [2], IV only in corrected French. Checked directly the infinite-origin counterexample and the rank-p finite-flat additive kernel. The cited smoothness/flatness theorems and the conic-Picard realization remain background. The kernel example continues on the next page.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
