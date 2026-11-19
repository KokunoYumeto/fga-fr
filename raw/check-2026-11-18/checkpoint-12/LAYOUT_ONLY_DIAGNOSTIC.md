# Layout-only diagnostic: fourteen overflows removed in frozen copies

The proposed candidate removes all **14 boxes above 2 pt** in the affected
successful baselines: five in French, six in printed French, and three in Korean.
The three affected layers each completed **three stable compiler passes**, with
zero engine errors and zero missing-glyph diagnostics. The eight other layers
retain their already successful, zero-overflow baseline evidence; their frozen
source hashes are unchanged.

This is a proposal for root's adoption and visual review. No live edition source,
correction ledger, scan, or credits/rights file was changed. No mathematical,
translation, scan, or PDF-content review was performed. The French baseline is
the frozen reading through **221-263**, not any later live French edits.

## Results across all eleven layers

| Layer | Baseline boxes >2 pt | Candidate boxes >2 pt | Candidate maximum | Pages | Evidence |
|---|---:|---:|---:|---:|---|
| fr | 5 | 0 | 0.94453 pt | 150 | New three-pass build |
| fr_printed | 6 | 0 | 0.94453 pt | 150 | New three-pass build |
| en | 0 | 0 | 0 pt | 151 | Unchanged successful baseline |
| es | 0 | 0 | 0 pt | 157 | Unchanged successful baseline |
| es_149_printed | 0 | 0 | 0 pt | 25 | Unchanged successful baseline |
| pt-BR | 0 | 0 | 0 pt | 155 | Unchanged successful baseline |
| pt-BR_printed | 0 | 0 | 0 pt | 153 | Unchanged successful baseline |
| vi | 0 | 0 | 0 pt | 142 | Unchanged successful baseline |
| vi_diplomatic | 0 | 0 | 0 pt | 140 | Unchanged successful baseline |
| ko | 3 | 0 | 0 pt | 130 | New three-pass build with open CJK fonts |
| zh-Hans | 0 | 0 | 0 pt | 151 | Unchanged successful open-font baseline |

All eleven selected evidence rows have engine exit 0, no engine errors, no
missing-glyph diagnostics, three passes, and stable auxiliary hashes. Page counts
are unchanged from the corresponding baselines. Each candidate source-tree hash
was checked against the selected build's recorded hash.

French evidence is in `build_reports/layout_mechanical_04/`; Korean evidence is
in `build_reports/layout_mechanical_07/`. The complete candidate source assembly
is the temporary `layout_mechanical_07` frozen work tree. Its French source bytes
are identical to those built in stage 04. The all-layer evidence mapping and
hashes are in `layout_diagnostics/ALL_LAYERS_SUMMARY.tsv`.

## Exact proposed changes

There are **14 local insertion regions in nine files**. No preamble, main file,
global tolerance, page geometry, overflow threshold, or warning-suppression
setting is changed.

| Affected layers and source | Baseline region | Proposed layout operation |
|---|---|---|
| Both French layers, `fr/149.tex` | Existing display ending at line 485; printed counterpart at 482 | Put the existing display inside a local `\small` group |
| Both French layers, `fr/182.tex` | 256-257 and 269-278 | Local `\emergencystretch=3em` groups |
| Both French layers, `fr/182.tex` | 439-444 | Local `\small` group around the existing corollary paragraph; its mathematics stays inline |
| Both French layers, `fr/212.tex` | 289-290 | Local `\emergencystretch=3em` group after the existing display |
| Printed French, `fr/182.tex` | 898-924 | Local `\emergencystretch=3em` group, extending through the existing paragraph/list block |
| Korean, `149.tex` | 72-79 | Local `\emergencystretch=3em` group |
| Korean, `182.tex` | Inline formula at 508, within 506-509 | Put only that complete existing inline formula inside `{\small ...}` |
| Korean, `190.tex` | 1112-1123 | Local `\emergencystretch=3em` group |

Use `layout_diagnostics/PROPOSED_LAYOUT_PATCH.diff` for review and
`layout_diagnostics/PROPOSED_LAYOUT_INSERTIONS.json` for exact byte-preserving
application. `PROPOSED_LAYOUT_CASES.tsv` gives every baseline error location,
overflow amount, wrapper region, and selected build stage. Source line numbers
refer to the mapped frozen baselines. Compiler/SyncTeX page numbers are location
candidates, not visually confirmed page findings.

All original source newlines and inline/display delimiters remain in place.
The inserted end-group commands follow existing paragraph termination. No
inline formula was converted to a display, and no formula was split or rewritten.

## Mechanical scope verification

An independent byte audit checked all **273 files** in the eleven frozen layers.
Of these, **264 are byte-identical** to baseline. The nine changed files differ
only by the 14 authorized layout regions, totaling **514 inserted bytes**.
Reversing the exact insertions restores all **5,955,847 original bytes**.

The ordered inline/display delimiter token sequences are unchanged. All 40 files
identified by notice, credits, rights, license, and related filenames are
byte-identical. The stronger whole-file reverse check also covers every original
byte in the nine changed files. Detailed evidence is in
`layout_diagnostics/SOURCE_BYTE_SCOPE.tsv` and
`layout_diagnostics/INDEPENDENT_BYTE_AUDIT.json`.

The application helper was also run on a fresh assembly of the mapped baselines.
All eleven reconstructed source-tree hashes exactly match the audited candidate;
see `layout_diagnostics/REPRODUCTION_CHECK.tsv`.

## Remaining layout review

The selected French spacing changes increase underfull horizontal-box diagnostics
from **2 to 5** in French and **1 to 5** in printed French. The selected French
candidate introduces **no badness-10000 horizontal box**. Korean retains its two
pre-existing underfull horizontal boxes, including one at badness 10000. Vertical
underfull counts are unchanged: two per French layer and zero in Korean.
`layout_diagnostics/UNDERFULL_COUNTS.tsv` records these counts explicitly.

An 8em French emergency-stretch trial removed the overflow but introduced one
badness-10000 line in each French layer; the selected local `\small` alternative
avoids that added diagnostic. Korean 3em and 5em stretch trials did not remove its
remaining 2.92223 pt box; the selected local inline-font change does. Trial outcomes
are summarized in `layout_diagnostics/EXPERIMENTS.tsv`.

The smaller local type and loosened paragraph spacing still need root's visual
judgment. Compiler diagnostics alone do not establish page-layout quality. The
remaining French 0.94453 pt box is below this task's 2 pt threshold and was left
outside the proposed changes.

## Reproducing the candidate

Start from a separate, stable frozen source copy. The CJK layers must first have
the separately documented open-font substitutions from
`CJK_OPEN_FONT_FALLBACK.md`; the layout proposal contains no font-name changes.
From the workspace root, apply and compile with a new work directory and tag:

```sh
python -B FGA_CHECK/scripts/apply_layout_diagnostic.py --work tmp/frozen_runs/layout_review_next --check-only
python -B FGA_CHECK/scripts/apply_layout_diagnostic.py --work tmp/frozen_runs/layout_review_next
python -B FGA_CHECK/scripts/build_fga.py --work tmp/frozen_runs/layout_review_next --runtime tmp/tex_runtime build --layers fr,fr_printed,ko --tag layout_review_next --max-passes 3
```

The application helper refuses live deliverable paths, verifies the pinned
insertion metadata, preflights every exact context, and verifies reverse recovery
before writing the separate copy. It does not create correction-ledger entries or
apply anything to live edition sources. Raw compiler logs and diagnostic PDFs
remain in the temporary runtime; only sanitized evidence is retained here.
