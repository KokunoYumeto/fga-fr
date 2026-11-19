# Independent terminology inventory audit

Status: **PASS**, with no failed checks. Completed at 2026-11-19 04:36:12 UTC.

This is a lexical and metadata audit. It does not adjudicate scans, mathematical senses, translation accuracy, paragraph coverage or application of terminology decisions. The audit wrote only its script and reports in its temporary output directory.

## Verified

- All 67 original decision records are copied field for field, with exact record numbers and input-line identifiers.
- The entire input has 38 high, 27 medium and 2 low decisions. The six FGA translation scopes have 53 applicable decisions: 31 high, 20 medium and 2 low. The remaining 14 have 7 high and 7 medium decisions.
- The first five records explicitly have `language=all`; their inventory scope lists all six requested languages. Japanese records and French/German records concerning other work remain present but are outside this translation scope.
- Both low-confidence decisions are reproduced field for field in `TERMINOLOGY_LOW_CONFIDENCE.md`, with an explicit non-application status.
- All 161 translation TeX files are covered: 137 unit files and 24 ancillary files, totaling 4,570,772 bytes. Every size and SHA-256 matches the captured source manifest.
- All 1,172 search-literal identifiers are unique. All 64,847 supplied occurrence locators reproduce the exact source bytes, literal, line, character column, byte column, line context, preceding literal page marker, file scope and language.
- An independent Unicode regex-lookahead search reproduced the entire low-confidence subset: 274 raw matches. All 274 low-confidence Markdown locator rows are exact.
- Source bytes and all inventory artifact bytes remained unchanged during the completed independent audit.
- No email address or absolute host path was detected in the inventory artifacts, low-confidence document or producing script.

## Low-confidence raw matches

| Decision | Literal | Raw matches |
| --- | --- | ---: |
| T051 | 归纳极限 | 1 |
| T051 | 逆极限 | 20 |
| T051 | 余极限 | 0 |
| T051 | 射影极限 | 0 |
| T051 | 正向极限 | 0 |
| T055 | 섬유 | 204 |
| T055 | 섬유곱 | 30 |
| T055 | 의 올 | 0 |
| T055 | 올곱 | 0 |
| T055 | 파이버 | 0 |
| T055 | 올 | 19 |

These are literal matches. The 30 longer Korean product terms overlap their shorter `섬유` matches. The 19 `올` matches are broad lexical candidates and are not classified as mathematical fibre terms by this audit.

## Audit-harness correction

The initial harness expected doubled TeX backslashes, while the revised Markdown correctly retained literal backslashes, and a broad Windows-path pattern overmatched six ordinary TeX control sequences following a colon. The harness was corrected and the complete audit rerun. No source or inventory-data repair was required. The final JSON records those detector false positives explicitly.

## Evidence

- `AUDIT.json`: individual checks, timings, counts and hashes of the audited artifacts.
- `audit.py`: reproducible independent audit using supplied records, current source bytes and the published inventory.
