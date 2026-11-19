"""Repair syntax introduced by checkpoint 05; no printed reading is changed."""
from audit_utils import *

for tree, layer in [('fr_printed', 'French as printed'), ('fr', 'French corrected')]:
    rel = f'sources/{tree}/fr/149.tex'
    replace(rel, '\\begin{equation}\\tag{4.3}\n\n',
            '\\begin{equation}\\tag{4.3}\n', layer, '149-178',
            'display (4.3), before its first term', '(4.3)',
            'corrects the earlier run: the added empty line produces a paragraph token inside the equation environment. Removing that source-only paragraph token preserves the formula and printed display.',
            kind='typesetting')
    rel = f'sources/{tree}/fr/182.tex'
    text = read(rel)
    candidates = []
    for m in re.finditer(r'^.*\\(?:longrightarrow|simeq|otimes)O(?:_|\^).*$' , text, re.M):
        markers = list(re.finditer(r'\\src\{(\d+)\}', text[:m.start()]))
        page = markers[-1].group(1)
        old = m.group(0)
        new = re.sub(r'\\(longrightarrow|simeq|otimes)O', r'\\\1 O', old)
        candidates.append((page, old, new, text[:m.start()].count('\n') + 1))
    if len(candidates) not in (0, 9):
        raise ValueError(f'Unexpected joined-control count: {len(candidates)}')
    for page, old, new, source_line in candidates:
        replace(rel, old, new, layer, f'182-{page}',
                f'formula at inherited source line {source_line}', '',
                'corrects the earlier run: replacing the sheaf macro by the printed ordinary O had joined O to the preceding TeX control word. A delimiter space restores the intended arrow, tensor sign, or isomorphism sign followed by O; it adds no mathematical spacing or content.',
                kind='typesetting')
    rel = f'sources/{tree}/fr/195.tex'
    replace(rel, r'\underset{\alpha}{\varprojlim}\nolimits',
            r'\mathop{\underset{\alpha}{\varprojlim}}\nolimits',
            layer, '195-373', 'extended-functor display, right-hand limit', '',
            'corrects the earlier run: the existing nolimits command must apply to an operator atom. The mathop wrapper makes the limit with alpha underneath an operator, retaining the category index on its right and changing no formula content.',
            kind='typesetting')

stamp = utc()
with (ROOT / 'CHECK_RECORD.md').open('a') as f:
    f.write('\n## Continuation: checkpoint 05 build repairs\n\n')
    f.write(f'Recorded {stamp}. The 22 source edits in the two French layers repair nine joined control words, one empty line in equation (4.3), and one invalid limit modifier per layer. These are TeX syntax repairs, not new scan-reading or page-completion claims. Each correction has its own typesetting row, with evidence beginning “corrects the earlier run:”. Engine verification is recorded separately.\n')
with (ROOT / 'progress.log').open('a') as f:
    f.write(f'checkpoint 05 syntax repairs applied {stamp}; compilation verification pending\n')
