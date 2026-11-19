# Source-marker inventory and side-by-side extraction

The frozen structural inventory covers **all eleven layers**, **171 unit files**,
and **2,133 literal page-marker calls**. The source copy was taken from
02:27:08.482769 to 02:27:09.014655 UTC on 2026-11-19. The reports describe that
snapshot; the reusable script can inventory or extract from a later stable copy.

No scans, wording, translations, mathematics, or images were assessed. No live
source, credits/rights, or correction-ledger bytes were changed.

## Structural findings

All eleven layers use **`\src{page}` with one required braced argument**. Every
observed page argument is decimal. There are no repeated page markers within a
unit and no missing expected unit files. All 171 unit files are reachable through
the literal include graph: 190 input edges reach 201 project TeX files.

The only differences against the French reference marker sets are:

| Layer | Unit | Absent marker | Source |
|---|---|---|---|
| ko | 195 | `377` | `sources/ko/195.tex` |
| ko | 195 | `385` | `sources/ko/195.tex` |

These are **missing anchors**, not findings that text is missing. Both values also
form internal gaps in that file's otherwise increasing decimal marker sequence.
No semantic conclusion is made about the surrounding material.

The partial layer `es_149_printed` deliberately declares only unit 149, with 25
markers. The other units are reported as outside its declared scope, not missing.
Korean has 209 markers; each of the other nine full-book layers has 211.

Always use **unit plus page**, such as `149 / 193` or `182 / 193`. Printed page
numbers recur in different units, especially among errata; those cross-unit
repetitions are not duplicate markers within a unit.

## Macro spellings and file routes

The base file of every layer defines `\src` with `\newcommand`. Four entry files
override it with `\renewcommand`: the current and printed-149 Spanish entries,
and the current and printed Portuguese entries. No marker `\let` aliases were
found. The inventory records each definition's path, line, arity, replacement
control-sequence spellings, body hash, and whether it is nested in another
definition; it does not reproduce the replacement text.

`\sid{unit}` is a separate one-argument unit identifier. There are 131 literal
calls: 81 decimal unit identifiers, 40 `e<digits>` identifiers, and 10 `com`
identifiers. It is not present in every unit file. Additional zero-argument
context macro names are `\FgaUnitKey` in the Spanish/Portuguese variants,
`\sourceunit` in Korean, `\fgasourceid` in the Vietnamese variants, and
`\fgaunitid` in Chinese.

The extractor obtains its unit key from the file route, without expanding these
macros:

| Layer | Unit-file directory beneath that layer |
|---|---|
| fr, fr_printed | `fr/` |
| en | `en/` |
| es | `es/` |
| es_149_printed | `es/149_diplomatic.tex` for unit 149 only |
| pt-BR | `pt_BR/current/` |
| pt-BR_printed | `pt_BR/diplomatic/` |
| vi | `sources/current/` |
| vi_diplomatic | `sources/diplomatic/` |
| ko | layer root |
| zh-Hans | `source/zh/` |

Full-book unit filenames are `149`, `182`, `190`, `195`, `212`, `221`, `232`, and
`236`, their corresponding `e<digits>` errata files, and `com`, each with `.tex`.
Entry-point and include paths are recorded separately in the reports.

## Reusable commands

The new helper is `scripts/source_segments.py`. It uses Python's standard
library and does not invoke TeX or read PDFs. From the workspace root:

```sh
python -B FGA_CHECK/scripts/source_segments.py --work FGA_CHECK inventory --out tmp/marker_inventory_after_edits
python -B FGA_CHECK/scripts/source_segments.py --work FGA_CHECK extract --unit 232 --page 149 --layers fr,en --out tmp/read_232_149_fr_en
python -B FGA_CHECK/scripts/source_segments.py --work FGA_CHECK extract --unit 232 --page 149 --layers fr,fr_printed --out tmp/read_232_149_french
python -B FGA_CHECK/scripts/source_segments.py --work FGA_CHECK extract --unit e149 --layers fr,en,ko --out tmp/read_e149_whole
```

Omit `--page` for the whole unit. Use `--layers all` for all eleven columns.
The `--page` argument uses printed source-page labels from `\src`; physical
page indices in compiled PDFs belong to the separate inspection-asset inventory.
Choose a new output directory for each run; existing directories are not
overwritten, and outputs inside source trees are refused.

Each extraction writes:

- `index.html`, a side-by-side reading aid with escaped literal TeX source;
- one exact `.tex` byte slice per successfully selected layer;
- `SEGMENTS.tsv`, recording source file/tree hashes, unit/page, byte and line
  boundaries, selection status, and segment hashes.

Columns are aligned only by the requested unit/page key, not by sentences or
mathematical expressions. No TeX or source HTML is executed. Slices are reading
aids and may begin or end inside TeX environments; they are not standalone
compilable documents.

### Boundary and ambiguity handling

A page slice begins at its literal `\src` invocation and ends immediately before
the next marker in the same unit, or at end of file. Every byte inside that span,
including line endings, is retained. `--include-unit-prefix` additionally includes
the unmarked prefix when selecting the first marker of a unit.

An absent marker normally produces an explicit placeholder and no guessed slice.
A duplicated marker requires an explicit one-based `--occurrence`. To request
surrounding context for a missing numeric marker deliberately:

```sh
python -B FGA_CHECK/scripts/source_segments.py --work FGA_CHECK extract --unit 195 --page 377 --layers fr,ko --neighbor-span --out tmp/read_195_377_neighbors
```

For the frozen Korean structure this selects the span from marker 376 up to
marker 378, clearly labeled **neighbor context; requested marker absent**. It
does not label that span as page 377. `--strict` writes the reports and then exits
with code 2 if any selection is missing, ambiguous, outside scope, or contextual.

## Reports and checks

`source_marker_structure/` contains `LAYER_SUMMARY.tsv`, `UNIT_STRUCTURE.tsv`,
`MARKER_OCCURRENCES.tsv`, `MACRO_DEFINITIONS.tsv`, `UNIT_IDENTIFIERS.tsv`,
`INPUT_GRAPH.tsv`, `CROSS_LAYER_MATRIX.tsv`, and `STRUCTURAL_ISSUES.tsv`.
They provide all source paths, per-unit marker sequences, offsets, hashes,
cross-layer counts, and structural flags without source text excerpts.

The parser masks unescaped percent comments while retaining byte offsets. It
recognizes literal numeric/Roman marker arguments and literal input paths. It
does not expand arbitrary TeX macros or simulate verbatim environments. All
current observed markers and include paths fit the supported literal forms.

Independent checks agree on all **2,133 marker positions, invocation ends,
segment ends, and source hashes**, and on **106 marker/context definitions**.
Synthetic comment/escape and duplicate-selection cases passed. Sixteen real
source slices were checked only as byte ranges and hashes; the extracted text
and HTML were not displayed or reviewed. All **274 frozen input files** remained
byte-identical. `EXTRACTOR_CHECKS.tsv` and `INDEPENDENT_STRUCTURE_AUDIT.json`
record this mechanical verification.
