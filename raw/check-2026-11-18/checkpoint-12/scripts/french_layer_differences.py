"""Freeze and inventory exact French-layer differences without adjudicating them.

Run from the workspace with python -B. All source and ledger inputs are read only.
The inventory orientation is fr (old/left) to fr_printed (new/right). Candidate
ledger rows are lexical links, not decisions about validity or completeness.
"""

import argparse
from bisect import bisect_right
import base64
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
import difflib
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
from source_segments import CONTROL, UNITS, markers, mask_comments, tree_hash


LAYERS = ("fr", "fr_printed")
HEADER = ["file", "layer", "printed_page", "line", "statement", "old", "new", "evidence", "kind", "confidence"]
ASCII_SPACE = re.compile(r"[ \t\r\n\f\v]+")
EMAIL = re.compile(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
LOCAL_PATH = re.compile(r"(?<![A-Za-z0-9:])/(?:workspace|home|root|Users|tmp|mnt|opt|private|var)/[^\s<>\"{}]*|\b[A-Za-z]:[\\/][^\s<>\"{}]+")


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def relative(path):
    return Path(os.path.relpath(path, Path.cwd())).as_posix()


def checked_path(path):
    path = path.resolve()
    if not path.is_relative_to(Path.cwd().resolve()):
        raise ValueError("Inputs and outputs must be inside the current workspace")
    return path


def paths_under(work):
    paths = [Path("CORRECTIONS.tsv")]
    for layer in LAYERS:
        root = work / "sources" / layer
        if not root.is_dir():
            raise ValueError("A required French source tree is missing")
        paths.extend(p.relative_to(work) for p in sorted(root.rglob("*")) if p.is_file() and "__pycache__" not in p.parts)
    return paths


def freeze(args):
    work, out = checked_path(args.work), checked_path(args.out)
    if out.exists() or out.is_relative_to(work):
        raise ValueError("Use a new frozen output directory outside the input tree")
    for attempt in range(1, 6):
        started = utc()
        paths = paths_under(work)
        first = {p: (work / p).read_bytes() for p in paths}
        second_paths = paths_under(work)
        second = {p: (work / p).read_bytes() for p in second_paths}
        completed = utc()
        if paths == second_paths and first == second:
            break
    else:
        raise RuntimeError("Inputs changed during five complete snapshot attempts; no snapshot written")
    for path, data in first.items():
        target = out / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    metadata = {
        "snapshot_started_utc": started, "snapshot_completed_utc": completed,
        "attempt": attempt, "frozen_root": relative(out),
        "consistency_check": "Two consecutive complete reads produced identical file sets and bytes; no subsequent live reads are required.",
        "files": [{"path": p.as_posix(), "bytes": len(data), "sha256": sha(data)} for p, data in first.items()],
    }
    (out / "SNAPSHOT.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in metadata.items() if k != "files"}, indent=2))


def category(path, text=True):
    if path in {"fr/" + unit + ".tex" for unit in UNITS}:
        return "content_tex"
    if path.endswith(".tex"):
        return "build_or_front_matter_tex"
    return "support_metadata" if text else "binary_support"


def classify_text(data):
    try:
        return data.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        return base64.b64encode(data).decode("ascii"), "base64"


def lexical_math_mode(prefix):
    """Recognize only literal math delimiters, without expanding or interpreting TeX."""
    data, position, mode = mask_comments(prefix.encode("utf-8")), 0, None
    while position < len(data):
        if data[position] == 92:
            token = CONTROL.match(data, position)
            if token:
                if token[1] in (b"(", b"["):
                    mode = token[1].decode()
                elif token[1] in (b")", b"]"):
                    mode = None
                position = token.end()
                continue
        if data[position] == 36:
            width = 2 if data[position:position + 2] == b"$$" else 1
            delimiter = "$" * width
            mode = None if mode == delimiter else delimiter
            position += width
            continue
        position += 1
    return mode


def mask_private(text, tex_prefix=None):
    findings, lookalikes = [], []
    for kind, pattern in [("email", EMAIL), ("local_absolute_path", LOCAL_PATH)]:
        for match in pattern.finditer(text):
            control = re.fullmatch(r"[A-Za-z]:\\([A-Za-z@]+)", match[0])
            if kind == "local_absolute_path" and tex_prefix is not None and control and lexical_math_mode(tex_prefix + text[:match.start()]):
                lookalikes.append({"character_start": match.start(), "character_end": match.end(), "control_token": "\\" + control[1], "span_sha256": sha(match[0].encode()), "rule": "colon_followed_by_TeX_control_word_inside_literal_math_delimiters"})
                continue
            findings.append((match.start(), match.end(), kind))
    if not findings:
        return text, [], lookalikes
    merged = []
    for start, end, kind in sorted(findings):
        if merged and start < merged[-1][1]:
            previous = merged.pop()
            merged.append((previous[0], max(previous[1], end), previous[2] + "+" + kind))
        else:
            merged.append((start, end, kind))
    safe = text
    for start, end, kind in reversed(merged):
        safe = safe[:start] + "[REDACTED_" + kind.upper() + "]" + safe[end:]
    return safe, [{"character_start": start, "character_end": end, "kind": kind} for start, end, kind in merged], lookalikes


def location(data, sequence, start, end):
    starts = [m["byte_start"] for m in sequence]
    index = bisect_right(starts, start) - 1
    preceding = sequence[index] if index >= 0 else None
    following = sequence[index + 1] if index + 1 < len(sequence) else None
    nearest = min(sequence, key=lambda m: (abs(m["byte_start"] - start), m["byte_start"] > start)) if sequence else None
    anchor = preceding or following
    pages = []
    if preceding:
        pages.append(preceding["page"])
    for item in sequence:
        if start <= item["byte_start"] < end and item["page"] not in pages:
            pages.append(item["page"])
    prefix = preceding is None and (not sequence or start < sequence[0]["byte_start"])
    return {
        "byte_start": start, "byte_end_exclusive": end,
        "line_start": data.count(b"\n", 0, start) + 1,
        "line_end": data.count(b"\n", 0, end - 1) + 1 if end > start else None,
        "preceding_page": preceding["page"] if preceding else "",
        "preceding_marker_byte": preceding["byte_start"] if preceding else None,
        "following_page": following["page"] if following else "",
        "following_marker_byte": following["byte_start"] if following else None,
        "nearest_page": nearest["page"] if nearest else "",
        "nearest_marker_byte": nearest["byte_start"] if nearest else None,
        "anchor_page": anchor["page"] if anchor else "",
        "anchor_rule": "preceding_marker" if preceding else ("following_marker_for_unmarked_prefix" if following else "no_marker"),
        "covered_pages": pages,
        "unmarked_prefix_included": prefix,
        "cross_page": len(pages) > 1 or (prefix and bool(pages)),
    }


def normalized(text):
    return ASCII_SPACE.sub(" ", text).strip(" \t\r\n\f\v")


def ledger_rows(data):
    stream = io.StringIO(data.decode("utf-8"), newline="")
    reader = csv.reader(stream, delimiter="\t")
    header = next(reader)
    if header != HEADER:
        raise ValueError("Unexpected correction-ledger header")
    rows, previous_end = [], reader.line_num
    for number, values in enumerate(reader, 1):
        physical_start, physical_end = previous_end + 1, reader.line_num
        previous_end = physical_end
        if len(values) != len(HEADER):
            raise ValueError("Malformed correction-ledger data row C" + str(number).zfill(6))
        row = dict(zip(HEADER, values))
        row.update({"row_id": "C" + str(number).zfill(6), "data_row": number,
                    "physical_line_start": physical_start, "physical_line_end": physical_end,
                    "row_sha256": sha(json.dumps(values, ensure_ascii=False, separators=(",", ":")).encode("utf-8")),
                    "old_normalized": normalized(row["old"]), "new_normalized": normalized(row["new"])})
        rows.append(row)
    return rows


def matches(row, left, right, left_normalized, right_normalized, page_compatible, minimum):
    old, new = row["old"], row["new"]
    if old == new:
        return []
    found = []
    for orientation, a, b in [("ledger_old_new_equals_fr_to_fr_printed", left, right), ("ledger_old_new_equals_fr_printed_to_fr", right, left)]:
        if old == a and new == b:
            found.append(("exact_full_hunk_pair", orientation, "old,new"))
        elif old and new and old in a and new in b and (old not in b or new not in a):
            found.append(("exact_distinguishing_substring_pair", orientation, "old,new"))
    if found:
        return found
    old_n, new_n = row["old_normalized"], row["new_normalized"]
    if old_n and new_n and old_n != new_n:
        for orientation, a, b in [("ledger_old_new_equals_fr_to_fr_printed", left_normalized, right_normalized), ("ledger_old_new_equals_fr_printed_to_fr", right_normalized, left_normalized)]:
            if old_n in a and new_n in b and (old_n not in b or new_n not in a):
                found.append(("ascii_whitespace_collapsed_distinguishing_pair", orientation, "old,new"))
    if found:
        return found
    if page_compatible:
        sides = []
        for field in ("old", "new"):
            value = row[field]
            if len(value) < minimum:
                continue
            in_left, in_right = value in left, value in right
            if in_left != in_right:
                sides.append(field + (":fr" if in_left else ":fr_printed"))
        if sides:
            return [("one_side_exact_distinguishing_substring", "one_side_only", ",".join(sides))]
    return []


def write_tsv(out, name, columns, rows):
    with (out / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value, ensure_ascii=False, separators=(",", ":")) if isinstance(value, (list, dict)) else value for key, value in row.items()})


