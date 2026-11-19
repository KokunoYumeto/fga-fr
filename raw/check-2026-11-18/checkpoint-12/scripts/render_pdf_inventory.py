"""Render a relative-path PDF page plan into temporary PNG assets.

This helper checks file provenance and PNG structure, but performs no image,
content, typography, or visual-quality inspection. It never writes source trees.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from datetime import datetime, timezone
import hashlib
from pathlib import Path, PurePosixPath
import struct
import subprocess

from pypdf import PdfReader


BASE = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_path(workspace, value, temporary=False):
    rel = PurePosixPath(value)
    if rel.is_absolute() or ".." in rel.parts or not rel.parts:
        raise ValueError("Expected a relative workspace path")
    if temporary and rel.parts[0] != "tmp":
        raise ValueError("Generated assets and inventories must stay under tmp")
    result = workspace / rel
    if not result.resolve().is_relative_to(workspace):
        raise ValueError("A planned path leaves the workspace")
    if temporary and (result.resolve() == BASE or BASE in result.resolve().parents):
        raise ValueError("Generated raster assets cannot be written in the deliverable tree")
    return result


def render_one(workspace, row, version):
    pdf = relative_path(workspace, row["pdf_path"])
    png = relative_path(workspace, row["image_path"], temporary=True)
    page, dpi = int(row["pdf_physical_page"]), int(row["dpi"])
    png.parent.mkdir(parents=True, exist_ok=True)
    command = ["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(dpi),
               "-png", "-singlefile", str(pdf), str(png.with_suffix(""))]
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if result.returncode:
        log = png.with_suffix(".render-error.log")
        log.write_bytes(result.stderr)
        raise RuntimeError("Rendering failed for " + row["layer"] + " page " + str(page))
    data = png.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise RuntimeError("Renderer did not produce the expected PNG structure")
    width, height = struct.unpack(">II", data[16:24])
    if not width or not height or len(data) < 100:
        raise RuntimeError("Rendered PNG has invalid dimensions or size")
    return dict(row, image_sha256=hashlib.sha256(data).hexdigest(),
                image_bytes=len(data), width_pixels=width, height_pixels=height,
                renderer=version,
                rendered_utc=datetime.now(timezone.utc).isoformat(),
                visual_review="rendered; not inspected")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--plan", required=True, help="relative TSV path")
    parser.add_argument("--inventory", required=True, help="relative output TSV under tmp")
    parser.add_argument("--jobs", type=int, default=2, choices=range(1, 5))
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    plan = relative_path(workspace, args.plan)
    inventory = relative_path(workspace, args.inventory, temporary=True)
    with plan.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    required = {"layer", "build_stage", "source_tree_sha256", "pdf_path", "pdf_sha256",
                "pdf_pages_total", "pdf_physical_page", "reason", "image_path", "dpi"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError("The render plan is empty or lacks required provenance columns")
    images, identities, pdfs = set(), set(), {}
    for row in rows:
        relative_path(workspace, row["image_path"], temporary=True)
        identity = (row["layer"], int(row["pdf_physical_page"]))
        if row["image_path"] in images or identity in identities:
            raise ValueError("The plan contains duplicate output images or layer/page identities")
        images.add(row["image_path"])
        identities.add(identity)
        pdf = relative_path(workspace, row["pdf_path"])
        expected = (row["pdf_sha256"], int(row["pdf_pages_total"]), row["source_tree_sha256"])
        if pdf in pdfs and pdfs[pdf] != expected:
            raise ValueError("Conflicting PDF provenance in render plan")
        pdfs[pdf] = expected
        if not 1 <= int(row["pdf_physical_page"]) <= expected[1]:
            raise ValueError("Physical page outside the recorded PDF range")
        if not 72 <= int(row["dpi"]) <= 600:
            raise ValueError("DPI must be between 72 and 600")
    for pdf, (expected_sha, expected_pages, source_sha) in pdfs.items():
        if digest(pdf) != expected_sha or len(PdfReader(pdf).pages) != expected_pages:
            raise ValueError("PDF differs from its recorded hash or page count; regenerate the plan")
    version_result = subprocess.run(["pdftoppm", "-v"], stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True, check=True)
    version = version_result.stdout.splitlines()[0]
    rendered = {}
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(render_one, workspace, row, version): row for row in rows}
        for completed, future in enumerate(as_completed(futures), 1):
            result = future.result()
            rendered[(result["layer"], int(result["pdf_physical_page"]))] = result
            if completed % 20 == 0 or completed == len(rows):
                print("Rendered " + str(completed) + " of " + str(len(rows)) + " planned pages.", flush=True)
    for pdf, (expected_sha, expected_pages, source_sha) in pdfs.items():
        if digest(pdf) != expected_sha:
            raise RuntimeError("A frozen PDF changed during rendering")
    final = [rendered[(row["layer"], int(row["pdf_physical_page"]))] for row in rows]
    inventory.parent.mkdir(parents=True, exist_ok=True)
    temporary_inventory = inventory.with_suffix(inventory.suffix + ".pending")
    with temporary_inventory.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(final[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(final)
    temporary_inventory.replace(inventory)
    print("Finished " + str(len(final)) + " PNG assets; visual and content review remain unperformed.")


if __name__ == "__main__":
    main()
