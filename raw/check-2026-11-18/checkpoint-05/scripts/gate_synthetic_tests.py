#!/usr/bin/env python3
"""Synthetic-only coverage/privacy gate tests; no real audit or archive action."""
import io
import json
from pathlib import Path
import tempfile
import validate_fga as validator
import final_zip as packager
from privacy_scan import scan_bytes


def run():
    results = []
    def check(name, condition, status="PASS"):
        assert condition, name
        results.append({"test": name, "status": status})
    with tempfile.TemporaryDirectory(prefix="fga-gate-fixture-") as temporary:
        root = Path(temporary)
        work = root / "work"; work.mkdir()
        blocks = {("fr", "149"): "### 149-169\nfr/fr/149.tex\nfr_printed/fr/149.tex\n"}
        progress = ["2026-11-18T00:00:00Z", "page 149-169 done 2026-11-18T00:00:00Z"]
        for layer in validator.LAYERS:
            if layer in {"fr", "fr_printed"}: continue
            for unit in (["149"] if layer == "es_149_printed" else validator.UNITS):
                blocks[(layer, unit)] = "### " + layer + " " + unit + "\n" + validator.source_path(layer, unit) + "\n"
                progress.append(layer + " " + unit + " done 2026-11-18T00:00:00Z")
        (work / "progress.log").write_text("\n".join(progress) + "\n")
        expected = [{"unit": "149", "printed_page": 169, "volume": 1, "scan": "synthetic.pdf", "scan_pdf_page": 2}]
        def coverage(values):
            (work / "CHECK_RECORD.md").write_text("\n".join(values.values()))
            return validator.coverage(work, expected)
        def missing(rows):
            return sum(not r["source_locator_present"] or not (r["own_completion_count"] or r["parent_completion_count"]) for r in rows)
        pages, translations, duplicates = coverage(blocks)
        check("all 137 translation layer/unit slots enumerated", len(translations) == 137 and missing(translations) == 0 and not duplicates)
        for key in [("en", "149"), ("en", "e149"), ("en", "com"), ("es_149_printed", "149")]:
            reduced = dict(blocks); del reduced[key]
            check("missing section detected: " + "/".join(key), missing(coverage(reduced)[1]) == 1)
        check("missing full English language detected", missing(coverage({k:v for k,v in blocks.items() if k[0] != "en"})[1]) == 17)
        fenced = dict(blocks); fenced[("en", "149")] = "```text\n" + fenced[("en", "149")] + "```\n"
        check("fenced pseudo-heading ignored", missing(coverage(fenced)[1]) == 1)
        tildes = dict(blocks); tildes[("en", "149")] = "~~~~text\n" + tildes[("en", "149")] + "~~~\n~~~~\n"
        check("tilde fences respect opening marker length", missing(coverage(tildes)[1]) == 1)
        backup = dict(blocks)
        backup[("en", "149")] = backup[("en", "149")].replace("149.tex", "149.tex.bak")
        check("backup suffix rejected as a source locator", missing(coverage(backup)[1]) == 1)
        unicode_suffix = dict(blocks); unicode_suffix[("en", "149")] = unicode_suffix[("en", "149")].replace("149.tex", "149.tex旧")
        check("Unicode filename suffix rejected", missing(coverage(unicode_suffix)[1]) == 1)
        annotated = dict(blocks); annotated[("en", "149")] = annotated[("en", "149")].replace("149.tex", "149.tex:12")
        check("source line annotation remains a valid locator", missing(coverage(annotated)[1]) == 0)
        combined = dict(blocks); del combined[("pt-BR_printed", "149")]
        combined[("pt-BR", "149")] += validator.source_path("pt-BR_printed", "149") + "\n"
        reduced_progress = [line for line in progress if not line.startswith("pt-BR_printed 149 done ")]
        (work / "progress.log").write_text("\n".join(reduced_progress) + "\n")
        check("existing combined-parent variant rule retained", missing(coverage(combined)[1]) == 0)
        (work / "progress.log").write_text("\n".join(progress) + "\n")
        # Gate consumer tests require only synthetic metadata, never PDFs or an archive.
        reports = root / "gate"; reports.mkdir()
        entries = {"pdf/FGA_" + layer + ".pdf": {"bytes": 1, "sha256": "0" * 64} for layer in packager.LAYERS}
        entries["sources/fixture.tex"] = {"bytes": 1, "sha256": "1" * 64}
        files = [{"path": name, **value} for name, value in entries.items()]
        pdfs = [{"layer": layer, "file": "pdf/FGA_" + layer + ".pdf", "status": "present with pages", "pages": 1,
                 "sha256": "0" * 64, "inspection": "synthetic metadata"} for layer in packager.LAYERS]
        sources = [{"path": "sources/fixture.tex", "baseline_member": "fixture", "status": "identical to baseline",
                    "bytes": 1, "sha256": "1" * 64, "baseline_sha256": "1" * 64}]
        for name, rows in [("FILE_INVENTORY.tsv", files), ("PDF_INVENTORY.tsv", pdfs), ("SOURCE_INVENTORY.tsv", sources)]:
            (reports / name).write_bytes(packager.table_bytes(packager.SCHEMAS[name], rows))
        summary = {name: 0 for name in packager.GAP_FIELDS}
        summary.update(mode="structural enforcement", completion_certified=False, scan_unit_page_occurrences=1,
                       expected_translation_layer_units=137, protected_files_compared=1, protected_files_identical=1)
        try:
            packager.require_gate(summary, reports, entries, set()); blocked = False
        except packager.PackageError: blocked = True
        check("packager requires fresh coverage tables", blocked)
        for name, rows in [("PAGE_COVERAGE.tsv", pages), ("TRANSLATION_COVERAGE.tsv", translations)]:
            (reports / name).write_bytes(packager.table_bytes(packager.SCHEMAS[name], rows))
        packager.require_gate(summary, reports, entries, set())
        (reports / "TRANSLATION_COVERAGE.tsv").write_bytes(packager.table_bytes(packager.SCHEMAS["TRANSLATION_COVERAGE.tsv"], translations[:-1]))
        try:
            packager.require_gate(summary, reports, entries, set()); blocked = False
        except packager.PackageError: blocked = True
        check("packager rejects an omitted layer/unit coverage row", blocked)
        (reports / "TRANSLATION_COVERAGE.tsv").write_bytes(packager.table_bytes(packager.SCHEMAS["TRANSLATION_COVERAGE.tsv"], translations))
        for field in ["page_occurrences_with_structural_gaps", "translation_layer_units_with_structural_gaps", "privacy_pattern_findings"]:
            try:
                packager.require_gate(dict(summary, **{field: 1}), reports, entries, set())
                blocked = False
            except packager.PackageError: blocked = True
            check("packager blocks " + field, blocked)
        address = "synthetic" + chr(64) + "example.invalid"
        absolute = "/" + "home" + "/" + "synthetic" + "/fixture"
        for filename, payload in [("fixture.sty", address.encode()), ("BUILD", absolute.encode()),
                                  ("fixture.txt", address.encode("utf-16")), ("fixture.html", address.encode())]:
            check("decoded text scanned: " + filename, bool(scan_bytes(filename, payload)[0]))
        unicode_path = "/" + "home" + "/" + "検証" + "/fixture.txt"
        check("Unicode absolute path components detected", bool(scan_bytes("fixture.txt", unicode_path.encode())[0]))
        (work / "fixture.sty").write_text(address)
        _, privacy_findings, _ = validator.deliverable_inventory(work, root / "private-output", set())
        check("validator integration scans included text beyond old extension list", any(row["file"] == "fixture.sty" for row in privacy_findings))
        for relative in ["sources/fr/fr/149.tex", ".." + "/" + "home" + "/fixture", "." + "/" + "tmp" + "/fixture"]:
            check("relative path accepted", not scan_bytes("fixture.txt", relative.encode())[0])
        check("concatenated directory fragment allowed", not scan_bytes("fixture.py", b'return layer + "/fr/" + unit + ".tex"')[0])
        check("TeX source-marker regex is not a network path", not scan_bytes("fixture.py", r'regex = rb"\\src\s*\{(\d+)\}"'.encode())[0])
        windows = "Q:" + chr(92) + "data" + chr(92) + "fixture.txt"
        network = chr(92) * 2 + "server" + chr(92) + "share" + chr(92) + "fixture.txt"
        check("Windows absolute path detected", bool(scan_bytes("fixture.txt", windows.encode())[0]))
        check("UNC network path detected", bool(scan_bytes("fixture.txt", network.encode())[0]))
        check("private interpreter shebang detected", bool(scan_bytes("fixture.py", ("#!" + absolute + "\n").encode())[0]))
        check("portable interpreter shebang allowed", not scan_bytes("fixture.py", ("#!" + "/" + "usr/bin/env python3\n").encode())[0])
        # Synthetic PDF content is created in memory and never rendered.
        from pypdf import PdfWriter
        from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject
        def pdf(text, metadata):
            writer = PdfWriter(); page = writer.add_blank_page(width=100, height=100)
            font = DictionaryObject({NameObject("/Type"): NameObject("/Font"), NameObject("/Subtype"): NameObject("/Type1"), NameObject("/BaseFont"): NameObject("/Helvetica")})
            page[NameObject("/Resources")] = DictionaryObject({NameObject("/Font"): DictionaryObject({NameObject("/F1"): writer._add_object(font)})})
            stream = DecodedStreamObject(); stream.set_data(("BT /F1 9 Tf 5 50 Td (" + text + ") Tj ET").encode())
            page[NameObject("/Contents")] = writer._add_object(stream)
            writer.add_metadata({"/Subject": metadata}); output = io.BytesIO(); writer.write(output); return output.getvalue()
        check("PDF extractable visible text scanned", bool(scan_bytes("fixture.pdf", pdf(address, "synthetic"))[0]))
        check("PDF metadata scanned", bool(scan_bytes("fixture.pdf", pdf("synthetic", address))[0]))
        (reports / "fresh.md").write_text(address)
        try:
            packager.generated_files(summary, reports, entries, [], pdfs); blocked = False
        except packager.PackageError: blocked = True
        check("new generated package text rescreened", blocked)
    return results


if __name__ == "__main__":
    print(json.dumps({"synthetic_only": True, "real_audit_examined": False, "results": run()}, indent=2))
