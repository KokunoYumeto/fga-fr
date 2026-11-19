# FGA_CHECK: the run's last message (environment failure, 18 Nov 2026 21:44 UTC)

Pasted by the user into the main session, 18 Nov ~22:4x UTC; kept verbatim. GPT-6 Astra (ChatGPT Pro mode). The newest checkpoint we hold is FGA_CHECK_checkpoint_05 (20:36 UTC, through 212-116); apply_221_266.py below was applied in the lost workspace, apply_221_267.py was not.

---

The audit remains incomplete because the execution environment failed. I retried for more than the required ten minutes, then attempted restoration from the latest saved checkpoint. The restore service returned the checkpoint and its expected checksum, but commands, file edits, image reads, and uploading the current ledger still failed with **“No usable execution environment is available.”** The last retry failed at **21:44:31 UTC on 18 November 2026**.

I could not create or make **`FGA_CHECK.zip`** available.

### Exact state at the interruption

| Work | State |
|---|---|
| French page checks, exposés 149, 182, 190, 195 and 212 | Applied and recorded |
| French page checks, exposé 221, pages 249–266 | Applied and recorded |
| Total French pages applied and recorded | **142** |
| Exposé 221, page 267 | Both source layers and the full scan plus all enlarged bands read; edit script drafted, **not applied** |
| Remaining French pages and supplements | Not completed |
| Translations and their diplomatic layers | Not begun |
| Second reading of every correction row | Not begun |
| Final builds, PDF inspection and notes | Not begun |

The latest successful durable save is **`FGA_CHECK_checkpoint_05.zip`**, saved at **20:36:13 UTC**, containing the work through **212–116**. Its SHA-256 is:

```text
4fb2dc9f455390aa15e28d92edbd2a03b9baf40c542879cf4ff52ea3736dc107
```

The twenty completed pages after that checkpoint—**212–117, 212–118 and 221–249 through 221–266**—were written successfully to the workspace, but their subsequent checkpoint was blocked by the outage. Checkpoint 06 was due at 21:33:19 UTC and was **not saved**.

Your fallback requires the complete ledgers and changed source files in chat. I cannot reproduce those files faithfully from the currently accessible data: the workspace cannot be read, and the remaining file service returns no readable text for the checkpoint ZIP. Earlier portions of this conversation are available to me as a summary rather than verbatim file contents. Reconstructing those thousands of rows as though they were the actual files would introduce invented records.

Below are the **complete recent edit scripts whose exact contents remain available**. The first was applied successfully; the second remains unapplied. They preserve concrete work from this part of the audit, but they do not replace the unavailable complete ledgers and source trees.

## `scripts/apply_221_266.py` — applied successfully

