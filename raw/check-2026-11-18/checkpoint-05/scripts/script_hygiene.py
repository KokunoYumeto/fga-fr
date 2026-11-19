#!/usr/bin/env python3
"""Compile and inspect Python scripts without importing or executing them.

Only structural findings, filenames, line numbers, and hashes are emitted.
Replacement values, evidence strings, and source lines are never printed.
"""

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import tokenize
import warnings


SCRIPTS = Path(__file__).resolve().parent
LEDGERS = {"CORRECTIONS.tsv", "CHECK_RECORD.md", "CHECK_EVENTS.tsv", "progress.log"}
APPEND_MODES = {"a", "a+", "ab", "ab+", "a+b"}


def literal(node):
    try:
        return ast.literal_eval(node)
    except (ValueError, TypeError, SyntaxError):
        return None


def ancestors(tree):
    result = {}
    def visit(node, parents):
        result[id(node)] = parents
        for child in ast.iter_child_nodes(node):
            visit(child, parents + [node])
    visit(tree, [])
    return result


def context(node, parents):
    chain = parents[id(node)]
    functions = [item.name for item in chain if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))]
    return {"scope": functions[-1] if functions else "module",
            "enclosing_controls": [type(item).__name__ for item in chain
                                   if isinstance(item, (ast.If, ast.IfExp, ast.For, ast.AsyncFor, ast.While, ast.Try))]}


def raw_single_quote_locations(data):
    findings, fstrings = [], []
    def descriptor(value):
        index = 0
        while index < len(value) and value[index].lower() in "rubf":
            index += 1
        prefix = value[:index].lower()
        quote = value[index:index + 1]
        length = 3 if value[index:index + 3] == quote * 3 else 1
        return prefix, quote, length, index + length
    def inspect(value, start, owner_start, prefix, quote_length, body_start=0, body_end=None):
        for index in range(body_start, len(value) if body_end is None else body_end):
            if value[index] != "'":
                continue
            previous = index - 1
            while previous >= body_start and value[previous] == "\\":
                previous -= 1
            if (index - 1 - previous) % 2 != 1:
                continue
            before = value[:index]
            line = start[0] + before.count("\n")
            column = len(before.rsplit("\n", 1)[-1]) + (start[1] if "\n" not in before else 0) + 1
            findings.append({"token_line": owner_start[0], "token_column": owner_start[1] + 1,
                             "line": line, "column": column, "prefix": prefix,
                             "quote_kind": "triple-single" if quote_length == 3 else "single",
                             "interpretation": "token pattern only; retained backslash may be intentional"})
    for token in tokenize.tokenize(io.BytesIO(data).readline):
        if token.type == tokenize.STRING:
            prefix, quote, length, begin = descriptor(token.string)
            if "r" in prefix and quote == "'":
                inspect(token.string, token.start, token.start, prefix, length, begin, len(token.string) - length)
        elif token.type == getattr(tokenize, "FSTRING_START", -1):
            fstrings.append((*descriptor(token.string), token.start))
        elif token.type == getattr(tokenize, "FSTRING_MIDDLE", -1) and fstrings:
            prefix, quote, length, _, owner_start = fstrings[-1]
            if "r" in prefix and quote == "'":
                inspect(token.string, token.start, owner_start, prefix, length)
        elif token.type == getattr(tokenize, "FSTRING_END", -1) and fstrings:
            fstrings.pop()
    return findings


def inspect_script(data, name):
    result = {"file": name, "sha256": hashlib.sha256(data).hexdigest(), "compiled": False,
              "compile_errors": [], "warnings": [], "literal_noop_candidates": [],
              "direct_append_sites": [], "append_helper_calls": [], "raw_single_quote_escapes": []}
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            compile(data, name, "exec")
            tree = ast.parse(data, filename=name)
            result["compiled"] = True
        except SyntaxError as error:
            result["compile_errors"].append({"line": error.lineno, "message": error.msg})
            tree = None
    seen = set()
    for item in caught:
        key = (item.category.__name__, item.lineno, str(item.message))
        if key not in seen:
            result["warnings"].append({"category": key[0], "line": key[1], "message": key[2]})
            seen.add(key)
    if tree is None:
        return result
    result["raw_single_quote_escapes"] = raw_single_quote_locations(data)
    parents = ancestors(tree)
    aliases, modules = {}, set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "audit_utils":
            for alias in node.names:
                if alias.name == "*":
                    aliases.update({name: name for name in ["replace", "event", "record_page"]})
                elif alias.name in {"replace", "event", "record_page"}:
                    aliases[alias.asname or alias.name] = alias.name
        elif isinstance(node, ast.Import):
            modules.update(alias.asname or alias.name for alias in node.names if alias.name == "audit_utils")
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        helper = aliases.get(node.func.id) if isinstance(node.func, ast.Name) else None
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id in modules:
            helper = node.func.attr
        if helper in {"event", "record_page"}:
            result["append_helper_calls"].append(dict(line=node.lineno, helper=helper, **context(node, parents)))
        pair = None
        if helper == "replace" and len(node.args) >= 3:
            pair = node.args[1:3]
            kind = "shared replacement helper; ledger effects possible, not dead code"
        elif isinstance(node.func, ast.Attribute) and node.func.attr == "replace" and len(node.args) >= 2:
            pair = node.args[:2]
            kind = "method replacement; receiver type and side effects require review"
        if pair:
            old, new = map(literal, pair)
            if isinstance(old, (str, bytes)) and type(old) is type(new) and old == new:
                result["literal_noop_candidates"].append({"line": node.lineno, "kind": kind, "pattern": "equal literal arguments"})
            elif helper != "replace" and len(node.args) >= 3 and literal(node.args[2]) == 0:
                result["literal_noop_candidates"].append({"line": node.lineno, "kind": kind, "pattern": "literal zero replacement count"})
        mode = None
        path_expression = None
        if isinstance(node.func, ast.Name) and node.func.id == "open":
            mode = literal(node.args[1]) if len(node.args) > 1 else None
            path_expression = node.args[0] if node.args else None
        elif isinstance(node.func, ast.Attribute) and node.func.attr == "open":
            mode = literal(node.args[0]) if node.args else None
            path_expression = node.func.value
        for keyword in node.keywords:
            if keyword.arg == "mode":
                mode = literal(keyword.value)
        if isinstance(mode, str) and mode in APPEND_MODES and path_expression is not None:
            targets = sorted({item.value for item in ast.walk(path_expression)
                              if isinstance(item, ast.Constant) and isinstance(item.value, str) and item.value in LEDGERS})
            result["direct_append_sites"].append(dict(line=node.lineno, mode=mode,
                target=targets[0] if len(targets) == 1 else "dynamic or non-ledger path", **context(node, parents)))
    for key in ["literal_noop_candidates", "direct_append_sites", "append_helper_calls"]:
        result[key].sort(key=lambda item: item["line"])
    return result


