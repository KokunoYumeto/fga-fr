from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/182.tex'
 def r(a,b,line,statement='',kind='reading',why='',count=1,full=False):
  replace(rel,a,b,layer,'182-219',line,statement,'400-dpi full scan and all three enlarged bands. '+why,kind,count=count,full=full)
 s=read(rel);a=s.index('des trois points »');b=s.index('\\src{220}')+len('\\src{220}');old=s[a:b];new='\\src{220}\n'+old.replace('\\src{220}','').rstrip()+'\n'
 r(old,new,'page boundary inside the three-points quotation','8',kind='structure',why='The page ends after Problème; des trois points begins page 220.',full=True)
 r('surjectif du\nthéorème 12, corollaire 2, est un isomorphisme.',r'\uline{surjectif du'+ '\n'+r'théorème 12, corollaire} 2, \uline{est un} isomorphisme.','first line','8-thm13',why='The reference numeral 12 is underlined with its prose, numeral 2 and isomorphisme are plain.')
 r(r'\kappa',r'\varkappa','Corollary 1 and characteristic-zero consequence','8-thm13-cor1',why='Crossed kappa is used in both occurrences.',count=2)
 if tree=='fr_printed':
  r('est de caractéristique nulle','est caractéristique nulle','characteristic-zero consequence','8-thm13-cor1',why='The print omits de; corrected French retains the preposition needed for the field to be of characteristic zero.')
 r(r"soit $\pi_1^t(Z')$",r"soit $\pi_1^t(\overline Z')$",'definition of the tame group','8-thm14',why='The Z-prime argument of the first tame group carries an overbar in the scan.')
 r(r"non ramifiés de $Z'$",r"non ramifiés de $\overline Z'$",'definition of the tame covers','8-thm14',why='The covering schemes in this phrase are over geometric Z-bar-prime.')
 if tree=='fr':
  r(r"$\pi_1(Z')$ qui",r"$\pi_1(\overline Z')$ qui",'ambient fundamental group in the tame definition','8-thm14',kind='misprint of the original',why='The printed ambient group omits the geometric bar. The quotient being defined is pi_1^t(Z-bar-prime), and the immediately following covers are of Z-bar-prime, so its ambient group must be pi_1(Z-bar-prime).')
 r('« tamely ramified »',r'\fquote{tamely ramified}','tame definition','8-thm14',why='Ordinary double quotation marks.')
 r(r'\widetilde\pi',r'\overline\pi','prime-to-p tame quotient map','8-thm14',why='The quotient mark is an overbar, agreeing with the definition on page 218.',count=2)
 for old in [r'''\[
  \pi_1^t(\overline X'_1)\longrightarrow\pi_1^t(\overline X'_0),
\]''',r'''\[
  \overline\pi_1^t(\overline X'_1)
  \longrightarrow\overline\pi_1^t(\overline X'_0)
\]''']:
  expr=old[2:-2].strip();punct=',' if expr.endswith(',') else '';expr=expr.rstrip(',')
  r(old,'$'+expr+'$'+punct,'specialization formulas in Theorem 14','8-thm14',kind='structure',why='Both homomorphisms run in the statement prose rather than in separate displays.')
 r(r'\sigma_1\cdots\sigma_n=1,',r'\sigma_1\cdots\sigma_n=1','surface relation','8-thm14-cor',why='The displayed relation has no terminal comma.')
 r(r'$x_i,y_i,\sigma_j$ satisfaisant',r'$\overline x_i,\overline y_i,\overline\sigma_j$ satisfaisant','finite-group realization clause','8-thm14-cor',why='All three elements of the finite group have overbars in the scan; they are images of the preceding topological generators.')
 r(r'les\n$\sigma_j$.',r'les\n$\overline\sigma_j$.','last inertia clause','8-thm14-cor',why='The final inertia generator is barred.') if False else None
 r('les\n$\\sigma_j$.','les\n$\\overline\\sigma_j$.','last inertia clause','8-thm14-cor',why='The final inertia generator is barred.')
 r(r'\le ',r'\leqslant ','index ranges','8-thm14-cor',why='Slanted less-than-or-equal signs in the three ranges.',count=6)
 for marker,sid in [(r'\result{COROLLAIRE}{1} ','8-thm13-cor1'),(r'\result{THÉORÈME}{14} ','8-thm14')]:
  txt,_,_=page_text(rel,219);a=txt.index(marker)+len(marker);b=txt.index('\n\n',a);old=txt[a:b]
  parts=re.split(r'(\(défini à un.*?\)|\\fquote\{tamely ramified\})',old,flags=re.S)
  new=''.join(x if i%2 else underline_prose(x) for i,x in enumerate(parts))
  new=new.replace(r'\fquote{tamely ramified}',r'\uline{\fquote{tamely ramified}}')
  if sid=='8-thm14':new=new.replace('homomorphisme surjectif}',r'homomorphisme} surjectif')
  r(old,new,'statement prose',sid,why='Restore selective underlining. Theorem 14 leaves surjectif and the inner-automorphism aside plain.')
 txt,_,_=page_text(rel,219);marker=r'\result{COROLLAIRE}{} ';a=txt.index(marker)+len(marker);b=txt.index('\n\nLorsque',a);old=txt[a:b]
 parts=re.split(r'(\\\[.*?\\\])',old,flags=re.S)
 new=''.join(x if i%2 else underline_prose(x) for i,x in enumerate(parts))
 new=new.replace(r'\uline{et} $\sigma_j$',r'et $\sigma_j$')
 new=new.replace(r"\uline{d'ordre premier à la caractéristique,"+ '\n'+r'engendré par des éléments}',"d'ordre premier à la caractéristique,\n"+r'\uline{engendré par des éléments}')
 r(old,new,'unnumbered corollary prose','8-thm14-cor',why='Restore statement underlining, leaving et before sigma and the finite-group prime-to-characteristic qualifier plain.')
 r('« Problème\n\\src{220}\ndes trois points »',r'\fquote{\uline{Problème}'+ '\n'+r'\src{220}'+ '\n'+r'des trois points}', 'three-points quotation','8',why='Ordinary quotation marks; Problème is underlined on this page. The continuation is checked on the next page.',full=True)
 upright_page(rel,layer,'182-219')
