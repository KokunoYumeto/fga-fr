#!/usr/bin/env python3
"""Mechanical privacy patterns for decoded text and extractable PDF text."""
import io
import re

EMAIL = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[^\W\d_]{2,}(?!\w)")
UNIX = re.compile(r"(?<![\w./:\\-])/(?:[\w.~+@%-]+/)+[\w.~+@%-]+")
WINDOWS = re.compile(r"(?<![\w\\])(?:[A-Za-z]:[\\/]+[^\s\"'<>|*?{}\[\]()]+|\\{2,}[\w.-]+[\\/]+[\w.-]+(?:[\\/]+[^\s\"'<>|*?{}\[\]()]+)*)(?=$|[\s\"'<>|,;])")
FILE_URI = re.compile(r"\bfile:(?://)?/[^\s\"'<>]+", re.I)


def decode_text(data):
    encodings = []
    if data.startswith((b"\xff\xfe\x00\x00", b"\x00\x00\xfe\xff")):
        encodings.append("utf-32")
    elif data.startswith((b"\xff\xfe", b"\xfe\xff")):
        encodings.append("utf-16")
    encodings.append("utf-8-sig")
    if b"\x00" in data:
        encodings.extend(["utf-16-le", "utf-16-be", "utf-32-le", "utf-32-be"])
    encodings.append("cp1252")
    for encoding in encodings:
        try:
            text = data.decode(encoding)
        except (UnicodeError, LookupError):
            continue
        if not text or encoding in {"utf-16", "utf-32"} or (encoding == "utf-8-sig" and "\x00" not in text) or sum(char.isprintable() or char in "\n\r\t\f" for char in text) / len(text) >= 0.98:
            return text, encoding
    return None, None


def text_findings(name, text, scope):
    result = []
    for label, pattern in [("email pattern", EMAIL), ("absolute local path pattern", UNIX),
                           ("Windows absolute or network path pattern", WINDOWS), ("local file URI pattern", FILE_URI)]:
        for match in pattern.finditer(text):
            start = text.rfind("\n", 0, match.start()) + 1
            if label == "absolute local path pattern" and text[start:match.start()] == "#!":
                interpreter = text[match.start():].splitlines()[0].split()[0]
                portable = {"/" + path for path in ["usr/bin/env", "usr/bin/python", "usr/bin/python3", "bin/sh", "bin/bash"]}
                if interpreter in portable:
                    continue
            result.append({"file": name, "line": text[:match.start()].count("\n") + 1,
                           "issue": label, "scope": scope + "; matched content omitted"})
    return result


def scan_bytes(name, data):
    if name.lower().endswith(".pdf"):
        from pypdf import PdfReader
        findings = []
        try:
            reader = PdfReader(io.BytesIO(data))
            for key, value in (reader.metadata or {}).items():
                findings += text_findings(name, str(value), "PDF metadata " + str(key))
            metadata = reader.trailer["/Root"].get("/Metadata")
            if metadata is not None:
                decoded, _ = decode_text(metadata.get_object().get_data())
                if decoded is not None:
                    findings += text_findings(name, decoded, "PDF XMP metadata")
            for number, page in enumerate(reader.pages, 1):
                try:
                    findings += text_findings(name, page.extract_text() or "", "PDF extractable visible text page " + str(number))
                except Exception:
                    findings.append({"file": name, "line": "", "issue": "PDF text extraction failed",
                                     "scope": "page " + str(number) + "; privacy coverage incomplete"})
        except Exception:
            findings.append({"file": name, "line": "", "issue": "PDF privacy inspection failed",
                             "scope": "metadata or document could not be read"})
        return findings, "PDF metadata, XMP, and extractable page text searched; raster text and attachments not inspected"
    text, encoding = decode_text(data)
    if text is None:
        return [], "binary or undecodable content not inspected"
    return text_findings(name, text, "decoded text " + encoding), "decoded text searched as " + encoding
