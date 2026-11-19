from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1,full=False):
  replace(rel,a,b,layer,'182-203',line,statement,'400-dpi scan, all three enlarged bands and the tight local-punctuation crop. '+why,kind,count=count,full=full)
 # The ending quotation crosses the printed-page boundary.
 r('« variations de structure »',r'\fquote{variations de structure}','last line','6',why='The quotation uses ordinary double quotes.')
 r('\\src{204}\n\\result{THÉORÈME}{8}',r'\result{THÉORÈME}{8}','page boundary','6','structure','The source marker was too late; the printed boundary precedes structure in the closing quotation.',full=True)
 r(r'\fquote{variations de structure}', '\\fquote{variations de\n\\src{204}\nstructure}','last line','6','structure','Move the page-204 marker to the actual continuation within the quoted phrase; the rest is reserved for page 204.',full=True)
 txt,_,_=page_text(rel,203)
 r(r'\Osh','O','structure sheaves','5/6',why='O is plain throughout this page.',count=txt.count(r'\Osh'))
 if tree=='fr_printed':
  r('O_Y','O_X','initial sheaf sequence and explanation','5-prop2-cor',why='All three unit-sheaf subscripts are X in the print. Corrected French retains Y because E, its automorphism sheaf and the scalar kernel are on the base Y.',count=3)
  r('local, séparé',"local', séparé",'section 6 opening paragraph','6',why='The tight crop confirms a stray apostrophe following local, before the comma; corrected French omits it.')
  r("$F_0$. Cet $F$ est\nd'ailleurs", "$F_0$. Cet $F$\nd'ailleurs",'Corollary 1, uniqueness sentence','6-prop3-cor1',why='The print omits est here. Corrected French retains it to complete the sentence.')
 r(r'\underline{\operatorname{Aut}}',r'\mathop{\text{\uwave{Aut}}}\nolimits','initial sequence and explanation','5-prop2-cor',why='All three Aut sheaves have wavy underlining.',count=3)
 r('\\longrightarrow e,\n\\]','\\longrightarrow e\n\\]','initial display','5-prop2-cor',why='No comma follows the terminal e.')
 for phrase in ['unités','algébrique']:
  r('« '+phrase+' »',r'\fquote{'+phrase+'}','quoted word','6',why='The scan has ordinary double quotes.')
 r('« théorie des modules »',r'\fquote{\uline{théorie des modules}}','last line','6',why='The phrase is underlined inside its ordinary double quotes.')
 r(r'''\fsection{6}{Application à des théorèmes d'existence et d'unicité pour des
faisceaux et schémas sur un anneau $J$-adique complet}''',r'''\fsection{\normalfont6}{\normalfont\uline{Application à des théorèmes d'existence et d'unicité pour des
faisceaux et schémas sur un anneau} $J$\uline{-adique complet}.}''','section title','6',why='The heading is roman and underlined except the mathematical J, with a final period.')
 for old,new in [("des théorèmes d'existence de faisceaux",r"des théorèmes \uline{d'existence} de faisceaux"),('séparé et complet.',r'séparé et \uline{complet}.'),('constructions formelles,',r'constructions \uline{formelles},'),('géométrie algébrique sur un anneau artinien',r'\uline{géométrie algébrique sur un anneau artinien}'),('$X_0$ simple','$X_0$ \\uline{simple}'),('entendons absolument simple',r'entendons \uline{absolument} simple')]:
  r(old,new,'local prose emphasis','6',why='Restore the specific underlined word or phrase shown in the scan.')
 txt,_,_=page_text(rel,203)
 r(r'\Homsh',r'\mathop{\text{\uwave{Hom}}}\nolimits','Proposition 3, proof and Corollary 1','6-prop3',why='All four Hom occurrences have wavy underlining.',count=txt.count(r'\Homsh'))
 r('=0$.)','=0$).','Proposition 3 parenthesis','6-prop3',why='The period follows the closing parenthesis.')
 txt,_,_=page_text(rel,203)
 for m in list(re.finditer(r'\\\[\s*(H\^2.*?)\s*\\\]',txt,re.S)):
  old=m.group(0);expr=m.group(1).strip().replace('\n  ',' ');punct=expr[-1];expr=expr[:-1]
  r(old,'$'+expr+'$'+punct,'vanishing and obstruction formulas','6-prop3','structure','Both formulas are inline in the original.')
 txt,_,_=page_text(rel,203);marker=r'\result{PROPOSITION}{3} ';a=txt.index(marker)+len(marker);b=txt.index(' (Cet ',a);old=txt[a:b]
 r(old,underline_prose(old),'Proposition 3 statement','6-prop3',why='The main statement prose is underlined; its uniqueness parenthesis is not.')
 txt,_,_=page_text(rel,203);marker=r'\result{COROLLAIRE}{1} ';a=txt.index(marker)+len(marker);b=txt.index('\n\n',a);old=txt[a:b]
 r(old,underline_prose(old),'Corollary 1 statement','6-prop3-cor1',why='The entire statement prose is underlined, excluding the mathematical letters.')
 upright_page(rel,layer,'182-203')
event('182-5-prop2-sheaf-sequence','targeted proof check','The sheaf sequence lives on Y: scalar units O_Y^* are the center of Aut(E), and projective automorphisms lift locally to linear automorphisms. All three printed O_X subscripts are restored only in printed French; corrected French retains Y. This matches the global sections sequence on page 202.','182, p. 203, initial display and following line')
event('182-6-prop3','targeted proof check','Checked the obstruction argument for one square-zero thickening: lift local trivializations and transition matrices; triple-overlap defects form a 2-cocycle in End(F_0) tensor J^n/J^(n+1), and changing overlap lifts adds a coboundary. H^2 vanishing removes it. H^1 vanishing similarly supplies compatible isomorphisms at successive stages. The inverse system gives a locally free formal sheaf. This is a targeted reconstruction of the stated induction, not a new proof of the formal comparison theorems.','182, p. 203, Proposition 3 and proof')
event('182-6-prop3-cor1','targeted proof check','Theorem 3 algebraizes the formal coherent sheaf and identifies morphisms. Local freeness holds near the special fiber by faithful completion and Nakayama; its closed failure locus is empty because properness over the local base makes every nonempty closed image meet the closed point. The same comparison gives the uniqueness assertion. The omitted est is retained in corrected French.','182, p. 203, Corollary 1')
record_page('182',203,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 487–560 with scan leaf 12 at 400 dpi, full page and all three enlarged bands; additionally viewed the tight crop confirming local followed by a stray apostrophe. The actual page ends within variations de structure; moved marker 204 before structure and did not treat the following source text as read against this page.

Restored plain O, wavy underlines on Aut and Hom, the section heading and local prose emphasis, ordinary double quotes, inline vanishing and obstruction expressions, statement underlining and punctuation. Printed French restores three O_X unit-sheaf subscripts, the stray apostrophe after local, and the missing est in Corollary 1. Corrected French retains the supplied Y subscripts and complete grammar. Reconstructed the square-zero obstruction step and the algebraization deduction as recorded; the underlying comparison theorem remains background.''')
from update_record_counts import update
update()
