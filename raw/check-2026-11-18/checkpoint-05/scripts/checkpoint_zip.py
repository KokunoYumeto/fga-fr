#!/usr/bin/env python3
"""Create a complete, immutable FGA checkpoint ZIP from the current work tree.

Use --plan to inspect eligibility without creating an archive. No Library action
is performed. A completed archive is published with an exclusive hard link, so
an existing checkpoint is never overwritten, renamed, or deleted.
"""

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import re
import tempfile
import zipfile


MAX_ARCHIVE_BYTES = 500_000_000
EXCLUDED_DIRS = {
    "runtime", "inputs", "upload", "scans", "renders", "rendered",
    "rendered_scans", "checkpoints", "archives", "__pycache__", ".cache",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".git", "node_modules",
}
BUILD_SUFFIXES = {
    ".aux", ".out", ".toc", ".lof", ".lot", ".fls", ".fdb_latexmk",
    ".xdv", ".dvi", ".nav", ".snm", ".vrb", ".bcf", ".blg", ".pyc",
}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp", ".bmp"}
TEXT_SUFFIXES = {
    ".tex", ".md", ".tsv", ".csv", ".json", ".jsonl", ".yaml", ".yml",
    ".toml", ".py", ".lua", ".ps1", ".cff", ".txt", ".log", ".sh",
}
INPUT_NAMES = {"FGA_scans.zip", "FGA_sources.zip", "FGA_context.zip",
               "PROMPT(20261118-153104).md"}
CHECKPOINT_NAME = re.compile(r"^FGA_CHECK(?:_checkpoint_\d+)?(?:_part\d+)?\.zip$", re.I)
GENERATED_NAMES = {"CHECKPOINT_FILE_LIST.tsv", "CHECKPOINT_INFO.md"}
EMAIL = re.compile(r"(?<![\w.+-])[\w.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![\w])")
UNIX_LOCAL = re.compile(r"(?<![\w:])/(?:workspace|home|Users|tmp|private|mnt|var/folders)/")
WINDOWS_LOCAL = re.compile(
    r"(?<![A-Za-z\\])[A-Za-z]:[\\/](?:Users|Documents and Settings|workspace|home|tmp|Temp|projects|repos|work|Desktop)[\\/]",
    re.I,
)


def exclude_reason(relative, allow_images):
    if any(part in EXCLUDED_DIRS or part.startswith("fga-tex-cache-")
           for part in relative.parts[:-1]):
        return "input, runtime, cache, archive, or rendering directory"
    if relative.name in INPUT_NAMES:
        return "supplied attachment"
    if CHECKPOINT_NAME.fullmatch(relative.name):
        return "earlier checkpoint or final archive"
    if relative.name in GENERATED_NAMES:
        return "previous generated checkpoint inventory"
    if relative.suffix in BUILD_SUFFIXES or relative.name.endswith((".synctex.gz", ".run.xml")):
        return "build intermediate or Python bytecode"
    if relative.suffix == ".log" and relative.as_posix() != "progress.log":
        return "raw build or execution log"
    if relative.suffix.lower() in IMAGE_SUFFIXES and relative.as_posix() not in allow_images:
        return "rendered image not explicitly retained as documented problem evidence"
    return ""


def privacy_issues(relative, data):
    issues = []
    text = relative.as_posix()
    if EMAIL.search(text) or UNIX_LOCAL.search(text) or WINDOWS_LOCAL.search(text):
        issues.append("unsafe path name")
    if relative.suffix.lower() in TEXT_SUFFIXES:
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError:
            issues.append("text file is not UTF-8; inspect before packaging")
            return issues
        for number, line in enumerate(text.splitlines(), 1):
            kinds = []
            if EMAIL.search(line):
                kinds.append("email pattern")
            if UNIX_LOCAL.search(line) or WINDOWS_LOCAL.search(line):
                kinds.append("machine-path pattern")
            if kinds:
                issues.append("line " + str(number) + ": " + ", ".join(kinds))
    return issues


