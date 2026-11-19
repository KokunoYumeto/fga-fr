"""Repair the LuaLaTeX build of the FGA corrected French of checkpoint 05 (FGA_CHECK, 18 Nov 2026), typesetting only.
French-school field agent (Claude Opus 5.5 at effort high), 19 Nov 2026, at the main session's word (job 4b, option b).
Works on the publication copy pub/ (a fresh copy of checkpoint 05's sources/fr); checkpoint 05 itself is not touched.
Every change is written to REPAIR_LOG.tsv. Run: python -I -B fix_fr.py"""
import csv, pathlib, re, shutil

H = pathlib.Path(__file__).parent
CP05 = next((H.parent / "returns").glob("FGA_CHECK_checkpoint_05_*_unzipped"))
PUB = H / "pub"
if PUB.exists():
    shutil.rmtree(PUB)
shutil.copytree(CP05 / "sources" / "fr", PUB)
FR = PUB / "fr"
for p in FR.iterdir():  # build products shipped in the checkpoint are not sources
    if p.suffix in (".aux", ".log", ".toc", ".out", ".pdf"):
        p.unlink()
BS = chr(92)
rows = []


def line_of(t, pos):
    return t.count("\n", 0, pos) + 1


def sub_once(name, old, new, error, why):
    f = FR / name
    t = f.read_text(encoding="utf-8")
    assert t.count(old) == 1, (name, old, t.count(old))
    pos = t.index(old)
    f.write_text(t.replace(old, new), encoding="utf-8", newline="")
    rows.append([name, line_of(t, pos), error, old, new, why])


# 1. Control words run together with a following O (from \Osh replaced by an upright O): \longrightarrowO_y etc.
MERGED = re.compile(re.escape(BS) + r"(longrightarrow|otimes|simeq)O(?=[_^(])")
for f in sorted(FR.glob("*.tex")):
    t = f.read_text(encoding="utf-8")
    hits = list(MERGED.finditer(t))
    for m in hits:
        rows.append([f.name, line_of(t, m.start()), "Undefined control sequence (and the Double subscript that follows)",
                     m.group(0), BS + m.group(1) + " O",
                     "control word run together with the letter O; a space separates them, the reading is unchanged"])
    if hits:
        f.write_text(MERGED.sub(lambda m: BS + m.group(1) + " O", t), encoding="utf-8", newline="")

# 2. 149.tex, equation (4.3): a blank line opens the display, which ends math mode inside the equation environment.
sub_once("149.tex", BS + "begin{equation}" + BS + "tag{4.3}\n\n" + BS + "symup{",
         BS + "begin{equation}" + BS + "tag{4.3}\n" + BS + "symup{",
         "Missing $ inserted; Display math should end with $$; Bad math environment delimiter; \\leqno in horizontal mode",
         "blank line inside the equation environment removed")

# 3. 182.tex, Théorème 4 i.: a stray closing brace after \uline{sur}.
sub_once("182.tex", "modules} plats " + BS + "uline{sur}} $",
         "modules} plats " + BS + "uline{sur} $",
         "Extra }, or forgotten \\endgroup",
         "stray closing brace removed")

# 4. 190.tex: F''_2^{-1} is a double superscript in TeX (the primes are a superscript); the base is grouped.
sub_once("190.tex", "F''_1F''_2^{-1}=F''", "F''_1{F''_2}^{-1}=F''",
         "Double superscript",
         "the base F''_2 grouped before the exponent -1; the formula is unchanged")

# 5. 195.tex: \nolimits after \underset{...}{\varprojlim}, which is not a math operator.
sub_once("195.tex", BS + "underset{" + BS + "alpha}{" + BS + "varprojlim}" + BS + "nolimits_",
         BS + "mathop{" + BS + "underset{" + BS + "alpha}{" + BS + "varprojlim}}" + BS + "nolimits_",
         "Limit controls must follow a math operator",
         "the limit sign with its index made a math operator, so that the subscript C' goes to its side as intended")

# 6. Overfull lines (PDF check: nothing beyond 2pt). Underlined statements (ulem) can break only between words, and
#    three paragraphs ran 5-37pt into the margin; more emergency stretch lets TeX loosen those lines instead.
sub_once("main.tex", BS + "setlength{" + BS + "emergencystretch}{1.5em}",
         BS + "setlength{" + BS + "emergencystretch}{6em}",
         "Overfull hbox 36.7pt (182.tex Corollaire 2), 11.9pt and 6.4pt (182.tex), 5.4pt (212.tex)",
         "emergency stretch of the paragraph builder raised from 1.5em to 6em (layout only)")

# 7. 149.tex, the display before (4.1 bis): one line of three equalities, 26.9pt too wide; set on three aligned lines.
OLD7 = r"""\[
\symup{\Extsh_{\Osh_X}^{p}(F,L)
=L\otimes(\underline{\Omega}_X^{n})'\otimes
  \Extsh_{\Osh_X}^{p}(F,\underline{\Omega}_X^{n})
=L\otimes(\underline{\Omega}_X^{n})'\otimes
  \Homsh_{\Osh_X}(F,\underline{\omega}_Y^{q})
=\Homsh_{\Osh_X}\!\left(
  F\otimes L'\otimes\underline{\Omega}_X^{n},\underline{\omega}_Y^{q}\right)}
\]"""
NEW7 = r"""\[
\begin{aligned}
\symup{\Extsh_{\Osh_X}^{p}(F,L)}
&\symup{{}=L\otimes(\underline{\Omega}_X^{n})'\otimes
  \Extsh_{\Osh_X}^{p}(F,\underline{\Omega}_X^{n})}\\
&\symup{{}=L\otimes(\underline{\Omega}_X^{n})'\otimes
  \Homsh_{\Osh_X}(F,\underline{\omega}_Y^{q})}\\
&\symup{{}=\Homsh_{\Osh_X}\!\left(
  F\otimes L'\otimes\underline{\Omega}_X^{n},\underline{\omega}_Y^{q}\right)}
\end{aligned}
\]"""
sub_once("149.tex", OLD7, NEW7, "Overfull hbox 26.9pt (display)",
         "the display set on three lines aligned at the equals signs; the formula is unchanged")

with open(H / "REPAIR_LOG.tsv", "w", encoding="utf-8", newline="") as out:
    w = csv.writer(out, delimiter="\t", lineterminator="\n")
    w.writerow(["file", "line", "build error (LuaLaTeX)", "before", "after", "repair"])
    w.writerows([[str(c).replace("\n", BS + "n") for c in r] for r in rows])
print(len(rows), "places repaired")
