#!/usr/bin/env python3
"""Check the build runner with two synthetic rule-only pages, never an edition."""
import argparse
from pathlib import Path
import csv

from pypdf import PdfReader
from build_fga import BASE, DRIVER, parse_log, map_boxes, utc
from tex_runtime import command_in_runtime


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path, default=BASE / "runtime")
    args = parser.parse_args()
    runtime = args.runtime.resolve()
    root = runtime / "build_runner_selftest"
    root.mkdir(parents=True, exist_ok=True)
    (root / "fixture.tex").write_text(
        "\\documentclass{article}\n\\begin{document}\n"
        "\\input{first.tex}\n\\newpage\n\\input{second.tex}\n\\end{document}\n")
    (root / "first.tex").write_text("\\noindent\\rule{600pt}{1pt}\\par\n")
    (root / "second.tex").write_text("\\noindent\\rule{700pt}{1pt}\\par\n")
    (root / "driver.tex").write_text(DRIVER.replace("ENTRYPOINT", "fixture.tex"))
    log = root / "probe.stdout.log"
    command = ["lualatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error",
               "-file-line-error", "-synctex=1", "-jobname=fixture", "driver.tex"]
    code = command_in_runtime(runtime, command, root, log, {"max_print_line": "100000"})
    assert code == 0, "Synthetic build failed"
    pdf = root / "fixture.pdf"
    assert len(PdfReader(pdf).pages) == 2, "Fixture must have exactly two synthetic pages"
    boxes, diagnostics, labels = parse_log(log.read_text(), root, root, "tooling_fixture")
    map_boxes(boxes, pdf, root / "fixture.synctex.gz", root, root, "tooling_fixture")
    assert len(boxes) == 2, "Expected one deliberate overflow per fixture page"
    expected = {"first.tex": 1, "second.tex": 2}
    for box in boxes:
        assert Path(box["source"]).name in expected, "File-hook context was not preserved"
        assert box["line_start"] == 1 and box["line_end"] == 1
        assert box["pdf_pages"] == [expected[Path(box["source"]).name]], "PDF page mapping mismatch"
        assert box["mapping"].startswith("SyncTeX"), "Expected a SyncTeX mapping"
    assert labels == {"1": "1", "2": "2"}, "Physical shipout markers missing"
    result = BASE / "BUILD_RUNNER_SELFTEST.tsv"
    with result.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t")
        writer.writerow(["test", "date_utc", "result", "scope"])
        writer.writerow(["source context and physical page mapping", utc(), "PASS",
                         "Two synthetic rule-only pages; no edition build, rendering, or visual inspection"])
        for box in boxes:
            writer.writerow([Path(box["source"]).name, utc(),
                             "PDF page " + str(box["pdf_pages"][0]) + "; " + box["mapping"],
                             "synthetic fixture only"])
    print("PASS: two synthetic overflows mapped to their distinct physical PDF pages")


if __name__ == "__main__":
    main()
