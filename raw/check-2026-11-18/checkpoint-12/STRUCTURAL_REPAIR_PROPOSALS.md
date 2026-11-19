# Structural repair proposals for root review

The exact, unapplied proposal package is `structural_repair_proposals/snapshot_20261119_055401/`.

Start with its `README.md` and `PROPOSAL_INDEX.tsv`. Exact old/new bytes and guards are in `ledger_events/OPERATIONS.json` and `locators/LOCATOR_OPERATIONS.json`.

The fixed capture completed at **2026-11-19T05:54:01.099052+00:00**. It reuses the existing after-French action report and refreshes only the named targets. All 83 candidate payloads match their captured old ranges; source/segment bindings and UTF-8 hashes pass. No whole structural gate or substantive review was repeated.

The package contains 69 mechanical candidates: two exact duplicate deletions, 14 legacy spelling changes, and 53 unambiguous locator insertions. Root decisions remain for the confidence category in C000214, nine H03 event-type mappings, and the section target for page 232-149. There are three confidence alternatives and two locator-target alternatives; choosing one of each and approving the remaining proposals would produce 80 changes. Nothing is selected or applied.

Duplicate groups retain C003871/C003872 and propose deleting C003873/C003874, all proven present in checkpoint 05. All event candidates preserve the original `how` verbatim in `where`. The 54 page-key gaps have 108 refreshed source pointers; only the corrected-French 149-177 numeric range changes, from 421-475 to 421-472. Existing section bodies remain byte-identical.

All files use relative paths. Production sources, ledgers, records, events and progress were not changed. Before later application, root must revalidate full-record/section guards against its then-current inputs; captured offsets are not valid merely because a row number looks unchanged.
