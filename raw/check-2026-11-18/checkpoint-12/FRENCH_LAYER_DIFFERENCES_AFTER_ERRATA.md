# Completed-French frozen difference navigator

This refresh uses the same frozen source bytes as the `read_through_errata_307` build, captured **2026-11-19T04:46:04.787397+00:00–04:46:04.868173+00:00**. It is an exact, mechanical difference and ledger-text candidate inventory. No content, mathematics, scans or visual output was adjudicated.

## Review entry points

The report directory is `french_layer_differences/snapshot_20261119_044604`.

- `UNMATCHED_REVIEW_INDEX.tsv` is the compact locator index for all **68 hunks without a ledger text candidate** under the existing matcher rules.
- `UNMATCHED_HUNKS.json` and `UNMATCHED_HUNKS.tsv` supply their exact old/new slices, printed-page keys, source-line ranges and byte hashes.
- `UNMATCHED_OTHER_FILES.json` supplies the **55 unmatched hunks outside 149.tex and 212.tex**, which root reports unchanged since capture. This is a report from the fixed snapshot, not a new live comparison.
- `HUNKS.json`/`HUNKS.tsv`, `CANDIDATE_ROWS.tsv`, and `PAGE_HUNK_INDEX.tsv` retain all 303 hunks and their candidate/locator relationships.

**Staleness:** after capture, root reported removal of nine editorial footnotes in corrected French `149.tex` and three in corrected French `212.tex`. The 13 unmatched hunks in these two files are explicitly flagged. Their frozen slices and line numbers must be regenerated before use against the live tree. No later source or ledger changes were read into this report. A text candidate is only a mechanical search result; absence of one is not evidence that a difference lacks a recorded decision.

## Unmatched counts

| Relative file | Unmatched hunks | Post-snapshot status |
| --- | ---: | --- |
| `fr/149.tex` | 10 | Known later corrected-French footnote removals |
| `fr/182.tex` | 9 | Root reports unchanged; no live comparison |
| `fr/190.tex` | 7 | Root reports unchanged; no live comparison |
| `fr/195.tex` | 5 | Root reports unchanged; no live comparison |
| `fr/212.tex` | 3 | Known later corrected-French footnote removals |
| `fr/221.tex` | 15 | Root reports unchanged; no live comparison |
| `fr/232.tex` | 7 | Root reports unchanged; no live comparison |
| `fr/236.tex` | 12 | Root reports unchanged; no live comparison |

## Full inventory and exactness

Of 29 relative file pairs, 19 are identical and 10 are nonidentical. Every nonidentical file is a declared content unit; build/front matter and support metadata remain identical within this frozen pair. The 303 changed hunks comprise 50 with one text candidate, 185 with multiple candidates and 68 unmatched; 81 hunks have only one-sided candidates. There are 909 hunk-to-ledger text links and 8,149 separate locator-only links. No hunk crosses a literal page marker or has differing anchor pages.

All 606 old/new byte slices were checked against their frozen offsets and SHA-256 hashes. All differences reconstruct the other file exactly. No privacy redactions were needed; two colon-plus-control-word matches are preserved as verified TeX syntax and listed in `PRIVACY_TEX_LOOKALIKES.tsv`.

The frozen ledger contains 20,729 data rows. Candidate IDs are tied to its hash; row numbers can change after later edits. The fixed orientation is old/left = `fr`, new/right = `fr_printed`, with no preference implied. The unchanged matcher and candidate limitations are documented in `FRENCH_LAYER_DIFFERENCES.md`.

| Input | SHA-256 |
| --- | --- |
| `fr source tree` | `196f6cd7bad9d57af39c75a0a392fe4a74c897b902fc9a668f3a4451d8d411a5` |
| `fr_printed source tree` | `98eb46a0df6d51fe190c2f6504291f84d28372ce8e5eadd54f5b0bbb9cf01add` |
| `CORRECTIONS.tsv` | `d3a12e44ee34221f973587541f4b7730f422724eb64e8da44196dac76029b943` |

## Reproduction

```sh
python -B FGA_CHECK/scripts/french_layer_differences.py inventory \
  --work tmp/french_layer_difference_after_errata_307 \
  --out tmp/french_difference_report_after_errata_307_recheck
```

For a later live state, run the existing script's `freeze` command first with a new empty destination, then inventory that new frozen root. Preserve this historical report and its hashes.
