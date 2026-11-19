# Structural readiness validator

`scripts/validate_fga.py` inventories the deliverables without changing source files, audit ledgers, notes, progress entries, or PDFs. It writes only its own tables and report under `validation/`. It does not read page text or images, judge mathematics or translations, or certify completion.

## Running the inventory

From the workspace containing `work/` and the original `upload/` attachments:

```sh
python -B work/scripts/validate_fga.py
```

The work directory defaults to the parent of `scripts/`, so the script also works after the complete deliverable tree has been moved. Supply the three original archives explicitly when they are elsewhere:

```sh
python -B scripts/validate_fga.py --sources-zip ../upload/FGA_sources.zip --scans-zip ../upload/FGA_scans.zip --context-zip ../upload/FGA_context.zip
```

Python 3 and `pypdf` are required. The sibling `build_fga.py` and `checkpoint_zip.py` scripts provide the eleven layer definitions and packaging exclusions. No TeX engine is invoked. The default mode returns a readiness inventory even when unfinished work produces gaps. It may overwrite earlier files in its own report directory; retain a checkpoint when an earlier inventory must remain available.

After the independent text, mathematical, translation, and PDF reviews are complete, the optional `--enforce-structure` flag returns a nonzero exit status for the structural gaps it can detect. That flag still does not certify those reviews. It has not been used for the in-progress inventory.

## Exact ledger schemas

`CORRECTIONS.tsv` must have these ten columns, in this order:

```text
file	layer	printed_page	line	statement	old	new	evidence	kind	confidence
```

Allowed kinds are `reading`, `misprint of the original`, `translation`, `typesetting`, and `structure`. Allowed final confidence values are exactly `high`, `medium`, and `low`. Provisional annotations are reported without being rewritten. Data-row numbers count logical TSV records, so embedded newlines do not change them.

`CHECK_EVENTS.tsv` must have these six columns, in this order:

```text
id	date_utc	who	how	result	where
```

Allowed event types are `targeted proof check`, `independent re-proof`, `computation or formal certificate`, `used and rechecked in this run`, `carried as background without fault found`, and `refuted, with the refined statement's id`. Event payloads are tested for presence and are not interpreted.

## Evidence reported

The generated `READINESS.md` gives counts and limitations. Its TSV companions cover original manifest integrity, current file hashes, source inventories, protected credit/rights files, front-matter byte comparisons, ledger schema issues, page and translation markers, duplicate markers, lexical source-page markers, required directories and entry points, eleven PDFs, and privacy patterns.

Page coverage derives expected identifiers from scan filenames and PDF page-tree counts, excluding each scan's cover sheet. It reports unit/page occurrences separately from distinct volume/page identifiers. A recognized page heading and progress completion remain structural evidence only. Literal source-file locators are checked with filename boundaries within the corresponding record section; absent, abbreviated, or backup-suffixed locators are reported as unrecognized evidence. Heading-looking lines inside backtick or tilde code fences are ignored. Translation sections may be separate by layer or combined under a parent language when the variant locator is present. The existing record format is never changed by this tool.

The default PDF names are `pdf/FGA_LAYER.pdf`, with `LAYER` replaced by each configured layer name. Use `--pdf-map relative-map.tsv` for different names; the mapping has `layer` and `file` columns and work-relative paths. PDF presence, readability, page count, hash, and metadata are checked. A separate privacy scan searches extractable PDF text and metadata; mathematical content and visual quality are not evaluated.

Original source files selected by credit/rights-related filenames, together with Korean front matter, are compared byte-for-byte. The added French printed tree is compared with the corresponding original French files. Main-document front-matter blocks are compared separately where their delimiters are present. Other inline credits are not interpreted.

Privacy checks report file and line locations without reproducing matching addresses or paths. Every included decodable text file is searched regardless of extension, including common Unicode encodings. Relative paths are allowed. Only explicitly portable interpreter shebangs are exempt. PDF metadata, XMP, and extractable visible page text are searched; failed extraction blocks the privacy gate. Raster text, attachments, and undecodable binary contents remain unexamined. The file inventory follows checkpoint exclusions and omits its own report directory to avoid self-referential hashes. Pass `--allow-image relative/path.png` for each documented evidence image that packaging will retain.

Run the final inventory with source and audit-record edits paused. An in-progress run samples files while work may continue and must not be treated as an atomic checkpoint or completion certificate.
