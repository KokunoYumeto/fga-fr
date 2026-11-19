from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/232.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'232-154',line,'4.5, 5',
                'Scan leaf 13 at 400 dpi and three enlarged bands: '+why,kind=kind,count=count)
    r('voisinage de $s$ »',"\\uline{voisinage de} $s$''",'opening continuation','The underline stops before s, and the closing quote is ordinary double.')
    r(r'\operatorname{Div}_{X/S}',r'\underline{\operatorname{Div}}_{X/S}','four divisor names','Three names denote schemes and are straight underlined; the functor occurrence is distinguished in the next operation.',count=4)
    r(r'\operatorname{Pic}_{X/S}',r'\underline{\operatorname{Pic}}_{X/S}','two Picard scheme names','Both are straight underlined.',count=2)
    r("\\fsection{5}{Démonstration du théorème principal d'existence}","\\fsection{5}{\\normalfont\\uwave{Démonstration du théorème principal d'existence}.}",'section heading','The upright heading is wavy underlined and ends with a period.')
    r("Posons pour abréger\n\\[\nP(S')=\\operatorname{Pic}(X\\times_SS'/S'),\n\\]\net", "Posons pour abréger\n$P(S')=\\operatorname{Pic}(X\\times_SS'/S')$, et",'abbreviated Picard functor','This definition is inline.','structure')
    r('$P',r'$\text{\uwave{P}}','Picard functor variables','These occurrences are wavy underlined, except the final unmarked P-plus restored below.',count=11)
    r('représentabilité de\n$\\text{\\uwave{P}}^+$.','représentabilité de\n$P^+$.','last Picard abbreviation','The last P-plus is locally unmarked in the print; retain that omission.')
    r('$D=\\underline{\\operatorname{Div}}_{X/S}$, et soit $D^+$', '$\\text{\\uwave{D}}=\\text{\\uwave{Div}}_{X/S}$, et soit $\\text{\\uwave{D}}^+$','divisor functor abbreviations','The first D and D-plus and this Div denote functors and are wavy underlined.')
    r(r'$D\longrightarrow P$',r'$\text{\uwave{D}}\longrightarrow\text{\uwave{P}}$','canonical morphism','Both variables denote functors and are wavy underlined.')
    r(r'D^+\longrightarrow P^+,',r'\text{\uwave{D}}^+\longrightarrow\text{\uwave{P}}^+,','display (+)','Both variables have wavy underlines.')
    r('on sait déjà que $D^+$','on sait déjà que $\\text{\\uwave{D}}^+$','representability sentence','Only the functor D-plus is wavy; the open subscheme D-plus later in the same sentence is plain.')
    r('« théorèmes A et B » de Serre',"``théorèmes A et B'' de SERRE",'Serre reference','Ordinary double quotes and uppercase SERRE are printed.')
    old="R^if'_*(\\mathcal L(n))=0\\quad\\text{pour $i>0$ et tout $n\\geq0$},\n\\qquad\nf'_*(\\mathcal L(n))\\neq0\\quad\\text{pour tout $n\\geq0$}."
    new="\\begin{gathered}\n\\symup{R^if'_*(\\mathcal L(n))=0}\\quad\\text{pour $i>0$ et tout $n\\geq0$}\\\\\n\\symup{f'_*(\\mathcal L(n))\\neq0}\\quad\\text{pour tout $n\\geq0$}.\n\\end{gathered}"
    r(old,new,'two positivity conditions','The two conditions occupy separate centered lines, with no comma after the first.','structure')
    r('simples projectifs surjectifs','\\uline{simples projectifs surjectifs}','morphism (+)','All three adjectives are straight underlined.')
    r('fibrés projectifs\nassociés à des Modules localement libres','\\uline{fibrés projectifs\nassociés à des Modules localement libres}','precise form of (+)','This entire phrase is underlined, stopping before partout non nuls.')
    r('est comme au début','est, comme au début','last paragraph punctuation','A comma follows est.')
    r('est un Module localement libre','est un Module \\uline{localement libre}','direct image module','Only localement libre is straight underlined.')
    r(r'\mathcal Q',r'\mathfrak Q','coherent module','The Q is Gothic.')
    r(r'\longrightarrow',r'\to','four arrows','The arrows are short.',count=4)
    if tree=='fr':
        r("\\symup{f'_*(\\mathcal L(n))\\neq0}\\quad\\text{pour tout $n\\geq0$}.","\\symup{f'_*(\\mathcal L(n))\\neq0}\\quad\\text{en tout point de $S'$ et pour tout $n\\geq0$}.",'nonvanishing condition','The proof needs positive rank everywhere, explicitly stated later as partout non nuls. Mere nonzero sheaf is not preserved by arbitrary base change: on two disjoint points, use X=P1 and L=O on the first component, O(-1) on the second. All higher cohomology vanishes for n>=0 and the pushforwards are globally nonzero, but restriction to the second point has H0(L)=0. Make the required pointwise scope explicit only in corrected French.','misprint of the original')
    upright_page(rel,layer,'232-154')
event('232-4.5-base-change','targeted proof check','The local dual-module description identifies the map (f_*L)_s to H0 of the fibre with Hom_A(Q,A) to Hom_k(Q tensor k,k). If surjective, lift a basis of the latter dual: the resulting Q to A^r is an isomorphism modulo the maximal ideal. It is surjective by Nakayama, splits because A^r is free, and its kernel has zero reduction, hence is zero. Thus Q is free, and conversely free Q gives all base changes. H1 vanishing implies the needed base-change surjectivity by the cohomology-and-base-change theorem. For the universal Abel map the same calculation is made after a local cover carrying a line bundle; descent preserves smoothness.','232, p. 154, conclusion of remarque 4.5')
event('232-5-nonvanishing','refuted, with the refined statement\'s id','Interpreting the displayed nonzero condition as nonzero sheaf is insufficient: let S be two disjoint k-points, X=P1_S, and L restrict to O and O(-1). For all n>=0, higher cohomology of L(n) vanishes and the pushforward is nonzero globally, yet after base change to the second point H0(L)=0. Refined statement 232-5-nonvanishing-refined requires nonvanishing at every point, as the later phrase partout non nuls already requires.','232, p. 154, defining display for P-plus')
event('232-5-nonvanishing-refined','targeted proof check','With the pointwise qualification, vanishing of higher direct images gives a locally free direct image commuting with arbitrary base change; its positive rank is then preserved. Twisting by O(1) shifts n to n+1 and preserves the conditions. Locally on any finite-presentation test family, uniform Serre vanishing handles all sufficiently large twists, while finitely many remaining cohomology and rank conditions are open. Sufficiently large twists of every line bundle satisfy the conditions locally on the base. Thus the translated opens exhaust the Picard functor, and the Abel map above P-plus is a projective bundle of positive rank, hence smooth and surjective. The cohomology, uniform Serre, and representability-gluing theorems remain the named background inputs.','232, p. 154, section 5 through the projective-bundle paragraph')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='232-154')
record_page('232',154,'Compared both French layers, entry lines 560-612, with scan leaf 13 at 400 dpi and three enlarged bands. Read the end of 4.5 and the start of the main existence proof, including both positivity conditions and map (+).\n\nRestored scheme/functor distinctions, local omissions of underlining, the inline abbreviation, the two-line conditions, heading, exact emphasis, punctuation and uppercase attribution. Rechecked the dual-module base-change criterion and the construction of the positive locus. The printed nonzero condition needs nonvanishing at every point to be stable under base change and to give a surjective projective bundle; recorded the disconnected-base counterexample and added that scope only in corrected French.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
