"""Synthetic whole-file/page-selection audit; never opens production sources."""
from pathlib import Path
from contextlib import redirect_stdout
from datetime import datetime, timezone
import argparse, ast, csv, hashlib, importlib, importlib.util, inspect, io, json, sys


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scripts", type=Path, default=Path("FGA_CHECK/scripts"))
    parser.add_argument("--baseline", type=Path, default=Path("tmp/translation_page_fragment_audit_20261119/scripts/translation_edits.py"))
    parser.add_argument("--isolated", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.isolated.exists() or args.out.exists():
        raise FileExistsError("Use new isolation and report directories.")
    started = datetime.now(timezone.utc).isoformat()
    names = ["translation_edits.py", "translation_math_lexer.py", "audit_utils.py"]
    frozen = {name: (args.scripts / name).read_bytes() for name in names}
    old_bytes = args.baseline.read_bytes()
    for name, data in frozen.items():
        assert (args.scripts / name).read_bytes() == data
        target = args.isolated / "scripts" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    old_path = args.isolated / "scripts/baseline_translation_edits.py"
    old_path.write_bytes(old_bytes)
    sys.path.insert(0, str((args.isolated / "scripts").resolve()))
    for name in ["translation_edits", "translation_math_lexer", "audit_utils"]:
        sys.modules.pop(name, None)
    current = importlib.import_module("translation_edits")
    utility = importlib.import_module("audit_utils")
    spec = importlib.util.spec_from_file_location("baseline_translation_edits", old_path)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    assert current.ROOT == old.ROOT == utility.ROOT == args.isolated.resolve()
    checks = []
    def check(name, good, details=None):
        checks.append({"check": name, "pass": bool(good), "details": details})
    rel, unit = "sources/en/fr/synthetic.tex", "synthetic"
    fr, printed = "sources/fr/fr/synthetic.tex", "sources/fr_printed/fr/synthetic.tex"
    ledger_path = args.isolated / "CORRECTIONS.tsv"
    def setup(source, target=None, literal=None, crlf=False):
        for path, text in [(fr, source), (rel, target if target is not None else source), (printed, literal if literal is not None else source)]:
            p = args.isolated / path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((text.replace("\n", "\r\n") if crlf else text).encode())
        with ledger_path.open("w", encoding="utf-8", newline="") as handle:
            csv.writer(handle, delimiter="\t").writerow(current.FIELDS)
    def files():
        return {p: (args.isolated / p).read_bytes() for p in [fr, printed, rel, "CORRECTIONS.tsv"]}
    def invoke(module, caller, page, literal=False):
        output = io.StringIO()
        with redirect_stdout(output):
            if caller == "show_math":
                value = module.show_math(rel, unit, page, printed=literal)
            else:
                value = module.align_math(rel, "en", unit, page, [(0, 0)], (1, 1), printed=literal)
        return value, output.getvalue()
    def rejected(function):
        before, exception = files(), None
        try:
            function()
        except ValueError as error:
            exception = error.args[0]
        return exception is not None and before == files(), exception
    def locators(result):
        text, lo, hi, data, spans = result
        return {"text": text, "lo": lo, "hi": hi, "data": data,
                "spans": [{"offsets": [s[k] for k in ["start", "end", "inner_start", "inner_end"]],
                           "payload": data[s["start"]:s["end"]],
                           "inner_payload": data[s["inner_start"]:s["inner_end"]],
                           "source_line": lo + data[:s["start"]].count(b"\n")} for s in spans]}
    def old_page(path, page):
        text, lo, hi = old.page_text(path, page)
        data, spans = old.math_ranges(text, page_fragment=True)
        return text, lo, hi, data, spans

    prefix = "Préface Ω 漢 🙂\n$z_0$\n"
    def document(a, b, mode="balanced"):
        if mode == "balanced":
            body = "\\src{1}\né \\fquote{mot} $" + a + "$\n\\src{2}\n漢 \\begin{enumerate}\\item $" + b + "$\\end{enumerate}\n"
        elif mode == "prose_group":
            body = "\\src{1}\né \\fquote{début $" + a + "$\n\\src{2}\n漢 $" + b + "$ fin}\n"
        elif mode == "list":
            body = "\\src{1}\n\\begin{enumerate}\\item $" + a + "$\n\\src{2}\n\\item $" + b + "$\\end{enumerate}\n"
        else:
            body = "\\src{1}\n\\fquote{é {\\begin{enumerate}\\item $" + a + "$\n\\src{2}\n漢 \\item $" + b + "$\\end{enumerate}} fin}\n"
        return prefix + body

    for mode in ["prose_group", "list", "nested_group_and_list"]:
        for crlf in [False, True]:
            setup(document("α", "β", mode), crlf=crlf)
            full_text = utility.read(rel)
            full_data, full_spans = current.math_ranges(full_text)
            for page, expected in [(1, "$α$"), (2, "$β$")]:
                result = current.page_math_ranges(rel, page)
                text, lo, hi, data, spans = result
                ptext, plo, phi = utility.page_text(rel, page)
                start = full_text.index("\\src{" + str(page) + "}")
                byte_start = len(full_text[:start].encode())
                exact = [s for s in full_spans if full_data[s["start"]:s["end"]].decode() == expected]
                good = text == ptext and (lo, hi) == (plo, phi) and data == text.encode() and len(spans) == len(exact) == 1
                good = good and all(spans[0][k] + byte_start == exact[0][k] for k in ["start", "end", "inner_start", "inner_end"])
                good = good and data[spans[0]["start"]:spans[0]["end"]].decode() == expected and byte_start != start
                check(f"{mode}_{'CRLF' if crlf else 'LF'}_page_{page}_exact_UTF8_offsets", good)
    for crlf in [False, True]:
        setup(document("α", "β"), crlf=crlf)
        for page in [1, 2]:
            check(f"balanced_{'CRLF' if crlf else 'LF'}_page_{page}_baseline_payloads_and_locators", locators(current.page_math_ranges(rel, page)) == locators(old_page(rel, page)))
    setup(prefix + "\\src{1}\n\\[x+\\text{é $y$}\\]\n\\src{2}\n$z$\n")
    result = current.page_math_ranges(rel, 1)
    check("nested_math_keeps_one_outer_span_and_exact_baseline_payload", len(result[4]) == 1 and locators(result) == locators(old_page(rel, 1)))
    setup(prefix + "\\src{1}$a$\\src{2}$b$")
    check("half_open_page_edges_exclude_adjacent_complete_formula", [current.page_math_ranges(rel, p)[3][s["start"]:s["end"]].decode() for p in [1, 2] for s in current.page_math_ranges(rel, p)[4]] == ["$a$", "$b$"])

    for literal in [False, True]:
        for page in [1, 2]:
            for caller in ["show_math", "align_math"]:
                a, b, p = document("a", "b"), document("u", "v"), document("p", "q")
                setup(a, b, p, crlf=True)
                before = invoke(old, caller, page, literal), files()
                setup(a, b, p, crlf=True)
                after = invoke(current, caller, page, literal), files()
                check(f"{caller}_balanced_page_{page}_{'printed' if literal else 'corrected'}_byte_identical_baseline", before == after)
            setup(document("a", "b", "nested_group_and_list"), document("u", "v", "nested_group_and_list"), document("p", "q", "nested_group_and_list"), crlf=True)
            initial = files()
            value, output = invoke(current, "show_math", page, literal)
            chosen = ("p" if page == 1 else "q") if literal else ("a" if page == 1 else "b")
            check(f"show_unbalanced_prose_page_{page}_{'printed' if literal else 'corrected'}", output.count("outer math count 1") == 2 and repr("$" + chosen + "$") in output and files() == initial)
            value, output = invoke(current, "align_math", page, literal)
            expected = document(chosen if page == 1 else "u", chosen if page == 2 else "v", "nested_group_and_list").replace("\n", "\r\n").encode()
            with ledger_path.open(encoding="utf-8", newline="") as handle:
                written = list(csv.DictReader(handle, delimiter="\t"))
            check(f"align_unbalanced_prose_page_{page}_{'printed' if literal else 'corrected'}", value == 1 and (args.isolated / rel).read_bytes() == expected and len(written) == 1 and ("Literal French" if literal else "Corrected French") in written[0]["evidence"])

    crossing = {
        "inline": "\\src{1}\n$x+\n\\src{2}\ny$\n",
        "display": "\\src{1}\n\\[x+\n\\src{2}\ny\\]\n",
        "environment": "\\src{1}\n\\begin{equation}x+\n\\src{2}\ny\\end{equation}\n",
    }
    for kind, text in crossing.items():
        setup(text)
        check(kind + "_crossing_file_is_otherwise_lexically_balanced", bool(current.math_ranges(utility.read(rel))[1]))
        for page in [1, 2]:
            good, error = rejected(lambda: current.page_math_ranges(rel, page))
            check(f"{kind}_crossing_page_{page}_rejected_without_writes", good and error == "A mathematical expression crosses the printed-page boundary")
    clean = "\\src{1}\n$x$\n\\src{2}\n$y$\n"
    malformed = {
        "unclosed_prose_brace": clean + "\\fquote{oops",
        "unclosed_math": clean + "$z",
        "unmatched_math_closer": clean + "\\]",
        "crossed_nonmath_environments": clean + "\\begin{enumerate}\\begin{description}x\\end{enumerate}\\end{description}",
    }
    for kind, text in malformed.items():
        setup(text)
        good, error = rejected(lambda: current.page_math_ranges(rel, 1))
        check("helper_rejects_complete_file_" + kind + "_outside_selected_page", good and isinstance(error, list), [i["code"] for i in error] if isinstance(error, list) else error)
    for kind, bad in [("crossing_formula", crossing["inline"]), ("malformed_complete_file", malformed["unclosed_prose_brace"]), ("crossed_nonmath_environments", malformed["crossed_nonmath_environments"])]:
        for side in ["source", "target", "printed_source"]:
            for caller in ["show_math", "align_math"]:
                setup(bad if side == "source" else clean, bad if side == "target" else clean, bad if side == "printed_source" else clean)
                good, error = rejected(lambda: invoke(current, caller, 1, side == "printed_source"))
                check(caller + "_rejects_" + side + "_" + kind + "_without_writes", good)

    public = ["math_ranges", "show_math", "align_math"]
    old_ast = {n.name: n for n in ast.parse(old_bytes).body if isinstance(n, ast.FunctionDef)}
    new_ast = {n.name: n for n in ast.parse(frozen["translation_edits.py"]).body if isinstance(n, ast.FunctionDef)}
    check("previous_three_public_signatures_unchanged", all(inspect.signature(getattr(old, n)) == inspect.signature(getattr(current, n)) for n in public))
    check("math_ranges_implementation_AST_unchanged", ast.dump(old_ast["math_ranges"]) == ast.dump(new_ast["math_ranges"]))
    callsites = []
    for path in sorted(args.scripts.glob("*.py")):
        if path.name.startswith("audit_") or path.name == "translation_edits.py":
            continue
        data = path.read_bytes()
        if not any(n.encode() in data for n in public + ["page_math_ranges"]):
            continue
        for node in ast.walk(ast.parse(data)):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in public + ["page_math_ranges"]:
                compatible = False
                if not any(isinstance(v, ast.Starred) for v in node.args) and not any(k.arg is None for k in node.keywords):
                    try:
                        inspect.signature(getattr(current, node.func.id)).bind(*[None for _ in node.args], **{k.arg: None for k in node.keywords})
                        compatible = True
                    except TypeError:
                        pass
                callsites.append({"file": path.as_posix(), "line": node.lineno, "function": node.func.id, "compatible": compatible, "file_sha256": sha(data)})
    check("saved_production_direct_call_signatures_compatible", bool(callsites) and all(c["compatible"] for c in callsites), {"callsites": len(callsites)})
    check("live_helper_inputs_unchanged_during_audit", all((args.scripts / name).read_bytes() == value for name, value in frozen.items()))
    failures = [r["check"] for r in checks if not r["pass"]]
    result = {"status": "PASS" if not failures else "FAIL", "started_utc": started, "completed_utc": datetime.now(timezone.utc).isoformat(), "checks": checks, "failed_checks": failures, "input_hashes": {name: sha(data) for name, data in frozen.items()}, "baseline": args.baseline.as_posix(), "baseline_sha256": sha(old_bytes), "isolated_fixtures": args.isolated.as_posix(), "signatures": {n: str(inspect.signature(getattr(current, n))) for n in public + ["page_math_ranges"]}, "callsites": callsites, "scope": "Only synthetic files and helper code. Four page-relative byte offsets, exact payloads, normalized source lines, strict rejection and API compatibility; no source text, ledger, translation, mathematics or scan review."}
    args.out.mkdir(parents=True)
    (args.out / "AUDIT.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (args.out / "REPORT.md").write_text(f"# Whole-file page-math selection audit\n\n**{result['status']}** — {result['completed_utc']}. {len(checks)} checks; {len(failures)} failures.\n\nOpen and close prose groups, nested groups, and lists spanning page markers work with UTF-8 prefixes/content and either LF or normalized CRLF input. All four shifted byte offsets, exact outer/inner payloads, and source-line locators agree with the strict whole-file spans.\n\nOn already balanced pages, payloads and locators match the previous helper exactly; show_math output and align_math source/ledger bytes are identical in isolated runs, including printed=True. Current show_math/align_math also work on the newly supported unbalanced prose fragments.\n\nInline, display-delimited and equation-environment formulas crossing either selected-page edge are rejected without writes. Malformed complete files are rejected even when the defect lies outside the selected page. Actual caller tests cover source, target, and printed-source failures.\n\nThe previous three public signatures and the math_ranges implementation are unchanged. All {len(callsites)} saved production direct calls remain signature-compatible. Whole-file span metadata identifiers retain whole-file scope; the comparison concerns the four documented page-relative byte offsets and line/payload locators.\n\nNo production source, ledger or root record was modified or reviewed. Audit details and frozen helper hashes are in AUDIT.json.\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "completed_utc": result["completed_utc"], "checks": len(checks), "failed_checks": failures, "saved_direct_calls": len(callsites), "input_hashes": result["input_hashes"]}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
