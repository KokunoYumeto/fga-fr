#!/usr/bin/env python3
"""Deterministic, read-only TeX span inventories and literal comparisons.

This is a lexical tool, not TeX execution or semantic verification. Ordinary
commands write only to stdout/stderr. Selftests use in-memory synthetic text.
"""

import argparse
from bisect import bisect_right
from collections import defaultdict
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import sys


MATH_ENVIRONMENTS = set("math displaymath equation equation* align align* alignat alignat* flalign flalign* gather gather* multline multline* eqnarray eqnarray* aligned alignedat gathered split array matrix pmatrix bmatrix Bmatrix vmatrix Vmatrix smallmatrix cases dcases".split())
VERBATIM_ENVIRONMENTS = set("verbatim verbatim* Verbatim BVerbatim LVerbatim SaveVerbatim lstlisting minted comment filecontents filecontents*".split())
TEXT_ARGUMENTS = {"\\" + name for name in "text textrm textup textnormal textsf texttt textbf textit textsl textsc mbox hbox vbox operatorname label tag ref eqref".split()}
FONT_WRAPPERS = {r"\symup", r"\mathrm"}
OPENERS = {"$": ("dollar", "$"), "$$": ("display_dollar", "$$"),
           r"\(": ("parentheses", r"\)"), r"\[": ("brackets", r"\]")}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def command_end(text, start):
    end = start + 1
    if end < len(text) and (text[end].isalpha() or text[end] == "@"):
        while end < len(text) and (text[end].isalpha() or text[end] == "@"):
            end += 1
    elif end < len(text):
        end += 1
    return end


def skip_space_comments(text, start):
    while start < len(text):
        if text[start].isspace():
            start += 1
        elif text[start] == "%":
            end = text.find("\n", start)
            start = len(text) if end < 0 else end + 1
        else:
            break
    return start


def group_at(text, start):
    """Return an exclusive end for a balanced braced argument, or None."""
    if start >= len(text) or text[start] != "{":
        return None
    depth, position = 1, start + 1
    while position < len(text):
        char = text[position]
        if char == "\\":
            position = command_end(text, position)
            continue
        if char == "%":
            end = text.find("\n", position)
            position = len(text) if end < 0 else end + 1
            continue
        depth += (char == "{") - (char == "}")
        position += 1
        if depth == 0:
            return position
    return None


def lex(text, structural=True, protect_text=False):
    tokens, issues = [], []
    position = 0

    def add(kind, value, start, end):
        tokens.append({"kind": kind, "value": value, "start": start, "end": end})

    while position < len(text):
        start, char = position, text[position]
        if char == "%":
            end = text.find("\n", start)
            position = len(text) if end < 0 else end
            add("comment", text[start:position], start, position)
            continue
        if char.isspace():
            while position < len(text) and text[position].isspace():
                position += 1
            add("space", text[start:position], start, position)
            continue
        if char == "\\":
            position = command_end(text, start)
            value = text[start:position]
            if value == r"\verb":
                if position < len(text) and text[position] == "*":
                    position += 1
                delimiter = text[position:position + 1]
                end = text.find(delimiter, position + 1) if delimiter and not delimiter.isspace() else -1
                newline = text.find("\n", position)
                if end < 0 or (newline >= 0 and end > newline):
                    issues.append({"code": "unclosed_verbatim_command", "offset": start})
                    position = len(text) if newline < 0 else newline
                else:
                    position = end + 1
                add("opaque", text[start:position], start, position)
                continue
            argument = skip_space_comments(text, position)
            if protect_text and value in TEXT_ARGUMENTS and argument < len(text) and text[argument] == "*":
                argument = skip_space_comments(text, argument + 1)
            end = group_at(text, argument)
            if value in (r"\begin", r"\end") and end is not None:
                name = text[argument + 1:end - 1].strip()
                if value == r"\begin" and name in VERBATIM_ENVIRONMENTS:
                    match = re.search(r"\\end\s*\{\s*" + re.escape(name) + r"\s*\}", text[end:])
                    if match:
                        position = end + match.end()
                    else:
                        issues.append({"code": "unclosed_verbatim_environment", "offset": start})
                        position = len(text)
                    add("opaque", text[start:position], start, position)
                    continue
                if structural:
                    position = end
                    add("begin" if value == r"\begin" else "end", name, start, end)
                    continue
            if structural and value == r"\src" and end is not None:
                position = end
                page = text[argument + 1:end - 1].strip()
                if not re.fullmatch(r"\d+", page):
                    issues.append({"code": "nonliteral_source_marker", "offset": start})
                add("src", page, start, end)
                continue
            if end is not None and (value in (r"\url", r"\nolinkurl", r"\path") or protect_text and value in TEXT_ARGUMENTS):
                position = end
                add("opaque", text[start:position], start, position)
                continue
            add("command", value, start, position)
            continue
        position += 1
        if char == "$" and position < len(text) and text[position] == "$":
            position += 1
        add("symbol", text[start:position], start, position)
    return tokens, issues


