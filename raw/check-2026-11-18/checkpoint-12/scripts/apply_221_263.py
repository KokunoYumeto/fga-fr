from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-263',line,'3.4-3.6',
                'Scan leaf 16 at 400 dpi, all three enlarged bands and the focused U_N crop: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,263)
    for a,b,body in list(footnotes(s)):
        r(s[a:b],'','supplied editorial notes','The scan has no footnotes. The supplied erratum paraphrase is not part of the exposé.','structure')
    r('propriété suivante : pour tout préschéma','propriété suivante : Pour tout préschéma','3.4 continuation','The first Pour is capitalized.')
    r(r'\longrightarrow',r'\to','two base morphisms','Both arrows are short.',count=2)
    s,_,_=page_text(rel,263)
    m=re.search(r'(ayant la propriété.*?)(?=\n\n)',s,re.S)
    r(m.group(1),underline_prose(m.group(1)),'3.4 continuation','The complete continued statement prose is straight-underlined.')
    old="tels que\n\\[\n\\operatorname{rang}_{k(s)}\nM_{ns}\\otimes_{\\mathcal O_{S,s}}k(s)\\leq P(n)\n\\quad\\text{pour tout $\\nu\\leq n\\leq N$}.\n\\]\nAlors"
    new="tels que\n$\\operatorname{rang}_{k(s)}M_{ns}\\otimes_{\\mathcal O_{S,s}}k(s)\\leq P(n)$\npour tout $\\nu\\leq n\\leq N$. Alors"
    r(old,new,'Lemma 3.5 rank inequality','The condition is inline; both inequalities in its degree range and the rank bound are visibly non-strict.','structure')
    s,_,_=page_text(rel,263)
    m=re.search(r'(\\result\{LEMME\}\{3\.5\} )(.*?)(?=\n\n)',s,re.S)
    r(m.group(2),underline_prose(m.group(2)),'Lemma 3.5','All statement prose is straight-underlined. The apparent mark above the last U_N is the comma in the preceding line tensor-base subscript, not a prime.')
    r("soit plat sur\n$S_i$. On peut","soit \\uline{plat} sur\n$S$ : On peut",'flat stratification','The print has S without i, a colon before On, and an underline only under plat.')
    if tree=='fr':
        r("soit \\uline{plat} sur\n$S$ : On peut","soit \\uline{plat} sur\n$S_i$ : On peut",'flat stratification','The stratification gives flatness over each stratum S_i, not over the original base S. For example a nonzero module supported at a closed point of an integral base cannot become S-flat by restriction to that closed stratum.','misprint of the original')
    r(r'\quad\text{pour $n\geq n_0$},',r'\quad\text{pour $n\geq n_0$}','Hilbert-polynomial rank display','No comma is printed at the end of this display.')
    r(r"$P<Q$, donc",r"$P\neq Q$ donc",'first polynomial case','The scan has not-equal and no comma before donc. Restore it in both layers: the user requires the 1962 erratum to remain separate, not merged into the exposé.','structure')
    r(r'$P(n)<Q(n)$',r'$P(n)\neq Q(n)$','first polynomial case','The second printed relation is also not-equal. The original argument is preserved for separate erratum treatment.','structure')
    old="Dans le cas contraire,\non aura $P(n)\\geq Q(n)$ pour $n$ grand, donc $U_N=U_{n_0}$"
    new="Si au contraire $P=Q$, alors on aura $U_N=U_{n_0}$"
    r(old,new,'second polynomial case','Restore the exact scanned second case. The supplied replacement had merged a later erratum into the body.','structure')
    if tree=='fr':
        r("l'ouvert $U_\\infty$","l'ouvert $U$",'open-locus reduction','The scan has plain U.')
        r("l'ouvert $U$","l'ouvert $U_\\infty$",'open-locus reduction','The open set just defined by all degree inequalities is U_infinity; U without subscript was not introduced in this proof. Retain the supplied index repair.','misprint of the original')
    old="Si on a\n\\[\n\\operatorname{rang}_{k(s)}\nM_s\\otimes_{\\mathcal O_{S,s}}k(s)\\leq r\n\\quad\\text{pour tout $s$},\n\\]\nalors"
    new="Si on a\n$\\operatorname{rang}_{k(s)}M_s\\otimes_{\\mathcal O_{S,s}}k(s)\\leq r$\npour tout $s$, alors"
    r(old,new,'Lemma 3.6 final condition','The rank bound and quantifier are inline in the printed statement.','structure')
    s,_,_=page_text(rel,263)
    m=re.search(r'(\\result\{LEMME\}\{3\.6\} )(.*?)(?=\n\n|$)',s,re.S)
    parts=m.group(2).split('(on suppose')
    assert len(parts)==2
    r(m.group(2),underline_prose(parts[0])+'(on suppose'+parts[1],'Lemma 3.6','All main statement prose is straight-underlined; the terminal coherence parenthesis is not.')
    # The two remaining displays contain text with inline math. Format their
    # principal expressions before the general inline pass.
    s,_,_=page_text(rel,263)
    for m in list(re.finditer(r'\\\[\n(.*?)\n\\\]',s,re.S)):
        body=m.group(1)
        tag=''
        if body.startswith(r'\tag{*}'+'\n'):
            tag=r'\tag{*}'+'\n';body=body[len(tag):]
        left,right=body.split(r'\quad',1)
        new='\\[\n'+tag+r'\symup{'+left.strip()+'}\n'+r'\quad'+right+'\n\\]'
        r(m.group(0),new,'two retained displays','The main mathematical letters are upright; the operator rang is roman and script O remains script.')
    upright_page(rel,layer,'221-263')
