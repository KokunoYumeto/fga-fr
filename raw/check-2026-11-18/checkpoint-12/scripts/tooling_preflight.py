#!/usr/bin/env python3
"""Read-only tool, package, language, and font inventory; no TeX build."""

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
from pathlib import Path


def run(args, env=None):
    result = subprocess.run(args, env=env, text=True, capture_output=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def tex_file(name, env=None):
    if not shutil.which("kpsewhich"):
        return False
    command = ["kpsewhich"]
    if name == "lualatex.fmt":
        command += ["-engine=luahbtex", "-progname=lualatex"]
    elif name == "xelatex.fmt":
        command += ["-engine=xetex", "-progname=xelatex"]
    status, output, _ = run(command + [name], env)
    return status == 0 and bool(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path)
    args = parser.parse_args()
    if args.runtime:
        from tex_runtime import environment
        os.environ.update(environment(args.runtime.resolve()))
    tools = ["lualatex", "xelatex", "latexmk", "kpsewhich", "pdftoppm", "pdfinfo"]
    versions = {}
    for name in tools:
        if not shutil.which(name):
            versions[name] = None
            continue
        option = "-v" if name in ("pdftoppm", "pdfinfo", "latexmk") else "--version"
        _, output, error = run([name, option])
        versions[name] = (output or error).splitlines()[0]

    # Database-only lookup can fail in a runtime with no ls-R databases.
    # Resolve the runtime's own tree expression instead of embedding local paths.
    recursive_env = dict(os.environ)
    if shutil.which("kpsewhich"):
        _, trees, _ = run(["kpsewhich", "-var-value=TEXMF"])
        recursive_env["TEXMF"] = trees.replace("!!", "")

    packages = ["geometry", "fontspec", "babel", "polyglossia", "microtype",
                "graphicx", "mathtools", "amsthm", "unicode-math", "bookmark",
                "hyperref", "xeCJK", "ulem"]
    names = [name + ".sty" for name in packages]
    names += ["gloss-french.ldf", "gloss-english.ldf", "gloss-spanish.ldf",
              "gloss-vietnamese.ldf", "brazilian.ldf", "portuges.ldf",
              "lualatex.fmt", "xelatex.fmt", "luaotfload-main.lua",
              "luatexbase.sty", "lualatex-math.sty"]
    tex = {name: {"default_lookup": tex_file(name),
                  "recursive_lookup": tex_file(name, recursive_env)} for name in names}

    fonts = ["TeX Gyre Pagella", "TeX Gyre Heros", "TeX Gyre Cursor",
             "Latin Modern Math", "Malgun Gothic", "Malgun Gothic Bold", "SimSun",
             "Microsoft YaHei", "Noto Sans CJK KR", "Noto Serif CJK SC",
             "Noto Sans CJK SC", "P052", "Nimbus Sans", "Nimbus Mono PS"]
    matches = {}
    if shutil.which("fc-match"):
        for font in fonts:
            _, family, _ = run(["fc-match", "-f", "%{family}", font])
            matches[font] = {"resolved_family": family,
                             "exact_family": font in family.split(",")}

    modules = ["fitz", "pypdf", "pdfplumber", "PIL", "reportlab"]
    print(json.dumps({"scope": "Tool availability only; no build or page inspection",
                      "versions": versions,
                      "python_modules": {n: importlib.util.find_spec(n) is not None for n in modules},
                      "tex_files": tex, "font_matches": matches}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