```python
from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/221.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'221-266',line,'3.9; 4 a','400-dpi full page and all three enlarged bands. '+why,kind,count=count)
 r("l'anneau de Chow des classes",r"\uline{l'anneau de Chow} des classes",'opening comparison',why='The first ring name has a straight underline.')
 r(", et l'anneau des classes\nde faisceaux",r", et \uline{l'anneau des classes de faisceaux}",'opening comparison',why='The second ring name is also straight-underlined.')
 r('Riemann--Roch','Riemann-Roch','opening reference',why='The printed compound has a single hyphen.')
 s,_,_=page_text(rel,266)
 for a,b,body in list(footnotes(s)):
  if body.startswith("L'erratum de 1962"):
   r(s[a:b],'','3.9, connectedness question',kind='structure',why='The Hartshorne footnote is not on this page. The author erratum remains in its own section.')
 r(r'\underline{\operatorname{Quot}}',r'\text{\uwave{Quot}}','4 a, Quot functor',why='The functor name has a wavy underline.')
 if tree=='fr_printed':
  r(r'\operatorname{Quot}^{P}_{(',r'\operatorname{Quot}_{(','3.9, first display right side',why='No P superscript is printed on the right-side Quot; preserve the omission here.')
 s,_,_=page_text(rel,266)
 r(r'\operatorname{Quot}',r'\underline{\operatorname{Quot}}','six representing Quot names',count=s.count(r'\operatorname{Quot}'),why='The representing scheme names all have straight underlines.')
 r(r'\operatorname{Hilb}',r'\underline{\operatorname{Hilb}}','two representing Hilbert names',count=2,why='Both representing Hilbert names have straight underlines.')
 s,_,_=page_text(rel,266)
 r(r'\mathbf P',r'\mathcal P','five projective-space letters',count=s.count(r'\mathbf P'),why='The handwritten projective P is looped, in the script family, as on the preceding pages.')
 r(r'\mathfrak Q',r'\mathcal Q','two universal-parameter letters',count=2,why='The parameter Q has the handwritten spiral form of script Q; it is not a Gothic letter.')
 r('Serre [7]','SERRE [7]','3.9 literature reference',why='The surname is printed in capitals.')
 r('question de Weil','question de WEIL','3.9 question',why='The surname is printed in capitals.')
 for old,new in [('« régulières »',r'\fquote{régulières}'),('« relativement connexes »',r'\fquote{relativement connexes}'),('« variétés de Chow »',r'\fquote{variétés de Chow}')]:
  r(old,new,'3.9 quoted terminology',why='The print uses ordinary double quotes.')
 r('i.e.','i. e.','3.9 abbreviation',why='The abbreviation is spaced in the print.')
 r(r'\fsection{4}{Variantes}',r'\fsection{\normalfont 4}{\normalfont\uline{Variantes}.}','section 4 heading',why='Only Variantes is straight-underlined; the heading has a final full stop.')
 r(r"S'\longrightarrow S",r"S'\to S",'3.9 base change',why='The inline arrow is short.')
 upright_page(rel,layer,'221-266')

with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 w.writerow(['sources/fr/fr/221.tex','French corrected','221-266','opening comparison','3.9','telle','tel','Canonical correction 0010 confirmed against the enlarged scan: telle is printed, but the subject of il and antecedent of the adjective is the masculine anneau. Existing correction and its explanatory footnote retained.','misprint of the original','low'])
 w.writerow(['sources/fr/fr/221.tex','French corrected','221-266','first display right side','3.9',r'\underline{\operatorname{Quot}}_{(',r'\underline{\operatorname{Quot}}^{P}_{(','The scan has no P on the right-side Quot. The left side and the preceding phrase specify a fixed Hilbert polynomial and a projective scheme; the unrestricted Quot is instead a coproduct over polynomials. Retain the existing P in the corrected formula.','misprint of the original','low'])

event('221-3.9-Chern-classes','refuted, with the refined statement\'s id','Refined statement 221-3.9-rank-and-Chern: the rank together with the Chern classes determines the Hilbert polynomial on projective space. The total Chern classes alone do not: O and O direct-sum O have total class 1 but Hilbert polynomials binomial(n+r,r) and twice that polynomial. This is a qualification of the mathematical assertion, not a silent text emendation.','221, p. 266, opening paragraph')
event('221-3.9-rank-and-Chern','targeted proof check','On projective r-space, the classes O(-i), 0<=i<=r, generate K_0 by finite graded resolutions and the Koszul relation (1-[O(-1)])^(r+1)=0. Their Hilbert polynomials binomial(n+r-i,r) are independent: evaluation at n=0,...,r gives a triangular matrix with diagonal 1. Thus the Hilbert polynomial determines the integral K_0 class and conversely. Finite graded resolutions and the Koszul relation are background inputs; the independence argument was checked here. Rank and Chern classes determine the rational Chern character by Newton identities, and torsion-freeness of this K_0 makes that determination integral.','221, p. 266, opening paragraph')
event('221-3.9-universal-reduction','targeted proof check','Locally on the noetherian base, a twist of the coherent source is a quotient of a finite free sheaf on projective space. Quotients factoring through the source form a closed locus in the free-source Quot scheme. The free-source construction is the base change of its model over Spec Z; twisting shifts the polynomial. This justifies reduction to the displayed universal schemes, with the fixed-polynomial P restored on the right. It is a base-change and closed-locus reduction, not an assertion that an arbitrary-base scheme is itself a closed subscheme over Spec Z without base change.','221, p. 266, remarks 3.9')
event('221-3.9-questions','carried as background without fault found','The connectedness and regular-extension questions are retained as questions. The reference to SERRE [7] for vertical irreducible components is not proved on this page and awaits the exact source check in the notes stage. The later Hartshorne statement has been removed from the exposition and will be read in its own printed erratum.','221, p. 266, final paragraph of remarks 3.9')
event('221-4a-support-open','independent re-proof','Let G be the universal quotient on X times_S Q. Its support intersected with the inverse image of X minus U is closed; properness of X over S makes its image in Q closed. The complement represents exactly the quotients supported in U after every base change: for finitely presented modules, support commutes set-theoretically with base change by the local Nakayama criterion. This proves the asserted open-subfunctor representation.','221, p. 266, section 4 a')
record_page('221',266,r'''Compared sources/fr_printed/fr/221.tex entry lines 811–863 and sources/fr/fr/221.tex entry lines 817–869 with scan leaf 19 at 400 dpi, full page and all three enlarged bands.

Confirmed canonical correction 0010, telle to tel. Restored the two opening underlines, single hyphen in Riemann-Roch, straight-underlined scheme names versus the wavy-underlined Quot functor, handwritten projective P and script Q, capital surnames, ordinary quotes, spaced abbreviation, short arrow, and the section heading. Removed the unprinted Hartshorne footnote from both exposition layers. The printed first display lacks the P superscript on its right side; the corrected formula retains it with an explicit row. The handwritten integer-ring Z is retained as the existing bold-Z approximation, provisionally for the typography second reading.

Checked the Hilbert-polynomial/K_0 comparison and identified the omitted rank qualification in the Chern-class assertion. Checked the universal reduction with its base-change and twisting qualifications. The connectedness questions and SERRE reference are carried as background for later source work. Proved the open support condition by properness of the universal support and Nakayama.''')
from update_record_counts import update
update()
```

