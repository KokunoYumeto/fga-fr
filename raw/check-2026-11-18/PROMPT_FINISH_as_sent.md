# Second pass FGA, continued: Alexander Grothendieck, *Fondements de la géométrie algébrique* (Séminaire Bourbaki, 1957–1962), every page against the print, in every language edition

You are GPT-6 Astra in ChatGPT Pro mode, with a Python and LaTeX environment. This prompt continues an earlier run and
holds its whole task. Attached: `FGA_scans.zip`, `FGA_sources.zip` and `FGA_context.zip` (as given to the earlier run;
each has `MANIFEST.tsv` at its root), the earlier run's `FGA_CHECK_checkpoint_05.zip` (with
`CHECKPOINT_FILE_LIST.tsv`), `FGA_CHECK_final_message_20261118.md`, the earlier run's last message, and the two files
of a terminology standard.

## This run continues an earlier one

An earlier run (GPT-6 Astra, ChatGPT Pro mode, 18 November 2026) saved its checkpoint 05 at 20:36 UTC; its environment
then failed at 21:44 UTC and the work after checkpoint 05 was lost. We verified checkpoint 05 against its file list:
every file is present with its size and SHA-256 (the five excluded entries are Python caches).

**Restore first.** Unzip `FGA_CHECK_checkpoint_05.zip` into the workspace with the three input zips beside it, check
every file against `CHECKPOINT_FILE_LIST.tsv`, then read its `README.md`, `CHECK_RECORD.md`, `progress.log`,
`CORRECTIONS.tsv`, `CORRECTION_REVIEW.md`, `VALIDATION.md`, `BUILD_RUNNER.md` and `scripts/` (its `audit_utils.py` is
the edit tool the earlier run used).

**The state at checkpoint 05:**
- The French as printed (`fr_printed/`, made by the earlier run) and the corrected French (`fr/`) are read against the
scan for exposés 149, 182, 190 and 195 and for exposé 212 through printed p. 116: 122 of about 205 printed pages.
- Lost after checkpoint 05: pages 212-117, 212-118 and 221-249 to 221-266, which the earlier run had read and applied
in its failed workspace, and the reading of 221-267, drafted and not applied. Its last message records what it
remembered of that work and gives two edit scripts (`apply_221_266.py`, applied in the lost workspace, and
`apply_221_267.py`, a draft). They are a guide to where to look, never a substitute for the reading: read these
twenty-one pages from the scan as every other page, and keep only what the image shows.
- The French at checkpoint 05 does not build. One LuaLaTeX pass of `fr/fr/main.tex` (by us, 19 November 2026) stops on
27 errors, among them control words run into the letter after them where `\Osh` was replaced by an upright O
(`\longrightarrowO_n`, `\simeqO_Y`, `\otimesO_X(n)`: nine undefined control sequences), a blank line inside equation
(4.3) of exposé 149 (line 516), with the errors that follow from it to line 522, and a limit control not after an
operator (`\overline F(\text{\uwave{X}}^{(\alpha)})`). The same edits are in `fr_printed/`. Repair every such place in
both layers, recorded as `typesetting` rows that correct the earlier run, before you go on, and keep both layers
building from then on.
- Not begun: the remaining French pages (exposé 221 from p. 267 to its end at p. 276, exposés 232 and 236, the
*Commentaires* and the errata), the six translations and their as-printed layers, the second reading of every
correction row, the builds and the PDF check, the notes and `CHECK_EVENTS.tsv` beyond what the checkpoint holds.

**Your task is the whole task below, from that state.** The earlier run's work is the draft you build on. Check each
part of it as you use it: a recorded correction against the scan, the as-printed layer against the print. Where you
find it wrong, correct it in every layer it belongs to and record the correction in `CORRECTIONS.tsv`, with `corrects
the earlier run:` at the start of its evidence. Then finish everything pending. The translations are realigned to the
corrected French as this check leaves it: every correction of meaning the check makes to the French goes into every
language edition, and every translation is read against the corrected French and checked against the print for its
formulas, numbers and references. Your checkpoints continue the earlier run's numbering from 06.

**The terminology standard.** Two more files are attached: `STANDARDS_20261119.md` and `DECISIONS_20261119.tsv`, one
standard of terms, notation and register per language for all our editions, written on 19 November 2026 by Claude
Fable 5.2 at effort max. The terms of every translation follow this standard where it differs from the edition; in
this work that is the realignment of all six translations (English, Spanish, Brazilian Portuguese, Vietnamese, Korean,
Chinese) and their as-printed layers, where the standard is applied with every other correction of the translation.
Each such change is recorded in `CORRECTIONS.tsv` with the kind `terminology` (a kind besides those listed below). The
decisions the standard marks with the confidence `low` are not applied: list them as they are in
`TERMINOLOGY_LOW_CONFIDENCE.md`, each with the places in the editions it would touch. Where the standard and the
glossary in the context zip differ, the standard holds.

