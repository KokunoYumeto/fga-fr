# Exact structural repair proposals

Status: **unapplied; no choices selected**. This package proposes repairs for the four defect classes already named in `structural_gate_actions/after_french_20261119_044604`. It does not reassess correction text, statements, mathematics, scans, evidence claims, or reading coverage. No whole structural gate was rerun.

## Frozen scope and provenance

The targeted capture completed at **2026-11-19T05:54:01.099052+00:00**, after two identical reads. `INPUT_CAPTURE.json` binds all 11 frozen files: the corrections ledger, event ledger, record, and eight French source files named by the prior locator report. The captured ledgers contain 22,552 correction rows and 860 event rows; the prior action report covered 20,729 and 786 respectively. Later additions are outside these proposed defect repairs.

`PRIOR_REPORT_HASHES.tsv` records the existing action-report inputs. `ledger_events/PROVENANCE.json` retains the previously verified checkpoint 05 archive/file-list/ledger hashes and exact row provenance. This task revalidated the named current records against those prior identities; it did not repeat the archive or whole-work checks.

## Proposed operations

| Class | Candidates | Treatment |
|---|---:|---|
| C000214 confidence | 3 mutually exclusive alternatives | Root selects `high`, `medium`, or `low`; none inferred |
| Exact duplicate records | 2 deletions | Keep C003871 and C003872; delete second identical occurrences C003873 and C003874 |
| H01/H02 legacy event spelling | 14 replacements | Mechanical spelling candidates; original `how` retained verbatim in `where` |
| H03 event subtype | 9 replacements | Conditional on root's category judgment |
| Source locators, unambiguous section | 53 insertions | Two source pointers per page key; existing section body unchanged |
| Source locators, page 232-149 | 2 alternatives | Root chooses one existing section target |

There are **83 candidate operations**. Selecting one confidence alternative and one 232-149 target, and approving all other candidates, yields 80 operations. The 69 mechanical candidates and 11 owner decisions are recorded separately. None is selected or applied.

## Exact bytes and locators

`PROPOSAL_INDEX.tsv` is the compact index. Exact old/new UTF-8 payloads are in `ledger_events/OPERATIONS.json` and `locators/LOCATOR_OPERATIONS.json`, keyed by operation ID. Encoding each `old_bytes_utf8` or `new_bytes_utf8` string as UTF-8 reconstructs its exact bytes, including original CSV quoting and line endings. Hashes and half-open byte ranges accompany every operation. The ledger/event file also gives full-record identity, occurrence ordinal, field preservation proof, and original-checkpoint provenance. The locator file gives page marker, current source/segment hashes, exact source line ranges, heading identity, and whole-section guard.

### Invalid confidence

C000214 is a valid ten-field record with a 71-byte disallowed confidence value. Its exact old value is in the three `CONFIDENCE_C000214_*` candidates. Only that serialized field is replaced; other field bytes and the record terminator are preserved. Case/whitespace normalization does not produce an allowed category. A category therefore needs root selection. The identical malformed record is present in checkpoint 05 at row C000214 / physical line 410.

### Exact duplicates

| Group | Retain | Delete | Retained physical lines | Deleted physical lines |
|---|---|---|---|---|
| D001 | C003871 | C003873 | 7917-7918 | 7921-7922 |
| D002 | C003872 | C003874 | 7919-7920 | 7923-7924 |

Both complete serialized records in each pair are byte-identical, including their terminators, and both occurrences were already present in checkpoint 05. The delete candidates select occurrence 2 of exactly 2 matching full records. Existing historical reports remain bound to their own file hashes and row numbering. Removing these two rows shifts subsequent current ledger row IDs by two; do not silently reinterpret historical row references under the new numbering. Any derived operation totals should be refreshed only through root's normal record-count workflow after approved changes.

### Legacy event spellings

| Rule | Old lexical form | Proposed `how` | Rows | Review |
|---|---|---|---:|---|
| H01 | `refuted, with refined statement <opaque ID>` | `refuted, with the refined statement's id` | 7 | Mechanical spelling candidate |
| H02 | `refuted, with the refined statement id <opaque ID>` | `refuted, with the refined statement's id` | 7 | Mechanical spelling candidate |
| H03 | `targeted <opaque subtype> check` | `targeted proof check` | 9 | Root judgment required |

These descriptions are lexical templates; each operation stores the complete exact old/new record. Every candidate appends ` | Original how (verbatim): ` plus the complete old `how` value to the end of the existing `where` value. Only the `how` and `where` field bytes change. The other columns and record terminator are unchanged. A canonical event name does not establish that the underlying check or refutation occurred or was valid.

### Missing source locators

The same 54 page keys require 108 pointers: 6 in exposé 149, 25 in 221, 19 in 232, and 4 in 236. `locators/CURRENT_SOURCE_LOCATORS.tsv` includes all exact current ranges and the prior hashes/ranges. Of 108 locators, 102 retain the prior source hash; six corrected-French 149 bindings reflect the footnote cleanup. Only one numeric range moves: `sources/fr/fr/149.tex` at page 149-177 changes from lines 421-475 to 421-472.

The inserted paragraph has this exact structural form, with each candidate's actual paths/ranges substituted:

`Source locators (mechanical snapshot 2026-11-19T05:54:01.099052+00:00): ...`

It adds only source pointers and capture time, with no reading, completion, or evidence claim. It is inserted immediately after the existing heading and blank line, before the unchanged section body.

Page 232-149 has two existing targets, with no automatic preference:

| Candidate | Captured record row | Heading level |
|---|---|---:|
| LOC-232-149-1 | R029502 | 3 |
| LOC-232-149-2 | R031073 | 4 |

The exact heading prefixes and section hashes are in the operation JSON. Either alternative plus the 53 unambiguous candidates passes the targeted source-path-presence check for all 54 selected page keys, in memory only. This does not select a target or validate the record's substantive claims.

## Application constraints for root review

All offsets and row identifiers refer to the frozen input hashes. If production files have changed since capture, resolve and validate the exact full record or section again before using an offset. Ledger/event candidates require the stored full-record hash, occurrence ordinal/count, and old bytes; never perform a global substring replacement. Locator candidates require both source/segment hashes, the correct page/heading occurrence, and the section guard.

Resolve every selected guard against one unchanged input before splicing anything. Some record sections are nested, so applying one insertion before resolving another section can invalidate an otherwise correct section hash. After explicit selection, perform disjoint byte splices in descending offset order per file. Select at most one confidence candidate and exactly one target for 232-149 if repairing that gap. Do not treat H03 as a mechanical equivalence.

No production applicator was run or included. The proposal generators remain in the temporary workspace at `tmp/structural_repair_proposals_20261119/prepare_locators.py` and `tmp/structural_repair_proposals_20261119/ledger_events/prepare_proposals.py`; their hashes are in `GENERATOR_PROVENANCE.tsv`. They only prepare proposals from the fixed inputs. The existing validator remains the later gate after root has reviewed and applied its selected metadata repairs.

## Verification limits

`PACKAGING_CHECKS.json` records exact frozen-range, hash and UTF-8 round-trip checks for every payload and all selected source bindings. `ledger_events/PROPOSAL_CHECKS.tsv` supplies the per-operation results; `locators/LOCATOR_PROPOSAL_CHECKS.json` records the two separate in-memory locator alternatives. No source/ledger/record/event/progress file was written. No semantic or visual review was performed.
