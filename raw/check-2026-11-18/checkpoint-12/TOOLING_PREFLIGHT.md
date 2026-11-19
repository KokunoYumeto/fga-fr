# Tooling preflight

This report records infrastructure preparation only. It is not a page comparison,
translation check, mathematical verification, book build, or PDF inspection.
The edition source trees were not edited by the tooling preflight.

## Installed tools and repaired runtime

| Component | Observed version or state |
| --- | --- |
| LuaLaTeX engine | LuaHBTeX 1.18.0, TeX Live 2025/dev/Debian |
| XeLaTeX engine | XeTeX 0.999996, TeX Live 2025/dev/Debian |
| LaTeX kernel | 2024-11-01, patch level 2 |
| latexmk | 4.86 |
| Poppler rendering tools | 26.05.0 |
| Python PDF/image libraries | PyMuPDF, pypdf, pdfplumber, Pillow, reportlab available |

The installed TeX distribution had no usable filename databases or LuaLaTeX and
XeLaTeX formats. Most package files existed, but database-only lookup did not
find them. An isolated copy of the installed TeX tree was made, its filename
databases were generated, and both requested formats were generated successfully.
The setup script was then rerun successfully to verify that it is repeatable.

The local runtime received the missing TeX Gyre fonts, LuaTeX support packages,
language hyphenation files, Portuguese Babel files, xeCJK, ctexhook, and ulem.
The complete pinned download list, byte counts, and SHA-256 hashes are in
`scripts/TEX_DEPENDENCIES.tsv`. The script checks those hashes before installing
an archive. Dependency archives are downloaded into the local runtime cache.

Current CTAN xeCJK required a newer LaTeX kernel than the installed one. A
compatible xeCJK and ctex package from the TeX Live 2024 final archive was used
instead. One attempted Portuguese binary-package download returned HTTP 402;
the official Portuguese source ZIP succeeded and its `.ldf` files were generated
with docstrip. One historical archive server returned HTTP 503; the recorded
historical mirror succeeded. Neither failure is reported as a successful fetch.

The common preamble packages resolve in the repaired environment: geometry,
fontspec, Babel, polyglossia, microtype, graphicx, mathtools, amsthm,
unicode-math, bookmark, hyperref, xeCJK, and ulem. French, English, Spanish,
Vietnamese, and Brazilian Portuguese language support is available.

## Fonts

| Font required by the supplied preambles | Preflight result |
| --- | --- |
| TeX Gyre Pagella | Exact family available after local installation |
| TeX Gyre Heros | Exact family available after local installation |
| TeX Gyre Cursor | Exact family available after local installation |
| Latin Modern Math | Exact family available |
| Malgun Gothic and Malgun Gothic Bold | Unavailable |
| SimSun | Unavailable |
| Microsoft YaHei | Unavailable |

Noto Sans CJK KR, Noto Serif CJK SC, and Noto Sans CJK SC are installed. The
XeLaTeX infrastructure probe uses Noto Serif CJK SC only to exercise xeCJK.
The tooling preflight has made no font substitution in an edition. The Korean
and Chinese font requirements therefore remain a matter for the later build
pass: install the licensed requested fonts or record an explicit preamble change.

## Zero-page probes

The reproducible probe sources are in `scripts/tooling_probes/`; their commands,
exit codes, UTC timestamps, and sanitized results are in
`TOOLING_PROBE_RESULTS.tsv`. Each probe creates an unshipped box and produces
zero PDF pages. No scan or book page is used.

All three recorded probes passed with exit code zero. LuaLaTeX with hyperref
left a zero-byte PDF placeholder while reporting that it shipped no pages;
the probe result explicitly records that placeholder.

The LuaLaTeX probe loads the common packages, all four requested Latin/math fonts,
French, English, Spanish, and Vietnamese language support, and `ulem` with
`normalem`. The XeLaTeX probe loads Brazilian Babel, xeCJK, the common packages,
the Latin/math fonts, and `ulem`. Both probes exercise underlining.

The probes emit the expected package notices about mathtools/unicode-math
command overlaps. The LuaLaTeX graphics setup reports that shell escape is
disabled. Hyperref can request another pass for page-label metadata in the
zero-page XeLaTeX probe. These probes do not establish any book's overflow,
cross-reference, page-count, or visual-inspection status; those belong in
`PDF_CHECK.md` after the actual builds.

## Math typography controls

The installed unicode-math 0.8r code supports `math-style=upright`, but its
policy handlers use global assignments. A surrounding group is not a reliable
scope for that option. Moreover, changing this option after `\setmathfont`
did not remap the already configured ordinary Latin characters in the probe.

The explicit scoped alphabet command was tested by reading glyph codes from an
unshipped math box:

| Expression | X | x | Script F | Fraktur G |
| --- | --- | --- | --- | --- |
| `X+x+\mathcal F+\mathfrak G` | U+1D44B | U+1D465 | U+2131 | U+1D50A |
| `\symup{X+x+\mathcal F+\mathfrak G}` | U+0058 | U+0078 | U+2131 | U+1D50A |

Thus `\symup{...}` makes the ordinary Latin letters upright while the nested
explicit script and Fraktur alphabets retain their own forms in this runtime.
The result concerns these tested controls, not any reading of the printed FGA.
Relevant implementation locators are unicode-math-luatex.sty's
`normal-style`/`math-style` handlers and `__um_prepare_mathstyle:n`.

In amsmath 2.17t, `\tagsleft@true` is itself a local conditional assignment,
but several tag-placement definitions are selected when the package loads.
In particular, `\veqno` is bound at package loading and used by ordinary
equation displays. Changing the conditional alone is therefore not a complete
local tag-placement switch. The class/package `leqno` option is the appropriate
initialization when left equation numbers are wanted throughout.

## Reproduce the infrastructure checks

From the package root, with TeX binaries and a basic installed TeX distribution:

```sh
python scripts/tex_runtime.py --setup
python scripts/tooling_preflight.py --runtime runtime
python scripts/run_tooling_probes.py --runtime runtime
```

The setup script prepares only the local runtime. It does not build an edition.
After setup, run an edition's required command through the wrapper, for example:

```sh
python scripts/tex_runtime.py --cwd sources/fr/fr -- lualatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

Use the same wrapper for each required pass. It supplies the prepared fonts and
formats and manages a temporary font cache inside the command's working
directory. This permits LuaTeX's cache writes without relaxing TeX's file-output
restrictions. The temporary cache is removed after the command.

Generated runtime caches, raw logs, and Python bytecode are execution
intermediates and must not be included in the delivered source package; they
can contain machine-local paths. The portable scripts and this report contain
no machine-local path or e-mail address.
