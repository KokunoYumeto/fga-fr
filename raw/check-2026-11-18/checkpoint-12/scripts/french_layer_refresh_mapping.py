"""Bind a fresh exact French difference inventory to an earlier inventory.

All source and correction-ledger inputs are read only. Payload, coordinate,
declared-wrapper and history links are mechanical candidates, not adjudications.
"""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone
import argparse, csv, hashlib, json, re

from french_layer_differences import HEADER, ledger_rows
from french_unmatched_format_candidates import (
    ALPHABETS, PROFILES, distinguishing, find_pair, md_payload, project,
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_tsv(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_tsv(path, rows, fields=None):
    fields = fields or list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value, ensure_ascii=False, separators=(",", ":")) if isinstance(value, (list, dict)) else value for key, value in row.items()})


def range_string(hunk, key):
    loc = hunk[key]
    return str(loc["line_start"]) + ("–" + str(loc["line_end"]) if loc["line_end"] not in (None, loc["line_start"]) else "")


def span(hunk, key="fr_printed_range"):
    loc = hunk[key]
    return loc["byte_start"], loc["byte_end_exclusive"]


def overlap(a, b):
    return max(a[0], b[0]) < min(a[1], b[1]) or (a[0] == a[1] == b[0] == b[1])


def manifest_inputs(root):
    manifest = read_json(root / "SNAPSHOT.json")
    inputs = {item["path"]: (root / item["path"]).read_bytes() for item in manifest["files"]}
    for item in manifest["files"]:
        data = inputs[item["path"]]
        assert sha(data) == item["sha256"] and len(data) == item["bytes"]
    return manifest, inputs


