# Continuation from checkpoint 05

The supplied checkpoint was restored and verified on 19 November 2026.
All 466 hash-bearing entries passed byte-count and SHA-256 verification.
The input scans, original sources and context were also verified separately;
see RESTORE_VERIFICATION.md. They are not nested in the output package.

The substantive reading remains one sequential stream by GPT-6 Astra,
ChatGPT Pro mode. A support worker is limited to archive verification and
TeX infrastructure; it does not read scan pages, edit text, or adjudicate
mathematics or translations.

The first confirmed continuation clock reading was
2026-11-19 00:57:32 UTC. The first continuation checkpoint, number 06,
is due after 45 minutes of work, at 01:42:32 UTC. Later checkpoints
continue at 45-minute intervals. No section-completion checkpoints are made.

The inherited page-completion record reaches 212-116 (122 page records).
Current progress is always determined from CHECK_RECORD.md and progress.log,
not from the mere presence of an edit script.

## Build repairs

Three scripts record 26 source edits across the two French layers:

- repair_checkpoint05_build.py: nine joined control words, the blank
  paragraph token in equation (4.3), and the limit-operator grouping
  in each layer.
- repair_checkpoint05_braces.py: one duplicated underline terminator
  in each layer.
- repair_checkpoint05_superscript.py: grouping the primed factor before
  its inverse exponent in each layer.

These correct the earlier run and are identified by that prefix in the
evidence column. Compilation and typography status are separate from
scan-reading completion.

## Terminology

TERMINOLOGY_LOW_CONFIDENCE.md preserves both supplied low-confidence
decisions and locates their candidate occurrences. Neither decision has
been applied. The six translations have not yet been read in this continuation.

## Review status

All confidence values remain provisional until the mandatory final reading.
No inherited correction is accepted solely because it appears in a previous
AI record. An edit script from the failed run is a locator guide only;
lost pages are read again directly from the scans.

## Checkpoint 06 status (historical)

The continuation has completed the scan reading through 221-264, for
140 completed French page records in total. Page 221-265 is in progress;
its full image has been read, but its enlarged-crop review and edits are
not yet complete. No translation reading has begun.

The fresh French diagnostic builds through 221-263 both have 150 pages,
zero engine errors and zero missing glyphs. The corrected layer has five
overflows above 2 pt and the as-printed layer has six. Three in each layer
exceed 10 pt and still require visual review and layout correction.

Separate Korean and Chinese diagnostic copies now compile with open
font substitutions, without engine errors or missing glyphs. The nine
font-name substitutions have not yet been adopted in the live sources.
The Korean copy has three overflows above 2 pt; the Chinese copy has none.

Checkpoint 06 is being saved after the 01:42:32 UTC interval boundary.
The next interval boundary is 02:27:32 UTC. Final correction-by-correction
review, remaining French reading, all translation reading, contextual
verification, layout work, final builds and the final archive remain open.

## Checkpoint 07 status

The continuation has completed the scan reading through 232-146, for
156 completed French page records in total. The next page is 232-147.
No translation reading or final correction-row review has begun.

Fresh French builds frozen through 221-276 have three stable LuaLaTeX
passes, 150 pages each, zero engine errors and zero missing glyphs.
Their overflow counts remain five and six above 2 pt, respectively.
Separate layout-only diagnostic patches remove every overflow above
2 pt in the French and Korean candidate copies. They are not yet
adopted in the live sources. Open CJK font substitutions likewise
remain separate diagnostic candidates.

The support worker prepared 148 inspection images for eleven candidate
books, covering distributed spreads and every large-overflow region.
Those images have not yet received the principal reader's visual review;
the manifest distinguishes preparation from inspection. A structural
source-segment extraction tool is the next mechanical support task.

The current French reading has identified and recorded the Picard
cover-category indexing issue on 232-145 and the omitted Pic-prime and
units-star signs on 232-146. All current row confidences remain provisional
until the mandatory second reading.

