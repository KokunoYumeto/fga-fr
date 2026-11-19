"""Apply the byte-audited layout candidate to a separate frozen work tree only.

No live edition path is accepted. Exact-context preflight runs before any write.
The pinned insertion set retains every original source byte and math delimiter.
Compilation and visual review remain separate steps.
"""

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path, PurePosixPath


BASE = Path(__file__).resolve().parents[1]
INSERTIONS_SHA256 = "fc5264a74c476b875748742f145da216eae182cf98cccf0fa6ed488ddc2f104d"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True,
                        help="existing separate frozen work tree containing sources/")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    work = args.work.resolve()
    if work == BASE or BASE in work.parents:
        raise ValueError("A separate frozen work tree outside the deliverable is required")
    source_root = work / "sources"
    if not source_root.is_dir() or not source_root.resolve().is_relative_to(work):
        raise ValueError("Frozen sources must be a directory inside the requested work tree")
    metadata = BASE / "layout_diagnostics/PROPOSED_LAYOUT_INSERTIONS.json"
    payload = metadata.read_bytes()
    if digest(payload) != INSERTIONS_SHA256:
        raise ValueError("Insertion metadata differs from the audited candidate")
    changes = json.loads(payload)
    grouped = defaultdict(list)
    for change in changes:
        rel = PurePosixPath(change["path"])
        if rel.is_absolute() or ".." in rel.parts or rel.suffix != ".tex":
            raise ValueError("Invalid relative source path in insertion metadata")
        grouped[rel.as_posix()].append(change)
    planned = []
    for rel, entries in grouped.items():
        path = source_root / rel
        resolved = path.resolve()
        if not resolved.is_relative_to(work) or resolved == BASE or BASE in resolved.parents:
            raise ValueError("A source path leaves the separate frozen work tree")
        original = path.read_bytes()
        candidate = original
        for change in entries:
            before = change["before"].encode()
            after = change["after"].encode()
            if candidate.count(before) != 1 or after in candidate:
                raise ValueError("Expected unapplied context is not unique in sources/" + rel)
            candidate = candidate.replace(before, after, 1)
        recovered = candidate
        for change in reversed(entries):
            after = change["after"].encode()
            if recovered.count(after) != 1:
                raise ValueError("Reverse recovery is not unique in sources/" + rel)
            recovered = recovered.replace(after, change["before"].encode(), 1)
        if recovered != original:
            raise ValueError("Original-byte recovery failed in sources/" + rel)
        planned.append((rel, path, original, candidate, len(entries)))
    if len(changes) != 14 or len(planned) != 9:
        raise ValueError("The audited candidate must contain 14 regions in 9 files")
    if args.check_only:
        print("Preflight passed: 14 exact layout regions in 9 frozen source files; no writes.")
        return
    for rel, path, original, candidate, count in planned:
        if path.read_bytes() != original:
            raise RuntimeError("Frozen source changed during preflight: sources/" + rel)
    for rel, path, original, candidate, count in planned:
        path.write_bytes(candidate)
    report = {
        "candidate": "layout_mechanical_07",
        "metadata_sha256": INSERTIONS_SHA256,
        "layout_regions": len(changes),
        "changed_files": len(planned),
        "original_bytes_recoverable": True,
        "visual_review": "not performed",
        "files": [{"path": "sources/" + rel,
                   "before_sha256": digest(original),
                   "after_sha256": digest(candidate),
                   "layout_regions": count}
                  for rel, path, original, candidate, count in planned],
    }
    report_path = work / "layout_candidate_application.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print("Applied 14 exact layout regions in 9 frozen source files; compilation is pending.")


if __name__ == "__main__":
    main()