def inventory(args):
    work, out = checked_path(args.work), checked_path(args.out)
    if out.exists() or out.is_relative_to(work):
        raise ValueError("Use a new report directory outside the frozen input tree")
    snapshot = json.loads((work / "SNAPSHOT.json").read_text(encoding="utf-8"))
    all_paths = paths_under(work)
    input_bytes = {p.as_posix(): (work / p).read_bytes() for p in all_paths}
    expected = {r["path"]: r for r in snapshot["files"]}
    if set(input_bytes) != set(expected):
        raise ValueError("Frozen file set differs from SNAPSHOT.json")
    for path, data in input_bytes.items():
        if len(data) != expected[path]["bytes"] or sha(data) != expected[path]["sha256"]:
            raise ValueError("Frozen input no longer matches its snapshot manifest")
    trees = {layer: {path[len("sources/" + layer + "/"):]: data for path, data in input_bytes.items() if path.startswith("sources/" + layer + "/")} for layer in LAYERS}
    rows = ledger_rows(input_bytes["CORRECTIONS.tsv"])
    by_file = defaultdict(list)
    for row in rows:
        by_file[row["file"]].append(row)
    files, hunks, candidates, locator_only, redactions, marker_issues, privacy_lookalikes = [], [], [], [], [], [], []
    for path in sorted(trees["fr"].keys() | trees["fr_printed"].keys()):
        present_left, present_right = path in trees["fr"], path in trees["fr_printed"]
        left, right = trees["fr"].get(path, b""), trees["fr_printed"].get(path, b"")
        left_text, left_encoding = classify_text(left)
        right_text, right_encoding = classify_text(right)
        is_text = left_encoding == right_encoding == "utf-8"
        file_class = category(path, is_text)
        identical = present_left == present_right and left == right
        unit = Path(path).stem if file_class == "content_tex" else ""
        sequences = {"fr": markers(left) if is_text and path.endswith(".tex") else [], "fr_printed": markers(right) if is_text and path.endswith(".tex") else []}
        for layer, sequence in sequences.items():
            counts = Counter(m["page"] for m in sequence)
            for page, count in counts.items():
                if count > 1:
                    marker_issues.append({"file": "sources/" + layer + "/" + path, "issue": "duplicate_literal_page_marker", "page": page, "count": count})
            if file_class == "content_tex" and not sequence:
                marker_issues.append({"file": "sources/" + layer + "/" + path, "issue": "no_literal_page_markers", "page": "", "count": 0})
        file_row = {"relative_file": path, "classification": file_class, "fr_present": present_left, "fr_printed_present": present_right,
                    "identical": identical, "fr_bytes": len(left), "fr_printed_bytes": len(right), "fr_sha256": sha(left) if present_left else "", "fr_printed_sha256": sha(right) if present_right else "", "fr_markers": len(sequences["fr"]), "fr_printed_markers": len(sequences["fr_printed"]), "hunks": 0, "reconstruction_verified": True}
        files.append(file_row)
        if identical:
            continue
        a_lines, b_lines = left.splitlines(keepends=True), right.splitlines(keepends=True)
        a_offsets, b_offsets = [0], [0]
        for line in a_lines:
            a_offsets.append(a_offsets[-1] + len(line))
        for line in b_lines:
            b_offsets.append(b_offsets[-1] + len(line))
        operations = difflib.SequenceMatcher(None, a_lines, b_lines, autojunk=False).get_opcodes() if is_text else [("replace", 0, len(a_lines), 0, len(b_lines))]
        rebuilt = b"".join(left[a_offsets[a0]:a_offsets[a1]] if operation == "equal" else right[b_offsets[b0]:b_offsets[b1]] for operation, a0, a1, b0, b1 in operations)
        if rebuilt != right:
            raise AssertionError("Difference reconstruction failed")
        if not operations and present_left != present_right:
            operations = [("insert" if present_right else "delete", 0, 0, 0, 0)]
        for operation, a0, a1, b0, b1 in operations:
            if operation == "equal":
                continue
            hunk_id = "FD" + str(len(hunks) + 1).zfill(6)
            start_left, end_left = a_offsets[a0], a_offsets[a1]
            start_right, end_right = b_offsets[b0], b_offsets[b1]
            old_bytes, new_bytes = left[start_left:end_left], right[start_right:end_right]
            old_raw, old_encoding = classify_text(old_bytes)
            new_raw, new_encoding = classify_text(new_bytes)
            old_prefix = left[:start_left].decode("utf-8") if is_text and path.endswith(".tex") else None
            new_prefix = right[:start_right].decode("utf-8") if is_text and path.endswith(".tex") else None
            old_safe, old_redactions, old_lookalikes = mask_private(old_raw, old_prefix) if old_encoding == "utf-8" else (old_raw, [], [])
            new_safe, new_redactions, new_lookalikes = mask_private(new_raw, new_prefix) if new_encoding == "utf-8" else (new_raw, [], [])
            for side, findings in [("fr", old_redactions), ("fr_printed", new_redactions)]:
                for finding in findings:
                    redactions.append(dict(finding, hunk_id=hunk_id, side=side))
            for side, findings in [("fr", old_lookalikes), ("fr_printed", new_lookalikes)]:
                for finding in findings:
                    privacy_lookalikes.append(dict(finding, hunk_id=hunk_id, side=side))
            left_location = location(left, sequences["fr"], start_left, end_left)
            right_location = location(right, sequences["fr_printed"], start_right, end_right)
            page_labels = set(left_location["covered_pages"] + right_location["covered_pages"])
            page_labels.update(value for value in [left_location["anchor_page"], right_location["anchor_page"]] if value)
            page_keys = sorted(unit + "-" + label for label in page_labels) if unit else []
            left_path, right_path = "sources/fr/" + path, "sources/fr_printed/" + path
            file_rows = by_file[left_path] + by_file[right_path]
            locator_rows = [row for row in file_rows if not page_keys or row["printed_page"] in page_keys]
            old_normalized, new_normalized = normalized(old_raw), normalized(new_raw)
            hunk_candidates = []
            if old_encoding == new_encoding == "utf-8":
                for row in file_rows:
                    compatible = not page_keys or row["printed_page"] in page_keys
                    found = matches(row, old_raw, new_raw, old_normalized, new_normalized, compatible, args.min_single_side_chars)
                    if not found:
                        continue
                    hunk_candidates.append({"hunk_id": hunk_id, "row_id": row["row_id"], "data_row": row["data_row"], "physical_line_start": row["physical_line_start"], "physical_line_end": row["physical_line_end"], "ledger_file": row["file"], "ledger_layer": row["layer"], "ledger_printed_page": row["printed_page"], "page_relation": "exact_file_no_marker_scope" if not page_keys else ("file_and_page_match" if compatible else "file_match_page_mismatch"), "methods": sorted({item[0] for item in found}), "orientations": sorted({item[1] for item in found}), "matched_fields": sorted({item[2] for item in found}), "row_sha256": row["row_sha256"], "ledger_old_sha256": sha(row["old"].encode()), "ledger_new_sha256": sha(row["new"].encode())})
            candidates.extend(hunk_candidates)
            paired = sum(any(method != "one_side_exact_distinguishing_substring" for method in item["methods"]) for item in hunk_candidates)
            if not hunk_candidates:
                for row in locator_rows:
                    locator_only.append({"hunk_id": hunk_id, "row_id": row["row_id"], "data_row": row["data_row"], "ledger_file": row["file"], "ledger_printed_page": row["printed_page"], "method": "exact_file_and_page_only_no_text_match" if page_keys else "exact_file_only_no_marker_or_text_match", "row_sha256": row["row_sha256"]})
            hunk = {"hunk_id": hunk_id, "relative_file": path, "classification": file_class, "operation": operation,
                    "fr_file": left_path, "fr_printed_file": right_path, "fr_range": left_location, "fr_printed_range": right_location,
                    "candidate_page_keys": page_keys, "cross_page": left_location["cross_page"] or right_location["cross_page"],
                    "different_anchor_pages": left_location["anchor_page"] != right_location["anchor_page"],
                    "old_text": old_safe, "new_text": new_safe, "old_encoding": old_encoding, "new_encoding": new_encoding,
                    "old_sha256": sha(old_bytes), "new_sha256": sha(new_bytes), "old_bytes": len(old_bytes), "new_bytes": len(new_bytes),
                    "exact_text_in_report": not old_redactions and not new_redactions,
                    "text_candidate_count": len(hunk_candidates), "paired_candidate_count": paired, "single_side_candidate_count": len(hunk_candidates)-paired,
                    "candidate_row_ids": [item["row_id"] for item in hunk_candidates],
                    "matching_status": "unmatched" if not hunk_candidates else ("one_candidate" if len(hunk_candidates) == 1 else "multiple_candidates"),
                    "mechanically_ambiguous": len(hunk_candidates) > 1,
                    "only_single_side_candidates": bool(hunk_candidates) and paired == 0,
                    "locator_candidate_count": len(locator_rows),
                    "candidate_page_mismatches": sum(item["page_relation"] == "file_match_page_mismatch" for item in hunk_candidates)}
            hunks.append(hunk)
            file_row["hunks"] += 1
    for path, data in input_bytes.items():
        if (work / path).read_bytes() != data:
            raise RuntimeError("A frozen input changed during inventory; no reports written")
    if set(p.as_posix() for p in paths_under(work)) != set(input_bytes):
        raise RuntimeError("Frozen file set changed during inventory; no reports written")
    counts = Counter(h["matching_status"] for h in hunks)
    summary = {"created_utc": utc(), "snapshot_started_utc": snapshot["snapshot_started_utc"], "snapshot_completed_utc": snapshot["snapshot_completed_utc"],
               "frozen_root": relative(work), "snapshot_manifest_sha256": sha((work / "SNAPSHOT.json").read_bytes()),
               "source_tree_sha256": {layer: tree_hash(trees[layer]) for layer in LAYERS}, "ledger_sha256": sha(input_bytes["CORRECTIONS.tsv"]), "ledger_rows": len(rows),
               "relative_file_pairs": len(files), "identical_file_pairs": sum(f["identical"] for f in files), "nonidentical_files": sum(not f["identical"] for f in files),
               "changed_hunks": len(hunks), "hunks_by_status": dict(counts), "hunks_with_only_single_side_candidates": sum(h["only_single_side_candidates"] for h in hunks),
               "candidate_row_links": len(candidates), "locator_only_links": len(locator_only), "cross_page_hunks": sum(h["cross_page"] for h in hunks), "different_anchor_page_hunks": sum(h["different_anchor_pages"] for h in hunks),
               "privacy_redactions": len(redactions), "privacy_TeX_control_lookalikes": len(privacy_lookalikes), "all_hunk_text_exact": not redactions, "all_differences_reconstruct": all(f["reconstruction_verified"] for f in files), "inputs_unchanged": True,
               "diff_algorithm": "Python difflib.SequenceMatcher on bytes.splitlines(keepends=True), autojunk=False; each non-equal opcode is one hunk; fr is left/old, fr_printed is right/new.",
               "single_side_minimum_characters": args.min_single_side_chars,
               "script_sha256": sha(Path(__file__).read_bytes()), "marker_helper_sha256": sha(Path(__file__).with_name("source_segments.py").read_bytes())}
    out.mkdir(parents=True)
    (out / "SUMMARY.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "HUNKS.json").write_text(json.dumps({"orientation": "fr_to_fr_printed", "hunks": hunks}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_tsv(out, "FILES.tsv", list(files[0]) if files else ["relative_file"], files)
    flat_hunks = []
    page_index = []
    for hunk in hunks:
        flat = {key: value for key, value in hunk.items() if key not in {"fr_range", "fr_printed_range"}}
        for layer, key in [("fr", "fr_range"), ("fr_printed", "fr_printed_range")]:
            flat.update({layer + "_" + field: value for field, value in hunk[key].items()})
        flat_hunks.append(flat)
        for page_key in hunk["candidate_page_keys"] or [""]:
            page_index.append({"unit_page_key": page_key, "hunk_id": hunk["hunk_id"], "relative_file": hunk["relative_file"], "classification": hunk["classification"], "fr_anchor_rule": hunk["fr_range"]["anchor_rule"], "fr_printed_anchor_rule": hunk["fr_printed_range"]["anchor_rule"], "fr_line_start": hunk["fr_range"]["line_start"], "fr_printed_line_start": hunk["fr_printed_range"]["line_start"], "cross_page": hunk["cross_page"], "matching_status": hunk["matching_status"], "candidate_row_ids": hunk["candidate_row_ids"]})
    write_tsv(out, "HUNKS.tsv", list(flat_hunks[0]) if flat_hunks else ["hunk_id"], flat_hunks)
    write_tsv(out, "PAGE_HUNK_INDEX.tsv", ["unit_page_key", "hunk_id", "relative_file", "classification", "fr_anchor_rule", "fr_printed_anchor_rule", "fr_line_start", "fr_printed_line_start", "cross_page", "matching_status", "candidate_row_ids"], page_index)
    candidate_columns = ["hunk_id", "row_id", "data_row", "physical_line_start", "physical_line_end", "ledger_file", "ledger_layer", "ledger_printed_page", "page_relation", "methods", "orientations", "matched_fields", "row_sha256", "ledger_old_sha256", "ledger_new_sha256"]
    write_tsv(out, "CANDIDATE_ROWS.tsv", candidate_columns, candidates)
    write_tsv(out, "LOCATOR_ONLY_CANDIDATES.tsv", ["hunk_id", "row_id", "data_row", "ledger_file", "ledger_printed_page", "method", "row_sha256"], locator_only)
    write_tsv(out, "MARKER_ISSUES.tsv", ["file", "issue", "page", "count"], marker_issues)
    write_tsv(out, "PRIVACY_REDACTIONS.tsv", ["hunk_id", "side", "character_start", "character_end", "kind"], redactions)
    write_tsv(out, "PRIVACY_TEX_LOOKALIKES.tsv", ["hunk_id", "side", "character_start", "character_end", "control_token", "span_sha256", "rule"], privacy_lookalikes)
    write_tsv(out, "MATCH_STATUS.tsv", ["hunk_id", "relative_file", "candidate_page_keys", "matching_status", "text_candidate_count", "paired_candidate_count", "single_side_candidate_count", "only_single_side_candidates", "mechanically_ambiguous", "locator_candidate_count", "candidate_page_mismatches"], hunks)
    print(json.dumps(summary, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ["freeze", "inventory"]:
        child = sub.add_parser(name)
        child.add_argument("--work", type=Path, required=True)
        child.add_argument("--out", type=Path, required=True)
        if name == "inventory":
            child.add_argument("--min-single-side-chars", type=int, default=12)
    args = parser.parse_args()
    if args.command == "freeze":
        freeze(args)
    else:
        if args.min_single_side_chars < 1:
            raise ValueError("Single-side minimum must be positive")
        inventory(args)


if __name__ == "__main__":
    main()
