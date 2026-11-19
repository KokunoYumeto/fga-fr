from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/190.tex'
 def r(a,b,line,statement='B.5',kind='reading',why='',count=1):
  replace(rel,a,b,layer,'190-324',line,statement,'400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 s,_,_=page_text(rel,324)
 for a,b,body in footnotes(s):
  if body.startswith('Le texte imprimé porte'):
   r(s[a:b],'','attribution footnote',kind='structure',why='The explanatory footnote is absent from the print and merges a later authorial erratum into the exposé.')
 r('Chow--Iang','IGUSA-LANG','attribution',why='The printed attribution is IGUSA-LANG. The later authorial correction belongs to its separate erratum section.')
 r(r'\kappa(x)',r'\varkappa(x)','residue field',why='Crossed handwritten kappa.')
 r('i.e.','i. e.','two explanations',count=2,why='Spaced abbreviation.')
 r('noethérien et régulier (','noethérien et \\uline{régulier} (','regular-base hypothesis',why='Only régulier is underlined at this occurrence.')
 r('théorème de\nconnexion de Murre','\\uline{théorème de connexion} de MURRE','extension theorem citation',why='Selective underline and uppercase author.')
 r("« d'égales caractéristiques »",r"\fquote{d'égales caractéristiques}",'equal-characteristic aside',why='Double quotation marks.')
 r('théorème classique de Weil','théorème classique de WEIL','classical attribution',why='Printed capitals.')
 old='que toute section rationnelle de\n$X$ sur $S$ est partout définie'
 r(old,underline_prose(old),'extension assertion',why='Prose underlined; letters excluded.')
 r('plus généralement, que','plus généralement que','next consequence',why='No comma after généralement.')
 old='$S$ étant noethérien et régulier et $K$ désignant\nson anneau des fonctions rationnelles'
 r(old,underline_prose(old),'model-uniqueness hypotheses',why='Underlined prose excluding the following composed-direct aside.')
 old='soit $X$ un\nschéma abélien au-dessus de $K$ ; si $X$ est isomorphe à un $K$-schéma de la\nforme $X_0\\times_S\\operatorname{Spec}(K)$, où $X_0$ est un schéma abélien sur\n$S$, alors $X_0$ est déterminé à un isomorphisme unique près.'
 r(old,underline_prose(old),'model-uniqueness assertion',why='Selective roman underlining.')
 r("$\\alpha:S'\\longrightarrow S$ est un morphisme simple de type fini","$S'\\longrightarrow S$ est un morphisme \\uline{simple} de type fini",'smooth base-change map',why='The print omits the alpha label here and underlines simple; its later reference to alpha is retained.')
 old="alors $X'_0$ est muni d'une\ndonnée de descente canonique relativement à $\\alpha$"
 r(old,underline_prose(old),'canonical descent datum',why='Underlined prose.')
 r('non ramifiée sur $S$','\\uline{non ramifiée sur} $S$','extension condition','5.1',why='Only this hypothesis phrase is underlined in Proposition 5.1.')
 r('simple et surjectif (même','\\uline{simple} et \\uline{surjectif} (même','historical question',why='Separate underlined words.')
 old='\\subsection*{6. Application à des critères de locale trivialité et isotrivialité}\n\\addcontentsline{toc}{subsection}{6. Critères de locale trivialité et isotrivialité}\n\n'
 new='\\addcontentsline{toc}{subsection}{6. Critères de locale trivialité et isotrivialité}\n\\result{6. \\uline{Application à des critères de locale trivialité et isotrivialité}}{} '
 r(old,new,'section 6 heading','B.6',kind='structure',why='Roman run-in underlined heading.')
 r('« pré-schéma en groupes »',r'\fquote{\uline{pré-schéma en groupes}}','group terminology','B.6',why='Double quotes and underlined prose.')
 r('« $G$ opère »',r'\fquote{$G$ \uline{opère}}','action terminology','B.6',why='Double quotes; only opère is underlined.')
 r('est formellement principal homogène sous','est \\uline{formellement principal homogène} sous','definition','B.6',why='Underlined term.')
 r(r'\mathcal O_x',r'\text{\uwave{O}}_x','local ring',why='Ordinary O with wavy underline.')
 upright_page(rel,layer,'190-324')
event('190-B5-extension','carried as background without fault found','The extension of rational sections over a regular noetherian base is a substantial theorem attributed here to Murre, with the printed equal-characteristic limitation. A complete proof has not been reconstructed in this run. The printed definition on 323–324 is smooth and proper with abelian-variety fibers; no additional group law or section is silently inserted.','190, p. 324, opening extension assertion')
event('190-B5-uniqueness','targeted proof check','Assuming the extension theorem, apply it after a smooth base change X-prime to S: the base is regular and the pulled-back family has the same kind of fibers, so a rational S-map into X extends. For two models with a fixed identification of their generic fibers, extend the generic isomorphism in both directions. The composites are the identity on a schematically dense generic fiber; separatedness makes them the identity everywhere. Thus uniqueness is relative to the generic identification. Without that understood identification, automorphisms of an abelian variety would contradict literal uniqueness; no unrecorded extra phrase is inserted.','190, p. 324, first paragraph consequences')
event('190-B5-locality-and-datum','targeted proof check','Models and identifications of their generic fibers glue over a Zariski cover because the extension theorem gives unique transition isomorphisms, hence the cocycle. A finite-presentation model over a local ring spreads to an open neighborhood, giving the stated local-ring reduction, conditional on the usual finite-presentation spreading facts. For a smooth base change S-prime to S, its double and triple fiber products are regular. The generic identification coming from X extends uniquely over the double product; uniqueness over the triple product gives the canonical descent datum.','190, p. 324, second paragraph')
event('190-5.1','targeted proof check','Use the preceding canonical datum on the projective model over the finite etale cover S-prime. Theorem 3 supplies effective descent and projectivity for this finite faithfully flat map. Smoothness and properness descend by the properties in B.2, and the fibers descend the given abelian varieties; the generic fiber is X by full faithfulness. This checks the deduction while retaining the extension theorem, finite-presentation spreading and the general projective descent theorem as background inputs.','190, p. 324, Proposition 5.1')
event('190-5.1-remarks','carried as background without fault found','The questions about a general smooth surjection, an etalement, and automatic projectivity are historical questions, preserved without inserting later answers. Their later development belongs in the notes. The attribution correction embedded in the supplied sources was removed from both layers so it can be checked in the separate authorial erratum.','190, p. 324, Remarks and first-paragraph attribution')
record_page('190',324,r'''Compared sources/fr_printed/fr/190.tex and sources/fr/fr/190.tex entry lines 1296–1349 with scan leaf 27 at 400 dpi, full page and all three enlarged bands. Read the residue-field sign, regularity and equal-characteristic qualifications, every model prime and base subscript, Proposition 5.1, its Remarks and the opening homogeneous-space definition.

Removed the unprinted authorial-erratum footnote and restored IGUSA-LANG in both layers. Restored crossed kappa, wavy local-ring O, MURRE and WEIL capitals, double quotes, selective underlines, the omitted-in-print alpha label, the run-in section 6 heading and punctuation. Proposition 5.1 itself is not wholly underlined: only its non-ramification phrase is. There is no new mathematical correction between the French layers on this page.

The extension theorem is explicitly carried as background. Conditional on it, checked the extension of rational maps from smooth schemes, uniqueness of the model with its fixed generic identification, local gluing, the canonical descent datum and the deduction of Proposition 5.1 from finite faithfully flat projective descent. The generic identification is essential to the uniqueness interpretation; automorphisms are not being denied. Historical questions in the Remarks are retained for later notes.''')
from update_record_counts import update
update()
