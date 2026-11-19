"""Remove explicitly identified earlier editorial notes from the historical text.

The explanations remain in the correction ledger and check record; this script
does not touch any footnote present in both French layers.
"""
import re
from audit_utils import ROOT, read, footnotes, replace, utc
from update_record_counts import update

found=[]
for unit in ('149','212'):
    rel=f'sources/fr/fr/{unit}.tex'
    text=read(rel)
    printed=read(f'sources/fr_printed/fr/{unit}.tex')
    for start,end,body in footnotes(text):
        if not re.match(r'Le texte\s+imprimé\b',body):
            continue
        old=text[start:end]
        if old in printed:
            raise ValueError('Refusing a footnote also present in the literal layer')
        pages=re.findall(r'\\src\{(\d+)\}',text[:start])
        page=f'{unit}-{pages[-1]}'
        found.append((rel,page,text[:start].count('\n')+1,old))
if len(found)!=12:
    raise ValueError(f'Expected the twelve reviewed editorial notes; found {len(found)}')
for rel,page,line,old in found:
    replace(rel,old,'','French corrected',page,f'editorial footnote; source line {line}',
        'editorial separation',
        'corrects the earlier run: this explanatory footnote occurs only in the corrected French and explicitly describes the printed text. The task keeps editorial notes apart from the historical text. Its explanation remains in the ledger and page record; the corrected reading itself is unchanged. Scan confirmation is reserved for the final per-row crop review.',
        kind='structure')
with (ROOT/'CHECK_RECORD.md').open('a') as f:
    f.write('\n## French-layer reconciliation: editorial notes\n\n')
    f.write(f'Reader: GPT-6 Astra, ChatGPT Pro mode, this run. Recorded {utc()}.\n\n')
    f.write('Removed twelve explanatory footnotes inserted by the earlier run into the corrected historical text (nine in exposé 149, three in exposé 212). They describe the print and have no counterpart in the literal French layer. The corrections they explain remain in the text and ledger; their reasons stay in the record and will be treated in the separate notes. Original footnotes, including the errata, are retained. These twelve structure rows remain provisional until their final crop review.\n')
with (ROOT/'progress.log').open('a') as f:
    f.write(f'French editorial-footnote separation recorded {utc()}\n')
update()
