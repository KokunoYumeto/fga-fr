from audit_utils import read, write

s=read('CHECK_RECORD.md')
anchor='| Source pagination |'
rows=r'''| Pro-object | `\text{\uwave{X}}` | Wavy-underlined ordinary X in 195-371 onward, distinct from Gothic formal-scheme X and from a tilde placed above X |
| Local category variants | `\text{\uwave{C}}`, `\text{\uwave{L}}` | Preserve the two printed L variants on 195-372; do not normalize them to C |
| Relative differentials | `\mathord{\underset{\sim}{\Omega}}` | Wavy-underlined Omega on 195-382; the exact underline style remains provisional for the final crop reading |
| Picard and line-bundle functors | `\text{\uwave{P}}`, `\text{\uwave{L}}` | Wavy ordinary letters on 195-383–384; plain Hom where printed |
| Ideal of definition | `\mathfrak J` or `\text{\uwave{J}}` | Gothic handwritten J on 195-387, typed wavy-underlined J on 388; retain the local distinction |
| Cover-class sheaf | `\text{\uwave{G}}` | Wavy-underlined G in 195-388 denotes the sheaf; ordinary G applied to an open or scheme denotes its class set |
| Representing complete ring | plain `O` or `\mathcal O` | Plain typed O in the earlier pages of 195; the handwritten cursive form at 388–389 is provisionally represented by script O, without a sheaf underline |
| Comma statement numbers | `5, 1`, `5, 2`, `3, 1` | Literal printed numbering in 195; not normalized to decimal points |
'''
assert '| Pro-object |' not in s
s=s.replace(anchor,rows+anchor,1)
old='- 195-369, title: corrected ALGÉBRIQUES to singular ALGÉBRIQUE to agree with géométrie; the printed layer retains the final S.\n\n'
assert s.count(old)==1
s=s.replace(old,'')
decisions=r'''- 190-323, Cartier connection: retained the printed tensor/pullback typography and corrected Omega's base X to X-prime, missing pullback and direct-image stars, and rationnelle to rationnel. The broader Cartier argument and its normalization are recorded separately.
- 190-324: restored IGUSA-LANG and the historical projectivity question without an inserted later footnote.
- 190-325: corrected the second Serre reference from [1] to [6], confirmed by bibliography 327; qualified the empty-cover issue by fidèlement plat. The quasi-compactness qualification on torsor trivialization is recorded separately.
- 195-369, title: corrected ALGÉBRIQUES to singular ALGÉBRIQUE to agree with géométrie; the printed layer retains the final S.
- 195-370–372, functor variance: corrected the two arrows, missing target primes and the target-category index J. Restored the printed local L category symbols and unindexed limit abbreviations in both layers.
- 195-373, pro-category formulas: corrected the missing outer parenthesis, three missing pro-object/functor marks, the equalizer source prime and the last category symbol. The strictness and size qualifications remain in the check events.
- 195-374: retained the asserted Artinian finite-group-scheme example but recorded a square-zero-base counterexample in the events.
- 195-375: restored the printed continuous-Hom wording and corrected the coefficient-algebra label A to Lambda. The restrictions needed for product decompositions and power-series presentations are separate notes obligations.
- 195-376: removed merged erratum footnotes and restored the original relative quotient and absolute m/m-squared discussion in both layers. Corrected only the module coefficient K to A, a missing parenthesis and stray punctuation. The derivation kernel, inseparable residue and unrestricted-surjection defects are separately recorded.
- 195-379: removed the merged footnote and corrected the base-point Y to S, the missing map target/prose closure, two coefficient-algebra labels Y to Lambda and the final closed-point base Y to S.
- 195-380: corrected the opening structural-sheaf base X to Y. The representability shorthand remains printed; unframed automorphisms are discussed separately.
- 195-381–382: corrected the Hom tangent cohomology degree from H1 to H0 and its missing parenthesis. The square-zero flatness probe was explicitly narrowed to algebras with the same underlying topological space after a flawed broader formulation was noticed.
- 195-383: removed merged representability footnotes; corrected two misplaced coherent-sheaf letters F to G, the omitted units star and Picard variance covariant to contravariant. The section-only Picard assertion remains a separate proof obligation.
- 195-384: restored the original proper/separable-fibres wording and removed later footnotes. Corrected the base Y to S and the missing prose parenthesis. A real-conic example qualifies the bare Picard exactness claim without changing its historical wording.
- 195-385–386: restored Gothic derivation G, crossed kappa and the printed product base A in both layers. Preserved the abbreviated At/(t-squared) notation; corrected only the stray product punctuation in the corrected layer. General existence assertions remain identified background inputs.
- 195-387: removed the merged all-thickenings non-zero-divisor hypothesis and smoothness footnotes. Corrected the lifting reference from section 1 to section A. Retained the absolute cotangent quotient and the weaker density claim, with counterexamples and refined forms in the events.
- 195-388: restored the printed completed-stalk equality and uncompleted marked tensor, removing the later inclusion and A_red clarification. Recorded the tensor defect and a nonalgebraizable completed-cover example separately; corrected revêtement plats to revêtements plats only in corrected French.
- 195-389: restored Proposition 5,1 without an inserted qualification, its inline product over uncompleted local rings, and its affirmative final smoothness assertion. Corrected un Lambda-algèbre to une and removed a doubled punctuation mark only in corrected French. A coefficient-flatness counterexample is recorded under the intended nilpotent marking; the final smoothness claim remains a later proof obligation.

'''
s=s.replace('## Open reading questions',decisions+'## Open reading questions',1)
write('CHECK_RECORD.md',s)
