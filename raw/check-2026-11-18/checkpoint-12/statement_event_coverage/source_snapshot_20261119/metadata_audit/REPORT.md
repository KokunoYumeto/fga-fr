# Statement/event inventory metadata audit

Status: **PASS**. Completed 2026-11-19T04:51:54.770954+00:00.

This audit checks frozen bytes, explicit heading-macro enumeration and locator consistency. It does not decide statement meaning, proof validity, scan readings or whether an event substantively covers a heading.

- 1196 exact heading/list spans verified, including 436 named numbered headings across both French layers.
- All 506 literal result macros and 82 fsection macros have inventory entries. Optional result arguments are included by the producing parser.
- 10 formatted manual numbered headings independently located by a separate line-prefix sweep.
- 786 event records preserved exactly, 5342 event link locators and 668 record link locators verified.
- Candidate counts and unmatched/ambiguous subsets reconcile; no unresolved result-macro parse issue.
- Captured source and record bytes stayed unchanged throughout this audit. No source or main-record edit was made.

Failed checks: 0. Exact check details are in `AUDIT.json`. Source hashes and limitations remain in the inventory's README and tables.
