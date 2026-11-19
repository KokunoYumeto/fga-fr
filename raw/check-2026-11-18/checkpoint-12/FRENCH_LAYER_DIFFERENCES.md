# Mechanical French-layer difference inventory

This inventory maps exact byte differences between frozen `fr` and `fr_printed` source trees. It provides lexical page-marker context and candidate correction-ledger row IDs for root's later complete review. No difference, correction, wording, mathematics, scan, translation, or PDF appearance was adjudicated.

## Frozen inputs

The source trees and `CORRECTIONS.tsv` were copied together after two consecutive complete reads produced identical file sets and bytes. The snapshot began **2026-11-19T03:34:25.873911+00:00** and completed **2026-11-19T03:34:26.031673+00:00**. All subsequent processing used `tmp/french_layer_difference_01`; evolving live sources and ledgers were not reread.

| Input | SHA-256 |
| --- | --- |
| `fr` source tree | `b8a5480e7fe5f2eb867063a3498e611a13abe6f6c04760cf772f67add3f69bc9` |
| `fr_printed` source tree | `925efa391d1bb3e9dc2307a8063674ce73ad750fe33634b8b9516f37b439a9ef` |
| Frozen `CORRECTIONS.tsv` | `e9cfe9f83f4b558a50486e0a2221710d7a3d7e85c178306dc9a944b7a401c140` |

Tree hashes use the existing build convention: sorted relative filenames, a zero byte, and each file's binary SHA-256 digest. The frozen ledger has **17,687 data rows**. Row IDs in this inventory are tied to this ledger hash and can move if rows are subsequently inserted or removed.

## Inventory result

There are **29 relative file pairs**: **21 byte-identical** and **8 nonidentical**. Every nonidentical file is a declared content `.tex` unit. Build/front-matter `.tex` files and support/rights metadata are identical in the frozen pair.

| Relative file | Changed hunks |
| --- | ---: |
| `fr/149.tex` | 48 |
| `fr/182.tex` | 38 |
| `fr/190.tex` | 41 |
| `fr/195.tex` | 33 |
| `fr/212.tex` | 11 |
| `fr/221.tex` | 72 |
| `fr/232.tex` | 16 |
| `fr/236.tex` | 16 |
| **Total** | **275** |

All 275 hunks are replacement opcodes. None crosses a literal printed-page marker or has different containing-page anchors between the two sides. These statements describe source-marker structure, not verified scan alignment.

All **550 source slices** (two sides of each hunk) match their frozen byte ranges and SHA-256 hashes exactly, and round-trip identically through JSON and TSV. **No privacy redaction was needed.** Two colon-plus-TeX-control-word lookalikes were independently checked as token syntax within literal math delimiters and are recorded in `PRIVACY_TEX_LOOKALIKES.tsv`; the exact source text is preserved.

The matcher produced **823 hunk-to-ledger candidate links**: 374 paired exact-substring links and 449 one-sided exact-substring links. Of the 275 hunks, **47 have one candidate row**, **169 have multiple candidate rows**, and **59 have no text candidate** under the declared rules. Among the 216 hunks with text candidates, **74 have only one-sided candidates**. Multiple rows can concern different portions of the same hunk; the script does not decide whether they compete or jointly explain it.

**122 paired-text candidate links have a ledger page key outside the hunk's marker-derived page keys.** They are retained with `file_match_page_mismatch` because the exact text pair occurs in the same file. No page equivalence is inferred. For the 59 hunks without a text candidate, a separate table lists **6,689 file/page-only locator links**; these are not counted as text matches or established coverage.

## Files for review

The published report directory is `french_layer_differences/snapshot_20261119_033425`.

- `FILES.tsv` includes all relative file pairs, classifications, presence, sizes, hashes, marker counts and hunk counts.
- `HUNKS.json` and `HUNKS.tsv` include every changed hunk, exact source slices, byte hashes, half-open byte ranges, physical source-line ranges, page-marker metadata and candidate IDs. The TSV flattens location fields; JSON retains the nested side-by-side structure.
- `PAGE_HUNK_INDEX.tsv` maps unit/page keys to hunk IDs for later sequential review.
- `CANDIDATE_ROWS.tsv` records each candidate's row ID, physical ledger-line range, row hash, file/page scope, method and old/new orientation. It does not reproduce ledger evidence or explanatory payloads.
- `MATCH_STATUS.tsv` separates unmatched hunks, single candidates, multiple candidates, one-sided-only candidates and page-mismatched links.
- `LOCATOR_ONLY_CANDIDATES.tsv` contains explicitly weaker file/page-only links for text-unmatched hunks.
- `MARKER_ISSUES.tsv` records missing or duplicate literal markers structurally.
- `PRIVACY_REDACTIONS.tsv` identifies any payload redactions by hunk, side and character range. Exactness is always separately flagged in the hunk records and summary.
- `PRIVACY_TEX_LOOKALIKES.tsv` records Windows-drive-like lexical matches that consist of a colon followed by a TeX control word inside literal math delimiters; it records token names and span hashes without inferring mathematical meaning.
- `SUMMARY.json` pins snapshot times, source/ledger/tool hashes, methods and aggregate counts.

