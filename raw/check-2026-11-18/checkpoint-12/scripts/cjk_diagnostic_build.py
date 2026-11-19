#!/usr/bin/env python3
"""Reproduce the unsuccessful CJK diagnostic font-substitution experiments.

KNOWN LIMITATION: fontconfig aliases and the attempted driver redirects did not
resolve the complete fontspec/NFSS font-selection chain. This helper is retained
as an experiment record, not as a working build solution.

No source is changed. The requested Windows fonts remain unavailable; these
substituted-font builds only reveal later compiler errors and cannot certify
the intended font metrics or final page layout.
"""

import argparse
import hashlib
import html
import json
from pathlib import Path
import subprocess

import build_fga
from tex_runtime import command_in_runtime, environment


ALIASES = [
    ("Malgun Gothic", "Noto Sans CJK KR", None),
    ("Malgun Gothic Bold", "Noto Sans CJK KR", "bold"),
    ("SimSun", "Noto Serif CJK SC", None),
    ("Microsoft YaHei", "Noto Sans CJK SC", None),
]

DRIVER_SUBSTITUTIONS = r"""
\ExplSyntaxOn
\tl_new:N \l_fga_diagnostic_font_call_tl
\cs_new_protected:Npn \fga_diagnostic_font_call:n #1
  {
    \tl_set:Nx \l_fga_diagnostic_font_call_tl {#1}
    \tl_replace_all:Nnn \l_fga_diagnostic_font_call_tl {Malgun~Gothic~Bold} {Noto~Sans~CJK~KR~Bold}
    \tl_replace_all:Nnn \l_fga_diagnostic_font_call_tl {Malgun~Gothic} {Noto~Sans~CJK~KR}
    \tl_replace_all:Nnn \l_fga_diagnostic_font_call_tl {Microsoft~YaHei} {Noto~Sans~CJK~SC}
    \tl_replace_all:Nnn \l_fga_diagnostic_font_call_tl {SimSun} {Noto~Serif~CJK~SC}
  }
\AddToHook{package/fontspec/after}{
  \cs_new_eq:NN \fga_original_font_set:Nnn \__fontspec_primitive_font_set:Nnn
  \cs_new_eq:NN \fga_original_font_gset:Nnn \__fontspec_primitive_font_gset:Nnn
  \cs_set_protected:Npn \__fontspec_primitive_font_set:Nnn #1#2#3
    {
      \fga_diagnostic_font_call:n {#2}
      \exp_args:NNV \fga_original_font_set:Nnn #1 \l_fga_diagnostic_font_call_tl {#3}
    }
  \cs_set_protected:Npn \__fontspec_primitive_font_gset:Nnn #1#2#3
    {
      \fga_diagnostic_font_call:n {#2}
      \exp_args:NNV \fga_original_font_gset:Nnn #1 \l_fga_diagnostic_font_call_tl {#3}
    }
}
\ExplSyntaxOff
"""


def font_config(runtime):
    path = runtime / "diagnostic-cjk-fonts.conf"
    parts = ["<?xml version=\"1.0\"?><!DOCTYPE fontconfig SYSTEM \"fonts.dtd\"><fontconfig>",
             "<include>" + html.escape(str(runtime / "fonts.conf")) + "</include>"]
    for requested, substitute, weight in ALIASES:
        parts.append("<match target=\"pattern\"><test name=\"family\" compare=\"eq\"><string>"
                     + html.escape(requested) + "</string></test><edit name=\"family\" mode=\"assign\" binding=\"strong\"><string>"
                     + html.escape(substitute) + "</string></edit>")
        if weight:
            parts.append("<edit name=\"weight\" mode=\"assign\"><const>" + weight + "</const></edit>")
        parts.append("</match>")
    parts.append("</fontconfig>")
    path.write_text("\n".join(parts))
    env = environment(runtime)
    env["FONTCONFIG_FILE"] = str(path)
    inventory = []
    for requested, expected, _ in ALIASES:
        result = subprocess.run(["fc-match", "--format=%{file}\t%{family}\t%{style}\t%{index}\n", requested],
                                env=env, text=True, capture_output=True, check=True)
        filename, family, style, index = result.stdout.strip().split("\t")
        if expected not in family:
            raise RuntimeError("Diagnostic font alias did not resolve: " + requested)
        font = Path(filename)
        data = font.read_bytes()
        inventory.append({"requested": requested, "resolved_family": family,
                          "style": style, "collection_index": index,
                          "font_file": font.name, "bytes": len(data),
                          "sha256": hashlib.sha256(data).hexdigest()})
    return path, inventory


def mark_diagnostic(work, runtime, tag, layers):
    """Prevent the ordinary publish helper from accepting substituted-font PDFs."""
    for layer in layers:
        path = build_fga.stage_root(runtime, tag) / layer / "result.json"
        result = json.loads(path.read_text())
        if not result["status"].startswith("diagnostic only: "):
            result["status"] = "diagnostic only: " + result["status"]
        result["original_font_requirements_satisfied"] = False
        result["publishable"] = False
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    build_fga.reports(work, runtime, tag)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True,
                        help="Existing frozen work directory; no live tree is read")
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--layers", default="ko,zh-Hans")
    parser.add_argument("--max-passes", type=int, default=3)
    parser.add_argument("--driver-substitutions", action="store_true",
                        help="Explicitly substitute font names in the diagnostic driver; XeTeX does not honor all fontconfig aliases")
    args = parser.parse_args()
    work, runtime = args.work.resolve(), args.runtime.resolve()
    path, inventory = font_config(runtime)

    def diagnostic_command(root, command, cwd, logfile=None, extra_env=None):
        overrides = dict(extra_env or {})
        overrides["FONTCONFIG_FILE"] = str(path)
        return command_in_runtime(root, command, cwd, logfile, overrides)

    build_fga.command_in_runtime = diagnostic_command
    if args.driver_substitutions:
        build_fga.DRIVER = DRIVER_SUBSTITUTIONS + build_fga.DRIVER
    results = [build_fga.build_layer(work, runtime, args.tag, layer, args.max_passes)
               for layer in build_fga.selected_layers(args.layers)]
    mark_diagnostic(work, runtime, args.tag, build_fga.selected_layers(args.layers))
    report = work / "build_reports" / args.tag / "FONT_SUBSTITUTIONS.md"
    build_fga.write_tsv(report.with_name("DIAGNOSTIC_FONTS.tsv"),
                       list(inventory[0]), inventory)
    report.write_text(
        "# Diagnostic font substitutions\n\n"
        "The requested Windows fonts are absent from this environment. This stage used "
        + ("explicit diagnostic-driver font substitutions" if args.driver_substitutions
           else "task-local fontconfig aliases only")
        + " to inspect later compiler diagnostics "
        "without editing the frozen edition sources. These builds do not certify the "
        "requested fonts, their metrics, or final layout and are not publishable editions.\n\n"
        "| Requested font | Diagnostic substitute |\n| --- | --- |\n"
        + "\n".join("| " + requested + " | " + replacement
                     + (" (bold)" if weight else "") + " |"
                     for requested, replacement, weight in ALIASES)
        + "\n\nThe standard runtime font configuration is unchanged. No source, credit, "
        "rights notice, audit ledger, or substantive text was edited by this helper.\n")
    if any(result["status"] != "automated build checks passed; visual review pending"
           for result in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
