# Partial diagnostic font redirect

The second driver attempt correctly redirected the top-level Chinese font requests, but stopped at the inline SimSun request in Chinese 149.tex, line 132. Korean stopped because the explicit nested italic font option still named Malgun Gothic. The next driver stage adds redirects for these font-selection paths without changing an edition source.
