from audit_utils import *
from collections import Counter
import csv
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/232.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'232-143',line,'1, (1.1)-(1.3)',
                'Scan leaf 2 at 400 dpi and all three enlarged bands: '+why,kind=kind,count=count)
    r(r'14\textsuperscript{e} année','14e année','seminar header','The e is printed on the baseline.')
    r(r'\fsection{1}{Groupes et foncteurs de Picard relatifs}',r'\fsection{\normalfont 1}{\normalfont\uwave{Groupes et foncteurs de Picard relatifs}.}','section heading','The upright section title has a wavy underline and a final full stop.')
    r(r'\emph{groupe de Picard}',r'\uline{groupe de Picard}','first definition','The words have a straight underline.')
    r('i.e.','i. e.','local triviality parenthesis','The printed abbreviation has an intervening space.')
    r(r'\xrightarrow{\sim}',r'\overset{\sim}{\to}','(1.1)','The isomorphism arrow is short.')
    r(r'unités de $\mathcal O_X$ (qui',r'unités de $\mathcal O_X$, (qui','units explanation','The print has a comma before the parenthesis.')
    r(r'\longmapsto',r'\rightsquigarrow','three object assignments','All three assignments have a wavy arrow without a source bar.',count=3)
    r(r'(\mathrm{Sch})/S',r'(\text{\uwave{Sch}})/S','two base-category signs','Sch has a wavy underline inside the parentheses.',count=2)
    r('« représentable »',r'\fquote{représentable}','representability sentence','The print uses ordinary double quotation marks.')
    r('car, par suite','car par suite','representability sentence','There is no comma after car.')
    r("d'automorphismes non triviaux",r"\uline{d'automorphismes non triviaux}",'representability sentence','The whole phrase, including d apostrophe, is straight underlined.')
    r('« nature\nlocale »',r'\fquote{\uline{nature locale}}','locality phrase','Only the words nature locale are straight underlined, between ordinary double quotes.')
    r('« rendre local »',r'\fquote{rendre local}','localization phrase','The print uses ordinary double quotes and no underline here.')
    r(r'f:X\longrightarrow S',r'f:X\to S','structural morphism','The arrow is short.')
    r('groupe de Picard relatif ; il sera','groupe de Picard relatif, il sera','terminology sentence','The print uses a comma, not a semicolon.')
    r(r'\emph{groupe de Picard relatif restreint}',r'\uline{groupe de Picard relatif restreint}','restricted relative definition','This phrase is straight underlined.')
    r(r"\operatorname{Pic}'_{X/S}",r"\mathop{\text{\uwave{Pic}}}\nolimits'_{X/S}",'two restricted Picard functor signs','Both functor signs have a wavy underline.',count=2)
    r("\\operatorname{Pic}'(X\\times_S S'/S').\n\\tag{1.3}","\\operatorname{Pic}(X\\times_S S'/S').\n\\tag{1.3}",'(1.3), right member','The print omits the prime after Pic in this right member.')
    if tree=='fr':
        r("\\operatorname{Pic}(X\\times_S S'/S').\n\\tag{1.3}","\\operatorname{Pic}'(X\\times_S S'/S').\n\\tag{1.3}",'(1.3), right member','The preceding sentence defines the functor value as the restricted relative Picard group Pic prime. Formula (1.2) defines that group, and the unprimed absolute Pic accepts a single space rather than this relative pair. The omitted prime is required.','misprint of the original')
    upright_page(rel,layer,'232-143')
event('232-1.1','independent re-proof','Choose local bases of an invertible module. Their transition automorphisms are units g_ij satisfying the multiplicative cocycle equation; changing bases multiplies by a coboundary. Conversely unit cocycles glue copies of O_X into an invertible module. Tensor product multiplies cocycles, and pullback pulls back the same cocycle. Via the degree-one torsor description of sheaf cohomology this gives the stated natural group isomorphism Pic(X)=H^1(X,O_X^*).','232, p. 143, first paragraph and (1.1)')
event('232-1-absolute-functor-locality','targeted proof check','For X=S=Spec k, the test-scheme functor is Pic(T). On T=P^1_k the classes O and O(1) are different but agree on the two standard affine opens; hence this functor is not even separated for the Zariski topology and cannot be represented. This checks the stated general obstruction by an explicit example; the rhetorical no-chance wording is not read as a universal assertion including the empty X.','232, p. 143, second paragraph')
event('232-1.2','targeted proof check','R^1 f_* O_X^* is the sheaf associated on S to the presheaf U maps to H^1(f inverse U,O_X^*). Taking its global sections gives the stated restricted relative group, which identifies families locally in the base. Pullback of invertible modules and sheafification give its contravariance under a base morphism. The definition here is not silently replaced by an étale or fppf Picard functor.','232, p. 143, (1.2)')
event('232-1.3','targeted proof check','Substituting X times_S S prime over S prime into definition (1.2) gives exactly the functor value stated in the preceding prose. The right member must therefore retain Pic prime; the printed missing prime is a notational misprint.','232, p. 143, (1.3)')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='232-143')
record_page('232',143,'Compared both French layers, entry lines 3-51, with scan leaf 2 at 400 dpi and all three enlarged bands. Read the complete seminar/title/author block, both paragraphs and all three numbered displays. Checked every star, prime, cohomological degree, base subscript, reference and emphasis span.\n\nRestored the baseline e, wavy section heading and category/functor underlines, straight prose emphasis, ordinary quotation marks, short arrows and wavy assignments, punctuation and upright typed variables. Retained the handwritten looped structure-sheaf O as script O. Printed French restores the omitted Pic prime in (1.3) as unprimed Pic; corrected French keeps the prime required by the definition and preceding sentence. Checked (1.1) by cocycle gluing, exhibited the O/O(1) locality failure for the naive Picard functor, and checked the definition and naturality of the restricted relative functor.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
