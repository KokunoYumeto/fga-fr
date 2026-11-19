# Synthetic coverage and privacy gate review

This review used helper source code and temporary synthetic fixtures only. No real edition, ledger, scan, page record, mathematical record, validator run, build, checkpoint, or archive was examined or produced. Content-audit rules were not changed.

## Coverage enforcement verified

The validator enumerates 137 required translation layer/unit combinations, including errata, Commentaires, and the printed variants. Synthetic tests confirmed that removing a single English unit, an English erratum, the English Commentaires section, or the Spanish printed section produces a coverage gap. Removing all English sections produces 17 gaps. Thus files and eleven PDFs alone cannot satisfy the gate. The packager rejects positive French-page, translation-coverage, or privacy gap counts even when its synthetic file/PDF metadata is otherwise complete.

Two mechanical false positives are now corrected: heading-looking lines inside backtick or tilde fences are ignored, and source locators require filename boundaries, including Unicode word boundaries. Backup suffixes do not count; a source-line annotation remains valid. The existing combined-parent section rule is retained. A heading, locator, and progress marker still cannot establish that the requested substantive review occurred.

The final packager now requires the fresh page and translation coverage TSVs with their exact validator-declared schemas. It checks the page-row count against the summary, requires every expected translation layer/unit exactly once, and rejects unresolved locator, heading, or completion markers in those rows. A zero-gap summary with absent or incomplete coverage tables is refused. The actual CLI still invokes the validator afresh; no stale-summary or skip-gate option was added. These are consistency checks on existing requirements, not additional content-audit requirements.

## Mechanical privacy gaps repaired

Added `scripts/privacy_scan.py` and connected it to the validator and generated-package text checks. Privacy scanning no longer depends on a filename-extension allowlist. It searches included decodable text, including extensionless files, TeX style files, HTML, and common Unicode encodings. Relative paths remain allowed, including paths beginning with dot or dot-dot components. Absolute local and Windows/network paths, local file URIs, and email patterns are checked without printing matches. Only an explicit list of portable interpreter shebangs is exempt; a private interpreter location is checked. Narrow regression tests also protect concatenated directory fragments and TeX source-marker regular expressions from being mistaken for absolute or network paths. Unicode path components are supported.

PDF inspection now searches document metadata, XMP metadata, and extractable visible page text. Extraction failures produce a privacy-gate finding. Newly generated final-package reports are independently screened before inclusion, closing the gap between the work-tree scan and later generated text.

The scan remains mechanical: rasterized text, embedded attachments, and binary or unsupported encodings are not interpreted. Pattern matches can require human reconciliation, especially where mathematical notation resembles a filesystem path. The heading recognizer supports the stated ATX/fence syntax rather than a complete Markdown/HTML parser; HTML-comment blocks are not specially excluded. Literal markers do not validate reviewer identity, the substance of a comparison, correction verdicts, or evidence. No OCR, semantic interpretation, or automatic audit-text alteration is performed.

## Reproduction

```sh
python -B work/scripts/gate_synthetic_tests.py
```

`GATE_SYNTHETIC_RESULTS.json` records 35 successful synthetic cases. The suite exercises missing language/unit sections, fenced pseudo-headings, exact and Unicode filename boundaries, preservation of combined sections, fresh coverage-table enforcement, gate propagation, extension-independent and Unicode text scanning, relative paths, interpreter shebangs, the two helper-source privacy regressions, PDF visible text and metadata, and newly generated text. The packager schemas were also compared directly with the validator declarations and matched. Its PDFs are synthetic in-memory fixtures and are never rendered. Existing content-audit requirements and all deliverable audit data remain unchanged; only mechanical recognition and privacy coverage were repaired.
