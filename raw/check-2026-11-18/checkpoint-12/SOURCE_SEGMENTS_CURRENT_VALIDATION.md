# Current source-segment extraction checks

The existing `scripts/source_segments.py` passes the current mechanical checks for all declared source units and layers. No extractor change was required. This report concerns literal markers, source ranges and exact extracted bytes; it does not establish textual, mathematical, translation, scan or visual correctness.

## Snapshot and reuse of earlier evidence

The all-layer snapshot was captured from **2026-11-19T04:11:47.386762+00:00** to **2026-11-19T04:11:47.915238+00:00**, after two complete reads produced identical file sets and bytes. It is retained at `tmp/frozen_build_inputs/read_through_236_243`. This capture precedes later Commentaires and errata edits made by root.

All **274 files / 6,038,152 bytes** match the capture manifest. Of these files, **270** are byte-identical to the earlier `source_marker_structure_01` snapshot. The only changed paths are `sources/fr/fr/232.tex`, `sources/fr/fr/236.tex`, and the corresponding two paths under `sources/fr_printed`. All nine translation trees are byte-identical to the earlier structural snapshot.

The published extractor is unchanged, with SHA-256 `d2cc95f1b28d52d2885c34c74838855face2485fe63f78f0553c5b9d9a9e2ca3`. Earlier metadata remains exact for **106 macro definitions, 190 include edges, 131 unit identifiers and 211 cross-layer matrix rows**. The earlier full structural inventory remains the reference for those unchanged tables; the new checks verify current byte ranges and extraction behavior.

## Coverage and result

- **11 layers** and **171 declared layer/unit pairs** passed whole-unit and independent lexical-range checks.
- **2,133 literal marker segments** passed byte-offset, endpoint and slice checks.
- **2,135 reference-page requests** produced the expected exact-page or known missing-marker status.
- **44 end-to-end CLI cases** passed, with **402 exact metadata records** and **365 exact source-slice outputs**.
- **8 token-only fixtures** checked lexical edge cases without using source content for interpretation.
- Every current marker sequence matches the earlier inventory. There are **zero duplicate marker groups, zero ambiguous current markers and zero nonliteral source-page tokens in the declared units**.
- Frozen input bytes remained unchanged throughout the checks.

The 17 unit identifiers are `149`, `e149`, `182`, `e182`, `190`, `e190`, `195`, `e195`, `212`, `e212`, `221`, `e221`, `232`, `e232`, `236`, `e236` and `com`. Ten layers declare all 17 units. The partial layer `es_149_printed` declares only unit `149`; its other unit selections intentionally produce an out-of-scope status.

### Previously known marker gaps

| Layer and unit | Missing literal marker | Explicit neighbor context |
| --- | ---: | --- |
| `ko`, `195` | 377 | Marker 376 to before marker 378 |
| `ko`, `195` | 385 | Marker 384 to before marker 386 |

These are the same two structural gaps reported earlier. They do not establish that any text is absent. Ordinary extraction records a missing-marker status and emits no Korean slice for that page. `--neighbor-span` explicitly selects surrounding source context and labels it as context, rather than an exact requested-page segment.

## Commands for the translation phase

Run from the workspace. Each output directory must be new. Commands below use the pinned snapshot; replace the `--work` argument with another chosen work tree when a later source state is intended.

All layers, complete unit 149:

```sh
python -B FGA_CHECK/scripts/source_segments.py \
  --work tmp/frozen_build_inputs/read_through_236_243 \
  extract --unit 149 --layers all --strict --out tmp/review_all_149
```

All layers at the exact printed-page marker 169 in unit 149, including any unmarked unit prefix:

```sh
python -B FGA_CHECK/scripts/source_segments.py \
  --work tmp/frozen_build_inputs/read_through_236_243 \
  extract --unit 149 --page 169 --layers all --include-unit-prefix \
  --strict --out tmp/review_all_149_169
```

All ten full layers for another complete unit, avoiding the partial Spanish layer's intentional scope status:

```sh
python -B FGA_CHECK/scripts/source_segments.py \
  --work tmp/frozen_build_inputs/read_through_236_243 \
  extract --unit 195 \
  --layers fr,fr_printed,en,es,pt-BR,pt-BR_printed,vi,vi_diplomatic,ko,zh-Hans \
  --strict --out tmp/review_full_layers_195
```

Explicit surrounding context for the known Korean page-377 marker gap:

```sh
python -B FGA_CHECK/scripts/source_segments.py \
  --work tmp/frozen_build_inputs/read_through_236_243 \
  extract --unit 195 --page 377 --layers fr,ko --neighbor-span \
  --out tmp/review_195_377_context
```

Change `--page 377` to `--page 385` for the other known gap. Omit `--neighbor-span` to retain the missing-marker status without creating a Korean context slice. Additional ready-to-run commands are in `CLI_EXAMPLES.txt` in the report directory.

## Selection behavior and limits

Page arguments refer to literal printed-page markers, not physical compiled-PDF page numbers. A page slice starts at its selected `\src` invocation and ends before the next invocation or at file end. The opening marker is included. `--include-unit-prefix` adds the unmarked prefix only when selecting the first marker. Whole-unit extraction returns the exact complete unit file.

`--strict` writes its selected outputs and then returns exit code **2** if any selection is missing, contextual, ambiguous or out of scope. Without `--strict`, those states are recorded in `SEGMENTS.tsv` and the command returns **0**. Thus `--layers all --unit 195 --strict` intentionally returns 2 because `es_149_printed` does not declare unit 195. Duplicate markers, if introduced later, require an explicit one-based `--occurrence N`; none exist in this snapshot.

Each extraction writes exact `.tex` slices, a `SEGMENTS.tsv` manifest and an escaped HTML comparison aid. The audit checked bytes, metadata, output-file sets and HTML nonempty-file status only; it did not open or inspect the HTML. Source fragments need not be standalone compilable TeX documents.

The helper recognizes literal marker calls and literal include paths. It does not expand arbitrary TeX or simulate verbatim environments. No scan, image, PDF, paragraph meaning or correction ledger was reviewed.

## Published evidence

The report directory is `source_segment_checks/snapshot_20261119_041147`.

`AUDIT.json` gives the complete result and tool/input hashes. `LAYER_CHECKS.tsv`, `UNIT_CHECKS.tsv`, `MARKER_CHECKS.tsv` and `PAGE_REQUEST_CHECKS.tsv` identify the checked scope and exact ranges. `CLI_CHECKS.tsv`, `CLI_OUTPUT_CHECKS.tsv` and `TOKEN_FIXTURE_CHECKS.tsv` record execution and token-case outcomes. `FILE_HASH_COMPARISON.tsv` and `CAPTURE_HASH_VERIFICATION.tsv` support reuse of unchanged prior evidence. `STRUCTURAL_DIFFERENCES.tsv` contains only the two known Korean marker gaps.

Published commands use workspace-relative paths and `python -B`. `SANITIZATION.tsv` records the presentation-only conversion of the command examples from their temporary absolute-path form. Extracted source fragments and HTML remain under `tmp`; sources, ledgers, rights files and existing extractor code were not changed.
