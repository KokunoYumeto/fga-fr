# Frozen PDF inspection assets

Prepared **148 lossless PNG page images at 180 dpi** across all eleven books.
The raster files occupy **63,756,940 bytes (60.8 MiB)** and remain under
`tmp/pdf_inspection_assets/candidate_baselines_01/images/`.

**The images have not been viewed, read, judged, or visually reviewed.** The
checks were limited to build provenance, PDF page counts, renderer completion,
PNG file structure, byte sizes, hashes, and inventory coverage. No source, credit,
rights, or correction-ledger bytes were changed.

## Selected frozen builds

| Layer | Frozen build stage | Book pages | Rendered pages |
|---|---|---:|---:|
| fr | layout_mechanical_04 | 150 | 17 |
| fr_printed | layout_mechanical_04 | 150 | 18 |
| en | translation_baselines_221_249 | 151 | 12 |
| es | translation_baselines_221_249 | 157 | 12 |
| es_149_printed | translation_baselines_221_249 | 25 | 12 |
| pt-BR | translation_baselines_221_249 | 155 | 12 |
| pt-BR_printed | translation_baselines_221_249 | 153 | 12 |
| vi | translation_baselines_221_249 | 142 | 12 |
| vi_diplomatic | translation_baselines_221_249 | 140 | 12 |
| ko | layout_mechanical_07 | 130 | 17 |
| zh-Hans | cjk_open_fonts | 151 | 12 |

The French and Korean PDFs include the proposed local layout changes. Korean
and Chinese use the separately documented open-font fallback. The French layout
candidate is based on the reading frozen through **221-263**. These assets do not
represent subsequent live edits or the separate `read_through_221_276` regression
build.

Every selected PDF belongs to a successful three-pass build. Its recorded source
hash matches the audited candidate source tree, and all corresponding frozen
source files were compared byte-for-byte with the compiler's retained source
copy. PDF SHA-256 values identify the exact rendered files. No live source tree
was used for render-time integrity checks.

## Selection and page mapping

The sample is mechanically distributed; no page was selected by reading its
content. Each book includes its first and last physical pages, plus five adjacent
even/odd physical-page pairs near **10%, 25%, 50%, 75%, and 90%** of its length.
For a fraction `f` and page count `N`, the pair begins at
`2 * floor(f * N / 2)`, clamped to the valid even range from 2 through the largest
even page at or below `N - 1`. Duplicate page selections are merged.

All six strict baseline cases above 10 pt are covered: physical pages **13, 29,
and 31 in each French layer**. Their original page numbers and their mapped
candidate source locations are both included. All **14 proposed layout regions**
are also covered, including the Korean changes and the smaller French overflows.

Source-location mapping uses only the exact inserted-region byte offsets and
SyncTeX line/page nodes. Newline-terminated regions use an inclusive last line
that excludes the first following source line. Three additional pages are retained
as explicitly labeled following-source context: **French 32, printed French 32,
and Korean 30**. They are not reported as part of the core changed regions.
All SyncTeX locations remain mechanical candidates pending root's inspection.

## Inventory files

- `pdf_inspection_assets/RENDERED_PAGES.tsv`: one row per image, including layer,
  source hash, build stage, PDF hash and physical page, selection reasons,
  image path relative to scratch, image hash, byte size, pixel dimensions, and
  unreviewed status.
- `pdf_inspection_assets/RENDER_PLAN.tsv`: the reproducible page/render plan.
- `pdf_inspection_assets/PDF_PROVENANCE.tsv`: the eleven PDF identities and the
  frozen-source comparison counts.
- `pdf_inspection_assets/BASELINE_OVERFLOW_PAGE_MAP.tsv`: the six baseline cases
  above 10 pt and their candidate page mappings.
- `pdf_inspection_assets/LAYOUT_REGION_PAGE_MAP.tsv`: all fourteen proposed
  regions, with separate core and following-context locations.
- `pdf_inspection_assets/RENDER_SUMMARY.tsv` and `SELECTION.json`: per-book counts
  and the deterministic selection rules.
- `pdf_inspection_assets/INVENTORY_METADATA_AUDIT.json`: independent metadata and
  file-stat verification. This audit did not open PDFs or images.

## Reproduction and later final review

Run the following from the workspace root while the recorded frozen PDFs remain
available:

```sh
python -B FGA_CHECK/scripts/render_pdf_inventory.py --plan FGA_CHECK/pdf_inspection_assets/RENDER_PLAN.tsv --inventory tmp/pdf_inspection_assets/candidate_baselines_01/RENDERED_PAGES.tsv --jobs 2
```

The renderer checks each PDF's recorded SHA-256 and page count before producing
assets, then checks that the PDFs stayed unchanged during rendering. Generated
images and inventories are restricted to `tmp/`. The recorded renderer is
`pdftoppm version 26.05.0`; the command uses full physical pages, lossless PNG,
and the per-row dpi without content extraction, cropping, annotation, or editing.

After substantive edits and adoption of layout candidates, compile a new frozen
stage and regenerate the affected source-to-page mappings from that final stage's
SyncTeX data. Create a new plan with its source and PDF hashes, current physical
page numbers, and a new temporary asset directory. The baseline physical page
numbers in this inventory are location aids, not claims about final pagination.
The same rendering helper can then produce the final review images from that new
plan. All visual and content decisions remain with root.
