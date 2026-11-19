#!/usr/bin/env python3
"""Package a freshly gated work snapshot as an immutable FGA_CHECK.zip.

No source or audit record is edited. Dry run performs the same fresh gate,
temporary compression, and integrity checks but publishes no archive.
Selftests use a temporary synthetic tree and never run the real validator.
"""

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

from build_fga import LAYERS
from checkpoint_zip import EMAIL, exclude_reason
from privacy_scan import scan_bytes
from validate_fga import UNITS


WORK = Path(__file__).resolve().parents[1]
LIMIT = 500_000_000
ARCHIVE = "FGA_CHECK.zip"
RESERVED = {"FINAL_FILE_LIST.tsv", "FINAL_PACKAGE.md", "FINAL_READINESS.json"}
GAP_FIELDS = ["schema_issues", "page_occurrences_with_structural_gaps",
              "translation_layer_units_with_structural_gaps", "duplicate_or_invalid_record_markers",
              "front_matter_blocks_flagged_for_review", "missing_required_items", "missing_or_invalid_pdfs",
              "missing_expected_source_files", "manifest_discrepancies", "privacy_pattern_findings"]
SCHEMAS = {
    "FILE_INVENTORY.tsv": ["path", "bytes", "sha256"],
    "PDF_INVENTORY.tsv": ["layer", "file", "status", "pages", "sha256", "inspection"],
    "SOURCE_INVENTORY.tsv": ["path", "baseline_member", "status", "bytes", "sha256", "baseline_sha256"],
    "PAGE_COVERAGE.tsv": ["unit", "printed_page", "volume", "scan", "scan_pdf_page", "heading_count",
                          "progress_completion_count", "corrected_locator_present", "printed_locator_present", "interpretation"],
    "TRANSLATION_COVERAGE.tsv": ["layer", "unit", "own_heading_count", "combined_parent_heading_count",
                                 "source_locator_present", "own_completion_count", "parent_completion_count", "interpretation"],
}


class PackageError(Exception):
    pass


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe_relative(value):
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or "\\" in value or ":" in value or any(ord(c) < 32 for c in value) or EMAIL.search(value):
        raise PackageError("A file inventory contains an unsafe relative filename; no matched content is printed.")
    return path


def final_exclusion(relative, allow_images):
    if relative.suffix.lower() == ".zip":
        return "earlier ZIP or supplied archive"
    if relative.name in RESERVED or "final_validation" in relative.parts[:-1]:
        return "earlier generated final-package metadata"
    if any(part in {"tmp", "temp", "rendered_builds"} for part in relative.parts[:-1]):
        return "temporary or rendered material"
    return exclude_reason(relative, allow_images)


def fingerprint(path):
    value = path.stat()
    return value.st_size, value.st_mtime_ns


def hash_file(path):
    before = fingerprint(path)
    result = hashlib.sha256()
    count = 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
            count += len(block)
    if before != fingerprint(path) or before[0] != count:
        raise PackageError("A work file changed while being hashed; pause edits and retry.")
    return count, result.hexdigest(), before


def snapshot(work, allow_images):
    entries, excluded = {}, []
    for path in sorted(work.rglob("*")):
        relative = path.relative_to(work)
        reason = final_exclusion(relative, allow_images)
        if path.is_symlink():
            if not reason:
                raise PackageError("A deliverable is a symbolic link: " + relative.as_posix())
            continue
        if not path.is_file():
            continue
        name = relative.as_posix()
        safe_relative(name)
        if reason:
            excluded.append({"path": name, "status": "excluded", "bytes": path.stat().st_size,
                             "sha256": "", "reason": reason})
            continue
        size, digest, stamp = hash_file(path)
        entries[name] = {"path": path, "bytes": size, "sha256": digest, "fingerprint": stamp}
    missing_images = set(allow_images) - set(entries)
    if missing_images:
        raise PackageError("A requested evidence image is absent or remains excluded.")
    return entries, excluded


