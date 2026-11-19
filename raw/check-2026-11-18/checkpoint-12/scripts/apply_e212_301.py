from audit_utils import *
from collections import Counter
import csv
dq=chr(96)*2
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    rel=f'sources/{tree}/fr/e212.tex'
    def r(a,b,line,why,kind='reading',count=1,full=False):
        replace(rel,a,b,layer,'e212-301',line,'Errata to TDTE III',
                'Scan leaf 2 at 400 dpi, full page and three enlarged bands: '+why,kind=kind,count=count,full=full)
    old="présentée\n\\src{302}\nici, est le manque d'un critère d'existence de quotients par une relation\nd'équivalence non propre, telles les relations d'équivalence provenant de\ncertaines opérations"
    new="présentée\nici, est le manque d'un critère d'existence de quotients par une relation\nd'équivalence non propre, telles les relations d'équivalence provenant de\ncertaines\n\\src{302}\nopérations"
    r(old,new,'last two lines and page boundary','Page 301 continues through certaines; the marker belongs immediately before opérations.','structure',full=True)
    r(r'\noindent\textbf{5. TDTE III : Préschémas quotients.}',r'\noindent 5. \uwave{TDTE} III : \uwave{Préschémas quotients}.','title','Separate wavy underlines under TDTE and the title words, in ordinary type.','typesetting')
    for s in ['Page 15, assertion (i)','Pages 18 et 19']:
        r(r'\textbf{'+s+'.}',r'\uline{'+s+'}.','entry headings','Straight underline, ordinary type, final period outside.','typesetting')
    r(' --- ',' - ','entry separators','Short dashes are printed.',count=2)
    r('$Y=X/R$',r'$Y=X/\mathcal R$','quotient','The relation symbol is the handwritten script R.')
    r('$R$',r'$\mathcal R$','relation condition','The repeated relation symbol is script R.')
    r('« ',dq,'fait positif','Ordinary double quotation marks are printed.')
    r(' »',"''",'fait positif','Ordinary double quotation marks are printed.')
    r('TDTE V',r'\uwave{TDTE} V','Picard reference','TDTE has a wavy underline.')
    r('(cf. SHMT)',r'(Cf. \uwave{SHMT})','Hilbert reference','Capital Cf. and wavy SHMT are printed.')
    upright_page(rel,layer,'e212-301')
event('e212-6.1-i','carried as background without fault found','Read the authorial qualification: the proof of quasi-projectivity of the quotient is asserted only when the pre-equivalence relation comes from an equivalence relation. This restricts the reported proof coverage; it is not itself a counterexample to the more general conclusion. The theorem and this qualification remain in their separate original sections.','Erratum 212, p. 301, Page 15, assertion (i); exposé 212, p. 113, Theorem 6.1(i)')
event('e212-8.1','carried as background without fault found','Read the explicit withdrawal of the quotient conjecture and the statement that the positive fact of Remark 8.1 was proved by several authors. The withdrawal agrees with the additive report at the end of exposé 221. The existence and verification of the relevant examples and the cited positive theorem are background here, not new proofs supplied by the erratum.','Erratum 212, p. 301, Pages 18 et 19; exposé 212, pp. 116-117; exposé 221, p. 276, Additif')
event('e212-hilbert-route','carried as background without fault found','Read the alternative Hilbert-scheme route to the Picard construction and the beginning of the stated gap for non-proper equivalence relations. The construction and the Mumford theorem are author-reported dependencies; this sentence continues on the next printed page.','Erratum 212, p. 301, last paragraph')
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
    c=Counter((x['layer'],x['kind']) for x in csv.DictReader(f,delimiter='\t') if x['printed_page']=='e212-301')
record_page('e212',301,'Compared sources/fr_printed/fr/e212.tex and sources/fr/fr/e212.tex, entry lines 5-30 including the misplaced page-boundary continuation, with scan leaf 2 at 400 dpi, full page and three enlarged bands. Read the title, bibliography, both dated corrections and the complete final paragraph portion through certaines. Moved the 302 marker after that word, restored wavy titles/abbreviations, straight entry headings, script relation R, ordinary quotation marks, capital Cf., short separators and upright mathematics. Both French layers agree. Distinguished the restricted proof coverage of quasi-projectivity from a refutation, and recorded the quotient-conjecture withdrawal and later construction reports as background with their internal locations.\n\nOperation counts: '+'; '.join(f'{a}, {b}: {n}' for (a,b),n in sorted(c.items()))+'. Final row verdicts remain pending.')
from update_record_counts import update
update()