Checkpoint 07 is scheduled for the 02:27:32 UTC interval boundary.
The next interval boundary is 03:12:32 UTC. Remaining French reading,
all translations, row-by-row review, contextual notes, final builds and
PDF inspection remain open.

## Checkpoint 09 status

The continuation has completed the scan reading through 236-238, for
189 completed French page records in total. Page 236-239 has been rendered
at 400 dpi and its full image and three enlarged bands have been read;
its source edits, mathematical decisions and completion record are still
pending. The remaining French pages, Commentaires and errata, all translation
reading and the final correction-row review remain open.

The last finished French builds, frozen through 236-224 with the repaired
232 arrow token, have three stable passes, 149 pages each, zero engine
errors, missing glyphs or unresolved references. Their overflows above
2 pt remain five and six. New builds frozen through 236-237 are running
in separate immutable copies; their reports are not yet published.
The CJK font and layout candidates are still separate from the live
sources and require adoption and final visual inspection.

A mechanical French-layer difference inventory is complete for the
03:34:25 UTC snapshot: 29 file pairs, eight differing content files,
275 changed hunks. Exact bytes, ranges and hashes were independently
checked. Ledger links are candidates only and have not received substantive
adjudication; the report identifies unmatched and page-mismatched candidates.
No support worker has read or judged the text, mathematics, translations
or images.

New mathematical decisions since checkpoint 08 are recorded page by page.
They include the sigma/rho order, missing identity component, several
base/index slips, an invertibility hypothesis in the openness argument,
branch-splitting qualifications, the regular cubic over F_3(a) justifying
geometric normality in 3.2, and the canonical abelian subgroup in 3.4.
These decisions and every new correction row still await the mandatory
second reading after the languages.

Checkpoint 09 is scheduled for the 03:57:32 UTC interval boundary.
The next interval boundary is 04:42:32 UTC. All remaining text reading,
final row review, contextual notes, final builds, PDF inspection and the
final archive remain open.

## Checkpoint 08 status

The continuation has completed the scan reading through 236-222, for
173 completed French page records in total. Page 236-223 has been rendered
at 400 dpi and its full image and three enlarged bands have been read;
its source edits and completion record are not yet applied. The page has
the reversed sigma/rho explanatory order in print, the missing identity
superscript on the first reduced subgroup, and the printed agreement
choisi une cloture to adjudicate in the corrected layer. No translation
reading or final correction-row review has begun.

Fresh French diagnostic builds frozen through 232-148 still have three
stable passes, 150 pages each, no engine errors, missing glyphs or unresolved
references. Their overflows above 2 pt remain five and six. The CJK font and
layout candidates remain separate from live text and require adoption and
the principal reader's final PDF inspection.

The support worker has completed the nonmutating source-segment extractor
and structural ledger/coverage validator. STRUCTURAL_GATES.md identifies
one inherited confidence-category mismatch and two exact duplicate row
groups, to be adjudicated during row review. Its explicitly frozen metrics
are older than this checkpoint's page progress. No support worker has read
or judged the text, mathematics, translations or images.

Checkpoint 08 is scheduled for the 03:12:32 UTC interval boundary.
The next interval boundary is 03:57:32 UTC. Remaining French reading,
all translations, row-by-row review, contextual notes, final builds and
PDF inspection remain open.

## Checkpoint 10 status

The sequential French reading is complete through e236-305: 209 of 211
item/page keys. The two remaining pages are e236-306 and e236-307. All
preceding Commentaires and errata have records, edits and check events.
Errata remain separate and unmerged. All translations and the mandatory
final correction-row reading are pending.

The fresh French build snapshot through 236-243 has 148 pages per layer,
three stable passes, no engine errors or missing glyphs, and the same five
and six boxes above 2 pt. It predates the subsequent Commentaires and
errata changes, which require another build. Diagnostic layout and CJK
font changes remain separate from live sources.