event('221-3.4-continuation','carried as background without fault found','Read the universal property: all graded pieces from degree nu become locally free of the specified polynomial ranks exactly on the unique subscheme. The proof reduces to affine noetherian S and the following two lemmas.','221, p. 263, first paragraph')
event('221-3.5-printed-polynomial-case','refuted, with the refined statement id 221-3.5-eventual-order','The inference P!=Q implies eventual emptiness of U_N is false. Take S=Spec(k), graded algebra k[T], M=k[T], nu=0, Q=1 and P=2: every rank is 1<=2, so U_N=S for all N although P!=Q. The source had merged a later erratum into the body. The scanned argument is restored in both layers under the instruction to keep errata separate.','221, p. 263, first polynomial case')
event('221-3.5-eventual-order','targeted proof check','On each of finitely many connected flat strata, sufficiently high graded ranks equal one polynomial Q. If P(n)<Q(n) eventually, the rank-bound loci eventually vanish on that stratum. Otherwise P(n)>=Q(n) eventually, so all sufficiently high degrees add no restrictions; the finitely many low-degree conditions stabilize. A finite maximum over strata gives stationarity. This checks the needed refinement without inserting the later erratum into the exposé. The supplied scan already has non-strict inequalities in 3.5 and (*).','221, p. 263, proof of 3.5 and (*)')
event('221-3.5-stratum-base','targeted proof check','The flat-stratification module is a module over O_{S_i}; replacing S by the stratum uses flatness over S_i. Flatness over the ambient S would fail, for example for a nonzero closed-point-supported module on an integral curve. Corrected French retains the missing i.','221, p. 263, first proof paragraph')
event('221-3.6','carried as background without fault found','Read the unique locally closed locus where a coherent module becomes locally free of rank r after base change, and its closedness under the global fiber-rank upper bound r. The coherence hypothesis appears in the final un-underlined parenthesis. The proof is on the next page.','221, p. 263, Lemma 3.6')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-263')
record_page('221',263,'Compared printed French entry lines 683-740 and corrected French entry lines 684-741 with scan leaf 16 at 400 dpi and all three enlarged bands. A focused 4x crop distinguishes the unprimed U_N from the preceding-line comma. Read 3.4 continuation, 3.5 and its full proof, the displayed (*) condition and 3.6, with every rank bound, degree range, tensor base and label.\n\nRestored inline inequalities in 3.5 and 3.6, their emphasis, the capital Pour, short arrows, printed colon and the absence of punctuation after the Q(n) display. The print itself has non-strict rank inequalities. Removed the supplied notes and withdrew the merged erratum in both body texts, restoring P!=Q, P(n)!=Q(n), and the P=Q second case. A point example refutes the printed emptiness inference; a separate targeted event checks the eventual-order refinement. Corrected French retains the justified S_i and U_infinity index repairs. The terminal coherence parenthesis in 3.6 is not underlined. The 3.6 proof is still pending.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
