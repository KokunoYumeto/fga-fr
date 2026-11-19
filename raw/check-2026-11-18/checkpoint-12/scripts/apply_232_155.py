from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/232.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'232-155',line,'3.1 proof, 5.1-5.2',
                'Scan leaf 14 at 400 dpi and all three enlarged bands: '+why,kind=kind,count=count)
    notes=list(footnotes(page_text(rel,155)[0]))
    assert len(notes)==1
    r('\\footnote{'+notes[0][2]+'}','','after reference [5], IX, 3.1','There is no editorial footnote in the print. The later erratum remains in its separate section.','structure')
    r('$P^+$',r'$\text{\uwave{P}}^+$','two positive Picard functors','Both functor signs are wavy underlined.',count=2)
    r('i.e.','i. e.','effectivity definition','The initials are spaced.')
    r('soit dans $\\mathfrak C$','soit $\\in\\mathfrak C$','quotient morphism condition','The print uses the membership sign, not the word dans.')
    r(r'\mathbf Q',r'\text{\uwave{Q}}','rational polynomial field','The rational-field Q has a wavy underline.')
    r('est\n$\\mathfrak C$-effective. Or maintenant','est\n$\\text{\\uwave{S}}$-effective. Or maintenant','effectivity of R-sup-Q','The local symbol is a typed S with a wavy underline, distinct from the handwritten class C elsewhere. Restore it in both layers; the preceding and following quotient assertions supply the needed class property without an unsupported normalization.')
    r(r'\result{REMARQUES}',r'\result{\uline{Remarques}}','two remark headings','Both are mixed case and straight underlined.',count=2)
    r('celle de Matsusaka','celle de MATSUSAKA','historical attribution','MATSUSAKA is uppercase.')
    r('schémas de Hilbert (cf.','schémas de Hilbert, (cf.','Hilbert-scheme reference','A comma precedes the first parenthesis.')
    r('(classiquement,','(Classiquement,','second parenthesis','The opening word has a capital C.')
    r(r'\operatorname{Pic}',r'\underline{\operatorname{Pic}}','four Picard scheme names','All four scheme names are straight underlined.',count=4)
    r('Hilbert pour les diviseurs définissant','Hilbert pour les \\uline{diviseurs} définissant','polynomial convention','Only diviseurs is underlined.')
    r('homomorphismes\n\\[\nk(s)\\longrightarrow H^0(X_s,\\mathcal O_{X_s})\\qquad(s\\in S)\n\\]\nsoient', 'homomorphismes $k(s)\\longrightarrow H^0(X_s,\\mathcal O_{X_s})$\n$(s\\in S)$ soient','fibrewise H-zero maps','The morphism and quantified parenthesis are inline.','structure')
    r(r'\longrightarrow',r'\to','four arrows','All arrows are short.',count=4)
    r(r'\xrightarrow{\sim}',r'\overset{\sim}{\to}','universal H-zero map','The tilde is over a short arrow.')
    r('celle de Chow, sauf erreur','celle de\nCHOW sauf erreur','analytic attribution','CHOW is uppercase, without a comma before sauf erreur.')
    upright_page(rel,layer,'232-155')
event('232-3.1-quotient-step','used and rechecked in this run','For the positive Picard locus with the pointwise nonvanishing condition, the cover by D-plus is a smooth surjective projective bundle. Its equivalence relation R has connected projective-space fibres. Each fixed-Hilbert-polynomial locus of D-plus is open and closed; the diagonal meets it, so connectedness of the relation fibres makes it R-stable. On each such quasi-projective locus, the restricted relation is proper and flat, with monomorphic relation map, hence satisfies 212-6.1, whose statement was reread here. That theorem supplies an effective quotient and a faithfully flat proper, hence quasi-compact, quotient map. Gluing these disjoint quotients and then the increasing translates gives the asserted representability. The proof of the quotient theorem and the general representability criterion are inputs already identified as background.','232, p. 155, first paragraph; 212, pp. 112-113, 6.1')
event('232-5-effectivity-symbol','targeted proof check','The printed local symbol before effective for R^Q is wavy S, whereas the four nearby class symbols are handwritten C. It has been restored in both layers. No mathematical emendation of that local category-style notation is justified merely by visual inconsistency; the explicitly cited quotient theorem yields effectiveness and the required fpqc projection in either formulation.','232, p. 155, first paragraph, sentence beginning pour tout Q')
event('232-5.1','targeted proof check','The positive locus is defined fpqc locally by the cohomological conditions and therefore descends when a universal line bundle is unavailable on the base itself. The Hilbert polynomial here is that of the divisor, not of the line bundle; invariance under equivalence follows from the connected projective-bundle fibres just checked. Formation of these invariant open-and-closed loci commutes with base change, allowing the section case to descend. The stated historical comparison with Matsusaka and Chow, and the alternative construction via the Hilbert scheme, are carried as background, not independently established.','232, p. 155, paragraph without a section and remarque 5.1')
event('232-5.2','carried as background without fault found','This is explicitly a proposed existence conjecture under properness, flatness and universal H-zero, followed by a historical analytic claim. Preserve its status as a conjecture and do not insert a later erratum into the expose. The equivalence of the fibrewise H-zero condition and the universal direct-image condition is the proper-flat cohomology-and-base-change input. The analytic existence assertion is not independently proved on this page.','232, p. 155, remarque 5.2 through its page-end fragment')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='232-155')
record_page('232',155,'Compared both French layers, entry lines 611-661, with scan leaf 14 at 400 dpi and three enlarged bands. Read the quotient step concluding the main proof, removal of the section hypothesis, all of 5.1 and the opening of 5.2.\n\nRestored wavy functors and field, membership sign, the locally printed wavy S-effective notation, mixed-case remark headings, straight Picard schemes, exact emphasis, inline cohomology map, arrows, names and punctuation. Removed the unprinted erratum footnote. Rechecked the application of 212-6.1 against its earlier-read statement and the invariant polynomial loci; kept historical and analytic assertions explicitly background. No mathematical difference between the French layers was introduced here.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
