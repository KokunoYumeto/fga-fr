# Read-only audit readiness inventory

This report inventories structural evidence only. It does not certify that a page was read, a correction was reread, a translation was checked, a proof was verified, or a PDF was visually inspected. Missing markers are reported as unrecognized structural evidence, not as a mathematical judgment.

| Measure | Observed value |
| --- | --- |
| mode | readiness inventory |
| date utc | 2026-11-18T16:51:17.855847+00:00 |
| correction rows | 2731 |
| check event rows | 96 |
| schema issues | 1 |
| scan unit page occurrences | 211 |
| distinct volume printed pages | 205 |
| page occurrences with heading | 34 |
| page occurrences with completion marker | 34 |
| page occurrences with structural gaps | 183 |
| expected translation layer units | 137 |
| translation layer units with locator | 0 |
| translation layer units with structural gaps | 137 |
| duplicate or invalid record markers | 0 |
| protected files compared | 72 |
| protected files identical | 72 |
| front matter blocks flagged for review | 0 |
| missing required items | 0 |
| missing or invalid pdfs | 11 |
| missing expected source files | 0 |
| manifest discrepancies | 0 |
| privacy pattern findings | 0 |
| completion certified | False |

## Scope and limits

Original archive manifests are checked against byte counts and SHA-256 hashes. Working source changes are listed separately and are not called original-manifest mismatches. The new fr_printed tree is compared to the corresponding original fr tree for inventory and protected-file purposes.

Protected metadata files are compared byte-for-byte. Front-matter blocks between the document and mainmatter delimiters receive a separate byte comparison; any difference requires credit-specific review. Other inline credit strings are not semantically examined. Refutation events use the allowed event-type label; the refined statement and mathematical outcome are not interpreted here.

Confidence values are checked against the final exact values high, medium, and low. Provisional annotations or withdrawal prose in that column therefore appear as final-schema gaps and are never rewritten. Empty mathematical result/evidence fields are tested only for presence; their content is not evaluated.

Page coverage uses scan PDF page-tree metadata, excluding each cover sheet. Shared printed pages are distinct unit/page occurrences while the volume/page total counts them once. Source page markers are listed lexically and their correctness is not decided. Translation headings can be separate by layer or combined under a parent language, provided the layer's source locator is present. Headings in an unrecognized format may need manual reconciliation.

Privacy checks search text bytes for email and machine-specific path patterns without displaying matches. PDF checks inspect metadata only; page text and images are not read. Other binary contents are explicitly listed as unexamined. Portable interpreter shebangs are not treated as private machine paths.

FILE_INVENTORY.tsv follows the checkpoint packager's default deliverable scope, with explicitly allowed evidence images added. This validator's own output directory is excluded from that inventory to avoid recursive self-hashing. No source, audit record, note, mathematical decision, or progress entry is modified.
