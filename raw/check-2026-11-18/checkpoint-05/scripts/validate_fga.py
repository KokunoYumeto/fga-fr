#!/usr/bin/env python3
"""Read-only structural readiness inventory for the eventual FGA final audit.

This script does not interpret mathematical content, compare translations, or
certify page reading, proof checking, or visual review. It writes only its own
reports. The default readiness mode deliberately makes no completion claim.
"""

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile

from pypdf import PdfReader
from build_fga import BASE, LAYERS
from checkpoint_zip import exclude_reason
from privacy_scan import scan_bytes


CORRECTION_COLUMNS = ["file", "layer", "printed_page", "line", "statement",
                      "old", "new", "evidence", "kind", "confidence"]
EVENT_COLUMNS = ["id", "date_utc", "who", "how", "result", "where"]
KINDS = {"reading", "misprint of the original", "translation", "typesetting", "structure"}
CONFIDENCES = {"high", "medium", "low"}
EVENT_TYPES = {
    "targeted proof check", "independent re-proof", "computation or formal certificate",
    "used and rechecked in this run", "carried as background without fault found",
    "refuted, with the refined statement's id",
}
UNITS = ["149", "e149", "182", "e182", "190", "e190", "195", "e195",
         "212", "e212", "221", "e221", "232", "e232", "236", "e236", "com"]
UNIT_PATTERN = r"(?:e?(?:149|182|190|195|212|221|232|236)|com)"
PAGE_ID = re.compile(r"\b(" + UNIT_PATTERN + r")\s*[-:]\s*(\d{1,3})\b", re.I)
UNIT_ID = re.compile(r"(?<![\w])(" + UNIT_PATTERN + r")(?![\w])", re.I)
PAGE_DONE = re.compile(r"^page\s+(" + UNIT_PATTERN + r")[-:](\d+)\s+done\s+(.+)$", re.I)
LANG_DONE = re.compile(r"^(.+?)\s+(" + UNIT_PATTERN + r")\s+done\s+(.+)$", re.I)
HEAD = re.compile(rb"^(#{1,6})[ \t]+(.*)$")
EMAIL = re.compile(rb"(?<![\w.+-])[\w.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![\w])")
LOCAL = re.compile(rb"(?<![\w:])/(?:workspace|home|Users|tmp|private|mnt|root|opt|usr|etc|data|media|Volumes|run|srv|var)/")
DRIVE = re.compile(
    rb"(?<![A-Za-z\\])[A-Za-z]:[\\/](?:Users|Documents and Settings|workspace|home|tmp|Temp|projects|repos|work|Desktop)[\\/]",
    re.I)
TEXT_EXTENSIONS = {".tex", ".md", ".tsv", ".csv", ".json", ".jsonl", ".py", ".lua",
                   ".ps1", ".cff", ".txt", ".log", ".sh", ".yaml", ".yml", ".toml"}
PROTECTED_TOKENS = ("readme", "rights", "notice", "attribution", "sources", "fuentes",
                    "citation", "purpose", "credits", "copyright")
