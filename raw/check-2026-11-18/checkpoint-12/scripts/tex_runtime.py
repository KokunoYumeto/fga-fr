#!/usr/bin/env python3
"""Prepare an isolated TeX runtime and run tools with its fonts and formats.

No edition source file is read or modified. Downloads are pinned by the adjacent
TEX_DEPENDENCIES.tsv. Runtime caches and logs are local build intermediates.
"""

import argparse
import csv
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request
import zipfile


SCRIPT_DIR = Path(__file__).resolve().parent


def capture(command, env=None):
    return subprocess.run(command, env=env, text=True, capture_output=True, check=True).stdout.strip()


def environment(root):
    env = dict(os.environ)
    tree_list = capture(["kpsewhich", "-var-value=TEXMF"]).replace("!!", "")
    env.update({"TEXMFDIST": str(root / "texmf-dist"),
                "TEXMFVAR": str(root / "texmf-var"),
                "TEXMFCONFIG": str(root / "texmf-config"),
                "TEXMFHOME": str(root / "texmf-home"),
                "TEXMF": "{" + ",".join(str(root / n) for n in
                           ["texmf-config", "texmf-var", "texmf-home", "texmf-dist"])
                           + "," + tree_list + "}",
                "FONTCONFIG_FILE": str(root / "fonts.conf"),
                "OSFONTDIR": str(root / "texmf-home/fonts/opentype/public/tex-gyre") + "//"})
    return env


def command_in_runtime(root, command, cwd, logfile=None, extra_env=None):
    """Use a real cache inside the working directory with shell escape disabled.

    This respects TeX's output restrictions rather than loosening openout_any.
    Cache data is copied to/from a shared runtime cache and the temporary copy
    is removed after the command. The command itself chooses its output files.
    """
    cwd = Path(cwd).resolve()
    cache = Path(tempfile.mkdtemp(prefix="fga-tex-cache-", dir=cwd))
    shared = root / "fontloader-cache"
    try:
        if shared.exists():
            shutil.copytree(shared, cache, dirs_exist_ok=True)
        env = environment(root)
        if extra_env:
            env.update(extra_env)
        env["TEXMFCACHE"] = cache.name
        if logfile:
            with Path(logfile).open("w", encoding="utf-8") as log:
                result = subprocess.run(command, cwd=cwd, env=env, text=True,
                                        stdout=log, stderr=subprocess.STDOUT)
        else:
            result = subprocess.run(command, cwd=cwd, env=env)
        shutil.copytree(cache, shared, dirs_exist_ok=True)
        return result.returncode
    finally:
        shutil.rmtree(cache)


def extract_tar(archive, destination):
    with tarfile.open(archive, "r:xz") as source:
        for member in source.getmembers():
            if member.name.startswith("tlpkg/"):
                continue
            if member.name.startswith("texmf-dist/"):
                member.name = member.name[len("texmf-dist/"):]
            name = Path(member.name)
            if name.is_absolute() or ".." in name.parts or member.issym() or member.islnk():
                raise ValueError("Unsafe dependency archive member")
            source.extract(member, destination, filter="data")


