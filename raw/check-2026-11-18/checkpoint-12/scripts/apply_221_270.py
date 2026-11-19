from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-270',line,'5.3 / relative cotangent module / conormal specialization',
                'Scan leaf 23 at 400 dpi and all three enlarged bands: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,270)
    for a,b,body in list(footnotes(s)):
        r(s[a:b],'','relative tensor note','There is no footnote in the print; the correction is documented in the ledger and check event.','structure')
    r(r'\mathcal F_0=\mathcal F_K',r'\mathcal F_0=F_K','opening quotient description','The right-hand F is an ordinary capital, unlike the script F_0.')
    r(r'\mathfrak m','m','maximal ideal and its square','The three letters are ordinary upright lower-case m, not Gothic.',count=3)
    r(r'\mathcal A=\operatorname{Hom}',r'\mathcal A=\underline{\operatorname{Hom}}','three definitions of the acting sheaf','Each sheaf-Hom is straight-underlined; the global Hom group in the intervening formula is not.',count=3)
    r(r'\longrightarrow',r'\to','base morphism g','The arrow is short.')
    r('i.e.','i. e.','interpretation as a section','The abbreviation is spaced.')
    r(r"\mathcal G\otimes_{\mathcal O_{S'}}\mathcal M",r'\mathcal G\otimes_{\mathcal O_S}\mathcal M','relative tensor product','The subscript S has no prime in the print.')
    r(r'\mathcal J_0=\mathcal K_0',r'\mathcal J_0=\mathcal M_0','defining ideal of Y_0','The print has the script M-shaped glyph, not the K of the kernel in 5.1.')
    r(r'où $\mathcal J_0/\mathcal J_0^2$',r'où $\mathcal J/\mathcal J^2$','last sentence, conormal module','The two J signs in the prose have no subscript zero.')
    r('le faisceau conormal à','le \\uline{faisceau conormal} à','conormal terminology','The words faisceau conormal are straight-underlined.')
    if tree=='fr':
        r(r'\mathcal G\otimes_{\mathcal O_S}\mathcal M',r"\mathcal G\otimes_{\mathcal O_{S'}}\mathcal M",'relative tensor product','The square-zero extension D(M) is over S prime. Tensoring over S instead gives the wrong tangent functor, as the explicit rank-one Quot example in CHECK_EVENTS shows.','misprint of the original')
        r(r'\mathcal J_0=\mathcal M_0',r'\mathcal J_0=\mathcal K_0','defining ideal of Y_0','The kernel K_0 of O_X0 -> O_Y0 is the ideal J_0. No M_0 has been defined in this specialization.','misprint of the original')
        r('alors (*) donne','alors (5.1) donne','reference preceding the conormal formula','The displayed formula defining A in Proposition 5.1 is the formula being specialized, but carries no star label. The earlier star on page 263 is an unrelated rank inequality.','misprint of the original')
        r(r'où $\mathcal J/\mathcal J^2$',r'où $\mathcal J_0/\mathcal J_0^2$','last sentence, conormal module','Here the conormal module is J_0/J_0 squared for the ideal of Y_0 in X_0. J without zero is the square-zero base ideal, whose quotient cannot denote this conormal module.','misprint of the original')
    upright_page(rel,layer,'221-270')
event('221-5.3','targeted proof check','Base change the point to K=k(x), making it K-rational on Q_K. The constant lift over K[epsilon]/epsilon^2 gives an origin in the quotient-lift torsor of 5.1; its translation space is Hom(K_0,G_0 tensor_K K epsilon)=H^0(X_K,A). The representing-functor definition identifies these lifts with the relative tangent space, dual to m/m^2 at the K-rational point of Q_K. X_0 in the printed Hom subscript denotes the X_K specialization of 5.1 and needs no normalization.','221, p. 270, conclusion of Corollary 5.3')
event('221-5.3-relative-tensor','refuted, with the refined statement id 221-5.3-relative-tensor-corrected','Take S=X=Spec k and F=k^2. The rank-one quotient component is Q=P^1_k. Put S prime=Spec k[t] and let g be a constant section, so its quotient G, kernel K and test module M are all free of rank one over k[t]. Hom(g*Omega_Q/S,M) is k[t]. With the printed tensor over k, the proposed right side is k[t] tensor_k k[t], of infinite rank over k[t], so the claimed isomorphism fails.','221, p. 270, relative formula for A')
event('221-5.3-relative-tensor-corrected','targeted proof check','Use G tensor_{O_S prime} M. Maps D(M) -> Q lifting g are derivations, hence Hom(g*Omega_Q/S,M); the constant lift supplies their origin. Proposition 5.1 identifies the same lifts with H^0 Hom(K,G tensor_{O_S prime} M). The conormal description g prime*(J/J^2)=g*Omega_Q/S follows from the section of Q times_S S prime.','221, p. 270, relative cotangent characterization')
event('221-conormal-specialization','targeted proof check','For I=J_0=K_0 and T=O_Y0 tensor_{O_S0} J, the ideal I annihilates T. Any O_X0-linear map I -> T therefore kills I^2 and factors uniquely through I/I^2, giving the displayed conormal formula. The final unindexed J/J^2 must refer to J_0/J_0^2, because the unindexed J elsewhere is the square-zero base ideal. The printed star reference has no local target; 5.1 is the applicable formula.','221, p. 270, last paragraph and display')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-270')
record_page('221',270,'Compared printed French entry lines 1013-1060 and corrected French entry lines 1014-1061 with scan leaf 23 at 400 dpi and all three enlarged bands. Read the tangent-space conclusion of 5.3, the relative cotangent characterization and the beginning of the conormal specialization.\n\nRestored ordinary F_K and m, all three sheaf-Hom underlines, the short arrow, spaced abbreviation, the printed tensor subscript S, printed M_0, and the unindexed J/J squared in the final prose. Removed the unprinted explanatory footnote. Corrected French repairs the tensor base to S prime, M_0 to K_0, the dangling star reference to 5.1 and the final conormal indices to zero. The tangent-space identification and relative version were checked using square-zero lifts; an explicit constant section of P^1 shows that the printed tensor base is wrong. The conormal factorization was checked algebraically. Retained the harmless X_0 notation in the first Hom formula and the printed plus sign defining D(M).\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
