#!/usr/bin/env python3
"""Run one non-stopping diagnostic pass of frozen source snapshots.

This helper never edits an edition. It is for error inventories only; its PDF
outputs are not publishable, and no page is visually inspected by this script.
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil

import build_fga
from tex_runtime import command_in_runtime


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot-work", type=Path, required=True)
    parser.add_argument("--report-work", type=Path, required=True)
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--layers", default="fr,fr_printed")
    args = parser.parse_args()
    runtime = args.runtime.resolve()
    work = args.snapshot_work.resolve()
    report = args.report_work.resolve() / "build_reports" / args.tag
    summaries, diagnostics, boxes = [], [], []
    for layer in build_fga.selected_layers(args.layers):
        entry, engine, _, _ = build_fga.LAYERS[layer]
        target = build_fga.stage_root(runtime, args.tag) / layer
        if target.exists():
            raise FileExistsError("Diagnostic stage exists; use a new tag")
        source = work / "sources" / layer
        source_hash = build_fga.tree_hash(source)
        snapshot = target / "source"
        shutil.copytree(source, snapshot)
        if build_fga.tree_hash(snapshot) != source_hash:
            raise RuntimeError("Snapshot integrity check failed")
        cwd = (snapshot / entry).parent
        stem = Path(entry).stem
        driver = target / "driver.tex"
        driver.write_text(build_fga.DRIVER.replace("ENTRYPOINT", Path(entry).name))
        log = target / "diagnostic.stdout.log"
        command = [engine, "-no-shell-escape", "-interaction=nonstopmode",
                   "-file-line-error", "-synctex=1", "-jobname=" + stem,
                   str(driver)]
        code = command_in_runtime(runtime, command, cwd, log,
                                  {"max_print_line": "100000"})
        raw = log.read_text(encoding="utf-8", errors="replace")
        overfull, messages, _ = build_fga.parse_log(raw, cwd, snapshot, layer)
        # Sanitized text retains the source diagnostics; no raw path is returned.
        report.mkdir(parents=True, exist_ok=True)
        (report / (layer + "_compiler.txt")).write_text(build_fga.sanitize(raw))
        for row in messages:
            diagnostics.append(dict(row, layer=layer))
        for row in overfull:
            boxes.append(dict(row, layer=layer))
        summaries.append({
            "layer": layer, "engine": engine, "entry": "sources/" + layer + "/" + entry,
            "passes": 1, "exit_code": code,
            "errors": sum(row["category"] == "error" for row in messages),
            "warnings": sum(row["category"] == "warning" for row in messages),
            "missing_glyphs": sum(row["category"] == "missing_glyph" for row in messages),
            "max_overfull_pt": max((row["pt"] for row in overfull), default=0),
            "source_tree_sha256": source_hash,
            "date_utc": datetime.now(timezone.utc).isoformat(),
            "status": "diagnostic pass only; not a completed build or visual review",
            "command": engine + " -no-shell-escape -interaction=nonstopmode -file-line-error -synctex=1 -jobname=" + stem + " <instrumented driver>",
        })
        if build_fga.tree_hash(source) != source_hash:
            raise RuntimeError("Frozen input changed during diagnostic build")
        print(layer + ": diagnostic pass finished; " + str(summaries[-1]["errors"]) + " errors", flush=True)
        (target / "diagnostic.json").write_text(json.dumps(summaries[-1], indent=2))
    build_fga.write_tsv(report / "DIAGNOSTIC_SUMMARY.tsv", list(summaries[0]), summaries)
    build_fga.write_tsv(report / "DIAGNOSTICS.tsv",
                       ["layer", "category", "source", "line", "message", "log_line"], diagnostics)
    build_fga.write_tsv(report / "OVERFULL_BOXES.tsv",
                       ["layer", "box", "pt", "source", "line_start", "line_end",
                        "shipout_candidate", "log_line"], boxes)
    (report / "README.md").write_text(
        "# Baseline diagnostic pass\n\n"
        "One non-stopping LuaLaTeX pass was run on each frozen source snapshot. "
        "These records inventory compiler errors before repairs; any emitted PDF is invalid "
        "for publication. Auxiliary stability, reference resolution, overflow repair, "
        "and visual review are not certified. Sanitized compiler text is retained here; "
        "raw logs and copied build trees remain outside the deliverables.\n")


if __name__ == "__main__":
    main()
