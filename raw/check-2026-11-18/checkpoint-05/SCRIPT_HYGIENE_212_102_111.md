# Script hygiene: 212 pages 102–111

Snapshot: **2026-11-18 20:23:08 UTC**. Scope is exactly `scripts/apply_212_102.py` through `scripts/apply_212_111.py`; all ten were present and unchanged during this review.

## Static results

All **10 scripts compile**, with **0 syntax errors, 0 warnings, 0 literal no-op candidates, 0 raw-single-quote escaped-apostrophe hazards, and 0 provably unreachable-code candidates**. The literal comparison check also followed each local `r()` wrapper into its `replace()` argument positions. Five synthetic structural assertions passed without executing fixture code. No script was changed or executed.

## Rerun hazards

The scripts contain **45 event calls and 10 page-record calls** at module level without enclosing conditional guards. If reached again, `audit_utils.event()` appends another event row; `record_page()` appends another page section and, by default, another progress completion. Earlier exceptions or replacement checks may stop a rerun before those calls.

| Script | Event-call lines | Page-record call line |
| --- | --- | --- |
| `scripts/apply_212_102.py` | 17–20 | 21 |
| `scripts/apply_212_103.py` | 24–27 | 28 |
| `scripts/apply_212_104.py` | 30–34 | 35 |
| `scripts/apply_212_105.py` | 31–34 | 35 |
| `scripts/apply_212_106.py` | 25–27 | 28 |
| `scripts/apply_212_107.py` | 25–26 | 27 |
| `scripts/apply_212_108.py` | 26–28 | 29 |
| `scripts/apply_212_109.py` | 32–37 | 38 |
| `scripts/apply_212_110.py` | 25–30 | 31 |
| `scripts/apply_212_111.py` | 21–28 | 29 |

`apply_212_109.py` additionally opens `CORRECTIONS.tsv` in append mode at **line 20**. Its three-item literal loop writes rows at **line 26** when the `else` selection branch beginning at line 15 is reached. That selection is not a duplicate-entry guard; repeating this branch appends those three rows again.

The shared `replace()` helper retains its limited preimage/ledger guard. It does not protect subsequent event/page calls or the direct append branch above. These apply scripts therefore remain historical mutation scripts, not an idempotent rebuild procedure.

## Scope and limits

Only Python syntax, tokens, AST structure, and script hashes were examined. Constant-condition and direct-unreachable-statement checks do not establish runtime behavior; literal no-op checks do not decide whether any replacement is correct. No edition text, scan, existing ledger row, audit record, notes, or programme was opened or interpreted. No build, validator, checkpoint, or archive ran.

`SCRIPT_HYGIENE_212_102_111.json` preserves the exact script hashes and call locations. The additional wrapper/control-flow checks are specific to this scoped review; the general checker was not modified.
