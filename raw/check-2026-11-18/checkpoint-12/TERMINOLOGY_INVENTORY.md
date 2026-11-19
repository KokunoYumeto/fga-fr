# Terminology candidate inventory

The supplied record has **67 decisions**. Its literal language scope places **53** within the six FGA translations: **31 high, 20 medium and 2 low**. The applicable high/medium count is **51**. The other 14 concern Japanese, French translation of other works and German; they remain visible in the inventory. The five all-language rules explicitly include all six FGA translation languages.

The inventory is a mechanical navigation aid. No source text was changed, no terminology decision was applied, and no paragraph or mathematical meaning was adjudicated by this work. The two low-confidence decisions remain excluded from application.

## Snapshot and validation

The translation files were captured on 19 November 2026 at **04:34:29 UTC**. The snapshot covers **161 TeX files**: 137 unit files and 24 ancillary files. A list of 1,172 explicit literal search strings produced **64,847 raw candidate matches**. The producing script checked that all captured sources remained unchanged during the search.

An independent lexical audit completed at **04:36:12 UTC** with no failed checks. It verified the exact 67 input records, scope counts, source sizes and hashes, all occurrence locators, and a separately enumerated low-confidence subset. This audit does not certify translation accuracy or paragraph coverage.

## Low-confidence candidates

| Decision | Raw literal matches | Different source starting positions | Source lines | Files |
| --- | ---: | ---: | ---: | ---: |
| T051, Chinese limit terms | 21 | 21 | 21 | 4 |
| T055, Korean fibre terms | 253 | 223 | 215 | 9 |

The Chinese matches comprise 20 occurrences of 逆极限 and one of 归纳极限. The Korean raw total includes 204 occurrences of the substring 섬유, 30 longer 섬유곱 matches nested within those occurrences, and 19 broad 올 substring matches. Those 19 are lexical candidates, not classified mathematical fibre terms. Candidate counts must not be reported as correction counts.

## Files and limits

- `TERMINOLOGY_LOW_CONFIDENCE.md` reproduces both low decisions field for field and lists every occurrence of the stated search strings.
- `terminology_inventory/snapshot_20261119_initial/DECISION_INVENTORY.tsv` retains all 67 input records with applicability and candidate counts.
- `SEARCH_LITERALS.tsv` and `LITERAL_OCCURRENCES.tsv` in that directory give the exact queries and byte/line/page-marker locators.
- `SOURCE_HASHES.tsv` and `INVENTORY.json` record the snapshot, input hashes and source integrity checks.
- `independent_audit/AUDIT.json` and `REPORT.md` in that directory contain the independent validation evidence.
- `scripts/terminology_inventory.py` and `scripts/audit_terminology_inventory.py` reproduce the inventory and its independent checks.

Literal searches do not expand TeX or join phrases across line breaks. They retain overlapping strings, compounds, ancillary material and potentially irrelevant senses. Page locators use the preceding literal source marker and therefore inherit any missing-marker problem. Formula, register, punctuation, spacing and meaning rules require the root reader's full sequential reading. Source edits after this snapshot make its source hashes and line locators historical; regenerate the inventory for a final current-text check.