def make_payload(row):
    return {key: row[key] for key in ["row_id", "data_row", "physical_line_start", "physical_line_end", "row_sha256", *HEADER]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ["old-report", "current-report", "old-frozen", "current-frozen", "supplement-report", "supplement-frozen", "out"]:
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError("Use a new mapping-report directory.")
    started = datetime.now(timezone.utc).isoformat()
    old_manifest, old_inputs = manifest_inputs(args.old_frozen)
    current_manifest, current_inputs = manifest_inputs(args.current_frozen)
    old_summary = read_json(args.old_report / "SUMMARY.json")
    current_summary = read_json(args.current_report / "SUMMARY.json")
    old_hunks = read_json(args.old_report / "HUNKS.json")["hunks"]
    current_hunks = read_json(args.current_report / "HUNKS.json")["hunks"]
    old_by_id = {h["hunk_id"]: h for h in old_hunks}
    current_by_id = {h["hunk_id"]: h for h in current_hunks}
    old_rows = ledger_rows(old_inputs["CORRECTIONS.tsv"])
    rows = ledger_rows(current_inputs["CORRECTIONS.tsv"])
    row_by_id = {row["row_id"]: row for row in rows}
    previous_supplement_rows = ledger_rows((args.supplement_frozen / "CORRECTIONS.tsv").read_bytes())
    assert all(a["row_sha256"] == b["row_sha256"] for a, b in zip(old_rows, rows)) and len(rows) >= len(old_rows)
    assert all(a["row_sha256"] == b["row_sha256"] for a, b in zip(previous_supplement_rows, rows)) and len(rows) >= len(previous_supplement_rows)
    french = lambda row: row["file"].startswith(("sources/fr/", "sources/fr_printed/"))
    same_french_rows = [r["row_sha256"] for r in previous_supplement_rows if french(r)] == [r["row_sha256"] for r in rows if french(r)]
    changes = []
    for path in sorted(set(old_inputs) | set(current_inputs)):
        if path == "CORRECTIONS.tsv":
            continue
        before, after = old_inputs.get(path), current_inputs.get(path)
        changes.append({"file": path, "old_sha256": sha(before) if before is not None else "", "current_sha256": sha(after) if after is not None else "", "old_bytes": len(before) if before is not None else 0, "current_bytes": len(after) if after is not None else 0, "identical": before == after})

    mappings, reverse = [], defaultdict(list)
    for hunk in current_hunks:
        old_pool = [old for old in old_hunks if old["relative_file"] == hunk["relative_file"]]
        printed_identical = old_inputs[hunk["fr_printed_file"]] == current_inputs[hunk["fr_printed_file"]]
        exact_span = [old for old in old_pool if printed_identical and span(old) == span(hunk) and old["new_sha256"] == hunk["new_sha256"]]
        exact_pair = [old for old in exact_span if old["old_sha256"] == hunk["old_sha256"]]
        if exact_pair:
            candidates, method = exact_pair, "exact_payload_pair_and_identical_printed_span"
        elif exact_span:
            candidates, method = exact_span, "identical_printed_span_and_payload_changed_corrected_payload"
        else:
            candidates = [old for old in old_pool if printed_identical and overlap(span(old), span(hunk))]
            if candidates and all(span(old)[0] <= span(hunk)[0] and span(hunk)[1] <= span(old)[1] for old in candidates):
                method = "current_printed_span_contained_in_old_span"
            else:
                method = "printed_span_overlap_candidate" if candidates else "unmapped"
        for old in candidates:
            reverse[old["hunk_id"]].append(hunk["hunk_id"])
        mapping = {"current_hunk_id": hunk["hunk_id"], "old_hunk_ids": [old["hunk_id"] for old in candidates], "relative_file": hunk["relative_file"], "pages": hunk["candidate_page_keys"], "method": method, "candidate_count": len(candidates), "printed_source_bytes_identical": printed_identical, "old_fr_lines": [range_string(old, "fr_range") for old in candidates], "current_fr_lines": range_string(hunk, "fr_range"), "old_printed_lines": [range_string(old, "fr_printed_range") for old in candidates], "current_printed_lines": range_string(hunk, "fr_printed_range"), "old_old_sha256": [old["old_sha256"] for old in candidates], "old_new_sha256": [old["new_sha256"] for old in candidates], "current_old_sha256": hunk["old_sha256"], "current_new_sha256": hunk["new_sha256"], "current_matching_status": hunk["matching_status"], "current_candidate_row_ids": hunk["candidate_row_ids"], "footnote_removal_row_ids": []}
        mappings.append(mapping)
    mapping_by_id = {m["current_hunk_id"]: m for m in mappings}

    post_french = [row for row in rows[len(old_rows):] if french(row)]
    footnotes, replay = [], []
    for path in sorted({r["file"] for r in post_french}):
        original = old_inputs[path]
        working = original
        use_crlf = b"\r\n" in original and b"\n" not in original.replace(b"\r\n", b"")
        policy = "ledger CRLF-to-LF then LF-to-CRLF; all original source newlines are CRLF" if use_crlf else "ledger CRLF-to-LF; source LF bytes"
        file_ops = []
        for row in [r for r in post_french if r["file"] == path]:
            def encoded(value):
                value = value.replace("\r\n", "\n")
                return (value.replace("\n", "\r\n") if use_crlf else value).encode("utf-8")
            left, right = encoded(row["old"]), encoded(row["new"])
            assert left and row["new"] == "" and row["old"].startswith("\\footnote{") and row["old"].endswith("}")
            assert original.count(left) == working.count(left) == 1
            original_start, replay_start = original.index(left), working.index(left)
            original_end = original_start + len(left)
            intersecting = [h for h in old_hunks if h["fr_file"] == path and overlap((original_start, original_end), span(h, "fr_range"))]
            current_ids = list(dict.fromkeys(cid for h in intersecting for cid in reverse[h["hunk_id"]]))
            for cid in current_ids:
                mapping_by_id[cid]["footnote_removal_row_ids"].append(row["row_id"])
            operation = {"row_id": row["row_id"], "data_row": row["data_row"], "physical_line_start": row["physical_line_start"], "physical_line_end": row["physical_line_end"], "file": path, "printed_page": row["printed_page"], "row_sha256": row["row_sha256"], "ledger_old_sha256": sha(row["old"].encode()), "ledger_new_sha256": sha(row["new"].encode()), "source_operand_sha256": sha(left), "source_operand_bytes": len(left), "newline_policy": policy, "original_byte_start": original_start, "original_byte_end_exclusive": original_end, "original_line_start": original.count(b"\n", 0, original_start) + 1, "original_line_end": original.count(b"\n", 0, original_end - 1) + 1, "intermediate_replay_byte_start": replay_start, "original_occurrence_count": 1, "intermediate_occurrence_count": 1, "old_hunk_ids": [h["hunk_id"] for h in intersecting], "current_hunk_ids": current_ids, "current_source_contains_deleted_operand": left in current_inputs[path]}
            footnotes.append(operation)
            file_ops.append(operation)
            working = working[:replay_start] + right + working[replay_start + len(left):]
        replay.append({"file": path, "old_sha256": sha(original), "current_sha256": sha(current_inputs[path]), "replayed_sha256": sha(working), "old_bytes": len(original), "current_bytes": len(current_inputs[path]), "replayed_bytes": len(working), "row_ids": [r["row_id"] for r in file_ops], "reproduces_current_bytes_exactly": working == current_inputs[path]})
        assert working == current_inputs[path]
        for operation in file_ops:
            current_anchor = operation["original_byte_start"] - sum(other["source_operand_bytes"] for other in file_ops if other["original_byte_end_exclusive"] <= operation["original_byte_start"])
            operation["current_deletion_anchor_byte"] = current_anchor
            operation["current_deletion_anchor_line"] = working.count(b"\n", 0, current_anchor) + 1

    unmatched = [h for h in current_hunks if h["matching_status"] == "unmatched"]
    by_file, mirrors = defaultdict(list), defaultdict(list)
    for row in rows:
        if french(row):
            rel = "/".join(row["file"].split("/")[2:])
            by_file[rel].append(row)
            if row["file"].startswith("sources/fr_printed/"):
                mirrors[rel, row["printed_page"], row["old"], row["new"]].append(row["row_id"])
    candidates, details, projections, statuses, histories, payload_ids = [], [], [], [], [], set()
    for hunk in unmatched:
        found = []
        collapsed = []
        for profile, wrappers in PROFILES:
            left, lm = project(hunk["old_text"], profile)
            right, rm = project(hunk["new_text"], profile)
            projections.append({"hunk_id": hunk["hunk_id"], "profile": profile, "fr_projection": left, "fr_printed_projection": right, "fr_metadata": lm, "fr_printed_metadata": rm})
            if left == right:
                collapsed.append(profile)
                continue
            for row in by_file[hunk["relative_file"]]:
                same_page = row["printed_page"] in hunk["candidate_page_keys"]
                if not same_page and min(len(row["old"]), len(row["new"])) < 12:
                    continue
                ro, rom = project(row["old"], profile)
                rn, rnm = project(row["new"], profile)
                if not ro or not rn or ro == rn:
                    continue
                for match in find_pair(ro, rn, left, right, same_page):
                    item = {"candidate_id": f"FC{len(candidates) + 1:06d}", "hunk_id": hunk["hunk_id"], "old_hunk_ids": mapping_by_id[hunk["hunk_id"]]["old_hunk_ids"], "row_id": row["row_id"], "data_row": row["data_row"], "physical_line_start": row["physical_line_start"], "physical_line_end": row["physical_line_end"], "ledger_file": row["file"], "ledger_layer": row["layer"], "ledger_page": row["printed_page"], "ledger_kind": row["kind"], "page_relation": "same page" if same_page else "different page", "profile": profile, "method": match["method"], "orientation": match["orientation"], "whole_hunk_pair": match["whole_hunk_pair"], "old_occurrences": match["old_occurrences"], "new_occurrences": match["new_occurrences"], "short_fragment": match["short_fragment"], "sensitive_wrappers_removed": any(m["sensitive_wrapper_removed"] for m in [lm, rm, rom, rnm]), "alphabet_controls_preserved": True, "row_sha256": row["row_sha256"], "ledger_old_sha256": sha(row["old"].encode()), "ledger_new_sha256": sha(row["new"].encode()), "fr_hunk_sha256": hunk["old_sha256"], "fr_printed_hunk_sha256": hunk["new_sha256"], "payload_link": "FORMAT_LEDGER_PAYLOADS.md#" + row["row_id"].lower()}
                    candidates.append(item)
                    found.append(item)
                    details.append({**item, "match": match, "ledger_old_projection": ro, "ledger_new_projection": rn, "ledger_old_projection_metadata": rom, "ledger_new_projection_metadata": rnm})
                    payload_ids.add(row["row_id"])
        current_history = []
        if not found:
            for row in by_file[hunk["relative_file"]]:
                if row["file"] != hunk["fr_file"] or row["printed_page"] not in hunk["candidate_page_keys"]:
                    continue
                twins = mirrors[hunk["relative_file"], row["printed_page"], row["old"], row["new"]]
                item = {"hunk_id": hunk["hunk_id"], "row_id": row["row_id"], "data_row": row["data_row"], "physical_line_start": row["physical_line_start"], "physical_line_end": row["physical_line_end"], "ledger_page": row["printed_page"], "kind": row["kind"], "statement": row["statement"], "identical_printed_operation_rows": twins, "no_identical_printed_operation": not twins, "row_sha256": row["row_sha256"], "payload_link": "FORMAT_LEDGER_PAYLOADS.md#" + row["row_id"].lower()}
                histories.append(item)
                current_history.append(item)
                if not twins:
                    payload_ids.add(row["row_id"])
        statuses.append({"hunk_id": hunk["hunk_id"], "old_hunk_ids": mapping_by_id[hunk["hunk_id"]]["old_hunk_ids"], "relative_file": hunk["relative_file"], "pages": hunk["candidate_page_keys"], "current_fr_lines": range_string(hunk, "fr_range"), "current_printed_lines": range_string(hunk, "fr_printed_range"), "mapping_method": mapping_by_id[hunk["hunk_id"]]["method"], "paired_candidate_row_ids": list(dict.fromkeys(c["row_id"] for c in found)), "paired_candidate_row_count": len({c["row_id"] for c in found}), "candidate_link_count": len(found), "profiles_with_pair": list(dict.fromkeys(c["profile"] for c in found)), "profiles_collapsing_difference": collapsed, "history_rows": len(current_history), "history_without_identical_printed_operation": sum(c["no_identical_printed_operation"] for c in current_history)})

    old_details = read_json(args.supplement_report / "CANDIDATE_DETAILS.json")
    revalidated = []
    for item in old_details:
        mapped = reverse[item["hunk_id"]]
        for cid in mapped:
            current = current_by_id[cid]
            left, _ = project(current["old_text"], item["profile"])
            right, _ = project(current["new_text"], item["profile"])
            x, y = (right, left) if item["orientation"] == "printed_to_corrected" else (left, right)
            a, b = item["match"]["ledger_old_fragment"], item["match"]["ledger_new_fragment"]
            row_unchanged = row_by_id[item["row_id"]]["row_sha256"] == item["row_sha256"]
            revalidated.append({"old_candidate_id": item["candidate_id"], "old_hunk_id": item["hunk_id"], "current_hunk_id": cid, "row_id": item["row_id"], "profile": item["profile"], "orientation": item["orientation"], "old_method": item["method"], "ledger_row_hash_unchanged": row_unchanged, "stored_fragment_pair_still_distinguishing": distinguishing(a, b, x, y) and row_unchanged, "old_occurrences_before": item["old_occurrences"], "new_occurrences_before": item["new_occurrences"], "old_occurrences_current": x.count(a), "new_occurrences_current": y.count(b), "whole_current_hunk_pair": a == x and b == y, "row_sha256": item["row_sha256"]})
    old_no_pair = [s for s in read_tsv(args.supplement_report / "HUNK_STATUS.tsv") if int(s["paired_candidate_row_count"]) == 0]
    status_by_id = {s["hunk_id"]: s for s in statuses}
    previous_no_pair = []
    for status in old_no_pair:
        old = old_by_id[status["hunk_id"]]
        for cid in reverse[old["hunk_id"]]:
            current = current_by_id[cid]
            fresh = status_by_id.get(cid)
            previous_no_pair.append({"old_hunk_id": old["hunk_id"], "current_hunk_id": cid, "pages": current["candidate_page_keys"], "relative_file": current["relative_file"], "old_fr_lines": range_string(old, "fr_range"), "current_fr_lines": range_string(current, "fr_range"), "current_printed_lines": range_string(current, "fr_printed_range"), "both_payloads_exactly_unchanged": old["old_sha256"] == current["old_sha256"] and old["new_sha256"] == current["new_sha256"], "current_ordinary_status": current["matching_status"], "current_format_candidate_links": fresh["candidate_link_count"] if fresh else "not searched", "current_history_rows": fresh["history_rows"] if fresh else 0, "current_history_without_identical_printed_operation": fresh["history_without_identical_printed_operation"] if fresh else 0, "fr_payload_sha256": current["old_sha256"], "printed_payload_sha256": current["new_sha256"]})

    args.out.mkdir(parents=True)
    write_tsv(args.out / "SOURCE_CHANGES.tsv", changes)
    write_tsv(args.out / "CURRENT_TO_OLD.tsv", mappings)
    write_tsv(args.out / "OLD_TO_CURRENT.tsv", [{"old_hunk_id": h["hunk_id"], "current_hunk_ids": reverse[h["hunk_id"]], "relative_file": h["relative_file"], "old_pages": h["candidate_page_keys"], "mapping_count": len(reverse[h["hunk_id"]])} for h in old_hunks])
    write_tsv(args.out / "FOOTNOTE_REMOVALS.tsv", footnotes)
    write_json(args.out / "FOOTNOTE_OPERATIONS.json", [make_payload(row) for row in post_french])
    write_json(args.out / "FOOTNOTE_REPLAY.json", replay)
    changed = [{"mapping": m, "old_hunks": [old_by_id[oid] for oid in m["old_hunk_ids"]], "current_hunk": current_by_id[m["current_hunk_id"]]} for m in mappings if m["method"] != "exact_payload_pair_and_identical_printed_span"]
    write_json(args.out / "CHANGED_HUNKS.json", changed)
    write_tsv(args.out / "PREVIOUS_NO_PAIR.tsv", previous_no_pair)
    write_tsv(args.out / "OLD_FORMAT_LINK_REVALIDATION.tsv", revalidated)
    write_tsv(args.out / "FORMAT_CANDIDATE_LINKS.tsv", candidates)
    write_json(args.out / "FORMAT_CANDIDATE_DETAILS.json", details)
    write_json(args.out / "FORMAT_HUNK_PROJECTIONS.json", projections)
    write_tsv(args.out / "FORMAT_HUNK_STATUS.tsv", statuses)
    write_tsv(args.out / "FR_CORRECTED_NO_PAIR_HISTORY.tsv", histories)
    write_tsv(args.out / "FR_ONLY_NO_PAIR_HISTORY.tsv", [item for item in histories if item["no_identical_printed_operation"]])
    payloads = [make_payload(row) for row in rows if row["row_id"] in payload_ids]
    write_json(args.out / "FORMAT_LEDGER_PAYLOADS.json", payloads)
    (args.out / "FORMAT_LEDGER_PAYLOADS.md").write_text("# Exact candidate and history ledger payloads\n\nQuoted as data from the frozen correction ledger; no row is approved or applied by this report. Row identifiers bind to the ledger hash in INVENTORY.json.\n\n" + "\n".join(md_payload(row) for row in payloads), encoding="utf-8")
    profiles = [{"profile": name, "removed_balanced_wrappers": list(wrappers), "whitespace": "ASCII whitespace collapsed to one space; outer ASCII whitespace trimmed", "retained_alphabet_controls": sorted(ALPHABETS), "meaning_warning": "Lexical projection only. Upright fonts and underline commands can distinguish notation; their removal never establishes equivalence."} for name, wrappers in PROFILES]
    write_json(args.out / "FORMAT_PROFILES.json", profiles)
    write_json(args.current_report / "FROZEN_SNAPSHOT.json", current_manifest)
    write_json(args.current_report / "UNMATCHED_HUNKS.json", {"snapshot": current_summary["snapshot_started_utc"], "orientation": "fr_to_fr_printed", "meaning": "No candidate from the original exact/ASCII-whitespace/one-sided matcher; this does not establish missing correction or reading.", "hunks": unmatched})
    write_tsv(args.current_report / "UNMATCHED_HUNKS.tsv", [{"hunk_id": h["hunk_id"], "relative_file": h["relative_file"], "pages": h["candidate_page_keys"], "fr_lines": range_string(h, "fr_range"), "printed_lines": range_string(h, "fr_printed_range"), "old_sha256": h["old_sha256"], "new_sha256": h["new_sha256"], "locator_candidate_count": h["locator_candidate_count"]} for h in unmatched])

    source_only_changes = [c["file"] for c in changes if not c["identical"]]
    counts = Counter(m["method"] for m in mappings)
    meta = {"created_utc": started, "completed_utc": datetime.now(timezone.utc).isoformat(), "paths": {key: getattr(args, key).as_posix() for key in vars(args)}, "old_snapshot_started_utc": old_summary["snapshot_started_utc"], "current_snapshot_started_utc": current_summary["snapshot_started_utc"], "current_snapshot_completed_utc": current_summary["snapshot_completed_utc"], "old_ledger_sha256": sha(old_inputs["CORRECTIONS.tsv"]), "current_ledger_sha256": sha(current_inputs["CORRECTIONS.tsv"]), "old_ledger_rows": len(old_rows), "current_ledger_rows": len(rows), "old_row_hash_prefix_unchanged": True, "supplement_row_hash_prefix_unchanged": True, "French_ledger_rows_unchanged_since_supplement_capture": same_french_rows, "source_changes": source_only_changes, "old_hunks": len(old_hunks), "current_hunks": len(current_hunks), "mapping_method_counts": dict(counts), "all_current_hunks_unique_mapping": all(m["candidate_count"] == 1 for m in mappings), "all_old_hunks_unique_mapping": all(len(reverse[h["hunk_id"]]) == 1 for h in old_hunks), "mapped_ids_happen_to_remain_same": all(m["old_hunk_ids"] == [m["current_hunk_id"]] for m in mappings), "recorded_footnote_removals": len(footnotes), "replay_exact_for_all_changed_files": all(r["reproduces_current_bytes_exactly"] for r in replay) and sorted(r["file"] for r in replay) == sorted(source_only_changes), "ordinary_unmatched_hunks": len(unmatched), "format_paired_hunks": sum(bool(s["candidate_link_count"]) for s in statuses), "format_no_pair_hunks": sum(not s["candidate_link_count"] for s in statuses), "format_candidate_links": len(candidates), "format_candidate_distinct_ledger_rows": len({c["row_id"] for c in candidates}), "format_payload_rows": len(payloads), "format_history_links": len(histories), "format_history_without_identical_printed_operation": sum(h["no_identical_printed_operation"] for h in histories), "previous_no_pair_cases": len(previous_no_pair), "previous_format_links_retested": len(revalidated), "previous_format_links_still_distinguishing": sum(r["stored_fragment_pair_still_distinguishing"] for r in revalidated), "previous_format_links_no_longer_distinguishing": [r["old_candidate_id"] for r in revalidated if not r["stored_fragment_pair_still_distinguishing"]], "input_hashes": {"old_HUNKS.json": sha((args.old_report / "HUNKS.json").read_bytes()), "current_HUNKS.json": sha((args.current_report / "HUNKS.json").read_bytes()), "old_manifest": sha((args.old_frozen / "SNAPSHOT.json").read_bytes()), "current_manifest": sha((args.current_frozen / "SNAPSHOT.json").read_bytes()), "previous_format_details": sha((args.supplement_report / "CANDIDATE_DETAILS.json").read_bytes()), "mapping_script": sha(Path(__file__).read_bytes()), "projection_helper": sha(Path(__file__).with_name("french_unmatched_format_candidates.py").read_bytes())}, "scope": "Mechanical coordinates, exact bytes, declared projections and ledger candidates only; no mathematical, translation, correction-validity, reading-completeness or net-coverage adjudication."}
    write_json(args.out / "INVENTORY.json", meta)

    mapping_md = ["# Current hunk to earlier FD mapping", "", "Both inventories use corrected French as old/left and printed French as new/right. All printed files are byte-identical between snapshots. Each current hunk maps uniquely to one old hunk by the declared payload/coordinate rule. The FD strings happen to remain identical; their snapshot-qualified meaning must still be retained.", "", "| Current FD | Old FD | Page | Current FR lines | Printed lines | Mechanical rule | Footnote row |", "|---|---|---|---|---|---|---|"]
    for m in mappings:
        short = {"exact_payload_pair_and_identical_printed_span": "Exact pair and span", "identical_printed_span_and_payload_changed_corrected_payload": "Same printed span; FR changed", "current_printed_span_contained_in_old_span": "Printed span shrank within old span"}.get(m["method"], m["method"])
        mapping_md.append(f"| {m['current_hunk_id']} | {', '.join(m['old_hunk_ids'])} | {', '.join(m['pages'])} | {m['current_fr_lines']} | {m['current_printed_lines']} | {short} | {', '.join(m['footnote_removal_row_ids'])} |")
    (args.out / "CURRENT_TO_OLD.md").write_text("\n".join(mapping_md) + "\n", encoding="utf-8")
    footnote_md = ["# Recorded footnote-removal continuity", "", "The twelve appended French operations are quoted as ledger data in FOOTNOTE_OPERATIONS.json. Each recorded old operand occurs exactly once in the earlier corrected source. Converting only ledger line endings to the source's existing CRLF convention and replaying these literal deletions in append order, in memory, reproduces both current source files byte for byte. No source or ledger was written. This establishes byte continuity only; it does not adjudicate the text of a note or any neighboring correction.", "", "| Ledger row | Page | Old FD → current FD | Old FR lines | Current deletion anchor line | Current hunk FR lines |", "|---|---|---|---|---|---|"]
    for f in footnotes:
        footnote_md.append(f"| {f['row_id']} | {f['printed_page']} | {', '.join(f['old_hunk_ids'])} → {', '.join(f['current_hunk_ids'])} | {f['original_line_start']}–{f['original_line_end']} | {f['current_deletion_anchor_line']} | {', '.join(range_string(current_by_id[c], 'fr_range') for c in f['current_hunk_ids'])} |")
    footnote_md += ["", "## Exact reconstruction hashes", "", "| File | Earlier SHA-256 | Current and replayed SHA-256 |", "|---|---|---|"]
    for r in replay:
        footnote_md.append(f"| {r['file']} | `{r['old_sha256']}` | `{r['current_sha256']}` |")
    (args.out / "FOOTNOTE_REMOVALS.md").write_text("\n".join(footnote_md) + "\n", encoding="utf-8")
    no_pair_md = ["# Previous twelve no-pair cases", "", "These are the twelve cases without a paired candidate in the previous declared-wrapper search. Both hunk payloads remain exactly unchanged, and the current search again yields no pair for each. Lack of a lexical pair does not establish an unrecorded correction, missing proof, or missing reading. Current French page operations are provided in append order in FR_CORRECTED_NO_PAIR_HISTORY.tsv; the subset without a byte-identical printed-layer operation is FR_ONLY_NO_PAIR_HISTORY.tsv.", "", "| Old FD | Current FD | Page | Current FR lines | Printed lines | Current candidate pairs | FR-only history links |", "|---|---|---|---|---|---|---|"]
    for r in previous_no_pair:
        no_pair_md.append(f"| {r['old_hunk_id']} | {r['current_hunk_id']} | {', '.join(r['pages'])} | {r['current_fr_lines']} | {r['current_printed_lines']} | {r['current_format_candidate_links']} | {r['current_history_without_identical_printed_operation']} |")
    (args.out / "PREVIOUS_NO_PAIR.md").write_text("\n".join(no_pair_md) + "\n", encoding="utf-8")
    review_md = ["# Current ordinary-unmatched hunks", "", "The ordinary inventory's unmatched count and the supplementary paired-candidate count describe different lexical searches. Candidate pairs can cover only local fragments. A paired candidate is not a finding that the full net hunk difference is recorded or justified.", "", "| Current FD | Old FD | Page | FR lines | Format pair links | Distinct ledger rows | First profile | History without identical printed operation |", "|---|---|---|---|---|---|---|---|"]
    for s in statuses:
        review_md.append(f"| {s['hunk_id']} | {', '.join(s['old_hunk_ids'])} | {', '.join(s['pages'])} | {s['current_fr_lines']} | {s['candidate_link_count']} | {', '.join(s['paired_candidate_row_ids'])} | {s['profiles_with_pair'][0] if s['profiles_with_pair'] else 'None'} | {s['history_without_identical_printed_operation']} |")
    (args.out / "CURRENT_UNMATCHED_REVIEW.md").write_text("\n".join(review_md) + "\n", encoding="utf-8")

    for path, data in old_inputs.items():
        assert (args.old_frozen / path).read_bytes() == data
    for path, data in current_inputs.items():
        assert (args.current_frozen / path).read_bytes() == data
    for path in args.out.iterdir():
        if path.is_file() and re.search(r"(?<![\w.-])[\w.%+-]+@[\w.-]+\.[A-Za-z]{2,}|/(?:workspace|home|root|tmp)/", path.read_text(encoding="utf-8")):
            raise AssertionError("Unexpected private identifier in output " + path.name)
    print(json.dumps({key: meta[key] for key in ["current_snapshot_started_utc", "current_ledger_rows", "current_hunks", "mapping_method_counts", "recorded_footnote_removals", "replay_exact_for_all_changed_files", "ordinary_unmatched_hunks", "format_paired_hunks", "format_no_pair_hunks", "format_candidate_links", "format_payload_rows", "previous_format_links_still_distinguishing", "previous_format_links_no_longer_distinguishing"]}, indent=2))


if __name__ == "__main__":
    main()
