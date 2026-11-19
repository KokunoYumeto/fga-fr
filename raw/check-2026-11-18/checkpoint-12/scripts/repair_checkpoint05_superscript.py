"""Keep prime marks inside a grouped base before its inverse superscript."""
from audit_utils import *
for tree,layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    replace(f'sources/{tree}/fr/190.tex',
            r"F''_1F''_2^{-1}=F''", r"F''_1{F''_2}^{-1}=F''",
            layer,'190-323','rationality criterion, tensor quotient of the two pullbacks','',
            'corrects the earlier run: literal prime characters already form a TeX superscript. Grouping the complete primed symbol before its inverse exponent avoids the Double superscript error, with no new visible parentheses or mathematical change.',
            kind='typesetting')
with (ROOT/'progress.log').open('a') as f:
    f.write('checkpoint 05 primed inverse grouping repaired '+utc()+'\n')