def parse_tex(text, extra_environments=()):
    tokens, issues = lex(text)
    line_starts = [0] + [match.end() for match in re.finditer("\n", text)]
    markers, spans, braces, environments = [], [], [], []
    current, page = None, None
    math_environments = MATH_ENVIRONMENTS | set(extra_environments)

    def line(offset):
        return bisect_right(line_starts, offset)

    def open_span(token, kind, mode, content_start=None, closer=None):
        return {"kind": kind, "mode": mode, "start": token["start"],
                "content_start": token["end"] if content_start is None else content_start,
                "brace_depth": len(braces), "environment_depth": len(environments),
                "page_at_start": page, "closer": closer}

    def finish(frame, end, content_end, closed):
        touched = [frame["page_at_start"]]
        for marker in markers:
            if frame["start"] < marker["start_offset"] < end and marker["printed_page"] not in touched:
                touched.append(marker["printed_page"])
        spans.append({"span_id": len(spans) + 1, "kind": frame["kind"],
                      "start_offset": frame["start"], "end_offset": end,
                      "content_start_offset": frame["content_start"], "content_end_offset": content_end,
                      "start_line": line(frame["start"]), "end_line": line(max(frame["start"], end - 1)),
                      "page_at_start": frame["page_at_start"], "pages_touched": touched,
                      "crosses_source_marker": len(touched) > 1,
                      "closed": closed, "raw_tex": text[frame["start"]:end]})

    for index, token in enumerate(tokens):
        kind, value = token["kind"], token["value"]
        if kind == "src":
            if value.isdigit():
                page = int(value)
                markers.append({"printed_page": page, "raw_marker": text[token["start"]:token["end"]],
                                "start_offset": token["start"], "end_offset": token["end"], "line": line(token["start"])})
            continue
        if kind in {"space", "comment", "opaque"}:
            continue
        if value == "{" and kind == "symbol":
            braces.append(token["start"])
            continue
        if value == "}" and kind == "symbol":
            if braces:
                braces.pop()
            else:
                issues.append({"code": "unmatched_closing_brace", "offset": token["start"]})
            if current and current["mode"] == "group" and len(braces) == current["brace_depth"]:
                finish(current, token["end"], token["start"], True)
                current = None
            continue
        if kind == "begin":
            environments.append((value, token["start"]))
            if current is None and value in math_environments:
                current = open_span(token, "environment:" + value, "environment", closer=value)
            continue
        if kind == "end":
            if not environments or environments[-1][0] != value:
                issues.append({"code": "environment_nesting_mismatch", "offset": token["start"]})
            matching = next((i for i in range(len(environments) - 1, -1, -1) if environments[i][0] == value), None)
            if matching is not None:
                del environments[matching:]
            if current and current["mode"] == "environment" and value == current["closer"] and len(environments) < current["environment_depth"]:
                if len(braces) != current["brace_depth"]:
                    issues.append({"code": "math_environment_brace_depth_mismatch", "offset": token["start"]})
                finish(current, token["end"], token["start"], True)
                current = None
            continue
        if current is None and value == r"\ensuremath":
            following = next((t for t in tokens[index + 1:] if t["kind"] not in {"space", "comment"}), None)
            if following and following["kind"] == "symbol" and following["value"] == "{":
                current = open_span(token, "ensuremath", "group", content_start=following["end"])
            else:
                issues.append({"code": "unbraced_ensuremath_not_expanded", "offset": token["start"]})
            continue
        at_boundary = current and len(braces) == current["brace_depth"] and len(environments) == current["environment_depth"]
        if current and current["mode"] == "delimiter" and value == current["closer"] and at_boundary:
            finish(current, token["end"], token["start"], True)
            current = None
        elif current is None and value in OPENERS:
            span_kind, closer = OPENERS[value]
            current = open_span(token, span_kind, "delimiter", closer=closer)
        elif value in (r"\)", r"\]") and (current is None or at_boundary):
            issues.append({"code": "unmatched_math_closing_delimiter", "offset": token["start"]})
    if current:
        issues.append({"code": "unclosed_math_span", "offset": current["start"]})
        finish(current, len(text), len(text), False)
    issues.extend({"code": "unclosed_brace", "offset": offset} for offset in braces)
    issues.extend({"code": "unclosed_environment", "offset": offset} for _, offset in environments)
    for issue in issues:
        issue["line"] = line(issue["offset"])
    for span in spans:
        span["parser_issue_count"] = sum(span["start_offset"] <= item["offset"] < span["end_offset"] for item in issues)
    return {"markers": markers, "spans": spans, "diagnostics": sorted(issues, key=lambda item: (item["offset"], item["code"]))}


