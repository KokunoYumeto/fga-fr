"""Independent lexical validation of the terminology inventory.

Reads supplied records and current edition bytes without modifying them.
Writes audit evidence only under the explicitly named temporary output folder.
"""
from pathlib import Path
import bisect, collections, csv, hashlib, json, re
from datetime import datetime, timezone

BASE=Path('FGA_CHECK')
SNAP=BASE/'terminology_inventory/snapshot_20261119_initial'
OUT=Path('tmp/terminology_independent_audit')
OUT.mkdir(parents=True,exist_ok=True)
failures=[]
checks=[]
def check(name,condition,details=None):
    checks.append({'check':name,'pass':bool(condition),'details':details})
    if not condition:failures.append(name)
def table(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
start=now()
artifact_paths=list(SNAP.iterdir())+[BASE/'TERMINOLOGY_LOW_CONFIDENCE.md',BASE/'scripts/terminology_inventory.py']
initial_artifact_bytes={p:p.read_bytes() for p in artifact_paths if p.is_file()}
original=table(Path('upload/DECISIONS_20261119(1).tsv'))
standards=Path('upload/STANDARDS_20261119(1).md').read_bytes()
inventory=table(SNAP/'DECISION_INVENTORY.tsv')
meta=json.loads((SNAP/'INVENTORY.json').read_text())
check('exactly_67_input_and_inventory_rows',len(original)==len(inventory)==67)
cols=list(original[0])
row_errors=[]
for n,(a,b) in enumerate(zip(original,inventory),1):
    if any(a[k]!=b[k] for k in cols):row_errors.append(n)
    if b['decision_id']!=f'T{n:03d}' or b['input_record']!=str(n) or b['input_line']!=str(n+1):row_errors.append(n)
check('all_original_fields_and_row_identifiers_exact',not row_errors,sorted(set(row_errors)))
langs=['en','es','pt-BR','vi','ko','zh-Hans']
applicable=[r for r in original if r['language']=='all' or r['language'] in langs]
other=[r for r in original if r['language']!='all' and r['language'] not in langs]
check('entire_input_confidence_counts',collections.Counter(r['confidence'] for r in original)=={'high':38,'medium':27,'low':2})
check('53_applicable_31_high_20_medium_2_low',len(applicable)==53 and collections.Counter(r['confidence'] for r in applicable)=={'high':31,'medium':20,'low':2})
check('14_out_of_scope_7_high_7_medium',len(other)==14 and collections.Counter(r['confidence'] for r in other)=={'high':7,'medium':7})
scope_errors=[]
for n,(a,b) in enumerate(zip(original,inventory),1):
    selected=langs if a['language']=='all' else [a['language']] if a['language'] in langs else []
    if b['applicable']!=str(bool(selected)) or b['applicable_languages']!=','.join(selected):scope_errors.append(n)
    if a['confidence']=='low' and b['application_status']!='excluded: low-confidence decision is not to be applied':scope_errors.append(n)
check('all_inventory_applicability_and_low_exclusion_exact',not scope_errors,scope_errors)
all_rows=[(n,r) for n,r in enumerate(original,1) if r['language']=='all']
check('five_all_language_rows_literal_scope',len(all_rows)==5 and [n for n,r in all_rows]==[1,2,3,4,5])
check('input_record_hash_exact',meta['input_decisions_sha256']==sha(Path('upload/DECISIONS_20261119(1).tsv').read_bytes()))
check('input_standard_hash_exact',meta['input_standards_sha256']==sha(standards))
manifest=table(SNAP/'SOURCE_HASHES.tsv')
filebytes={r['file']:(BASE/r['file']).read_bytes() for r in manifest}
source_problems=[]
for row in manifest:
    b=filebytes[row['file']]
    if len(b)!=int(row['bytes']) or sha(b)!=row['sha256']:source_problems.append(row['file'])
check('all_manifest_sizes_and_hashes_exact',not source_problems,source_problems)
layers=['en','es','es_149_printed','pt-BR','pt-BR_printed','vi','vi_diplomatic','ko','zh-Hans']
actual_files={p.relative_to(BASE).as_posix() for layer in layers for p in (BASE/'sources'/layer).rglob('*.tex')}
check('manifest_covers_all_translation_tex_files',actual_files==set(filebytes),{'manifest_files':len(filebytes),'actual_files':len(actual_files)})
check('161_files_137_units_24_ancillary',len(manifest)==161 and collections.Counter(r['scope'] for r in manifest)=={'unit':137,'ancillary':24})
manifest_index={r['file']:r for r in manifest}
literals=table(SNAP/'SEARCH_LITERALS.tsv')
literal_index={r['literal_id']:r for r in literals}
check('unique_literal_identifiers',len(literal_index)==len(literals)==1172)
occurrences=table(SNAP/'LITERAL_OCCURRENCES.tsv')
low=table(SNAP/'LOW_CONFIDENCE_OCCURRENCES.tsv')
expected_low=[r for r in occurrences if r['decision_id'] in {'T051','T055'}]
check('low_table_is_exact_ordered_subset',low==expected_low)
check('all_occurrence_count_matches_metadata',len(occurrences)==meta['literal_occurrences']==64847)
# Independent text-offset interpretation of every supplied match, avoiding the
# generating script and its byte-based locator calculation.
text_index={}
for file,b in filebytes.items():
    s=b.decode('utf-8');starts=[0]
    for m in re.finditer('\n',s):starts.append(m.end())
    # Mask TeX comments independently with an escaped-percent parity check.
    masked=[]
    for line in s.splitlines(keepends=True):
        chars=list(line)
        for i,ch in enumerate(line):
            if ch!='%':continue
            before=i-1
            while before>=0 and line[before]=='\\':before-=1
            if (i-before-1)%2==0:
                for j in range(i,len(chars)):
                    if chars[j] not in '\r\n':chars[j]=' '
                break
        masked.append(''.join(chars))
    page_positions=[]
    for m in re.finditer(r'\\src\s*\{\s*([0-9]+|[IVXLCDMivxlcdm]+)\s*\}', ''.join(masked)):
        page=m.group(1)
        page=str(int(page)) if page.isdigit() else page.upper()
        page_positions.append((m.start(),page))
    text_index[file]=(s,starts,page_positions)
locator_errors=[]
for n,r in enumerate(occurrences,1):
    b=filebytes.get(r['file']);literal=literal_index.get(r['literal_id'])
    if b is None or literal is None:locator_errors.append((n,'missing source/literal'));continue
    lo,hi=int(r['byte_start']),int(r['byte_end'])
    s,starts,pages=text_index[r['file']]
    if b[lo:hi].decode('utf-8')!=r['matched_literal'] or literal['literal']!=r['matched_literal']:
        locator_errors.append((n,'literal'));continue
    pos=len(b[:lo].decode('utf-8'));line=bisect.bisect_right(starts,pos);col=pos-starts[line-1]+1
    end=s.find('\n',starts[line-1]);end=len(s) if end<0 else end
    line_text=s[starts[line-1]:end].rstrip('\r')
    prior=[p for p in pages if p[0]<=pos]
    page=prior[-1][1] if prior else ''
    expected={'source_line':str(line),'column_character':str(col),'column_byte':str(len(s[starts[line-1]:pos].encode('utf-8'))+1),'source_line_text':line_text,'preceding_literal_page':page,
              'language':manifest_index[r['file']]['language'],'layer':manifest_index[r['file']]['layer'],'unit':manifest_index[r['file']]['unit'],'scope':manifest_index[r['file']]['scope'],'decision_id':literal['decision_id']}
    wrong=[k for k,v in expected.items() if r[k]!=v]
    if wrong:locator_errors.append((n,','.join(wrong)))
check('all_64847_literal_byte_line_page_and_scope_locators_exact',not locator_errors,locator_errors[:50])
# Exhaustive independent regex lookahead enumeration of the specified low
# strings; zero counts and overlapping candidates remain explicit.
low_terms={'T051':('zh-Hans',['归纳极限','逆极限','余极限','射影极限','正向极限']),
           'T055':('ko',['섬유','섬유곱','의 올','올곱','파이버','올'])}
expected_occ=[];term_counts={}
for rid,(lang,terms) in low_terms.items():
    specified=[x['literal'] for x in literals if x['decision_id']==rid]
    check(rid+'_exact_low_literal_set',specified==terms)
    term_counts[rid]={}
    for term in terms:
        hits=0
        pattern=re.compile('(?='+re.escape(term)+')')
        for file,(s,starts,pages) in text_index.items():
            if manifest_index[file]['language']!=lang:continue
            for m in pattern.finditer(s):
                lo=len(s[:m.start()].encode('utf-8'));hi=lo+len(term.encode('utf-8'))
                expected_occ.append((rid,file,lo,hi,term));hits+=1
        term_counts[rid][term]=hits
actual_occ=[(r['decision_id'],r['file'],int(r['byte_start']),int(r['byte_end']),r['matched_literal']) for r in low]
check('exhaustive_independent_low_occurrence_enumeration',collections.Counter(expected_occ)==collections.Counter(actual_occ),{'expected':len(expected_occ),'actual':len(actual_occ),'per_literal':term_counts})
check('low_counts_21_chinese_253_korean',collections.Counter(r['decision_id'] for r in low)=={'T051':21,'T055':253})
low_md=(BASE/'TERMINOLOGY_LOW_CONFIDENCE.md').read_text()
low_markdown_errors=[]
for ordinal in [51,55]:
    row=original[ordinal-1];rid=f'T{ordinal:03d}'
    title=f"## {rid}: {row['language']} — {row['concept']}\n"
    if title not in low_md:low_markdown_errors.append((rid,'title'));continue
    section=low_md.split(title,1)[1].split('\n## ',1)[0]
    for field in cols:
        exact=f'**{field}:** {row[field]}\n'
        if exact not in section:low_markdown_errors.append((rid,field))
check('both_low_decisions_reproduced_field_for_field',not low_markdown_errors,low_markdown_errors)
# Verify that each mechanical occurrence is represented by one Markdown row;
# exact field formatting is independently reconstructed here.
def md(s):return str(s).replace('|','\\|').replace('\n',' ')
markdown_rows=[]
for r in low:
    loc=(r['unit']+'-'+r['preceding_literal_page']) if r['unit'] and r['preceding_literal_page'] else 'ancillary / no preceding marker'
    markdown_rows.append(f"| {r['file']} | {loc} | {r['source_line']} | {r['column_character']} | {r['byte_start']}–{r['byte_end']} | {md(r['matched_literal'])} | {md(r['source_line_text'])} |")
actual_rows=[line for line in low_md.splitlines() if line.startswith('| sources/')]
check('all_274_low_markdown_locator_rows_exact',actual_rows==markdown_rows,{'expected':len(markdown_rows),'actual':len(actual_rows)})
privacy_paths=list(SNAP.iterdir())+[BASE/'TERMINOLOGY_LOW_CONFIDENCE.md',BASE/'scripts/terminology_inventory.py']
email=re.compile(r'(?<![\w.+-])[A-Za-z0-9.!#$%&*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?\.[A-Za-z]{2,}(?![\w.-])')
prefixes=['/'+x+'/' for x in ('workspace','home','root','tmp','mnt','Users')]
windows=re.compile(r'(?<![A-Za-z])[A-Za-z]:[\\/]')
privacy=[]
tex_control_path_false_positives=collections.Counter()
known_tex_controls={'overline','widetilde','xi','mathcal','operatorname','bigwedge'}
for p in privacy_paths:
    if not p.is_file():continue
    s=p.read_text()
    for n,line in enumerate(s.splitlines(),1):
        actual_windows=[]
        for match in windows.finditer(line):
            command=re.match(r'[A-Za-z@]+',line[match.end():])
            if line[match.end()-1]=='\\' and command and command.group() in known_tex_controls:
                tex_control_path_false_positives[command.group()]+=1
            else:actual_windows.append(match.start())
        if email.search(line) or any(q in line for q in prefixes) or actual_windows:privacy.append({'file':p.relative_to(BASE).as_posix(),'line':n})
check('outputs_contain_no_detected_host_paths_or_emails',not privacy,privacy[:50])
source_unchanged=all((BASE/r).read_bytes()==b for r,b in filebytes.items())
check('source_bytes_unchanged_during_independent_audit',source_unchanged)
check('inventory_artifact_bytes_stable_during_independent_audit',all(p.read_bytes()==b for p,b in initial_artifact_bytes.items()))
result={'status':'PASS' if not failures else 'FAIL','started_utc':start,'completed_utc':now(),'scope':'Independent lexical metadata audit; no scan, paragraph, mathematical or translation adjudication. No FGA_CHECK or source writes by this audit.',
        'checks':checks,'failed_checks':failures,'source_files':len(filebytes),'source_bytes':sum(map(len,filebytes.values())),'decision_rows':len(original),'applicable_decisions':len(applicable),'literal_candidates':len(literals),'literal_occurrences_checked':len(occurrences),'low_occurrences_independently_enumerated':len(expected_occ),'low_term_counts':term_counts,'path_detector_tex_false_positives':dict(tex_control_path_false_positives),'audit_harness_revision':'The first audit compared doubled TeX backslashes against the revised Markdown and overmatched six ordinary TeX controls as Windows paths. Those two detector false positives were corrected before this complete rerun; no source or inventory data repair was required.',
        'audited_artifact_sha256':{p.relative_to(BASE).as_posix():sha(p.read_bytes()) for p in privacy_paths if p.is_file()}}
(OUT/'AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','completed_utc','failed_checks','source_files','source_bytes','decision_rows','applicable_decisions','literal_candidates','literal_occurrences_checked','low_occurrences_independently_enumerated','low_term_counts']},ensure_ascii=False,indent=2))
