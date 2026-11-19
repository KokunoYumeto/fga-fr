#!/usr/bin/env python3
"""Run zero-page package/font probes without reading edition sources."""
import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path
import shutil

from tex_runtime import command_in_runtime


def main():
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path, default=base.parent / "runtime")
    parser.add_argument("--output", type=Path, default=base.parent / "TOOLING_PROBE_RESULTS.tsv")
    args = parser.parse_args()
    runtime = args.runtime.resolve()
    target = runtime / "tooling-probes"
    target.mkdir(parents=True, exist_ok=True)
    for source in (base / "tooling_probes").iterdir():
        if source.is_file():
            shutil.copy2(source, target / source.name)
    rows = []
    probes = [("lualatex", "lua-fonts.tex", "FGA-ZERO-PAGE-FONT-SMOKE-PASS"),
              ("xelatex", "xe-fonts.tex", "FGA-ZERO-PAGE-XETEX-SMOKE-PASS"),
              ("lualatex", "math-probe.tex", "FGA-MATH-symup:")]
    for engine, source, marker in probes:
        command = [engine, "-interaction=nonstopmode", "-halt-on-error", "-no-shell-escape", source]
        log = runtime / "logs" / (source + ".probe.txt")
        code = command_in_runtime(runtime, command, target, log)
        transcript = log.read_text(encoding="utf-8", errors="replace")
        pdf = target / Path(source).with_suffix(".pdf")
        # LuaTeX with hyperref can leave an empty placeholder despite shipping
        # no pages. An empty file is not a PDF containing an inspected page.
        no_pdf = not pdf.exists() or pdf.stat().st_size == 0
        passed = code == 0 and marker in transcript and no_pdf and "no pages of output" in transcript.lower()
        rows.append({"probe": source, "date_utc": datetime.now(timezone.utc).isoformat(),
                     "command": " ".join(command), "exit_code": code,
                     "result": ("PASS; zero pages generated" +
                                ("; zero-byte PDF placeholder" if pdf.exists() and pdf.stat().st_size == 0 else ""))
                               if passed else "FAIL; inspect local runtime log"})
        for line in transcript.splitlines():
            if line.startswith("FGA-MATH-"):
                label, value = line.split(": ", 1)
                rows.append({"probe": label, "date_utc": rows[-1]["date_utc"],
                             "command": "glyph traversal of an unshipped math box",
                             "exit_code": code, "result": value})
        print(source, "PASS" if passed else "FAIL", "exit", code)
    with args.output.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["probe", "date_utc", "command", "exit_code", "result"], delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    if any(row["result"].startswith("FAIL") for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
