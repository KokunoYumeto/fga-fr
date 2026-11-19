from audit_utils import *
from collections import Counter
before_rows=list(csv.DictReader((ROOT/'CORRECTIONS.tsv').open(newline=''),delimiter='\t'))
locators=[]
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/212.tex'
 _,lo,hi=page_text(rel,117);locators.append(f'{rel}, entry lines {lo}-{hi}')
 def r(a,b,line,why,kind='reading',count=1):
  replace(rel,a,b,layer,'212-117',line,'8.1','Scan 212, printed p. 117, PDF leaf 20, rendered at 400 dpi; full page and all three 1.3x enlarged bands inspected. '+why,kind=kind,count=count)
 s,_,_=page_text(rel,117)
 for a,b,body in list(footnotes(s)):
  if body.startswith("L'erratum lié"):
   r(s[a:b],'','conjecture heading','There is no footnote at the heading or foot of this printed page. The later author erratum belongs in its separate printed section.','structure')
 old=r"""\emph{La relation d'équivalence définie par $G$ est
effective, le quotient $Y=X/G$ est de type fini sur $S$ et le morphisme
canonique $f:X\to Y$ est plat et surjectif}"""
 r(old,underline_prose(old[len(r'\emph{'):-1]),'conjecture 1, main assertion','The prose is straight-underlined, with mathematical expressions excluded from the underline; it is not italic.')
 old=r"""(donc $X$ devient un fibré
principal homogène sur $Y$, de groupe $G\times_S Y=\operatorname{GP}(n)_Y$)"""
 r(old,underline_prose(old),'conjecture 1, parenthesis','The prose of this parenthesis is also underlined; the supplied emphasis omitted it.')
 old=r"""Soit $\mathcal L'$ le faisceau inversible sur $Y$ déduit
de $\mathcal L$ par « descente fidèlement plate » par $f$ (cf. [1], B,
\S~th. 1). Alors $\mathcal L'$ est \emph{préample sur $Y$ par rapport à $S$},
i.e. il existe un entier $m$ et un morphisme quasi-fini de $Y$ dans un schéma
projectif-type convenable $\mathbf P_S^N$, tels que $(\mathcal L')^{\otimes m}$
soit isomorphe à l'image inverse de $\mathcal O_{\mathbf P_S^N}(1)$."""
 p1=r"""Soit $\mathcal L'$ le faisceau inversible sur $Y$ déduit de $\mathcal L$ par \fquote{descente fidèlement plate} par $f$"""
 p2=r"""Alors $\mathcal L'$ est \fquote{préample} sur $Y$ par rapport à $S$"""
 p3=r"""il existe un entier $m$ et un morphisme quasi-fini de $Y$ dans un schéma projectif-type convenable $\mathbf P_S^N$, tels que $(\mathcal L')^{\otimes m}$ soit isomorphe à l'image inverse de $\mathcal O_{\mathbf P_S^N}(1)$."""
 new=underline_prose(p1)+r' (cf. [1], B, \S~th. 1). '+underline_prose(p2)+',\ni. e. '+underline_prose(p3)
 r(old,new,'conjecture 2, whole assertion','Straight underlining covers the assertion prose, except the parenthetical reference and i. e.; both descente fidèlement plate and the first préample have ordinary double quotation marks.')
 r(r'\mathbf P',r'P','conjecture 2, projective-space symbols','Both projective-space P symbols are plain upright typed letters, not bold.',count=2)
 r('« problèmes de modules »',r'\fquote{problèmes de modules}','separatedness paragraph','The printed quotation marks are ordinary double quotes.')
 r('i.e.','i. e.','separatedness and ampleness abbreviations','Both explanatory abbreviations have spaces between the letters in the print.',count=2)
 if tree=='fr_printed':
  r('parvient a bien','parvient à bien','last line before remarks','The printed à has a visible grave accent; preserve this original grammatical misprint.')
 else:
  with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
   csv.writer(f,delimiter='\t').writerow([rel,layer,'212-117','last line before remarks','8.1','parvient à bien','parvient a bien','The enlarged middle band visibly prints à. Retain the existing corrected a: the subject la relation requires the verb a in a bien un graphe fermé, not the preposition à.','misprint of the original','low'])
 r(r'\noindent\textbf{REMARQUES 8.1. ---}',r'\result{REMARQUES}{8.1}','remarks heading','The heading uses ordinary upright capitals, with a period and short dash; no boldface.')
 r('« formes »',r'\fquote{formes}','remarks, group forms','Ordinary double quotes are printed.')
 old=r"""soit $X$ \emph{un schéma
affine sur un corps $k$ de caractéristique $0$, où le groupe
$\operatorname{Gl}(n)_k$ ou $\operatorname{GP}(n-1)_k$ opère librement. Alors
la relation d'équivalence définie par $G$ est effective, le quotient $X/G$ est
également affine, et le morphisme $X\to X/G$ est plat et surjectif}"""
 new=r"""Soit $X$ un schéma
affine sur un corps $k$ de caractéristique $0$, où le groupe
$\operatorname{Gl}(n)_k$ ou $\operatorname{GP}(n-1)_k$ opère librement. Alors
la relation d'équivalence définie par $G$ est effective, le quotient $X/G$ est
également affine, et le morphisme $X\to X/G$ est plat et surjectif"""
 r(old,underline_prose(new),'remarks, positive assertion','The scan begins Soit with capital S and underlines its prose through surjectif, including Soit; mathematical letters remain outside the underlines.')
 upright_page(rel,layer,'212-117')
event('212-8.1','carried as background without fault found','Read as the historical conjecture stated on this page, not as a proved theorem. The supplied footnote about the later erratum is absent from the scan and is removed from the exposition. The separate author erratum will be read in its own sequence. No change to the conjecture hypotheses or conclusions is made here.','212, p. 117, Conjecture 8.1, 1 and 2')
event('212-8.1-remark','carried as background without fault found','The characteristic-zero affine quotient assertion and the stated representation-theoretic input were compared with the scan. Their proofs are not supplied on this page and are not certified by this reading.','212, p. 117, Remarks 8.1')
rows=list(csv.DictReader((ROOT/'CORRECTIONS.tsv').open(newline=''),delimiter='\t'))[len(before_rows):]
counts=Counter((x['layer'],x['kind']) for x in rows)
record_page('212',117,'Compared '+ '; '.join(locators)+' with scan leaf 20 at 400 dpi, full page and all three enlarged bands. Read every paragraph and all inline formulas, indices, punctuation, emphasis and references.\n\nRemoved the unprinted later-erratum footnote, restored the scope of straight underlining (including the first parenthesis and Soit in the remarks), ordinary quotation marks including the omitted quotes around préample, plain projective P, the ordinary heading, and upright typed variables. A further 3x crop confirms the looped handwritten O of the twisting sheaf; its script alphabet is retained. The print has parvient à bien; the printed layer retains it and the corrected layer retains the justified a. The conjecture and the positive affine assertion remain historical statements, without a claim of proof.\n\nOperation counts: '+ '; '.join(f'{layer}, {kind}: {n}' for (layer,kind),n in sorted(counts.items()))+'. The required final second reading remains pending.')
from update_record_counts import update
update()
