# Build infrastructure restored for the continued check

The host had LuaHBTeX 1.18.0 and XeTeX 0.999996, but its TeX file index pointed to a missing generated database and its generated formats and PDF font map were absent. A task-local runtime was prepared with the existing `scripts/tex_runtime.py`. All 15 downloaded dependencies passed the size and SHA-256 checks in `scripts/TEX_DEPENDENCIES.tsv`; temporary CTAN mirror errors were retried without changing the pinned contents.

The initial setup produced the LuaLaTeX and XeLaTeX formats. The absent system PDF font map caused a later `lasy6` font error at PDF output. `scripts/prepare_fontmaps.py` generates the standard installed Computer Modern, LaTeX, Euler, and AMS maps only inside the task-local runtime and verifies the required `lasy6` entry. No edition text, font design, or system configuration is changed by these steps.

## Commands

From the working directory containing the deliverable folder:

```sh
python -B FGA_CHECK/scripts/tex_runtime.py --runtime tmp/tex_runtime --setup
python -B FGA_CHECK/scripts/prepare_fontmaps.py --runtime tmp/tex_runtime
python -B FGA_CHECK/scripts/build_fga.py --runtime tmp/tex_runtime build --layers fr,fr_printed --tag CHOOSE_NEW_TAG --max-passes 3
```

The runtime and intermediate build trees are reproducible working files and are not included in the deliverable ZIP. The dependency list and scripts are retained. The main build runner uses immutable stage tags; choose a new tag for every rerun.

## Baseline and repair evidence

`checkpoint05_baseline` records a single non-stopping diagnostic pass of each frozen restored French source tree. Its 27 source diagnostics per layer are followed by two output-stage diagnostics for the initially missing font map. These diagnostic PDFs are not deliverables. The frozen snapshot was taken before any source repair in this run.

`repaired_checkpoint05` is the first ordinary build of the repaired trees. It passed the repaired exposé 149 syntax and stopped at an extra closing brace in exposé 182. Further stages are recorded in `build_reports/` under distinct tags.

No scan reading, mathematical verification, translation check, or visual PDF review is performed by these infrastructure helpers. Even an engine-error-free build may still have overfull boxes requiring the later layout pass.

## Result after the 26 recorded source repairs

Stage `repaired_checkpoint05c` completes three LuaLaTeX passes for each French layer. Both PDFs have 151 physical pages; both have stable auxiliary files, engine exit status 0, zero source errors, zero missing-glyph diagnostics, and no unresolved-reference diagnostic. The original sources did not change during either build.

The corrected layer still has five overfull boxes above 2 pt and the as-printed layer has six (maximum 36.72565 pt in each), including three above 10 pt in each. The stage therefore correctly reports `overflow above 2 pt` rather than a completed final build. These are layout tasks for the later PDF pass, not engine failures. Candidate pages for boxes above 10 pt are physical pages 13, 29, and 31. No PDF has been published to `pdf/`, and no rendered-page inspection is claimed.

| Source file | Source lines | Overflow in pt | Candidate physical PDF page |
| --- | --- | ---: | ---: |
| 149.tex | 485 | 26.84898 | 13 |
| 182.tex | 256–258 | 6.36914 | 29 |
| 182.tex | 269–279 | 11.93977 | 29 |
| 182.tex | 440–445 | 36.72565 | 31 |
| 212.tex | 288–291 | 5.36102 | 86 |

The rows above describe the corrected layer. The as-printed layer has the same five overflow sizes and one additional box above 2 pt; its full set of source line ranges and candidate page mappings is in its own `OVERFULL_BOXES.tsv` rows. Source line ranges may differ after further edits. Candidate page mappings need the requested later visual confirmation.

The additional as-printed overflow is 4.89633 pt at `182.tex` lines 898–910, mapped to candidate physical page 37. Both latest passes report 73 warnings, recorded verbatim in the sanitized diagnostic table.
