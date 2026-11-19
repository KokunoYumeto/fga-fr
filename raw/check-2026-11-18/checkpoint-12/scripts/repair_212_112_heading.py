from audit_utils import *
bad=r"\fsection{\normalfont 6}{\normalfont\uline{Quotient par une relation d'équivalence propre et plate}."
good=bad+'}'
for tree in ['fr_printed','fr']:
 rel=f'sources/{tree}/fr/212.tex'
 s=read(rel)
 if s.count(bad+'\n')!=1: raise ValueError('Expected one incomplete heading macro')
 write(rel,s.replace(bad+'\n',good+'\n'))
with (ROOT/'CORRECTIONS.tsv').open(newline='') as f: rows=list(csv.DictReader(f,delimiter='\t'))
selected=[r for r in rows if r['printed_page']=='212-112' and r['new']==bad]
if len(selected)!=2: raise ValueError('Expected two heading rows')
for r in selected: r['new']=good
with (ROOT/'CORRECTIONS.tsv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=FIELDS,delimiter='\t');w.writeheader();w.writerows(rows)
s=read('scripts/apply_212_112.py')
if s.count(bad+'"')!=1: raise ValueError('Expected one generating literal')
write('scripts/apply_212_112.py',s.replace(bad+'"',good+'"'))
with (ROOT/'CHECK_RECORD.md').open('a') as f:
 f.write('\nPage 212-112 implementation check: supplied a missing closing macro brace in the newly typed section heading before proceeding to the next page; the two heading ledger rows and generating literal were amended to the intended complete TeX. This is not a change of the printed reading.\n')
