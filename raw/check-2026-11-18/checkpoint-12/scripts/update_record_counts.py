"""Recount recorded operations without certifying unread material."""
from audit_utils import *
from collections import Counter
def update():
    log=read('progress.log')
    done=re.findall(r'^page (\S+) done ',log,re.M)
    with (ROOT/'CORRECTIONS.tsv').open(newline='') as f: rows=list(csv.DictReader(f,delimiter='\t'))
    from translation_edits import NAMES
    translation_pages={(NAMES[la],page) for la,page in re.findall(r'^translation page (\S+) (\S+) read ',log,re.M)}
    selected=[r for r in rows if (r['layer'] in ('French as printed','French corrected') and r['printed_page'] in done) or (r['layer'],r['printed_page']) in translation_pages]
    totals=Counter((r['layer'],r['kind']) for r in selected)
    txt=read('CHECK_RECORD.md')
    txt=re.sub(r'Completed source-page comparisons: \d+',f'Completed source-page comparisons: {len(done)}',txt)
    block='<!-- audit-metrics-begin -->\n## Provisional operation totals\n\nThese are ledger operations on completed pages, including amendments and withdrawals; they are not final surviving-difference counts. Provisional restorations on unread pages are excluded. The mandated final second reading has not begun.\n\n| Layer | Kind | Operations |\n| --- | --- | ---: |\n'
    for (layer,kind),n in sorted(totals.items()): block+=f'| {layer} | {kind} | {n} |\n'
    completed_units=re.findall(r'^(?:en|es|es_149_printed|pt-BR|pt-BR_printed|vi|vi_diplomatic|ko|zh-Hans) (?:e?\d+|com) done ',log,re.M)
    block+=f'\nCompleted French page records: {len(done)}. Translation units completed: {len(completed_units)}. Pages with no recorded operation in either French layer: '+str(sum(not any(r['printed_page']==p and r['layer'] in ('French as printed','French corrected') for r in selected) for p in done))+'.\n<!-- audit-metrics-end -->\n\n'
    if '<!-- audit-metrics-begin -->' in txt:
        txt=re.sub(r'<!-- audit-metrics-begin -->.*?<!-- audit-metrics-end -->\n\n',lambda m:block,txt,flags=re.S)
    else: txt=txt.replace('## Scope and status',block+'## Scope and status',1)
    for p in done:
        pattern=r'(### '+re.escape(p)+r'\n)(.*?)(?=\n### |\Z)'
        m=re.search(pattern,txt,re.S)
        if not m: continue
        body=re.sub(r'\n\nLedger operation counts \(provisional\):[^\n]*','',m.group(2))
        counts=Counter((r['layer'],r['kind']) for r in selected if r['printed_page']==p and r['layer'] in ('French as printed','French corrected'))
        body+='\n\nLedger operation counts (provisional): '+ '; '.join(f'{la}, {ki}: {n}' for (la,ki),n in sorted(counts.items()))+'.\n'
        txt=txt[:m.start(2)]+body+txt[m.end(2):]
    write('CHECK_RECORD.md',txt)
if __name__=='__main__': update()