def inspect_directory(root):
    before = sorted(path for path in root.rglob("*.py") if "__pycache__" not in path.parts)
    results, changing = [], []
    for path in before:
        first = path.stat()
        data = path.read_bytes()
        last = path.stat()
        name = path.relative_to(root).as_posix()
        if (first.st_size, first.st_mtime_ns) != (last.st_size, last.st_mtime_ns):
            changing.append(name)
        results.append(inspect_script(data, name))
    after = sorted(path for path in root.rglob("*.py") if "__pycache__" not in path.parts)
    summary = {"date_utc": datetime.now(timezone.utc).isoformat(), "python_scripts": len(results),
               "compiled": sum(item["compiled"] for item in results),
               "compile_errors": sum(len(item["compile_errors"]) for item in results),
               "warnings": sum(len(item["warnings"]) for item in results),
               "literal_noop_candidates": sum(len(item["literal_noop_candidates"]) for item in results),
               "raw_single_quote_escape_occurrences": sum(len(item["raw_single_quote_escapes"]) for item in results),
               "raw_single_quote_escape_tokens": sum(len({(hit["token_line"], hit["token_column"]) for hit in item["raw_single_quote_escapes"]}) for item in results),
               "scripts_with_raw_single_quote_escapes": sum(bool(item["raw_single_quote_escapes"]) for item in results),
               "scripts_with_append_helpers": sum(bool(item["append_helper_calls"]) for item in results),
               "scripts_with_direct_append_sites": sum(bool(item["direct_append_sites"]) for item in results),
               "script_set_changed_during_scan": before != after, "files_changed_while_read": changing,
               "scripts_executed_or_imported": 0}
    return {"summary": summary, "scripts": results,
            "limits": "Static call sites only. Earlier guards or exceptions can prevent execution; their absence is not a proof of idempotence. No replacement payload or edition content is inspected semantically."}


def selftest():
    source = (b'from audit_utils import event\n'
              b'raise RuntimeError("must never execute")\n'
              b'value = "fixture"\nvalue = value.replace("fixture", "fixture")\n'
              b'event("fixture", "fixture", "fixture", "fixture")\n'
              b'with open("fixture.tsv", "a") as stream: stream.write("fixture")\n'
              b'bad_escape = "\\q"\n')
    result = inspect_script(source, "synthetic.py")
    assert result["compiled"] and len(result["warnings"]) == 1
    assert len(result["literal_noop_candidates"]) == len(result["direct_append_sites"]) == len(result["append_helper_calls"]) == 1
    quote_fixture = (b"raw = r'fixture\\'suffix'\n" + b"triple = r" + b"'" * 3 + b"fixture\\'suffix" + b"'" * 3 + b"\n"
                     + b"plain = 'fixture\\'suffix'\n" + b'double = r"fixture\'suffix"\n'
                     + b"formatted = rf'fixture\\'suffix{1}'\n" + b"raw_bytes = rb'fixture\\'suffix'\n")
    quotes = inspect_script(quote_fixture, "synthetic_quotes.py")
    assert quotes["compiled"] and len(quotes["raw_single_quote_escapes"]) == 4
    assert {hit["quote_kind"] for hit in quotes["raw_single_quote_escapes"]} == {"single", "triple-single"}
    assert {hit["prefix"] for hit in quotes["raw_single_quote_escapes"]} == {"r", "rf", "rb"}
    print("PASS: synthetic compile warning, exact literal no-op, append mode, helper calls, and raw single-quote token patterns; fixture code was not executed.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=SCRIPTS)
    parser.add_argument("--report", type=Path, help="Optional JSON metadata report outside the scripts directory")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        selftest(); return
    root = args.root.resolve()
    if args.report and (args.report.resolve() == root or root in args.report.resolve().parents):
        parser.error("Keep the metadata report outside the scripts directory.")
    result = inspect_directory(root)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps(result["summary"], indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["summary"]["compile_errors"] or result["summary"]["warnings"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