## What this is for

This is the second pass that brings our editions of Grothendieck's *Fondements de la géométrie algébrique* to the
standard of our SGA and EGA editions: the French as printed, the corrected French and every translation, each checked
against the printed original, page by page. The record of the check is kept as well, so that we can see how well a
check of this kind works. It follows the same form as our checks of the Tôhoku paper, Serre's GAGA and FAC, Verdier's
thesis and Illusie's *Complexe cotangent*.

**The work and the editions.** Alexander Grothendieck, *Fondements de la géométrie algébrique*: his eight exposés at
the Séminaire Bourbaki, nos. 149 (1957), 182, 190, 195 (1959–1960), 212, 221 (1960–1961), 232 and 236 (1961–1962), the
*Commentaires* of 1962 and the errata to the eight exposés, about 205 printed pages. Our editions were AI-transcribed
(the French) and AI-translated (the other six languages) by OpenAI Codex models (GPT-5.6 Sol, GPT-6.1 Sol and GPT-6
Astra, at reasoning effort ultra) between July and October 2026; each edition's README and source notes say what it
was made with and from. The French edition (github KokunoYumeto/fga-fr) is a corrected edition: it carries 17
corrections to exposés 212 and 221, each marked in the text, and has no as-printed layer. The English (fga-en), Korean
(fga-ko) and Chinese (fga-zh-hans-cn) editions have one layer each; the Spanish (ega-fga-es) has the corrected text
and exposé 149 as printed; the Brazilian Portuguese (ega-fga-sga-pt-br) and Vietnamese (ega-fga-sga-vi) have a
corrected and an as-printed (diplomatic) layer.

**What earlier checks found.** No second reader has compared these editions with the scan page by page. The records of
the 17 corrections (`edition_records/fr_en_release_2026-08-30/`) give for each one the printed reading, the corrected
reading and the reason; the first of them is a nerve whose components were printed as the (n+1)-fold fiber power with
K_0 = R where the mathematics needs the n-fold fiber power with K_0 = X. Look for slips of this kind on every page.

## The attachments

- `FGA_scans.zip`: the Numdam scans of the printed text, one PDF per item: `FGA_149_….pdf` to `FGA_236_….pdf` (the
  eight exposés), `FGA_com_….pdf` (the *Commentaires*) and `FGA_e149_….pdf` to `FGA_e236_….pdf` (the errata). The
  first page of each PDF is Numdam's cover sheet; the pages after it are the printed pages of the Séminaire Bourbaki
  volume, in order, from the first page named in the manifest. The *Commentaires* and the errata share printed pages
  297–307 of volume 7, so a printed page can appear in two neighbouring PDFs. The editions mark the printed page with
  `\src{N}` (Bourbaki volume pagination) or a margin number: in this check a page is a printed page.
- `FGA_sources.zip`: the editions at the repositories' main branches of 18 November 2026, one folder each: `fr/`
  (French, corrected: `fr/*.tex`, one file per exposé, erratum list and the *Commentaires*, preamble `tex/base.tex`),
  `en/` (English, the same layout), `es/` (Spanish, corrected) and `es_149_printed/` (Spanish, exposé 149 as printed),
  `pt-BR/` and `pt-BR_printed/` (Brazilian Portuguese, corrected and as printed), `vi/` and `vi_diplomatic/`
  (Vietnamese, corrected and as printed), `ko/` (Korean), `zh-Hans/` (Simplified Chinese). Each folder has its README,
  source and credit notes and rights notice; `_repository/` subfolders hold the repository-level README, attribution
  and rights files. The single-file "direct" versions of some editions are assembled from these sources and are not in
  the zip.
- `FGA_context.zip`: start with its `README.md`. `edition_records/` holds the records of the 17 corrections and the
  Korean edition's integration and terminology records; use them for item 2. The other folders serve the notes (item
  6): `programme/` (our programme map and the reference page of Grothendieck's Montpellier archive), `glossary/` (the
  English standard of our SGA editions), `notes/` (research notes of our archive work on the subjects of FGA) and
  `stacks/fga/` (the map from FGA statements to the Stacks project made for our AI-integrated Stacks project).

