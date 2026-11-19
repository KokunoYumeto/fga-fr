# FGA en français : les *Fondements de la géométrie algébrique* de Grothendieck

Une transcription en LaTeX des *Fondements de la géométrie algébrique* (FGA) d'Alexandre Grothendieck : ses huit
exposés au Séminaire Bourbaki de 1957 à 1962 (n° 149, 182, 190, 195, 212, 221, 232 et 236), leurs errata et les
Commentaires de 1962, en édition corrigée. Les exposés traitent de la dualité des faisceaux cohérents, de géométrie
formelle, de descente, de représentabilité des foncteurs, des schémas de Hilbert et de Picard, et des schémas en
groupes.

## Réalisation

La transcription, les corrections, l'édition et la composition sont produites par IA, d'après les textes originaux.
L'édition du 30 août 2026 contenait 17 corrections aux exposés 212 et 221, signalées dans le texte ; le relevé de ces
corrections et de leur vérification se trouve dans [releases/2026-08-30-r1](releases/2026-08-30-r1).

Le 18 novembre 2026, GPT-6 Astra (mode Pro de ChatGPT) a commencé un contrôle de toute l'édition sur les numérisations
de NUMDAM. Il a relu sur l'image, page par page, **les exposés 149, 182, 190 et 195 en entier et l'exposé 212 jusqu'à
la p. 116** : 122 des quelque 205 pages imprimées. Pour ces pages, il a établi une couche nouvelle, le français tel
qu'imprimé, et contrôlé le français corrigé publié ici : chaque leçon contre l'imprimé, chaque correction justifiée ou
remplacée par la leçon imprimée, les coquilles de l'original corrigées. Le français corrigé compte
**4 939 modifications** (lecture de l'imprimé 4 618, coquille de l'original 115, structure 191, typographie 15), et
9 959 avec la couche tel qu'imprimé. Le contrôle s'est arrêté à ce point, son environnement d'exécution ayant cessé de
fonctionner ; la seconde lecture de ces modifications et les notes ne sont pas encore faites. Le reste de l'édition
(exposé 212 après la p. 116, exposés 221, 232 et 236, errata, Commentaires) est tel que dans l'édition du 30 août
2026, à la présentation près (préambule commun). Une suite du contrôle est prévue.

Tous les relevés de ce contrôle sont dans [raw/check-2026-11-18](raw/check-2026-11-18) : le point de sauvegarde
complet (`checkpoint-05/`, avec `CORRECTIONS.tsv`, `CHECK_RECORD.md`, `CHECK_EVENTS.tsv` et la couche tel qu'imprimé
`sources/fr_printed/`), le dernier message du contrôle et le prompt tel qu'envoyé.

Le français de ce point de sauvegarde ne compilait pas. Claude (Claude Opus 5.5, effort high) a réparé la compilation
par script, en ne touchant qu'à la composition, en 15 endroits, chacun consigné dans
[REPAIR_LOG.tsv](raw/check-2026-11-18/build-repair-2026-11-19/REPAIR_LOG.tsv) :

- neuf commandes accolées à la lettre qui les suit (`\longrightarrowO_y` devient `\longrightarrow O_y`, dans
  l'exposé 182) ;
- une ligne vide dans l'équation (4.3) de l'exposé 149, une accolade en trop dans l'exposé 182, un double exposant
  dans l'exposé 190, une limite mal placée dans l'exposé 195 ;
- deux débordements dans la marge : une formule centrée de l'exposé 149, composée sur trois lignes alignées, et des
  lignes d'énoncés soulignés, que le préambule laisse maintenant s'espacer davantage.

Aucune leçon n'a été changée. L'édition compile avec LuaLaTeX en trois passes, sans erreur et sans ligne ni formule qui
déborde dans la marge (151 pages). Claude a ensuite regardé des pages du livre et comparé quatre corrections du
contrôle aux numérisations : exposé 149, p. 171 (l'imprimé porte « anticommutent à u », corrigé en « commutent à d »
avec une note) ; exposé 182, p. 205 (l'imprimé porte Aut(X_n), corrigé en Aut(X_{n-1})) ; exposé 195, p. 376 (la
parenthèse ouvrante qui manque à l'imprimé) ; exposé 212, p. 107 (la lettre S′ laissée en blanc à l'imprimé). Dans
les quatre cas, l'imprimé est bien tel que le relevé le dit.

## État

La transcription est complète. Le contrôle sur les numérisations couvre les pages indiquées ci-dessus ; des erreurs
peuvent subsister, en particulier dans les pages non encore contrôlées. Merci de les signaler par une issue GitHub.

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

- [Lecteur PDF, édition du 19 novembre 2026](https://github.com/KokunoYumeto/fga-fr/releases/download/fga-fr-2026-11-19/fga-fr-2026-11-19.pdf) :
  les huit exposés, chacun suivi de ses errata, et les Commentaires de 1962.
- [sources/current](sources/current/README.md) : les sources LaTeX, un fichier par exposé (`149.tex` à `236.tex`),
  par liste d'errata (`e149.tex` à `e236.tex`) et pour les Commentaires (`com.tex`). Compiler `fr/main.tex` avec
  LuaLaTeX depuis le dossier `fr`, en trois passes ; le préambule commun est `tex/base.tex`.
- [raw/check-2026-11-18](raw/check-2026-11-18) : les relevés du contrôle du 18 novembre 2026 et de la réparation de
  la compilation.
- [releases/2026-08-30-r1](releases/2026-08-30-r1) : les fichiers de la publication du 30 août 2026, avec le relevé
  des corrections. Le lecteur de cette édition reste disponible dans la
  [publication du 30 août 2026](https://github.com/KokunoYumeto/fga-fr/releases/tag/fga-fr-2026-08-30-r1).

## Sources

L'œuvre originale : Alexandre Grothendieck, *Fondements de la géométrie algébrique*, exposés 149, 182, 190, 195, 212,
221, 232 et 236 du Séminaire Bourbaki, leurs errata et les Commentaires de 1962. Les textes originaux sont accessibles
sur [NUMDAM](https://www.numdam.org/) et sur le site du
[Grothendieck Circle](https://webusers.imj-prg.fr/~leila.schneps/grothendieckcircle/FGA.pdf). La traduction anglaise de
Tim Hosgood ([thosgood/fga](https://github.com/thosgood/fga/tree/9976dd5f8e2ddcb388f0a07f3aa334f120d1019f), version
9976dd5) a servi de référence.

## Droits

Les droits sur l'œuvre originale appartiennent à son auteur ou à ses représentants ou ayants droit. Notre
transcription, nos corrections et notre composition ont été produites par IA. Elles n'ont pas d'auteur humain et,
selon notre compréhension, ne sont pas protégées par le droit d'auteur ; là où un droit nous appartiendrait malgré
tout, il est versé au domaine public sous [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/deed.fr). Tout
ce travail reproduit l'œuvre originale : rien ici n'accorde de licence ni n'autorise une reproduction, une traduction
ou un autre usage de cette œuvre. Cette édition est publiée à des fins éducatives et non lucratives, et nous ne
revendiquons aucun droit que nous ne détenons pas. Si vous détenez des droits sur cette œuvre et vous opposez à sa
publication ici, veuillez ouvrir une issue GitHub et nous la retirerons. Mention complète :
[RIGHTS_NOTICE.md](RIGHTS_NOTICE.md).
