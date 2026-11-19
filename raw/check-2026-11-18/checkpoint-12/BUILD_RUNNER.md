# Build and rendering runner

The runner is prepared for the later build phase. Preparing it did not build an
edition, inspect a scan, compare prose or formulas, or change a source file.
PDF_CHECK.md remains the authoritative human-readable record of the actual
build and visual checks when those are performed.

## Entry points

| Layer | Entry point within sources | Engine | Passes |
| --- | --- | --- | --- |
| French corrected | fr/fr/main.tex | LuaLaTeX | At least three; continue if necessary |
| French as printed | fr_printed/fr/main.tex | LuaLaTeX | At least three; continue if necessary |
| English | en/en/main.tex | LuaLaTeX | At least three; continue if necessary |
| Spanish corrected | es/es/FGA_ES_CURRENT.tex | LuaLaTeX | At least three; continue if necessary |
| Spanish 149 as printed | es_149_printed/es/FGA_ES_149_PRINTED.tex | LuaLaTeX | At least three; continue if necessary |
| Portuguese corrected | pt-BR/pt_BR/FGA_PTBR_CURRENT.tex | XeLaTeX | Exactly three prescribed passes |
| Portuguese as printed | pt-BR_printed/pt_BR/FGA_PTBR_PRINTED.tex | XeLaTeX | Exactly three prescribed passes |
| Vietnamese corrected | vi/FGA_vi_current.tex | LuaLaTeX | At least three; continue if necessary |
| Vietnamese diplomatic | vi_diplomatic/FGA_vi_diplomatic.tex | LuaLaTeX | At least three; continue if necessary |
| Korean | ko/main.tex | XeLaTeX | At least three; continue if necessary |
| Simplified Chinese | zh-Hans/source/zh/main.tex | XeLaTeX | At least three; continue if necessary |

The paths follow the supplied trees. In particular, the Korean README's
repository-level source directory is already the supplied ko directory.
The runner also checked that adjustbox and collectbox, used by the Chinese
entry point, are available in the isolated runtime.

## Commands from the package root

The default runtime directory is runtime. Prepare it with
scripts/tex_runtime.py --setup if it is not already present. All commands below
are Python script invocations. In the live scratch workspace, invoke the
scripts under work/scripts and add --runtime runtime before the subcommand.

List the eleven layers without building:

    python scripts/build_fga.py plan

Build all layers, retaining a distinct baseline stage:

    python scripts/build_fga.py build --layers all --tag baseline

Build selected layers after correcting their preambles or line breaking:

    python scripts/build_fga.py build --layers fr,fr_printed --tag after_01

Each stage/layer directory is immutable to this runner: an existing one is
refused, so use a new tag for a later run. The non-Portuguese builds continue
only while auxiliary files or rerun diagnostics require another pass, with a
default maximum of six. The Portuguese builds retain the requested three-pass
procedure and report any remaining instability.
The build command returns a nonzero status if any selected layer fails the
automated requirements, including the 2 pt overflow limit; its reports preserve
the distinction between an engine failure and a typesetting issue.

Render specific physical PDF pages, or a spread through a book:

    python scripts/build_fga.py render --layer fr --tag after_01 --pages 1,10-12,last
    python scripts/build_fga.py render --layer fr --tag after_01 --pages spread

The default render resolution is 400 dpi. A spread selects the first two pages,
quarter points, and last page, with duplicate page numbers removed.

Render baseline pages with boxes exceeding 10 pt, then locate their candidates
in a later build:

    python scripts/build_fga.py render-overflows --layer fr --baseline baseline --tag baseline
    python scripts/build_fga.py render-overflows --layer fr --baseline baseline --tag after_01

Inspect those images separately. Any unmapped baseline box is reported as
requiring manual location. A later build is mapped using the earlier source
line locations; check those locations if a typesetting repair changed source
line numbering.

Copy successful build PDFs into the deliverable pdf directory:

    python scripts/build_fga.py publish-pdfs --layers fr,fr_printed --tag after_01

The copy operation requires stable auxiliary files, an error-free engine run,
no missing-glyph or unresolved-reference diagnostic, and no recorded overfull
box above 2 pt. It does not certify visual review. Final visual observations
must still be written in PDF_CHECK.md.
The current source-tree hash must also match the chosen build, so a stale PDF
cannot be copied after further source edits.

## Build isolation and evidence

Each layer is copied byte-for-byte into its runtime stage, with a SHA-256 of
the source tree checked before compilation. The prescribed entry point is
compiled in its own directory inside that unchanged snapshot. A separate
driver installs log-only file and physical-shipout hooks; it does not insert
typeset material or alter the edition's files, credits, or rights notices.
The original source-tree hash is checked again after the run.

The engine is invoked with shell escape disabled, file/line diagnostics, and
SyncTeX enabled. The runtime wrapper supplies its installed fonts and formats
and manages the temporary font cache. Raw logs, driver files, compiled build
copies, SyncTeX files, and rendered PNGs remain outside the deliverable tree.

The runner writes sanitized, cumulative stage reports into build_reports:

| Report | Contents |
| --- | --- |
| BUILD_SUMMARY.tsv | Engine, entry point, command, actual passes, PDF page count, stability, diagnostic totals, overflow totals, source-tree hash, and build status |
| OVERFULL_BOXES.tsv | Every pass's box sizes, source context, line range, candidate PDF pages, and mapping method; the latest pass is identified |
| DIAGNOSTICS.tsv | Sanitized error, warning, and missing-glyph messages with their source context |
| RENDERED_PAGES.tsv | Pages rendered, dpi, reason, timestamp, and an explicit statement that rendering is not visual inspection |
| OVERFLOW_REVIEW_MAP.tsv | Baseline overflows mapped to candidate pages in the chosen review stage |

All page numbers in these tables are one-based physical PDF pages. The runner
first uses SyncTeX nodes in the diagnostic's source-line range, then a SyncTeX
forward query, then a clearly labelled next-shipout candidate. File-hook
context can be approximate when TeX typesets delayed material. Every mapping
therefore retains its method and requires visual confirmation.

## Infrastructure verification

scripts/build_runner_selftest.py exercises the hooks and SyncTeX mapping on
two synthetic rule-only pages, each with a deliberate overflow. It reads no
edition and renders no image. The test mapped the two overflows to distinct
physical PDF pages 1 and 2; the sanitized evidence is in
BUILD_RUNNER_SELFTEST.tsv. No book has been built by this test.

## Checkpoint compatibility

The checkpoint packager includes these new scripts, this document, the
synthetic-test evidence, and all future sanitized build_reports files.
Execution caches and rendered pages are excluded. No attached ZIP or separate
unchanged input tree is nested in a checkpoint. Unchanged files that belong
to the required complete current source trees are included once in those
trees, as needed for a self-contained recoverable snapshot. No deliverable is
omitted as unchanged.