ALIASES = {
    "fr_printed": ["fr_printed", "French as printed"],
    "fr": ["French corrected", "French", "fr"],
    "en": ["English", "en"],
    "es_149_printed": ["es_149_printed", "Spanish 149 as printed", "Spanish as printed"],
    "es": ["Spanish", "es"],
    "pt-BR_printed": ["pt-BR_printed", "Portuguese as printed", "Brazilian Portuguese as printed"],
    "pt-BR": ["Brazilian Portuguese", "Portuguese", "pt-BR"],
    "vi_diplomatic": ["vi_diplomatic", "Vietnamese diplomatic", "Vietnamese as printed"],
    "vi": ["Vietnamese", "vi"],
    "ko": ["Korean", "ko"],
    "zh-Hans": ["Simplified Chinese", "Chinese", "zh-Hans", "zh-Hans-CN"],
}
PARENTS = {"es_149_printed": "es", "pt-BR_printed": "pt-BR", "vi_diplomatic": "vi"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def table(path, columns, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def layer_hint(text):
    # More specific names win over their parent-language words.
    options = [(alias, layer) for layer, values in ALIASES.items() for alias in values]
    for alias, layer in sorted(options, key=lambda item: len(item[0]), reverse=True):
        if re.search(r"(?<![\w])" + re.escape(alias) + r"(?![\w])", text, re.I):
            return layer
    return None


def valid_utc(value):
    value = value.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        try:
            datetime.fromisoformat(value)
            return True
        except ValueError:
            return False
    try:
        value = value.replace(" UTC", "+00:00").replace("Z", "+00:00")
        date = datetime.fromisoformat(value)
        return date.tzinfo is not None and date.utcoffset().total_seconds() == 0
    except (ValueError, AttributeError):
        return False


def read_records(path, expected, issues):
    if not path.exists():
        issues.append({"file": path.name, "data_row": "", "field": "", "issue": "required file missing"})
        return []
    try:
        with path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream, delimiter="\t")
            rows = list(reader)
            columns = reader.fieldnames
    except (UnicodeDecodeError, csv.Error):
        issues.append({"file": path.name, "data_row": "", "field": "", "issue": "TSV decoding/parsing failed"})
        return []
    if columns != expected:
        issues.append({"file": path.name, "data_row": "", "field": "header",
                       "issue": "column names or order differ from the exact required schema"})
    for number, row in enumerate(rows, 1):
        if None in row or any(row.get(column) is None for column in expected):
            issues.append({"file": path.name, "data_row": number, "field": "",
                           "issue": "record has missing or excess fields"})
    return rows


def schemas(work):
    issues = []
    corrections = read_records(work / "CORRECTIONS.tsv", CORRECTION_COLUMNS, issues)
    events = read_records(work / "CHECK_EVENTS.tsv", EVENT_COLUMNS, issues)
    for number, row in enumerate(corrections, 1):
        for field, allowed in [("kind", KINDS), ("confidence", CONFIDENCES)]:
            if row.get(field) not in allowed:
                issues.append({"file": "CORRECTIONS.tsv", "data_row": number, "field": field,
                               "issue": "value is not an exact allowed final-schema value"})
        for field in ["file", "layer", "evidence"]:
            if not (row.get(field) or "").strip():
                issues.append({"file": "CORRECTIONS.tsv", "data_row": number, "field": field,
                               "issue": "required value is empty"})
        value = row.get("file") or ""
        file_path = Path(value)
        if file_path.is_absolute() or ".." in file_path.parts:
            issues.append({"file": "CORRECTIONS.tsv", "data_row": number, "field": "file",
                           "issue": "file locator is not a safe source-relative path"})
        elif value and not any(path.is_file() for path in [work / value, work / "sources" / value]):
            issues.append({"file": "CORRECTIONS.tsv", "data_row": number, "field": "file",
                           "issue": "file locator does not resolve within current deliverables"})
    for number, row in enumerate(events, 1):
        if row.get("how") not in EVENT_TYPES:
            issues.append({"file": "CHECK_EVENTS.tsv", "data_row": number, "field": "how",
                           "issue": "event type is not an exact allowed type"})
        if not valid_utc(row.get("date_utc") or ""):
            issues.append({"file": "CHECK_EVENTS.tsv", "data_row": number, "field": "date_utc",
                           "issue": "not a valid UTC date or explicitly UTC timestamp"})
        for field in ["id", "who", "result", "where"]:
            if not (row.get(field) or "").strip():
                issues.append({"file": "CHECK_EVENTS.tsv", "data_row": number, "field": field,
                               "issue": "required value is empty"})
    return corrections, events, issues


def archive_inventory(path, kind):
    rows, baseline, expected_pages = [], {}, []
    if not path.exists():
        return [{"archive": path.name, "member": "", "check": "archive availability", "result": "missing"}], baseline, expected_pages
    try:
        archive = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile):
        return [{"archive": path.name, "member": "", "check": "archive availability", "result": "unreadable ZIP"}], baseline, expected_pages
    with archive:
        try:
            manifest = archive.read("MANIFEST.tsv").decode("utf-8-sig")
        except (KeyError, UnicodeDecodeError, OSError, zipfile.BadZipFile):
            return [{"archive": path.name, "member": "MANIFEST.tsv", "check": "manifest availability", "result": "missing or unreadable"}], baseline, expected_pages
        reader = csv.DictReader(
            io.StringIO("\n".join(line for line in manifest.splitlines() if not line.startswith("#"))),
            delimiter="\t")
        try:
            records = list(reader)
        except csv.Error:
            return [{"archive": path.name, "member": "MANIFEST.tsv", "check": "manifest schema", "result": "unreadable TSV"}], baseline, expected_pages
        if reader.fieldnames != ["path_in_zip", "source", "bytes", "sha256", "role"]:
            rows.append({"archive": path.name, "member": "MANIFEST.tsv", "check": "manifest schema", "result": "unexpected columns"})
        for name, count in Counter(archive.namelist()).items():
            if count > 1:
                rows.append({"archive": path.name, "member": name, "check": "member inventory", "result": "duplicate ZIP member"})
        listed = set()
        for record in records:
            name = record.get("path_in_zip", "")
            if not name or None in record:
                rows.append({"archive": path.name, "member": name or "", "check": "manifest schema", "result": "missing or excess fields"})
                continue
            if name in listed:
                rows.append({"archive": path.name, "member": name, "check": "manifest inventory", "result": "duplicate manifest member"})
            listed.add(name)
            try:
                data = archive.read(name)
                ok = len(data) == int(record["bytes"]) and sha(data) == record["sha256"].lower()
                rows.append({"archive": path.name, "member": name, "check": "manifest bytes and SHA-256",
                             "result": "match" if ok else "mismatch"})
                if kind == "sources":
                    baseline[name] = data
                elif kind == "scans":
                    match = re.match(r"FGA_(" + UNIT_PATTERN + r")_SB_.*__(\d+)__(\d+)_\d+\.pdf$", name)
                    if match:
                        # Only the PDF page tree is examined; no page text or image is extracted.
                        count = len(PdfReader(io.BytesIO(data)).pages)
                        for offset in range(max(0, count - 1)):
                            expected_pages.append({"unit": match[1], "printed_page": int(match[3]) + offset,
                                                   "volume": int(match[2]), "scan": name,
                                                   "scan_pdf_page": offset + 2})
            except Exception:
                rows.append({"archive": path.name, "member": name, "check": "manifest member", "result": "unreadable"})
        actual = {name for name in archive.namelist() if not name.endswith("/") and name != "MANIFEST.tsv"}
        for name in sorted(actual - listed):
            rows.append({"archive": path.name, "member": name, "check": "member inventory", "result": "not listed in manifest"})
        for name in sorted(listed - actual):
            rows.append({"archive": path.name, "member": name, "check": "member inventory", "result": "listed member missing"})
    return rows, baseline, expected_pages


