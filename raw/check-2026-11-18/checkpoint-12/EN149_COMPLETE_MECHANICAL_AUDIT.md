# Completed English 149: exact replay and frozen build

The whole-unit mechanical replay **passes** for all 25 printed-page markers 169–193, including page 193 and `finish_en_149.py`. No wording, mathematics, scans or visual output was adjudicated.

## Exact replay

The replay is bound to 64 files captured at **2026-11-19T05:31:50.613835+00:00–05:31:50.644129+00:00**. The entire English tree, French 149 reference, 25 page-edit scripts, finish script, helpers and recorded metadata were frozen before subsequent English 182 work.

All 26 scripts execute once without exception in an isolated disposable tree. All 389 declared edit/reporting call sites are observed. The result matches all **72,352 bytes** of the frozen EN 149 source and each of its 25 page slices. Final source SHA-256: `0f3ed1355b33dbeebdb46d8f38f1a5a149da42b79b2e98d3dce646eae7df9d8b`.

All **1,128 generated correction rows**, `C020742`–`C021869`, match the frozen ledger exactly and in order, including their serialized append bytes. The earlier 20,729-row ledger remains an exact byte prefix. There are no new duplicate rows or unexecuted replacement operations; the two existing duplicate groups are wholly within the earlier baseline.

The 266 explicit replacement calls generate 294 rows. The 24 formula-alignment calls inspect 835 explicitly supplied index pairs and generate 834 rows; one page 174 pair is already byte-identical after its preceding operation. All occurrence guards, count tuples, index bounds and independent byte-replacement predictions pass. These are operation counts and exact-string checks, not semantic approvals.

### Page 192 guard and finish

The final captured page 192 script replays cleanly from the original state. Its corrected separator guard observes exactly 5 occurrences and emits 5 rows; the page script generates 61 rows in total. The finish script completes and generates 8 rows. The earlier partial runtime attempt is not replayed as a separate script, because the requested reproducible path is the final full script from the original source.

All 47 generated events match frozen event fields in order, with simulated runtime timestamps excluded from that projection. All 25 page-record/progress entries have matching structural keys, order and timestamps. The single unit-completion entry agrees with progress at **2026-11-19 05:31:05 UTC**. These recorded claims were matched as opaque data, not assessed for meaning.

All 64 input hashes remain unchanged, captured scripts/helpers are unmodified, and no unexpected isolated writes or final-source lexical issues occur.

## Compiler result and preamble repair

The first frozen build, `en149_complete_193`, stopped at `sources/en/en/149.tex` line 67 on undefined `uline`. Root then applied the separately prepared `repair_en_ulem.py`, inserting `\usepackage[normalem]{ulem}` in the English preamble and recording the typesetting correction. Support prepared that script but did not apply it.

The repaired build `en149_complete_193_ulem` uses a fresh **05:39:16 UTC** English-tree capture. Its EN 149 bytes are identical to the completed-unit replay. The fresh tree also includes root's completed EN 182 pages 193–197. The preamble differs from the first capture by exactly the one recorded package line, with CRLF bytes preserved; EN 182 is the only other changed source file between these two captures.

The repaired book completes **three LuaLaTeX passes with engine exit codes 0, 0, 0**, stable last-two-pass auxiliaries, **149 physical PDF pages**, **zero errors**, **zero missing glyphs**, and **zero unresolved-reference/citation diagnostics**. There are 36 final warnings. The remaining overflow gate records exactly two boxes above 2 pt:

| Source | Lines | Overflow | Physical PDF page |
| --- | --- | ---: | ---: |
| `sources/en/en/149.tex` | 111–114 | 7.59183 pt | 8 |
| `sources/en/en/149.tex` | 480 | 26.84898 pt | 13 |

These page mappings come from compiler/SyncTeX metadata; no PDF image or content was inspected. All engine passes succeed, while the build runner returns its separate nonzero overflow-gate status.

The repaired English tree SHA-256 is `abb6575adc58bf1927f68ecbd436fc6d3ed08a28718e74c3cd3f3f371715fbf5`.

## Evidence

Replay metadata is under `translation_script_audits/en149_169_193_snapshot_20261119_053150`. It includes exact page and row checks, operation/count guards, call-site coverage, captured hashes, source/ledger deltas, and record/event/progress correspondence. The isolated replay driver is retained as `REPLAY_AUDIT.py`; raw disposable inputs/outputs remain in `tmp`.

Compiler reports and frozen metadata are under `build_reports/en149_complete_193_ulem`; the original failed stage remains under `build_reports/en149_complete_193`. Raw compiler logs, PDFs and runtime files stay outside the deliverable tree.

No live source, correction ledger, record, progress or rights file was edited by support. Later English 182 edits are outside both frozen captures.
