# Frozen French compiler regression comparison

Current stage: `read_through_236_222`. Comparison stage: `read_through_232_148`.

The requested page boundary was retained by extracting the two French source trees from checkpoint 08, created at 2026-11-19T03:12:42.111973+00:00. Live source work had advanced when this support task resumed. All 58 extracted files matched the checkpoint manifest in both size and SHA-256 before the existing frozen-build helper copied them again for compilation. No evolving live source tree was read or compared.

Archive: `checkpoints/FGA_CHECK_checkpoint_08.zip`. SHA-256: `ac3e3ec98edfa9d31c4049220a18ec726e04f61f2aa7d576b0ba190d8743d493`.

The tables compare the latest completed pass in each stage. A failed first pass is partial evidence: its counts cannot establish final warning, glyph, reference, page-count or overflow stability. A zero page count after a fatal error means no output PDF was produced; it is not a pagination change. The configured limit was three passes, but the existing runner halts a layer on its first engine error. See `SOURCE_BLOCKERS.tsv` for the first observed blocker per failed layer; later errors may be hidden by the halt.

These reports do not verify source meaning, scans, translations, or PDF appearance. No source, font, layout, ledger or rights bytes were changed; separate layout proposals remain unapplied.

| Layer | Passes | Engine exits | Pages | Errors | Missing glyphs | Unresolved references | Warnings | Boxes >2 pt | Boxes >10 pt | Maximum overflow |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fr | 1 | 1 | 0 | 2 | 0 | 0 | 71 | 5 | 3 | 36.72565 pt |
| fr_printed | 1 | 1 | 0 | 2 | 0 | 0 | 71 | 6 | 3 | 36.72565 pt |

`REGRESSION_GATE.tsv` records completion, auxiliary stability and the exact comparison of observed >2 pt source locations and amounts. `COMPILATION_COMPARISON.tsv` contains all numeric deltas; `DIAGNOSTIC_DELTA.tsv` records changed compiler-warning/error groups without copying source passages. `OVERFLOW_COMPARISON.tsv` retains every >2 pt location from either stage. A matching observed subset from an aborted build does not establish a complete overflow gate.

Raw logs, copied compiler sources, SyncTeX files and any PDFs remain under the task-local runtime. Build-runner exit status 1 can indicate either an engine failure or the retained >2 pt overflow gate; engine exit codes and `SOURCE_BLOCKERS.tsv` distinguish these cases.

Comparison generated UTC: 2026-11-19T03:18:08.017307+00:00.
