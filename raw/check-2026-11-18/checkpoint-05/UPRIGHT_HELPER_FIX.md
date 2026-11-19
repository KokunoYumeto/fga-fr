# Upright-display count fix

Verified: **2026-11-18 20:07:45 UTC**.

`scripts/audit_utils.py` now processes each identical numbered or unnumbered display block once per page-stage snapshot and passes its exact observed occurrence count to `replace()`. The existing replacement helper rechecks that count against the current page before writing; its page scoping, file writing, ledger schema, and ledger append behavior are unchanged.

Identical replacements still produce one aggregate correction row. **Each affected place still needs later individual ledger treatment and review.** This helper does not perform or certify that work.

Synthetic verification passed: **3 test methods, 8 cases** covering repeated numbered displays, tags, unnumbered and aligned displays, neighboring-page isolation, distinct blocks, no additional changes on a completed helper rerun, and refusal when an occurrence is added between observation and replacement. The mismatch fixtures produced no correction row or formatted replacement. Both changed Python files also compiled with zero warnings.

```sh
python -B work/scripts/test_upright_page.py
```

The tests redirect helper access to temporary fixtures. No apply script, edition, existing ledger, audit record, scan, or context file was executed or opened. No build, real validator, or archive operation ran.

Helper SHA-256 before: `80f5a995d2ddfa23e9037419e55eca9672552c69e38c2e6dccea85b9df1b56a2`.

Helper SHA-256 after: `f03de162dd4ef05f1cb6166230550d2419aa60b30d8c9bcbc80a0fec9acfff39`.
