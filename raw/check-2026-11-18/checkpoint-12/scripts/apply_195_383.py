from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/195.tex'
 def r(a,b,line,kind='reading',why='',count=1,full=False):
  replace(rel,a,b,layer,'195-383',line,'C.2–3','400-dpi full scan and all three enlarged bands. '+why,kind,count=count,full=full)
 r('\\src{384}\n','', 'page boundary, old position',kind='structure',why='Page 383 ends with sont les fibres; the existing marker is too late.',full=True)
 r(r'fibres de $\underline P(X/S)$.', 'fibres\n\\src{384}\nde $\\underline P(X/S)$.','page boundary, new position',kind='structure',why='Page 384 begins with de P(X/S), after fibres.',full=True)
 s,_,_=page_text(rel,383)
 notes=list(footnotes(s))
 assert len(notes)==2
 for a,b,n in reversed(notes):
  r(s[a:b],'','editorial footnote after '+('quasi-projectivity' if 'Nagata' in n else 'opening S-prescheme'),kind='structure',why='This 1962 erratum commentary is absent from the exposé scan; the author errata remain in their own sections.')
 r('topologique $O$ correspondant sont','topologique $O$ correspondants sont','quotient paragraph, agreement',why='The scan prints correspondants; it can agree with composants, so both layers retain it.')
 r('« $S$-algèbres artiniennes »',r'\fquote{$S$-algèbres artiniennes}','Artinian-algebra quotation',why='Literal S, and ordinary double quotes.')
 r('« schéma de Chow »',r'\fquote{schéma de Chow}','Chow quotation',why='Ordinary double quotation marks.')
 r('qui soient de type fini (','qui soient de \\uline{type fini} (','finite-type emphasis',why='Only this type fini is underlined, not the following localement de type fini.')
 r('est même projectif ou','est même \\uline{projectif} ou','projectivity emphasis',why='Only projectif is underlined.')
 r('quasi projectif sur','quasi-projectif sur','quasi-projectif hyphen',why='The scan prints a hyphen.')
 r(r'\subsection*{3. Schémas de Picard}',r'\subsection*{\textnormal{3. \uline{Schémas de Picard}.}}','section heading',kind='typesetting',why='Roman heading; words underlined; final period.')
 s,_,_=page_text(rel,383)
 r(r'\mathcal O',r'\text{\uwave{O}}','structural sheaf letter',count=s.count(r'\mathcal O'),why='O has a wavy underline.')
 r(r'P(X/S)=H^0\bigl(S,R^1f_*(\text{\uwave{O}}_X^*)\bigr),',r'P(X/S)=H^0(S,R^1f_*(\text{\uwave{O}}_X^*))','relative Picard display typography',kind='typesetting',why='Ordinary-size parentheses, no terminal comma; the units star is separately adjudicated.')
 r('appelé groupe de Picard relatif','appelé \\uline{groupe de Picard relatif}','definition emphasis',why='These four words are underlined.')
 s,_,_=page_text(rel,383)
 r('L_i',r'\text{\uwave{L}}_i','invertible sheaf i',count=s.count('L_i'),why='L has a wavy underline.')
 r('L_j',r'\text{\uwave{L}}_j','invertible sheaf j',why='L has a wavy underline.')
 r('de telle façon que, pour','de telle façon que pour','compatibility clause punctuation',why='No comma follows que.')
 r('(i.e. ces deux faisceaux sont « équivalents » au sens de [3], B, 4).','(i. e. ces deux faisceaux sont \\fquote{équivalents} au sens de [3], B, 4.).','equivalence parenthesis',why='Spaced i. e., ordinary quotes, and a period before as well as after the closing parenthesis.')
 r('à « équivalence » près',r'à \fquote{équivalence} près','equivalence quotation',why='Ordinary double quotation marks.')
 r('maintenant, pour tout $T$ sur $S$,','maintenant, pour tout $T$ sur $S$ :','functor definition introduction',why='Printed colon.')
 r('F(T)=P(X_T/T) ;','F(T)=P(X_T/T)','functor definition display',why='No printed semicolon.')
 r('le foncteur de\nPicard de','le \\uline{foncteur de\nPicard} de','Picard functor emphasis',why='Only foncteur de Picard is underlined.')
 r('appelé le pré-schéma de Picard de','appelé le \\uline{pré-schéma de Picard} de','Picard prescheme emphasis',why='Only pré-schéma de Picard is underlined.')
 s,_,_=page_text(rel,383)
 r(r'\underline P',r'\text{\uwave{P}}','representing Picard letter',count=s.count(r'\underline P'),why='Wavy, not straight, underline.')
 r('un isomorphisme de foncteurs\n','un isomorphisme de foncteurs :\n','universality introduction',why='Printed colon.')
 r(r'\operatorname{Hom}_S\bigl(T,\text{\uwave{P}}(X/S)\bigr)',r'\operatorname{Hom}_S(T,\text{\uwave{P}}(X/S))','universality parentheses',kind='typesetting',why='Ordinary-size printed parentheses; Hom itself is not underlined.')
 r('base, en particulier les','base, en particulier, les','base-change paragraph punctuation',why='Printed comma follows particulier.')
 if tree=='fr_printed':
  r('lorsque $G$ est de plus cohérent','lorsque $F$ est de plus cohérent','first coherence hypothesis',why='The printed letter is F.')
  r('et $G$ cohérent,','et $F$ cohérent,','second coherence hypothesis',why='The printed letter is F.')
  r(r'R^1f_*(\text{\uwave{O}}_X^*)',r'R^1f_*(\text{\uwave{O}}_X)','relative Picard display, units star',why='No superscript star is printed on this O_X, although the preceding definition uses units.')
  r('un foncteur contravariant en','un foncteur covariant en','variance word',why='The scan unambiguously prints covariant.')
 upright_page(rel,layer,'195-383')

