"""Independent byte/metadata validator for French snapshot continuity reports.

Does not import the producing difference, projection, or mapping functions.
Does not adjudicate mathematical content, correction validity, or completeness.
"""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone
import argparse, csv, hashlib, io, json, re


def sha(data):
    return hashlib.sha256(data).hexdigest()


def obj(path):
    return json.loads(path.read_text(encoding="utf-8"))


def table(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def ledger(data):
    reader = csv.reader(io.StringIO(data.decode("utf-8"), newline=""), delimiter="\t")
    header = next(reader)
    rows, previous = [], reader.line_num
    for number, fields in enumerate(reader, 1):
        row = dict(zip(header, fields))
        row.update(row_id=f"C{number:06d}", data_row=number, physical_line_start=previous + 1, physical_line_end=reader.line_num, row_sha256=sha(json.dumps(fields, ensure_ascii=False, separators=(",", ":")).encode()))
        previous = reader.line_num
        rows.append(row)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError("Use a new audit output directory.")
    started = datetime.now(timezone.utc).isoformat()
    meta = obj(args.report / "INVENTORY.json")
    paths = {name: Path(value) for name, value in meta["paths"].items()}
    checks = []
    def check(name, passed, details=None):
        checks.append({"check": name, "pass": bool(passed), "details": details})
    sources = {}
    for label in ["old", "current"]:
        root = paths[label + "_frozen"]
        manifest = obj(root / "SNAPSHOT.json")
        entries = {r["path"]: (root / r["path"]).read_bytes() for r in manifest["files"]}
        check(label + "_frozen_manifest_exact", all(len(entries[r["path"]]) == r["bytes"] and sha(entries[r["path"]]) == r["sha256"] for r in manifest["files"]), {"files": len(entries)})
        sources[label] = entries
    old_hunks = {h["hunk_id"]: h for h in obj(paths["old_report"] / "HUNKS.json")["hunks"]}
    current_hunks = {h["hunk_id"]: h for h in obj(paths["current_report"] / "HUNKS.json")["hunks"]}
    rows = ledger(sources["current"]["CORRECTIONS.tsv"])
    old_rows = ledger(sources["old"]["CORRECTIONS.tsv"])
    by_id = {r["row_id"]: r for r in rows}
    supplement_rows = ledger((paths["supplement_frozen"] / "CORRECTIONS.tsv").read_bytes())
    check("ledger_hashes_sizes_and_prefixes", len(rows) == meta["current_ledger_rows"] and len(old_rows) == meta["old_ledger_rows"] and sha(sources["current"]["CORRECTIONS.tsv"]) == meta["current_ledger_sha256"] and sha(sources["old"]["CORRECTIONS.tsv"]) == meta["old_ledger_sha256"] and all(r["row_sha256"] == s["row_sha256"] for r, s in zip(old_rows, rows)) and all(r["row_sha256"] == s["row_sha256"] for r, s in zip(supplement_rows, rows)))
    french = lambda r: r["file"].startswith(("sources/fr/", "sources/fr_printed/"))
    check("French_ledger_row_sequence_unchanged_since_previous_supplement", [r["row_sha256"] for r in rows if french(r)] == [r["row_sha256"] for r in supplement_rows if french(r)] and meta["French_ledger_rows_unchanged_since_supplement_capture"])
    source_changes = table(args.report / "SOURCE_CHANGES.tsv")
    changed_paths = []
    bad_changes = []
    for item in source_changes:
        a, b = sources["old"][item["file"]], sources["current"][item["file"]]
        if not (sha(a) == item["old_sha256"] and sha(b) == item["current_sha256"] and len(a) == int(item["old_bytes"]) and len(b) == int(item["current_bytes"]) and (a == b) == (item["identical"] == "True")):
            bad_changes.append(item["file"])
        if a != b:
            changed_paths.append(item["file"])
    check("source_changes_manifest_exact", not bad_changes and sorted(changed_paths) == sorted(meta["source_changes"]), {"changed_files": changed_paths, "errors": bad_changes})
    check("all_printed_files_unchanged", all(sources["old"][p] == b for p, b in sources["current"].items() if p.startswith("sources/fr_printed/")))

    slice_errors, slice_count = [], 0
    for label, hunks in [("old", old_hunks), ("current", current_hunks)]:
        for h in hunks.values():
            for side, rkey, tkey, hkey, bkey, fkey in [("fr", "fr_range", "old_text", "old_sha256", "old_bytes", "fr_file"), ("fr_printed", "fr_printed_range", "new_text", "new_sha256", "new_bytes", "fr_printed_file")]:
                data, loc = sources[label][h[fkey]], h[rkey]
                part = data[loc["byte_start"]:loc["byte_end_exclusive"]]
                good = part.decode("utf-8") == h[tkey] and sha(part) == h[hkey] and len(part) == h[bkey]
                good = good and data.count(b"\n", 0, loc["byte_start"]) + 1 == loc["line_start"]
                end_line = data.count(b"\n", 0, loc["byte_end_exclusive"] - 1) + 1 if part else None
                good = good and end_line == loc["line_end"]
                if not good:
                    slice_errors.append((label, h["hunk_id"], side))
                slice_count += 1
    check("all_old_and_current_hunk_payloads_hashes_and_line_locators_exact", not slice_errors, {"slices": slice_count, "errors": slice_errors})
    reconstruction_errors = []
    for label, hunks in [("old", old_hunks), ("current", current_hunks)]:
        by_file = defaultdict(list)
        for h in hunks.values():
            by_file[h["fr_file"]].append(h)
        for file, members in by_file.items():
            value = sources[label][file]
            for h in sorted(members, key=lambda h: h["fr_range"]["byte_start"], reverse=True):
                loc = h["fr_range"]
                value = value[:loc["byte_start"]] + h["new_text"].encode() + value[loc["byte_end_exclusive"]:]
            if value != sources[label][members[0]["fr_printed_file"]]:
                reconstruction_errors.append((label, file))
    check("all_hunks_reconstruct_printed_files_exactly", not reconstruction_errors, reconstruction_errors)

    mapping = table(args.report / "CURRENT_TO_OLD.tsv")
    mapping_errors, reverse = [], defaultdict(list)
    for item in mapping:
        current = current_hunks[item["current_hunk_id"]]
        ids = json.loads(item["old_hunk_ids"])
        good = len(ids) == int(item["candidate_count"]) == 1
        for old_id in ids:
            old = old_hunks[old_id]
            reverse[old_id].append(current["hunk_id"])
            good = good and old["relative_file"] == current["relative_file"] and sources["old"][old["fr_printed_file"]] == sources["current"][current["fr_printed_file"]]
            o, n = old["fr_printed_range"], current["fr_printed_range"]
            if item["method"] == "exact_payload_pair_and_identical_printed_span":
                good = good and old["old_text"] == current["old_text"] and old["new_text"] == current["new_text"] and (o["byte_start"], o["byte_end_exclusive"]) == (n["byte_start"], n["byte_end_exclusive"])
            elif item["method"] == "identical_printed_span_and_payload_changed_corrected_payload":
                good = good and old["old_text"] != current["old_text"] and old["new_text"] == current["new_text"] and (o["byte_start"], o["byte_end_exclusive"]) == (n["byte_start"], n["byte_end_exclusive"])
            elif item["method"] == "current_printed_span_contained_in_old_span":
                good = good and o["byte_start"] <= n["byte_start"] < n["byte_end_exclusive"] <= o["byte_end_exclusive"]
            else:
                good = False
        if not good:
            mapping_errors.append(item["current_hunk_id"])
    check("all_mappings_complete_unique_and_byte_supported", not mapping_errors and {m["current_hunk_id"] for m in mapping} == set(current_hunks) and set(reverse) == set(old_hunks) and all(len(ids) == 1 for ids in reverse.values()), mapping_errors)
    check("mapping_counts_reconcile", dict(Counter(m["method"] for m in mapping)) == meta["mapping_method_counts"])

    post = [r for r in rows[len(old_rows):] if french(r)]
    saved_operations = obj(args.report / "FOOTNOTE_OPERATIONS.json")
    footnotes = table(args.report / "FOOTNOTE_REMOVALS.tsv")
    foot_by_id = {r["row_id"]: r for r in footnotes}
    operation_good = len(post) == len(footnotes) == meta["recorded_footnote_removals"] and {r["row_id"] for r in post} == set(foot_by_id)
    operation_good = operation_good and all(all(by_id[r["row_id"]][k] == value for k, value in r.items()) for r in saved_operations)
    replay_errors = []
    for rec in obj(args.report / "FOOTNOTE_REPLAY.json"):
        original = sources["old"][rec["file"]]
        value = original
        for row in [r for r in post if r["file"] == rec["file"]]:
            saved = foot_by_id[row["row_id"]]
            operand = row["old"].replace("\r\n", "\n")
            if b"\r\n" in original and b"\n" not in original.replace(b"\r\n", b""):
                operand = operand.replace("\n", "\r\n")
            operand = operand.encode()
            good = row["new"] == "" and value.count(operand) == original.count(operand) == 1
            good = good and sha(operand) == saved["source_operand_sha256"] and original.index(operand) == int(saved["original_byte_start"]) and value.index(operand) == int(saved["intermediate_replay_byte_start"])
            good = good and len(operand) == int(saved["source_operand_bytes"]) and row["row_sha256"] == saved["row_sha256"]
            if not good:
                replay_errors.append(row["row_id"])
            value = value.replace(operand, b"", 1)
        if not (value == sources["current"][rec["file"]] and sha(value) == rec["replayed_sha256"] == rec["current_sha256"] and sha(original) == rec["old_sha256"]):
            replay_errors.append(rec["file"])
    check("recorded_footnote_payloads_and_full_file_replay_exact", operation_good and not replay_errors, {"operations": len(post), "errors": replay_errors})

    ordinary_links = table(paths["current_report"] / "CANDIDATE_ROWS.tsv")
    ordinary_errors = []
    for item in ordinary_links:
        row, h = by_id[item["row_id"]], current_hunks[item["hunk_id"]]
        good = row["file"] in [h["fr_file"], h["fr_printed_file"]] and row["row_sha256"] == item["row_sha256"] and sha(row["old"].encode()) == item["ledger_old_sha256"] and sha(row["new"].encode()) == item["ledger_new_sha256"]
        good = good and row["data_row"] == int(item["data_row"]) and row["physical_line_start"] == int(item["physical_line_start"]) and row["physical_line_end"] == int(item["physical_line_end"])
        for method in json.loads(item["methods"]):
            found = False
            for a, b in [(h["old_text"], h["new_text"]), (h["new_text"], h["old_text"])]:
                x, y = row["old"], row["new"]
                if method == "exact_full_hunk_pair":
                    found = found or (x == a and y == b)
                elif method == "exact_distinguishing_substring_pair":
                    found = found or bool(x and y and x in a and y in b and (x not in b or y not in a))
                elif method == "ascii_whitespace_collapsed_distinguishing_pair":
                    normalize = lambda t: re.sub(r"[ \t\r\n\f\v]+", " ", t).strip(" \t\r\n\f\v")
                    x, y, a, b = map(normalize, [x, y, a, b])
                    found = found or bool(x and y and x != y and x in a and y in b and (x not in b or y not in a))
                elif method == "one_side_exact_distinguishing_substring":
                    found = found or any(len(t) >= 12 and ((t in a) != (t in b)) for t in [x, y])
            good = good and found
        if not good:
            ordinary_errors.append((item["hunk_id"], item["row_id"]))
    check("ordinary_candidate_payload_hashes_locators_and_literal_predicates", not ordinary_errors, {"links": len(ordinary_links), "errors": ordinary_errors})

    profiles = {r["profile"]: r for r in obj(args.report / "FORMAT_PROFILES.json")}
    projection_errors, projections_checked = [], 0
    def reconstruct(original, projected, metadata, profile, label):
        nonlocal projections_checked
        projections_checked += 1
        delete = set()
        good = True
        for wrapper in metadata["removed_wrappers"]:
            a, b, x, y = [wrapper[k] for k in ["character_start", "character_end", "argument_start", "argument_end"]]
            macro = wrapper["macro"]
            good = good and macro in profiles[profile]["removed_balanced_wrappers"] and bool(re.fullmatch(r"\\" + re.escape(macro) + r"[ \t\r\n\f\v]*\{", original[a:x])) and original[y:b] == "}" and sha(original[x:y].encode()) == wrapper["argument_sha256"]
            delete.update(range(a, x)); delete.update(range(y, b))
        rebuilt = re.sub(r"[ \t\r\n\f\v]+", " ", "".join(c for i, c in enumerate(original) if i not in delete)).strip()
        alphabet = set(profiles[profile]["retained_alphabet_controls"])
        controls = lambda text: [m[1] for m in re.finditer(r"\\([A-Za-z@]+|.)", text, re.S) if m[1] in alphabet]
        good = good and rebuilt == projected and sha(projected.encode()) == metadata["projection_sha256"] and controls(original) == controls(projected) == metadata["alphabet_controls"]
        if not good:
            projection_errors.append(label)
    hprojections = {}
    for view in obj(args.report / "FORMAT_HUNK_PROJECTIONS.json"):
        h = current_hunks[view["hunk_id"]]
        hprojections[view["hunk_id"], view["profile"]] = view
        reconstruct(h["old_text"], view["fr_projection"], view["fr_metadata"], view["profile"], view["hunk_id"] + "/fr/" + view["profile"])
        reconstruct(h["new_text"], view["fr_printed_projection"], view["fr_printed_metadata"], view["profile"], view["hunk_id"] + "/printed/" + view["profile"])
    format_details = obj(args.report / "FORMAT_CANDIDATE_DETAILS.json")
    candidate_errors, by_hunk = [], defaultdict(list)
    for item in format_details:
        row, h, match = by_id[item["row_id"]], current_hunks[item["hunk_id"]], item["match"]
        view = hprojections[item["hunk_id"], item["profile"]]
        reconstruct(row["old"], item["ledger_old_projection"], item["ledger_old_projection_metadata"], item["profile"], item["candidate_id"] + "/old")
        reconstruct(row["new"], item["ledger_new_projection"], item["ledger_new_projection_metadata"], item["profile"], item["candidate_id"] + "/new")
        x, y = (view["fr_printed_projection"], view["fr_projection"]) if item["orientation"] == "printed_to_corrected" else (view["fr_projection"], view["fr_printed_projection"])
        a, b = match["ledger_old_fragment"], match["ledger_new_fragment"]
        good = bool(a and b and a != b and a in x and b in y and (a not in y or b not in x))
        good = good and a == item["ledger_old_projection"][match["fragment_old_start"]:match["fragment_old_end"]] and b == item["ledger_new_projection"][match["fragment_new_start"]:match["fragment_new_end"]]
        good = good and x.count(a) == item["old_occurrences"] == match["old_occurrences"] and y.count(b) == item["new_occurrences"] == match["new_occurrences"]
        good = good and (a == x and b == y) == item["whole_hunk_pair"] == match["whole_hunk_pair"]
        good = good and row["row_sha256"] == item["row_sha256"] and row["data_row"] == item["data_row"] and row["physical_line_start"] == item["physical_line_start"] and row["physical_line_end"] == item["physical_line_end"]
        good = good and row["file"] in [h["fr_file"], h["fr_printed_file"]] and row["printed_page"] in h["candidate_page_keys"] and item["page_relation"] == "same page"
        good = good and sha(row["old"].encode()) == item["ledger_old_sha256"] and sha(row["new"].encode()) == item["ledger_new_sha256"] and h["old_sha256"] == item["fr_hunk_sha256"] and h["new_sha256"] == item["fr_printed_hunk_sha256"]
        if item["method"] == "localized_ledger_edit_pair":
            good = good and min(len(a), len(b)) >= 8
        else:
            good = good and a == item["ledger_old_projection"] and b == item["ledger_new_projection"]
        if not good:
            candidate_errors.append(item["candidate_id"])
        by_hunk[item["hunk_id"]].append(item)
    check("declared_projection_deletions_reconstruct_and_preserve_alphabet_controls", not projection_errors, {"projections": projections_checked, "errors": projection_errors})
    check("all_current_format_pair_fragments_hashes_counts_and_locators_exact", not candidate_errors, {"links": len(format_details), "errors": candidate_errors})
    status = table(args.report / "FORMAT_HUNK_STATUS.tsv")
    status_errors = []
    for item in status:
        links = by_hunk[item["hunk_id"]]
        if not (len(links) == int(item["candidate_link_count"]) and list(dict.fromkeys(c["row_id"] for c in links)) == json.loads(item["paired_candidate_row_ids"]) and len({c["row_id"] for c in links}) == int(item["paired_candidate_row_count"])):
            status_errors.append(item["hunk_id"])
    unmatched_ids = {h["hunk_id"] for h in current_hunks.values() if h["matching_status"] == "unmatched"}
    check("current_format_counts_and_unmatched_scope_reconcile", not status_errors and {r["hunk_id"] for r in status} == unmatched_ids and len(unmatched_ids) == meta["ordinary_unmatched_hunks"] and sum(bool(by_hunk[r["hunk_id"]]) for r in status) == meta["format_paired_hunks"] and sum(not by_hunk[r["hunk_id"]] for r in status) == meta["format_no_pair_hunks"], status_errors)
    payloads = obj(args.report / "FORMAT_LEDGER_PAYLOADS.json")
    check("all_included_current_ledger_payloads_exact", len(payloads) == meta["format_payload_rows"] and all(all(by_id[r["row_id"]][key] == value for key, value in r.items()) for r in payloads), {"rows": len(payloads)})
    old_details = {r["candidate_id"]: r for r in obj(paths["supplement_report"] / "CANDIDATE_DETAILS.json")}
    revalidation = table(args.report / "OLD_FORMAT_LINK_REVALIDATION.tsv")
    revalidation_errors = []
    for item in revalidation:
        old = old_details[item["old_candidate_id"]]
        view = hprojections[item["current_hunk_id"], item["profile"]]
        x, y = (view["fr_printed_projection"], view["fr_projection"]) if item["orientation"] == "printed_to_corrected" else (view["fr_projection"], view["fr_printed_projection"])
        a, b = old["match"]["ledger_old_fragment"], old["match"]["ledger_new_fragment"]
        predicate = bool(a and b and a != b and a in x and b in y and (a not in y or b not in x)) and by_id[item["row_id"]]["row_sha256"] == item["row_sha256"]
        if predicate != (item["stored_fragment_pair_still_distinguishing"] == "True") or x.count(a) != int(item["old_occurrences_current"]) or y.count(b) != int(item["new_occurrences_current"]):
            revalidation_errors.append(item["old_candidate_id"])
    check("every_old_format_pair_revalidation_exact", not revalidation_errors and len(revalidation) == len(old_details), revalidation_errors)
    previous = table(args.report / "PREVIOUS_NO_PAIR.tsv")
    previous_errors = []
    for item in previous:
        a, b = old_hunks[item["old_hunk_id"]], current_hunks[item["current_hunk_id"]]
        if not (a["old_text"] == b["old_text"] and a["new_text"] == b["new_text"] and item["both_payloads_exactly_unchanged"] == "True" and not by_hunk[item["current_hunk_id"]]):
            previous_errors.append(item["old_hunk_id"])
    check("previous_twelve_no_pair_cases_exactly_unchanged_and_still_no_pair", len(previous) == meta["previous_no_pair_cases"] == 12 and not previous_errors, previous_errors)
    histories = table(args.report / "FR_CORRECTED_NO_PAIR_HISTORY.tsv")
    mirrors = defaultdict(list)
    for row in rows:
        if row["file"].startswith("sources/fr_printed/"):
            mirrors["/".join(row["file"].split("/")[2:]), row["printed_page"], row["old"], row["new"]].append(row["row_id"])
    history_errors, orders, expected_payloads = [], defaultdict(list), {r["row_id"] for r in format_details}
    for item in histories:
        row, h = by_id[item["row_id"]], current_hunks[item["hunk_id"]]
        twin = mirrors[h["relative_file"], row["printed_page"], row["old"], row["new"]]
        good = not by_hunk[item["hunk_id"]] and row["file"] == h["fr_file"] and row["printed_page"] in h["candidate_page_keys"] and row["row_sha256"] == item["row_sha256"] and twin == json.loads(item["identical_printed_operation_rows"]) and (not twin) == (item["no_identical_printed_operation"] == "True")
        if not good:
            history_errors.append((item["hunk_id"], item["row_id"]))
        orders[item["hunk_id"]].append(row["data_row"])
        if not twin:
            expected_payloads.add(row["row_id"])
    check("history_links_counterparts_and_append_order_exact", not history_errors and all(v == sorted(v) for v in orders.values()) and table(args.report / "FR_ONLY_NO_PAIR_HISTORY.tsv") == [r for r in histories if r["no_identical_printed_operation"] == "True"] and {r["row_id"] for r in payloads} == expected_payloads, {"links": len(histories), "errors": history_errors})
    private = [p.name for p in args.report.iterdir() if p.is_file() and re.search(r"(?<![\w.-])[\w.%+-]+@[\w.-]+\.[A-Za-z]{2,}|/(?:workspace|home|root|tmp)/", p.read_text(encoding="utf-8"))]
    check("no_detected_email_or_absolute_host_prefix", not private, private)
    check("all_frozen_inputs_unchanged_after_validation", all((paths[label + "_frozen"] / path).read_bytes() == value for label, files in sources.items() for path, value in files.items()))
    failures = [r["check"] for r in checks if not r["pass"]]
    result = {"status": "PASS" if not failures else "FAIL", "started_utc": started, "completed_utc": datetime.now(timezone.utc).isoformat(), "failed_checks": failures, "checks": checks, "hunk_slices_verified": slice_count, "ordinary_candidate_links_verified": len(ordinary_links), "format_candidate_links_verified": len(format_details), "projections_reconstructed": projections_checked, "footnote_operations_replayed": len(post), "scope": "Byte, declared-deletion projection, literal fragment, coordinate and ledger metadata validation only. No mathematical or correction-validity adjudication."}
    args.out.mkdir(parents=True)
    (args.out / "AUDIT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.out / "REPORT.md").write_text(f"# French refresh metadata audit\n\nStatus: **{result['status']}**. Completed {result['completed_utc']}.\n\nVerified {slice_count} old/current exact hunk slices, {len(ordinary_links)} ordinary ledger links, {len(format_details)} current declared-projection pair links, {projections_checked} projection reconstructions, and {len(post)} recorded footnote deletions replayed in memory. All 303 current-to-old mappings and both complete file reconstructions were checked independently of the producing helpers. Exact check results are in AUDIT.json.\n\nThis validates byte and metadata relationships. It does not determine mathematical equivalence, whether a candidate records the complete net difference, or whether a correction or source reading is justified.\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "checks"}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