## `scripts/apply_221_267.py` — draft, not applied

This script was retained in the conversation’s tool state. It has **not** been run, compiled, or used to append a page-completion record.

```python
from audit_utils import *

for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
 rel=f'sources/{tree}/fr/221.tex'
 def r(a,b,line,kind='reading',why='',count=1):
  replace(rel,a,b,layer,'221-267',line,'4 a–c','400-dpi full page and all three enlarged bands. '+why,kind,count=count)
 r('est quasi-projectif sur',r'est \uline{quasi-projectif} sur','4 a, opening hypothesis',why='The first quasi-projectif is straight-underlined.')
 r('dans les conclusions le mot','dans les conclusions les mots','4 a, replacement wording',why='The print has the plural les mots.')
 r('« projectif »',r'\fquote{projectif}','4 a, first quoted term',why='Ordinary double quotes in the scan.')
 r('« quasi-projectif »',r'\fquote{quasi-projectif}','4 a, second quoted term',why='Ordinary double quotes around the handwritten replacement.')
 r("dont le\nsupport est propre sur $S'$",r"\uline{dont le support est propre sur} $S'$",'4 a, proper support',why='The prose through sur is straight-underlined; S-prime is outside it.')
 r(r'aux quotients $\mathcal G$ de',r'aux quotients $G$ de','4 b, first quotient letter',why='This G is typed plain, unlike the handwritten G in the preceding paragraph.')
 r(r"""\mathcal O_{S'}$, plats sur $S'$,
toutes""",r"""\mathcal O_{S'}$ plats sur $S'$
toutes""",'4 b, opening formula punctuation',why='Neither comma is printed here.')
 if tree=='fr_printed':
  r(r"$\mathcal G_s$ ($s'\in S'$)",r"$G_s$, ($s'\in S'$)",'4 b 1°, module and comma',why='The module is typed G_s, followed by a comma before the parenthesis.')
 else:
  r(r"$\mathcal G_{s'}$ ($s'\in S'$)",r"$G_{s'}$, ($s'\in S'$)",'4 b 1°, module and comma',why='Restore the typed alphabet and comma; retain the justified corrected prime.')
  r(r'Le texte imprimé porte $\mathcal G_s$',r'Le texte imprimé porte $G_s$','4 b 1°, editorial reading note',kind='typesetting',why='The explanatory note now uses the typed alphabet actually visible in the scan.')
 r('préschéma simple\n','préschéma '+r'\uline{simple}'+'\n','4 b 2°, simple',why='The adjective is straight-underlined.')
 r('resp. normal sur',r'resp. \uline{normal} sur','4 b 2°, normal',why='The adjective is straight-underlined.')
 if tree=='fr_printed':
  r('« sur $k(s)$ »',r'\fquote{sur $k(s)$}','4 b 2°, residue-field phrase',why='Ordinary double quotes in the scan.')
 else:
  r("« sur $k(s')$ »",r"\fquote{sur $k(s')$}",'4 b 2°, residue-field phrase',why='Ordinary double quotes; retain the corrected residue-field prime.')
  r(r"sont des $S'$-intersections complètes",r"est une $S'$-intersection complète",'4 b 2°, local complete intersection clause',kind='misprint of the original',why='The subject is the single closed subscheme Y, introduced by Y est. The plural sont des ... complètes breaks that sentence; restore singular agreement while retaining the canonical base correction.')
  r("locales dans $X'$ relativement", "locale dans $X'$ relativement",'4 b 2°, local complete intersection agreement',kind='misprint of the original',why='Singular agreement with the preceding corrected une intersection complète.')
 r('i.e.','i. e.','three explanatory abbreviations',count=3,why='All three abbreviations are spaced.')
 r(r"Modules $\mathcal G_{s'}$ induits",r"Modules $G_{s'}$, induits",'4 b, cohomological conditions',why='Typed G and a comma before induits are visible.')
 r(r'\underline{\operatorname{Quot}}',r'\text{\uwave{Quot}}','two Quot functor names',count=2,why='The functor names are wavy-underlined.')
 r(r'\operatorname{Quot}',r'\underline{\operatorname{Quot}}','two representing Quot names',count=2,why='The representing scheme names have straight underlines.')
 r(r'de $\underline{\operatorname{Quot}}_{\mathcal F/X/S}$ est représentée',r'de $\underline{\operatorname{Quot}}_{\mathcal F/X/S}$, est représentée','4 b, conjunction sentence',why='A comma follows the Quot expression in the print.')
 r(r"""Comme on a
\[
\operatorname{Hom}_S(X,Y)=\Pi_{X/S}((X\times_SY)/X),
\]
le cas""",r"""Comme on a $\operatorname{Hom}_S(X,Y)=\Pi_{X/S}((X\times Y)/X)$, le cas""",'4 c, section-functor identity',kind='structure',why='The identity runs inline and abbreviates the product as X times Y without a printed base subscript.')
 r(r'\Pi_{X/S}',r'\mathop{\Pi}\limits_{X/S}','three section-functor symbols',count=3,why='The X/S index sits below the Pi even in inline occurrences.')
 s,_,_=page_text(rel,267)
 r(r'\operatorname{Hom}',r'\underline{\operatorname{Hom}}','representing Hom names',count=s.count(r'\operatorname{Hom}'),why='Straight underlines distinguish these representing scheme names.')
 r(r'\operatorname{Isom}',r'\underline{\operatorname{Isom}}','representing Isom name',why='The Isom scheme name is straight-underlined.')
 if tree=='fr':
  r("l'identité affichée précédente","l'identité précédente",'4 c, editorial reading note',kind='structure',why='The original identity is inline, so the editorial note must not call it displayed.')
 r(r'\longrightarrow',r'\to','two final arrows',count=2,why='Both printed arrows are short.')
 upright_page(rel,layer,'221-267')

with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
 w=csv.writer(f,delimiter='\t')
 for loc,old,new,why in [
  ('4 b 1°, quantified fibre module','G_s',"G_{s'}",'0011: the scan has s, while the quantified point and the fibre are indexed by s-prime.'),
  ('4 b 2°, residue field','k(s)',"k(s')",'0012: the scan has k(s), but geometric normality of the indicated fibre is over its residue field k(s-prime).'),
  ('4 b 2°, relative intersection base','k', "S'",'0013 composed with 0016: k is not the base of this general family; the relative property is over the test base S-prime.'),
  ('4 b 2°, simple over base','simple sur S',"simple sur S'",'0016, first base occurrence: the family Y is a scheme over the test base S-prime.'),
  ('4 b 2°, normal over base','normal sur S',"normal sur S'",'0016, second base occurrence: fibrewise geometric normality is relative to S-prime.'),
  ('4 b 2°, intersection ambient scheme','dans X',"dans X'",'0016, ambient occurrence: Y is a closed subscheme of X-prime after base change.'),
  ('4 b 2°, relative intersection clause','relativement à S',"relativement à S'",'0016, relative-base occurrence: regular immersion is tested relative to S-prime.'),
  ('4 b 2°, intersection fibre ambient scheme',"X_{s'}","X'_{s'}",'0016, final fibre occurrence: the fibre of the changed ambient scheme is X-prime at s-prime. The sixth semantic operation is the k-to-S-to-S-prime composition recorded separately.'),
  ('4 c, reduction after the identity','Hom_S(X,X)','Hom_S(X,Y)','0014: the stated reduction immediately uses the section functor of X times Y over X, so its target is Y.'),
  ('4 c, graph ambient scheme','Gamma in Z',"Gamma in Z'",'0015: a section over X-prime has graph in Z-prime, not the original Z.')
 ]:
  w.writerow(['sources/fr/fr/221.tex','French corrected','221-267',loc,'4 b–c',old,new,'Canonical correction '+why+' Existing corrected reading retained after direct image verification.','misprint of the original','low'])

event('221-4a-quasiprojective','targeted proof check','Embed the quasi-projective X as an open in a projective closure and extend the coherent source to that closure. A quotient with support proper over the test base extends by zero coherently across the complement: its support maps properly to the separated closure, hence is closed there. The quotient of the extended source is therefore supported in X. Conversely restriction recovers the quotient. The open support locus of p. 266 supplies representability, and its fixed-polynomial pieces are open in projective schemes, hence quasi-projective. Coherent extension over the noetherian closure is a background input.','221, p. 267, opening paragraph')
event('221-4b-open-properties','carried as background without fault found','The claimed openness of restrictions on associated-point dimensions, geometric normality, smoothness (simple), and fibrewise regular immersions uses openness theorems for flat finitely presented proper families. Those theorems are not reproved here. The scan confirms that the six base/object operations of canonical 0016, together with 0011–0013, are needed to formulate the properties on the test family; the original flatness hypothesis on X over S is retained because it implies flatness after base change.','221, p. 267, 1° and 2°')
event('221-4b-conjunction','refuted, with the refined statement\'s id','Refined statement 221-4b-finite-conjunction: a finite conjunction of open conditions is represented by their open intersection. For an arbitrary infinite family the open-intersection claim fails. On Hilb^1(P^1_k)=P^1_k with k algebraically closed, impose for each closed point a the condition that the length-one subscheme avoid a. Each condition is open, whereas their total intersection is the generic point and is not open. The wording is retained; finiteness is an explicit qualification for the notes.','221, p. 267, conjunction sentence')
event('221-4b-finite-conjunction','targeted proof check','For finitely many open subfunctors represented by U_i in Q, a map T to Q factors through all U_i exactly when it factors through their finite intersection. The intersection is open, proving the refined claim.','221, p. 267, conjunction sentence')
event('221-4b-etale-covers','targeted proof check','On the proper flat Hilbert family, the smooth locus is open. Imposing zero-dimensional fibres makes smoothness etaleness; a proper etale morphism is finite etale. Its locally constant rank selects an open-and-closed part of that locus. Thus the stated fixed-rank cover functor is represented, conditional on the openness theorem just carried as background.','221, p. 267, etale-cover example')
event('221-4c-graphs','independent re-proof','An S-prime morphism X-prime to Y-prime determines its graph in X-prime times_{S-prime} Y-prime; projection to X-prime is an isomorphism. Conversely an embedded subscheme with that projection an isomorphism gives the morphism by its inverse followed by the second projection. More generally the same construction identifies sections of Z-prime over X-prime with such subschemes of Z-prime. A section of a separated morphism is closed by pulling back the diagonal. This directly verifies the prime on Z and the target Y; the openness of the graph locus is deferred to the continuation.','221, p. 267, section 4 c')
record_page('221',267,r'''Compared sources/fr_printed/fr/221.tex entry lines 860–916 and sources/fr/fr/221.tex entry lines 866–922 with scan leaf 20 at 400 dpi, full page and all three enlarged bands.

Confirmed canonical corrections 0011–0016 from the scan, including all six semantic operations of 0016 and its composition with 0013. Added singular grammatical agreement in the corrected local-complete-intersection clause. Restored the plural les mots, selective underlines, ordinary quotes, plain typed G abbreviations, commas, spaced abbreviations, wavy functor versus straight scheme underlines, inline Hom/section identity, omitted product-base abbreviation, Pi indices below, and short arrows. The inserted provenance footnotes remain only in the corrected layer.

Checked the proper-support reduction from quasi-projective to projective ambient space, the fixed-rank etale-cover consequence conditional on openness, and the graph/section correspondence. The geometric openness theorems themselves remain background inputs. Recorded the finite-conjunction qualification with an infinite-intersection counterexample; the printed wording is preserved.''')
from update_record_counts import update
update()
```

**The audit has not passed its completion gates, and no final ZIP has been produced.** An executable workspace is required to recover the actual files, finish page 267, and continue the remaining checks in the prescribed order.