**What the context is for.** The edition records tell you what earlier passes did; they are records of AI passes, not
authorities, and the scan decides every reading. The programme map, the notes and the Stacks map let your notes
connect FGA to our programme: where it meets Grothendieck's archive, our open questions and our Stacks-style
statements. The check of the text does not depend on them: read them when you write the notes, after the pages are
done.

## The work, in order of importance

1. **The French as printed against the scans, every page.** The edition has no as-printed French layer yet: make it,
   as `fr_printed/` (the same files, with its own `main.tex`), from `fr/`, with the printed reading restored at each
   of the 17 marked corrections. Then compare it with the scan line by line: words, punctuation, formulas, symbols,
   indices and exponents, the fonts of letters (italic, bold, roman, script, Gothic, underlined letters), emphasis,
   the numbering of sections and statements, cross-references, footnotes, which formulas are displayed and which run
   in the line, and the page markers. Every difference from the print is a correction of this layer: the as-printed
   layer says what the print says, its misprints included. The errata and the *Commentaires* are printed text like the
   exposés and are checked the same way.
2. **The corrected French.** The corrected layer is `fr/`. Every place where it differs from the as-printed layer is a
   correction of the original, and each one is justified: by the scan reading, and by the mathematical reason that
   makes the printed reading a misprint (a wrong index, a reversed arrow, a reference to the wrong number, a word that
   breaks the sentence). A correction that is not justified goes back to the printed reading. Misprints of the
   original that you find now are corrected in this layer and recorded. Grothendieck's errata stay in their own
   sections, as printed; they are not merged into the exposés. The corrected layer differs from the as-printed layer
   at the recorded corrections and at no other place.
3. **The English.** The English is `en/`. Read it against the corrected French, paragraph by paragraph: every sentence
   says what the French says, with nothing left out and nothing added; the mathematics is correct and every formula is
   the corrected French formula; the terms are the same through the work and agree with the English of our SGA
   editions (`glossary/GLOSSARY_SGA_EN_UNIFIED.tsv`, one English rendering per French term) and with standard English
   usage in algebraic geometry. Correct errors of meaning, omissions, additions and inconsistent terms; leave style
   alone.
4. **Every other language edition.** Spanish `es/`, Brazilian Portuguese `pt-BR/`, Vietnamese `vi/`, Korean `ko/` and
   Simplified Chinese `zh-Hans/`: read each against the corrected French, exposé by exposé and paragraph by paragraph,
   by the same standard as the English (what the French says, nothing left out or added, every formula the corrected
   French formula, the same terms through the edition, the standard mathematical terms of that language). The
   as-printed layers of the translations (`es_149_printed/`, `pt-BR_printed/`, `vi_diplomatic/`) differ from their
   corrected layers exactly where the French as printed differs from the corrected French, with the printed reading
   translated: check each by its differences from its corrected layer, place by place against the two French layers,
   and make it so. Every correction this check makes to the French that changes what a sentence or formula says is
   carried into every language edition, in every layer it belongs to.
5. **The build.** Every layer builds without errors: the two French layers and the English with LuaLaTeX from their
   folders (`main.tex`); the other editions as their `BUILD.md` or README says (Spanish `es/FGA_ES_CURRENT.tex`,
   LuaLaTeX; Brazilian Portuguese `pt_BR/FGA_PTBR_CURRENT.tex` and `pt_BR/FGA_PTBR_PRINTED.tex`, XeLaTeX, three
   passes; Vietnamese `FGA_vi_current.tex` and `FGA_vi_diplomatic.tex`; Korean `main.tex`; Chinese
   `source/zh/main.tex`, XeLaTeX). No overfull box in any build log sticks out by more than 2pt. Fix overfull boxes in
   the preamble or by a reader-level pass (line-breaking parameters, `\emergencystretch`, a scaled or broken display
   set by a macro of the preamble), never by changing the text. Then render and look at every page of each PDF that
   had an overflow over 10pt before your fix, and a spread of pages over each book.
6. **Notes**, kept apart from the text; they never change a reading. Write in `NOTES.md`: the misprints and slips of
   the original, each with the corrected statement; what each erratum and the *Commentaires* change, and whether the
   change holds; the claims the author leaves without proof, each with what a proof needs; where later work corrects,
   extends or uses a result (EGA, SGA, the literature on Hilbert and Picard schemes, descent and formal geometry),
   with exact locators (cite only sources you can cite to the statement); where FGA meets our programme, using the
   context; and your own ideas, labelled as yours, each with your confidence and your reason. One note per item, with
   its exposé, printed page and statement number.

## Rules

1. **The scan is the authority.** Render every page of the scan yourself at 400 dpi and look at it; enlarge every
   place you decide (crop and scale), and every index, exponent, accent and small sign. The text layer of a scan PDF
   and OCR may help you find your place and flag candidate differences; every reading you keep or change is decided by
   looking at the image.