def normalize(raw, mode="none"):
    if mode == "none":
        return {"mode": mode, "text": raw, "tokens": None, "operations": [], "cautions": []}
    tokens, lexical_issues = lex(raw, structural=False, protect_text=True)
    kept, operations, cautions = [], [], [item["code"] for item in lexical_issues]
    for token in tokens:
        kind, value = token["kind"], token["value"]
        operation = None
        if kind in {"space", "comment"}:
            operation = "ignored_math_whitespace" if kind == "space" else "ignored_TeX_comment"
        elif kind == "command" and value in {r"\left", r"\right"}:
            operation = "removed_delimiter_sizing_command"
        elif kind == "command" and value in FONT_WRAPPERS:
            argument = skip_space_comments(raw, token["end"])
            if group_at(raw, argument) is not None:
                operation = "removed_font_control_word_retained_argument_braces"
            else:
                cautions.append("unbraced_font_command_retained")
        if operation:
            entry = {"operation": operation, "start_offset_in_span": token["start"], "end_offset_in_span": token["end"]}
            if kind == "command":
                entry["command"] = value
            operations.append(entry)
        else:
            kept.append(value)
    # A token separator is retained where concatenation would create a different
    # control word. Comparisons use the token array, not this display string.
    display = ""
    previous = ""
    for value in kept:
        if re.fullmatch(r"\\[^\W\d_@]+|\\[A-Za-z@]+", previous) and value and (value[0].isalpha() or value[0] == "@"):
            display += " "
        display += value
        previous = value
    return {"mode": mode, "text": display, "tokens": kept, "operations": operations,
            "cautions": sorted(set(cautions))}


def line_range(value, text):
    total = max(1, len(text.splitlines()))
    if value is None:
        return (1, total)
    match = re.fullmatch(r"(\d*):(\d*)", value)
    if not match or not any(match.groups()):
        raise ValueError("Line ranges use START:END, START:, or :END.")
    start, end = int(match[1] or 1), int(match[2] or total)
    if start < 1 or end < start:
        raise ValueError("Line ranges must be positive and ordered.")
    return (start, end)


def inventory(text, label, args, range_value=None):
    parsed = parse_tex(text, args.math_env)
    first, last = line_range(range_value, text)
    selected = []
    for span in parsed["spans"]:
        if span["end_line"] < first or span["start_line"] > last or args.page and not set(args.page).intersection(span["pages_touched"]):
            continue
        span["range_partial"] = span["start_line"] < first or span["end_line"] > last
        span["normalization"] = normalize(span["raw_tex"], args.normalize)
        sequence = span["normalization"]["tokens"] if args.normalize != "none" else span["raw_tex"]
        span["comparison_digest"] = sha(json.dumps(sequence, ensure_ascii=False, separators=(",", ":")).encode())
        selected.append(span)
    markers = [marker for marker in parsed["markers"] if first <= marker["line"] <= last and (not args.page or marker["printed_page"] in args.page)]
    return {"source": label, "source_utf8_sha256": sha(text.encode()), "requested_lines": [first, last],
            "selected_pages": args.page, "normalization": args.normalize, "markers": markers,
            "spans": selected, "file_parser_diagnostics": parsed["diagnostics"],
            "review_certified": False}


