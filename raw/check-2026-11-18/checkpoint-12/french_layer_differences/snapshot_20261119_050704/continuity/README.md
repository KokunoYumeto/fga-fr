# Continuity and current declared-projection candidate search

This supplementary report binds the current **05:08:12 UTC** exact inventory to the earlier **04:46:04 UTC** inventory and refreshes the earlier formatting search against the current 69 ordinary-unmatched hunks. It preserves the earlier reports and does not adjudicate or apply any correction.

## Mapping and recorded deletions

All 303 current hunks map uniquely to the 303 earlier hunks. For 291, both complete payloads and the printed-side span are exact. For six, the printed span and payload remain exact while the corrected payload changed. For six, the current printed span is strictly contained in the earlier span. All printed source files are byte-identical across snapshots. The FD strings happen to be the same; use the snapshot along with the ID.

The twelve appended French rows `C020730`–`C020741` contain nonempty footnote operands and empty replacements. Each operand occurs exactly once in its earlier source file. Replaying the operations in ledger order, in memory, after converting only ledger newlines to the original source CRLF convention, reconstructs current corrected `149.tex` and `212.tex` byte for byte. Those are the only changed source files. `FOOTNOTE_OPERATIONS.json` quotes exact ledger fields; `FOOTNOTE_REMOVALS.tsv` gives operand hashes and byte/line coordinates, and `FOOTNOTE_REPLAY.json` gives complete file hashes. No note's substance is endorsed by these relationships.

## Current candidate counts

| Measure | Count |
|---|---:|
| Current ordinary-unmatched hunks searched | 69 |
| Hunks with a paired lexical candidate | 57 |
| Hunks without a pair | 12 |
| Candidate links | 339 |
| Distinct candidate ledger rows | 105 |
| Exact included ledger payload rows | 159 |
| Append-order corrected-French history links for no-pair cases | 722 |
| History links without a byte-identical printed-layer operation | 59 |

The current ledger has 21,269 rows. Its original 20,729 rows and the previous supplement's 20,939 rows remain unchanged row-hash prefixes. The French row sequence is unchanged since the previous supplement's capture; later appends in the current frozen ledger are outside those French rows.

The first successful projection is P0 for 18 hunks, P1 for 33, P2 for five, and P3 for one. P0 collapses only ASCII whitespace. P1 additionally removes exact balanced `symup` wrappers. P2 additionally removes `uline`. P3 additionally removes `underline` and `uwave`. Every removal has offsets, an argument hash and notational-sensitivity metadata. All other commands and characters are preserved apart from ASCII whitespace; the alphabet-command sequence is independently checked. This declared projection never establishes that fonts or underline notation have equal meaning.

49 paired hunks have at least one pair of whole ledger operands occurring in opposite projected hunk sides. Eight have only localized ledger edit fragments: `FD000002`, `FD000023`, `FD000057`, `FD000100`, `FD000219`, `FD000244`, `FD000246`, and `FD000270`. Only `FD000014`, `FD000103`, `FD000170`, and `FD000298` have a pair equal to both entire projected hunk payloads. Even a whole projected pair remains a candidate, not a correction judgment.

The previous twelve no-pair hunks have exact unchanged payloads and remain no-pair in the refreshed search. Their detailed table is PREVIOUS_NO_PAIR.md. There are 722 same-page corrected-French history links in append order; 59 lack an operation with byte-identical old/new fields on the printed layer at that page. “No identical counterpart” does not determine intended layer policy or net effect.

## Previous-link changes

332 of the earlier 335 stored fragment pairs still distinguish the corresponding current projected hunk sides. The three failures are `FM000007`, `FM000010`, and `FM000013`, all for old `FD000005` and ledger row `C000549`. This is recorded in OLD_FORMAT_LINK_REVALIDATION.tsv. Revalidation counts refer to the old stored fragments; the complete refreshed search is recorded separately under `FC` identifiers.

`FD000002` is the newly ordinary-unmatched hunk after its footnote removal. The refreshed formatting search finds seven local-fragment candidates to `C000212` and `C000260`. Their directions, profiles, source fragments, row hashes and exact ledger fields are retained. The refreshed complete search has 339 links; it is not an automatic carry-forward of 335 old links.

## Files

- CURRENT_TO_OLD.md / .tsv: complete 303-row mapping, source-line locators, payload hashes and current ordinary candidate IDs.
- OLD_TO_CURRENT.tsv: reciprocal map, including empty/ambiguous cases if any; this run has none.
- CHANGED_HUNKS.json: exact earlier/current payloads for the twelve changed hunks.
- SOURCE_CHANGES.tsv: all source-file hashes and equality flags.
- FOOTNOTE_REMOVALS.md / .tsv, FOOTNOTE_OPERATIONS.json and FOOTNOTE_REPLAY.json: literal recorded-deletion continuity.
- PREVIOUS_NO_PAIR.md / .tsv: current mapping of the previous twelve no-pair cases.
- CURRENT_UNMATCHED_REVIEW.md and FORMAT_HUNK_STATUS.tsv: current per-hunk candidate/history navigation.
- FORMAT_CANDIDATE_LINKS.tsv and FORMAT_CANDIDATE_DETAILS.json: current links, orientations, row hashes, exact projected fragments and offsets.
- FORMAT_HUNK_PROJECTIONS.json and FORMAT_PROFILES.json: projected hunk values and every declared wrapper removal.
- FORMAT_LEDGER_PAYLOADS.json / .md: exact row fields for all candidate rows and the history subset without identical printed operations.
- FR_CORRECTED_NO_PAIR_HISTORY.tsv and FR_ONLY_NO_PAIR_HISTORY.tsv: append-order page operations and their mechanically identified subset.
- OLD_FORMAT_LINK_REVALIDATION.tsv: each previous stored fragment predicate retested on current hunk payloads.
- INVENTORY.json: counts, input hashes, source paths and precise snapshot timestamps.
- metadata_audit/AUDIT.json and REPORT.md: separate validation, **PASS at 05:15:51 UTC**, with zero failed checks.

No source, ledger, mathematics, translation or complete-net-coverage adjudication is performed. Absence of a candidate does not establish missing proof or reading. All claims are limited to the frozen inputs identified in INVENTORY.json. Reproduction commands are in the parent README.md.
