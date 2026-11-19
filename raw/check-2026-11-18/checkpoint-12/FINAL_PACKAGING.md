# Final package helper

`scripts/final_zip.py` prepares the single `FGA_CHECK.zip` deliverable from a complete current work tree. It preserves every previous checkpoint and never overwrites an existing final archive. No source, ledger, audit record, or build is edited or executed by the packager. It invokes the existing read-only validator for a fresh structural gate, then packages opaque file bytes. No separate human-approval flag or content-certification claim is introduced.

## Usage

From the directory containing `work/`, first pause edits and run:

```sh
python -B work/scripts/final_zip.py --dry-run
```

Dry run uses the same fresh validator gate, eleven-PDF checks, temporary compression, size limit, and ZIP/member-integrity checks as publication. It retains private diagnostic reports but publishes no archive. It is not a shortcut around unfinished audit work.

After the human audit and the dry run succeed, publish with:

```sh
python -B work/scripts/final_zip.py
```

The default destination is the sibling `final/FGA_CHECK.zip`. The command refuses an existing destination, including a symbolic link; choose a different `--output-dir` to preserve and supersede an earlier final without overwriting it. The archive directory and `--private-dir` must remain outside the work tree. Private run reports default to `runtime/final_packaging/` beside `work/`; each attempt uses a new directory. Raw validator output stays there and is excluded from delivery.

Override input locations when necessary:

```sh
python -B work/scripts/final_zip.py --dry-run --sources-zip upload/FGA_sources.zip --scans-zip upload/FGA_scans.zip --context-zip upload/FGA_context.zip
```

The supplied archives otherwise follow the validator's normal sibling `upload/` defaults. `--work` selects a moved complete deliverable tree. `--pdf-map` is passed to the validator; every mapped layer PDF must be a distinct nonempty file under `pdf/`. Repeat `--allow-image relative/path.png` only for evidence images intentionally retained under the existing packaging policy. The validator and packager receive the same image selection. A source file excluded by packaging policy causes failure instead of silently producing an incomplete source tree.

## Required mechanical gate

The helper always invokes `scripts/validate_fga.py --enforce-structure` into a new private report directory. There is no skip-gate option and no acceptance of a stale externally supplied success report. A successful validator exit and its exact structural-enforcement summary are required, including zero reported schema, recognized coverage, duplicate-marker, protected-front-matter, presence, manifest, and privacy gaps. The summary must still say that completion is not certified.

The packager also requires the fresh page and translation coverage TSVs with exact schemas, checks the page count against the summary, requires every translation layer/unit exactly once, and rejects unresolved structural markers. It checks the validator's current file inventory against the work snapshot by filename, byte count, and SHA-256. It requires every inventoried source file in the package. It also checks the PDF inventory schema and requires each of the eleven configured layers exactly once, with a readable-with-pages status, positive page count, distinct `pdf/` path, nonempty current file, and matching hash. It does not open PDF page contents itself.

Any missing requirement, stale hash, changed file set, malformed report, failing gate, missing PDF, unsupported symbolic link, or archive-integrity problem blocks publication. The command prints a clear blocked status and exits nonzero. Failed validator attempts retain their private reports for diagnosis; the packager does not repair or reinterpret the findings.

## Archive contents and integrity

The archive contains the complete included work tree, including all current source trees, PDFs, scripts, and audit deliverables. No unchanged deliverable is omitted in favor of an earlier checkpoint. Existing checkpoint exclusions apply; supplied inputs, runtime/cache trees, renders, temporary material, raw logs other than `progress.log`, every earlier ZIP, and previous generated final-package metadata are excluded. Required inventoried source files cannot be silently excluded.

Fresh mechanical evidence is added as `final_validation/`, `FINAL_READINESS.json`, and `FINAL_PACKAGE.md`. Generated report text is independently privacy-screened before inclusion. The validator also scans all included decodable text regardless of extension and searches extractable PDF page text plus metadata; it allows relative paths. `FINAL_FILE_LIST.tsv` lists all archive members with byte counts and SHA-256 hashes, plus excluded paths and reasons. Its own entry explicitly omits a self-referential hash and byte count; the command separately reports the manifest hash and the complete ZIP hash. Excluded file contents are not read to obtain hashes.

The compressed candidate must be strictly smaller than **500,000,000 bytes**. Before publication, the helper checks ZIP member uniqueness, exact member inventory, CRC integrity, and every member's byte count and SHA-256. It checks work-file stability again before an exclusive, atomic publication step. If the size limit is reached, it publishes nothing and reports that the prompt's multipart fallback requires separate preparation; this helper does not silently split or omit files.

Creating the ZIP does not save or publish it to another service. The calling workflow remains responsible for the final file save and download presentation.

## Human verification and synthetic tests

A passing structural gate does not establish that each page was read, each correction received its second-reading verdict, evidence is sound, mathematical decisions are correct, every translation was checked, meaning changes reached every relevant layer, each PDF came from the current sources, or the required PDF visual checks and inline-credit review occurred. Those remain the human audit's responsibility. Packaging does not add progress completions, change confidence values, or certify content.

Run `python -B work/scripts/final_zip.py --selftest` to exercise temporary synthetic fixtures only. The tests cover schema/gate consumption, all eleven PDF entries, exclusions, complete manifests, ZIP/member integrity, dry-run nonpublication, strict size refusal, existing-archive preservation, work-change refusal, and unchanged prior checkpoints. The fixture PDF bytes and readiness records are explicitly synthetic; the test does not invoke the real validator, inspect an edition or scan, or produce an actual final deliverable. Only these synthetic tests were used while preparing the helper.
