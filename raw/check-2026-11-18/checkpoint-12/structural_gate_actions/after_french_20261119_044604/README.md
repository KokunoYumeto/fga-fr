# Mechanical action candidates after the first French reading

This report is bound to the 20,729-row correction ledger and 786-event input of `tmp/structural_gate_after_french`, plus the French source capture at 2026-11-19T04:46:04 UTC. It contains structural metadata and owner-action candidates only; no correction, check, refutation, source wording or mathematics was adjudicated. No live source, ledger, record, progress or rights file was changed.

## Findings for owner action

- `MALFORMED_ROW.json`: C000214 (physical ledger line 410) has the expected ten fields but an invalid confidence category. Whitespace/case normalization supplies no allowed value; a replacement requires root's judgment. The identical row is present in original checkpoint 05.
- `DUPLICATE_ACTION_CANDIDATES.tsv`: two exact duplicate groups predate this run. Metadata-only candidates keep C003871/C003872 and remove their exact repetitions C003873/C003874. These IDs bind to the frozen ledger hash, so current row identities must be checked before any edit.
- `FRENCH_SOURCE_LOCATORS.tsv`: 108 exact frozen-source locators cover all 54 page keys reported as missing literal source pointers. Six corrected-French 149 locators are flagged stale after root's reported footnote removals. French 212 is stale in provenance but contributes no gap here. These are pointer-format gaps, not a determination that page reading was omitted.
- `RECORD_TARGETS.tsv`: page key 232-149 has two record headings. Root must choose the intended insertion target.
- `HOW_MAPPING_CANDIDATES.tsv` and `HOW_MAPPING_RULES.json`: all 23 nonlegacy how values fit three explicit lexical patterns. Fourteen have the legacy refutation-category string as a lexical candidate and nine have `targeted proof check` as a lexical candidate. Opaque ID/subtype hashes remain recorded; no check, proof or refutation is inferred to have occurred.

`CHECKPOINT_ROW_PROVENANCE.tsv` binds the malformed row and duplicate groups byte-for-byte to the original supplied checkpoint archive. `INPUT_PROVENANCE.json` records source, ledger, event and gate hashes and capture times. `FRENCH_SOURCE_HASHES.tsv` binds source locators. `ACTIONS_SUMMARY.json` provides aggregate counts and the zero-failure structural audit status.

Root's later 12 correction rows for editorial-footnote removals and subsequent reconciliation or translation edits are deliberately excluded. Current live inputs were not reread for this report. The underlying gate remains a historical partial-stage result; it does not certify final task coverage.
