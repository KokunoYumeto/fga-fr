from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='A.4(e)',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-314',line,statement,'400-dpi full image and all three enlarged bands. '+why,kind,count=count)
 r("\\[\n  H^1(S'/S,G_m)=0\n\\]", "$H^1(S'/S,G_m)=0$",'line 1',kind='structure',why='The formula runs inline with the following condition.')
 old="\\emph{lorsque $A$ est un corps et $A'$ une extension galoisienne finie de ce\ndernier (cf. exemple 1), et peut encore s'exprimer en disant que, dans le cas\nenvisagé, $S'\\longrightarrow S$ est un morphisme de descente strict pour la\ncatégorie fibrée des faisceaux localement libres de rang 1.}"
 left="lorsque $A$ est un corps et $A'$ une extension galoisienne finie de ce dernier"
 right="et peut encore s'exprimer en disant que dans le cas envisagé, $S'\\longrightarrow S$ est un morphisme de descente strict pour la catégorie fibrée des faisceaux localement libres de rang"
 new=underline_prose(left)+" (cf. exemple 1), "+underline_prose(right)+" 1."
 r(old,new,'lines 1–4',why='Selective prose underlining excludes the reference and rank numeral; no comma after que.')
 r('local artinien','local \\uline{artinien}','Artinian hypothesis',why='Underlined adjective.')
 r("d'idéal maximal $\\mathfrak m$","d'idéal maximal $m$",'first maximal-ideal letter',why='This first occurrence is typed ordinary m; the handwritten quotient letters retain their supplied Gothic encoding provisionally.')
 for label in ['i','ii','iii']:
  r('\\item[('+label+')]',r'\item[\textnormal{('+label+').}]','condition '+label,why='Roman label with a period.')
 r("c'est un morphisme de descente strict pour les","c'est un morphisme de descente \\uline{strict} pour les",'free-module conclusion',why='Only strict is underlined here.')
 r('Amitsur','AMITSUR','attribution','A.4 remark',why='Printed capitals.')
 r('« globale »',r'\fquote{globale}','Brauer-group description','A.4 remark',why='Double quotes.')
 r(r'\fsection{B}{Descente par morphismes fidèlement plats}',r'\section*{\normalfont B. \uline{Descente par morphismes fidèlement plats}.}'+'\n'+r'\addcontentsline{toc}{section}{B. Descente par morphismes fidèlement plats}','section B heading','B',kind='structure',why='Roman underlined heading with a period, rather than the bold fsection style.')
 r(r'\subsection*{1. Énoncé des théorèmes de descente}',r'\subsection*{\normalfont 1. \uline{Enoncé des théorèmes de descente}.}','subsection heading','B.1',why='Unaccented initial E, roman underline and final period.')
 r('préschémas','pré-schémas','definition first line','B.1.1',why='Printed hyphen.')
 for term in ['plat','fidèlement plat']:
  r('\\emph{'+term+'}','\\uline{'+term+'}','definition of '+term,'B.1.1',why='Underline.')
 r('est dit \\uline{plat} si, pour tout','est dit \\uline{plat} si pour tout','definition first line','B.1.1',why='No comma after si.')
 r('i.e.','i. e.','two explanatory abbreviations','B.1.1',why='Printed spacing.',count=2)
 r('Serre [5]','SERRE [5]','last paragraph reference','B.1.1',why='Printed capitals.')
 r('est exact et fidèle) ;','est \\uline{exact} et \\uline{fidèle}) ;','faithfully-flat module definition','B.1.1',why='Exact and fidèle are separately underlined.')
 r(r'\mathcal O',r'\text{\uwave{O}}','five local-ring identifiers','B.1.1',why='The principal occurrences use ordinary wavy-underlined O.',count=5)
 if tree=='fr_printed':
  r("\\otimes_{\\text{\\uwave{O}}_{\\alpha(x')}}","\\otimes_{O_{\\alpha(x')}}",'tensor base ring','B.1.1',why='No wavy underline is printed on this tensor-base O.')
  r("le $\\text{\\uwave{O}}_{\\alpha(x')}$-module","le $O_{\\alpha(x')}$-module",'coefficient-module ring','B.1.1',why='No wavy underline is printed on this O either.')
 upright_page(rel,layer,'190-314')
