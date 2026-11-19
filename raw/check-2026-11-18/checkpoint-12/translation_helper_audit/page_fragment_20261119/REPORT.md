# Translation helper page-fragment audit

**PASS** — 2026-11-19T05:42:20.704893+00:00. 45 checks; 0 failures.

Synthetic tests confirm open and close fragments for all six classified nonmath environments are accepted only with the fragment flag; mathematical delimiter, brace, environment and classification errors remain rejected. Real calls to the frozen helper copies against isolated synthetic files reject crossed whole-file nonmath environments and malformed math outside the selected page, for either source or target, without changing any isolated source or ledger. Math extending across a page boundary is still rejected at fragment extraction. Both open and close list-page cases work through show_math and align_math, including printed=True.

The two existing caller signatures are unchanged; math_ranges adds only page_fragment=False. All 33 saved direct calls bind to the current signatures. Existing one-argument math_ranges calls retain strict behavior.

Guard detail: page_fragment=True alone also suppresses crossed nonmath environment-end issues. show_math strictly validates each complete file before that file's fragment; align_math strictly validates both files before fragment math extraction or writes. The isolated full-file crossing tests exercise those actual guards.

No production source, ledger, or root record was changed, and no source text or scan was reviewed. Input hashes, exact issue codes, signatures and caller locations are in AUDIT.json.
