# Translation footnote contents: exact-byte inventory

This small lexical navigator extracts literal, noncommented footnote contents from all translation-source `.tex` files and compares their bytes with the corresponding attached originals. It makes no judgment about wording, origin within the printed book, purpose or validity. **Original** identifies the attached translation-file version only.

## Frozen scope and result

The nine current translation layers and their originals were captured by identical consecutive reads at **2026-11-19T05:23:16.008741+00:00–05:23:16.154329+00:00**. Each version has 161 `.tex` files with the same relative filename set. All selected original files match the supplied original-source manifest. Live translation edits after capture are excluded.

| Translation layer | Current footnotes | Original footnotes |
| --- | ---: | ---: |
| `en` | 84 | 94 |
| `es` | 88 | 88 |
| `es_149_printed` | 9 | 9 |
| `pt-BR` | 81 | 81 |
| `pt-BR_printed` | 9 | 9 |
| `vi` | 85 | 85 |
| `vi_diplomatic` | 5 | 5 |
| `ko` | 93 | 93 |
| `zh-Hans` | 90 | 90 |
| **Total** | **544** | **554** |

Every one of the 544 current bodies has at least one exact counterpart in the same original file. Ten original EN 149 bodies have no exact counterpart in the captured current English layer. Their original marker keys are 170,171,175,177 (two), 183 (two), 185, 187 and 188. `ORIGINAL_WITHOUT_EXACT_CURRENT_MATCH.tsv` supplies only their IDs, paths, lines, byte ranges and hashes. These counts and equality statuses do not classify the notes or explain the changes.

There are 539 unique exact bodies across both versions. All are preserved in `CONTENTS.json`, with no redaction or withholding. A single path-shaped regex match was verified lexically as a colon plus an `overline` control word inside balanced inline math; its hashes and offsets are recorded in `PRIVACY_TEX_LOOKALIKES.json`. No prose was interpreted for that token check.

Eight `footnotemark` calls in each version contain optional marker arguments but no footnote body; they are listed separately. There are no unbalanced extraction cases, crossing page-marker ranges or literal parameter-template candidates in this capture.

## Files for sequential reading

The published directory is `translation_footnotes/snapshot_20261119_052316`.

- `FOOTNOTES.tsv` contains all 1,098 occurrences, labelled current/original, with layer, source path, declared unit, literal-page anchor, source and body line ranges, half-open byte ranges, complete source-file hash, body hash, invocation hash and exact counterpart IDs.
- `CONTENTS.json` stores each distinct body once, keyed by `body_sha256`; `exact_body_utf8` retains every original byte after UTF-8 round-trip, including whitespace, comments, macros and line endings. Join this key to `FOOTNOTES.tsv` to read a selected body.
- `ORIGINAL_WITHOUT_EXACT_CURRENT_MATCH.tsv` is the compact ten-row difference index.
- `MARKER_ONLY_CALLS.tsv` lists the 16 marker-only invocations. `FILES.tsv` inventories every selected `.tex` file, including files with no footnotes. `COMMAND_COUNTS.tsv` records the observed footnote-related macro spellings; formatting commands such as `footnotesize` are counted there but are not treated as note bodies.
- `CAPTURE.json`, `SUMMARY.json`, `EXTRACTION_ISSUES.json`, `SANITIZATION.json` and the independent audit files retain provenance, exactness and structural checks.

## Equality and locator policy

A body is the byte range strictly inside the mandatory braced argument. The complete invocation has a separate hash. Neither comparison normalizes whitespace, line endings, macros, punctuation or language. Links search the opposite version within the same translation layer; same-file, same-file/page, different-file and complete-invocation matches are recorded separately. All matching candidates are retained, so a repeated body can have more than one counterpart. Hash collisions are excluded by direct equality of the extracted byte buffers.

Page keys are literal source-marker locators. The preceding marker is used; an unmarked prefix can use the first following marker and is explicitly labelled. Missing markers are not invented. Existing source-marker caveats continue to apply, including the known missing Korean 195 markers 377 and 385. The inventory does not certify physical printed-page placement or expand TeX macros/conditionals.

The observed content calls are all simple, immediately braced `footnote` forms; no verb-like controls or parameter templates were found. The extractor also records marker-only calls and supports literal optional arguments. The script is a lexical tool for this source syntax, not a full TeX interpreter.

## Reproduction

```sh
python -B FGA_CHECK/scripts/inventory_translation_footnotes.py \
  --frozen tmp/translation_footnote_inventory_20261119_0521/frozen \
  --out tmp/translation_footnotes_recheck
```

The frozen bundle and raw working inputs remain in `tmp`. No source, ledger, record, progress, scan or rights file was edited, and no substantive or visual review was performed.

## Independent exactness audit

The independent audit passed all 322 capture hashes, all 161 original manifest bindings, all 1,098 invocation ranges and 16 marker-only ranges, all 539 exact payload bodies, and every counterpart list. Its 1,088 directed same-file links also match by literal page and complete invocation bytes. No contents were withheld or changed. `INPUT_AUDIT.json`, `EXACT_REPORT_AUDIT.json` and `VERSION_FILE_COMPARISON.tsv` retain compact evidence; the full mechanical reconstruction tables remain in the task-local working directory.
