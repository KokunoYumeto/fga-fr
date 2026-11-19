from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/232.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'232-146',line,'1, (1.9)-(1.10), 2.1-2.2',
                'Scan leaf 5 at 400 dpi and all three enlarged bands: '+why,kind=kind,count=count)
    w=r'\mathop{\text{\uwave{Pic}}}\nolimits'
    u=r'\underline{\operatorname{Pic}}'
    r(r'\operatorname{Pic}_{X/S}',w+r'_{X/S}','five unprimed Pic signs','The functor is wavy underlined; the representing schemes are straight underlined as restored individually below.',count=5)
    r(r"\operatorname{Pic}'_{X/S}",w+r"'_{X/S}",'two primed functor signs','The functor names are wavy underlined.',count=2)
    r('et noté encore\n$'+w+r'_{X/S}$','et noté encore\n$'+u+r'_{X/S}$','name of representing scheme','The representing scheme has a straight underline.')
    r('lorsque\n$'+w+r'_{X/S}$ existe','lorsque\n$'+u+r'_{X/S}$ existe','before (1.10)','The representing scheme has a straight underline.')
    r(r"\operatorname{Hom}_S(S',"+w+r'_{X/S})',r"\operatorname{Hom}_S(S',"+u+r'_{X/S})','(1.10)','The Hom target is the straight-underlined representing scheme.')
    r(r'\emph{préschéma de Picard}',r'\uline{préschéma de Picard}','definition','The phrase is straight underlined.')
    r(r"P'="+w+r"'_{X/S}",r"P'="+w+r'_{X/S}','sufficient representability condition','The printed Pic sign has no prime here, although P-prime is intended.')
    r('« faisceau »',"``faisceau''",'representability paragraph','The print uses ordinary double quotation marks.')
    r("par l'isomorphisme fonctoriel\n", "par l'isomorphisme fonctoriel :\n",'before (1.10)','A colon follows fonctoriel.')
    r(r'\fsection{2}{Relations entre les divers groupes de Picard relatifs et absolus}',r'\fsection{2}{\normalfont\uwave{Relations entre les divers groupes de Picard relatifs et absolus}.}','section 2 heading','The upright heading has a wavy underline and a final period.','structure')
    r(r'\longrightarrow',r'\to','ten arrows','The arrows are short right arrows.',count=10)
    r(r"\operatorname{Pic}'(X/S)\xrightarrow{\sim}",r"\operatorname{Pic}'(X/S)\simeq",'quotient in 2.1','The isomorphism sign is a tilde over a plain bar, without an arrowhead.')
    r(r'\xrightarrow{\sim}',r'\overset{\sim}{\to}','three isomorphism arrows','The other three isomorphisms have short arrowheads under the tilde.',count=3)
    r('i.e.','i. e.','two abbreviations','The initials are spaced.',count=2)
    r(r'pour $f$ et $\mathcal O_X^*$',r'pour $f$ et $\mathcal O_X$','Leray coefficient','The printed coefficient is O-sub-X without a units star.')
    r('quasi-compact. Alors :','quasi-compact. Alors','2.2 opening','There is no colon after Alors.')
    r(r'\noindent (ii) si',r'\noindent (ii) Si','2.2(ii)','Si begins with a capital letter.')
    r(r'\rightrightarrows',r'\mathrel{\substack{\longrightarrow\\[-0.6ex]\longrightarrow}}','last diagram','The two parallel arrows are distinctly longer than the first short arrow.')
    if tree=='fr':
        r(r"P'="+w+r'_{X/S}',r"P'="+w+r"'_{X/S}",'sufficient representability condition','The definition of P-prime on p. 145 and the source of (1.9) require the restricted Picard functor with a prime.','misprint of the original')
        r(r'pour $f$ et $\mathcal O_X$',r'pour $f$ et $\mathcal O_X^*$','Leray coefficient','Picard groups classify torsors under the sheaf of units. The five-term sequence is for O-X-star, not the additive structure sheaf.','misprint of the original')
    upright_page(rel,layer,'232-146')
event('232-1.9','targeted proof check','P-prime is the restricted Picard functor already defined on p. 145. If it is representable, fpqc descent of morphisms makes it a sheaf. Its map to its associated sheaf is then an isomorphism, and (1.8) identifies the target with the full Picard functor. This verifies the sufficient condition and fixes the omitted prime in the preceding printed equality.','232, p. 146, representability paragraph and (1.9)')
event('232-1.10','used and rechecked in this run','The straight-underlined Picard scheme represents the wavy-underlined functor; evaluating its defining natural isomorphism on S-prime gives exactly (1.10), with the relative group of the base-changed family on the right.','232, p. 146, (1.10)')
event('232-2.1','independent re-proof','The hypothesis f_* O_X=O_S identifies f_* O_X^* with O_S^*. Leray for the units sheaf gives 0 to Pic(S) to Pic(X) to H^0(S,R^1 f_* O_X^*) to H^2(S,O_S^*) to H^2(X,O_X^*). The middle H-zero is Pic-prime(X/S) by definition. A section s makes pullback on H^2 split injective since s^* f^*=identity, so the obstruction vanishes and the final map in the displayed short sequence is surjective. This also identifies the printed omission of the units star in the Leray sentence. The general Leray spectral sequence is the background input.','232, p. 146, proposition 2.1 and its proof')
event('232-2.2-opening','carried as background without fault found','Read the hypotheses and both conclusions through the diagram at the page end. Quasi-compactness, separatedness, the structure-sheaf direct-image equality and faithful-flat quasi-compact base change have been retained. The proof and the final exactness clause continue on p. 147 and are not yet claimed checked here.','232, p. 146, proposition 2.2 through final diagram')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='232-146')
record_page('232',146,'Compared both French layers, entry lines 155-214, against scan leaf 5 at 400 dpi and all three enlarged bands. Read the opening continuation, the complete representability paragraph and (1.9)-(1.10), section 2, proposition 2.1 and proof, and the beginning of 2.2 through the final diagram.\n\nRestored wavy functor versus straight scheme underlines, straight definition emphasis, quotation marks and punctuation, the wavy upright section heading, short arrows and the tilde-over-bar quotient isomorphism. The last diagram has two long parallel arrows. Proposition headings and ordinary statement text are retained. The printed equality defining P-prime omits the prime on Pic, and the Leray sentence omits the units star; both are preserved as printed and corrected with reasons in the corrected French. Re-proved 2.1 from the five-term sequence and the section splitting; checked (1.9) and (1.10). The unfinished proof of 2.2 is explicitly deferred to the next page.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
