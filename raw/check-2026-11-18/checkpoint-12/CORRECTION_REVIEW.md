# Correction second-reading helper

`scripts/correction_review.py` selects correction records for a human second reading. It never edits the ledger, sources, confidence values, audit records, progress, or images. Selection and printed output do not confirm a correction. No OCR, image decoding, TeX build, semantic matching, or review decision is performed.

## Commands

Run these examples from the directory containing `work/`. Only the Python standard library is required.

```sh
# Metadata only; no old/new/evidence/statement payloads.
python -B work/scripts/correction_review.py inventory --format tsv

# Exact field filters combine with AND; repeated values of one filter use OR.
python -B work/scripts/correction_review.py inventory --layer 'French corrected' --page 169 --kind reading --format tsv

# Full selected records, including multiline old/new/evidence fields.
python -B work/scripts/correction_review.py show --unit 149 --page 169 --assets

# Stable content selection: replace DIGEST with a digest from the inventory.
python -B work/scripts/correction_review.py show --id DIGEST

# Existing scan, render, and crop links; this command does not read the ledger.
python -B work/scripts/correction_review.py links --unit 149 --page 169

# Exact-content changes between two ledger snapshots; metadata only.
python -B work/scripts/correction_review.py compare --against checkpoints/previous_CORRECTIONS.tsv --format tsv

# Synthetic fixtures only; no real ledger or image is read.
python -B work/scripts/correction_review.py selftest
```

The ledger defaults to `CORRECTIONS.tsv` in the work directory containing `scripts/`, so moving the complete work tree is supported. Override it with `--ledger path/to/ledger.tsv`. Commands print to standard output; snapshot fingerprints and counts go to standard error. There is no output-file or update command. Unfiltered full-row output requires explicit `show --all`.

## Row identity and historical records

Each `row_id` is `sha256:` followed by the full digest of all parsed field names and values. Column reordering, row reordering, appending other rows, and quoted TSV formatting do not change an unchanged record's ID. A changed field, including confidence, changes its ID. Every identical duplicate remains a separate occurrence; identical duplicates necessarily share a content ID. Selecting that ID returns every matching occurrence. Digest prefixes must contain at least twelve hexadecimal characters and must identify one distinct content digest.

`row_number` is a current logical TSV record number, not a physical line number or permanent identifier. `--row N` selects it. Use `--expect-ledger-sha256 DIGEST` with the raw-file fingerprint printed by an inventory to reject a ledger changed since that inventory. The helper imposes no expected ledger length. Comparison counts exact digest occurrences and accepts IDs present only in the old or current snapshot; it never infers which old correction was superseded, combined, reverted, or replaced. Positional `--row` selection is therefore unavailable for comparison.

Multiline, quoted, tab-containing, empty, historical, and aggregate field values are retained literally. Stored source line numbers are historical metadata; the helper does not relocate them or check whether old/new text is currently present. Layer, kind, and page filters are exact raw-field matches. For example, `--page 169` does not include a record whose page field is `169-193`; select that literal value separately or inventory the complete unit. No aggregate replacement is expanded into guessed constituent corrections. Noncanonical confidence annotations remain unchanged.

## Asset links and limits

The defaults search existing files in the sibling `inputs/scans`, `tmp/renders`, and `tmp/crops` directories. Override these using repeatable `--scan-root`, `--render-root`, and `--crop-root` options. `--assets` adds links to full-row JSONL output when the source filename identifies a unit and the page field is one integer. For ambiguous, global, or aggregate locators, use the explicit `links --unit ... --page ...` command.

If present, `validation/PAGE_COVERAGE.tsv` supplies the scan filename and PDF page index; `--page-map` can select another metadata table with `unit`, `printed_page`, `scan`, and `scan_pdf_page` columns. Without a matching map entry, a scan link is explicitly a candidate calculated from the filename's first printed page and one cover sheet; its upper page bound is not checked. Render and crop matches use the exact unit/page filename boundary, so page 169 does not accidentally match page 1690. The helper checks file existence, not image contents, crop coverage, or scan fidelity.

Links and displayed paths are relative to the invocation directory by default. `--link-style sandbox` produces runtime-specific clickable links for an interactive review; do not copy those absolute links into delivered documentation. `show` defaults to JSONL, which escapes embedded newlines without losing their values; `--format tsv` produces properly quoted full TSV records. It does not sanitize the selected ledger's payloads because exact review requires their preservation.

The embedded synthetic test checks multiline round trips, unchanged-content ID stability after reordering and appending, duplicate preservation, changed-value IDs, exact filters, digest-count comparisons, filename boundaries, mapped scan-page links, and a byte-unchanged fixture ledger. Its placeholder assets are never opened as images or PDFs.