def install_dependencies(root):
    with (SCRIPT_DIR / "TEX_DEPENDENCIES.tsv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    downloads = root / "downloads"
    for row in rows:
        path = downloads / row["filename"]
        if not path.exists():
            with urllib.request.urlopen(row["source"], timeout=60) as response:
                path.write_bytes(response.read())
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != row["sha256"] or path.stat().st_size != int(row["bytes"]):
            raise ValueError("Dependency checksum mismatch: " + path.name)
        if path.name.endswith(".tar.xz"):
            extract_tar(path, root / "texmf-home")
        elif path.name == "tex-gyre.zip":
            fonts = root / "texmf-home/fonts/opentype/public/tex-gyre"
            fonts.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(path) as source:
                for name in source.namelist():
                    if name.endswith(".otf") and any(n in name for n in ("pagella", "heros", "cursor")):
                        (fonts / Path(name).name).write_bytes(source.read(name))
        elif path.name == "portuges.zip":
            target = root / "unpack/portuges"
            target.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(path) as source:
                for name in source.namelist():
                    if name.endswith((".ins", ".dtx")):
                        (target / Path(name).name).write_bytes(source.read(name))


def configure_languages(root):
    config = root / "texmf-home/tex/generic/config"
    config.mkdir(parents=True, exist_ok=True)
    (config / "language.dat").write_text(
        "english hyphen.tex\n=usenglish\n=USenglish\n=american\n"
        "french loadhyph-fr.tex\n=francais\n"
        "spanish loadhyph-es.tex\n=espanol\n"
        "portuguese loadhyph-pt.tex\n=portuges\n=brazilian\n=brazil\n"
        "vietnamese zerohyph.tex\nnohyphenation zerohyph.tex\n", encoding="utf-8")
    (config / "language.dat.lua").write_text("""return {
 english={loader='hyphen.tex',lefthyphenmin=2,righthyphenmin=3,patterns='hyph-en-us.pat.txt',hyphenation='hyph-en-us.hyp.txt',synonyms={'usenglish','USenglish','american'},special='language0'},
 french={loader='loadhyph-fr.tex',lefthyphenmin=2,righthyphenmin=2,patterns='hyph-fr.pat.txt',hyphenation='',synonyms={'francais','patois'}},
 spanish={loader='loadhyph-es.tex',lefthyphenmin=2,righthyphenmin=2,patterns='hyph-es.pat.txt',hyphenation='',synonyms={'espanol'}},
 portuguese={loader='loadhyph-pt.tex',lefthyphenmin=2,righthyphenmin=3,patterns='hyph-pt.pat.txt',hyphenation='hyph-pt.hyp.txt',synonyms={'portuges','brazilian','brazil'}},
 vietnamese={loader='zerohyph.tex',lefthyphenmin=2,righthyphenmin=3,patterns='',hyphenation='',synonyms={}},
 nohyphenation={loader='zerohyph.tex',lefthyphenmin=2,righthyphenmin=3,patterns='',hyphenation='',synonyms={}}
}
""", encoding="utf-8")


def configure_fonts(root):
    baseline = capture(["fc-conflist"])
    system_config = None
    for match in re.finditer(r"[+]\s+(.+?\.conf):", baseline):
        for parent in Path(match.group(1)).parents:
            candidate = parent / "fonts.conf"
            if candidate.is_file():
                system_config = candidate
                break
        if system_config:
            break
    if system_config is None:
        raise RuntimeError("Cannot locate the installed fontconfig configuration")
    fontdir = root / "texmf-home/fonts/opentype/public/tex-gyre"
    content = ('<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig>'
               '<include>' + html.escape(str(system_config)) + '</include>'
               '<dir>' + html.escape(str(fontdir)) + '</dir>'
               '<cachedir>' + html.escape(str(root / "cache/fontconfig")) + '</cachedir>'
               '</fontconfig>')
    (root / "fonts.conf").write_text(content, encoding="utf-8")
    subprocess.run(["fc-cache", "-f", str(fontdir)], env=environment(root), check=True)


def setup(root):
    root.mkdir(parents=True, exist_ok=True)
    for name in ("texmf-var", "texmf-config", "texmf-home", "cache", "logs", "downloads"):
        (root / name).mkdir(exist_ok=True)
    source_tree = Path(capture(["kpsewhich", "-var-value=TEXMFDIST"]))
    if not (root / "texmf-dist").exists():
        shutil.copytree(source_tree, root / "texmf-dist", ignore_dangling_symlinks=True)
    install_dependencies(root)
    configure_languages(root)
    configure_fonts(root)
    env = environment(root)
    subprocess.run(["mktexlsr", str(root / "texmf-dist"), str(root / "texmf-home"),
                    str(root / "texmf-var")], env=env, check=True)
    for engine, name in (("luahbtex", "lualatex"), ("xetex", "xelatex")):
        target = root / "texmf-var/web2c" / engine
        target.mkdir(parents=True, exist_ok=True)
        command = [engine, "-ini", "-etex", "-interaction=nonstopmode", "-halt-on-error",
                   "-no-shell-escape", "-jobname=" + name, "-progname=" + name, name + ".ini"]
        code = command_in_runtime(root, command, target, root / "logs" / (name + "-format.txt"))
        if code:
            raise RuntimeError(name + " format creation failed; inspect the local runtime log")
    subprocess.run(["mktexlsr", str(root / "texmf-var")], env=env, check=True)
    # These are generated docstrip outputs in this script's private unpack tree.
    # Remove them before regeneration so an unattended repeat does not prompt.
    for generated in (root / "unpack/portuges").glob("*.ldf"):
        generated.unlink()
    (root / "unpack/portuges/docstrip.cfg").write_text("\\askforoverwritefalse\n", encoding="utf-8")
    code = command_in_runtime(root,
        ["lualatex", "-interaction=nonstopmode", "-halt-on-error", "-no-shell-escape", "portuges.ins"],
        root / "unpack/portuges", root / "logs/portuges-unpack.txt")
    if code:
        raise RuntimeError("Portuguese docstrip generation failed")
    target = root / "texmf-home/tex/generic/babel-portuges"
    target.mkdir(parents=True, exist_ok=True)
    for source in (root / "unpack/portuges").glob("*.ldf"):
        shutil.copy2(source, target / source.name)
    subprocess.run(["mktexlsr", str(root / "texmf-home")], env=env, check=True)
    print("Task-local TeX formats, open-source fonts, and support packages prepared.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path, default=SCRIPT_DIR.parent / "runtime")
    parser.add_argument("--setup", action="store_true")
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    root = args.runtime.resolve()
    if args.setup:
        setup(root)
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if command:
        raise SystemExit(command_in_runtime(root, command, args.cwd))
    if not args.setup:
        parser.error("Specify --setup or a command after --")


if __name__ == "__main__":
    main()
