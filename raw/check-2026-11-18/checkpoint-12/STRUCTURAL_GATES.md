# Nonmutating ledger and coverage structural gates

`scripts/ledger_structure.py` checks schemas and literal structural markers. It
does not decide whether corrections, statements, evidence, translations, or
completion claims are valid. It never repairs, normalizes, deduplicates, or
rewrites inputs. Reports contain counts, row/line identifiers, structural keys,
relative source paths, and hashes; correction and evidence text is omitted.

## Frozen result

The retained report is in `structural_gates/snapshot_20261119_025622/`. Its input
copy began at **2026-11-19 02:56:22.170879 UTC** and ended at
**02:56:22.671601 UTC**. Later live progress is outside these metrics.

| Check | Result |
|---|---|
| Correction records | 15,736; exact required header; no malformed field counts |
| Event records | 622; exact required header; no malformed field counts |
| Correction kinds | All fit the allowed set, including support for `terminology` |
| Confidence categories | One issue: correction data row **214**, identifier **C000214**, physical line **410** |
| Exact duplicate corrections | Two groups: data rows **3871/3873** and **3872/3874**; two excess rows |
| Exact duplicate events | None |
| Required source files | All **274** present |
| UTC date/timestamp checks | **963** checked; none invalid |
| French section/completion correspondence | **165** matched page keys; no orphan completions or duplicate keys |
| Pending French page keys | **46** of the pinned 211 expected keys |
| Translation-unit correspondence | No recorded keys; **137** pending layer/unit keys |

The confidence finding is an exact category-set mismatch. No replacement value
is proposed. Exact duplicate groups compare all decoded TSV cell values without
trimming or interpreting them; no conclusion about the underlying corrections
is made. Correction records may span physical lines, so both data-row identifiers
and physical line ranges are retained.

There are **22 event `how` values outside the six legacy exact strings**. These
are advisory by default, because the current log uses additional check labels
and identifiers. Their text is not reproduced. `--strict-legacy-events` promotes
them to schema issues when that exact legacy vocabulary is required. Repeated
event IDs occur in 15 groups and are inventoried separately; they are not treated
as exact duplicate events.

Literal full source locators are inventoried separately from section/completion
correspondence. **44 recorded page sections lack one or both exact French file
locator strings recognized by the parser.** This is not classified as missing
reading or a syntax defect. `--require-source-locators` enables that additional
coverage condition explicitly. The default 46 pending pages count only absent
section/completion correspondence, not these pointer-format observations.

## Running the gates

From the workspace root, use a new report directory:

```sh
python -B FGA_CHECK/scripts/ledger_structure.py --work FGA_CHECK --out tmp/structural_gate_next
python -B FGA_CHECK/scripts/ledger_structure.py --work FGA_CHECK --out tmp/structural_gate_final --require-complete
```

Use a stable or frozen work copy for reproducible metrics. The helper captures
ledger bytes, verifies them again before reporting, and aborts if they changed
during the check. Existing output directories are refused, as are outputs inside
source trees. The frozen run returned exit code **1**, correctly reflecting the
confidence-category issue and duplicate-row flags; intentionally pending coverage
does not itself fail the default mode.

Default exit 0 requires clear syntax, no exact duplicate rows, and no duplicate
section/completion keys. `--require-complete` additionally requires all expected
French and translation correspondence markers. These are structural gates only;
passing them does not certify substantive completion.

The policy file is `scripts/structural_gate_policy.json`. It pins the exact TSV
headers, six correction kinds (`reading`, `misprint of the original`,
`translation`, `typesetting`, `structure`, `terminology`), three confidence
categories (`high`, `medium`, `low`), 211 expected page keys, and 274 required
source paths. Catalog hashes identify the metadata from which the expected sets
were derived. The validator does not open scans or archives.

UTC validation preserves the existing accepted forms: an explicitly UTC timestamp
or a valid date-only value. Precision is recorded. No chronological or substantive
claim is inferred from a timestamp. Informational progress lines are hashed and
inventoried separately from recognized completion markers; line 18, for example,
is not interpreted as a page-completion claim.

French page headings and `page UNIT-PAGE done TIMESTAMP` lines share a unit/page
key. Translation headings and `ALIAS UNIT done TIMESTAMP` lines use the established
layer aliases. The existing parent relationships for Spanish printed 149,
Portuguese printed, and Vietnamese diplomatic are supported; parent sections
qualify for a child only when the child's exact source locator is present.

## Reports, exclusions, and verification

`SUMMARY.json` separates syntax, duplicate flags, advisories, and pending coverage.
The TSV reports list schema issues, duplicate row identifiers/hashes, category
counts, timestamp checks, required sources, heading/progress identifiers, French
and translation coverage, key multiplicities, and repeated event-ID hashes.

The helper reuses the existing `checkpoint_zip.exclude_reason` function and
records its code hash. It does not invent new archive exclusions or invoke any
archive-creation routine. Source/rights files and all live ledgers remain untouched;
only the requested report directory is written.

Independent frozen metrics agree on row counts, the confidence-row identifier,
both duplicate groups, and the 165/46 French correspondence split. Synthetic
non-document fixtures verified malformed field counts, invalid categories,
naive timestamps, missing required files, terminology acceptance, and duplicate
detection. `VALIDATOR_CHECKS.tsv` records those checks without payload text.