def protected_file(name):
    basename = Path(name).name.lower()
    return basename == "front-ko.tex" or any(token in basename for token in PROTECTED_TOKENS)


def front_matter(data):
    start = data.find(b"\\begin{document}")
    end = data.find(b"\\mainmatter", start + 1)
    return data[start:end] if start >= 0 and end >= start else None


def source_inventory(work, baseline):
    files, protected, front = [], [], []
    expected = dict(baseline)
    for name, data in baseline.items():
        if name.startswith("fr/"):
            expected["fr_printed/" + name[len("fr/"):]] = data
    for name, original in sorted(expected.items()):
        path = work / "sources" / name
        current = path.read_bytes() if path.is_file() else None
        origin = "fr/" + name[len("fr_printed/"):] if name.startswith("fr_printed/") else name
        status = "missing" if current is None else "identical to baseline" if current == original else "changed working file"
        files.append({"path": "sources/" + name, "baseline_member": origin, "status": status,
                      "bytes": len(current) if current is not None else "",
                      "sha256": sha(current) if current is not None else "", "baseline_sha256": sha(original)})
        if protected_file(name):
            protected.append({"path": "sources/" + name, "baseline_member": origin,
                              "comparison": "missing" if current is None else
                              "byte-for-byte identical" if current == original else "bytes differ; review credit/rights preservation"})
        if Path(name).name == "main.tex" or Path(name).name.startswith("FGA_") and name.endswith(".tex"):
            old_block = front_matter(original)
            new_block = front_matter(current) if current is not None else None
            front.append({"path": "sources/" + name,
                          "comparison": "not located: document/mainmatter delimiters absent" if old_block is None else
                          "current block missing" if new_block is None else
                          "front-matter block byte-for-byte identical" if new_block == old_block else
                          "front-matter block differs; credit-specific review required"})
    known = set(expected)
    for path in sorted((work / "sources").rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            name = path.relative_to(work / "sources").as_posix()
            if name not in known:
                data = path.read_bytes()
                files.append({"path": "sources/" + name, "baseline_member": "",
                              "status": "additional current file", "bytes": len(data),
                              "sha256": sha(data), "baseline_sha256": ""})
    return files, protected, front


def record_sections(path):
    if not path.exists():
        return []
    lines = path.read_bytes().splitlines()
    heads = []
    fence = None
    for number, line in enumerate(lines):
        marker = re.match(rb"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if marker and marker[1][:1] == fence[0] and len(marker[1]) >= fence[1] and not marker[2].strip():
                fence = None
            continue
        if marker and (marker[1][:1] != b"`" or b"`" not in marker[2]):
            fence = (marker[1][:1], len(marker[1]))
            continue
        match = HEAD.match(line)
        if match:
            # Decode headings only; section bodies are searched only for literal file locators.
            heads.append((number, len(match[1]), match[2].decode("utf-8", errors="replace")))
    sections = []
    for index, (start, level, heading) in enumerate(heads):
        end = next((number for number, next_level, _ in heads[index + 1:] if next_level <= level), len(lines))
        sections.append({"heading": heading, "line": start + 1, "level": level,
                         "body": b"\n".join(lines[start + 1:end])})
    return sections


def structural_records(work):
    page_heads, translation_heads = {}, {}
    for section in record_sections(work / "CHECK_RECORD.md"):
        hint = layer_hint(section["heading"])
        page = PAGE_ID.search(section["heading"])
        if page and hint in (None, "fr", "fr_printed"):
            page_heads.setdefault((page[1].lower(), int(page[2])), []).append(section)
        elif hint and hint not in ("fr", "fr_printed"):
            unit = UNIT_ID.search(section["heading"])
            if unit:
                translation_heads.setdefault((hint, unit[1].lower()), []).append(section)
    page_done, language_done = Counter(), Counter()
    time_issues = []
    path = work / "progress.log"
    lines = path.read_text().splitlines() if path.exists() else []
    if not lines or not valid_utc(lines[0]):
        time_issues.append({"record": "progress.log", "key": "first line", "count": "", "issue": "missing or invalid initial UTC timestamp"})
    for number, line in enumerate(lines, 1):
        match = PAGE_DONE.match(line)
        if match:
            page_done[(match[1].lower(), int(match[2]))] += 1
            if not valid_utc(match[3]):
                time_issues.append({"record": "progress.log", "key": "line " + str(number), "count": "", "issue": "page completion timestamp is not recognized as UTC"})
        else:
            match = LANG_DONE.match(line)
            if match:
                language = layer_hint(match[1])
                if language:
                    language_done[(language, match[2].lower())] += 1
                    if not valid_utc(match[3]):
                        time_issues.append({"record": "progress.log", "key": "line " + str(number), "count": "", "issue": "language completion timestamp is not recognized as UTC"})
    duplicates = list(time_issues)
    for label, records in [("page heading", page_heads), ("translation heading", translation_heads),
                           ("page completion", page_done), ("language completion", language_done)]:
        for key, value in records.items():
            count = len(value) if isinstance(value, list) else value
            if count > 1:
                duplicates.append({"record": label, "key": "-".join(map(str, key)),
                                   "count": count, "issue": "duplicate structural marker; review rather than infer intent"})
    return page_heads, translation_heads, page_done, language_done, duplicates


def source_path(layer, unit):
    if layer in ("fr", "fr_printed"):
        return layer + "/fr/" + unit + ".tex"
    if layer == "en":
        return "en/en/" + unit + ".tex"
    if layer == "es":
        return "es/es/" + unit + ".tex"
    if layer == "es_149_printed":
        return "es_149_printed/es/149_diplomatic.tex"
    if layer == "pt-BR":
        return "pt-BR/pt_BR/current/" + unit + ".tex"
    if layer == "pt-BR_printed":
        return "pt-BR_printed/pt_BR/diplomatic/" + unit + ".tex"
    if layer == "vi":
        return "vi/sources/current/" + unit + ".tex"
    if layer == "vi_diplomatic":
        return "vi_diplomatic/sources/diplomatic/" + unit + ".tex"
    if layer == "ko":
        return "ko/" + unit + ".tex"
    return "zh-Hans/source/zh/" + unit + ".tex"


def has_source_locator(body, layer, unit):
    locator = re.escape(source_path(layer, unit))
    return bool(re.search(r"(?<![\w.+~@%-])" + locator + r"(?![\w./\\+~@%-])",
                          body.decode("utf-8", errors="replace")))


def coverage(work, expected_pages):
    page_heads, trans_heads, page_done, lang_done, duplicates = structural_records(work)
    pages = []
    expected_keys = {(row["unit"], row["printed_page"]) for row in expected_pages}
    for record in expected_pages:
        key = (record["unit"], record["printed_page"])
        sections = page_heads.get(key, [])
        pages.append(dict(record, heading_count=len(sections), progress_completion_count=page_done[key],
                          corrected_locator_present=any(has_source_locator(row["body"], "fr", key[0]) for row in sections),
                          printed_locator_present=any(has_source_locator(row["body"], "fr_printed", key[0]) for row in sections),
                          interpretation="structural marker inventory only; reading not certified"))
    for key in sorted((set(page_heads) | set(page_done)) - expected_keys):
        duplicates.append({"record": "page marker", "key": "-".join(map(str, key)), "count": "",
                           "issue": "page identifier not found in scan metadata inventory"})
    translations = []
    for layer in LAYERS:
        if layer in ("fr", "fr_printed"):
            continue
        units = ["149"] if layer == "es_149_printed" else UNITS
        for unit in units:
            own = trans_heads.get((layer, unit), [])
            parent = PARENTS.get(layer)
            combined = trans_heads.get((parent, unit), []) if parent else []
            sections = own + combined
            translations.append({"layer": layer, "unit": unit, "own_heading_count": len(own),
                                 "combined_parent_heading_count": len(combined),
                                 "source_locator_present": any(has_source_locator(row["body"], layer, unit) for row in sections),
                                 "own_completion_count": lang_done[(layer, unit)],
                                 "parent_completion_count": lang_done[(parent, unit)] if parent else "",
                                 "interpretation": "structural marker inventory only; translation check not certified"})
    return pages, translations, duplicates


def source_markers(work):
    rows = []
    for layer in LAYERS:
        for unit in (["149"] if layer == "es_149_printed" else UNITS):
            relative = source_path(layer, unit)
            path = work / "sources" / relative
            data = path.read_bytes() if path.exists() else b""
            markers = re.findall(rb"\\src\s*\{(\d+)\}", data)
            numbers = [int(value) for value in markers]
            repeated = sorted(value for value, count in Counter(numbers).items() if count > 1)
            rows.append({"file": "sources/" + relative, "present": path.exists(),
                         "marker_count": len(numbers), "printed_page_markers": ",".join(map(str, numbers)),
                         "repeated_markers": ",".join(map(str, repeated)),
                         "interpretation": "lexical source markers only; correctness not decided"})
    return rows


def presence(work, pdf_map):
    rows = []
    for name in ["sources", "pdf", "scripts", "CORRECTIONS.tsv", "CHECK_RECORD.md", "CHECK_EVENTS.tsv",
                 "PDF_CHECK.md", "NOTES.md", "README.md", "progress.log"]:
        rows.append({"item": name, "kind": "required deliverable", "status": "present" if (work / name).exists() else "missing"})
    pdfs = []
    for layer, (entry, _, _, _) in LAYERS.items():
        relative = "sources/" + layer + "/" + entry
        rows.append({"item": relative, "kind": "layer entry point",
                     "status": "present" if (work / relative).is_file() else "missing"})
        name = pdf_map.get(layer, "pdf/FGA_" + layer + ".pdf")
        path = work / name
        record = {"layer": layer, "file": name, "status": "missing", "pages": "", "sha256": "",
                  "inspection": "page-tree metadata only; visual inspection not performed"}
        if path.is_file():
            record["sha256"] = sha(path.read_bytes())
            try:
                reader = PdfReader(path)
                record["pages"] = len(reader.pages)
                record["status"] = "present with pages" if record["pages"] else "zero-page PDF"
            except Exception:
                record["status"] = "unreadable PDF"
        pdfs.append(record)
    return rows, pdfs


def deliverable_inventory(work, output, allow_images):
    files, privacy, binary = [], [], []
    for path in sorted(work.rglob("*")):
        if not path.is_file() or path.is_symlink() or output == path or output in path.parents:
            continue
        relative = path.relative_to(work)
        if exclude_reason(relative, allow_images):
            continue
        data = path.read_bytes()
        files.append({"path": relative.as_posix(), "bytes": len(data), "sha256": sha(data)})
        findings, scope = scan_bytes(relative.as_posix(), data)
        privacy.extend(findings)
        binary.append({"file": relative.as_posix(), "scope": scope})
    return files, privacy, binary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, default=BASE)
    parser.add_argument("--sources-zip", type=Path)
    parser.add_argument("--scans-zip", type=Path)
    parser.add_argument("--context-zip", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--pdf-map", type=Path, help="Optional TSV with layer and file columns; paths relative to work")
    parser.add_argument("--allow-image", action="append", default=[])
    parser.add_argument("--enforce-structure", action="store_true",
                        help="Return nonzero for structural gaps; never certifies mathematical or visual completion")
    args = parser.parse_args()
    work = args.work.resolve()
    output = args.output.resolve() if args.output else work / "validation"
    output.mkdir(parents=True, exist_ok=True)
    archives = {
        "sources": args.sources_zip or work.parent / "upload" / "FGA_sources.zip",
        "scans": args.scans_zip or work.parent / "upload" / "FGA_scans.zip",
        "context": args.context_zip or work.parent / "upload" / "FGA_context.zip",
    }
    manifest_rows, baseline, expected_pages = [], {}, []
    for kind, path in archives.items():
        rows, original, pages = archive_inventory(path, kind)
        manifest_rows.extend(rows)
        if kind == "sources":
            baseline = original
        if kind == "scans":
            expected_pages = pages
    corrections, events, schema_issues = schemas(work)
    source_files, protected, front = source_inventory(work, baseline)
    pages, translations, duplicates = coverage(work, expected_pages)
    pdf_map = {}
    if args.pdf_map:
        with args.pdf_map.open(newline="", encoding="utf-8-sig") as stream:
            for row in csv.DictReader(stream, delimiter="\t"):
                relative = Path(row["file"])
                if relative.is_absolute() or ".." in relative.parts or row["layer"] not in LAYERS:
                    raise ValueError("PDF map must use known layers and safe relative file paths")
                pdf_map[row["layer"]] = relative.as_posix()
    required, pdfs = presence(work, pdf_map)
    inventory, privacy, binary = deliverable_inventory(work, output, set(args.allow_image))
    tables = [
        ("MANIFEST_CHECKS.tsv", ["archive", "member", "check", "result"], manifest_rows),
        ("SOURCE_INVENTORY.tsv", ["path", "baseline_member", "status", "bytes", "sha256", "baseline_sha256"], source_files),
        ("PROTECTED_FILES.tsv", ["path", "baseline_member", "comparison"], protected),
        ("FRONT_MATTER.tsv", ["path", "comparison"], front),
        ("SCHEMA_ISSUES.tsv", ["file", "data_row", "field", "issue"], schema_issues),
        ("PAGE_COVERAGE.tsv", ["unit", "printed_page", "volume", "scan", "scan_pdf_page", "heading_count",
                               "progress_completion_count", "corrected_locator_present", "printed_locator_present",
                               "interpretation"], pages),
        ("TRANSLATION_COVERAGE.tsv", ["layer", "unit", "own_heading_count", "combined_parent_heading_count",
                                      "source_locator_present", "own_completion_count", "parent_completion_count",
                                      "interpretation"], translations),
        ("RECORD_DUPLICATES.tsv", ["record", "key", "count", "issue"], duplicates),
        ("SOURCE_PAGE_MARKERS.tsv", ["file", "present", "marker_count", "printed_page_markers",
                                      "repeated_markers", "interpretation"], source_markers(work)),
        ("REQUIRED_PRESENCE.tsv", ["item", "kind", "status"], required),
        ("PDF_INVENTORY.tsv", ["layer", "file", "status", "pages", "sha256", "inspection"], pdfs),
        ("FILE_INVENTORY.tsv", ["path", "bytes", "sha256"], inventory),
        ("PRIVACY_FINDINGS.tsv", ["file", "line", "issue", "scope"], privacy),
        ("BINARY_PRIVACY_SCOPE.tsv", ["file", "scope"], binary),
    ]
    for filename, columns, rows in tables:
        table(output / filename, columns, rows)
    missing_pages = sum(not row["heading_count"] or not row["progress_completion_count"] or
                        not row["corrected_locator_present"] or not row["printed_locator_present"] for row in pages)
    missing_translations = sum(not row["source_locator_present"] or
                               not (row["own_completion_count"] or row["parent_completion_count"]) for row in translations)
    summary = {
        "mode": "structural enforcement" if args.enforce_structure else "readiness inventory",
        "date_utc": datetime.now(timezone.utc).isoformat(),
        "correction_rows": len(corrections), "check_event_rows": len(events),
        "schema_issues": len(schema_issues),
        "scan_unit_page_occurrences": len(pages),
        "distinct_volume_printed_pages": len({(row["volume"], row["printed_page"]) for row in pages}),
        "page_occurrences_with_heading": sum(bool(row["heading_count"]) for row in pages),
        "page_occurrences_with_completion_marker": sum(bool(row["progress_completion_count"]) for row in pages),
        "page_occurrences_with_structural_gaps": missing_pages,
        "expected_translation_layer_units": len(translations),
        "translation_layer_units_with_locator": sum(bool(row["source_locator_present"]) for row in translations),
        "translation_layer_units_with_structural_gaps": missing_translations,
        "duplicate_or_invalid_record_markers": len(duplicates),
        "protected_files_compared": len(protected),
        "protected_files_identical": sum(row["comparison"] == "byte-for-byte identical" for row in protected),
        "front_matter_blocks_flagged_for_review": sum("differs" in row["comparison"] or "missing" in row["comparison"] for row in front),
        "missing_required_items": sum(row["status"] == "missing" for row in required),
        "missing_or_invalid_pdfs": sum(row["status"] != "present with pages" for row in pdfs),
        "missing_expected_source_files": sum(row["status"] == "missing" for row in source_files),
        "manifest_discrepancies": sum(row["result"] != "match" for row in manifest_rows),
        "privacy_pattern_findings": len(privacy),
        "completion_certified": False,
    }
    narrative = "# Read-only audit readiness inventory\n\n"
    narrative += "This report inventories structural evidence only. It does not certify that a page was read, a correction was reread, a translation was checked, a proof was verified, or a PDF was visually inspected. Missing markers are reported as unrecognized structural evidence, not as a mathematical judgment.\n\n"
    narrative += "| Measure | Observed value |\n| --- | --- |\n"
    narrative += "".join("| " + key.replace("_", " ") + " | " + str(value) + " |\n" for key, value in summary.items())
    narrative += "\n## Scope and limits\n\n"
    narrative += "Original archive manifests are checked against byte counts and SHA-256 hashes. Working source changes are listed separately and are not called original-manifest mismatches. The new fr_printed tree is compared to the corresponding original fr tree for inventory and protected-file purposes.\n\n"
    narrative += "Protected metadata files are compared byte-for-byte. Front-matter blocks between the document and mainmatter delimiters receive a separate byte comparison; any difference requires credit-specific review. Other inline credit strings are not semantically examined. Refutation events use the allowed event-type label; the refined statement and mathematical outcome are not interpreted here.\n\n"
    narrative += "Confidence values are checked against the final exact values high, medium, and low. Provisional annotations or withdrawal prose in that column therefore appear as final-schema gaps and are never rewritten. Empty mathematical result/evidence fields are tested only for presence; their content is not evaluated.\n\n"
    narrative += "Page coverage uses scan PDF page-tree metadata, excluding each cover sheet. Shared printed pages are distinct unit/page occurrences while the volume/page total counts them once. Source page markers are listed lexically and their correctness is not decided. Translation headings can be separate by layer or combined under a parent language, provided the layer's source locator is present. Headings in an unrecognized format may need manual reconciliation.\n\n"
    narrative += "Privacy checks search every included decodable text file, independent of extension, for email and absolute-path patterns without displaying matches. PDF metadata, XMP, and extractable visible text are searched. Relative paths are allowed. Raster text, attachments, and undecodable binary contents remain outside this mechanical scan. Only explicit portable interpreter shebangs are exempt.\n\n"
    narrative += "FILE_INVENTORY.tsv follows the checkpoint packager's default deliverable scope, with explicitly allowed evidence images added. This validator's own output directory is excluded from that inventory to avoid recursive self-hashing. No source, audit record, note, mathematical decision, or progress entry is modified.\n"
    (output / "READINESS.md").write_text(narrative, encoding="utf-8")
    print(json.dumps(summary, indent=2))
    if args.enforce_structure:
        gates = ["schema_issues", "page_occurrences_with_structural_gaps",
                 "translation_layer_units_with_structural_gaps", "duplicate_or_invalid_record_markers",
                 "front_matter_blocks_flagged_for_review", "missing_required_items", "missing_or_invalid_pdfs",
                 "missing_expected_source_files", "manifest_discrepancies", "privacy_pattern_findings"]
        if not expected_pages or not baseline or any(summary[key] for key in gates) or summary["protected_files_identical"] != summary["protected_files_compared"]:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
