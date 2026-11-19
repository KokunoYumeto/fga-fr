# Frozen French net-difference inventory

Capture: **2026-11-19T05:08:12.450298+00:00** through **05:08:12.468587+00:00**, with two consecutive identical complete reads. The `050704` directory suffix is a job label. Orientation: corrected `fr` is old/left; `fr_printed` is new/right. These are line-difference hunks, not adjudicated correction units.

## Exact inventory

There are 29 relative file pairs: 19 identical pairs and ten differing content files. The differing files contain **303 hunks**. The unchanged ordinary matcher finds 49 hunks with one candidate, 185 with multiple candidates, and 69 without a text candidate. It reports 895 candidate links, 8,253 locator-only links, and 80 hunks with only one-sided candidates. No hunk crosses a literal page marker or has different left/right anchor pages. No payload was redacted; two TeX colon/control-word lookalikes were retained as recorded in PRIVACY_TEX_LOOKALIKES.tsv.

| Artifact | Contents |
|---|---|
| `HUNKS.json` / `HUNKS.tsv` | Exact old/new payloads, hashes, byte spans, source lines, literal page anchors, candidate IDs |
| `FILES.tsv` | File hashes, sizes, categories, equality and reconstruction status |
| `CANDIDATE_ROWS.tsv` | Ordinary lexical links, ledger row hashes, physical-line locators, matching directions |
| `PAGE_HUNK_INDEX.tsv` / `MATCH_STATUS.tsv` | Page and candidate-status navigation |
| `LOCATOR_ONLY_CANDIDATES.tsv` | Same-file/page rows for hunks without ordinary text links; not text matches |
| `UNMATCHED_HUNKS.json` / `.tsv` | The 69 current ordinary-unmatched hunks |
| `SUMMARY.json` / `FROZEN_SNAPSHOT.json` | Capture and source-tree hashes; full frozen input manifest |
| `continuity/CURRENT_TO_OLD.md` / `.tsv` | All 303 current-to-earlier FD mappings |
| `continuity/CHANGED_HUNKS.json` | Exact earlier/current payloads for the twelve changed hunks |
| `continuity/FOOTNOTE_REMOVALS.md` | The twelve recorded deletions, source lines, mapped FD identifiers |
| `continuity/PREVIOUS_NO_PAIR.md` | Current mapping of the previous twelve supplementary no-pair cases |
| `continuity/CURRENT_UNMATCHED_REVIEW.md` | Current supplementary candidate and history navigation |
| `continuity/metadata_audit/` | Separate byte, mapping, projection and locator validation |

## Snapshot hashes

- Ledger rows: **21,269**.
- Ledger SHA-256: `25fd221d32f32383d6ff285c1f36bea3b3a64483e4a41866f7bf7854bbbea6d5`.
- Corrected French tree SHA-256: `80622703811ebf5bede6e9cca6f02e73a5c5c6eab8a674f47fc0185f9cf5917e`.
- Printed French tree SHA-256: `98eb46a0df6d51fe190c2f6504291f84d28372ce8e5eadd54f5b0bbb9cf01add`.
- Frozen manifest SHA-256: `a42e84a95929950cd3452a4c98745251a27c0b9fa3fc67aaab65f15bb9a18705`.

The earlier snapshot `snapshot_20261119_044604` and the supplementary report `french_unmatched_format_candidates/snapshot_20261119` remain unchanged. The current-to-old mapping is unique for every hunk; all FD strings happen to remain identical, but the twelve changed payloads make snapshot qualification necessary.

## Commands executed

Run from the workspace root. Each generation command requires a new output directory; these commands record the completed run and are not intended to overwrite its artifacts.

```sh
python3 -B FGA_CHECK/scripts/french_layer_differences.py freeze --work FGA_CHECK --out tmp/french_layer_difference_refresh_20261119_050704
```

```sh
python3 -B FGA_CHECK/scripts/french_layer_differences.py inventory --work tmp/french_layer_difference_refresh_20261119_050704 --out FGA_CHECK/french_layer_differences/snapshot_20261119_050704
```

```sh
python3 -B FGA_CHECK/scripts/french_layer_refresh_mapping.py --old-report FGA_CHECK/french_layer_differences/snapshot_20261119_044604 --current-report FGA_CHECK/french_layer_differences/snapshot_20261119_050704 --old-frozen tmp/french_layer_difference_after_errata_307 --current-frozen tmp/french_layer_difference_refresh_20261119_050704 --supplement-report FGA_CHECK/french_unmatched_format_candidates/snapshot_20261119 --supplement-frozen tmp/french_unmatched_format_frozen --out FGA_CHECK/french_layer_differences/snapshot_20261119_050704/continuity
```

```sh
python3 -B FGA_CHECK/scripts/audit_french_layer_refresh.py --report FGA_CHECK/french_layer_differences/snapshot_20261119_050704/continuity --out FGA_CHECK/french_layer_differences/snapshot_20261119_050704/continuity/metadata_audit
```

## Limits

Candidates are lexical links to the frozen ledger, not decisions that a correction is valid or fully records a net hunk difference. One-sided and local-fragment candidates are labeled separately. The line-difference segmentation can shrink or merge when text is removed; the mapping reports the actual printed-side coordinate relation. Literal page-marker anchors are mechanical locators, not scan adjudication. Later changes require comparison with this snapshot. No sources or ledger were changed by these scripts; no programme, notes, or Stacks context was opened.
