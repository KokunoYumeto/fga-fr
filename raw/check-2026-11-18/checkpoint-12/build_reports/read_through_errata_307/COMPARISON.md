# Frozen French compiler regression comparison

Current stage: `read_through_errata_307`. Successful comparison stage: `read_through_236_243`.

The existing frozen-build helper copied both French trees before compiling. All engine passes and source-integrity checks use those frozen copies; later live edits were not read or compared. Snapshot timing and root-requested scope are recorded in `FROZEN_BUILD.md`.

All layers completed three engine passes. The following counts describe their final passes.

| Layer | Passes | Engine exits | Stable auxiliaries | Pages | Errors | Missing glyphs | Unresolved references | Warnings | Boxes >2 pt | Boxes >10 pt | Maximum overflow |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fr | 3 | 0,0,0 | True | 148 | 0 | 0 | 0 | 100 | 5 | 3 | 36.72565 pt |
| fr_printed | 3 | 0,0,0 | True | 148 | 0 | 0 | 0 | 100 | 6 | 3 | 36.72565 pt |

`COMPILATION_COMPARISON.tsv` records every numerical delta. `DIAGNOSTIC_DELTA.tsv` groups changed compiler messages by category and source. `OVERFLOW_COMPARISON.tsv` compares all >2 pt source locations and amounts. `HYPERREF_WARNING_LOCATIONS.tsv` extracts only compiler-reported input lines and removed tokens; it contains no source passages. `SOURCE_BLOCKERS.tsv` contains any primary engine error and is header-only when none occurred.

Engine exit codes and auxiliary stability are distinct from the remaining overflow gate. The build runner returns status 1 for boxes above 2 pt even if every engine pass exits 0. Existing layout proposals remain separate and unapplied.

No source, font, layout, ledger or rights bytes were changed by support. Raw logs, compiler copies, PDFs and SyncTeX files remain in the task-local runtime. These mechanical reports do not certify wording, mathematics, translations, scans or visual PDF appearance.

Comparison generated UTC: 2026-11-19T04:54:12.052944+00:00.

This capture includes the completed French reading through errata page 307 and the local footnote-marker groups present at 04:46:04 UTC. All six engine passes finished without errors. Root-reported later removal of twelve editorial footnotes and subsequent reconciliation/translation edits are excluded. The exact frozen source hashes also bind the refreshed French-layer difference report and mathematical-expression navigator.
