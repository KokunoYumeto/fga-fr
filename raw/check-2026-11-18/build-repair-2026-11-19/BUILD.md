# Build of the repaired French, 19 November 2026

LuaLaTeX (MiKTeX), three passes of `fr/main.tex` from the `fr` directory, after `fix_fr.py`:

- errors in the last pass: 0
- overfull boxes: 0
- underfull boxes: 9
- pages: 151

Before the repair one pass stopped on 27 errors (listed by place in `REPAIR_LOG.tsv`) and, once those were repaired, five lines ran 5.4pt to 36.7pt into the margin; both are repaired as logged. The LuaLaTeX log is not published because it holds local paths.
