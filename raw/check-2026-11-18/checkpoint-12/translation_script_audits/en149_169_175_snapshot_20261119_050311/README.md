# English 149 pages 169–175: mechanical script audit

**Result: the seven captured page-edit scripts reproduce the captured selected pages and their correction rows exactly.** No mismatch, omitted scripted edit, duplicate selected correction row, page-marker problem or lexical balance/mode issue was detected within this scope. This is a mechanical execution/source/ledger check, with no scan, language, mathematical, translation or visual adjudication and no TeX compilation.

## Frozen scope

Selected live files were captured by two identical reads at **2026-11-19T05:03:11.053149+00:00–05:03:11.072235+00:00**. The initial capture contains the current French/English 149 source files, seven `apply_en_149_169.py` through `apply_en_149_175.py` scripts, their two edit helpers and lexer, and the correction ledger, check record and progress log. A separate timestamped capture adds `update_record_counts.py` and `CHECK_EVENTS.tsv`; both captures are hash-bound in the report.

The replay starts from the original English 149 bytes in the shared **04:46:04 source snapshot**, whose manifest hash and file hash are independently checked. It uses the captured current French 149 source and unchanged copies of the seven edit scripts/helpers. All execution occurs in `tmp/en149_mechanical_audit_169_175/replay`, with empty simulated append-only records and fixed simulation timestamps. Root's original scripts and all live source/ledger/record/progress files are untouched by this audit. A successful replay and exact resulting bytes support the stated mechanical result; they do not establish historical process execution independently of the recorded artifacts.

## Exact operation checks

| Page | Target/French outer counts at alignment | Explicit pair count | Generated math rows | All generated correction rows |
| --- | ---: | ---: | ---: | ---: |
| 169 | 33/33 | 33 | 33 | 41 |
| 170 | 35/30 | 24 | 24 | 30 |
| 171 | 51/51 | 51 | 51 | 63 |
| 172 | 26/26 | 26 | 26 | 30 |
| 173 | 24/24 | 24 | 24 | 34 |
| 174 | 37/37 | 37 | 36 | 45 |
| 175 | 60/60 | 60 | 60 | 71 |

All **255 explicit math pairs** have unique destination indices and valid bounds, and every requested count guard passes. They generate **254 math correction rows**: one page 174 pair is already byte-identical after the script's preceding explicit operation and is skipped by the helper's documented equality check. The **58 explicit replacement calls** generate another **60 rows**, including explicitly counted repeated occurrences. Thus all seven scripts generate **314 correction rows**.

Every generated row matches a captured actual row exactly across all ten decoded TSV fields, in the same order. There are no missing or extra selected rows and no exact duplicate selected rows. All seven selected page segments match the replay byte for byte. Their final outer-span counts are 33,30,51,26,24,37,60 respectively; these are lexical counts, not assertions that content correspondence is valid.

## Preservation and lexical checks

The earlier **20,729-row ledger remains an exact byte prefix** of the captured **21,124-row ledger**. The suffix consists of 12 French rows, 314 English rows for 169–175 and 69 English rows for 176. Page 176 lies outside the requested audit.

The replay preserves the English unit prefix and every byte after the page 175 segment, all page-marker spellings/order, and the complete captured French source. No unexpected file is changed in the isolated replay. All captured inputs still match their initial hashes afterward.

The captured current English file differs from the seven-script replay only in 13 line-diff hunks anchored to page 176. These locators are recorded solely to explain why the whole-file hashes differ; their content and edits were not reviewed.

The literal TeX parser reports zero balance/mode issues in the captured English unit. Within pages 169–175, no introduced control-word spelling is absent from both the initial English and current French control inventories. This is a static token check; it does not resolve macro definitions or replace an engine build.

## Report files

`translation_script_audits/en149_169_175_snapshot_20261119_050311` contains the summary, script execution metadata, exact page hashes/ranges, math-pair counts/hashes, explicit-operation hashes, 314 row-to-ledger matches, empty row-delta and lexical-issue files, frozen-input checks and replay provenance. Row IDs bind to the captured ledger hash. `OUTSIDE_SELECTED_SCOPE_DIFFERENCES.json` contains only metadata for the page 176 differences. No source passages or correction payload text is included in these reports.

## Independent metadata audit

A separate audit confirms all 17 frozen input hashes, the exact ledger prefix, row IDs `C020742`–`C021055`, no appended exact duplicates, all seven page-record/progress key and timestamp pairs, and all eight literal script-event projections. The English unit has no completion marker, consistent with this being a partial unit snapshot. Event fields and record prose were matched as opaque strings; their claims were not adjudicated.

`INDEPENDENT_METADATA_AUDIT.json`, `SCRIPT_AST_SHAPES.tsv`, `APPENDED_EN169_175_ROWS.tsv`, `EVENT_CORRESPONDENCE.tsv` and `RECORD_PROGRESS_CORRESPONDENCE.tsv` preserve this independent evidence. `REPLAY_AUDIT.py` preserves the exact isolated-replay driver; its supporting frozen inputs and disposable outputs remain in `tmp`. Captured script/helper hashes identify the unchanged root code used for the replay.