with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 for line,old,new in [
  ('tensor base ring',"\\otimes_{O_{\\alpha(x')}}","\\otimes_{\\text{\\uwave{O}}_{\\alpha(x')}}"),
  ('coefficient-module ring',"le $O_{\\alpha(x')}$-module","le $\\text{\\uwave{O}}_{\\alpha(x')}$-module")]:
  w.writerow(['sources/fr/fr/190.tex','French corrected','190-314',line,'B.1.1',old,new,'The bottom band omits the wavy underline at this occurrence. Corrected French supplies the same local-ring identifier already explicitly named immediately above as the coefficient ring.','misprint of the original','low'])
event('190-A4e-hilbert90','targeted proof check','For a finite Galois extension L/K and multiplicative cocycle a_sigma with a_sigma_tau=a_sigma sigma(a_tau), choose x such that b=sum_sigma a_sigma sigma(x) is nonzero (linear independence of distinct field automorphisms). Then tau(b)=a_tau^-1 b, so a_tau=b/tau(b), a coboundary. This proves H¹=0 in the convention used, and the preceding classification interprets it as effectivity for rank-one objects; Hom descent follows from L^Gamma=K. Linear independence is the standard elementary field-theory input, not re-proved here.','190, p. 314, first paragraph')
event('190-A4e-artinian-equivalence','carried as background without fault found','Read all three vanishing conditions, the k>0 range, powers k+1 and strict-epimorphism addendum. No independent proof of their full equivalence is claimed. A proof must control the congruence filtrations 1+M_n(m^r A-prime), identify successive square-zero increments with additive matrices, and justify lifting invariant bases. The assertion for infinitely generated free modules additionally requires control of column-finite changes of basis; finite n alone does not supply that step automatically. These requirements are retained for the notes.','190, p. 314, Artinian conditions (i)–(iii) and following paragraph')
event('190-A4-remark-amitsur-brauer','carried as background without fault found','Read the stated Amitsur attribution and the Brauer-group comparison with [1], chapter VII. No historical priority claim or exact Brauer comparison is independently established at this stage; the supplied reference will be assessed with the bibliography and later notes.','190, p. 314, remark')
event('190-B1.1-flatness','targeted proof check','Local flatness of stalk maps is equivalent to affine algebra flatness by localization of the finite-relation criterion. A flat A-algebra is faithfully flat iff every residue field has nonzero tensor product, equivalent to surjectivity on Spec. A flat local map of local rings is faithfully flat; hence a surjective flat scheme map detects nonzero sheaf stalks and gives exact, faithful pullback of quasi-coherent modules. The concluding sequence criterion continues on 315.','190, p. 314, definition B.1.1 and following paragraph')
record_page('190',314,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 794–848 with scan leaf 17 at 400 dpi, full page and all three enlarged bands. Read all cohomology groups, quotient powers, Greek subscripts and the faithful-flatness definitions.

Restored the opening Hilbert-90 formula inline, selective prose underlines excluding rank 1 and the reference, ordinary typed m at its first occurrence, Roman condition labels with periods, the underline on strict, AMITSUR/SERRE capitals, double quotes, hyphenated pré-schémas, spaced i. e. and heading typography (including unaccented Enoncé). The two handwritten quotient m letters retain their supplied Gothic encoding provisionally. The tensor-base and coefficient-module O letters lack the wavy underline in print: those omissions are represented in printed French and recorded as notation repairs in corrected French.

Checked the elementary Hilbert-90 cocycle argument and its descent interpretation, and the local/affine faithfully-flat criteria. The full Artinian equivalence and its infinite-free-module extension are carried as background with the proof requirements stated explicitly, not as a completed proof. The Amitsur/Brauer reference remains a reference to be assessed at the notes stage.''')
from update_record_counts import update
update()
