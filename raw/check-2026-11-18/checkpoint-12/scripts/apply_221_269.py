from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-269',line,'5.1 / 5.2 / opening of 5.3',
                'Scan leaf 22 at 400 dpi, all three enlarged bands and a 3x word crop: '+why,kind=kind,count=count)
    r(r'\fsection{5}{Étude différentielle des schémas de Hilbert}',r'\fsection{5}{\normalfont\uline{Étude différentielle des schémas de Hilbert}.}','section heading','The title is straight-underlined upright prose with a terminal period.')
    s,_,_=page_text(rel,269)
    for a,b,body in list(footnotes(s)):
        r(s[a:b],'','Hom-base note','No footnote occurs in the print; the proposed change of scalar ring is also mathematically unnecessary.','structure')
    r(r'X_0=X\times_SS_0',r'X_0=\mathcal F\times_SS_0','definition of X_0','The right-hand factor is clearly the script sheaf F in the scan.')
    r('sur $X$. Ceci posé','sur $U$. Ceci posé','base of the quotient-lift sheaf','The print says U, although the preceding construction varies U over X.')
    r(r'\mathcal A=\operatorname{Hom}',r'\mathcal A=\underline{\operatorname{Hom}}','definition of the acting sheaf','The sheaf Hom sign is straight-underlined, unlike the global Hom group later.')
    r('« formellement principal homogène sous $\\mathcal A$ »','"formellement principal homogène sous $\\mathcal A$"','torsor terminology','The print uses ordinary double quotation marks.')
    r('i.e.','i. e.','two explanatory abbreviations','Both abbreviations are spaced.',count=2)
    r('quotient de $\\mathcal F$ plat\nsur $S$ (','quotient de $\\mathcal F$ plat\nqur $S$, (','5.2 initial flatness condition','The tight crop shows qur, with a descending q, and a comma after S.')
    old="homogène sous\n\\[\n\\mathcal A(X)=\\operatorname{Hom}_{\\mathcal O_{X_0}}\n(\\mathcal K_0,\\mathcal G_0\\otimes_{\\mathcal O_{S_0}}\\mathcal J).\n\\]"
    new=r'homogène sous $\mathcal A(X)=\operatorname{Hom}_{\mathcal O_X}(\mathcal K_0,\mathcal G_0\otimes_{\mathcal O_{S_0}}\mathcal J)$.'
    r(old,new,'5.2 global action group','The formula runs inline and its scalar ring is O_X, without a zero. Keep this in both layers: both arguments are O_X0-modules, so O_X-linear and O_X0-linear maps coincide. The supplied alteration is a normalization, not a mathematical repair.','structure')
    r('est alors garantie','est alors garanti','last sentence of 5.2','The print has the masculine garanti.')
    r(r'\operatorname{Quot}',r'\underline{\operatorname{Quot}}','5.3 representing scheme','The scheme sign has a straight underline.')
    r('(cf. 4 (a)) --','(cf. 4. (a)) -','5.3 reference and dash','There is a period after 4 and a short dash after the parenthesis.')
    if tree=='fr':
        r(r'X_0=\mathcal F\times_SS_0',r'X_0=X\times_SS_0','definition of X_0','The base change defining the scheme X_0 is X times_S S_0. The sheaf F is not the ambient scheme in this fiber product.','misprint of the original')
        r('sur $U$. Ceci posé','sur $X$. Ceci posé','base of the quotient-lift sheaf','The presheaf U -> E(U) on the opens of X glues to a sheaf on X; U is the variable open, not a fixed sheaf base.','misprint of the original')
        r('plat\nqur $S$, (','plat\nsur $S$, (','5.2 flatness preposition','The printed qur is a typographical slip for the preposition sur.','misprint of the original')
        r('est alors garanti','est alors garantie','last sentence of 5.2','The subject existence is feminine.','misprint of the original')
    upright_page(rel,layer,'221-269')
event('221-5.1','targeted proof check','Fix one flat quotient F -> G lifting F_0 -> G_0, and let H=ker(F -> G_0). Flatness identifies JG with J tensor G_0. The restricted map H -> JG agrees on JF with the canonical multiplication map. For any phi:K_0 -> J tensor G_0, subtract phi after H -> K_0 and take the new kernel. The resulting quotient still has reduction G_0 and its J-multiplication map is an isomorphism; the square-zero flatness criterion makes it flat. Conversely the difference of the H-maps of two flat lifts vanishes on JF and factors uniquely through K_0. This supplies the simply transitive action whenever a lift exists and is compatible with restriction. The square-zero flatness criterion is an explicitly used standard algebra input.','221, p. 269, Proposition 5.1')
event('221-5.2','targeted torsor check','Local nonemptiness makes E an A-torsor. Differences of local lift sections form an additive Cech 1-cocycle; changes of choices add a coboundary. Its H^1 class vanishes exactly when the local sections can be adjusted to glue, and any resulting global sections form an A(X)-torsor. Fibres here means stalks of the set-valued sheaf, not geometric fibers of a scheme. The printed global Hom over O_X equals Hom over O_X0 because the source and target actions both factor through O_X0; no correction of that scalar ring is needed.','221, p. 269, Corollary 5.2')
event('221-5.3','carried as background without fault found','Read the hypotheses introducing a point of the representing Quot scheme and its residue extension. The conclusion continues on the following page and is not yet checked.','221, p. 269, opening of Corollary 5.3')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-269')
record_page('221',269,'Compared printed French entry lines 965-1018 and corrected French entry lines 966-1019 with scan leaf 22 at 400 dpi, all three enlarged bands and a 3x crop of the printed word qur. Read the section-5 heading, all of Proposition 5.1 and Corollary 5.2, and the opening hypotheses of 5.3.\n\nRestored the printed F in the X_0 definition, U as the stated base of E, qur and its following comma, garanti, the sheaf-Hom underline, the inline global action group over O_X, the scheme-Quot underline, ordinary quotes, spaced abbreviations and reference punctuation. Corrected French repairs F to X, U to X, qur to sur and the agreement of garantie. Both layers retain the printed global Hom over O_X: the supplied change to O_X0 has no mathematical justification because the two Hom groups are identical here. Removed the unprinted note. The local torsor action was checked through the square-zero flatness criterion, and its H^1 obstruction consequence was checked by gluing cocycles.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