with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 for line in ['first coherence hypothesis','second coherence hypothesis']:
  w.writerow(['sources/fr/fr/195.tex','French corrected','195-383',line,'C.2 quotient-sheaf functor','F','G','The scan prints F, the set-valued quotient functor. Coherence is a property of the fixed quasi-coherent sheaf G introduced on page 382, not of that functor. Existing corrected G confirmed.','misprint of the original','low'])
 w.writerow(['sources/fr/fr/195.tex','French corrected','195-383','relative Picard display, units star','C.3 definition of P(X/S)',r'R^1f_*(\text{\uwave{O}}_X)',r'R^1f_*(\text{\uwave{O}}_X^*)','The enlarged display omits the star. The immediately preceding sentence specifies the multiplicative sheaf of units and the following sentence classifies invertible sheaves. R^1 of the additive structural sheaf instead describes additive cohomology. Existing units star confirmed.','misprint of the original','low'])
 w.writerow(['sources/fr/fr/195.tex','French corrected','195-383','variance word','C.3 Picard functor','covariant','contravariant','The scan prints covariant en T. A map T-prime to T pulls an invertible sheaf on X_T back to X_T-prime; the induced map is F(T) to F(T-prime). The displayed Hom_S(T,P) has the same contravariance. Existing correction confirmed.','misprint of the original','low'])
event('195-C2-quotient-formal','carried as background without fault found','The asserted pro-representability for flat quotients is read as an application of B.1 and the flat-module descent statement B.2. No independent proof of that general descent theorem is claimed. The preceding global existence sentence says Il semble and is retained as a historical expectation; its later author amendment is kept separate. The two coherence hypotheses concern G, while F denotes the quotient functor.','195, p. 383, first paragraph')
event('195-C2-quotient-tangent-finiteness','targeted proof check','At a quotient G_K to Q with kernel N, a first-order flat quotient is locally the graph of a map N to Q, and these maps glue to Hom_X_K(N,Q). On the noetherian proper X_K with G_K coherent, both N and Q are coherent, hence the sheaf Hom(N,Q) is coherent. Proper coherent H^0 finiteness makes this tangent space finite-dimensional. Conditional on the stated pro-representability and A.5,1, the local representing components are noetherian. The general flat-module descent input and the complete-local noetherian criterion are not independently reproved here.','195, p. 383, noetherian local components')
event('195-C3-Picard-definition','targeted proof check','R^1 f_* of the multiplicative units sheaf is locally represented by invertible sheaf classes. Its H^0 consists of local representatives agreeing as such classes after further localization on the base, exactly as the paragraph describes. The missing units star changes the group to additive cohomology and is a misprint. Pullback gives contravariance in T. If the functor is represented, base change follows by evaluating on any S-prime-scheme T: X_S-prime times_S-prime T equals X times_S T; Yoneda identifies the representing base change and its fibres. This argument does not assert an unrestricted cohomology base-change theorem for R^1 f_*.','195, p. 383, section 3 definition and last paragraph')
event('195-C3-section-global-classes','carried as background without fault found','The assertion that a section suffices to replace local relative Picard classes by global invertible sheaves needs its descent argument. Under the additional universal equality f_*O_X=O_S used on the next page, rigidification along the section kills the remaining scalar automorphisms and gives the expected argument. No unrestricted proof using a section alone has been established in this check; the printed statement is retained, with the missing proof/possible hypotheses left for the notes rather than an unsupported textual alteration.','195, p. 383, Si X/S admet une section')
record_page('195',383,r'''Compared sources/fr_printed/fr/195.tex entry lines 689–764 and sources/fr/fr/195.tex entry lines 690–765 with scan leaf 16 at 400 dpi, full page and all three enlarged bands. The source interval initially ran into page 384; moved that marker to the scan boundary immediately after sont les fibres, before de P(X/S). Checked each coherence letter, the absent units star, all R/H exponents and restrictions, the wavy sheaf and representing letters, and the variance word.

Both layers remove two unprinted editorial footnotes that had merged later author material, restore literal punctuation, ordinary quotation marks, hyphenation, selective emphasis, upright mathematical letters and wavy O/L/P. The printed plural correspondants is retained in both layers because it can agree with composants. Printed French restores the two F readings, absent units star, and covariant. Corrected French retains G at both hypotheses, O_X^* in the defining cohomology, and contravariant; each has an explicit misprint row.

Checked finite tangent dimension for coherent quotients on a proper scheme, conditional on the announced formal representability inputs. Checked the relative Picard sheaf description, contravariance and represented-functor base change. The global quotient-scheme existence expectation and the section-only global line-bundle assertion are not presented as independently proved; the latter needs a descent argument or further hypotheses, and is flagged for the notes without rewriting the historical text.''')
from update_record_counts import update
update()
