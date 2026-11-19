"""Publication copy of the FGA corrected French at checkpoint 12 (FGA_CHECK, 19 Nov 2026): the two layout repairs of
19 Nov (the run kept the build repairs but not these) and the revised rights notice of 15 Nov in NOTICE.tex.
Typesetting and notice only. French-school field agent (Claude Opus 5.5 at effort high), 19 Nov 2026.
Run: python -I -B fix_fr2.py  (recreates pub/ from checkpoint 12, then logs each change in REPAIR_LOG.tsv)"""
import csv, pathlib, shutil, sys

H = pathlib.Path(__file__).parent
W = H.parent
sys.path.insert(0, str(W))
from apply_notice import FR_FGA  # noqa: E402

CP = W / "returns/FGA_CHECK_checkpoint_12_20261119T0612Z_unzipped"
PUB = H / "pub"
if PUB.exists():
    shutil.rmtree(PUB)
shutil.copytree(CP / "sources/fr", PUB, ignore=shutil.ignore_patterns("_repository"))
BS = chr(92)
rows = []


def sub_once(rel, old, new, error, why):
    f = PUB / rel
    t = f.read_text(encoding="utf-8")
    assert t.count(old) == 1, (rel, t.count(old))
    line = t[:t.index(old)].count("\n") + 1
    f.write_text(t.replace(old, new), encoding="utf-8", newline="")
    rows.append([rel, line, error, old, new, why])


sub_once("fr/main.tex", BS + "setlength{" + BS + "emergencystretch}{1.5em}",
         BS + "setlength{" + BS + "emergencystretch}{6em}",
         "Overfull hbox 36.7pt, 11.9pt and 6.4pt (182.tex), 5.4pt (212.tex)",
         "emergency stretch of the paragraph builder raised from 1.5em to 6em (layout only)")
src = (W / "fga_publish/fix_fr.py").read_text(encoding="utf-8")
OLD7 = src.split('OLD7 = r"""', 1)[1].split('"""', 1)[0]
NEW7 = src.split('NEW7 = r"""', 1)[1].split('"""', 1)[0]
sub_once("fr/149.tex", OLD7, NEW7, "Overfull hbox 26.9pt (display)",
         "the display set on three lines aligned at the equals signs; the formula is unchanged")
n = PUB / "NOTICE.tex"
t = n.read_text(encoding="utf-8")
start, end = t.index("Les droits sur les œuvres originales"), t.index(BS + "par" + BS + "endgroup")
n.write_text(t[:start] + FR_FGA + "\n\n" + t[end:], encoding="utf-8", newline="")
rows.append(["NOTICE.tex", t[:start].count("\n") + 1, "", "rights paragraphs of 2026-08-30", "revised notice of 15 Nov 2026",
             "rights notice only; the credit paragraphs before it unchanged"])
rn = PUB / "RIGHTS_NOTICE.md"
head = rn.read_text(encoding="utf-8").split("\n", 1)[0]
rn.write_text(head + "\n\n" + FR_FGA + "\n", encoding="utf-8", newline="")
with open(H / "REPAIR_LOG.tsv", "w", encoding="utf-8", newline="") as out:
    w = csv.writer(out, delimiter="\t", lineterminator="\n")
    w.writerow(["file", "line", "build finding (LuaLaTeX)", "before", "after", "change"])
    w.writerows([[str(c).replace("\n", BS + "n") for c in r] for r in rows])
print(len(rows), "changes")
