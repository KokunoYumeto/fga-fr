# Mechanical math and reference navigator

The reusable script `scripts/math_expression_inventory.py` makes exact page-local French/translation source slices, balanced math records and ordered lexical candidate blocks. It performs no semantic alignment or adjudication and never modifies its inputs. It uses the unchanged `translation_math_lexer.py` copied by root and the existing `source_segments.py` marker helper.

## Current-page use

Run from the workspace. Use a fresh output directory each time.

```sh
python -B FGA_CHECK/scripts/math_expression_inventory.py \
  --work FGA_CHECK --out tmp/math_review_en149_171 \
  --layers en --units 149 --page 171 --source-segments \
  --note 'Selected current files captured for root review; later live edits excluded.'
```

The script reads only the selected unit files twice and requires identical bytes before analyzing its in-memory capture. `CAPTURE.json` records the exact file hashes and capture UTC interval. Later changes to live files do not alter the report. To use a fixed historical tree, replace `--work FGA_CHECK` with its frozen work directory.

For all pages of EN149, omit `--page`. For a different translation or unit, change `--layers` and `--units`; both accept comma-separated lists. `--layers all --units all --compact` creates a compressed complete inventory. No external program, scan, context folder, source edit or mathematical decision is invoked.

## Files to read

Each selected page has `pages/en/149/171/` (with the requested layer/unit/page substituted):

- `french.tex` and `translation.tex`: exact page-marker slices. The first literal page also includes the unmarked unit prefix; this is flagged explicitly.
- `MATH.json`: exact raw spans on each side, their outer/nested identities, byte/line locators, source-page anchor, hashes and parent IDs. Outermost counts exclude nested environments and math inside text-command bodies already contained by an outer span.
- `REFERENCES.json`: literal braced commands such as `\tag`, with exact ranges. Commands are not interpreted as verified references.
- `REFERENCE_SHAPES.json`: deliberately conservative literal patterns such as parenthesized dotted numbers or bracketed numerical labels. They are only reference-shaped navigation candidates and can include unrelated text. Plain numerical labels, translated names, macro-expanded references and other syntaxes are not exhaustively recognized.
- `PAIR.json`: counts, boundary status and ordered candidate blocks. Equal-token runs identify candidate pairs; replace/insert/delete runs remain whole ordered blocks with both sides' span IDs. No arbitrary pairing is imposed inside a changed block.

`PAGE_COUNTS.tsv` is the compact page index. `MATH_REGIONS.jsonl`, `REFERENCES.jsonl`, `REFERENCE_SHAPED_CANDIDATES.jsonl`, `PAGE_PAIRS.jsonl` and `CANDIDATE_ALIGNMENT.jsonl` retain the complete ordered records. With `--compact`, these have `.jsonl.gz` endings; gzip timestamps are fixed. `LEXICAL_ISSUES.json`, `PRIVACY.json`, `EXACTNESS_CHECKS.json` and `SUMMARY.json` expose structural limitations and checks.

## Exact comparison policy

Candidate alignment compares the **inner-span token signature** in source order using `difflib.SequenceMatcher(..., autojunk=False)`. Opening/closing math delimiters are excluded from that search key, but the complete raw span and full-token hash are retained. Comments and ASCII whitespace are omitted from the key. Control-sequence boundaries, braces, alphabet/font macros, symbols, Unicode bytes and all other punctuation remain unchanged. Thus a spaced control word and a merged longer control word remain different; font and alphabet declarations remain different too.

The signature is a search aid, not a claim of TeX or mathematical equivalence. Whitespace can matter inside text bodies, and delimiter changes can affect presentation. Every record keeps `human_review_required=true`, including byte-identical pairs. Raw text and complete hashes always remain available for root's decision. Source text, translations and mathematics are not corrected by this script.

Only outermost math spans are compared in the main stream. Nested spans are retained with parent IDs. Explicit command references and literal reference-shaped candidates have separate ordered streams. If page-marker boundaries differ, a marker is missing/duplicated, or the lexical parser reports an issue, the page is labelled and no candidate pairing is generated. A missing marker is not described as missing content.

Default corresponding French layers: en/es/pt-BR/vi/ko/zh-Hans use `fr`; es_149_printed/pt-BR_printed/vi_diplomatic use `fr_printed`. The Spanish printed layer declares only unit 149. The parser's supported literal syntax and deliberate exclusions are documented in its module; it does not expand macros, catcodes or conditional TeX.

## Published historical EN149 example

`math_expression_inventory/en149_snapshot_20261119_044604` contains all 25 pages from the source capture at **2026-11-19T04:46:04 UTC**. It has 1,751 balanced spans (1,716 outermost and 35 nested), 132 explicit reference commands and 155 literal reference-shaped candidates across the two files. There are no lexical issues or marker-boundary mismatches. The exact-fragment and token-boundary fixtures pass.

**This example is stale for current editing:** root subsequently removed nine editorial footnotes from corrected French 149 and began English edits. It is retained as a fixed example and must not be treated as the current live source. Regenerate the current selected page with the command above. This fixed example preserves all font/alphabet wrappers in its strict search signature, yielding 24 unpaired math blocks and no automatically paired math expressions; this does not mean that the expressions are semantically unrelated.

The input pair is bound by source hashes in `CAPTURE.json`. `PRIVACY.json` records two colon-plus-control-word lookalikes inside literal math; their exact bytes are retained. No actual email or local absolute path was found. Local runtime/source locations in metadata are relative to the workspace.
