# English exposé 182, pages 193–204: mechanical replay

**PASS**. The final replay completed at **2026-11-19T06:05:37.271545+00:00**. This is a script, byte, ledger and provenance audit only; no source meaning, translation, mathematics, scan content or correction validity was reviewed.

## Fixed endpoint

The 316-file capture completed at **2026-11-19 05:58:45 UTC**, before any English 182 page 205 ledger rows. It freezes the current English source, both French reference files, Python helpers/scripts and recorded metadata. The original English source was separately pinned against two byte-identical available copies. No endpoint reconstruction was needed. The target is the complete source state after the saved page 193–204 scripts, including their recorded full-file marker operations.

All twelve saved scripts execute once in the final isolated replay. All **78,838 bytes** of the resulting English source equal the frozen source, and all twelve requested page slices match exactly. Source SHA-256: `50291b6050b583508a7add3313397af4b1b6a099afe676a4e16935413660b219`.

All **682 generated correction rows** equal the scoped frozen rows exactly and in order, including their physical serialized bytes. Their global range is **C021870–C022552**, excluding only **C022110**, an unrelated English preamble row. The earlier 21,869-row ledger is an exact byte and parsed-row prefix. No scoped duplicate rows occur.

| Page | Generated and frozen rows | Global first row | Global last row |
|---|---:|---|---|
| 193 | 25 | C021870 | C021894 |
| 194 | 56 | C021895 | C021950 |
| 195 | 65 | C021951 | C022015 |
| 196 | 43 | C022016 | C022058 |
| 197 | 51 | C022059 | C022109 |
| 198 | 58 | C022111 | C022168 |
| 199 | 62 | C022169 | C022230 |
| 200 | 65 | C022231 | C022295 |
| 201 | 69 | C022296 | C022364 |
| 202 | 61 | C022365 | C022425 |
| 203 | 53 | C022426 | C022478 |
| 204 | 74 | C022479 | C022552 |

## Page 199 recovery check

The corrected saved `apply_en_182_199.py` executes once from the original-source replay path and generates exactly **62 rows**, **C022169–C022230**. All 17 declared edit/reporting call sites are observed. Its 13 explicit replacement calls generate 15 rows, and its 47 supplied math-index pairs generate 47 rows. Every count guard passes; no replacement is a no-op and no generated row has multiple frozen matches. The final page slice is byte-identical to the captured page slice.

Saved script SHA-256: `0f569b71cbc11ef40d736a30822acc5e00ca0e27032c760d5127523bf7f623e9`. Page slice SHA-256: `849d07d7315de149c065a2649566974b85e6660dfa15b17866e6ec1a2f0bc1cf`.

This verifies the reproducible path through the final saved script. The previously reported partial process invocations are not rerun or reconstructed as separate executions. Exact metadata is in [PAGE199_RECOVERY_CHECK.json](PAGE199_RECOVERY_CHECK.json).

## Instrumented operations and recorded metadata

The 133 explicit replacement calls generate 137 rows; all occurrence guards and independent full-file replacement predictions match. Twelve alignment calls use 545 explicitly supplied index pairs and generate 545 rows; span-count guards, destination uniqueness, index ranges and independent page-byte predictions match. These are lexical operation facts, not substantive approval of pairings.

All 188 declared edit/reporting call sites execute. All 27 generated event projections match the frozen events in order when simulated runtime timestamps are excluded. The twelve page-record/progress entries have matching structural keys, order and timestamps. No unit-completion marker is present. Recorded claims are treated as opaque data.

The frozen English source has no lexer issues. All 316 captured input hashes remain unchanged; copied scripts/helpers remain byte-identical. The execution guard records no external I/O attempts and no unexpected isolated writes. Production sources, ledger and root records were not modified.

## Scope facts and initial harness correction

The first inherited EN149 harness recorded two nonapplicable assumptions as blockers even though whole-source and all 682 row comparisons already passed. Its output is preserved in the sibling `en182_193_204_initial_harness_20261119` directory. The final driver follows the actual helper contract and the requested frozen endpoint:

- Page 202 explicitly pairs destination indices 22 and 23 with French reference index 23. Destination indices remain unique, and every index is in range. The helper prohibits repeated destination indices; it does not prohibit reference reuse. This audit records the reuse without assessing its meaning.
- Recorded full-file row **C022479** relocates the literal `\src{205}` marker from character offset 1388 to offset 0 within its old/new operands. After deleting that marker and LF characters, the remaining operand strings are exactly equal. Consequently, the suffix beginning at marker 205 is not byte-identical to the original suffix; the complete replayed source is nevertheless exactly equal to the requested frozen endpoint. Marker placement is not adjudicated here.

The final successful replay uses fresh disposable output files and the same unchanged captured scripts. [HARNESS_SCOPE_FACTS.json](HARNESS_SCOPE_FACTS.json) retains the literal hashes and coordinates.

## Artifacts

| File | Purpose |
|---|---|
| `SUMMARY.json` | Final PASS/FAIL gates and counts |
| `FROZEN_SNAPSHOT.json`, `BASELINE_PROVENANCE.json`, `CAPTURE_HASH_CHECKS.tsv` | Capture and original-input identities |
| `SCRIPT_EXECUTION.json`, `STATIC_OPERATION_COVERAGE.tsv`, `INSTRUMENTED_CALLS.json` | Actual execution and call-site coverage |
| `PAGE_BYTE_CHECKS.tsv`, `SOURCE_BYTE_DELTAS.json` | Exact source comparisons; zero delta blocks |
| `LEDGER_ROW_CHECKS.tsv`, `LEDGER_DELTAS.json` | All 682 exact row identities; zero delta blocks |
| `EXPLICIT_OPERATIONS.json`, `MATH_ALIGNMENT_COUNTS.json`, `MATH_PAIR_CHECKS.tsv` | Literal mutation guards and byte predictions |
| `PAGE199_RECOVERY_CHECK.json` | Page 199 final-script reproducibility |
| `EVENT_CORRESPONDENCE.tsv`, `RECORD_PROGRESS_CORRESPONDENCE.tsv` | Opaque event and record/progress correspondences |
| `REPLAY_AUDIT.py` | Exact final replay driver |

Frozen inputs: `tmp/en182_replay_193_204_20261119/frozen`. Original baseline: `tmp/en182_replay_193_204_20261119/baseline_original`. Final disposable replay: `tmp/en182_replay_193_204_20261119/isolated_verified`.

Command executed from the workspace root:

```sh
python3 -B FGA_CHECK/scripts/replay_en182_193_204.py
```

The driver refuses existing output directories. A new run requires new output paths. Later page 205 or later edits are outside this fixed capture.

## Independent metadata check

A separate agent’s narrow metadata audit completed **PASS at 06:06:53 UTC**. It independently verified all 316 captured files and their exact file set, the original-source copies and 21,869-row ledger prefix, all 682 selected ledger records and their physical serialization, and the published row identities. Page199’s 62 records occupy frozen physical lines 34029–34125 and bytes [7327116,7364806); their concatenated serialized SHA-256 is `cef29800ce154e6c4f70e0ef2c7b870d703aed546484dcc75b58f30a0b4a7392`, equal to replay. Its scope excludes mathematical, translation and source-meaning review. See [independent summary](independent_metadata/SUMMARY.json).
