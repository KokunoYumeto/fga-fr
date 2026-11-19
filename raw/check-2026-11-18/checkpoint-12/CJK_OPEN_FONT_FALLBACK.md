# CJK open-font fallback: successful diagnostic compilation

The two CJK editions compile after nine font-name replacements in three files of a separate diagnostic copy. The live edition sources were not edited. No new French snapshot was made. The diagnostic copy was derived from the already frozen translation baseline, so the ongoing French page edits were outside this work.

## Minimal font mapping

| Original request | Replacement | Occurrences | Purpose |
| --- | --- | ---: | --- |
| Malgun Gothic | Noto Sans CJK KR | 3 | Korean body, italic base, and sans family |
| Malgun Gothic Bold | Noto Sans CJK KR Bold | 1 | Korean bold italic base |
| SimSun | Noto Serif CJK SC | 3 | Chinese serif body and two inline font requests |
| Microsoft YaHei | Noto Sans CJK SC | 2 | Chinese sans and existing mono-family declarations |

All existing fake-slant, fake-bold, scaling, size, geometry, and line-breaking settings remain unchanged. The Korean edition retains a sans-serif family. The Chinese edition retains a serif CJK body and sans CJK family. Latin text and mathematics retain the supplied TeX Gyre and Latin Modern fonts.

The exact changes are in `cjk_font_fallback/CJK_OPEN_FONT_PATCH.diff` and `cjk_font_fallback/CJK_OPEN_FONT_CHANGES.tsv`. They affect Korean `base-ko.tex` at lines 4, 5, 7, and 10; Chinese `source/tex/zh.tex` at lines 8–10; and the two inline SimSun declarations in Chinese `source/zh/149.tex` at lines 132 and 832. These are snapshot locators and may move during later text edits.

`FONT_ONLY_VERIFICATION.tsv` checks all 59 files in the two diagnostic trees: 56 are byte-identical to the frozen originals, and reverting only the recorded font names restores the other three byte-for-byte. Credits, rights notices, substantive prose, formulas, and every other source byte are therefore preserved in this diagnostic comparison.

## Actual build results

Stage: `build_reports/cjk_open_fonts/`. Engine: XeLaTeX, three passes per layer, shell escape disabled. Both builds have stable auxiliary files and no unresolved-reference diagnostic.

| Layer | PDF pages | Errors | Missing glyphs | Warnings | Boxes over 2 pt | Boxes over 10 pt | Maximum overflow |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Korean | 130 | 0 | 0 | 47 | 3 | 0 | 7.77426 pt |
| Chinese | 151 | 0 | 0 | 3 | 0 | 0 | 0 pt |

Korean still has layout work for the later phase:

| Source | Lines | Overflow | Candidate physical PDF pages |
| --- | --- | ---: | --- |
| `ko/149.tex` | 72–75 | 7.77426 pt | 7–8 |
| `ko/182.tex` | 505–510 | 2.92223 pt | 29 |
| `ko/190.tex` | 1111–1119 | 4.14710 pt | 52 |

These are SyncTeX candidates, not visually confirmed locations. No text, scan, translation, or PDF page image was reviewed. The PDF font resources were inventoried as metadata only; their lists are in the build stage.

## Font provenance and regional selection

The available static font collections are Noto Sans CJK **2.004** and Noto Serif CJK **2.003**, verified from their font name tables. `CJK_OPEN_FONTS.tsv` records their file sizes, SHA-256 values, collection indices, family names, styles, and numeric font versions. Four collection files are copied into the isolated runtime; no font binary is bundled into this report or the edition sources.

The upstream projects publish both families under the SIL Open Font License 1.1:

- [Noto Sans CJK license](https://github.com/notofonts/noto-cjk/blob/main/Sans/LICENSE)
- [Noto Serif CJK license](https://github.com/notofonts/noto-cjk/blob/main/Serif/LICENSE)
- [Official Noto CJK releases and download guides](https://github.com/notofonts/noto-cjk/releases)

The fontspec log explicitly selects the KR and SC families; the extracted selections are in `cjk_font_fallback/FONT_SELECTION.tsv`. The collections share CFF programs whose internal names end in `jp`, so `pdffonts` shows those shared internal names even for the selected KR and SC faces. `COLLECTION_NAMES.tsv` records the differing regional name-table entries and shared CFF name directly from the font metadata. The `jp` name alone is therefore not evidence that the wrong regional family was selected.

## Reproduction

The standard isolated runtime and standard font maps must first be prepared as described in `BUILD_RESUME.md`. Make the official Noto Sans CJK 2.004 and Noto Serif CJK 2.003 static collections visible to fontconfig. The setup helper verifies the existing manifest and refuses different font bytes or collection indices on a repeat run.

```sh
python -B FGA_CHECK/scripts/prepare_open_cjk_fonts.py --runtime tmp/tex_runtime --manifest FGA_CHECK/CJK_OPEN_FONTS.tsv
```

For a new diagnostic experiment, copy only the Korean and Chinese source trees into a separate temporary work directory, then run the font-only patch helper and an ordinary build with a new immutable stage tag:

```sh
python -B FGA_CHECK/scripts/patch_diagnostic_cjk_fonts.py --diagnostic-work tmp/frozen_runs/cjk_open_fonts --report-dir FGA_CHECK/cjk_font_fallback
python -B FGA_CHECK/scripts/build_fga.py --work tmp/frozen_runs/cjk_open_fonts --runtime tmp/tex_runtime build --layers ko,zh-Hans --tag cjk_open_fonts --max-passes 3
```

The commands above name the successful run; choose new temporary directories and stage tags when repeating it. The patch helper refuses the live deliverable tree and requires the expected original font-name counts. It preserves line endings and every non-font byte. The ordinary build runner is used without font-redirection hooks.

For later adoption, apply the nine recorded font-name replacements to the then-current edition sources and add the corresponding typesetting rows. The updated sources must then receive their normal final builds and PDF review. This diagnostic run has not published a PDF and has not added any source change to the live audit ledger.
