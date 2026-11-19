# Diagnostic font substitutions

The requested Windows fonts are absent from this environment. This stage used explicit task-local fontconfig substitutions to inspect later compiler diagnostics without editing the frozen edition sources. These builds do not certify the requested fonts, their metrics, or final layout and are not publishable editions.

| Requested font | Diagnostic substitute |
| --- | --- |
| Malgun Gothic | Noto Sans CJK KR |
| Malgun Gothic Bold | Noto Sans CJK KR (bold) |
| SimSun | Noto Serif CJK SC |
| Microsoft YaHei | Noto Sans CJK SC |

The standard runtime font configuration is unchanged. No source, credit, rights notice, audit ledger, or substantive text was edited by this helper.