event('182-8-thm13','targeted proof check','Completing the deduction from page 218: specialization is surjective by Theorem 12 Corollary 2; every finite Galois quotient of prime-to-p order on the geometric generic fiber extends after finite base change by the tame step and Corollary 5. Hence no nontrivial element of the kernel survives in any finite prime-to-p quotient. Together with the universal description of the barred quotient, this proves the asserted isomorphism conditional on the cited specialization, purity, tame and descent inputs. In residue characteristic zero the same unramified-extension argument applies to every finite cover; no pro-0 Sylow terminology is needed.','182, pp. 218–219, Theorem 13')
event('182-8-thm13-cor1','targeted proof check','A continuous isomorphism of the maximal prime-to-p fundamental groups identifies their finite quotient representations, hence the Galois covers with group order prime to p. This is the Galois-category interpretation of Theorem 13. The characteristic-zero sentence has a grammatical omission of de in the print, restored only in corrected French.','182, p. 219, Corollary 1 and following paragraph')
event('182-8-thm14-geometric-bar','targeted proof check','The print defines pi_1^t(Z-bar-prime) and explicitly classifies covers of Z-bar-prime, but names its ambient group as pi_1(Z-prime). Corrected French adds the missing bar on that ambient group. Without it the phrase treats a geometric tame group as an arithmetic tame quotient, and arithmetic constant-field covers need not be removed. All other printed geometric bars are restored in both French layers.','182, p. 219, Theorem 14 definition')
event('182-8-thm14','carried as background without fault found','Read the tame specialization theorem for a smooth proper family with a smooth relative divisor. A proof must extend the formal lifting and purity argument to covers tamely ramified along the horizontal divisor, control the inertia by local Kummer charts/Abhyankar’s lemma, construct specialization compatibly with geometric basepoints, and establish prime-to-p invariance. These extensions are announced rather than proved in the exposé and are not independently established here.','182, p. 219, Theorem 14')
event('182-8-thm14-cor','targeted proof check','Conditional group-theoretic deduction checked: a smooth pointed curve lifts, and characteristic-zero comparison supplies the surface relation with puncture loops. The tame specialization surjection preserves the generators and their relation; prime-to-p invariance realizes every finite prime-to-p quotient specified by barred generators satisfying that relation. Inertia is generated by the images of the puncture loops, explaining the printed bars in the finite-group clause. Lifting marked points, comparison with topology and the inertia-compatible version of Theorem 14 are background inputs; no complete presentation in arbitrary characteristic is asserted by the first sentence. The genus g is inherited from the curve convention of the preceding corollaries.','182, p. 219, unnumbered corollary')
record_page('182',219,r'''Compared sources/fr_printed/fr/182.tex and sources/fr/fr/182.tex entry lines 1260–1320 with scan leaf 28 at 400 dpi and all three enlarged bands. Read the end of Theorem 13, Corollary 1, Theorem 14 and its unnumbered corollary through the start of the three-points remark. Moved the next-page marker inside the quotation after Problème.

Restored crossed kappa, the quotient overbars, the two missing geometric Z-prime bars, the three barred finite-group generators and the final barred inertia generator, slanted inequalities, the unpunctuated surface relation, selective underlining, ordinary quotation marks and both inline Theorem 14 homomorphisms. Printed French restores the omitted de in est caractéristique nulle as an omission; corrected French retains de. Newly corrected only in corrected French: the ambient fundamental group in the geometric tame definition needs the bar on Z-prime, because the defined quotient and its covers are geometric. Theorem 13’s conditional deduction and the corollaries’ group-theoretic consequences are recorded separately from the unproved tame-family background needed for Theorem 14.''')
p='CHECK_RECORD.md';t=read(p).replace('## Open reading questions','- 182-219, Theorem 14: added the missing geometric bar in the ambient pi_1(Z-prime) of the tame definition; its quotient and classified covers are of geometric Z-bar-prime.\n- 182-219, characteristic-zero consequence: retained de in corrected French; the print omits it.\n\n## Open reading questions');write(p,t)
from update_record_counts import update
update()
