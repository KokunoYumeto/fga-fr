#!/usr/bin/env python3
"""Build FGA layer snapshots, summarize diagnostics, and render selected PDF pages.

No edition source is changed. Raw logs, build copies, SyncTeX data, and rendered
pages stay in the isolated runtime. Sanitized reports go into build_reports/.
Rendering is recorded as rendering, never as a completed visual inspection.
"""

import argparse
import csv
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

from pypdf import PdfReader
from tex_runtime import command_in_runtime, environment


BASE = Path(__file__).resolve().parents[1]
LAYERS = {
    "fr": ("fr/main.tex", "lualatex", 3, False),
    "fr_printed": ("fr/main.tex", "lualatex", 3, False),
    "en": ("en/main.tex", "lualatex", 3, False),
    "es": ("es/FGA_ES_CURRENT.tex", "lualatex", 3, False),
    "es_149_printed": ("es/FGA_ES_149_PRINTED.tex", "lualatex", 3, False),
    "pt-BR": ("pt_BR/FGA_PTBR_CURRENT.tex", "xelatex", 3, True),
    "pt-BR_printed": ("pt_BR/FGA_PTBR_PRINTED.tex", "xelatex", 3, True),
    "vi": ("FGA_vi_current.tex", "lualatex", 3, False),
    "vi_diplomatic": ("FGA_vi_diplomatic.tex", "lualatex", 3, False),
    "ko": ("main.tex", "xelatex", 3, False),
    "zh-Hans": ("source/zh/main.tex", "xelatex", 3, False),
}
OVERFULL = re.compile(r"Overfull \\([hv])box \(([0-9.]+)pt too (?:wide|high)\)")
SOURCE_LINES = re.compile(r"at lines? (\d+)(?:--(\d+))?")
SHIPOUT = re.compile(r"FGA-SHIPOUT\|(\d+)\|([^\r\n]*)")
FILE_BEGIN = re.compile(r"FGA-FILE-BEGIN\|([^|\r\n]*)\|([^|\r\n]+)")
FILE_END = re.compile(r"FGA-FILE-END\|")
RERUN = re.compile(r"(?:Rerun to get|Rerun LaTeX|Label\(s\) may have changed|rerunfilecheck Warning)", re.I)
EMAIL = re.compile(r"(?<![\w.+-])[\w.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![\w])")
ABSOLUTE = re.compile(r"(?<![:\w])/(?:[A-Za-z0-9_.~-]+/)+[A-Za-z0-9_.~+-]+")
WINDOWS = re.compile(r"(?<![A-Za-z\\])[A-Za-z]:\\(?:[^ \t\r\n<>]+)")
DRIVER = r"""
\errorcontextlines=0
\newcount\FgaPhysicalPage
\FgaPhysicalPage=0
\AddToHook{shipout/before}{%
  \global\advance\FgaPhysicalPage by 1
  \typeout{FGA-SHIPOUT|\the\FgaPhysicalPage|\thepage}%
}
\AddToHook{file/before}{\typeout{FGA-FILE-BEGIN|\CurrentFilePath|\CurrentFile}}
\AddToHook{file/after}{\typeout{FGA-FILE-END|}}
\input{ENTRYPOINT}
"""


def utc():
    return datetime.now(timezone.utc).isoformat()


def sanitize(value):
    return EMAIL.sub("<email>", WINDOWS.sub("<local>", ABSOLUTE.sub("<local>", str(value))))


def selected_layers(value):
    names = list(LAYERS) if value == "all" else value.split(",")
    if not names or any(name not in LAYERS for name in names):
        raise ValueError("Unknown layer; choose all or comma-separated names from the plan")
    return list(dict.fromkeys(names))


def stage_root(runtime, tag):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", tag):
        raise ValueError("Stage tag must use letters, digits, underscores, or hyphens")
    return runtime / "builds" / tag


