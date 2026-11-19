#!/usr/bin/env python3
"""Read-only correction-ledger selection; no review decision or confidence update.

All ordinary commands write to stdout/stderr only. The selftest command uses
temporary synthetic fixtures, removes them, and never opens the real ledger.
"""

import argparse
from collections import Counter
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import quote


WORK = Path(__file__).resolve().parents[1]
UNIT = r"(?:e?(?:149|182|190|195|212|221|232|236)|com)"
META = ["row_number", "row_id", "occurrence", "identical_rows", "file", "layer",
        "printed_page", "line", "kind", "confidence", "source_unit"]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def parse_ledger(data):
    # CSV parsing, including quoted multiline fields, happens before hashing.
    reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig"), newline=""),
                            delimiter="\t", strict=True)
    columns = reader.fieldnames
    if not columns or len(set(columns)) != len(columns) or any(not c for c in columns):
        raise ValueError("The TSV must have a nonempty, unique column header.")
    rows = []
    occurrences = Counter()
    for number, fields in enumerate(reader, 1):
        if None in fields or any(value is None for value in fields.values()):
            raise ValueError(f"Logical data row {number} has missing or excess fields.")
        canonical = json.dumps(fields, sort_keys=True, ensure_ascii=False,
                               separators=(",", ":")).encode("utf-8")
        row_id = "sha256:" + digest(canonical)
        occurrences[row_id] += 1
        stem = Path(fields.get("file", "").replace("\\", "/")).stem
        unit = re.fullmatch("(" + UNIT + r")(?:_diplomatic)?", stem)
        rows.append({"row_number": number, "row_id": row_id,
                     "occurrence": occurrences[row_id], "fields": fields,
                     "source_unit": unit[1] if unit else ""})
    for row in rows:
        row["identical_rows"] = occurrences[row["row_id"]]
    return columns, rows


def load_ledger(path):
    before = path.stat()
    data = path.read_bytes()
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError("The ledger changed while being read; retry with edits paused.")
    columns, rows = parse_ledger(data)
    return columns, rows, digest(data)


def metadata(row):
    return {key: row[key] if key in row else row["fields"].get(key, "") for key in META}


def select(rows, args, id_rows=None):
    ids = set()
    for value in args.id:
        prefix = value.removeprefix("sha256:").lower()
        if not re.fullmatch(r"[0-9a-f]{12,64}", prefix):
            raise ValueError("Row IDs require a full digest or at least 12 hexadecimal prefix characters.")
        matches = {r["row_id"] for r in (rows if id_rows is None else id_rows)
                   if r["row_id"][7:].startswith(prefix)}
        if len(matches) != 1:
            raise ValueError("A requested row ID is absent or its prefix is ambiguous; refresh the inventory.")
        ids.update(matches)
    return [row for row in rows
            if (not ids or row["row_id"] in ids)
            and (not args.row or row["row_number"] in args.row)
            and (not args.unit or row["source_unit"] == args.unit)
            and all(not wanted or row["fields"].get(field, "") in wanted
                    for field, wanted in [("layer", args.layer), ("printed_page", args.page),
                                          ("kind", args.kind)])]


def asset_links(unit, page, args):
    if not re.fullmatch(UNIT, unit) or not re.fullmatch(r"\d+", page):
        return []
    found = []
    mapping = {}
    if args.page_map.is_file():
        with args.page_map.open(encoding="utf-8-sig", newline="") as stream:
            for row in csv.DictReader(stream, delimiter="\t"):
                if row.get("unit") == unit and row.get("printed_page") == page:
                    name, index = row.get("scan", ""), row.get("scan_pdf_page", "")
                    if name == Path(name).name and index.isdigit():
                        mapping[name] = int(index)

    def add(path, kind, pdf_page="", status="existing filename; contents unopened"):
        relative = Path(os.path.relpath(path, Path.cwd())).as_posix()
        href = ("sandbox:" + path.resolve().as_posix()) if args.link_style == "sandbox" else quote(relative)
        if pdf_page:
            href += "#page=" + str(pdf_page)
        found.append({"kind": kind, "path": relative, "pdf_page": pdf_page,
                      "href": href, "status": status})

    for root in args.scan_root:
        for path in sorted(root.glob("FGA_" + unit + "_SB_*.pdf")):
            if not path.is_file():
                continue
            match = re.fullmatch(r"FGA_" + unit + r"_SB_.*__\d+__(\d+)_\d+\.pdf", path.name)
            if path.name in mapping:
                add(path, "scan", mapping[path.name], "existing file; PDF page from supplied page-map metadata")
            elif match and int(page) >= int(match[1]):
                add(path, "scan candidate", int(page) - int(match[1]) + 2,
                    "page offset from filename and one cover; upper page bound unchecked")
    name = re.compile(re.escape(unit + "-" + page) + r"(?:[._-]|$)")
    for kind, roots in [("render", args.render_root), ("crop", args.crop_root)]:
        for root in roots:
            if root.is_dir():
                for path in sorted(root.rglob("*")):
                    if path.is_file() and name.match(path.name) and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}:
                        add(path, kind)
    # Overlapping search roots should not repeat the same asset link.
    return list({(r["kind"], r["href"]): r for r in found}.values())


