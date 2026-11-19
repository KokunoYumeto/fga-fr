# Whole-file page-math selection audit

**PASS** — 2026-11-19T05:53:31.553197+00:00. 69 checks; 0 failures.

Open and close prose groups, nested groups, and lists spanning page markers work with UTF-8 prefixes/content and either LF or normalized CRLF input. All four shifted byte offsets, exact outer/inner payloads, and source-line locators agree with the strict whole-file spans.

On already balanced pages, payloads and locators match the previous helper exactly; show_math output and align_math source/ledger bytes are identical in isolated runs, including printed=True. Current show_math/align_math also work on the newly supported unbalanced prose fragments.

Inline, display-delimited and equation-environment formulas crossing either selected-page edge are rejected without writes. Malformed complete files are rejected even when the defect lies outside the selected page. Actual caller tests cover source, target, and printed-source failures.

The previous three public signatures and the math_ranges implementation are unchanged. All 38 saved production direct calls remain signature-compatible. Whole-file span metadata identifiers retain whole-file scope; the comparison concerns the four documented page-relative byte offsets and line/payload locators.

No production source, ledger or root record was modified or reviewed. Audit details and frozen helper hashes are in AUDIT.json.