def comparison(left, right, grouping):
    groups = defaultdict(lambda: [[], []])
    if grouping == "range":
        groups["requested ranges"] = [left["spans"], right["spans"]]
    else:
        for side, document in enumerate((left, right)):
            for marker in document["markers"]:
                groups[str(marker["printed_page"])]
            for span in document["spans"]:
                for page in span["pages_touched"]:
                    if document["selected_pages"] and page not in document["selected_pages"]:
                        continue
                    groups["unmarked" if page is None else str(page)][side].append(span)
    rows = []
    for page in sorted(groups, key=lambda value: (not value.isdigit(), int(value) if value.isdigit() else value)):
        a, b = groups[page]
        changes = []
        for tag, i, j, k, l in difflib.SequenceMatcher(None, [s["comparison_digest"] for s in a], [s["comparison_digest"] for s in b], autojunk=False).get_opcodes():
            if tag != "equal":
                changes.append({"operation": tag, "left_span_ids": [s["span_id"] for s in a[i:j]],
                                "right_span_ids": [s["span_id"] for s in b[k:l]]})
        rows.append({"group": page, "left_span_count": len(a), "right_span_count": len(b),
                     "sequence_comparison": "different" if changes else "identical selected representation",
                     "changes": changes})
    return {"grouping": grouping, "left": left, "right": right, "groups": rows,
            "scope": "Ordered lexical span comparison only; equality is not semantic equivalence or review completion.",
            "review_certified": False}


def unified_source_diff(left, right, left_label, right_label, left_range=None, right_range=None, context=3):
    a, b = line_range(left_range, left), line_range(right_range, right)
    lines = difflib.unified_diff(left.splitlines(keepends=True)[a[0] - 1:a[1]],
                                right.splitlines(keepends=True)[b[0] - 1:b[1]],
                                fromfile=left_label + f" (source lines {a[0]}:{a[1]})",
                                tofile=right_label + f" (source lines {b[0]}:{b[1]})", n=context)
    return "".join(line if line.endswith("\n") else line + "\n\\ No newline at end of file\n" for line in lines)


def read_source(path):
    before = path.stat()
    data = path.read_bytes()
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError("An input changed while being read; retry with edits paused.")
    return data.decode("utf-8"), Path(os.path.relpath(path, Path.cwd())).as_posix()


