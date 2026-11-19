# Frozen French compiler regression comparison

Current stage: `read_after_note_cleanup`. Successful comparison stage: `read_through_errata_307`.

The existing frozen-build helper copied both French trees before compiling. All engine passes and source-integrity checks use those frozen copies; later live edits were not read or compared. Snapshot timing and root-requested scope are recorded in `FROZEN_BUILD.md`.

All layers completed three engine passes. The following counts describe their final passes.

| Layer | Passes | Engine exits | Stable auxiliaries | Pages | Errors | Missing glyphs | Unresolved references | Warnings | Boxes >2 pt | Boxes >10 pt | Maximum overflow |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fr | 3 | 0,0,0 | True | 148 | 0 | 0 | 0 | 100 | 5 | 3 | 36.72565 pt |
| fr_printed | 3 | 0,0,0 | True | 148 | 0 | 0 | 0 | 100 | 6 | 3 | 36.72565 pt |

`COMPILATION_COMPARISON.tsv` records every numerical delta. `DIAGNOSTIC_DELTA.tsv` groups changed compiler messages by category and source. `OVERFLOW_COMPARISON.tsv` compares all >2 pt source locations and amounts. `HYPERREF_WARNING_LOCATIONS.tsv` extracts only compiler-reported input lines and removed tokens; it contains no source passages. `SOURCE_BLOCKERS.tsv` contains any primary engine error and is header-only when none occurred.

Engine exit codes and auxiliary stability are distinct from the remaining overflow gate. The build runner returns status 1 for boxes above 2 pt even if every engine pass exits 0. Existing layout proposals remain separate and unapplied.

No source, font, layout, ledger or rights bytes were changed by support. Raw logs, compiler copies, PDFs and SyncTeX files remain in the task-local runtime. These mechanical reports do not certify wording, mathematics, translations, scans or visual PDF appearance.

Comparison generated UTC: 2026-11-19T05:16:29.810653+00:00.

## Note-cleanup comparison details

The two source trees were captured by identical consecutive complete reads from **2026-11-19T05:13: 56.178278+00:00 to 05:13: 56.199917+00:00**. The capture contains 58 files. The baseline is the completed-reading snapshot used by `read_through_errata_307`; the source comparison is hash-based and does not interpret the root's reported footnote removals.

All compiler diagnostic category/source/message counts are unchanged: 100 warnings per final layer, zero errors, zero missing glyphs and zero unresolved-reference diagnostics. There are 192 extracted final-pass hyperref token-removal warning records across both layers. Their signature counts are unchanged, while nine locations move within corrected French 149/212. `WARNING_LOCATION_SHIFTS.tsv` pairs the affected metadata entries by source/token signature and compiler order. These are shifted locations, not newly classified warnings.

Across all six passes, all 45 overflow records retain their source, box type, amount and mapped physical PDF page. The sole line-range change is corrected French `149.tex`, line 485 to 482: 26.84898 pt on final PDF physical page 13. It appears once in each pass. `OVERFLOW_LOCATION_SHIFTS.tsv` and `OVERFLOW_METADATA_COMPARISON.json` show this exact comparison. The ordinary location-sensitive regression flag is false for `fr` because this source-line number changed; it does not indicate a new overflow magnitude or PDF page.

The remaining final overflows above 2 pt are unchanged in magnitude and physical page: 5 in `fr`, 6 in `fr_printed`; both have 3 above 10 pt and maximum 36.72565 pt. PDF physical page counts remain 148 in both books. Compiler/SyncTeX page mapping is mechanical evidence only and has not been visually confirmed.

| Source tree | Baseline SHA-256 | Current SHA-256 |
| --- | --- | --- |
| `fr` | `196f6cd7bad9d57af39c75a0a392fe4a74c897b902fc9a668f3a4451d8d411a5` | `80622703811ebf5bede6e9cca6f02e73a5c5c6eab8a674f47fc0185f9cf5917e` |
| `fr_printed` | `98eb46a0df6d51fe190c2f6504291f84d28372ce8e5eadd54f5b0bbb9cf01add` | `98eb46a0df6d51fe190c2f6504291f84d28372ce8e5eadd54f5b0bbb9cf01add` |

The printed French tree is byte-identical to its baseline. The corrected French changes are detailed by relative filename and exact hashes in the independent source comparison. Source, ledger, record, progress and rights bytes were not edited by support. Raw logs, PDFs and disposable compiler trees remain outside this report directory.

## Independent metadata verification

The independent audit passed for all 58 capture files and 1,318,607 source bytes, including equality with the actual frozen compilation input. The baseline file set is identical: 56 files are unchanged, and only corrected French `149.tex` and `212.tex` have different bytes/hashes. All four candidate/baseline layer hashes match their frozen trees. `CAPTURE_HASHES.tsv` and `SOURCE_COMPARISON.tsv` retain exact per-file evidence.

`COMPILER_METADATA_AUDIT.json` and `PASS_METRICS.tsv` confirm six zero engine exits, stable last-two-pass auxiliary hashes, unchanged final diagnostic/message-hash multisets, and PDF page metadata covering 1–148 continuously. `OVERFLOW_LOCATION_COMPARISON.tsv` independently confirms the final overflow amounts, pages and sole source-line shift. These are mechanical checks only; no PDF content or image was inspected.