def source_label(filename, cwd, snapshot, layer):
    path = Path(filename)
    if not path.is_absolute():
        path = cwd / path
    try:
        return "sources/" + layer + "/" + path.resolve().relative_to(snapshot.resolve()).as_posix()
    except ValueError:
        return "<package>/" + path.name


def tree_hash(root):
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            name = path.relative_to(root).as_posix()
            digest.update(name.encode())
            digest.update(b"\0")
            digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def aux_hash(cwd, stem):
    digest = hashlib.sha256()
    for suffix in [".aux", ".toc", ".out", ".lof", ".lot"]:
        path = cwd / (stem + suffix)
        digest.update(suffix.encode())
        if path.exists():
            digest.update(path.read_bytes())
    return digest.hexdigest()


def parse_log(text, cwd, snapshot, layer):
    stack = []
    physical = 0
    overfull = []
    diagnostics = []
    page_labels = {}
    lines = text.splitlines()
    for index, line in enumerate(lines):
        begin = FILE_BEGIN.search(line)
        if begin:
            stack.append(str(Path(begin[1]) / begin[2]) if begin[1] else begin[2])
        if FILE_END.search(line) and stack:
            stack.pop()
        ship = SHIPOUT.search(line)
        if ship:
            physical = int(ship[1])
            page_labels[str(physical)] = sanitize(ship[2].strip())
        current = stack[-1] if stack else ""
        match = OVERFULL.search(line)
        if match:
            location = SOURCE_LINES.search(line)
            start = int(location[1]) if location else None
            end = int(location[2] or location[1]) if location else None
            overfull.append({
                "box": match[1] + "box", "pt": float(match[2]),
                "source": source_label(current, cwd, snapshot, layer) if current else "",
                "raw_source": current, "line_start": start, "line_end": end,
                "shipout_candidate": physical + 1, "pdf_pages": [],
                "mapping": "not yet mapped", "log_line": index + 1,
            })
        category = ""
        message = ""
        error_location = re.match(r"^(.+?\.(?:tex|sty|cls|cfg|def|ldf)):(\d+):\s*(.*)", line)
        if error_location:
            category, message = "error", error_location[3]
            current = error_location[1]
            location_line = int(error_location[2])
        else:
            location_line = ""
            if line.startswith("!"):
                category, message = "error", line.lstrip("! ")
            elif line.startswith("Missing character:"):
                category, message = "missing_glyph", line
            elif re.match(r"^(?:LaTeX|Package .+?|Class .+?) Warning:", line):
                category, message = "warning", line
        if category:
            diagnostics.append({
                "category": category,
                "source": source_label(current, cwd, snapshot, layer) if current else "",
                "line": location_line, "message": sanitize(message),
                "log_line": index + 1,
            })
    return overfull, diagnostics, page_labels


def synctex_index(path, cwd):
    inputs = {}
    index = {}
    page = None
    if not path.exists():
        return inputs, index
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", errors="replace") as stream:
        for line in stream:
            match = re.match(r"Input:(\d+):(.*)", line)
            if match:
                filename = Path(match[2].strip())
                if not filename.is_absolute():
                    filename = cwd / filename
                inputs[int(match[1])] = str(filename.resolve())
                continue
            match = re.match(r"\{(\d+)", line)
            if match:
                page = int(match[1])
                continue
            if line.startswith("}"):
                page = None
                continue
            match = re.match(r"[\[\(vhkgxr$](\d+),(\d+)(?:,\d+)?:", line)
            if match and page:
                index.setdefault(int(match[1]), {}).setdefault(int(match[2]), set()).add(page)
    return inputs, index


