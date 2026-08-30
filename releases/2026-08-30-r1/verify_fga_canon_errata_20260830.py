"""Deterministic replay for FGA-CANON-ERR-0001 through -0017.

The verifier reads only the four maintained source units, their exact Git
preimages, the bounded intake master, the semantic receipt, the two build
logs/PDFs, and the bounded render directory.  It does not mutate authority
witnesses or edition sources.  Its sole output is the JSON QA receipt named
below.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[4]
FGA = ROOT / "03_projects/language_management/english_germanic/03_working_translations/fga_r1"
MASTER = ROOT / "03_projects/language_management/romance/00_lane_control/FGA_CANON_INTAKE_MASTER.jsonl"
OUT = ROOT / "03_projects/language_management/romance/00_lane_control/FGA_CANON_ERRATA_0001_0017_IMPLEMENTATION_QA.json"

PATHS = {
    "fr212": "03_projects/language_management/english_germanic/03_working_translations/fga_r1/fr/212.tex",
    "en212": "03_projects/language_management/english_germanic/03_working_translations/fga_r1/en/212.tex",
    "fr221": "03_projects/language_management/english_germanic/03_working_translations/fga_r1/fr/221.tex",
    "en221": "03_projects/language_management/english_germanic/03_working_translations/fga_r1/en/221.tex",
}

BASE_SHA = {
    "fr212": "9C868DB596A2DA534C013C377DD507B1FFFE1D7E039455B41FAA39152E47234B",
    "en212": "67E8088E8719D0915A5563E3D91E3669A635E84573254724638FEDB340A53A18",
    "fr221": "951C461B15ED60C2CBE44338F89143E1FD7DCF6709FAD75FA7B50FA905749A1D",
    "en221": "D571D5C0DFE5B845044BAAD57D5780D6302D084673C610B8B598B0BD6D3C9037",
}

LIVE_SHA = {
    "fr212": "BFC8784D358704109A24E7041259E364184782C0027413EFEB4A42C0A8F53102",
    "en212": "B83B5CA0A17A28FC92EF58CDBE8CACA95827A12AEA17456E0C4FE9F1C7162DC7",
    "fr221": "F3C962FE48853E7F31113AD3F1EC93005494A89ED78F1BE35F19E80332D7A94C",
    "en221": "35E156BC6768E3C9125B66E20C38B339DA059C09A78A2563BAD9714745CE119E",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def git_preimage(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"HEAD:{path}"], cwd=ROOT)


def strip_footnotes(text: str) -> str:
    marker = r"\footnote{"
    out: list[str] = []
    cursor = 0
    while True:
        start = text.find(marker, cursor)
        if start < 0:
            out.append(text[cursor:])
            break
        out.append(text[cursor:start])
        i = start + len(marker)
        depth = 1
        while i < len(text) and depth:
            if text[i] == "{" and (i == 0 or text[i - 1] != "\\"):
                depth += 1
            elif text[i] == "}" and (i == 0 or text[i - 1] != "\\"):
                depth -= 1
            i += 1
        if depth:
            raise AssertionError("unbalanced footnote while stripping")
        cursor = i
    return "".join(out)


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


REPLACEMENTS = {
    "fr212": [
        (r"$(n+1)$-ième de $(R,p_1)$ sur $X$", r"$n$-ième de $(R,p_1)$ sur $X$"),
        (r"K_0=R,qquad", r"K_0=X,qquad"),
    ],
    "en212": [
        (r"the $(n+1)$-fold fiber power of $(R,p_1)$ over $X$", r"the $n$-fold fiber power of $(R,p_1)$ over $X$"),
        (r"K_0=R,qquad", r"K_0=X,qquad"),
    ],
    "fr221": [
        ("transforment encore ensembles limités", "transforment encore des ensembles limités"),
        ("coupe au morceaux", "coupe en morceaux"),
        (r"0\longrightarrow\mathcal G_{T_1}\longrightarrow\mathcal G'' \longrightarrow\mathcal G'_{T_1}\longrightarrow0", r"0\longrightarrow\mathcal G'_{T_1}\longrightarrow\mathcal G'' \longrightarrow\mathcal G_{T_1}\longrightarrow0"),
        ("famille limitée de classe de faisceaux", "famille limitée de classes de faisceaux"),
        ("transforme Modules $S'$-plats", "transforme les Modules $S'$-plats"),
        ("modules localisés de $N$ pour", "modules localisés de $N_*$ pour"),
        ("remplacer $S$ par l'ouvert $U$", "remplacer $S$ par l'ouvert $U_\\infty$"),
        ("sous-schémas fermés de $Z$, donc", "sous-schémas fermés de $S$, donc"),
        ("(telle qu'il s'introduit", "(tel qu'il s'introduit"),
        ("simple ([3], IV) sur $S$,", "simple ([3], IV) sur $S'$,"),
        ("normal sur $S$ (i.e.", "normal sur $S'$ (i.e."),
        ("des $S$-intersections complètes", "des $S'$-intersections complètes"),
        ("locales dans $X$ relativement", "locales dans $X'$ relativement"),
        ("relativement à $S$ (i.e.", "relativement à $S'$ (i.e."),
        ("dans les $X_{s'}$", "dans les $X'_{s'}$"),
        (r"Soient $\mathcal L$ (resp. $\mathcal M$)", r"Soit $\mathcal L$ (resp. $\mathcal M$)"),
    ],
    "en221": [
        (r"0\longrightarrow\mathcal G_{T_1}\longrightarrow\mathcal G'' \longrightarrow\mathcal G'_{T_1}\longrightarrow0", r"0\longrightarrow\mathcal G'_{T_1}\longrightarrow\mathcal G'' \longrightarrow\mathcal G_{T_1}\longrightarrow0"),
        ("localizations of $N$ at", "localizations of $N_*$ at"),
        ("replace $S$ by the open set $U$", "replace $S$ by the open set $U_\\infty$"),
        ("closed subschemes of $Z$, and hence", "closed subschemes of $S$, and hence"),
        ("over $S$, respectively normal", "over $S'$, respectively normal"),
        ("normal over $S$ (that is", "normal over $S'$ (that is"),
        ("a relative local complete intersection", "an $S'$-local complete intersection"),
        ("in $X$ over $S$ (that is", "in $X'$ over $S'$ (that is"),
        ("in the $X_{s'}$", "in the $X'_{s'}$"),
    ],
}

STRUCTURAL_PATTERNS = {
    "src": r"\\src\{",
    "result": r"\\result\{",
    "fsection": r"\\fsection\{",
    "begin": r"\\begin\{",
    "end": r"\\end\{",
    "display_open": r"\\\[",
    "display_close": r"\\\]",
    "inline_math_delimiters": r"(?<!\\)\$",
}


def overlay_replay(key: str, baseline: str, live: str) -> dict:
    baseline_body = norm(strip_footnotes(baseline))
    live_body = norm(strip_footnotes(live))
    replay = baseline_body
    checks = []
    for old, new in REPLACEMENTS[key]:
        old_n, new_n = norm(old), norm(new)
        count = replay.count(old_n)
        if count != 1:
            raise AssertionError(f"{key}: preimage count {count} for {old_n!r}")
        replay = replay.replace(old_n, new_n, 1)
        checks.append({"old": old, "new": new, "preimage_matches": count})
    if replay != live_body:
        raise AssertionError(f"{key}: declared overlay does not reconstruct live reader body")
    before_structure = {name: len(re.findall(pattern, baseline_body)) for name, pattern in STRUCTURAL_PATTERNS.items()}
    after_structure = {name: len(re.findall(pattern, live_body)) for name, pattern in STRUCTURAL_PATTERNS.items()}
    expected_after = dict(before_structure)
    # English ERR-0013 makes the previously implicit relative base explicit as
    # the single inline-math atom $S'$.  This intentionally adds one math span
    # (two delimiters) and is itself a declared semantic correction.
    if key == "en221":
        expected_after["inline_math_delimiters"] += 2
    if expected_after != after_structure:
        raise AssertionError(f"{key}: undeclared structural topology change: {expected_after} != {after_structure}")
    if baseline_body.count("{") != baseline_body.count("}") or live_body.count("{") != live_body.count("}"):
        raise AssertionError(f"{key}: unbalanced braces")
    return {
        "declared_replacements": checks,
        "normalized_body_exact_after_declared_overlay": True,
        "structural_topology_before": before_structure,
        "structural_topology_after": after_structure,
        "braces_balanced": True,
    }


def tree_digest(files: list[Path], base: Path) -> str:
    serial = b""
    for path in sorted(files, key=lambda p: p.relative_to(base).as_posix()):
        data = path.read_bytes()
        rel = path.relative_to(base).as_posix()
        serial += f"{rel}\0{len(data)}\0{sha(data)}\n".encode("utf-8")
    return sha(serial)


def main() -> None:
    originals = []
    for line in MASTER.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            if row.get("master_schema") in {"fga_canon_intake_master/v1", "fga_canon_intake_master/v2"}:
                originals.append(row)
    provisional_ids = [row["provisional_id"] for row in originals]
    assert len(originals) == 18 and len(set(provisional_ids)) == 18

    source_results = {}
    for key, rel in PATHS.items():
        baseline_bytes = git_preimage(rel)
        live_path = ROOT / rel
        live_bytes = live_path.read_bytes()
        assert sha(baseline_bytes) == BASE_SHA[key]
        assert sha(live_bytes) == LIVE_SHA[key]
        source_results[key] = {
            "path": rel,
            "baseline": {"bytes": len(baseline_bytes), "sha256": sha(baseline_bytes)},
            "live": {"bytes": len(live_bytes), "sha256": sha(live_bytes)},
            "replay": overlay_replay(key, baseline_bytes.decode("utf-8"), live_bytes.decode("utf-8")),
        }

    stable_ids = [f"FGA-CANON-ERR-{n:04d}" for n in range(1, 18)]
    for lang in ("fr", "en"):
        text = (FGA / lang / "212.tex").read_text(encoding="utf-8") + (FGA / lang / "221.tex").read_text(encoding="utf-8")
        counts = Counter(re.findall(r"FGA-CANON-ERR-\d{4}", text))
        for stable_id in stable_ids:
            assert counts[stable_id] >= 1, (lang, stable_id, counts[stable_id])

    sem_path = FGA / "ed/sem.json"
    sem = json.loads(sem_path.read_text(encoding="utf-8"))
    assert sem["status"] == "PASS" and not sem["errors"]

    log_forbidden = re.compile(
        r"(^! )|(Undefined control sequence)|(LaTeX Error)|(Emergency stop)|(Fatal error)|"
        r"(Missing character)|(Overfull \\[hv]box)|(undefined references)|"
        r"(Citation .* undefined)|(Rerun to get cross-references right)",
        re.IGNORECASE | re.MULTILINE,
    )
    builds = {}
    expected_build = {
        "fr": (154, "150D3C6D73105116BB1BD53C89B13789E4CB08276CF5C859BEA8A418C6762EA1", "768A800238ABC098BCB1A0D9F5B1F9231E625ED24698660B8F733261C26D269E"),
        "en": (149, "AD7AECDFA01484DF2B98513E0C3644E20D82FF7546190A516C3A3DFAD9683C71", "D6EBE2EEBA655FECDDC50FC9621A22F0E9D06CD58D8D2B7FAEA12BD2AAD6D250"),
    }
    for lang, (pages_expected, pdf_sha, log_sha) in expected_build.items():
        pdf = FGA / f"out/{lang}/main.pdf"
        log = FGA / f"out/{lang}/main.log"
        pdf_bytes, log_bytes = pdf.read_bytes(), log.read_bytes()
        assert sha(pdf_bytes) == pdf_sha and sha(log_bytes) == log_sha
        assert not log_forbidden.search(log_bytes.decode("utf-8", errors="replace"))
        reader = PdfReader(str(pdf))
        assert len(reader.pages) == pages_expected
        extracted = "\n".join((page.extract_text() or "") for page in reader.pages)
        for stable_id in stable_ids:
            assert stable_id in extracted
        builds[lang] = {
            "pdf": {"path": pdf.relative_to(ROOT).as_posix(), "bytes": len(pdf_bytes), "sha256": pdf_sha, "pages": pages_expected},
            "log": {"path": log.relative_to(ROOT).as_posix(), "bytes": len(log_bytes), "sha256": log_sha, "blocking_diagnostics": 0},
            "all_17_provenance_ids_extract": True,
        }

    qa_root = FGA / "qa/fga-canon-errata-0001-0017-20260830"
    page_pngs = list(qa_root.glob("*/page-*.png"))
    contact_pngs = list(qa_root.glob("*/contact-*.png"))
    assert len(page_pngs) == 25 and len(contact_pngs) == 5

    receipt = {
        "schema": "fga_canon_errata_implementation_qa/v1",
        "status": "PASS",
        "date": "2026-08-30",
        "scope": "FGA Exposes 212 and 221; FGA-CANON-ERR-0001 through FGA-CANON-ERR-0017",
        "intake": {"master_path": MASTER.relative_to(ROOT).as_posix(), "provisional_records": 18, "unique_provisional_ids": 18},
        "adjudication": {
            "accepted_provisional_records": 18,
            "stable_dispositions": 17,
            "linked_deduplication": {"stable_id": "FGA-CANON-ERR-0001", "provisional_records": 2},
            "rejected": 0,
            "authority_witness_bytes_modified": 0,
        },
        "implementation": {
            "french_stable_issues_with_reader_correction_or_explicit_provenance": 17,
            "french_semantic_operations": 19,
            "english_stable_issues_with_semantic_rewrite": 6,
            "english_semantic_operations": 13,
            "english_stable_issues_already_idiomatic_or_correct_with_provenance_only": 11,
            "source_units": source_results,
        },
        "semantic_validation": {"path": sem_path.relative_to(ROOT).as_posix(), "bytes": sem_path.stat().st_size, "sha256": sha(sem_path.read_bytes()), "status": "PASS"},
        "builds": builds,
        "visual_qa": {
            "status": "PASS",
            "changed_pages_rendered_and_inspected": 25,
            "contact_sheets_inspected": 5,
            "blocking_layout_defects": 0,
            "root": qa_root.relative_to(ROOT).as_posix(),
            "page_tree_sha256": tree_digest(page_pngs, qa_root),
            "contact_tree_sha256": tree_digest(contact_pngs, qa_root),
        },
        "publication": {"performed": False, "reason": "bounded implementation/QA handoff; no complete release-lineage transaction was established in this bounded step"},
        "nonhuman_blockers": [],
    }
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": "PASS", "receipt": str(OUT), "receipt_bytes": OUT.stat().st_size, "receipt_sha256": sha(OUT.read_bytes())}, indent=2))


if __name__ == "__main__":
    main()
