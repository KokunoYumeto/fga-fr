from audit_utils import *
import csv
from collections import Counter
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/221.tex'
    def r(a,b,line,why,kind='reading',count=1):
        replace(rel,a,b,layer,'221-251',line,'1.1 and following paragraphs',
                'Scan leaf 4 at 400 dpi, full page and enlarged bands: '+why,kind=kind,count=count)
    s,_,_=page_text(rel,251)
    for a,b,body in list(footnotes(s)):
        r(s[a:b],'','last paragraph / footnotes','No footnote or note marker occurs on this page; keep the rationale in the audit ledger.','structure')
    if tree=='fr':
        r('encore des ensembles limités','encore ensembles limités','last paragraph, operations assertion','The printed sentence omits des.')
        r('coupe en morceaux','coupe au morceaux','last line','The print reads coupe au morceaux.')
    r(r'\emph{limité}','limité','definition','The defining adjective alone is not underlined or italic.')
    s,_,_=page_text(rel,251)
    m=re.search(r'(\\result\{DÉFINITION\}\{1\.1\} )(.*?)(\n\n)',s,re.S)
    assert m
    body=m.group(2)
    if r'\uline{' not in body:
        r(body,underline_prose(body).replace(r'\uline{est limité}',r'\uline{est} limité'),
          'definition, all five lines','The prose of the definition is straight-underlined except the defined adjective limité; formulas are not underlined.')
    r(r'\uline{Soit}',r'\uline{Boit}','definition opening','The additional close crop shows two closed bowls and a left vertical stroke: the printed word is Boit.')
    r(r"X_s\otimes_{k(s)}k(s')",r"X\otimes(X_s)_{k(s')}",'fibre explanation, line 3','The print has X tensor (X_s) with the lower k(s-prime) on the parenthesized expression.')
    r(r'\emph{famille algébrique}',r'\uline{famille algébrique}','fibre explanation, line 5','The phrase has a straight underline.')
    r(r'\mathbf Z','Z','reduction to finite type over the integers','Z is ordinary upright type, not bold.')
    r(r'$T\longrightarrow S$ et $\mathcal F$ sur',r'$T\longrightarrow S$ et $F$ sur','tensor-family paragraph, line 3','This F is an ordinary typed capital, distinct from the later handwritten script F.')
    r(r"$\mathcal F'$ sur $X_{T'}$",r"$F'$ sur $X_{T'}$",'tensor-family paragraph, line 4','The second family sheaf is an ordinary typed F-prime here.')
    r(r"$\mathcal F''$ sur $X_{T''}$,",r"$F''$ sur $X_{T''}$",'tensor-family paragraph, line 5','The product sheaf is ordinary typed F-double-prime, and no comma follows the base.')
    r(r"T''=T\times_S T'",r"T'=T\times_S T'",'tensor-family paragraph, line 5','The left-hand T has only one prime in the print.')
    for op in ['Tor','Hom','Ext']:
        r(r'\operatorname{'+op+'}',r'\mathop{\text{\uwave{'+op+r'}}}\nolimits','local operations','The local '+op+' operator has a wavy underline.')
    r('plat relativement','\\uline{plat} relativement','penultimate lines','The word plat is straight-underlined.')
    r('« coupe au morceaux »','"coupe au morceaux"','last line','The phrase is enclosed in ordinary double quotation marks.')
    r('initial.)','initial).','last line','The full stop is after the closing parenthesis.')
    if tree=='fr':
        r(r'\uline{Boit}',r'\uline{Soit}','definition opening','Boit is a typographical substitution for the opening imperative Soit in this definition.','misprint of the original')
        r(r"X\otimes(X_s)_{k(s')}",r"X_s\otimes_{k(s)}k(s')",'fibre explanation, line 3',
          'The fibre of X-prime=X times_S S-prime at s-prime equals the fibre X_s extended from k(s) to k(s-prime). The printed redundant X tensor expression is malformed; the supplied base-change formula is retained.','misprint of the original')
        r(r"T'=T\times_S T'",r"T''=T\times_S T'",'tensor-family paragraph, line 5',
          'T-prime already parametrizes the second family; the product is the new T-double-prime used in both following bases X_T-double-prime.','misprint of the original')
        r('encore ensembles limités','encore des ensembles limités','last paragraph, operations assertion','Retain the supplied missing determinant des for the direct-object noun phrase.','misprint of the original')
        r('coupe au morceaux','coupe en morceaux','last line','The idiom is coupe en morceaux; au cannot agree with plural morceaux or express the intended subdivision.','misprint of the original')
    upright_page(rel,layer,'221-251')
event('221-1.1','carried as background without fault found','Read the complete definition of bounded families, preserving its quantifiers and finite-type hypothesis; corrected only the printed word Boit and restored emphasis. No new proof is asserted.','221, p. 251, Definition 1.1')
event('221-1-fibre-identity','targeted proof check','Checked the defining base changes: (X times_S S-prime) times_S-prime Spec k(s-prime) = X times_S Spec k(s-prime) = X_s times_k(s) Spec k(s-prime). This identifies the intended formula and justifies the existing repair of the malformed printed expression.','221, p. 251, paragraph after Definition 1.1, lines 3-4')
event('221-1-bounded-tensor','carried as background without fault found','Read the product-parameter construction and retained T-double-prime for the newly introduced product. The printed ordinary F, F-prime and F-double-prime are retained as local font variants; the tensor-product argument is not claimed as an independent re-proof.','221, p. 251, last paragraph, first seven lines')
event('221-1-bounded-local-operations','carried as background without fault found','Read the assertion for sheaf Tor, Hom and Ext and the appeal to flat families; its continuation and proof dependencies remain to be read. The cited reference is [3], IV, 6.11 as printed.','221, p. 251, last paragraph, lower half')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='221-251')
record_page('221',251,'Compared sources/fr_printed/fr/221.tex and sources/fr/fr/221.tex, entry lines 94-141, with scan leaf 4 at 400 dpi, the full image and all three enlarged bands. An additional close crop confirms Boit. Read the page continuation, Definition 1.1 and each following paragraph, every prime, subscript, arrow, operator, reference and punctuation mark.\n\nRestored the definition underline excluding limité, script-versus-ordinary sheaf-letter variants, wavy local operators, ordinary Z, plat underline, quotation marks and parenthesis punctuation. Removed two unprinted explanatory notes in corrected French. Printed French preserves Boit, the malformed fibre expression, single-prime product parameter, the omitted des and coupe au morceaux; corrected French has five justified repairs. The fibre identity received the explicit base-change check in CHECK_EVENTS; the other assertions are reading/background events.\n\nOperation counts: '+ '; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final second reading pending.')
from update_record_counts import update
update()
