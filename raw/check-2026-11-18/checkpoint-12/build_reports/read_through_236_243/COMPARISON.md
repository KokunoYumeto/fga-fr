# Frozen French compiler regression comparison

Current stage: `read_through_236_243`. Successful comparison stage: `read_through_236_237`.

The existing frozen-build helper copied both French trees before compiling. All engine passes and source-integrity checks use those frozen copies; later live edits were not read or compared. Snapshot timing and root-requested scope are recorded in `FROZEN_BUILD.md`.

All layers completed three engine passes. The following counts describe their final passes.

| Layer | Passes | Engine exits | Stable auxiliaries | Pages | Errors | Missing glyphs | Unresolved references | Warnings | Boxes >2 pt | Boxes >10 pt | Maximum overflow |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fr | 3 | 0,0,0 | True | 148 | 0 | 0 | 0 | 100 | 5 | 3 | 36.72565 pt |
| fr_printed | 3 | 0,0,0 | True | 148 | 0 | 0 | 0 | 100 | 6 | 3 | 36.72565 pt |

## Changes from the preceding successful stage

The all-layer live source capture began at 2026-11-19T04:11:47.386762+00:00 and ended at 2026-11-19T04:11:47.915238+00:00. `LIVE_FREEZE.json` records its file hashes; the compiler audit checks the 58 French entries and both compiler snapshots. The frozen scope precedes the subsequent Commentaires and errata edits described by root, including the new local footnote-marker groups. Those later edits require a later frozen build.

Both layers retain 148 physical PDF pages. Each has 100 compiler warnings, compared with 99 in `read_through_236_237`. The sole additional warning is a hyperref PDF-string removal of `\uwave` associated with `236.tex`, input line 954, in each layer. Warning line/token deltas are recorded separately.

All six engine passes exit 0. Final errors, missing-glyph and unresolved-reference/citation diagnostics are zero, and auxiliary state is stable. Every overflow source range, amount and mapped physical page is unchanged, including records below 2 pt and all three passes; independent tables preserve these checks. Existing layout proposals remain separate.

`COMPILATION_COMPARISON.tsv` records every numerical delta. `DIAGNOSTIC_DELTA.tsv` groups changed compiler messages by category and source. `OVERFLOW_COMPARISON.tsv` compares all >2 pt source locations and amounts. `HYPERREF_WARNING_LOCATIONS.tsv` extracts only compiler-reported input lines and removed tokens; it contains no source passages. `SOURCE_BLOCKERS.tsv` contains any primary engine error and is header-only when none occurred.

Engine exit codes and auxiliary stability are distinct from the remaining overflow gate. The build runner returns status 1 for boxes above 2 pt even if every engine pass exits 0. Existing layout proposals remain separate and unapplied.

No source, font, layout, ledger or rights bytes were changed by support. Raw logs, compiler copies, PDFs and SyncTeX files remain in the task-local runtime. These mechanical reports do not certify wording, mathematics, translations, scans or visual PDF appearance.

Comparison generated UTC: 2026-11-19T04:25:52.163939+00:00.
