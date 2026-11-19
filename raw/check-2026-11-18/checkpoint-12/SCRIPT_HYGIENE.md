# Scripts-only hygiene review

Snapshot: **2026-11-18 19:56:15 UTC**. The static pass compiled all **132** Python files then present under `scripts/`, with **0 syntax errors, 0 warnings, and 0 remaining literal no-op candidates**. The file set was stable during that pass. These counts describe this recorded snapshot.

No apply script was executed. No edition tree, ledger, audit record, progress entry, scan, or mathematical record was opened by this review. Python source was inspected programmatically; replacement and evidence payloads were not printed or interpreted. No book build, real validator gate, checkpoint, or final deliverable was produced.

## Raw single-quote token review

The current token pass found **zero remaining escaped-apostrophe occurrences in raw single-quoted string tokens** across all 132 scripts. The already-corrected `apply_195_370.py` and `apply_195_371.py` were included, compiled cleanly, and had no remaining matches. There are therefore no remaining token-pattern locations to list from this snapshot.


The requested `apply_195_388.py`, `apply_195_389.py`, `apply_195_390.py`, `update_front_record_through_195.py`, `apply_212_99.py`, `apply_212_100.py`, and optional `apply_212_101.py` were all present when scope was captured at **2026-11-18 19:56:14 UTC**. All seven compiled without errors or warnings and had no literal no-op or raw-single-quote escaped-apostrophe findings. No checker defect was evidenced, and no Python script was changed in this pass.

The scanner looks for an odd-length backslash run immediately before an apostrophe inside raw single-quoted tokens. It covers ordinary raw strings, raw bytes, raw formatted strings, and triple-single-quoted raw strings. It records only filename, token start, occurrence line/column, prefix, and quote kind; it does not print the token payload or infer whether a retained backslash is intentional. Synthetic positive and negative cases passed without executing their code.

No apply script or mathematical string was changed in this pass. No compiler-warning repair was needed. The changes below are earlier, separately verified mechanical repairs.

## Earlier behavior-preserving changes

| Script | Location | Change and verification |
| --- | --- | --- |
| `scripts/apply_182_201.py` | Line 25 | Repaired four invalid escape spellings in a Python string literal. The complete evaluated AST before and after was identical, so every runtime string value was preserved. |
| `scripts/apply_190_300.py` | Line 43 | Removed an exact identity `str.replace` assignment immediately following a decoded-text read. The two replacement arguments were identical literals and the count was literal. The remaining AST was unchanged. |

No deduplication, mathematical replacement, historical entry, confidence value, or execution ordering was changed.

### Script fingerprints

- `scripts/apply_182_201.py`: before `9bf7ae7cd616838965e8946bfe391f330b6c0f67988a9b3416e3091f7d6165bb`; after `2666adb63bc843189f1c34d1eb17fc96463c56b4eff72d8b79d151bde44fccda`.
- `scripts/apply_190_300.py`: before `f3c566af6054c134f8def678a25c825c3fe529f7369c085c714b307f83b15328`; after `01a408fa18aacd997f7aa6d72f829ba7e9c6ce86583af4ee8bccc98e4895f855`.

## Rerun findings

The snapshot contains **110 scripts calling the append helpers** and **33 files with direct append-mode sites**, including the shared helper itself. These are structural findings, not a claim that every rerun necessarily reaches every write: an earlier failed replacement or exception can stop a script first, and a loop may have no items.

The shared helper behavior is decisive:

- `audit_utils.event()` appends a new `CHECK_EVENTS.tsv` row whenever called; it has no duplicate-ID guard.
- `audit_utils.record_page()` appends a `CHECK_RECORD.md` section whenever called, and appends a `progress.log` completion when `done` is true, its default. Neither append checks for an existing record.
- `audit_utils.replace()` has a limited rerun guard: it can return when the old text is absent, a matching ledger record already exists, and the new text is present. When replacement proceeds, it appends a correction row. That guard does not make the surrounding script idempotent, because subsequent event/page appends remain unguarded.

