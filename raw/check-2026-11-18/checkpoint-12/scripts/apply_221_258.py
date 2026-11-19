from audit_utils import *
from collections import Counter
import csv
printed = ("Pour la dernière assertion de (2.2), on note que les noyaux $N_s$ de\n"
           "$\\mathcal F\\longrightarrow\\mathcal F_{(s)}$ restent limités en vertu de (1.2)\n"
           "(i), et que le coefficient du terme en $n^{s-1}$ dans $P_{N_s}$ reste borné ;\n"
           "le lemme 2.6 prouve alors que le coefficient du terme suivant reste minoré.\n")
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-258',line,'2.6 / 2.2 proof / section 3',
                'Scan leaf 11 at 400 dpi and all three enlarged page bands: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,258)
    m=re.search(r'Pour la dernière assertion de \(2\.2\),.*?(?=Cela achève la démonstration\.)',s,re.S)
    assert m
    r(m.group(0),printed,'last four proof lines','The supplied simultaneous-induction discussion is not printed. Restore the exact printed argument about N_s, its coefficient of n^(s-1), and Lemma 2.6 before adjudicating its local slip.','structure')
    if tree=='fr':
        r("$\\mathcal F\\longrightarrow\\mathcal F_{(s)}$ restent limités en vertu de (1.2)",
          "$\\mathcal F\\longrightarrow\\mathcal F_{(s)}$ sont quotients des noyaux des\nhomomorphismes $\\mathcal L_K\\longrightarrow\\mathcal F_{(s)}$, qui restent limités en vertu de (1.2)",
          'last four proof lines, bounded-kernel assertion',
          'The printed N_s need not be bounded: on P^2 let F=O_X direct-sum O_Z with length(Z) arbitrary and s=2. These are quotients of O_X^2, their coefficients in degrees >=1 are fixed, F_(2)=O_X, but N_2=O_Z is unbounded. The kernels of L_K->F_(s) are bounded by 1.2(i) and surject onto N_s. Hence the latter have a fixed coherent source; with the stated bound on their leading coefficient, 2.6 applies. The localized qualification repairs this actual inference without the supplied replacement proof.','misprint of the original')
    old="\\[\nN_r(\\mathcal F)=\\operatorname{Ker}(\\mathcal F\\longrightarrow\\mathcal F_{(r)}),\n\\]\nsoient"
    new=r'$N_r(\mathcal F)=\operatorname{Ker}(\mathcal F\longrightarrow\mathcal F_{(r)})$, soient'
    r(old,new,'induction paragraph, kernel definition','The kernel formula is part of the running sentence, followed by a comma.','structure')
    s,_,_=page_text(rel,258)
    n=s.count(r'\longrightarrow')
    assert n==(5 if tree=='fr' else 4),n
    r(r'\longrightarrow',r'\to','inline morphisms and kernel formulas','The printed arrows are short; the inserted corrected-layer map uses the same notation.',count=n)
    r(r"\fsection{3}{Schémas de Hilbert : définition, théorème d'existence}",
      r"\fsection{3}{\normalfont\uline{Schémas de Hilbert : définition, théorème d'existence}.}",
      'section 3 heading','The heading is ordinary straight-underlined type followed by a full stop.')
    upright_page(rel,layer,'221-258')
event('221-2.6','carried as background without fault found','Read the nilpotent thickening by J_F^a, bounded family of its structure sheaves and reduction to 2.5 over the parameter scheme. The use of bounded algebra structures is carried as background; no independent proof of the entire lemma is claimed.','221, p. 258, first paragraph')
event('221-2.2-small-kernels-printed','refuted, with the refined statement\'s id','Let X=P^2 over an algebraically closed field, L=O_X^2, s=2, and F=O_X direct-sum O_Z for finite Z of arbitrary length m. Then P_F(n)=binomial(n+2,2)+m, so all coefficients in degrees >=s-1=1 are fixed; (a) holds. F_(2)=O_X is bounded, but N_2=O_Z has unbounded Hilbert polynomial m and is not bounded. Thus the printed boundedness assertion for N_s is false. Refined statement id: 221-2.2-small-kernel-sources.','221, p. 258, final proof sentence invoking 1.2(i)')
event('221-2.2-small-kernel-sources','targeted proof check','For the surjection L_K->F and its composite to F_(s), let H be the latter kernel. The map H->N_s is surjective. Since L_K and F_(s) range in bounded families, 1.2(i) bounds H; necessity (a) of 2.1 supplies a common coherent source for H, hence for N_s. Additivity gives bounded coefficient of degree s-1 in P_Ns, and dim supp N_s<=s-1. Lemma 2.6 with r=s-1 then bounds below its next coefficient. Adding the bounded polynomial of F_(s) gives the desired bound for F. This repairs the local proof inference, conditional on the previously stated boundedness lemmas.','221, p. 258, corrected final proof sentence')
event('221-2.2','carried as background without fault found','Read the remaining induction using N_r, additivity of Hilbert polynomials and boundedness under extensions. This records the sequential reading and the separately identified local repair; it does not claim an independent proof of every earlier boundedness input.','221, p. 258, induction paragraph')
event('221-3-Quot-definition','carried as background without fault found','Read the definition of Quot(F/X/S) as quasi-coherent quotient modules flat over S and the initial base-change setup. Preserved the distinction between quotient objects and mere isomorphism classes of underlying modules.','221, p. 258, section 3 opening')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-258')
record_page('221',258,'Compared both French 221.tex files, entry lines 434-477, with scan leaf 11 at 400 dpi and all three enlarged bands. Read the end of Lemma 2.6, the complete proof of Theorem 2.2 on this page, the section heading, the displayed Quot definition and base-change paragraph. Checked the nilpotence exponent, all filtration subscripts, both Hilbert-polynomial expressions, relation signs, primes and tensor base.\n\nRemoved the supplied unprinted replacement proof paragraph and restored the historical text in both layers. In fr only, a localized qualification now distinguishes N_s from the bounded kernels of L_K->F_(s) which surject onto it. The printed assertion is disproved by F=O_(P^2) direct-sum O_Z with arbitrarily large length(Z); the corrected inference to Lemma 2.6 is separately checked and recorded. Restored the inline N_r formula, short arrows, section underlining and upright typed mathematics. The other displayed formulas and all script sheaf letters agree with the scan.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
