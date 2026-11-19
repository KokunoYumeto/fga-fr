# Compiler baselines from the frozen sources

The frozen snapshot contains the current two French layers after the 221-249 markup and all nine unchanged translation source trees. All source-integrity checks during compilation used the frozen copy, not the evolving live editions. No edition source, credit, rights notice, audit ledger, or page record was edited for these builds.

## Unmodified-source results

| Layer | Passes | Engine exit | PDF pages | Errors | Missing glyphs | Boxes over 2 pt | Maximum overflow, pt |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fr | 3 | 0 | 151 | 0 | 0 | 5 | 36.72565 |
| fr_printed | 3 | 0 | 151 | 0 | 0 | 6 | 36.72565 |
| en | 3 | 0 | 151 | 0 | 0 | 0 | 0 |
| es | 3 | 0 | 157 | 0 | 0 | 0 | 0 |
| es_149_printed | 3 | 0 | 25 | 0 | 0 | 0 | 0 |
| pt-BR | 3 | 0 | 155 | 0 | 0 | 0 | 0 |
| pt-BR_printed | 3 | 0 | 153 | 0 | 0 | 0 | 0 |
| vi | 3 | 0 | 142 | 0 | 0 | 0 | 0 |
| vi_diplomatic | 3 | 0 | 140 | 0 | 0 | 0 | 0 |
| ko | 1 | 1 | 0 | 1 | 0 | 0 | 0 |
| zh-Hans | 1 | 1 | 0 | 1 | 0 | 0 | 0 |

All nine layers that completed compilation have stable auxiliary files after three passes. All seven translation layers that completed compilation pass the automated overflow threshold as well. The two French layers retain their recorded overflow findings. These are compiler and log checks only; no page or PDF image was reviewed.

## Concrete font blockers

Korean stops at `sources/ko/base-ko.tex`, line 9, because `Malgun Gothic` is absent. Its declared bold italic face also requires `Malgun Gothic Bold`. Chinese stops at `sources/zh-Hans/source/tex/zh.tex`, line 8, because `SimSun` is absent; the same preamble also requires `Microsoft YaHei`. The supplied BUILD files explicitly list these fonts and say they are not bundled. The relevant TeX packages, including xeCJK, adjustbox, collectbox, and the language support, are available.

To complete these exact source builds, the required fonts must be supplied under their applicable terms, or the sources need a recorded typesetting change to installed fonts when that phase is reached. No verdict about later compiler behavior of either CJK edition can be made from the original font-blocked runs.

## Diagnostic experiments and limits

The unmodified-source baseline remains in `build_reports/translation_baselines_221_249/`. Its source hashes and compiler evidence are preserved exactly. Additional stages document unsuccessful attempts to use installed Noto fonts without editing the sources. Fontconfig aliases did not satisfy XeTeX. Driver experiments exposed wrapper and nested-option issues; the last primitive-call redirect still left original names in NFSS declarations. These experiments do not produce usable alternative editions and are marked diagnostic-only, so the ordinary publish helper rejects them. Their reports and the attempted helper are retained solely as a record of the work.

`scripts/cjk_diagnostic_build.py` is explicitly labelled as an unsuccessful experiment, not a recommended build route. `scripts/frozen_build.py` remains the reusable ordinary build route.

No PDF was copied to the final `pdf/` directory. The original source font requirements remain unchanged.

## Subsequent open-font diagnostic copy

After the unmodified-source baselines, a separately authorized diagnostic copy changed only the nine required font-name occurrences to Noto CJK. Both CJK editions then completed three XeLaTeX passes with zero errors and zero missing glyphs. See `CJK_OPEN_FONT_FALLBACK.md` for the minimal patch, font provenance, and remaining Korean overflow metrics. The live sources still retain their original font requests until the later adoption phase.