def snapshot(root, allow_images):
    entries = []
    excluded = []
    faults = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        reason = exclude_reason(relative, allow_images)
        if path.is_symlink():
            if not reason:
                faults.append(relative.as_posix() + ": symbolic link requires explicit handling")
            continue
        if not path.is_file():
            continue
        if reason:
            excluded.append((relative.as_posix(), reason))
            continue
        before = path.stat()
        data = path.read_bytes()
        after = path.stat()
        fingerprint = (before.st_size, before.st_mtime_ns)
        if fingerprint != (after.st_size, after.st_mtime_ns):
            faults.append(relative.as_posix() + ": changed while being read")
        faults.extend(relative.as_posix() + ": " + issue for issue in privacy_issues(relative, data))
        entries.append({"path": path, "relative": relative.as_posix(), "data": data,
                        "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                        "fingerprint": fingerprint})
    existing = {entry["relative"] for entry in entries}
    for image in sorted(allow_images - existing):
        faults.append(image + ": requested evidence image is missing or excluded")
    if faults:
        raise RuntimeError("Checkpoint preparation failed:\n" + "\n".join(faults))
    return entries, excluded


def inventory(entries, excluded, archive_name, created):
    info = ("# FGA checkpoint\n\n"
            f"Archive: {archive_name}\n\nCreated UTC: {created}\n\n"
            f"Current work files included: {len(entries)}.\n\n"
            "This is a complete snapshot of the current deliverables, including every "
            "current source tree. No deliverable is omitted as unchanged, and no "
            "earlier checkpoint is needed to recover an included file. "
            "Earlier checkpoint ZIPs and supplied attachments are not nested here.\n\n"
            "CHECKPOINT_FILE_LIST.tsv lists each included file with its SHA-256 and "
            "each excluded intermediate with its reason. Its own hash is intentionally "
            "omitted to avoid a self-referential checksum. An included filename does "
            "not imply that its textual or mathematical audit is complete; consult "
            "CHECK_RECORD.md, CHECK_EVENTS.tsv, and progress.log for actual status.\n").encode()
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
    writer.writerow(["path", "status", "bytes", "sha256", "reason", "checkpoint"])
    for entry in entries:
        writer.writerow([entry["relative"], "included", entry["bytes"], entry["sha256"],
                         "complete current deliverable", archive_name])
    writer.writerow(["CHECKPOINT_INFO.md", "included", len(info), hashlib.sha256(info).hexdigest(),
                     "generated checkpoint information", archive_name])
    writer.writerow(["CHECKPOINT_FILE_LIST.tsv", "included", "", "",
                     "this inventory; self-hash omitted", archive_name])
    for name, reason in excluded:
        writer.writerow([name, "excluded", "", "", reason, ""])
    return info, stream.getvalue().encode()


def publish(root, output, entries, info, file_list):
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError("Checkpoint already exists: " + output.name)
    descriptor, temporary_name = tempfile.mkstemp(prefix="fga-packing-", suffix=".tmp", dir=output.parent)
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
            for entry in entries:
                archive.writestr(entry["relative"], entry["data"])
            archive.writestr("CHECKPOINT_INFO.md", info)
            archive.writestr("CHECKPOINT_FILE_LIST.tsv", file_list)
        size = temporary.stat().st_size
        if size >= MAX_ARCHIVE_BYTES:
            raise RuntimeError("Compressed archive reaches the 500 MB cap; partition before saving")
        with zipfile.ZipFile(temporary) as archive:
            corrupt = archive.testzip()
            if corrupt:
                raise RuntimeError("ZIP integrity failure: " + corrupt)
        for entry in entries:
            now = entry["path"].stat()
            if (now.st_size, now.st_mtime_ns) != entry["fingerprint"]:
                raise RuntimeError("Work changed during packing: " + entry["relative"])
        # Atomic no-overwrite publication; never use replace() on a checkpoint.
        os.link(temporary, output)
        return size
    finally:
        temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--number", type=int, required=True)
    parser.add_argument("--not-before", help="Optional earliest UTC ISO timestamp; ignored by --plan")
    parser.add_argument("--plan", action="store_true", help="Inspect without creating or saving an archive")
    parser.add_argument("--allow-image", action="append", default=[], metavar="RELATIVE_PATH",
                        help="Retain one image specifically discussed as a problem in a report")
    args = parser.parse_args()
    if args.number < 1:
        parser.error("Checkpoint number must be positive")
    root = args.root.resolve()
    required = ["sources", "scripts", "CORRECTIONS.tsv", "CHECK_RECORD.md",
                "CHECK_EVENTS.tsv", "NOTES.md", "PDF_CHECK.md", "README.md", "progress.log"]
    missing = [name for name in required if not (root / name).exists()]
    if missing:
        parser.error("Work tree is incomplete; required entries missing: " + ", ".join(missing))
    output_dir = args.output_dir.resolve() if args.output_dir else root.parent / "checkpoints"
    name = f"FGA_CHECK_checkpoint_{args.number:02d}.zip"
    output = output_dir / name
    try:
        output.relative_to(root)
    except ValueError:
        pass
    else:
        parser.error("Put checkpoint archives outside the current work tree")
    allow_images = set()
    for value in args.allow_image:
        path = Path(value)
        if path.is_absolute() or ".." in path.parts:
            parser.error("Evidence image paths must be relative to the work tree")
        allow_images.add(path.as_posix())
    now = datetime.now(timezone.utc)
    if args.not_before and not args.plan:
        earliest = datetime.fromisoformat(args.not_before.replace("Z", "+00:00"))
        if earliest.tzinfo is None:
            parser.error("--not-before requires an explicit time zone")
        if now < earliest:
            parser.error("The requested hourly checkpoint time has not arrived")
    entries, excluded = snapshot(root, allow_images)
    summary = {"archive": name, "mode": "plan" if args.plan else "created",
               "included_files": len(entries), "excluded_intermediates": len(excluded),
               "uncompressed_work_bytes": sum(entry["bytes"] for entry in entries),
               "unchanged_deliverables_omitted": 0, "archive_limit_bytes": MAX_ARCHIVE_BYTES}
    if not args.plan:
        info, file_list = inventory(entries, excluded, name, now.isoformat())
        summary["archive_bytes"] = publish(root, output, entries, info, file_list)
        summary["sha256"] = hashlib.sha256(output.read_bytes()).hexdigest()
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