def required_presence(work):
    failures = []
    for name in ["sources", "pdf", "scripts"]:
        if not (work / name).is_dir():
            failures.append("required directory missing: " + name)
    for name in ["CORRECTIONS.tsv", "CHECK_RECORD.md", "CHECK_EVENTS.tsv", "PDF_CHECK.md", "NOTES.md", "README.md", "progress.log", "scripts/validate_fga.py"]:
        if not (work / name).is_file():
            failures.append("required file missing: " + name)
    for layer, config in LAYERS.items():
        name = "sources/" + layer + "/" + config[0]
        if not (work / name).is_file():
            failures.append("layer entry point missing: " + name)
    return failures


def read_table(directory, name):
    path = directory / name
    if not path.is_file():
        raise PackageError("Fresh validation report missing: " + name)
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        rows = list(reader)
    if reader.fieldnames != SCHEMAS[name] or any(None in row or any(value is None for value in row.values()) for row in rows):
        raise PackageError("Fresh validation report has an unexpected schema: " + name)
    return rows


def numeric(summary, field):
    value = summary.get(field)
    if type(value) is not int or value < 0:
        raise PackageError("Readiness summary lacks a valid count: " + field)
    return value


def require_gate(summary, report_dir, entries, allow_images):
    faults = []
    if summary.get("mode") != "structural enforcement":
        faults.append("validator did not use structural enforcement")
    if summary.get("completion_certified") is not False:
        faults.append("validator completion-certification field is not the expected false value")
    for field in GAP_FIELDS:
        if numeric(summary, field):
            faults.append(field + "=" + str(summary[field]))
    for field in ["scan_unit_page_occurrences", "expected_translation_layer_units", "protected_files_compared"]:
        if numeric(summary, field) == 0:
            faults.append(field + " is empty")
    if numeric(summary, "protected_files_compared") != numeric(summary, "protected_files_identical"):
        faults.append("protected-file byte comparisons are not all identical")
    pages = read_table(report_dir, "PAGE_COVERAGE.tsv")
    translations = read_table(report_dir, "TRANSLATION_COVERAGE.tsv")
    if len(pages) != numeric(summary, "scan_unit_page_occurrences"):
        faults.append("page coverage table count differs from the fresh summary")
    expected_slots = {(layer, unit) for layer in LAYERS if layer not in {"fr", "fr_printed"}
                      for unit in (["149"] if layer == "es_149_printed" else UNITS)}
    actual_slots = [(row["layer"], row["unit"]) for row in translations]
    if set(actual_slots) != expected_slots or len(actual_slots) != len(expected_slots) or len(actual_slots) != numeric(summary, "expected_translation_layer_units"):
        faults.append("translation coverage table does not contain every required layer/unit exactly once")
    def positive(value):
        return value.isdigit() and int(value) > 0
    for row in pages:
        if not (positive(row["heading_count"]) and positive(row["progress_completion_count"]) and
                row["corrected_locator_present"] == "True" and row["printed_locator_present"] == "True"):
            faults.append("page coverage table contains an unresolved structural gap")
            break
    for row in translations:
        if not (row["source_locator_present"] == "True" and
                (positive(row["own_heading_count"]) or positive(row["combined_parent_heading_count"])) and
                (positive(row["own_completion_count"]) or positive(row["parent_completion_count"]))):
            faults.append("translation coverage table contains an unresolved structural gap")
            break
    file_rows = read_table(report_dir, "FILE_INVENTORY.tsv")
    listed = {}
    for row in file_rows:
        name = row["path"]
        relative = safe_relative(name)
        if final_exclusion(relative, allow_images):
            continue
        if name in listed:
            faults.append("duplicate file in validator inventory: " + name)
        listed[name] = row
    if set(listed) != set(entries):
        faults.append("validator and packaging file inventories differ")
    for name in listed.keys() & entries.keys():
        if listed[name]["sha256"] != entries[name]["sha256"] or listed[name]["bytes"] != str(entries[name]["bytes"]):
            faults.append("file changed since the gate snapshot: " + name)
    pdf_rows = read_table(report_dir, "PDF_INVENTORY.tsv")
    counts = Counter(row["layer"] for row in pdf_rows)
    if set(counts) != set(LAYERS) or any(count != 1 for count in counts.values()):
        faults.append("PDF inventory must name each of the eleven layers exactly once")
    pdf_paths = []
    for row in pdf_rows:
        name = row["file"]
        relative = safe_relative(name)
        pdf_paths.append(name)
        if not relative.parts or relative.parts[0] != "pdf" or relative.suffix.lower() != ".pdf":
            faults.append("a layer PDF is outside the required pdf directory")
        if row["status"] != "present with pages" or not row["pages"].isdigit() or int(row["pages"]) < 1:
            faults.append("a layer PDF is missing, unreadable, or has no pages")
        if name not in entries or entries[name]["bytes"] == 0 or row["sha256"] != entries[name]["sha256"]:
            faults.append("a layer PDF is absent from the archive snapshot or its hash differs")
    if len(set(pdf_paths)) != len(pdf_paths):
        faults.append("multiple layers refer to the same PDF file")
    for row in read_table(report_dir, "SOURCE_INVENTORY.tsv"):
        name = row["path"]
        safe_relative(name)
        if name not in entries or row["sha256"] != entries[name]["sha256"]:
            faults.append("an inventoried source file is missing, excluded, or changed: " + name)
    if faults:
        raise PackageError("Readiness gate blocked packaging:\n" + "\n".join(faults))
    return pdf_rows