The terminology inventory contains all 67 supplied decisions; 53 apply
by language scope, of which 51 are high or medium and two are low. The
two low decisions are excluded from application and reproduced exactly
with literal candidate locations. Independent lexical validation passed;
no translation meaning or term choice has been adjudicated by a worker.
The expression/reference navigator and statement/event locator inventory
are mechanical support work in progress, not substantive reading.

This checkpoint is created at the 04:42:32 UTC interval boundary. The
next checkpoint is due at 05:27:32 UTC. Do not substitute build success,
lexical inventories or inherited records for scan or translation review.
The final archive is not yet ready.

## Checkpoint 11 status

All 211 French item/page keys have completed their sequential scan reading.
The English reading is complete through exposé 149, printed page 191.
Page 192 has been rendered at 400 dpi; its full image and top enlarged
band have been read. Its middle and bottom bands, edits and completion
record remain pending. No English exposé is yet marked complete.

Twelve unprinted editorial footnotes have been removed from corrected
French 149 and 212. Fresh builds after these removals have 148 pages per
French layer, three stable passes each, zero engine errors, missing glyphs
or unresolved references, and five/six boxes above 2 pt respectively.
Layout and CJK font candidates still await adoption and final inspection.

The English review found an unjustified editorial replacement of the
printed hypercohomology spectral sequence on page 191. The original
nested-cohomology expression has been restored: it computes cohomology
of the complex of termwise cohomology groups and is needed in the duality
argument. Its explanatory footnote was removed. This finding must be
carried into the remaining translations. English cobord terminology in
149 still needs its final consistency pass against the supplied glossary.

The refreshed French-layer difference inventory contains 303 hunks;
its mechanical mapping and footnote-removal replay passed independent
validation. Sixty-nine ordinary unmatched hunks still require the
principal reader's substantive adjudication. Mechanical inventories do
not constitute textual or mathematical review. All new correction rows
remain low confidence until the mandatory final second crop reading.

The scheduled checkpoint boundary was 05:27:32 UTC. Creation follows
shortly after that boundary following a context handover. The next
checkpoint boundary remains 06:12:32 UTC. Remaining translations,
row review, repeated-error searches, structural cleanup, final builds,
PDF inspection, contextual notes and the final archive remain open.

## Checkpoint 12 status

The first French reading is complete for all 211 item-page keys. English
149 is complete through its Addendum and English 182 is complete through
printed page 212. Page 182-213 has received the full-image, all enlarged-crop
and paragraphwise source reading, but its edits and page record are not yet
applied. The other translation streams and all diplomatic comparisons are
still pending. The final correction-by-correction crop rereading has not
begun, and no provisional confidence is promoted by a mechanical replay.

The complete English 149 replay reproduces its source and 1,128 ledger rows
exactly. The fixed English 182 replay through page 204 reproduces the full
source and 682 scoped rows exactly, including all 62 rows of the repaired
page-199 script. Detailed reports preserve the exact frozen inputs and
hash-bound row numbering. A harmless repeated French reference index on
page 202 and the recorded page-205 marker movement are documented rather
than treated as replay failures.

The English preamble now loads ulem with normalem. Its frozen build through
182-197 has three successful stable passes, zero engine errors, zero missing
glyphs, and two remaining overflows above 2 pt in exposé 149. Later source
pages have not yet been included in a new frozen build. French builds after
the editorial-note cleanup likewise succeed; layout candidates and the CJK
font proposals remain separate pending final adoption and visual review.

Unapplied structural-repair proposals are now preserved: exact duplicate
ledger deletions, event-category spelling normalization retaining original
wording, source-locator insertions, and explicit choices reserved for the
principal reader. None of these proposals changes a substantive judgment.
The translation page-record helper now accepts printed=False, allowing the
future diplomatic records to name the appropriate French source; existing
calls retain their original bindings and output.

Checkpoint 12 is scheduled for the 06:12:32 UTC interval boundary. The next
boundary is 06:57:32 UTC. All later English reading, the five other corrected
translations, their diplomatic layers, second correction reading, repeated
error searches, structural finalization, final builds and PDF inspection,
contextual notes and the final archive remain open.