def selftest():
    text = r'''\src{10}
literal \$ and \verb|$ignored$| % $ignored$ \src{99}
$x_i+\mathcal{F}+\mathfrak{g}+\underline{a}$
\src{11}
\[\begin{aligned}a&=b\\c&=d\end{aligned}\]
\begin{equation}\mathrm{AB}_{i}\end{equation}
\begin{verbatim}$ignored$ \src{99}\end{verbatim}
\src{12}\(y^2\) \ensuremath{z_{j}}
'''
    parsed = parse_tex(text)
    assert len(parsed["spans"]) == 5 and not parsed["diagnostics"]
    assert [marker["printed_page"] for marker in parsed["markers"]] == [10, 11, 12]
    assert [span["page_at_start"] for span in parsed["spans"]] == [10, 11, 11, 12, 12]
    nested = parse_tex(r'$a+\text{inner $b$ and \{x\}}$ $$c$$')
    assert len(nested["spans"]) == 2 and not nested["diagnostics"]
    crossing = parse_tex(r'\src{1}\begin{align}a\\\src{2}b\end{align}')
    assert crossing["spans"][0]["pages_touched"] == [1, 2]
    assert crossing["spans"][0]["crosses_source_marker"]
    broken = parse_tex('$x_{')
    assert not broken["spans"][0]["closed"] and {i["code"] for i in broken["diagnostics"]} >= {"unclosed_math_span", "unclosed_brace"}
    assert parse_tex(r'\begin{align}x\end{gather}')["diagnostics"]
    raw = r'$\symup{X}_{i}+\mathrm{Y}+\left(\mathcal{F}+\mathfrak{g}+\underline{x}\right)$'
    expected = r'${X}_{i}+{Y}+(\mathcal{F}+\mathfrak{g}+\underline{x})$'
    normalized = normalize(raw, "presentation")
    assert normalized["tokens"] == normalize(expected, "presentation")["tokens"]
    assert normalize(raw)["text"] == raw and normalize(raw)["operations"] == []
    for changed in [expected.replace('_{i}', '_{j}'), expected.replace('+', '-', 1), expected.replace(r'\mathcal', r'\mathfrak'), expected.replace(r'\underline', '')]:
        assert normalized["tokens"] != normalize(changed, "presentation")["tokens"]
    assert normalize(r'$\alpha x$', "presentation")["tokens"] != normalize(r'$\alphax$', "presentation")["tokens"]
    assert normalize(r'$\alpha x$', "presentation")["text"] == r'$\alpha x$'
    assert normalize(r'$\text{two words}$', "presentation")["text"] == r'$\text{two words}$'
    assert normalize(r'$\mathrm X+\,Y$', "presentation")["text"] == r'$\mathrm X+\,Y$'
    assert normalize('$a % comment\n+b$', "presentation")["tokens"] == normalize('$a+b$', "presentation")["tokens"]
    args = argparse.Namespace(math_env=[], page=[], normalize="none")
    left = inventory(text, "synthetic-left.tex", args)
    right = inventory(text.replace('x_i', 'x_j'), "synthetic-right.tex", args)
    report = comparison(left, right, "page")
    assert [r["group"] for r in report["groups"] if r["changes"]] == ["10"]
    partial = inventory("\\src{1}\n\\[\na+b\n\\]\n", "synthetic.tex", args, "3:3")
    assert partial["spans"][0]["range_partial"] and partial["spans"][0]["raw_tex"] == "\\[\na+b\n\\]"
    diff = unified_source_diff("a\nb", "a\nc\n", "left.tex", "right.tex")
    assert "-b\n\\ No newline at end of file\n+c\n" in diff
    print("PASS: escaped dollars/comments/verbatim, balanced nested groups/environments, math delimiters, ensuremath, source markers, crossing-page spans, malformed-input diagnostics, conservative opt-in normalization, token boundaries, indices/operators/fonts, range selection, sequence comparison, and exact unified diff.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["extract", "compare", "diff", "selftest"])
    parser.add_argument("left", nargs="?", type=Path)
    parser.add_argument("right", nargs="?", type=Path)
    parser.add_argument("--left-lines", help="Inclusive source line range START:END")
    parser.add_argument("--right-lines", help="Inclusive source line range START:END")
    parser.add_argument("--page", action="append", type=int, default=[])
    parser.add_argument("--math-env", action="append", default=[], help="Additional literal math-environment name")
    parser.add_argument("--normalize", choices=["none", "presentation"], default="none")
    parser.add_argument("--group", choices=["page", "range"], default="page")
    parser.add_argument("--context", type=int, default=3, help="Unified diff context lines")
    args = parser.parse_args()
    if args.action == "selftest":
        selftest()
        return
    if args.left is None or args.action in {"compare", "diff"} and args.right is None:
        parser.error("Supply one input for extract, and two inputs for compare or diff.")
    if args.context < 0:
        parser.error("Diff context must be nonnegative.")
    if args.action == "diff" and (args.normalize != "none" or args.page):
        parser.error("Source diff is literal and accepts source line ranges, not normalization or page filters.")
    left, left_label = read_source(args.left)
    if args.action == "extract":
        result = inventory(left, left_label, args, args.left_lines)
    else:
        right, right_label = read_source(args.right)
        if args.action == "diff":
            sys.stdout.write(unified_source_diff(left, right, left_label, right_label, args.left_lines, args.right_lines, args.context))
            print(json.dumps({"left_sha256": sha(left.encode()), "right_sha256": sha(right.encode()),
                              "scope": "literal source diff; no semantic evaluation or confirmation"}), file=sys.stderr)
            return
        result = comparison(inventory(left, left_label, args, args.left_lines),
                            inventory(right, right_label, args, args.right_lines), args.group)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, UnicodeError, ValueError) as error:
        message = str(error) if isinstance(error, ValueError) and not isinstance(error, UnicodeError) else "Input could not be read as UTF-8; check the requested files."
        print("tex_compare: " + message, file=sys.stderr)
        raise SystemExit(2)
