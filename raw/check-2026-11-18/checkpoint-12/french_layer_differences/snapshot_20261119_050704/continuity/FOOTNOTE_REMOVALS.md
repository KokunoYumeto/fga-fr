# Recorded footnote-removal continuity

The twelve appended French operations are quoted as ledger data in FOOTNOTE_OPERATIONS.json. Each recorded old operand occurs exactly once in the earlier corrected source. Converting only ledger line endings to the source's existing CRLF convention and replaying these literal deletions in append order, in memory, reproduces both current source files byte for byte. No source or ledger was written. This establishes byte continuity only; it does not adjudicate the text of a note or any neighboring correction.

| Ledger row | Page | Old FD → current FD | Old FR lines | Current deletion anchor line | Current hunk FR lines |
|---|---|---|---|---|---|
| C020730 | 149-171 | FD000002 → FD000002 | 149–149 | 149 | 148 |
| C020731 | 149-175 | FD000005 → FD000005 | 343–343 | 343 | 342–343 |
| C020732 | 149-177 | FD000009 → FD000009 | 427–428 | 427 | 426 |
| C020733 | 149-177 | FD000010 → FD000010 | 447–449 | 446 | 446 |
| C020734 | 149-183 | FD000033 → FD000033 | 755–757 | 752 | 752 |
| C020735 | 149-183 | FD000034 → FD000034 | 774–775 | 769 | 768 |
| C020736 | 149-185 | FD000036 → FD000036 | 899–900 | 893 | 894 |
| C020737 | 149-187 | FD000038 → FD000038 | 972–973 | 965 | 964 |
| C020738 | 149-188 | FD000042 → FD000042 | 1035–1037 | 1027 | 1028 |
| C020739 | 212-109 | FD000166 → FD000166 | 480–483 | 480 | 480 |
| C020740 | 212-114 | FD000169 → FD000169 | 738–740 | 735 | 735 |
| C020741 | 212-116 | FD000170 → FD000170 | 840–841 | 835 | 835 |

## Exact reconstruction hashes

| File | Earlier SHA-256 | Current and replayed SHA-256 |
|---|---|---|
| sources/fr/fr/149.tex | `a237670c2a981f1c617518213be9903b8fb2076c96a49da9224e4733d54d1db4` | `f00873843cbad6224b1422a8e08b36c52b7478d759b53d1c17f840f4bb0e77c8` |
| sources/fr/fr/212.tex | `75d058b403369ccd32a61af823d77cb1b0fb829af0a208f8b3b277781380ec43` | `fb6400edd43e608e81f9384d0c8a5c0461a1f789bdb4075eb88c216ca7ec2ac7` |
