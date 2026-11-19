# Frozen English build blocker

Stage: `en149_complete_193`. The entire English tree and replay metadata were captured at **2026-11-19T05:31:50.613835+00:00–05:31:50.644129+00:00**.

The first LuaLaTeX pass exited 1 at `sources/en/en/149.tex`, line 67, with undefined `\uline`. The literal preceding source marker is 170. No PDF was produced, so page counts, final references, auxiliary stability and complete overflow coverage are unavailable. Passes 2 and 3 did not run after this blocker. Partial diagnostics must not be treated as final book metrics.

The captured English tree has neither a ulem package load nor a local definition of uline/uwave. The successful French preamble loads `\usepackage[normalem]{ulem}`; the package is already available in the pinned runtime.

At root's request, `scripts/repair_en_ulem.py` was prepared but **not executed or applied by support**. It inserts exactly that one package declaration between the existing microtype and graphicx package declarations and uses `audit_utils.replace` to append one low-confidence typesetting row when root applies it. `PREPARED_ULEM_REPAIR.json` pins the exact two-line preimage, postimage and script hash; `PROPOSED_ULEM.patch` shows the one-line insertion. Static checks confirmed a unique preimage, absent postimage, exact inverse replacement and an idempotent two-line anchor. The helper preserves the captured CRLF source convention.

The original frozen replay and compiler inputs remain fixed. Any root-applied repair will be captured and rebuilt under a separate tag. No source, ledger, record, progress or rights bytes were changed by support, and no source meaning, scans or PDF contents were reviewed.
