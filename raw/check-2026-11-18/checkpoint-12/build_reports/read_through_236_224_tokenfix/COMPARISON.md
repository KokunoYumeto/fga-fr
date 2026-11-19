# Frozen French compiler regression comparison

Current stage: `read_through_236_224_tokenfix`. Successful comparison stage: `read_through_232_148`.

The existing frozen-build helper copied both French trees before compiling. All engine passes and source-integrity checks use those frozen copies; later live edits were not read or compared. Snapshot timing and root-requested scope are recorded in `FROZEN_BUILD.md`.

All layers completed three engine passes. The following counts describe their final passes.

| Layer | Passes | Engine exits | Stable auxiliaries | Pages | Errors | Missing glyphs | Unresolved references | Warnings | Boxes >2 pt | Boxes >10 pt | Maximum overflow |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fr | 3 | 0,0,0 | True | 149 | 0 | 0 | 0 | 89 | 5 | 3 | 36.72565 pt |
| fr_printed | 3 | 0,0,0 | True | 149 | 0 | 0 | 0 | 89 | 6 | 3 | 36.72565 pt |

## Changes from the successful baseline

Both layers have 149 physical pages, compared with 150 previously. Each has 89 compiler warnings, compared with 84 previously. The five additional warnings per layer are hyperref PDF-string removals of `\uwave`: `232.tex` at input lines 387, 569 and 715, and `236.tex` at input lines 9 and 59. These locations come directly from compiler diagnostics. No cause for the pagination difference was inferred.

The >2 pt overflow source locations and amounts are identical to the previous successful stage in both layers. There are no engine-error, missing-glyph or unresolved-reference diagnostics, and the third-pass auxiliaries are stable.

`COMPILATION_COMPARISON.tsv` records every numerical delta. `DIAGNOSTIC_DELTA.tsv` groups changed compiler messages by category and source. `OVERFLOW_COMPARISON.tsv` compares all >2 pt source locations and amounts. `HYPERREF_WARNING_LOCATIONS.tsv` extracts only compiler-reported input lines and removed tokens; it contains no source passages. `SOURCE_BLOCKERS.tsv` contains any primary engine error and is header-only when none occurred.

Engine exit codes and auxiliary stability are distinct from the remaining overflow gate. The build runner returns status 1 for boxes above 2 pt even if every engine pass exits 0. Existing layout proposals remain separate and unapplied.

No source, font, layout, ledger or rights bytes were changed by support. Raw logs, compiler copies, PDFs and SyncTeX files remain in the task-local runtime. These mechanical reports do not certify wording, mathematics, translations, scans or visual PDF appearance.

Comparison generated UTC: 2026-11-19T03:31:43.719299+00:00.
