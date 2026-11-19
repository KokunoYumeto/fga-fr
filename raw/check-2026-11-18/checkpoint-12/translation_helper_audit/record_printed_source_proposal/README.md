# Printed French source selection proposal

Status: **unapplied**. `PROPOSED.diff` changes only two lines of `scripts/translation_edits.py`: it appends `printed=False` after the existing `entry_lines=None` parameter and chooses `fr_printed` when that flag is true, otherwise `fr`. The expression matches the existing `show_math` and `align_math` source-selection rule.

All six existing positional slots retain their names, order and defaults. Existing five-argument calls, six-argument calls with `None` or an entry-line tuple, and keyword `entry_lines` calls produce byte-identical record and progress output under the proposal. Explicit `printed=False` also produces identical output. `printed=True` can be supplied as a keyword or seventh positional argument; the keyword form is clearer at call sites.

The isolated checks execute only the old/proposed recording function and the existing `read`/`page_text` functions. They use frozen source bytes and temporary output files. For printed page 177 of exposé 149, the expected French path and line boundaries were independently calculated from raw marker offsets. `printed=True` writes the exact printed-French path/range; the only output change is that French locator. The translation locator, entry-line text, body, fixed timestamp and progress bytes remain unchanged. No source prose, formula, scan or evidence claim is judged by these checks.

`PREIMAGE_AND_CHANGE.json` gives exact two-line old/new UTF-8 bytes and full-file preimage/proposed hashes. `INPUT_CAPTURE.json` binds the five frozen inputs. `CHECKS.json` records the checks and exact source ranges. The test driver remains at `tmp/record_printed_source_proposal_20261119.py`; temporary synthetic records remain under `tmp/record_printed_source_proposal_20261119/runs/` and are not production records.

Root should verify the preimage hash and review the diff before applying. No production helper, source, ledger, record, event or progress file was changed.

## Existing callers

The independent AST inventory found 44 existing calls, all with six positional arguments and no keywords, `*args`, or `**kwargs`. The sixth argument remains `entry_lines`; `printed` defaults to `False`. See `CALLER_SIGNATURE_CHECK.json`, `CALLERS.json`, and `CALLER_CODE_HASHES.json`. Wildcard imports are present; no explicit aliases or unresolved attribute calls were found. Dynamic rebinding is outside this static check. A separate distinct-line sentinel check records exactly the printed branch's line range (40–50), never the corrected branch's range (20–30), and verifies both `page_text` call arguments.
