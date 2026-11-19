> Superseded mechanical parser-development snapshot. Use `statement_event_coverage/source_snapshot_20261119/` for the corrected candidate inventory. Earlier snapshots include intentionally retained parser diagnostics and must not be used as current heading counts.

# Statement and event candidate coverage

Captured 2026-11-19T04:48:13.034522+00:00; completed 2026-11-19T04:48:17.192879+00:00. The source snapshot includes both French layers, all eight exposés, the Commentaires and all eight errata. Records were captured in the same stable two-read interval. No source or main-record file was edited.

## Scope

This is a lexical navigator, **not a certificate of reading, proof, mathematical validity or correction coverage**. A missing identifier match can reflect another name, an unnumbered assertion, a grouped event, a continuation on another page, or parser limitations. A match can be a cross-reference to a different statement. All links require the root reader's inspection.

The parser records literal `\result` arguments, including optional separator arguments, numbered identifiers in a first argument, section headings, manual line-start named headings, erratum page/line locators, explicit list labels and implicit list markers. It retains both numbered and unnumbered named headings. A list member is only associated with the nearest preceding lexical heading; this is not a decision that it is an independent statement or part of that heading's mathematics. Section and other list labels remain in `SOURCE_HEADINGS.tsv` but are outside the main named-heading candidate coverage table.

The exact heading bytes, file, line, byte range and nearest preceding literal page marker are retained. Plain projections remove TeX control words and braces only for navigation; they do not expand TeX. Equation tags and literal labels/anchors are separate in `AUXILIARY_IDENTIFIERS.tsv` and are not counted as named statements. Implicit list counters are not expanded.

## Snapshot totals

- 1198 source heading/list rows across both layers, including 434 named numbered headings.
- 626 named-heading, remark-member or erratum candidate entries.
- 786 captured check-event rows; 211 page sections in the check record.
- 5402 event candidate links and 674 record candidate links.
- 8 entries have no identifier event candidate; 466 have multiple candidates or a different-page identifier match. These are navigation flags only.
- 280 event rows have no named-heading identifier candidate; events concerning formulas, general claims, typography or cross-work links naturally need not match a named heading.
- 54 repeated source-number groups, counted separately by layer and unit. Reused numbers across theorem types, remark members and erratum locators are not automatically errors.
- 0 unresolved result-macro parse issues.

## Candidate rules

An event is considered only when its ID or locator contains the same literal unit. Identifier candidates come from bounded identifier tokens in the event ID, a named identifier in `where` or `result` using an explicit French/English label-alias list, or an erratum target/roman-label match. The report separately records agreement, disagreement or absence of an extracted printed-page locator. Same-page links without identifier matches are labelled page-only context and do not count as identifier coverage. Repeated source identifiers and multiple events are retained rather than guessed apart.

For the check record, the exact page-section key supplies context. Within that section, named identifiers, unit-identifier tokens and explicit erratum targets are lexical candidate lines. A page section without such a line is reported only as page-section context. The absence of a named identifier in prose does not imply that the statement was not read.

## Files

- `SOURCE_HEADINGS.tsv`: every extracted heading and list label, with exact identifying text and offsets.
- `AUXILIARY_IDENTIFIERS.tsv`: equation tags, labels and source anchors.
- `CANDIDATE_COVERAGE.tsv`: the root reader's central candidate table.
- `EVENT_CANDIDATES.tsv`, `RECORD_CANDIDATES.tsv`: every candidate link and its literal basis.
- `NO_IDENTIFIER_CANDIDATE.tsv`, `AMBIGUOUS_OR_DIFFERENT_PAGE.tsv`: subsets for inspection, with no substantive verdict.
- `REPEATED_SOURCE_NUMBERS.tsv`: source-number collision groups.
- `EVENTS_WITHOUT_HEADING_IDENTIFIER_CANDIDATE.tsv`: event rows outside the named-heading match set.
- `EVENT_LOCATORS.tsv`, `UNIT_SUMMARY.tsv`, `SOURCE_HASHES.tsv`, `PARSER_ISSUES.tsv`, `INVENTORY.json`: metadata, locators, integrity and parser diagnostics.

## Reproduction and freshness

Run `python3 -B FGA_CHECK/scripts/statement_event_coverage.py --work FGA_CHECK --out FGA_CHECK/statement_event_coverage/<new-snapshot> --frozen tmp/<new-frozen-inputs>`. Use new output names; the script never overwrites a snapshot. The full immutable input capture is held only in the temporary workspace; the deliverable records its hashes and exact extracted heading text.

Live inputs changed after capture: 0. This is expected if the root reading continues; the report remains tied to its captured hashes. Regenerate against final sources and records before using locators as current.