def map_boxes(boxes, pdf, synctex, cwd, snapshot, layer):
    if not pdf.exists():
        return
    count = len(PdfReader(pdf).pages)
    inputs, nodes = synctex_index(synctex, cwd)
    input_tags = {filename: tag for tag, filename in inputs.items()}
    query_env = dict(os.environ)
    query_env.pop("SYNCTEX_VIEWER", None)
    for box in boxes:
        relative_prefix = "sources/" + layer + "/"
        filename = None
        if box["source"].startswith(relative_prefix):
            filename = snapshot / box["source"][len(relative_prefix):]
        pages = set()
        start, end = box["line_start"], box["line_end"]
        if filename and start is not None:
            tag = input_tags.get(str(filename.resolve()))
            if tag is not None:
                line_nodes = nodes.get(tag, {})
                for line_number, found in line_nodes.items():
                    if start <= line_number <= (end or start):
                        pages.update(found)
                if pages:
                    box["mapping"] = "SyncTeX nodes in diagnostic line range; visual confirmation required"
            if not pages and shutil.which("synctex"):
                for line_number in sorted({start, end or start}):
                    result = subprocess.run(
                        ["synctex", "view", "-i", str(line_number) + ":0:" + str(filename),
                         "-o", str(pdf)], cwd=cwd, env=query_env, text=True,
                        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                    pages.update(int(value) for value in re.findall(r"^Page:(\d+)", result.stdout, re.M))
                if pages:
                    box["mapping"] = "SyncTeX forward-query candidates; visual confirmation required"
        if not pages and box.get("shipout_candidate"):
            pages.add(box["shipout_candidate"])
            box["mapping"] = "next-shipout candidate only; source/page association unconfirmed"
        box["pdf_pages"] = sorted(page for page in pages if 1 <= page <= count)
        if not box["pdf_pages"]:
            box["mapping"] = "unmapped; inspect raw log and locate manually"


def write_tsv(path, columns, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def reports(work, runtime, tag):
    summary, boxes, diagnostics = [], [], []
    for path in sorted(stage_root(runtime, tag).glob("*/result.json")):
        result = json.loads(path.read_text())
        passes = result["passes"]
        last = passes[-1] if passes else {}
        current = last.get("overfull", [])
        messages = last.get("diagnostics", [])
        summary.append({
            "layer": result["layer"], "engine": result["engine"], "entry": result["entry"],
            "working_directory": str(Path(result["entry"]).parent),
            "command": " ".join(last.get("command", [])),
            "passes": len(passes), "exit_code": last.get("exit_code", ""),
            "pdf_pages": result.get("pdf_pages", 0), "aux_stable": result.get("aux_stable", False),
            "errors": sum(row["category"] == "error" for row in messages),
            "warnings": sum(row["category"] == "warning" for row in messages),
            "missing_glyphs": sum(row["category"] == "missing_glyph" for row in messages),
            "max_overfull_pt": max((row["pt"] for row in current), default=0),
            "boxes_over_2pt": sum(row["pt"] > 2 for row in current),
            "boxes_over_10pt": sum(row["pt"] > 10 for row in current),
            "status": result["status"], "source_tree_sha256": result["source_tree_sha256"],
            "date_utc": result.get("finished_utc", ""), "visual_review": "not performed by this script",
        })
        for run in passes:
            for row in run["overfull"]:
                boxes.append(dict(row, layer=result["layer"], pass_number=run["number"],
                                  latest_pass=run["number"] == len(passes),
                                  pdf_pages=",".join(map(str, row["pdf_pages"]))))
            for row in run["diagnostics"]:
                diagnostics.append(dict(row, layer=result["layer"], pass_number=run["number"],
                                        latest_pass=run["number"] == len(passes)))
    output = work / "build_reports" / tag
    write_tsv(output / "BUILD_SUMMARY.tsv",
              ["layer", "engine", "entry", "passes", "exit_code", "pdf_pages", "aux_stable",
               "errors", "warnings", "missing_glyphs", "max_overfull_pt", "boxes_over_2pt",
               "boxes_over_10pt", "status", "source_tree_sha256", "date_utc",
               "working_directory", "command", "visual_review"], summary)
    write_tsv(output / "OVERFULL_BOXES.tsv",
              ["layer", "pass_number", "latest_pass", "box", "pt", "source", "line_start",
               "line_end", "pdf_pages", "mapping", "shipout_candidate", "log_line"], boxes)
    write_tsv(output / "DIAGNOSTICS.tsv",
              ["layer", "pass_number", "latest_pass", "category", "source", "line",
               "message", "log_line"], diagnostics)
    (output / "README.md").write_text(
        "# Automated build evidence\n\n"
        "These tables record actual engine runs. They do not record a visual inspection. "
        "Page numbers are one-based physical PDF pages. Source locations come from LaTeX "
        "file-hook context; delayed typesetting can make that context approximate. "
        "SyncTeX and next-shipout mappings are candidates to verify visually. "
        "All raw logs, copied build trees, and SyncTeX files remain outside this deliverable tree.\n\n"
        "The two Portuguese layers run exactly three prescribed XeLaTeX passes. Other "
        "layers run at least three passes and continue only while auxiliary files or rerun "
        "diagnostics require it, up to the requested maximum. A typeset result with no "
        "recorded overflow above 2 pt still needs the visual checks required in PDF_CHECK.md.\n",
        encoding="utf-8")


def build_layer(work, runtime, tag, layer, max_passes):
    entry, engine, minimum, fixed = LAYERS[layer]
    source = work / "sources" / layer
    target = stage_root(runtime, tag) / layer
    if target.exists():
        raise FileExistsError("Build stage already exists for " + layer + "; choose a new tag")
    target.mkdir(parents=True)
    snapshot = target / "source"
    before_hash = tree_hash(source)
    shutil.copytree(source, snapshot)
    if tree_hash(snapshot) != before_hash:
        raise RuntimeError("Source snapshot mismatch for " + layer)
    cwd = (snapshot / entry).parent
    stem = Path(entry).stem
    driver = target / "driver.tex"
    driver.write_text(DRIVER.replace("ENTRYPOINT", Path(entry).name), encoding="utf-8")
    result = {"layer": layer, "entry": "sources/" + layer + "/" + entry,
              "engine": engine, "source_tree_sha256": before_hash, "passes": [],
              "status": "running", "aux_stable": False, "pdf_pages": 0}
    result_path = target / "result.json"
    previous = None
    limit = minimum if fixed else max(minimum, max_passes)
    for number in range(1, limit + 1):
        log = target / ("pass-" + str(number) + ".stdout.log")
        command = [engine, "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error",
                   "-file-line-error", "-synctex=1", "-jobname=" + stem, str(driver)]
        code = command_in_runtime(runtime, command, cwd, log, {"max_print_line": "100000"})
        text = log.read_text(encoding="utf-8", errors="replace")
        overfull, diagnostics, labels = parse_log(text, cwd, snapshot, layer)
        pdf = cwd / (stem + ".pdf")
        sync = cwd / (stem + ".synctex.gz")
        if code == 0 and pdf.exists() and pdf.stat().st_size:
            map_boxes(overfull, pdf, sync, cwd, snapshot, layer)
            result["pdf_pages"] = len(PdfReader(pdf).pages)
        current = aux_hash(cwd, stem)
        stable = previous is not None and current == previous and not RERUN.search(text)
        result["passes"].append({
            "number": number, "exit_code": code, "aux_sha256": current,
            "aux_stable": stable, "overfull": overfull, "diagnostics": diagnostics,
            "page_labels": labels, "date_utc": utc(),
            "command": [engine, "-no-shell-escape", "-interaction=nonstopmode",
                        "-halt-on-error", "-file-line-error", "-synctex=1",
                        "-jobname=" + stem, "<instrumented driver for " + Path(entry).name + ">"],
        })
        result["aux_stable"] = stable
        result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
        if code != 0:
            result["status"] = "engine error"
            break
        previous = current
        if number >= minimum and (fixed or stable):
            break
    last = result["passes"][-1]
    if result["status"] != "engine error":
        if not result["aux_stable"]:
            result["status"] = "auxiliary files or rerun diagnostics not stable"
        elif any(row["category"] in ("error", "missing_glyph") for row in last["diagnostics"]):
            result["status"] = "error or missing glyph diagnostic"
        elif any(re.search(r"undefined references|(?:Reference|Citation).+undefined",
                           row["message"], re.I) for row in last["diagnostics"]):
            result["status"] = "unresolved reference or citation"
        elif any(row["pt"] > 2 for row in last["overfull"]):
            result["status"] = "overflow above 2 pt"
        else:
            result["status"] = "automated build checks passed; visual review pending"
    result["finished_utc"] = utc()
    if tree_hash(source) != before_hash:
        result["status"] = "original source changed during build; snapshot retained"
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    reports(work, runtime, tag)
    print(layer + ": " + result["status"], flush=True)
    return result


def load_build(runtime, tag, layer):
    entry = LAYERS[layer][0]
    target = stage_root(runtime, tag) / layer
    result = json.loads((target / "result.json").read_text())
    cwd = (target / "source" / entry).parent
    return result, target, cwd, cwd / (Path(entry).stem + ".pdf")


def page_selection(value, count):
    if value == "spread":
        return sorted({1, min(2, count), max(1, count // 4), max(1, count // 2),
                       max(1, 3 * count // 4), count})
    pages = set()
    for part in value.split(","):
        if part == "last":
            pages.add(count)
        elif "-" in part:
            first, last = map(int, part.split("-", 1))
            pages.update(range(first, last + 1))
        else:
            pages.add(int(part))
    if not pages or any(page < 1 or page > count for page in pages):
        raise ValueError("Requested physical PDF page is out of range")
    return sorted(pages)


def render_pages(work, runtime, tag, layer, pages, dpi, reason):
    _, _, _, pdf = load_build(runtime, tag, layer)
    count = len(PdfReader(pdf).pages)
    if any(page < 1 or page > count for page in pages):
        raise ValueError("Render page outside PDF range")
    target = runtime / "rendered_builds" / tag / layer
    target.mkdir(parents=True, exist_ok=True)
    rows = []
    for page in sorted(set(pages)):
        prefix = target / ("page-" + str(page).zfill(4))
        subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(dpi),
                        "-png", "-singlefile", str(pdf), str(prefix)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        rows.append({"layer": layer, "pdf_page": page, "dpi": dpi, "reason": reason,
                     "render_key": tag + "/" + layer + "/" + prefix.name + ".png",
                     "date_utc": utc(), "visual_review": "rendered; not inspected by this script"})
    report = work / "build_reports" / tag / "RENDERED_PAGES.tsv"
    previous = list(csv.DictReader(report.open(), delimiter="\t")) if report.exists() else []
    write_tsv(report, ["layer", "pdf_page", "dpi", "reason", "render_key", "date_utc", "visual_review"],
              previous + rows)
    print(layer + ": rendered physical PDF pages " + ",".join(map(str, sorted(set(pages)))), flush=True)


def render_overflows(work, runtime, baseline, tag, layer, threshold, dpi):
    earlier, _, _, _ = load_build(runtime, baseline, layer)
    current, target, cwd, pdf = load_build(runtime, tag, layer)
    selected = [dict(row) for row in earlier["passes"][-1]["overfull"] if row["pt"] > threshold]
    if not selected:
        print(layer + ": no baseline boxes above the requested threshold")
        return
    for row in selected:
        row["baseline_pdf_pages"] = list(row["pdf_pages"])
    if tag != baseline:
        for row in selected:
            row["shipout_candidate"] = None
            row["pdf_pages"] = []
        map_boxes(selected, pdf, cwd / (pdf.stem + ".synctex.gz"), cwd, target / "source", layer)
    unmapped = [row for row in selected if not row["pdf_pages"]]
    pages = sorted({page for row in selected for page in row["pdf_pages"]})
    report = work / "build_reports" / tag / "OVERFLOW_REVIEW_MAP.tsv"
    previous = list(csv.DictReader(report.open(), delimiter="\t")) if report.exists() else []
    mapped = [dict(row, layer=layer, baseline=baseline, review_stage=tag,
                   baseline_pdf_pages=",".join(map(str, row["baseline_pdf_pages"])),
                   pdf_pages=",".join(map(str, row["pdf_pages"])),
                   date_utc=utc(), visual_review="candidate mapping; visual inspection pending")
              for row in selected]
    write_tsv(report,
              ["layer", "baseline", "review_stage", "box", "pt", "source", "line_start",
               "line_end", "baseline_pdf_pages", "pdf_pages", "mapping", "date_utc", "visual_review"],
              previous + mapped)
    if pages:
        render_pages(work, runtime, tag, layer, pages, dpi,
                     "candidate pages for boxes above " + str(threshold) + " pt in " + baseline)
    if unmapped:
        raise RuntimeError(str(len(unmapped)) + " baseline boxes remain unmapped; locate them manually")


def publish_pdf(work, runtime, tag, layer):
    result, _, _, pdf = load_build(runtime, tag, layer)
    if result["status"] != "automated build checks passed; visual review pending":
        raise RuntimeError(layer + ": automated build requirements have not passed")
    if tree_hash(work / "sources" / layer) != result["source_tree_sha256"]:
        raise RuntimeError(layer + ": current sources differ from the selected build snapshot")
    output = work / "pdf" / ("FGA_" + layer + ".pdf")
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(pdf, output)
    print(layer + ": copied successful build PDF; visual inspection remains separately recorded")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, default=BASE)
    parser.add_argument("--runtime", type=Path, default=BASE / "runtime")
    commands = parser.add_subparsers(dest="action", required=True)
    commands.add_parser("plan")
    build = commands.add_parser("build")
    build.add_argument("--layers", default="all")
    build.add_argument("--tag", required=True)
    build.add_argument("--max-passes", type=int, default=6)
    render = commands.add_parser("render")
    render.add_argument("--layer", choices=LAYERS, required=True)
    render.add_argument("--tag", required=True)
    render.add_argument("--pages", required=True, help="One-based pages, ranges, last, or spread")
    render.add_argument("--dpi", type=int, default=400)
    overflow = commands.add_parser("render-overflows")
    overflow.add_argument("--layer", choices=LAYERS, required=True)
    overflow.add_argument("--baseline", required=True)
    overflow.add_argument("--tag", required=True)
    overflow.add_argument("--threshold", type=float, default=10)
    overflow.add_argument("--dpi", type=int, default=400)
    publish = commands.add_parser("publish-pdfs")
    publish.add_argument("--layers", default="all")
    publish.add_argument("--tag", required=True)
    args = parser.parse_args()
    work, runtime = args.work.resolve(), args.runtime.resolve()
    if args.action == "plan":
        for layer, (entry, engine, passes, fixed) in LAYERS.items():
            print(layer + "\t" + engine + "\t" + ("exactly " if fixed else "at least ") +
                  str(passes) + " passes\tsources/" + layer + "/" + entry)
    elif args.action == "build":
        results = []
        for layer in selected_layers(args.layers):
            results.append(build_layer(work, runtime, args.tag, layer, args.max_passes))
        if any(result["status"] != "automated build checks passed; visual review pending"
               for result in results):
            raise SystemExit(1)
    elif args.action == "render":
        _, _, _, pdf = load_build(runtime, args.tag, args.layer)
        pages = page_selection(args.pages, len(PdfReader(pdf).pages))
        render_pages(work, runtime, args.tag, args.layer, pages, args.dpi, "requested review pages")
    elif args.action == "render-overflows":
        render_overflows(work, runtime, args.baseline, args.tag, args.layer, args.threshold, args.dpi)
    else:
        for layer in selected_layers(args.layers):
            publish_pdf(work, runtime, args.tag, layer)


if __name__ == "__main__":
    main()
