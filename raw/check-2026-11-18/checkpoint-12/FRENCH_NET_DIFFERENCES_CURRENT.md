# Current French corrected-versus-printed difference inventory

The refreshed inventory is bound to the two-read snapshot captured **2026-11-19 05:08:12 UTC**. Its directory label `050704` is a job label, not the capture timestamp. Sources and the correction ledger were read only. Earlier snapshots and the earlier supplementary audit are preserved.

There are **303 exact line-difference hunks** in ten content files, with corrected French as old/left and printed French as new/right. All 303 map uniquely to the previous 04:46:04 snapshot: **291 retain the exact payload pair**, six retain the same printed span with a changed corrected payload, and six have a current printed span contained in the old span. The FD strings happen to remain the same; identifiers must still be qualified by snapshot. See the [complete current-to-old table](french_layer_differences/snapshot_20261119_050704/continuity/CURRENT_TO_OLD.md).

## Footnote-removal continuity

The twelve recorded deletions, `C020730`–`C020741`, account byte for byte for all source changes between the two snapshots: nine operations in corrected `149.tex`, three in corrected `212.tex`. Replaying their literal operands in memory, with only the ledger-to-source newline conversion declared in the report, reproduces both current files exactly. All printed files and all other French source-tree files are unchanged. The [footnote table](french_layer_differences/snapshot_20261119_050704/continuity/FOOTNOTE_REMOVALS.md), [exact ledger operations](french_layer_differences/snapshot_20261119_050704/continuity/FOOTNOTE_OPERATIONS.json), and [reconstruction hashes](french_layer_differences/snapshot_20261119_050704/continuity/FOOTNOTE_REPLAY.json) record this byte relationship without judging any note or correction.

## Candidate searches

| Search result | Current count |
|---|---:|
| Exact line-difference hunks | 303 |
| One ordinary ledger candidate | 49 |
| Multiple ordinary ledger candidates | 185 |
| No ordinary ledger text candidate | 69 |
| Ordinary links | 895 |
| Hunks with only one-sided ordinary candidates | 80 |
| Ordinary-unmatched hunks with a declared-projection pair | 57 |
| Ordinary-unmatched hunks without such a pair | 12 |
| Declared-projection links / distinct candidate ledger rows | 339 / 105 |

“Ordinary” refers to the unchanged exact-pair, distinguishing-substring, ASCII-whitespace and one-sided matcher. Its unmatched count is separate from the supplementary formatting search. The refreshed formatting search uses the earlier declared profiles and preserves alphabet commands. Formatting removals are recorded and can erase notational distinctions; no projection establishes semantic equivalence.

Of the 57 supplementary paired cases, 49 have at least one whole-ledger-operand substring pair and eight have only local edit-fragment pairs. Only `FD000014`, `FD000103`, `FD000170`, and `FD000298` have a pair equal to both entire projected hunk payloads. These are lexical observations, not net-coverage findings.

The twelve earlier no-pair cases retain exact payloads and again produce no pair: `FD000012`, `FD000020`, `FD000068`, `FD000087`, `FD000127`, `FD000141`, `FD000183`, `FD000198`, `FD000224`, `FD000231`, `FD000236`, and `FD000281`. The [twelve-case table](french_layer_differences/snapshot_20261119_050704/continuity/PREVIOUS_NO_PAIR.md) gives current source lines and append-order history links. Lack of a literal candidate does not establish a missing correction, proof, or reading.

`FD000002` became ordinary-unmatched after its footnote was removed; its refreshed formatting search finds seven local-fragment links to `C000212` and `C000260`. Of the previous 335 supplementary links, 332 still satisfy the stored projected-fragment predicate. `FM000007`, `FM000010`, and `FM000013`, all linking old `FD000005` to `C000549`, no longer do. See [old-link revalidation](french_layer_differences/snapshot_20261119_050704/continuity/OLD_FORMAT_LINK_REVALIDATION.tsv) and the [current unmatched review table](french_layer_differences/snapshot_20261119_050704/continuity/CURRENT_UNMATCHED_REVIEW.md).

## Frozen input and validation

The frozen ledger has **21,269 data rows**; the earlier 20,729 row hashes remain an unchanged prefix. Ledger SHA-256: `25fd221d32f32383d6ff285c1f36bea3b3a64483e4a41866f7bf7854bbbea6d5`.

A separate validator completed **PASS at 05:15:51 UTC**, checking 1,212 old/current exact hunk slices, 895 ordinary links, 339 current formatting links, 1,230 projection reconstructions, all 303 mappings, and the twelve literal deletions. It did not import the producing mapping or projection helpers. See [validation report](french_layer_differences/snapshot_20261119_050704/continuity/metadata_audit/REPORT.md) and [exact checks](french_layer_differences/snapshot_20261119_050704/continuity/metadata_audit/AUDIT.json).

The snapshot limits all claims to its captured bytes. Later ledger appends or source changes require comparison to these hashes. This report provides mechanical candidates for root inspection; it makes no mathematical, translation, correction-validity, reading-completeness, or full-net-difference coverage judgment.

## Entry points

- [Exact hunk payloads and locators](french_layer_differences/snapshot_20261119_050704/HUNKS.json)
- [Exact ordinary candidate links and row hashes](french_layer_differences/snapshot_20261119_050704/CANDIDATE_ROWS.tsv)
- [Fresh inventory guide and reproduction commands](french_layer_differences/snapshot_20261119_050704/README.md)
- [Continuity and refreshed formatting-search guide](french_layer_differences/snapshot_20261119_050704/continuity/README.md)
