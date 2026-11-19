# Automated build evidence

These tables record actual engine runs. They do not record a visual inspection. Page numbers are one-based physical PDF pages. Source locations come from LaTeX file-hook context; delayed typesetting can make that context approximate. SyncTeX and next-shipout mappings are candidates to verify visually. All raw logs, copied build trees, and SyncTeX files remain outside this deliverable tree.

The two Portuguese layers run exactly three prescribed XeLaTeX passes. Other layers run at least three passes and continue only while auxiliary files or rerun diagnostics require it, up to the requested maximum. A typeset result with no recorded overflow above 2 pt still needs the visual checks required in PDF_CHECK.md.
