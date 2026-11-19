# Read-only TeX comparison helper

`scripts/tex_compare.py` inventories lexical math spans and source-page markers, compares selected span sequences, and produces literal unified diffs. It does not execute TeX, expand macros, inspect a scan, evaluate meaning, edit a source or ledger, or certify a review. Only Python's standard library is required. Ordinary commands write to standard output and standard error; there is no update or output-file command.

## Commands

Examples run from the directory containing `work/`. Substitute the intended pair of source files and source line ranges. These examples are instructions for later use; no actual source comparison was performed while preparing this helper.

```sh
# Extract raw math spans and literal source-page markers for one printed page.
python -B work/scripts/tex_compare.py extract work/sources/fr/fr/149.tex --page 169

# Compare page groups, with exact raw-span comparison as the default.
python -B work/scripts/tex_compare.py compare work/sources/fr/fr/149.tex work/sources/en/en/149.tex --page 169

# Explicitly choose the conservative presentation normalization.
python -B work/scripts/tex_compare.py compare work/sources/fr/fr/149.tex work/sources/en/en/149.tex --page 169 --normalize presentation

# Compare two requested source ranges as one ordered sequence.
python -B work/scripts/tex_compare.py compare left.tex right.tex --left-lines 10:40 --right-lines 12:45 --group range

# Literal corrected/as-printed source diff, independent of math extraction.
python -B work/scripts/tex_compare.py diff work/sources/fr_printed/fr/149.tex work/sources/fr/fr/149.tex --context 3

# In-memory synthetic tests only; no source file or scan is opened.
python -B work/scripts/tex_compare.py selftest
```

Repeat `--page` to select several explicit printed pages. `--left-lines` and `--right-lines` use inclusive one-based ranges and accept `START:`, `:END`, or `START:END`. The parser reads the complete selected input file to establish nesting and inherited page markers, then selects spans intersecting the requested range. A span cut by a requested range is retained whole and flagged `range_partial`; it is never silently truncated. Unified-diff hunk positions are relative to the selected line slices, whose original source ranges appear in the diff headers.

## Parsing and page attribution

Recognized math delimiters include `$...$`, `$$...$$`, `\(...\)`, `\[...\]`, and balanced braced `\ensuremath`. Standard equation, align, alignat, flalign, gather, multline, eqnarray, matrix, array, cases, and related environments are recognized, including common starred variants. Add another literal environment name using repeatable `--math-env NAME` options. Nested math environments remain part of their outer span.

The scanner respects escaped control symbols, comments, balanced braces, nested environments, `\verb`, common verbatim environments, and braced URL/path arguments. It records exact raw spans, offsets, source line ranges, literal `\src{integer}` markers, and diagnostics for incomplete or inconsistent constructs. A nonliteral page argument is flagged and is not evaluated.

Each span inherits the latest preceding recognized page marker. A span crossing another marker lists every touched page and is flagged. Page-group comparison includes that complete span in each touched page, so a cross-page formula is not cut into guessed pieces. Spans before any marker have an explicit unmarked group. `--group range` compares the complete selected span sequence without regrouping by page. A selected page containing no lexical math can have an empty sequence; that is not evidence of a completed page review.

This scanner assumes ordinary TeX catcodes and literal syntax. It does not expand aliases, conditional branches, macro arguments with arbitrary delimiters, macro-generated math or page markers, or custom active characters. It may inventory literal math inside a macro definition even if that macro is never used. It is not a TeX validity checker. Unsupported constructs, malformed input, and source-range boundaries require human interpretation; diagnostics never authorize automatic repair.

## Opt-in normalization

The default `--normalize none` compares each complete raw span, including delimiter/environment syntax, comments, whitespace, font commands, and labels. The optional `presentation` mode compares an explicit token array and records every removal with offsets within the original span:

- Ignore ordinary math whitespace and TeX comments, while preserving escaped spaces and explicit spacing commands.
- Remove only the `\left` and `\right` sizing control words, preserving their delimiter tokens, including a literal null-delimiter dot.
- Remove the `\symup` and `\mathrm` control words only when followed by a balanced braced argument. **Retain every argument brace.** An unbraced form remains unchanged and receives a caution.

Indices, operators, actual symbol tokens, and commands such as `\mathcal`, `\mathfrak`, and `\underline` remain present. Literal braced arguments of common text, operator-name, label, tag, and reference commands are preserved as opaque chunks, including their spaces. Token boundaries remain explicit: `\alpha x` never becomes the different control word `\alphax`. The display string retains a separator wherever concatenation would merge control words; the token array determines comparison.

Keeping braces is intentional: `{x}` and `x` may remain different after a font control word is removed. Nothing simplifies grouping or reattaches an index. No other command aliases, typographic variants, equation labels, alignment syntax, or mathematical expressions are normalized. Numeric primitives and custom macros can give otherwise ordinary whitespace special meaning; lexical normalization is therefore a transparent comparison aid, not a semantic equivalence test. Raw spans remain available alongside every normalized representation.

## Output and tests

Extraction and comparison produce JSON containing input fingerprints, selected ranges, page markers, complete spans, normalization operations, parser diagnostics, and ordered sequence differences referring to span IDs. Equal selected representations are reported literally as such; `review_certified` is always false. Source diff emits ordinary unified text and prints input fingerprints to standard error, preserving a missing-final-newline distinction. Paths in output labels are relative to the invocation directory; no machine-specific path is embedded in this documentation.

The embedded tests cover escaped dollars, comments, verbatim text, nested groups/environments, all delimiter families, `\ensuremath`, page attribution, crossing-page spans, incomplete input, exact versus opt-in comparison, preserved grouping/indices/operators/font commands, control-word boundaries, retained text spaces, partial-range selection, sequence differences, and missing-final-newline diffs. All fixtures are synthetic strings held in memory.
