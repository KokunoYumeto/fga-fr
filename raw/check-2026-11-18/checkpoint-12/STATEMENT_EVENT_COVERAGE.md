# Statement and check-event candidate inventory

The current candidate report is `statement_event_coverage/source_snapshot_20261119/`, captured **19 November 2026 at 04:50:05 UTC**. It covers both French trees, the eight exposés, the Commentaires and all eight errata, together with the check events and page records captured in the same stable read interval. **No source or main-record text was edited.**

This is a lexical navigation report. A matching identifier can be a cross-reference, and an absent identifier match can reflect a grouped event, another name, an unnumbered assertion or a continuation on another page. The inventory does not decide whether a statement was read, proved, corrected or substantively covered.

## Counts

| Item | Corrected French | French as printed | Both layers |
| --- | ---: | ---: | ---: |
| Named numbered headings | 218 | 218 | 436 |
| Core named-heading, remark-member, numbered-paragraph or erratum candidates | 310 | 310 | 620 |
| Candidates with no identifier event match | 4 | 4 | 8 |
| Candidates with multiple matches or a different-page match | 230 | 230 | 460 |
| Candidates without their literal page-record section | 0 | 0 | 0 |

The wider extraction has **1,196 heading/list rows**, including section headings, unformatted line-start reference candidates and bibliography/list labels kept outside the core table. The captured record has **786 check-event rows** and **211 page sections**. There are **5,342 event candidate links** and **668 record candidate links**. Equation tags and source anchors are stored separately and are not counted as named statements.

## Places without an identifier event candidate

The four locations below occur in each French layer. Each has same-page event context and a corresponding page-record section; lack of a named match is not a claim of missing reading or proof.

| Unit and printed page | Source locator in corrected French | Literal heading or label | Same-page event context |
| --- | --- | --- | ---: |
| 182-213 | `sources/fr/fr/182.tex`, line 1004 | `\item[(ii)]` | 4 events |
| 182-213 | `sources/fr/fr/182.tex`, line 1006 | `\item[(iii)]` | 4 events |
| 190-305 | `sources/fr/fr/190.tex`, line 356 | `\result{DÉFINITION}{2.4}` | 6 events |
| e236-303 | `sources/fr/fr/e236.tex`, line 22 | Page 21, § 4: the finiteness heading | 4 events |

The first two are only lexical member candidates associated with the nearest preceding remark heading. That mechanical association is not a determination of their mathematical status. Exact headings, corresponding printed-layer locators and candidate event IDs are in the TSV files.

## What was checked mechanically

The producing parser handles optional arguments to `\result`, identifiers printed in its first argument, `\fsection`, formatted manual headings, paragraph controls such as `\par\noindent`, multiline erratum headings, and explicit list labels. Unformatted line-start references beginning with words such as “proposition” and “théorème” are kept outside named-heading coverage. Bibliography barriers and bracketed bibliography labels are separated from remark-member candidates. Implicit counters are not expanded.

The metadata audit completed **04:52:42 UTC** with no failed checks. It verified all frozen input sizes and hashes, every extracted heading's exact bytes and line/column/page locator, all **506 literal result macros**, all **82 fsection macros**, a separate sweep of formatted manual headings, exact captured event records, candidate foreign keys, record lines and reconciliation of the report's counts. The macro/manual sweeps covered all **34 unit files**, including units without a numbered heading. The captured inputs remained unchanged during the audit. This validation does not adjudicate the semantics of a candidate link.

## Files

Within `statement_event_coverage/source_snapshot_20261119/`:

- `CANDIDATE_COVERAGE.tsv` is the central inspection table, with candidate event IDs and separate counts for identifier matches, same-page matches, different-page matches and page-only context.
- `SOURCE_HEADINGS.tsv` gives exact identifying text, source files, source lines, byte spans and preceding literal page markers.
- `EVENT_CANDIDATES.tsv` and `RECORD_CANDIDATES.tsv` give each link and its literal basis.
- `NO_IDENTIFIER_CANDIDATE.tsv` and `AMBIGUOUS_OR_DIFFERENT_PAGE.tsv` are inspection subsets with no substantive verdict.
- `REPEATED_SOURCE_NUMBERS.tsv` preserves 50 repeated-number groups across the two layers; repeated numbers across different statement types are not automatically errors.
- `EVENTS_WITHOUT_HEADING_IDENTIFIER_CANDIDATE.tsv` holds 280 event rows without a named-heading match. Formula checks, unnumbered claims and other events need not match a named statement.
- `AUXILIARY_IDENTIFIERS.tsv`, `EVENT_LOCATORS.tsv`, `UNIT_SUMMARY.tsv`, `SOURCE_HASHES.tsv`, `PARSER_ISSUES.tsv` and `INVENTORY.json` provide supporting metadata. There are no unresolved result-macro parse issues.
- `metadata_audit_complete_units/AUDIT.json` and `REPORT.md` contain the complete metadata audit. The earlier `metadata_audit/` is retained as an intermediate validation record.

The reproducible scripts are `scripts/statement_event_coverage.py` and `scripts/audit_statement_event_coverage.py`. Four earlier parser-development snapshots are explicitly marked superseded. Use the current snapshot above for counts and inspection. Source or record edits after capture make its locators historical; regenerate the report against the final texts and records before treating them as current.
