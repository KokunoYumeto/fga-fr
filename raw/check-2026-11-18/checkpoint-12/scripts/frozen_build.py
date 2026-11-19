#!/usr/bin/env python3
"""Freeze selected source trees, build them, and retain sanitized reports.

Edition edits should pause only while the initial copies are made. The compiler
and all build-time integrity checks use the frozen copies, never the live trees.
No text review, source editing, or visual PDF inspection is performed.
"""

import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import subprocess
import sys

from build_fga import BASE, selected_layers, stage_root


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, default=BASE)
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--frozen-root", type=Path, required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--layers", default="fr,fr_printed")
    parser.add_argument("--max-passes", type=int, default=3)
    parser.add_argument("--note", default="")
    args = parser.parse_args()
    work = args.work.resolve()
    runtime = args.runtime.resolve()
    layers = selected_layers(args.layers)
    # Reuse the build runner's tag validation before constructing destinations.
    stage_root(runtime, args.tag)
    frozen = args.frozen_root.resolve() / args.tag
    report = work / "build_reports" / args.tag
    if frozen.exists() or report.exists() or stage_root(runtime, args.tag).exists():
        raise FileExistsError("A frozen work tree, report, or build stage already exists; use a new tag")
    frozen.mkdir(parents=True)
    started = datetime.now(timezone.utc).isoformat()
    for layer in layers:
        shutil.copytree(work / "sources" / layer, frozen / "sources" / layer)
    finished = datetime.now(timezone.utc).isoformat()
    print("Source copies frozen; live edition work may continue.", flush=True)
    command = [sys.executable, "-B", str(Path(__file__).with_name("build_fga.py")),
               "--work", str(frozen), "--runtime", str(runtime), "build",
               "--layers", ",".join(layers), "--tag", args.tag,
               "--max-passes", str(args.max_passes)]
    result = subprocess.run(command)
    source_report = frozen / "build_reports" / args.tag
    if not source_report.is_dir():
        raise RuntimeError("Build runner produced no report stage; inspect runtime failure")
    shutil.copytree(source_report, report)
    note = ("\nSnapshot note: " + args.note + "\n") if args.note else ""
    (report / "FROZEN_BUILD.md").write_text(
        "# Build from frozen source copies\n\n"
        + "Stage: `" + args.tag + "`. Layers: " + ", ".join(layers) + ".\n\n"
        + "Copy started: " + started + ". Copy completed: " + finished + ".\n\n"
        + "All compilation and build-time source-integrity comparisons used frozen copies. "
        "Later changes to the live edition trees were not read or assessed. "
        "The sanitized build reports were copied without modification and retain their "
        "original source-tree hashes. No PDF was published and no visual inspection "
        "was performed by this helper.\n" + note)
    print("Sanitized frozen-build reports retained under build_reports/" + args.tag + ".", flush=True)
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
