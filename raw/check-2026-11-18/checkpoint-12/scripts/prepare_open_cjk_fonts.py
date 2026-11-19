#!/usr/bin/env python3
"""Copy verified installed Noto CJK fonts into the task-local TeX runtime."""

import argparse
import csv
import hashlib
import html
from pathlib import Path
import shutil
import subprocess

from tex_runtime import environment

QUERIES = ["Noto Sans CJK KR", "Noto Sans CJK KR:style=Bold",
           "Noto Serif CJK SC", "Noto Serif CJK SC:style=Bold"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    runtime = args.runtime.resolve()
    expected = {}
    if args.manifest.exists():
        expected = {r["query"]: r for r in csv.DictReader(args.manifest.open(), delimiter="\t")}
    destination = runtime / "texmf-home/fonts/opentype/public/noto-cjk"
    destination.mkdir(parents=True, exist_ok=True)
    rows = []
    env = environment(runtime)
    for query in QUERIES:
        result = subprocess.run(["fc-match", "--format=%{file}\t%{family}\t%{style}\t%{index}\t%{fontversion}\n", query],
                                env=env, text=True, capture_output=True, check=True)
        filename, family, style, index, version = result.stdout.strip().split("\t")
        if query.split(":")[0] not in family:
            raise RuntimeError("Required Noto CJK family unavailable; install the documented open font release: " + query)
        source = Path(filename)
        data = source.read_bytes()
        row = {"query": query, "family": family, "style": style,
               "collection_index": index, "fontversion": version,
               "file": source.name, "bytes": str(len(data)),
               "sha256": hashlib.sha256(data).hexdigest(),
               "license": "SIL Open Font License 1.1"}
        if expected and any(row[key] != expected[query][key] for key in ("sha256", "bytes", "collection_index")):
            raise RuntimeError("Installed Noto CJK font differs from the recorded baseline: " + query)
        target = destination / source.name
        if source.resolve() != target.resolve():
            shutil.copy2(source, target)
        rows.append(row)
    config = runtime / "fonts.conf"
    text = config.read_text()
    directory = "<dir>" + html.escape(str(destination)) + "</dir>"
    if directory not in text:
        config.write_text(text.replace("<fontconfig>", "<fontconfig>" + directory, 1))
    subprocess.run(["fc-cache", "-f", str(destination)], env=environment(runtime), check=True)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    with args.manifest.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    print("Four verified Noto CJK font collections are available in the task-local runtime.")


if __name__ == "__main__":
    main()
