# Mechanical terminology inventory

Captured 2026-11-19T04:34:29.506380+00:00; completed 2026-11-19T04:34:34.417416+00:00.

No translation or French source was edited. This inventory does not count as a paragraph reading, terminology application, mathematical check, or correction-row verdict.

## Decision scope

| Scope | Decisions | High | Medium | Low |
| --- | ---: | ---: | ---: | ---: |
| Entire supplied record | 67 | 38 | 27 | 2 |
| Six FGA translations, including all-language rules | 53 | 31 | 20 | 2 |
| Other language/work scopes | 14 | 7 | 7 | 0 |

Thus **51 high/medium decisions and 2 excluded low-confidence decisions** fall within the six translation scopes. The earlier count of 65 high/medium decisions describes the whole input table; it is not the count applicable to these translations. No application is inferred from these counts.

The five records T001–T005 explicitly have `language=all`, so their literal scope includes English, Spanish, Brazilian Portuguese, Vietnamese, Korean and Simplified Chinese. Their original decisions are retained without rewriting in `DECISION_INVENTORY.tsv`.

The 14 out-of-scope records are T040–T047 (Japanese), T062–T064 (French for translation of other works) and T065–T067 (German). They are retained in the inventory with empty candidate searches rather than silently discarded.

## Search coverage and limits

Searched 161 current translation `.tex` files: 137 exposé/Commentaires/erratum files and 24 ancillary files. Applied 1172 explicitly enumerated, case-sensitive literal strings and recorded 64847 matches. All captured source bytes were rechecked unchanged after searching.

The input counts concern other works and are copied only as provenance, never treated as FGA counts. Each FGA count in this inventory comes from this snapshot. Literal searches preserve whitespace and do not expand TeX. Phrases split by line breaks or commands can be missed. Stems can match larger words; overlapping shorter and longer literals are retained. These are candidate counts, not correction counts.

Rules about all formulas, register, meaning, punctuation outside mathematics, Unicode normalization and formula/character spacing cannot be verified by a finite literal vocabulary. The root reader must examine every paragraph and formula. T001 lists operator-name candidates only; it is not a substitute for the separate mathematical-expression navigator or the scan. T053 includes punctuation candidates both inside and outside formulas without deciding their function.

The two low decisions are reproduced exactly in `TERMINOLOGY_LOW_CONFIDENCE.md`, with the complete lexical candidate tables. No low-confidence choice was applied. Korean `올` produces intentionally broad matches; Chinese absent candidate spellings remain visible with zero counts.

## Files

- `DECISION_INVENTORY.tsv`: all 67 original record rows, applicability and candidate counts.
- `SEARCH_LITERALS.tsv`: every search string and its explicit case variant.
- `LITERAL_OCCURRENCES.tsv`: every match, original line text, byte span, line/column and preceding literal page marker.
- `LOW_CONFIDENCE_OCCURRENCES.tsv`: exact subset for T051 and T055.
- `SOURCE_HASHES.tsv`: file scope, sizes, SHA-256 and NFC diagnostics.
- `INVENTORY.json`: timing, input hashes and totals.

Reproduce from the deliverable parent directory with `python3 -B FGA_CHECK/scripts/terminology_inventory.py --work FGA_CHECK --decisions <supplied-decisions.tsv> --standards <supplied-standards.md> --out FGA_CHECK/terminology_inventory/<new-snapshot-name>`. Input files are not copied into the deliverable.
