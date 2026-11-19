# Supplementary candidate links for unmatched French hunks

Original hunk snapshot: 2026-11-19T04:46:04.787397+00:00. Current source/ledger capture: 2026-11-19T05:01:08.968875+00:00.

This report considers exactly the original 68 unmatched hunks, including 55 outside exposés 149 and 212. It uses the current correction ledger, preserving exact row payloads and hashes, and checks current source-file hashes and occurrence of the old hunk payloads. **No source or ledger was edited; no correction was adjudicated.**

## Results

- 56 hunks have at least one paired lexical candidate under the declared projections.
- 12 have no pair; their same-page corrected-French operations are listed in ledger append order.
- 335 candidate links refer to 104 distinct ledger rows. Multiple profiles, directions and local edits can link the same row.
- 158 exact ledger payloads are included, only for these unmatched hunks and their fallback histories.

## Normalization is a search aid

P0 collapses ASCII whitespace. P1 additionally removes exact balanced `\symup{...}` wrappers. P2 also removes `\uline{...}`. P3 additionally looks through `\underline{...}` and `\uwave{...}`. No other wrapper, macro, alphabet, index, sign, word, punctuation or footnote is removed or substituted. Alphabet controls such as `\mathcal`, `\mathfrak`, `\mathbf`, `\mathrm` and `\operatorname` remain literal and are checked unchanged by projection.

Underlines and upright letters can distinguish mathematical notation. Every removal is retained as field-level metadata with positions and argument hashes, and sensitive-decoration removals are flagged. A projection that collapses a hunk difference is reported explicitly, never treated as proof of equivalence.

A full-payload pair means both projected ledger fields occur on opposite hunk sides with at least one distinguishing occurrence. A localized edit pair uses an actual differing block of the projected ledger operation, with up to 48 characters of matching adjacent context; both fragments must be at least eight characters. Such a fragment is only a candidate for part of the hunk, not evidence that its entire net difference is accounted for. Page mismatches and repeated occurrences remain visible.

## History and direction

The hunk direction is corrected French to printed French. Ledger operation directions are reported separately as printed-to-corrected or corrected-to-printed. A reverse match can represent restoration or withdrawal and must not be mistaken for a surviving correction.

For hunks without a pair, `FR_CORRECTED_PAGE_HISTORY.tsv` retains all corrected-French rows for the exact file/page in ledger order. `FR_ONLY_OPERATION_HISTORY.tsv` selects rows with no byte-identical old/new counterpart in the printed layer on that page. This is a mechanical distinction, not a judgment about which operation changes meaning. The exact payload collection includes this latter set.

## Snapshot limits

The original ledger had 20729 rows; the captured current ledger has 20939. Original row hashes remain an unchanged prefix: True. Current ledger SHA-256: `7e0e76f752bd7d79ecba5d51b3cfcaec97bda738ab7380da3eb73a774e3d4584`. Original hunk-snapshot ledger SHA-256: `d3a12e44ee34221f973587541f4b7730f422724eb64e8da44196dac76029b943`.

Root reported twelve editorial-footnote removals in corrected French 149 and 212 after the hunk snapshot. The report does not delete footnotes from hunk text or pretend the old hunks are current. `CURRENT_SOURCE_STATUS.tsv` and `HUNK_STATUS.tsv` show actual current hashes and exact-payload survival. The original hunk payload no longer occurs in current corrected French for 3 of the 68 hunks. All links still refer explicitly to the original 68 hunks. Regenerate the main layer diff for a final current net-difference accounting.

## Review files

- `REVIEW.md`: paired source payloads and links to candidate or fallback ledger rows.
- `LEDGER_PAYLOADS.md` and `.json`: exact current-ledger old/new/evidence fields, row IDs, physical lines and hashes.
- `CANDIDATE_LINKS.tsv`, `CANDIDATE_DETAILS.json`: candidate direction, profile, actual paired fragments and normalization metadata.
- `HUNK_STATUS.tsv`, `HUNK_PAYLOADS.json`, `HUNK_PROJECTIONS.json`: original hunk identity and projected navigation views.
- `FR_CORRECTED_PAGE_HISTORY.tsv`, `FR_ONLY_OPERATION_HISTORY.tsv`: append-order fallback history.
- `CURRENT_SOURCE_STATUS.tsv`, `NORMALIZATION_PROFILES.json`, `INVENTORY.json`: input binding, declared rules and timing.

Projected fragment offsets in `CANDIDATE_DETAILS.json` are character indices in the declared projected ledger fields, not byte offsets in the original sources. Original source/ledger locators and original payload hashes remain separate. `POST_SNAPSHOT_FRENCH_ROWS.tsv` lists the twelve appended French rows and their hashes without extending the original hunk set.
