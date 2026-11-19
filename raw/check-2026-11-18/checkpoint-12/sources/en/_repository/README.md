# FGA in English: Grothendieck's *Fondements de la géométrie algébrique*

An English translation of Alexander Grothendieck's *Fondements de la géométrie algébrique* (FGA, *Foundations of
Algebraic Geometry*): his eight exposés at the Séminaire Bourbaki of 1957–1962 (nos. 149, 182, 190, 195, 212, 221,
232 and 236), with their errata and the comments of 1962. The exposés treat duality for coherent sheaves, formal
geometry, descent, representable functors, Hilbert and Picard schemes, and group schemes.

## How it was made

The English text shares wording with Tim Hosgood's English translation
([thosgood/fga](https://github.com/thosgood/fga), compared at version
[9976dd5](https://github.com/thosgood/fga/tree/9976dd5f8e2ddcb388f0a07f3aa334f120d1019f)), which keeps its
attribution. The rest of the translation is AI-translated, and the corrections, editing and typesetting are
AI-produced. The edition of 30 August 2026 contains 17 corrections to Exposés 212 and 221, each marked in the text; the
records of these corrections and of their check are in [releases/2026-08-30-r1](releases/2026-08-30-r1).

## Status

The translation is complete. Errors may remain.

## Other editions of FGA

- French: [fga-fr](https://github.com/KokunoYumeto/fga-fr): complete transcription, corrected edition.
- Spanish: [ega-fga-es](https://github.com/KokunoYumeto/ega-fga-es): complete.
- Brazilian Portuguese: [ega-fga-sga-pt-br](https://github.com/KokunoYumeto/ega-fga-sga-pt-br): complete, in a
  corrected and a diplomatic edition.
- Vietnamese: [ega-fga-sga-vi](https://github.com/KokunoYumeto/ega-fga-sga-vi): complete, in a corrected and a
  diplomatic edition.
- Korean: [fga-ko](https://github.com/KokunoYumeto/fga-ko): complete.
- Chinese (Simplified): [fga-zh-hans-cn](https://github.com/KokunoYumeto/fga-zh-hans-cn): complete.

All editions of EGA, FGA and SGA made in this project are listed in
[ega-fga-sga](https://github.com/KokunoYumeto/ega-fga-sga).

## Contents

- [Reader PDF, edition of 30 August 2026](https://github.com/KokunoYumeto/fga-en/releases/download/fga-en-2026-08-30-r1/fga-en-canon-errata-0001-0017.pdf):
  the eight exposés, each followed by its errata, and the comments of 1962.
- [sources/current](sources/current/README.md): the LaTeX sources, one file per exposé (`149.tex` to `236.tex`), per
  errata list (`e149.tex` to `e236.tex`) and for the comments (`com.tex`). Compile `en/main.tex` with LuaLaTeX from the
  `en` folder; the shared preamble is `tex/base.tex`.
- [releases/2026-08-30-r1](releases/2026-08-30-r1): the files of the release of 30 August 2026, with the correction
  records.

## Sources and credits

- The original work: Alexandre Grothendieck, *Fondements de la géométrie algébrique*, Séminaire Bourbaki exposés 149,
  182, 190, 195, 212, 221, 232 and 236, their errata and the 1962 comments. The French originals are available
  through [NUMDAM](https://www.numdam.org/) and the
  [Grothendieck Circle](https://webusers.imj-prg.fr/~leila.schneps/grothendieckcircle/FGA.pdf).
- [Tim Hosgood's English translation](https://github.com/thosgood/fga): English wording shared with it remains his.
  His translator's note also thanks Steve Hnizdur for corrections and Jon Sterling for technical support. These
  credits do not attribute the AI-translated additions or the AI-produced corrections to them.

## Rights

To the extent that the publisher holds any rights in the AI-produced translation, corrections and typesetting, they
are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). This does not
affect the rights in the original work or in Tim Hosgood's translation, and grants no permission to use them. Full
notice: [RIGHTS_NOTICE.md](RIGHTS_NOTICE.md).
