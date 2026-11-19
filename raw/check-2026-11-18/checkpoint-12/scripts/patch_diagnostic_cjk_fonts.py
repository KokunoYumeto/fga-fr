#!/usr/bin/env python3
"""Apply the minimal open-font patch to a separate diagnostic work tree only."""

import argparse
import csv
import difflib
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
PATCHES = {
    "ko/base-ko.tex": [("Malgun Gothic Bold", "Noto Sans CJK KR Bold", 1),
                        ("Malgun Gothic", "Noto Sans CJK KR", 3)],
    "zh-Hans/source/tex/zh.tex": [("SimSun", "Noto Serif CJK SC", 1),
                                  ("Microsoft YaHei", "Noto Sans CJK SC", 2)],
    "zh-Hans/source/zh/149.tex": [("SimSun", "Noto Serif CJK SC", 2)],
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--diagnostic-work", type=Path, required=True)
    parser.add_argument("--report-dir", type=Path, required=True)
    args = parser.parse_args()
    work = args.diagnostic_work.resolve()
    if work == BASE or work.is_relative_to(BASE):
        raise ValueError("This helper must not edit the live deliverable source trees")
    rows, diffs = [], []
    planned = []
    for name, edits in PATCHES.items():
        path = work / "sources" / name
        before = path.read_bytes()
        after = before
        for old, new, count in edits:
            old_bytes, new_bytes = old.encode(), new.encode()
            if after.count(old_bytes) != count:
                raise ValueError("Unexpected font occurrence count in " + name)
            for number, line in enumerate(after.splitlines(), 1):
                for _ in range(line.count(old_bytes)):
                    rows.append({"file": "sources/" + name, "line": number,
                                 "old_font": old, "new_font": new,
                                 "scope": "diagnostic copy only"})
            after = after.replace(old_bytes, new_bytes)
        planned.append((path, after))
        diffs.extend(difflib.unified_diff(before.decode().splitlines(keepends=True),
                                         after.decode().splitlines(keepends=True),
                                         fromfile="a/sources/" + name,
                                         tofile="b/sources/" + name))
    for path, content in planned:
        path.write_bytes(content)
    args.report_dir.mkdir(parents=True, exist_ok=True)
    (args.report_dir / "CJK_OPEN_FONT_PATCH.diff").write_text("".join(diffs), newline="")
    with (args.report_dir / "CJK_OPEN_FONT_CHANGES.tsv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    print("Nine font-name occurrences changed in three diagnostic files; other bytes preserved.")


if __name__ == "__main__":
    main()
