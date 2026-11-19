"""Small synthetic audit of translation page-fragment boundary handling.

Runs frozen helper copies against isolated synthetic files only. No production
source, correction ledger, or root record is opened by the tested functions.
"""
from pathlib import Path
from contextlib import redirect_stdout
from datetime import datetime, timezone
import argparse, ast, csv, hashlib, importlib, inspect, io, json, sys


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scripts", type=Path, default=Path("FGA_CHECK/scripts"))
    parser.add_argument("--baseline", type=Path, default=Path("tmp/frozen_build_inputs/en149_complete_193/scripts/translation_edits.py"))
    parser.add_argument("--isolated", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.isolated.exists() or args.out.exists():
        raise FileExistsError("Use new isolation and report directories.")
    started = datetime.now(timezone.utc).isoformat()
    captured = {name: (args.scripts / name).read_bytes() for name in ["translation_edits.py", "translation_math_lexer.py", "audit_utils.py"]}
    baseline_bytes = args.baseline.read_bytes()
    for name, data in captured.items():
        assert (args.scripts / name).read_bytes() == data
        target = args.isolated / "scripts" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    sys.path.insert(0, str((args.isolated / "scripts").resolve()))
    for name in ["translation_edits", "translation_math_lexer", "audit_utils"]:
        sys.modules.pop(name, None)
    helper = importlib.import_module("translation_edits")
    utility = importlib.import_module("audit_utils")
    lexer = importlib.import_module("translation_math_lexer")
    assert helper.ROOT == utility.ROOT == args.isolated.resolve()
    checks = []
    def check(name, passed, details=None):
        checks.append({"check": name, "pass": bool(passed), "details": details})
    def outcome(text, flag=None):
        try:
            data, spans = helper.math_ranges(text) if flag is None else helper.math_ranges(text, page_fragment=flag)
            return {"accepted": True, "payloads": [data[s["start"]:s["end"]].decode() for s in spans], "issues": []}
        except ValueError as error:
            issues = error.args[0]
            return {"accepted": False, "payloads": [], "issues": [i["code"] for i in issues]}

    allowed_codes = {"unclosed_environment_at_end_of_file", "unmatched_or_crossed_environment_end"}
    for environment in sorted(lexer.NONMATH_ENVIRONMENTS):
        for boundary, text in [("open", "\\begin{" + environment + "}\n\\item $x$\n"), ("close", "\\item $x$\n\\end{" + environment + "}")]:
            strict, fragment = outcome(text), outcome(text, True)
            check(environment + "_" + boundary + "_fragment", not strict["accepted"] and set(strict["issues"]).issubset(allowed_codes) and fragment["accepted"] and fragment["payloads"] == ["$x$"], {"strict": strict, "fragment": fragment})
    balanced = "é \\begin{enumerate}\\item $x$ \\[y\\]\\end{enumerate}"
    check("default_false_true_identical_on_balanced_input", helper.math_ranges(balanced) == helper.math_ranges(balanced, False) == helper.math_ranges(balanced, True))
    malformed = {
        "unclosed_dollar": "$x",
        "unmatched_display_closer": "x\\]",
        "unclosed_equation": "\\begin{equation}x",
        "crossed_math_environment": "\\begin{equation}x\\end{align}",
        "unclosed_math_brace": "$x_{1$",
        "inner_environment_without_math": "\\begin{aligned}x\\end{aligned}",
        "unclassified_environment": "\\begin{itemize}x\\end{itemize}",
    }
    for name, expression in malformed.items():
        text = "\\begin{enumerate}\n" + expression
        strict, fragment = outcome(text), outcome(text, True)
        check("malformed_" + name + "_still_rejected", not strict["accepted"] and not fragment["accepted"] and bool(set(fragment["issues"]) - allowed_codes), {"strict_issue_codes": strict["issues"], "fragment_issue_codes": fragment["issues"]})
    crossed = "\\begin{enumerate}\\begin{description}$x$\\end{enumerate}\\end{description}"
    check("raw_fragment_mode_requires_whole_file_guard", not outcome(crossed)["accepted"] and outcome(crossed, True)["accepted"])

    rel, unit = "sources/en/fr/synthetic.tex", "synthetic"
    source = "sources/fr/fr/synthetic.tex"
    printed_source = "sources/fr_printed/fr/synthetic.tex"
    ledger_path = args.isolated / "CORRECTIONS.tsv"
    def setup(fr, target):
        for path, text in [(source, fr), (printed_source, fr), (rel, target)]:
            destination = args.isolated / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(text, encoding="utf-8")
        with ledger_path.open("w", encoding="utf-8", newline="") as handle:
            csv.writer(handle, delimiter="\t").writerow(helper.FIELDS)
    def whole(a, b):
        return "\\src{1}\n\\begin{enumerate}\n\\item $" + a + "$\n\\src{2}\n\\item $" + b + "$\n\\end{enumerate}\n"
    def invoke(name, page, printed=False):
        with redirect_stdout(io.StringIO()) as captured_stdout:
            if name == "show_math":
                value = helper.show_math(rel, unit, page, printed=printed)
            else:
                value = helper.align_math(rel, "en", unit, page, [(0, 0)], (1, 1), printed=printed)
        return value, captured_stdout.getvalue()
    for printed in [False, True]:
        for page in [1, 2]:
            setup(whole("a", "b"), whole("u", "v"))
            before = (args.isolated / rel).read_bytes(), ledger_path.read_bytes()
            value, output = invoke("show_math", page, printed)
            check(f"show_valid_{'printed' if printed else 'corrected'}_list_boundary_page_{page}", output.count("outer math count 1") == 2 and before == ((args.isolated / rel).read_bytes(), ledger_path.read_bytes()))
            value, output = invoke("align_math", page, printed)
            with ledger_path.open(encoding="utf-8", newline="") as handle:
                ledger_data = list(csv.DictReader(handle, delimiter="\t"))
            expected = whole("a", "v") if page == 1 else whole("u", "b")
            check(f"align_valid_{'printed' if printed else 'corrected'}_list_boundary_page_{page}", value == 1 and (args.isolated / rel).read_text() == expected and len(ledger_data) == 1)

    valid = "\\src{1}\n$x$\n\\src{2}\n$y$\n"
    bad_wholes = {
        "actual_crossed_nonmath_environments_outside_page": "\\src{1}\n$x$\n\\src{2}\n" + crossed,
        "unclosed_math_outside_page": "\\src{1}\n$x$\n\\src{2}\n$y",
        "balanced_whole_math_crossing_page_boundary": "\\src{1}\n$x+\n\\src{2}\ny$\n",
    }
    for kind, bad in bad_wholes.items():
        for side in ["source", "target"]:
            for caller in ["show_math", "align_math"]:
                setup(bad if side == "source" else valid, bad if side == "target" else valid)
                before = {path: (args.isolated / path).read_bytes() for path in [source, printed_source, rel, "CORRECTIONS.tsv"]}
                caught = None
                try:
                    invoke(caller, 1)
                except ValueError as error:
                    caught = error.args[0]
                after = {path: (args.isolated / path).read_bytes() for path in before}
                code_list = [i["code"] for i in caught] if isinstance(caught, list) else []
                check(caller + "_rejects_" + side + "_" + kind, isinstance(caught, list) and bool(caught) and before == after, {"issue_codes": code_list, "isolated_files_unchanged": before == after})

    names = {"math_ranges", "show_math", "align_math"}
    old_defs = {n.name: n for n in ast.parse(baseline_bytes).body if isinstance(n, ast.FunctionDef) and n.name in names}
    new_defs = {n.name: n for n in ast.parse(captured["translation_edits.py"]).body if isinstance(n, ast.FunctionDef) and n.name in names}
    signatures = {name: {"before": ast.unparse(old_defs[name].args), "current": str(inspect.signature(getattr(helper, name)))} for name in sorted(names)}
    check("show_and_align_signatures_unchanged", all(ast.dump(old_defs[name].args) == ast.dump(new_defs[name].args) for name in ["show_math", "align_math"]))
    sig = inspect.signature(helper.math_ranges)
    check("math_ranges_keeps_one_argument_and_adds_optional_false_flag", list(sig.parameters) == ["text", "page_fragment"] and sig.parameters["page_fragment"].default is False and ast.unparse(old_defs["math_ranges"].args) == "text")
    callsites = []
    for path in sorted(args.scripts.glob("*.py")):
        if path.name in ["translation_edits.py", Path(__file__).name]:
            continue
        code = path.read_bytes()
        if not any(name.encode() in code for name in names):
            continue
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.func.id not in names:
                continue
            variable_args = any(isinstance(a, ast.Starred) for a in node.args) or any(k.arg is None for k in node.keywords)
            compatible = False
            if not variable_args:
                try:
                    inspect.signature(getattr(helper, node.func.id)).bind(*[None for _ in node.args], **{k.arg: None for k in node.keywords})
                    compatible = True
                except TypeError:
                    pass
            callsites.append({"file": path.as_posix(), "line": node.lineno, "function": node.func.id, "positional_count": len(node.args), "keywords": [k.arg for k in node.keywords], "variable_arguments": variable_args, "signature_compatible": compatible, "file_sha256": sha(code)})
    check("existing_saved_direct_call_signatures_compatible", bool(callsites) and all(r["signature_compatible"] for r in callsites), {"callsites": len(callsites), "unresolved": [r for r in callsites if not r["signature_compatible"]]})
    check("captured_live_helper_inputs_unchanged", all((args.scripts / name).read_bytes() == data for name, data in captured.items()))
    failures = [r["check"] for r in checks if not r["pass"]]
    report = {"status": "PASS" if not failures else "FAIL", "started_utc": started, "completed_utc": datetime.now(timezone.utc).isoformat(), "checks": checks, "failed_checks": failures, "signatures": signatures, "callsites": callsites, "input_hashes": {name: sha(data) for name, data in captured.items()}, "baseline_file": args.baseline.as_posix(), "baseline_sha256": sha(baseline_bytes), "isolated_fixture_root": args.isolated.as_posix(), "scope": "Synthetic lexical boundary and call-signature audit only. No translation, mathematical, scan, source or ledger review; no production sources or records modified.", "guard_note": "page_fragment=True alone also filters crossed nonmath environment ends. show_math validates each complete file strictly before its fragment; align_math validates both complete files strictly before fragment math extraction or writes. Raw fragment mode therefore depends on that whole-file guard."}
    args.out.mkdir(parents=True)
    (args.out / "AUDIT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    text = f"# Translation helper page-fragment audit\n\n**{report['status']}** — {report['completed_utc']}. {len(checks)} checks; {len(failures)} failures.\n\nSynthetic tests confirm open and close fragments for all six classified nonmath environments are accepted only with the fragment flag; mathematical delimiter, brace, environment and classification errors remain rejected. Real calls to the frozen helper copies against isolated synthetic files reject crossed whole-file nonmath environments and malformed math outside the selected page, for either source or target, without changing any isolated source or ledger. Math extending across a page boundary is still rejected at fragment extraction. Both open and close list-page cases work through show_math and align_math, including printed=True.\n\nThe two existing caller signatures are unchanged; math_ranges adds only page_fragment=False. All {len(callsites)} saved direct calls bind to the current signatures. Existing one-argument math_ranges calls retain strict behavior.\n\nGuard detail: page_fragment=True alone also suppresses crossed nonmath environment-end issues. show_math strictly validates each complete file before that file's fragment; align_math strictly validates both files before fragment math extraction or writes. The isolated full-file crossing tests exercise those actual guards.\n\nNo production source, ledger, or root record was changed, and no source text or scan was reviewed. Input hashes, exact issue codes, signatures and caller locations are in AUDIT.json.\n"
    (args.out / "REPORT.md").write_text(text, encoding="utf-8")
    print(json.dumps({key: report[key] for key in ["status", "completed_utc", "failed_checks", "signatures", "input_hashes"]} | {"checks": len(checks), "saved_direct_calls": len(callsites)}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