The append-helper callers in this snapshot are `apply_149_169.py` through `apply_149_193.py`, `apply_182_193.py` through `apply_182_220.py`, `apply_190_299.py` through `apply_190_327.py`, `apply_195_369.py` through `apply_195_390.py`, `apply_212_99.py` through `apply_212_101.py`, `amend_149_184_degree.py`, `clarify_195_381_probe.py`, `finalize_149_169.py`. The JSON companion gives each exact call line and its enclosing control-flow context.

Direct append-mode sites outside the shared helper are:

| Script | Append-open line | Target |
| --- | --- | --- |
| `amend_149_184_degree.py` | 6 | `progress.log` |
| `apply_182_202.py` | 33 | `CORRECTIONS.tsv` |
| `apply_190_301.py` | 40 | `CORRECTIONS.tsv` |
| `apply_190_304.py` | 29 | `CORRECTIONS.tsv` |
| `apply_190_305.py` | 26 | `CORRECTIONS.tsv` |
| `apply_190_307.py` | 19 | `CORRECTIONS.tsv` |
| `apply_190_308.py` | 33 | `CORRECTIONS.tsv` |
| `apply_190_309.py` | 30 | `CORRECTIONS.tsv` |
| `apply_190_310.py` | 28 | `CORRECTIONS.tsv` |
| `apply_190_311.py` | 29 | `CORRECTIONS.tsv` |
| `apply_190_312.py` | 51 | `CORRECTIONS.tsv` |
| `apply_190_314.py` | 33 | `CORRECTIONS.tsv` |
| `apply_190_317.py` | 30 | `CORRECTIONS.tsv` |
| `apply_190_319.py` | 30 | `CORRECTIONS.tsv` |
| `apply_190_320.py` | 38 | `CORRECTIONS.tsv` |
| `apply_190_321.py` | 41 | `CORRECTIONS.tsv` |
| `apply_190_322.py` | 36 | `CORRECTIONS.tsv` |
| `apply_190_323.py` | 39 | `CORRECTIONS.tsv` |
| `apply_190_325.py` | 43 | `CORRECTIONS.tsv` |
| `apply_195_370.py` | 30 | `CORRECTIONS.tsv` |
| `apply_195_371.py` | 39 | `CORRECTIONS.tsv` |
| `apply_195_372.py` | 36 | `CORRECTIONS.tsv` |
| `apply_195_373.py` | 35 | `CORRECTIONS.tsv` |
| `apply_195_375.py` | 39 | `CORRECTIONS.tsv` |
| `apply_195_376.py` | 51 | `CORRECTIONS.tsv` |
| `apply_195_379.py` | 57 | `CORRECTIONS.tsv` |
| `apply_195_380.py` | 22 | `CORRECTIONS.tsv` |
| `apply_195_382.py` | 34 | `CORRECTIONS.tsv` |
| `apply_195_383.py` | 47 | `CORRECTIONS.tsv` |
| `apply_195_384.py` | 36 | `CORRECTIONS.tsv` |
| `apply_195_386.py` | 46 | `CORRECTIONS.tsv` |
| `finalize_149_169.py` | 12 | `progress.log` |

These historical apply scripts should not be used as an idempotent rebuild procedure. The current source trees are the build inputs. Changing audit-entry semantics or adding deduplication would require a separate decision; no such change was made here.

## Requested-script control flow and rerun review

The additional AST-only review of the seven requested scripts found **zero provably dead conditional branches, empty literal loops, or directly unreachable statement runs**. It checked constant truth values and literal comparisons without evaluating script code. Runtime-dependent conditions and the correctness of replacement values remain outside this result.

The six apply scripts have the following append-helper calls at module level, with no enclosing conditional. These are unsafe to treat as an idempotent rerun procedure: if execution reaches them again, the shared helpers append again. Earlier exceptions or replacement checks can prevent execution from reaching them.

| Script | Event-call lines | Page-record call line |
| --- | --- | --- |
| `apply_195_388.py` | 63–69 | 70 |
| `apply_195_389.py` | 43–48 | 49 |
| `apply_195_390.py` | None | 18 |
| `apply_212_99.py` | 22–24 | 25 |
| `apply_212_100.py` | 31–33 | 34 |
| `apply_212_101.py` | 21–22 | 23 |

