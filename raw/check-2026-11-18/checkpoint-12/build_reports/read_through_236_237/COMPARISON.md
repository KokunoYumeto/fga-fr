# Frozen French compiler regression comparison

Current stage: `read_through_236_237`. Successful comparison stage: `read_through_236_224_tokenfix`.

The existing frozen-build helper copied both French trees before compiling. All engine passes and source-integrity checks use those frozen copies; later live edits were not read or compared. Snapshot timing and root-requested scope are recorded in `FROZEN_BUILD.md`.

All layers completed three engine passes. The following counts describe their final passes.

| Layer | Passes | Engine exits | Stable auxiliaries | Pages | Errors | Missing glyphs | Unresolved references | Warnings | Boxes >2 pt | Boxes >10 pt | Maximum overflow |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fr | 3 | 0,0,0 | True | 148 | 0 | 0 | 0 | 99 | 5 | 3 | 36.72565 pt |
| fr_printed | 3 | 0,0,0 | True | 148 | 0 | 0 | 0 | 99 | 6 | 3 | 36.72565 pt |

## Changes from the preceding successful stage

The live source capture began at 2026-11-19T03:54:21.368976+00:00 and ended at 2026-11-19T03:54:21.481694+00:00. Two complete reads matched before the source files were copied; `LIVE_FREEZE.json` pins all 58 file hashes. The later helper-copy times in `FROZEN_BUILD.md` describe copying this captured input into the compiler work tree.

Both layers have 148 physical pages, compared with 149 in `read_through_236_224_tokenfix`. Each has 99 compiler warnings, compared with 89 previously. The full increase is in hyperref PDF-string warnings associated with `236.tex`: 9 previously and 19 currently per layer. Current input line 470 has one such warning and line 707 has thirteen; the previous stage had four at input line 784. The five warnings at lines 9 and 59 are unchanged. These are literal compiler-line comparisons; no source-content correspondence or cause of the pagination difference was inferred. `HYPERREF_WARNING_LINE_DELTA.tsv` and `HYPERREF_WARNING_TOKEN_DELTA.tsv` retain the detailed changes.

Every >2 pt overflow source range and amount is unchanged in both layers. All three engine passes exit 0, the final auxiliary state is stable, and final engine-error, missing-glyph and unresolved-reference diagnostic counts are zero. Existing overflow layout proposals remain separate.

`COMPILATION_COMPARISON.tsv` records every numerical delta. `DIAGNOSTIC_DELTA.tsv` groups changed compiler messages by category and source. `OVERFLOW_COMPARISON.tsv` compares all >2 pt source locations and amounts. `HYPERREF_WARNING_LOCATIONS.tsv` extracts only compiler-reported input lines and removed tokens; it contains no source passages. `SOURCE_BLOCKERS.tsv` contains any primary engine error and is header-only when none occurred.

Engine exit codes and auxiliary stability are distinct from the remaining overflow gate. The build runner returns status 1 for boxes above 2 pt even if every engine pass exits 0. Existing layout proposals remain separate and unapplied.

No source, font, layout, ledger or rights bytes were changed by support. Raw logs, compiler copies, PDFs and SyncTeX files remain in the task-local runtime. These mechanical reports do not certify wording, mathematics, translations, scans or visual PDF appearance.

Comparison generated UTC: 2026-11-19T04:06:22.501884+00:00.
