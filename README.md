# FGA en français : les *Fondements de la géométrie algébrique* de Grothendieck

Une transcription en LaTeX des *Fondements de la géométrie algébrique* (FGA) d'Alexandre Grothendieck : ses huit
exposés au Séminaire Bourbaki de 1957 à 1962 (n° 149, 182, 190, 195, 212, 221, 232 et 236), leurs errata et les
Commentaires de 1962, en édition corrigée. Les exposés traitent de la dualité des faisceaux cohérents, de géométrie
formelle, de descente, de représentabilité des foncteurs, des schémas de Hilbert et de Picard, et des schémas en
groupes.

## Réalisation

La transcription, les corrections, l'édition et la composition sont produites par IA, d'après les textes originaux.
L'édition du 30 août 2026 contient 17 corrections aux exposés 212 et 221, signalées dans le texte ; le relevé de ces
corrections et de leur vérification se trouve dans [releases/2026-08-30-r1](releases/2026-08-30-r1).

## État

La transcription est complète. Des erreurs peuvent subsister.

## Autres éditions de FGA

- Anglais : [fga-en](https://github.com/KokunoYumeto/fga-en), traduction complète.
- Espagnol : [ega-fga-es](https://github.com/KokunoYumeto/ega-fga-es), traduction complète.
- Portugais du Brésil : [ega-fga-sga-pt-br](https://github.com/KokunoYumeto/ega-fga-sga-pt-br), traduction
  complète, en édition corrigée et en édition diplomatique.
- Vietnamien : [ega-fga-sga-vi](https://github.com/KokunoYumeto/ega-fga-sga-vi), traduction complète, en édition
  corrigée et en édition diplomatique.
- Coréen : [fga-ko](https://github.com/KokunoYumeto/fga-ko), traduction complète.
- Chinois simplifié : [fga-zh-hans-cn](https://github.com/KokunoYumeto/fga-zh-hans-cn), traduction complète.

Toutes les éditions d'EGA, de FGA et de SGA de ce projet sont recensées dans
[ega-fga-sga](https://github.com/KokunoYumeto/ega-fga-sga).

## Contenu

- [Lecteur PDF, édition du 30 août 2026](https://github.com/KokunoYumeto/fga-fr/releases/download/fga-fr-2026-08-30-r1/fga-fr-canon-errata-0001-0017.pdf) :
  les huit exposés, chacun suivi de ses errata, et les Commentaires de 1962.
- [sources/current](sources/current/README.md) : les sources LaTeX, un fichier par exposé (`149.tex` à `236.tex`),
  par liste d'errata (`e149.tex` à `e236.tex`) et pour les Commentaires (`com.tex`). Compiler `fr/main.tex` avec
  LuaLaTeX depuis le dossier `fr` ; le préambule commun est `tex/base.tex`.
- [releases/2026-08-30-r1](releases/2026-08-30-r1) : les fichiers de la publication du 30 août 2026, avec le relevé
  des corrections.

## Sources

L'œuvre originale : Alexandre Grothendieck, *Fondements de la géométrie algébrique*, exposés 149, 182, 190, 195, 212,
221, 232 et 236 du Séminaire Bourbaki, leurs errata et les Commentaires de 1962. Les textes originaux sont accessibles
sur [NUMDAM](https://www.numdam.org/) et sur le site du
[Grothendieck Circle](https://webusers.imj-prg.fr/~leila.schneps/grothendieckcircle/FGA.pdf). La traduction anglaise de
Tim Hosgood ([thosgood/fga](https://github.com/thosgood/fga/tree/9976dd5f8e2ddcb388f0a07f3aa334f120d1019f), version
9976dd5) a servi de référence.

## Droits

Dans la mesure où l'éditeur détient des droits sur la transcription, les corrections et la composition produites par
IA, ces droits sont dédiés au domaine public sous
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/deed.fr). Cette dédicace n'affecte pas les droits sur
l'œuvre originale et n'accorde aucune autorisation de l'utiliser. Mention complète :
[RIGHTS_NOTICE.md](RIGHTS_NOTICE.md).