def emit(rows, columns, format_name):
    if format_name == "tsv":
        writer = csv.DictWriter(sys.stdout, fieldnames=columns, delimiter="\t",
                                lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    else:
        for row in rows:
            print(json.dumps(row, ensure_ascii=False))


def compare(old, current):
    previous = Counter(row["row_id"] for row in old)
    present = Counter(row["row_id"] for row in current)
    representatives = {row["row_id"]: row for row in old + current}
    result = []
    for row_id in sorted(previous.keys() | present.keys()):
        if previous[row_id] != present[row_id]:
            result.append(dict(metadata(representatives[row_id]),
                               old_count=previous[row_id], current_count=present[row_id],
                               count_change=present[row_id] - previous[row_id]))
    return result


def selftest():
    columns = ["file", "layer", "printed_page", "line", "statement", "old", "new",
               "evidence", "kind", "confidence"]
    base = dict(zip(columns, ["fr/fr/149.tex", "French corrected", "169", "12;14",
                              "synthetic", 'old\nsecond\t"quoted"', "new\naggregate",
                              "synthetic evidence", "structure", "low; provisional"]))
    aggregate = dict(base, printed_page="169-193", old="historical batch", new="later batch")

    def payload(rows, header=columns):
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=header, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
        return stream.getvalue().encode("utf-8")

    _, first = parse_ledger(payload([base, aggregate, base]))
    _, shifted = parse_ledger(payload([aggregate, base, base, dict(base, confidence="high")], list(reversed(columns))))
    assert first[0]["fields"] == base and first[1]["fields"] == aggregate
    assert first[0]["row_id"] == shifted[1]["row_id"] == shifted[2]["row_id"]
    assert first[0]["identical_rows"] == 2 and first[2]["occurrence"] == 2
    assert first[1]["row_id"] == shifted[0]["row_id"]
    assert shifted[3]["row_id"] != first[0]["row_id"]
    assert len(compare(first, shifted)) == 1 and compare(first, shifted)[0]["count_change"] == 1
    query = argparse.Namespace(id=[], row=[], unit="149", layer=["French corrected"], page=["169"], kind=["structure"])
    assert len(select(first, query)) == 2
    query.id = [first[0]["row_id"][:23]]
    assert len(select(first, query)) == 2
    changed_history = shifted[1:]
    query.id, query.page = [aggregate_id := first[1]["row_id"]], []
    assert len(select(first, query, first + changed_history)) == 1
    assert select(changed_history, query, first + changed_history) == []
    assert next(r for r in compare(first, changed_history) if r["row_id"] == aggregate_id)["count_change"] == -1
    with tempfile.TemporaryDirectory(prefix="correction-review-selftest-") as directory:
        root = Path(directory)
        ledger = root / "fixture.tsv"
        ledger.write_bytes(payload([base, aggregate, base]))
        fingerprint = digest(ledger.read_bytes())
        assert load_ledger(ledger)[2] == fingerprint
        (root / "149-169-top.png").write_bytes(b"unopened synthetic placeholder")
        (root / "149-1690-top.png").write_bytes(b"unopened synthetic placeholder")
        (root / "FGA_149_SB_1956-1958__4__169_0.pdf").write_bytes(b"unopened synthetic placeholder")
        page_map = root / "pages.tsv"
        page_map.write_text("unit\tprinted_page\tscan\tscan_pdf_page\n149\t169\tFGA_149_SB_1956-1958__4__169_0.pdf\t2\n")
        options = argparse.Namespace(page_map=page_map, scan_root=[root], render_root=[], crop_root=[root], link_style="relative")
        links = asset_links("149", "169", options)
        assert len(links) == 2 and links[0]["pdf_page"] == 2
        assert asset_links("149", "169-193", options) == []
        assert digest(ledger.read_bytes()) == fingerprint
    print("PASS: multiline fields, exact filters, aggregates, reorder/append stability, duplicate occurrences, changed-value IDs, snapshot comparison, unopened asset links, and unchanged fixture ledger.")


def main():
    csv.field_size_limit(100_000_000)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["inventory", "show", "compare", "links", "selftest"])
    parser.add_argument("--ledger", type=Path, default=WORK / "CORRECTIONS.tsv")
    parser.add_argument("--against", type=Path, help="Older ledger for exact-content comparison")
    parser.add_argument("--expect-ledger-sha256", help="Refuse a ledger whose raw-file digest changed")
    for option in ["layer", "page", "kind", "id"]:
        parser.add_argument("--" + option, action="append", default=[])
    parser.add_argument("--row", type=int, action="append", default=[], help="Current logical row number; not a stable identifier")
    parser.add_argument("--unit", help="Exact source filename unit, such as 149 or e149")
    parser.add_argument("--format", choices=["tsv", "jsonl"], default="jsonl")
    parser.add_argument("--assets", action="store_true", help="Add unopened asset links to show JSONL output")
    parser.add_argument("--all", action="store_true", help="Explicitly allow show with no selectors")
    parser.add_argument("--page-map", type=Path, default=WORK / "validation" / "PAGE_COVERAGE.tsv")
    parser.add_argument("--scan-root", type=Path, action="append")
    parser.add_argument("--render-root", type=Path, action="append")
    parser.add_argument("--crop-root", type=Path, action="append")
    parser.add_argument("--link-style", choices=["relative", "sandbox"], default="relative")
    args = parser.parse_args()
    if args.action == "selftest":
        selftest()
        return
    args.scan_root = args.scan_root or [WORK.parent / "inputs" / "scans"]
    args.render_root = args.render_root or [WORK.parent / "tmp" / "renders"]
    args.crop_root = args.crop_root or [WORK.parent / "tmp" / "crops"]
    if args.action == "links":
        if not args.unit or not args.page or any(not p.isdigit() for p in args.page):
            parser.error("links requires --unit and one or more integer --page values")
        for page in args.page:
            print(json.dumps({"unit": args.unit, "printed_page": page, "assets": asset_links(args.unit, page, args)}, ensure_ascii=False))
        return
    if args.action == "show" and not (args.all or args.id or args.row or args.layer or args.page or args.kind or args.unit):
        parser.error("show requires an explicit selector or --all")
    if args.assets and (args.action != "show" or args.format != "jsonl"):
        parser.error("--assets requires show with JSONL output")
    if args.action == "compare" and (not args.against or args.row):
        parser.error("compare requires --against and uses content IDs or metadata filters, not --row positions")
    columns, rows, ledger_sha = load_ledger(args.ledger)
    if args.expect_ledger_sha256 and ledger_sha != args.expect_ledger_sha256.lower():
        raise ValueError("The ledger fingerprint changed; refresh the inventory before selecting current row numbers.")
    old, old_sha = [], ""
    if args.action == "compare":
        _, old, old_sha = load_ledger(args.against)
    chosen = select(rows, args, old + rows if args.action == "compare" else None)
    snapshot = {"ledger_sha256": ledger_sha, "logical_rows": len(rows), "selected_rows": len(chosen),
                "review_decision": "none; selection is not confirmation"}
    if args.action == "compare":
        snapshot["older_ledger_sha256"] = old_sha
        output = compare(select(old, args, old + rows), chosen)
        emit(output, META + ["old_count", "current_count", "count_change"], args.format)
    elif args.action == "inventory":
        emit([metadata(row) for row in chosen], META, args.format)
    elif args.format == "tsv":
        if {"review_row_id", "review_row_number", "review_occurrence"} & set(columns):
            raise ValueError("The ledger uses reserved display-column names; use JSONL to preserve all fields.")
        emit([dict(row["fields"], review_row_id=row["row_id"], review_row_number=row["row_number"],
                   review_occurrence=row["occurrence"]) for row in chosen],
             ["review_row_id", "review_row_number", "review_occurrence"] + columns, "tsv")
    else:
        for row in chosen:
            output = dict(row)
            if args.assets:
                output["assets"] = asset_links(row["source_unit"], row["fields"].get("printed_page", ""), args)
                output["asset_scope"] = "filename/metadata links only; unresolved or aggregate locators need explicit links lookup"
            print(json.dumps(output, ensure_ascii=False))
    print(json.dumps(snapshot), file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        # Avoid printing raw local paths or ledger payloads from library errors.
        message = str(error) if isinstance(error, ValueError) and not isinstance(error, UnicodeError) else "Input could not be read or parsed; check the named files and TSV encoding."
        print("correction_review: " + message, file=sys.stderr)
        raise SystemExit(2)
