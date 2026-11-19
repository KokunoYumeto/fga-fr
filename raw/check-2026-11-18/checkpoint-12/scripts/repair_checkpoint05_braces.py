"""Repair the duplicated underline terminator reported by LuaLaTeX."""
from audit_utils import *
for tree, layer in [('fr_printed','French as printed'),('fr','French corrected')]:
    replace(f'sources/{tree}/fr/182.tex',
            r'modules} plats \uline{sur}}', r'modules} plats \uline{sur}',
            layer, '182-198', 'Theorem 4, condition i, words modules plats sur', '4',
            'corrects the earlier run: the prose-underlining replacement in apply_182_198.py appended a duplicate closing brace after sur. Removing the extra terminator restores balanced TeX grouping and retains the intended absence of an underline beneath plats. LuaLaTeX reported Extra }, or forgotten endgroup at this location.',
            kind='typesetting')
with (ROOT/'progress.log').open('a') as f:
    f.write('checkpoint 05 duplicated underline terminators repaired '+utc()+'\n')
