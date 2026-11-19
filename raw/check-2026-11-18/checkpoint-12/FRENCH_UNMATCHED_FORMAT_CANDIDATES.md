# Supplementary links for unmatched French differences

The report is `french_unmatched_format_candidates/snapshot_20261119/`. It starts from the **68 unmatched hunks** in the French-layer snapshot captured at **04:46:04 UTC on 19 November 2026**, and compares them with a fresh source/ledger capture at **05:01:08 UTC**.

**No source or ledger was edited. No candidate was adjudicated as a valid correction.** These are links for the root reader's net-difference review.

## Result

| Scope | Original unmatched hunks | Hunks with a paired lexical candidate | Still without a pair |
| --- | ---: | ---: | ---: |
| All eight exposés | 68 | 56 | 12 |
| Excluding 149 and 212 | 55 | 45 | 10 |

There are **335 candidate links to 104 distinct ledger rows**; every link is on the same recorded page as its hunk. The report includes **158 exact ledger payloads**, only for candidate rows or fallback histories associated with these unmatched hunks.

For 49 hunks, both entire projected ledger operands occur on the respective hunk sides. For seven hunks, only a context-bearing local edit fragment was found: FD000023, FD000057, FD000100, FD000219, FD000244, FD000246 and FD000270. **Neither category establishes that the complete net hunk difference is accounted for.** Only FD000014, FD000103 and FD000298 have a candidate whose two projected operands equal the two whole projected hunk payloads; those still require source and mathematical review.

## Declared search projections

| Profile | Only these balanced wrappers are removed | Hunks first finding a pair here |
| --- | --- | ---: |
| P0 | None; ASCII whitespace collapse only | 17 |
| P1 | `\symup{...}` | 33 |
| P2 | `\symup{...}`, `\uline{...}` | 5 |
| P3 | `\symup{...}`, `\uline{...}`, `\underline{...}`, `\uwave{...}` | 1 |

The only hunk first linked under P3 is **FD000017**, to **C000872**. It deserves explicit inspection of the preserved underline distinction. Underlines and upright letterforms can carry mathematical meaning; removal for a search projection does not declare them equivalent.

Every removed wrapper is recorded with its original positions and argument hash. Alphabet controls such as `\mathcal`, `\mathfrak`, `\mathbf`, `\mathrm` and `\operatorname` remain literal, and their sequence was checked unchanged in each projection. No footnote, word, punctuation, index, sign or other macro is removed. Actual original old/new ledger payloads are preserved separately.

Candidate direction is explicit because the hunk runs **corrected French → printed French**, while a ledger row records its own **old → new** operation. A reverse-direction match can be a restoration or withdrawal; it is not automatically a surviving original correction.

## Remaining twelve hunks

| Hunk | Printed page | Corrected-French operations lacking an identical printed-layer counterpart |
| --- | --- | ---: |
| FD000012 | 149-177 | 7 |
| FD000020 | 149-179 | 3 |
| FD000068 | 182-205 | 7 |
| FD000087 | 190-300 | 1 |
| FD000127 | 190-325 | 2 |
| FD000141 | 195-376 | 4 |
| FD000183 | 221-252 | 2 |
| FD000198 | 221-260 | 12 |
| FD000224 | 221-269 | 5 |
| FD000231 | 221-271 | 8 |
| FD000236 | 221-272 | 4 |
| FD000281 | 236-231 | 4 |

Their fallback histories contain **722 corrected-French operation links**, in ledger append order. Of these, **59** have no byte-identical old/new operation recorded in the printed layer on the same page. The latter rows have complete linked payloads. This mechanical counterpart test does not decide whether an operation changes meaning, and the sequence is not presented as a reconstructed net change.

## Snapshot limits

The old ledger's **20,729 row hashes remain an unchanged prefix** of the captured current ledger's **20,939 rows**. Twelve appended French rows record the later footnote removals. Their row IDs and hashes are in `POST_SNAPSHOT_FRENCH_ROWS.tsv`.

Actual source hashes show that only `sources/fr/fr/149.tex` and `sources/fr/fr/212.tex` changed after the original hunk snapshot. The original corrected-French hunk payload no longer occurs in the current file for **FD000005, FD000038 and FD000170**. Other old payloads in those files can survive with shifted line positions. The report keeps the old hunks explicit and does not remove footnotes to manufacture a current match. A fresh main French-layer diff is needed for final net-difference accounting.

Current captured ledger SHA-256: `7e0e76f752bd7d79ecba5d51b3cfcaec97bda738ab7380da3eb73a774e3d4584`.

Original hunk-snapshot ledger SHA-256: `d3a12e44ee34221f973587541f4b7730f422724eb64e8da44196dac76029b943`.

## Review and validation

Start with `REVIEW.md` in the report directory. Each hunk shows both exact source payloads and links to `LEDGER_PAYLOADS.md`; the JSON version preserves the same exact old/new/evidence fields, IDs and hashes. `CANDIDATE_DETAILS.json` records the actual matched fragments and projection metadata. Fragment offsets are character positions in the declared projected ledger fields, not original source-byte offsets.

The metadata audit passed at **05:04:52 UTC**, with no failed checks. It reconstructed **1,214 projections** directly from their declared wrapper-deletion ranges, verified all **335 literal candidate links**, all **158 exact payload rows**, all **722 history links**, hunk/ledger hashes, source locators, fragment ranges, occurrence counts and current-payload survival counts. Alphabet-control sequences were preserved in every reconstruction. Audit evidence is in `metadata_audit/AUDIT.json` and `REPORT.md`.

The producing and validation scripts are `scripts/french_unmatched_format_candidates.py` and `scripts/audit_french_unmatched_candidates.py`. They make no mathematical, translation or correction-validity judgment.