2. **The as-printed layer is the print.** No modernization, no normalization of notation, no silent correction: the
   print's spelling, accents, punctuation, abbreviations, numbering and typography stay as printed.
3. **Edit the sources in place.** Keep each tree's structure, file names, macros, labels, anchors and page markers; a
   change of structure is made only where the print requires it (a missing or extra paragraph break, a heading, a
   display), and it is recorded like any other correction.
4. **Credits and rights notices stay exactly as they are** in every file, README and front matter: the rights
   statement of each edition, and every name, model and source each edition credits, among them the credits to Tim
   Hosgood's English translation of FGA (and to Steve Hnizdur and Jon Sterling, whom his project thanks) that the
   English, Spanish, Brazilian Portuguese and Vietnamese editions carry.
5. **Work from the printed original only.** This check works from Grothendieck's printed French only; no other edition
   or translation is consulted.
6. **Privacy.** The records replace local paths by `<local>`. Copy no local path and no e-mail address into any file
   you return.

## Method

1. Before the first page, write the current time (UTC) as the first line of `progress.log`, and start
   `CHECK_RECORD.md` with a notation table: the recurring signs, alphabets and abbreviations of the print, each with
   how the layers write it in LaTeX. Keep it up to date.
2. **The French, page by page, in printed order** (exposés 149, 182, 190, 195, 212, 221, 232, 236, then the
   *Commentaires* and the errata, in the order of `fr/main.tex`): render the page; read the as-printed layer against
   the image, line by line; then the corrected layer's text of that page. Write each correction into the files at once
   and its row into `CORRECTIONS.tsv`, then the page's section of `CHECK_RECORD.md`, then append `page
   <exposé>-<printed page> done <current UTC time>` to `progress.log`. Only then go to the next page.
3. **Then each translation, exposé by exposé**, in the order English, Spanish, Brazilian Portuguese, Vietnamese,
   Korean, Chinese: read it against the corrected French, with the scan open for every formula, number and reference;
   then its as-printed layer, where it has one. Write each correction at once, with its row, and the exposé's section
   for that language in `CHECK_RECORD.md`; append `<language> <exposé> done <current UTC time>` to `progress.log`.
4. **One stream.** Do the pages yourself, in one stream, in order: do not split them among parallel workers or
   sub-agents. When the pages of an earlier transcription were split among workers, the same signs were read in
   different ways and the errors went unmarked.
5. **A second reading of every correction.** When the last language is done, go through `CORRECTIONS.tsv` row by row
   against the scan crop of each place: confirm, amend or withdraw each row, and say so in its `confidence` column.
   Then, for every kind of error you found in more than one place (a sign misread the same way, an index dropped, a
   term rendered two ways), search the whole work for it, in every layer, and record what the search found.
6. **Build and PDF check** (item 5), recorded in `PDF_CHECK.md`: per layer, the build command, the errors and
   warnings, the overfull boxes before and after your fix with their sizes, and the pages you rendered and what you
   saw.
7. **The notes** (item 6): only now open `programme/`, `notes/` and the other folders of the context, and write
   `NOTES.md`. For each note, search the context for the same objects and words (grep works well on these files) and
   say where our materials already have the point and whether FGA adds to it, restates it or differs from it. The
   notes in the context are leads from earlier runs, never results to cite as established.
8. **Check events.** For every statement, record its check events in CHECK_EVENTS.tsv: statement id, date, who (model,
   effort, run), type (targeted proof check / independent re-proof / computation or formal certificate / used and
   rechecked in this run / carried as background without fault found / refuted, with the refined statement's id),
   outcome. The file has six columns: `id` (the statement id, for example `212-4.3`), `date_utc`, `who` (GPT-6 Astra,
   ChatGPT Pro mode, this run), `how` (the type), `result` (the outcome) and `where` (exposé, printed page and line).
   A statement here is each numbered statement of FGA whose mathematics this check or the notes examine: every
   statement a correction of the mathematics touches, and every misprint, erratum, claim or link the notes discuss.
   Each type says what happened: a statement you only read through is "carried as background without fault found", not
   "targeted proof check".
9. **Checkpoints.** Save a checkpoint ZIP to the user's Library, or wherever files survive the loss of the execution
   environment, once every 45 minutes of work, each under a new name, `FGA_CHECK_checkpoint_<NN>.zip` with `NN` counting
   up; never overwrite, rename or delete an earlier checkpoint, and put no earlier checkpoint ZIP inside a checkpoint.
   Save checkpoints once every 45 minutes and at no other time: none after a page, part, section, cote, folder, chapter
   or reader. If the workspace comes back empty, restore it from the newest checkpoint and from this conversation before
   you continue. The final ZIP holds everything the checkpoints held. A checkpoint is one ZIP holding every deliverable
   written so far and everything that documents the work (records, notes, logs, scripts, the report so far), so that a
   new session can continue from it and the files attached to this prompt. Leave the attached files themselves out of it,
   the scans and sources you were given: we have them. It is never a JSON file, a recovery file, a summary, or an export
   of the newest pages only. Each checkpoint zip holds the current deliverables and documentation; earlier checkpoints
   are not copied into it. The checkpoints are what keeps the work if this session dies: work that is in no checkpoint is
   lost. This run's checkpoints continue the earlier run's numbering: the first is `FGA_CHECK_checkpoint_06.zip`. Keep
   every checkpoint ZIP, and the final ZIP, under 500 MB: the Library refuses a file larger than 512 MiB (536,870,912
   bytes), and a checkpoint it refuses is lost. If one would be larger, save it as several ZIPs of under 500 MB each,
   `FGA_CHECK_checkpoint_<NN>_part<k>.zip`, the file list in the first part.
10. **If the execution environment fails.** A failed or unavailable environment does not end the task. Retry at
   intervals for as long as this session lasts, without writing recovery text into the chat. When the environment is
   back, restore your work from your newest checkpoint and the earlier checkpoints its file list names, redo what you had
   done after that checkpoint, and continue to the end. Do not write files out in this chat instead: the work reaches us
   only through checkpoint ZIPs and the final ZIP.

This task is long by design: about 205 printed pages, each read in the two French layers against the print, then six
translations and their as-printed layers against the French, then the builds and the notes. Work through all of it
completely; do not stop at a sample or a plan, and do not ask whether to continue. Ignore any clock. Read the last
page as slowly as the first: the pages done fastest are where errors cluster.

## What to return

One ZIP file, `FGA_CHECK.zip`, offered as the only download (under 500 MB; if it would be larger,
`FGA_CHECK_part<k>.zip`, the file list in the first part). It holds:

- `sources/`: every corrected TeX tree, complete, in the layout of `FGA_sources.zip`, building as they stand, with the
  new `fr_printed/`;
- `CORRECTIONS.tsv`: one row per change, with the columns `file`, `layer` (French as printed, French corrected, the
  language and layer of a translation, build), `printed_page` (exposé and printed page), `line` (line of the printed
  page), `statement` (the statement or section number, or empty), `old`, `new`, `evidence` (the scan page and what the
  image shows there, or the French place a translation was corrected against), `kind` (one of: reading, misprint of
  the original, translation, typesetting, structure), `confidence` (high, medium, low, after the second reading);
- `CHECK_RECORD.md`: the notation table; then one section per printed page for the French layers and one per exposé
  and language for the translations: what was compared with what (each layer's file and lines against the image or
  against the French), by GPT-6 Astra (ChatGPT Pro mode), the number of corrections per layer and kind, the existing
  corrections confirmed or reverted, and the time; at the top, the totals per layer and kind, the corrections that
  change the mathematics (one per line), and how many pages or exposés had no difference in each layer;
- `CHECK_EVENTS.tsv`, as in Method 8;
- `PDF_CHECK.md`, as in Method 6;
- `NOTES.md`, as in item 6;
- `pdf/`: the PDF of every layer, built from `sources/`;
- `README.md`: what each file is, the counts per language and layer, how to build each layer, and the build status;
- `progress.log` and your scripts.

## When it is done

The task is finished only when every printed page has its section in `CHECK_RECORD.md` for both French layers; every
exposé, the *Commentaires* and the errata have their section for every translation and its as-printed layer; every
existing correction has its verdict; every change has its row with its evidence; every correction of meaning is
carried into every language edition it belongs to; every layer builds and passes the PDF check; and `CHECK_EVENTS.tsv`
and `NOTES.md` are written. Keep working until then. Do not stop because what remains is long, because a part of the
work looks presentable, or because much has already been done.

Not acceptable:

- a sample of pages, exposés or languages in place of all of them;
- a change without a row in `CORRECTIONS.tsv`, or a row without its evidence;
- a change to the as-printed layer that the print does not show;
- a correction of a misprint made in the as-printed layer, or a difference between the two layers of an edition that
  is not a recorded correction;
- a correction of the French that changes the meaning and is missing from a language edition;
- a change of style in a translation recorded as a correction of meaning;
- a credit or rights notice changed or removed;
- a local path or an e-mail address in any returned file.
