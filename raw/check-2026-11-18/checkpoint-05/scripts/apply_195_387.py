from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/195.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'195-387',line,'C.4–5','400-dpi full scan and all three enlarged bands. '+why,kind,count=count)
 s,_,_=page_text(rel,387)
 notes=list(footnotes(s)); assert len(notes)==2
 for a,b,n in reversed(notes):
  r(s[a:b],'','editorial erratum footnote '+('on abelian smoothness' if 'Mumford' in n else 'on the open subset'),kind='structure',why='Absent from this exposé page; later author material remains in its separate erratum section.')
 r('dû à Serre','dû à SERRE','attributed argument typography',why='SERRE is printed in capitals.')
 r('(À partir de là','(A partir de là','parenthesis initial accent',why='The printed capital A is unaccented.')
 r('« théorème d\'existence »',r"\fquote{théorème d'existence}",'existence theorem quotation',why='Ordinary double quotation marks.')
 r('connexe.) Cela','connexe). Cela','end of generalization parenthesis',why='The period follows the closing parenthesis in the scan.')
 r(r'\Theta',r'\mathfrak G','derivation sheaf letter',why='Same Gothic G as on the preceding pages.')
 r('simple sur $\\Lambda$, i.e.','\\uline{simple} sur $\\Lambda$, i. e.','formal smoothness wording typography',why='Only simple is underlined; spaced i. e.')
 r('proposition 5.2, permet','proposition 5, 2 permet','lifting criterion reference number',why='Printed comma numbering, with no comma after 2.')
 span="problème d'existence de\nschémas abéliens se réduisant suivant un schéma abélien donné"
 r(span,r'\uline{'+span+'}','lifting problem emphasis',why='The whole phrase, from problème through donné, is underlined.')
 r('de\ncaractéristique zéro.','de\ncaractéristique $0$.','characteristic-zero notation',why='The scan uses the numeral 0, not the word zéro.')
 r('« foncteur\nde Greenberg »',r'\fquote{\uline{foncteur'+ '\n' +r'de Greenberg}}','Greenberg quotation and emphasis',why='Ordinary double quotation marks; the three words are underlined.')
 r(r'\subsection*{5. Extension des revêtements}',r'\subsection*{\textnormal{5. \uline{Extension des revêtements}.}}','section heading',kind='typesetting',why='Roman heading, words underlined, final period.')
 r('un pré-schéma formel noethérien','un pré-schéma \\uline{formel} noethérien','formal-prescheme emphasis',why='Only formel is underlined.')
 r('« non-annulation »',r'\fquote{non annulation}','nonvanishing quotation',why='Ordinary double quotation marks and no hyphen in the printed words.')
 old='qui est non-diviseur de zéro non\nseulement sur $\\mathfrak X$, mais sur tout\n$X_n$, donc assez gros pour'
 new='qui est non\ndiviseur de zéro, donc assez gros pour'
 r(old,new,'non-zero-divisor hypothesis',kind='structure',why='The original says only non diviseur de zéro. The added condition on every X_n is an author erratum and must not be merged into either exposé layer.')
 r('sur un ouvert $V$, nulle sur\n$U\\cap V$, soit nulle.','sur un ouvert $V$ nulle sur\n$U\\cap V$ soit nulle.','density assertion punctuation',why='Neither comma is printed.')
 r('« idéal de définition »',r'\fquote{idéal de définition}','ideal-of-definition quotation',why='Ordinary double quotation marks.')
 old=r'''$\mathfrak X$, et soit
\[
  X_n=(\mathfrak X,\mathcal O_{\mathfrak X}/\mathcal J^{n+1}),
\]
qui est donc'''
 new=r'''$\mathfrak X$, et soit $X_n=(\mathfrak X,\mathcal O_{\mathfrak X}/\mathcal J^{n+1})$, qui est donc'''
 r(old,new,'ordinary thickening formula',kind='structure',why='The definition of X_n is inline, followed by its comma.')
 r('sont deux revêtements plats de','sont deux \\uline{revêtements plats} de','flat covers emphasis',why='Both words are underlined.')
 r('i.e. deux','i. e. deux','cover explanation abbreviation',why='Spaced i. e.')
 r('modules), non\nramifiés sur $U$','modules), \\uline{non\nramifiés sur} $U$','unramified locus emphasis',why='The prose span is underlined; U is outside it.')
 r('est injective ; en particulier,','est \\uline{injective}, en particulier','injectivity sentence punctuation and emphasis',why='Printed comma, not semicolon; no comma after particulier; injective is underlined.')
 span="un automorphisme de $\\mathfrak X'$ qui induit\nl'identité sur $X'_0$ est l'identité"
 r(span,underline_prose(span),'automorphism conclusion emphasis',why='The prose is underlined, excluding the mathematical scheme symbols.')
 r('Partons, en particulier,','Partons en particulier,','last sentence punctuation',why='No comma follows Partons.')
 s,_,_=page_text(rel,387)
 r(r'\mathcal O',r'\text{\uwave{O}}','structural sheaf letter',count=s.count(r'\mathcal O'),why='Short wavy O underline; the complete coefficient ring O remains plain.')
 s,_,_=page_text(rel,387)
 r(r'\mathcal J',r'\mathfrak J','ideal-of-definition letter',count=s.count(r'\mathcal J'),why='Handwritten Gothic J, matching formal X; not calligraphic J.')
 if tree=='fr':
  r('Le paragraphe 1, proposition','Le paragraphe A, proposition','section identifier in lifting reference',kind='misprint of the original',why='The scan prints 1. Proposition 5,2 is in part A, subsection 5 (page 376); subsection 1 contains Proposition 1,1 and no 5,2. The referenced lifting criterion uniquely identifies A.')
 upright_page(rel,layer,'195-387')