`update_front_record_through_195.py` has no direct append-mode or append-helper site. Its write is at line 40. The assertion at line 14 rejects a text marker already present, and a literal-only comparison confirmed that the marker is included in the rows inserted by that script. Thus an ordinary rerun after a successful insertion is stopped by the assertion; Python optimization disables assertions, so the guard does not establish safety under optimized execution or for arbitrary prior file states. No record content was opened to make this structural observation.

These seven files still matched their compile-pass hashes when this report was updated. The JSON stores the captured scope, method limits, call locations, and targeted results. The targeted control-flow supplement belongs to this snapshot; the standalone checker command below regenerates its standard compile/token/append report.

## Repeating the static check

`scripts/script_hygiene.py` compiles code objects and inspects syntax trees without importing or executing the inspected scripts. It does not print source lines or literal replacement values. The JSON report records per-script hashes, compile results, warnings, literal no-op candidates, escaped-apostrophe raw-token locations, append-mode sites, and append-helper calls.

```sh
python -B work/scripts/script_hygiene.py --report work/SCRIPT_HYGIENE.json
python -B work/scripts/script_hygiene.py --selftest
```

The synthetic selftest confirmed warning, literal no-op, append-mode, helper-call, and raw single-quote token detection without executing its fixture code. Static detection is intentionally limited: valid Python escape sequences with unintended meaning are not diagnosed, runtime-dependent no-ops are not inferred, and a method with equal literal arguments is only a candidate until its receiver and side effects are established.

## Earlier checkpoint 04 metadata readiness

The following observations were recorded at 19:24 UTC before checkpoint 04 and were not rechecked in this static-only pass. No checkpoint 05 action was performed.

Checkpoint 04 is due **2026-11-18 19:33:19 UTC**. The checkpoint packager compiled cleanly and its help interface ran. The destination directory exists and passed a write/access metadata check; `checkpoints/FGA_CHECK_checkpoint_04.zip` does not exist. All required top-level work items are present. Checkpoints 01, 02, and 03 remain present and were not opened or changed. The private transfer helper remains available.

A filename/stat-only walk of the default checkpoint scope observed **434 files** and **10,159,123 uncompressed bytes**, with **62,263,115,776 filesystem bytes free**. These are observed metadata totals, not a content audit or an actual ZIP-size result; ongoing work and this report update can change them.

The packager's content-reading plan was deliberately not run. Hashes, content privacy, compression, ZIP integrity, and the durable save remain for the actual checkpoint operation. No checkpoint or archive was created by this review.

```sh
python -B work/scripts/checkpoint_zip.py --number 4 --not-before 2026-11-18T19:33:19Z
```

## Earlier final-packaging review (not rerun in this pass)

The existing `final_zip.py` implementation and `FINAL_PACKAGING.md` agree with the mechanical inventory rules reviewed:

- The final archive includes the complete current deliverable snapshot. It omits no unchanged deliverable in favor of an older checkpoint, so no checkpoint is needed to recover an included file.
- Existing checkpoints and final archives are preserved. Earlier ZIPs, original input archives, runtime/cache material, renders, and excluded intermediates are not nested in the final archive.
- A fresh enforcing validator run and hash-matching inventories are mandatory. Every inventoried source file and each of the eleven distinct layer PDFs must be included.
- The manifest names every included member, with its size and SHA-256. Its own self-hash is deliberately omitted, and the command reports the detached manifest hash.
- The candidate must be strictly below 500,000,000 bytes. Member inventory, manifest consistency, CRC, all member hashes, and work stability are checked before exclusive no-overwrite publication.

The earlier final-packaging synthetic selftest passed. It used temporary fixtures only and exercised gate/schema consumption, all eleven PDF entries, exclusions, complete manifests and hashes, CRC integrity, dry-run nonpublication, size refusal, existing-archive preservation, changed-work refusal, and prior-checkpoint preservation.

Remaining mechanical limits are explicit: multipart output is not implemented, so an oversize candidate is refused; fresh validation requires the original supplied archives to remain available outside the final ZIP; work should be paused during packaging rather than relying on a transactional filesystem lock; and the helper creates the ZIP but does not perform its durable file save. Its gate also cannot establish human page reading, second-reading verdicts, mathematical or translation accuracy, current-source PDF provenance, visual checks, or inline-credit review. Those limits are documented rather than treated as completed checks.