## Exact difference definition

The fixed orientation is **old/left = `fr`; new/right = `fr_printed`**. These names indicate comparison direction, not which wording should be adopted. Ledger matching checks both historical old/new orientations independently.

For UTF-8 files, the script runs Python `difflib.SequenceMatcher` on `bytes.splitlines(keepends=True)` with `autojunk=False`. Each non-equal opcode is one changed hunk, without added surrounding context. A replacement block may contain several character-level differences. Newline bytes and all source text inside each block are retained. File-level reconstruction from unchanged blocks and right-side hunk bytes must exactly reproduce the right-side file before any report is written. Added, deleted, empty and non-UTF-8 files are supported; binary content is represented by base64 with an explicit encoding label.

Content-file classification is purely path based: the declared exposé, errata and commentary filenames from `source_segments.py` are `content_tex`. Other `.tex` files are `build_or_front_matter_tex`; other UTF-8 files are `support_metadata`. These classes do not describe a difference's significance.

## Page-marker mapping

The existing lexical marker helper ignores commented markers and recognizes literal `\src{...}` invocations. Each side records the preceding marker, following marker, closest marker by byte distance, containing-page anchor, pages touched by the complete hunk range and any unmarked prefix. The primary anchor is the last marker at or before the hunk start. Before the first marker, the following marker is recorded as a fallback and explicitly labelled `following_marker_for_unmarked_prefix`.

Ranges are byte-based and end-exclusive. A marker at a range's end belongs to the following range. Cross-page flags describe hunk extent, including any unmarked-prefix/marked-page crossing. They do not expand TeX, certify printed page numbers, or inspect PDFs/scans.

## Candidate matching rules

All text candidates must name the exact corresponding source file in the frozen ledger. The `printed_page` value is treated as a unit/page key, not a numerical interval. The free-form `line`, `statement`, `evidence`, `kind` and `confidence` payloads are not interpreted.

The first applicable rule for a ledger row and hunk is retained:

1. **Exact full hunk pair:** ledger old/new cells equal the two complete hunk slices, in either orientation.
2. **Exact distinguishing substring pair:** nonempty, unequal ledger old/new cells occur as exact substrings on their respective sides; at least one is absent from the opposite side.
3. **ASCII-whitespace-collapsed distinguishing pair:** the same paired test after runs of ASCII whitespace are replaced with one space and boundary ASCII whitespace is stripped. No other characters, commands, punctuation or case are normalized. This is a search rule, not an assertion of TeX equivalence. No current candidate used this rule.
4. **One-sided exact distinguishing substring:** when no paired rule matches, an old or new cell of at least 12 Unicode characters occurs on exactly one hunk side. This fallback also requires the ledger's exact file/page key to fit the marker scope; files without markers use file-only scope. The unmatched counterpart and historical direction are not inferred.

Paired rules can retain an exact-text candidate elsewhere in the same file, with a page-mismatch flag. One-sided matches are restricted to the mapped page scope. Equal old/new cells do not provide a contrast and are skipped. Candidate IDs are not proof that a ledger row covers all or any substantive part of a difference.

`C000001` denotes the first data row after the TSV header. Quoted multiline fields count as one data row. Physical start/end lines and a hash of all decoded cell values bind each ID to the frozen ledger. The row hash is SHA-256 of compact UTF-8 JSON containing the ordered header-field values.

## Reuse

Run from the workspace. Use a new output directory for each operation:

```sh
python -B FGA_CHECK/scripts/french_layer_differences.py freeze \
  --work FGA_CHECK --out tmp/french_difference_next

python -B FGA_CHECK/scripts/french_layer_differences.py inventory \
  --work tmp/french_difference_next --out tmp/french_difference_next_reports
```

The inventory command requires `SNAPSHOT.json`, checks every input size/hash, and confirms frozen inputs remain unchanged before writing. It refuses existing output directories and outputs inside the input tree. It writes only its new report directory; it does not edit sources, ledgers, rights files, progress records or archives. The optional `--min-single-side-chars` setting changes the explicitly recorded one-sided fallback threshold.

The script extracts exact text for root to read later. Running it does not perform that reading or establish substantive review completion.