event('195-C4-abelian-multiplication','carried as background without fault found','The uniqueness and associativity/commutativity of a multiplication with unit on the proper smooth geometrically connected family use a rigidity theorem. The existence of that multiplication on a deformation uses the announced obstruction argument and Serre\'s argument, followed by formal existence and descent for the general base. These are substantive inputs; no independent proof of this chain has been completed here. The assumptions are read with the proper smooth family of the preceding paragraph. The historical smoothness question is preserved; its later author answer is not inserted into the exposé.','195, pp. 386–387, multiplication and lifting discussion')
event('195-C4-forget-abelian-law','targeted proof check','Conditional on existence and uniqueness of the group law for a pointed deformation, forgetting the origin induces a bijection on deformation classes. Smoothness lifts the original point to a section over an Artinian thickening; two choices differ by translation in the resulting abelian scheme, and the translation reduces to the identity on the marked special fibre. Conversely an isomorphism of unpointed deformations becomes origin-preserving after composing with the unique appropriate translation, hence respects the unique group law. This checks the comparison of class functors, while retaining group-law existence as an explicit input.','195, p. 387, Cela prouve que le foncteur')
event('195-C4-cotangent-relative','refuted, with the refined statement\'s id','Refined statement id: 195-C4-relative-cotangent. Over a general local coefficient ring Lambda with maximal ideal n, the tangent functor uses Lambda-linear derivations, whose dual is m/(m^2+nO), not necessarily m/m^2. An explicit zero-dimensional abelian variety is the one-point group. Its deformation functor is constant, represented by O=Lambda when Lambda=k[[s]], but m/m^2 has dimension one while n^2 in the printed dimension claim is zero. Thus the absolute-cotangent assertion fails for the stated general coefficient ring. It is a substantive qualification, not silently rewritten as a typography correction; both French layers retain the printed m/m^2.','195, p. 387, cotangent and n-squared dimension assertion')
event('195-C4-relative-cotangent','targeted proof check','A local Lambda-algebra map O to k[epsilon] reducing to the residue map differs from it by a derivation killing the image of Lambda. Such derivations are exactly the k-linear dual of m/(m^2+nO). For an abelian variety of dimension n, translation identifies T with O tensor Lie(X_0); using h^1(O)=n gives h^1(T)=n^2. The equality h^1(O)=n is a standard abelian-variety input not independently reproved here. If Lambda=k, the relative cotangent quotient reduces to m/m^2. A power-series description over a noncomplete Lambda must also use its completion.','195, p. 387, relative form of the cotangent assertion')
event('195-C4-lifting-reference','targeted proof check','The printed reference Le paragraphe 1, proposition 5,2 points to the formal smoothness lifting criterion of part A, subsection 5, page 376. Subsection 1 has no Proposition 5,2. Corrected the section identifier to A while preserving 1 in the printed layer. The criterion is used with nilpotent Artinian lifting maps; the unrestricted-surjection issue already recorded for A.5,2 is not erased. The characteristic-zero and Witt-vector reductions remain announced background arguments, not completed independent proofs here.','195, p. 387, reference to Proposition 5,2')
event('195-C5-density-hypothesis','refuted, with the refined statement\'s id','Refined statement id: 195-C5-levelwise-density. A non-zero-divisor on a formal scheme need not define the claimed schematically dense open. On Spf(k[[t]]) with ideal of definition (t), t is a non-zero-divisor but its nonvanishing open is empty. Therefore the stated implication to injectivity of restriction of functions fails. The later author condition that the section be a non-zero-divisor on every X_n addresses this defect and is kept in its own erratum text. The present exposé restores the weaker printed wording in both layers.','195, p. 387, section 5 first sentence')
event('195-C5-levelwise-density','targeted proof check','If a local defining section is a non-zero-divisor on every O_X_n, a section vanishing after localization is killed by a power of it and hence is zero on every level. Passing to the separated complete inverse limit gives injectivity on formal functions. This verifies the density consequence under the stronger levelwise condition.','195, p. 387, refined density condition for the notes')
event('195-C5-Hom-injectivity','targeted proof check','Assume the stated injectivity of O_X to its restriction on U, or the stronger levelwise condition just checked. On U, finite locally free unramified covers are etale. Two maps agreeing on the closed fibre agree on every nilpotent thickening over U by formal unramifiedness, hence agree on the formal restriction to U. The source algebra is locally free over O_X, so restriction to U remains injective for it. The two pullback maps on the target algebra consequently agree everywhere. This proves the displayed Hom injectivity and the automorphism consequence under the density hypothesis. The bare non-zero-divisor assertion alone does not establish that hypothesis.','195, p. 387, displayed Hom map and conclusion')
record_page('195',387,r'''Compared sources/fr_printed/fr/195.tex entry lines 884–945 and sources/fr/fr/195.tex entry lines 885–946 with scan leaf 20 at 400 dpi, full page and all three enlarged bands. Checked the cotangent square and n-squared exponents, the printed section reference 1, the two nested formal-thickening indices, both Hom bases and primes, and the precise open-subset hypothesis.

Both layers remove the unprinted smoothness/covering erratum footnotes and the merged requirement on all X_n. They restore SERRE capitals, unaccented A, the parenthesis punctuation, the numeral 0, comma numbering, literal quotation marks, missing hyphen distinctions, inline X_n definition, selective emphasis, Gothic G/J, wavy structural O and upright letters. The corrected layer changes the unambiguous section reference 1 to A; the printed layer retains 1. The printed absolute quotient m/m^2 remains in both layers, with its mathematical qualification recorded separately rather than silently expanded.

Checked the comparison of pointed and unpointed deformation classes conditional on the group-law theorem; kept the rigidity/existence chain as named background. Recorded a one-point abelian example refuting the absolute-cotangent claim over a general coefficient ring and derived the relative quotient. Checked the lifting reference against page 376. At the start of section 5, a formal-disc example refutes the claimed density consequence of the weaker printed hypothesis; proved the consequence under the later levelwise condition and proved Hom injectivity under actual schematic density.''')
from update_record_counts import update
update()