def run_validator(args, run_dir):
    reports = run_dir / "validation"
    command = [sys.executable, "-B", str(args.work / "scripts" / "validate_fga.py"),
               "--work", str(args.work), "--output", str(reports), "--enforce-structure"]
    for option in ["sources_zip", "scans_zip", "context_zip", "pdf_map"]:
        value = getattr(args, option)
        if value is not None:
            command += ["--" + option.replace("_", "-"), str(value)]
    for value in args.allow_image:
        command += ["--allow-image", value]
    with (run_dir / "validator.stdout.log").open("wb") as stdout, (run_dir / "validator.stderr.log").open("wb") as stderr:
        process = subprocess.run(command, stdout=stdout, stderr=stderr, check=False)
    try:
        summary = json.loads((run_dir / "validator.stdout.log").read_text())
    except (ValueError, UnicodeError):
        raise PackageError("Validator did not return a readable JSON summary; private logs retain the failure.")
    if not isinstance(summary, dict):
        raise PackageError("Validator returned an unexpected summary type; private logs retain the failure.")
    (run_dir / "readiness-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if process.returncode != 0:
        gaps = [field + "=" + str(summary.get(field, "missing")) for field in GAP_FIELDS if summary.get(field) != 0]
        raise PackageError("Validator structural enforcement failed (exit " + str(process.returncode) + "). " + "; ".join(gaps))
    return summary, reports


def table_bytes(columns, rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=columns, delimiter="\t", lineterminator="\n", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode()


def generated_files(summary, reports, entries, excluded, pdfs):
    generated = {}
    for path in sorted(reports.rglob("*")):
        if path.is_file() and not path.is_symlink() and path.suffix in {".md", ".tsv"}:
            name = "final_validation/" + path.relative_to(reports).as_posix()
            safe_relative(name)
            generated[name] = path.read_bytes()
    generated["FINAL_READINESS.json"] = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode()
    info = ("# Final package mechanical evidence\n\n"
            "Archive: FGA_CHECK.zip\n\n"
            "This archive contains a complete current deliverable snapshot, including every included source file; no earlier checkpoint is needed to recover it. Original input archives, runtime/cache material, renderings, earlier ZIPs, and excluded intermediates are not nested here. Existing checkpoints were not changed.\n\n"
            "A fresh validate_fga.py structural-enforcement run passed, its file hashes matched the packaged snapshot, and all eleven layers had distinct, nonempty, hash-matching PDFs reported as readable with pages. Fresh validation tables are in final_validation/. Earlier readiness reports may also remain as historical work files.\n\n"
            "These are mechanical checks. The packager does not certify page reading, correction verdicts or evidence, mathematical decisions, translation accuracy, current-source build provenance, PDF visual inspection, or inline credit preservation. Those remain the human audit's responsibility and must be recorded in the audit documents.\n\n"
            "FINAL_FILE_LIST.tsv lists every archive member and its SHA-256, except its own self-referential hash. That entry intentionally has no hash or byte count. Excluded paths and reasons are also listed; excluded contents are not read for hashing. ZIP integrity and every included member hash were checked before publication. The final archive and manifest hashes are reported by the command.\n\n"
            "## PDF inventory\n\n| Layer | File | Pages |\n| --- | --- | --- |\n")
    info += "".join("| " + row["layer"] + " | " + row["file"] + " | " + str(row["pages"]) + " |\n" for row in pdfs)
    generated["FINAL_PACKAGE.md"] = info.encode()
    rows = [{"path": name, "status": "included", "bytes": item["bytes"], "sha256": item["sha256"], "reason": "complete current work file"} for name, item in sorted(entries.items())]
    rows += [{"path": name, "status": "included", "bytes": len(data), "sha256": sha(data), "reason": "fresh mechanical packaging evidence"} for name, data in sorted(generated.items())]
    rows.append({"path": "FINAL_FILE_LIST.tsv", "status": "included", "bytes": "", "sha256": "", "reason": "this manifest; self-hash intentionally omitted"})
    rows += excluded
    generated["FINAL_FILE_LIST.tsv"] = table_bytes(["path", "status", "bytes", "sha256", "reason"], rows)
    for name, data in generated.items():
        findings, _ = scan_bytes(name, data)
        if findings:
            raise PackageError("Privacy patterns found in generated package text: " + name)
    return generated


def ensure_snapshot(work, entries, allow_images):
    names = set()
    for path in work.rglob("*"):
        relative = path.relative_to(work)
        if final_exclusion(relative, allow_images):
            continue
        if path.is_symlink():
            raise PackageError("A deliverable became a symbolic link while packaging.")
        if path.is_file():
            names.add(relative.as_posix())
    if names != set(entries):
        raise PackageError("The deliverable file set changed while packaging; pause edits and retry.")
    for name, item in entries.items():
        if fingerprint(item["path"]) != item["fingerprint"]:
            raise PackageError("A work file changed while packaging: " + name)


def make_archive(work, output, run_dir, entries, generated, allow_images, dry_run=False, limit=LIMIT):
    if output.exists() or output.is_symlink():
        raise PackageError("Refusing to overwrite existing archive: " + output.name)
    temporary = run_dir / "candidate.zip"
    expected = {name: (item["bytes"], item["sha256"]) for name, item in entries.items()}
    expected.update({name: (len(data), sha(data)) for name, data in generated.items()})
    if len(expected) != len(entries) + len(generated):
        raise PackageError("Generated metadata would collide with a work filename.")
    try:
        with zipfile.ZipFile(temporary, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
            for name in sorted(expected):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                mode = 0o755 if name in entries and entries[name]["path"].stat().st_mode & 0o111 else 0o644
                info.external_attr = (stat.S_IFREG | mode) << 16
                if name in generated:
                    archive.writestr(info, generated[name])
                    continue
                item = entries[name]
                hashed, count = hashlib.sha256(), 0
                with item["path"].open("rb") as source, archive.open(info, "w") as target:
                    for block in iter(lambda: source.read(1024 * 1024), b""):
                        target.write(block)
                        hashed.update(block)
                        count += len(block)
                if (count, hashed.hexdigest()) != expected[name]:
                    raise PackageError("Archived work bytes changed after validation: " + name)
        size = temporary.stat().st_size
        if size >= limit:
            raise PackageError("Compressed archive reaches the strict 500 MB cap; no archive published. Multipart packaging would require separate preparation.")
        with zipfile.ZipFile(temporary) as archive:
            names = archive.namelist()
            if len(names) != len(set(names)) or set(names) != set(expected) or archive.testzip() is not None:
                raise PackageError("ZIP member inventory or CRC integrity check failed.")
            manifest = csv.DictReader(io.StringIO(archive.read("FINAL_FILE_LIST.tsv").decode("utf-8")), delimiter="\t")
            manifest_rows = list(manifest)
            included = [row for row in manifest_rows if row.get("status") == "included"]
            if manifest.fieldnames != ["path", "status", "bytes", "sha256", "reason"] or len(included) != len(expected) or {row.get("path") for row in included} != set(expected):
                raise PackageError("The final manifest does not list every archive member exactly once.")
            for row in included:
                name = row["path"]
                if name == "FINAL_FILE_LIST.tsv":
                    if row["bytes"] or row["sha256"]:
                        raise PackageError("The manifest self-hash omission is inconsistent.")
                elif (row["bytes"], row["sha256"]) != (str(expected[name][0]), expected[name][1]):
                    raise PackageError("The final manifest has an inconsistent member hash or size: " + name)
            for name, (expected_size, expected_sha) in expected.items():
                hashed, count = hashlib.sha256(), 0
                with archive.open(name) as stream:
                    for block in iter(lambda: stream.read(1024 * 1024), b""):
                        hashed.update(block)
                        count += len(block)
                if (count, hashed.hexdigest()) != (expected_size, expected_sha):
                    raise PackageError("ZIP member hash verification failed: " + name)
        ensure_snapshot(work, entries, allow_images)
        archive_sha = hash_file(temporary)[1]
        if not dry_run:
            output.parent.mkdir(parents=True, exist_ok=True)
            # The candidate and output may be on different filesystems. First
            # copy to a unique temporary file beside the destination, then use
            # an exclusive hard link for atomic no-overwrite publication.
            descriptor, local_name = tempfile.mkstemp(prefix="fga-final-", suffix=".tmp", dir=output.parent)
            os.close(descriptor)
            local = Path(local_name)
            try:
                shutil.copyfile(temporary, local)
                if hash_file(local)[1] != archive_sha:
                    raise PackageError("Publication copy checksum differs from the verified ZIP.")
                ensure_snapshot(work, entries, allow_images)
                try:
                    os.link(local, output)
                except FileExistsError:
                    raise PackageError("Refusing to overwrite an archive created during publication: " + output.name)
            finally:
                try:
                    local.unlink(missing_ok=True)
                except OSError:
                    pass
        return {"archive_bytes": size, "archive_sha256": archive_sha, "manifest_sha256": sha(generated["FINAL_FILE_LIST.tsv"]),
                "archive_members": len(expected), "integrity": "CRC and all member hashes verified",
                "published": not dry_run}
    finally:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass


def selftest():
    with tempfile.TemporaryDirectory(prefix="fga-final-selftest-") as directory:
        root = Path(directory)
        work, reports, run = root / "work", root / "gate", root / "run"
        reports.mkdir(); run.mkdir()
        for name in ["CORRECTIONS.tsv", "CHECK_RECORD.md", "CHECK_EVENTS.tsv", "PDF_CHECK.md", "NOTES.md", "README.md", "progress.log", "scripts/validate_fga.py"]:
            path = work / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(b"synthetic fixture\n")
        for layer, config in LAYERS.items():
            path = work / "sources" / layer / config[0]; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(b"synthetic source bytes\n")
            path = work / "pdf" / ("FGA_" + layer + ".pdf"); path.parent.mkdir(exist_ok=True); path.write_bytes(b"synthetic PDF presence fixture\n")
        for name in ["runtime/cache.bin", "renders/page.png", "checkpoints/old.zip", "other.zip"]:
            path = work / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(b"excluded fixture\n")
        checkpoint = root / "checkpoints" / "previous.zip"; checkpoint.parent.mkdir(); checkpoint.write_bytes(b"preserve previous checkpoint")
        checkpoint_sha = hash_file(checkpoint)[1]
        assert not required_presence(work)
        entries, excluded = snapshot(work, set())
        assert len(excluded) == 4 and not any(name.endswith(".zip") for name in entries)
        summary = {field: 0 for field in GAP_FIELDS}
        summary.update(mode="structural enforcement", completion_certified=False, scan_unit_page_occurrences=1,
                       expected_translation_layer_units=137, protected_files_compared=1, protected_files_identical=1)
        files = [{"path": name, "bytes": item["bytes"], "sha256": item["sha256"]} for name, item in entries.items()]
        pdfs = [{"layer": layer, "file": "pdf/FGA_" + layer + ".pdf", "status": "present with pages", "pages": 1,
                 "sha256": entries["pdf/FGA_" + layer + ".pdf"]["sha256"], "inspection": "synthetic gate fixture only"} for layer in LAYERS]
        sources = [dict(row, baseline_member="fixture", status="identical to baseline", baseline_sha256=row["sha256"]) for row in files if row["path"].startswith("sources/")]
        for name, rows in [("FILE_INVENTORY.tsv", files), ("PDF_INVENTORY.tsv", pdfs), ("SOURCE_INVENTORY.tsv", sources)]:
            (reports / name).write_bytes(table_bytes(SCHEMAS[name], rows))
        pages = [{"unit": "149", "printed_page": 169, "volume": 1, "scan": "synthetic.pdf", "scan_pdf_page": 2,
                  "heading_count": 1, "progress_completion_count": 1, "corrected_locator_present": True,
                  "printed_locator_present": True, "interpretation": "synthetic metadata"}]
        translations = [{"layer": layer, "unit": unit, "own_heading_count": 1, "combined_parent_heading_count": 0,
                         "source_locator_present": True, "own_completion_count": 1, "parent_completion_count": 0,
                         "interpretation": "synthetic metadata"} for layer in LAYERS if layer not in {"fr", "fr_printed"}
                        for unit in (["149"] if layer == "es_149_printed" else UNITS)]
        for name, rows in [("PAGE_COVERAGE.tsv", pages), ("TRANSLATION_COVERAGE.tsv", translations)]:
            (reports / name).write_bytes(table_bytes(SCHEMAS[name], rows))
        require_gate(summary, reports, entries, set())
        generated = generated_files(summary, reports, entries, excluded, pdfs)
        output = root / "final" / ARCHIVE
        assert not make_archive(work, output, run, entries, generated, set(), dry_run=True)["published"] and not output.exists()
        try:
            make_archive(work, output, run, entries, generated, set(), limit=1)
            raise AssertionError("oversize fixture was published")
        except PackageError:
            assert not output.exists()
        bad = dict(summary, mode="readiness inventory")
        try:
            require_gate(bad, reports, entries, set()); raise AssertionError("non-enforcing gate accepted")
        except PackageError:
            pass
        (reports / "PDF_INVENTORY.tsv").write_bytes(table_bytes(SCHEMAS["PDF_INVENTORY.tsv"], pdfs[:-1]))
        try:
            require_gate(summary, reports, entries, set()); raise AssertionError("missing layer PDF accepted")
        except PackageError:
            pass
        (reports / "PDF_INVENTORY.tsv").write_bytes(table_bytes(SCHEMAS["PDF_INVENTORY.tsv"], pdfs))
        result = make_archive(work, output, run, entries, generated, set())
        assert result["published"] and hash_file(checkpoint)[1] == checkpoint_sha
        original = output.read_bytes()
        try:
            make_archive(work, output, run, entries, generated, set()); raise AssertionError("existing archive overwritten")
        except PackageError:
            assert output.read_bytes() == original
        (work / "README.md").write_bytes(b"changed synthetic fixture\n")
        try:
            ensure_snapshot(work, entries, set()); raise AssertionError("changed work accepted")
        except PackageError:
            pass
    print("PASS: synthetic gate/schema consumption, eleven PDF requirement, exclusions, complete manifest/member hashes, CRC integrity, dry run, strict size rejection, no-overwrite publication, changed-work rejection, and checkpoint preservation. No real validator, edition, or final package was used.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, default=WORK)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--private-dir", type=Path, help="Parent for retained private gate reports and raw logs")
    for name in ["sources-zip", "scans-zip", "context-zip", "pdf-map"]:
        parser.add_argument("--" + name, type=Path)
    parser.add_argument("--allow-image", action="append", default=[])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        selftest(); return
    args.work = args.work.resolve()
    output_dir = args.output_dir.resolve() if args.output_dir else args.work.parent / "final"
    private = args.private_dir.resolve() if args.private_dir else args.work.parent / "runtime" / "final_packaging"
    for path in (output_dir, private):
        if path == args.work or args.work in path.parents:
            parser.error("Keep archive output and private reports outside the work tree.")
    output = output_dir / ARCHIVE
    if output.exists() or output.is_symlink():
        raise PackageError("Refusing to overwrite existing archive: " + ARCHIVE)
    for name in args.allow_image:
        safe_relative(name)
    faults = required_presence(args.work)
    if faults:
        raise PackageError("Required deliverables are absent:\n" + "\n".join(faults))
    private.mkdir(parents=True, exist_ok=True)
    run_dir = Path(tempfile.mkdtemp(prefix=datetime.now(timezone.utc).strftime("run_%Y%m%dT%H%M%SZ_"), dir=private))
    report_location = Path(os.path.relpath(run_dir, Path.cwd())).as_posix()
    try:
        entries, excluded = snapshot(args.work, set(args.allow_image))
        summary, reports = run_validator(args, run_dir)
        pdfs = require_gate(summary, reports, entries, set(args.allow_image))
        generated = generated_files(summary, reports, entries, excluded, pdfs)
        result = make_archive(args.work, output, run_dir, entries, generated, set(args.allow_image), args.dry_run)
        result.update(archive=ARCHIVE, mode="dry run" if args.dry_run else "published",
                      work_files=len(entries), excluded_files=len(excluded), layer_pdfs=len(pdfs),
                      unchanged_deliverables_omitted=0, archive_limit_bytes=LIMIT,
                      private_reports=report_location, content_review_certified=False)
        try:
            (run_dir / "packaging-summary.json").write_text(json.dumps(result, indent=2) + "\n")
        except OSError:
            result["private_summary_saved"] = False
        print(json.dumps(result, indent=2))
    except (PackageError, OSError, UnicodeError, csv.Error, ValueError, zipfile.BadZipFile) as error:
        reason = str(error) if isinstance(error, PackageError) else "A filesystem, ZIP, or report-parsing operation failed; inspect the private run reports."
        failure = {"status": "blocked", "archive_published": False, "reason": reason, "private_reports": report_location}
        try:
            (run_dir / "packaging-failure.json").write_text(json.dumps(failure, indent=2) + "\n")
        except OSError:
            failure["private_summary_saved"] = False
        print(json.dumps(failure, indent=2))
        raise SystemExit(2)


if __name__ == "__main__":
    try:
        main()
    except PackageError as error:
        print(json.dumps({"status": "blocked", "archive_published": False, "reason": str(error)}, indent=2))
        raise SystemExit(2)
    except (OSError, UnicodeError, csv.Error, ValueError):
        print(json.dumps({"status": "blocked", "archive_published": False,
                          "reason": "A filesystem or report-parsing operation failed; inspect private reports if a run directory was created."}, indent=2))
        raise SystemExit(2)
