"""Nonmutating ledger and coverage structural gates for FGA.

Only schemas, literal categories, timestamps, locators, hashes, headings, and
completion markers are checked. No correction/evidence/result text is reported
or judged. A successful run is not a certificate of substantive review.
"""
import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re

from checkpoint_zip import exclude_reason
from source_segments import CONFIG, UNITS, expected_units, source_path

ALIASES = {
 'fr_printed':['fr_printed','French as printed'], 'fr':['French corrected','French','fr'],
 'en':['English','en'], 'es_149_printed':['es_149_printed','Spanish 149 as printed','Spanish as printed'],
 'es':['Spanish','es'], 'pt-BR_printed':['pt-BR_printed','Portuguese as printed','Brazilian Portuguese as printed'],
 'pt-BR':['Brazilian Portuguese','Portuguese','pt-BR'], 'vi_diplomatic':['vi_diplomatic','Vietnamese diplomatic','Vietnamese as printed'],
 'vi':['Vietnamese','vi'], 'ko':['Korean','ko'], 'zh-Hans':['Simplified Chinese','Chinese','zh-Hans','zh-Hans-CN']}
PARENTS = {'es_149_printed':'es','pt-BR_printed':'pt-BR','vi_diplomatic':'vi'}
UNIT_PATTERN = r'(?:e?(?:149|182|190|195|212|221|232|236)|com)'
PAGE_ID = re.compile(r'\b('+UNIT_PATTERN+r')\s*[-:]\s*(\d{1,3})\b',re.I)
UNIT_ID = re.compile(r'(?<![\w])('+UNIT_PATTERN+r')(?![\w])',re.I)
PAGE_DONE = re.compile(r'^page\s+('+UNIT_PATTERN+r')[-:](\d+)\s+done\s+(.+)$',re.I)
LANG_DONE = re.compile(r'^(.+?)\s+('+UNIT_PATTERN+r')\s+done\s+(.+)$',re.I)
STAMP = re.compile(r'\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?: UTC|Z|[+-]\d{2}:\d{2})?)?')

def sha(data): return hashlib.sha256(data).hexdigest()
def utc(): return datetime.now(timezone.utc).isoformat()
def safe_identifier(value): return value if re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.:=+-]{0,159}',value or '') else ''
def safe_relative(value):
    p=Path(value)
    return bool(value) and not p.is_absolute() and '..' not in p.parts and '\\' not in value and not re.match(r'^[A-Za-z]:',value) and '\n' not in value and '\r' not in value
def layer_hint(text):
    choices=sorted(((a,l) for l,values in ALIASES.items() for a in values),key=lambda x:len(x[0]),reverse=True)
    return next((l for a,l in choices if re.search(r'(?<![\w])'+re.escape(a)+r'(?![\w])',text,re.I)),None)
def exact_layer(text):
    return next((l for l,values in ALIASES.items() if text.casefold() in {v.casefold() for v in values}),None)
def valid_utc(value):
    value=value.strip()
    try:
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}',value): datetime.fromisoformat(value); return True,'date only'
        parsed=datetime.fromisoformat(value.replace(' UTC','+00:00').replace('Z','+00:00'))
        return bool(parsed.tzinfo is not None and parsed.utcoffset().total_seconds()==0),'explicit UTC timestamp'
    except (ValueError,AttributeError): return False,'invalid'
def table(path,columns,rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=columns,delimiter='\t',extrasaction='ignore');w.writeheader();w.writerows(rows)
def sections(data):
    lines=data.splitlines();heads=[];fence=None
    for i,line in enumerate(lines):
        mark=re.match(rb'^[ \t]*(`{3,}|~{3,})',line)
        if mark:
            kind=mark[1][:1];size=len(mark[1])
            if fence and kind==fence[0] and size>=fence[1]: fence=None
            elif not fence:fence=(kind,size)
            continue
        if fence:continue
        h=re.match(rb'^(#{1,6})[ \t]+(.*)$',line)
        if h:heads.append((i,len(h[1]),h[2].decode('utf-8')))
    result=[]
    for j,(start,level,heading) in enumerate(heads):
        end=next((n for n,l,_ in heads[j+1:] if l<=level),len(lines))
        result.append(dict(line=start+1,level=level,heading=heading,body=b'\n'.join(lines[start+1:end])))
    return result
def locator(body,layer,unit):
    value=layer+'/'+source_path(layer,unit)
    return bool(re.search(rb'(?<![\w.+~@%-])'+re.escape(value.encode())+rb'(?![\w./\\+~@%-])',body))

def run(args):
    work=args.work.resolve();output=args.out.resolve();policy_path=args.policy.resolve()
    if output.exists():raise FileExistsError('Choose a new report directory')
    protected=[(work/'sources').resolve(),(Path(__file__).resolve().parents[1]/'sources').resolve()]
    if any(output==p or output.is_relative_to(p) for p in protected):raise ValueError('Reports cannot be written in source trees')
    policy_bytes=policy_path.read_bytes();policy=json.loads(policy_bytes);started=utc()
    filenames=['CORRECTIONS.tsv','CHECK_EVENTS.tsv','CHECK_RECORD.md','progress.log']
    captured={name:(work/name).read_bytes() for name in filenames if (work/name).is_file()}
    syntax=[];advisory=[];duplicates=[];timestamps=[];ledgers={};categories=[];sources=[]
    def issue(file,rid,field,code,data_row='',physical_start='',physical_end=''):
        syntax.append(dict(file=file,row_id=rid,data_row=data_row,physical_start=physical_start,physical_end=physical_end,field=field,code=code))
    def stamp(file,rid,value):
        okay,precision=valid_utc(value);timestamps.append(dict(file=file,row_id=rid,valid=okay,precision=precision,value_sha256=sha(value.encode())))
        if not okay:issue(file,rid,'timestamp','invalid UTC date or timestamp')
    for name,columns,prefix in [('CORRECTIONS.tsv',policy['correction_columns'],'C'),('CHECK_EVENTS.tsv',policy['event_columns'],'E')]:
        if name not in captured:issue(name,'','file','required ledger missing');ledgers[name]=[];continue
        try:reader=csv.reader(io.StringIO(captured[name].decode('utf-8-sig'),newline=''),delimiter='\t',strict=True);header=next(reader)
        except (UnicodeDecodeError,csv.Error,StopIteration):issue(name,'','header','TSV header decoding or parsing failed');ledgers[name]=[];continue
        if header!=columns:issue(name,'','header','exact column names or order differ')
        rows=[];last_line=reader.line_num;number=0
        try:
            for cells in reader:
                number+=1;rid=f'{prefix}{number:06d}';start=last_line+1;end=reader.line_num;last_line=end
                info=dict(row_id=rid,data_row=number,physical_start=start,physical_end=end)
                if len(cells)!=len(columns):issue(name,rid,'row','wrong field count',number,start,end);continue
                rows.append(dict(info,values=dict(zip(columns,cells)),cells=tuple(cells)))
        except csv.Error:issue(name,f'{prefix}{number+1:06d}','row','TSV quoting/parsing error',number+1,last_line+1,reader.line_num)
        groups=defaultdict(list)
        for row in rows:groups[row['cells']].append(row)
        for cells,members in groups.items():
            if len(members)>1:duplicates.append(dict(file=name,row_ids=','.join(r['row_id'] for r in members),data_rows=','.join(str(r['data_row']) for r in members),physical_ranges=','.join(f"{r['physical_start']}-{r['physical_end']}" for r in members),count=len(members),extra_rows=len(members)-1,row_sha256=sha(json.dumps(cells,ensure_ascii=False,separators=(',',':')).encode())))
        ledgers[name]=rows
    lookup={}
    for row in ledgers['CORRECTIONS.tsv']:
        values=row['values'];rid=row['row_id']
        def bad(field,code):issue('CORRECTIONS.tsv',rid,field,code,row['data_row'],row['physical_start'],row['physical_end'])
        for field,allowed in [('kind',policy['allowed_kinds']),('confidence',policy['allowed_confidences'])]:
            if values[field] not in allowed:bad(field,'outside exact allowed category set')
        for field in ['file','layer','evidence']:
            if not values[field].strip():bad(field,'required value empty')
        value=values['file'];layer=exact_layer(values['layer'])
        if layer is None:bad('layer','unknown exact layer alias')
        if value not in lookup:
            if not safe_relative(value):lookup[value]=(False,None)
            else:
                paths=[work/value,work/'sources'/value];found=next((p for p in paths if p.is_file() and p.resolve().is_relative_to(work)),None)
                lookup[value]=(True,found)
        safe,found=lookup[value]
        if not safe:bad('file','unsafe source-relative locator')
        elif found is None:bad('file','source locator does not resolve')
    event_ids=defaultdict(list)
    for row in ledgers['CHECK_EVENTS.tsv']:
        v=row['values'];rid=row['row_id'];stamp('CHECK_EVENTS.tsv',rid,v['date_utc'])
        for field in ['id','who','how','result','where']:
            if not v[field].strip():issue('CHECK_EVENTS.tsv',rid,field,'required value empty',row['data_row'],row['physical_start'],row['physical_end'])
        event_ids[v['id']].append(rid)
        if v['how'] not in policy['legacy_event_types']:
            advisory.append(dict(file='CHECK_EVENTS.tsv',row_id=rid,data_row=row['data_row'],code='how outside legacy exact vocabulary',value_sha256=sha(v['how'].encode())))
            if args.strict_legacy_events:issue('CHECK_EVENTS.tsv',rid,'how','outside requested strict legacy event vocabulary',row['data_row'],row['physical_start'],row['physical_end'])
    for field,allowed in [('kind',policy['allowed_kinds']),('confidence',policy['allowed_confidences'])]:
        counts=Counter(r['values'][field] for r in ledgers['CORRECTIONS.tsv'])
        categories.extend(dict(file='CORRECTIONS.tsv',field=field,category=value,count=counts[value]) for value in allowed)
        categories.append(dict(file='CORRECTIONS.tsv',field=field,category='<outside allowed set>',count=sum(n for v,n in counts.items() if v not in allowed)))
    required=policy['required_source_paths']
    for number,value in enumerate(required,1):
        if not safe_relative(value):issue('source policy',f'S{number:04d}','path','unsafe required-source path');continue
        why=exclude_reason(Path(value),set())
        exists=(work/value).is_file()
        sources.append(dict(source=value,required=not bool(why),present=exists,excluded_reason=why))
        if not why and not exists:issue('required sources',f'S{number:04d}','path','required source file missing')
    page_heads=defaultdict(list);translation_heads=defaultdict(list);section_rows=[]
    record=captured.get('CHECK_RECORD.md')
    if record is None:issue('CHECK_RECORD.md','','file','required record file missing');record=b''
    try:parsed=sections(record)
    except UnicodeDecodeError:issue('CHECK_RECORD.md','','encoding','not UTF-8');parsed=[]
    for sec in parsed:
        hint=layer_hint(sec['heading']);p=PAGE_ID.search(sec['heading']);u=UNIT_ID.search(sec['heading']);rid=f'R{sec["line"]:06d}'
        key='';kind='other heading'
        if p and hint in (None,'fr','fr_printed'):
            unit,page=p[1].lower(),str(int(p[2]));page_heads[unit,page].append(sec);key=unit+'-'+page;kind='French page heading'
        elif hint and hint not in ('fr','fr_printed') and u:
            unit=u[1].lower();translation_heads[hint,unit].append(sec);key=hint+'/'+unit;kind='translation unit heading'
        section_rows.append(dict(row_id=rid,line=sec['line'],level=sec['level'],kind=kind,key=key,heading_sha256=sha(sec['heading'].encode())))
    for n,line in enumerate(record.decode('utf-8',errors='replace').splitlines(),1):
        for j,value in enumerate(STAMP.findall(line),1):stamp('CHECK_RECORD.md',f'R{n:06d}T{j}',value)
    page_done=defaultdict(list);lang_done=defaultdict(list);progress_rows=[]
    progress=captured.get('progress.log')
    if progress is None:issue('progress.log','','file','required progress file missing');progress=b''
    try:lines=progress.decode('utf-8').splitlines()
    except UnicodeDecodeError:issue('progress.log','','encoding','not UTF-8');lines=[]
    if not lines:issue('progress.log','','initial timestamp','missing initial timestamp')
    else:stamp('progress.log','P000001-initial',lines[0])
    for n,line in enumerate(lines,1):
        rid=f'P{n:06d}';p=PAGE_DONE.match(line);l=LANG_DONE.match(line);kind='informational';key=''
        if p:
            key=p[1].lower()+'-'+str(int(p[2]));page_done[p[1].lower(),str(int(p[2]))].append(n);kind='page completion';stamp('progress.log',rid,p[3])
        elif l and layer_hint(l[1]):
            layer=layer_hint(l[1]);unit=l[2].lower();lang_done[layer,unit].append(n);key=layer+'/'+unit;kind='language completion';stamp('progress.log',rid,l[3])
        elif n==1:kind='initial timestamp'
        else:
            for j,value in enumerate(STAMP.findall(line),1):stamp('progress.log',rid+'T'+str(j),value)
        progress_rows.append(dict(row_id=rid,line=n,kind=kind,key=key,line_sha256=sha(line.encode())))
    expected={(r['unit'],str(int(r['printed_page']))) for r in policy['expected_pages']};coverage=[];flags=[]
    for unit,page in sorted(expected,key=lambda p:(UNITS.index(p[0]),int(p[1]))):
        heads=page_heads[unit,page];done=page_done[unit,page];fr=any(locator(s['body'],'fr',unit) for s in heads);printed=any(locator(s['body'],'fr_printed',unit) for s in heads)
        status='recorded markers present' if heads and done and (not args.require_source_locators or (fr and printed)) else 'pending coverage'
        coverage.append(dict(unit=unit,printed_page=page,section_lines=','.join(str(s['line']) for s in heads),progress_lines=','.join(map(str,done)),heading_count=len(heads),completion_count=len(done),fr_locator_present=fr,fr_printed_locator_present=printed,status=status))
        if done and not heads:issue('progress/CHECK_RECORD',unit+'-'+page,'correspondence','completion marker has no recognized page section')
        if len(heads)>1 or len(done)>1:flags.append(dict(kind='page key multiplicity',key=unit+'-'+page,section_count=len(heads),completion_count=len(done)))
    for unit,page in (page_heads.keys()|page_done.keys())-expected:issue('progress/CHECK_RECORD',unit+'-'+page,'key','page key outside pinned expected set')
    translations=[]
    for layer in CONFIG:
        if layer in ('fr','fr_printed'):continue
        for unit in expected_units(layer):
            own=translation_heads[layer,unit];parent=PARENTS.get(layer);parent_sections=translation_heads.get((parent,unit),[]) if parent else []
            combined=[s for s in parent_sections if locator(s['body'],layer,unit)]
            chosen=own+combined;done=lang_done[layer,unit];parent_done=lang_done.get((parent,unit),[]) if combined else []
            present=any(locator(s['body'],layer,unit) for s in chosen)
            translations.append(dict(layer=layer,unit=unit,own_heading_count=len(own),eligible_parent_heading_count=len(combined),own_completion_count=len(done),eligible_parent_completion_count=len(parent_done),source_locator_present=present,status='recorded markers present' if chosen and (done or parent_done) and (present or not args.require_source_locators) else 'pending coverage'))
            if done and not chosen:issue('progress/CHECK_RECORD',layer+'/'+unit,'correspondence','language completion has no recognized corresponding section')
            if len(own)>1 or len(done)>1:flags.append(dict(kind='language key multiplicity',key=layer+'/'+unit,section_count=len(own),completion_count=len(done)))
    repeated_ids=[dict(id_sha256=sha(value.encode()),row_ids=','.join(ids),count=len(ids)) for value,ids in event_ids.items() if len(ids)>1]
    pending_pages=sum(r['status']=='pending coverage' for r in coverage);pending_translations=sum(r['status']=='pending coverage' for r in translations)
    for name,data in captured.items():
        if (work/name).read_bytes()!=data:raise RuntimeError('An input ledger changed while being checked; use a frozen copy')
    output.mkdir(parents=True)
    specifications=[('SYNTAX_ISSUES.tsv',['file','row_id','data_row','physical_start','physical_end','field','code'],syntax),('EXACT_DUPLICATE_ROWS.tsv',['file','row_ids','data_rows','physical_ranges','count','extra_rows','row_sha256'],duplicates),('ADVISORIES.tsv',['file','row_id','data_row','code','value_sha256'],advisory),('CATEGORY_COUNTS.tsv',['file','field','category','count'],categories),('TIMESTAMP_CHECKS.tsv',['file','row_id','valid','precision','value_sha256'],timestamps),('REQUIRED_SOURCES.tsv',['source','required','present','excluded_reason'],sources),('RECORD_SECTIONS.tsv',['row_id','line','level','kind','key','heading_sha256'],section_rows),('PROGRESS_MARKERS.tsv',['row_id','line','kind','key','line_sha256'],progress_rows),('FRENCH_COVERAGE.tsv',list(coverage[0]),coverage),('TRANSLATION_COVERAGE.tsv',list(translations[0]),translations),('KEY_MULTIPLICITY.tsv',['kind','key','section_count','completion_count'],flags),('REPEATED_EVENT_IDS.tsv',['id_sha256','row_ids','count'],repeated_ids)]
    for name,columns,rows in specifications:table(output/name,columns,rows)
    summary=dict(started_utc=started,completed_utc=utc(),policy_sha256=sha(policy_bytes),script_sha256=sha(Path(__file__).read_bytes()),correction_rows=len(ledgers['CORRECTIONS.tsv']),event_rows=len(ledgers['CHECK_EVENTS.tsv']),syntax_issue_count=len(syntax),exact_duplicate_groups=len(duplicates),exact_duplicate_extra_rows=sum(r['extra_rows'] for r in duplicates),advisory_count=len(advisory),key_multiplicity_groups=len(flags),repeated_event_id_groups=len(repeated_ids),expected_french_pages=len(expected),recorded_french_pages=len(expected)-pending_pages,pending_french_pages=pending_pages,expected_translation_units=len(translations),recorded_translation_units=len(translations)-pending_translations,pending_translation_units=pending_translations,required_sources=len([s for s in sources if s['required']]),missing_required_sources=sum(s['required'] and not s['present'] for s in sources),timestamp_checks=len(timestamps),invalid_timestamps=sum(not s['valid'] for s in timestamps),input_sha256={name:sha(data) for name,data in captured.items()},source_or_ledger_writes=False,substantive_validity_assessed=False,strict_legacy_event_vocabulary=args.strict_legacy_events,completion_required=args.require_complete)
    if (work/'SNAPSHOT.json').exists():summary['frozen_snapshot']=json.loads((work/'SNAPSHOT.json').read_text())
    summary['recorded_pages_with_literal_locator_gaps']=sum(bool(r['heading_count']) and bool(r['completion_count']) and not (r['fr_locator_present'] and r['fr_printed_locator_present']) for r in coverage)
    summary['literal_source_locators_required']=args.require_source_locators
    summary['checkpoint_exclusion_code_sha256']=sha(Path(exclude_reason.__code__.co_filename).read_bytes())
    summary['source_route_code_sha256']=sha(Path(source_path.__code__.co_filename).read_bytes())
    summary['structural_gate_passed']=not syntax and not duplicates and not flags
    summary['coverage_gate_passed']=not pending_pages and not pending_translations
    (output/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ['correction_rows','event_rows','syntax_issue_count','exact_duplicate_groups','advisory_count','recorded_french_pages','pending_french_pages','pending_translation_units','invalid_timestamps']},sort_keys=True))
    if not summary['structural_gate_passed'] or (args.require_complete and not summary['coverage_gate_passed']):raise SystemExit(1)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True,help='new report directory; inputs are never modified')
    parser.add_argument('--policy',type=Path,default=Path(__file__).with_name('structural_gate_policy.json'))
    parser.add_argument('--require-complete',action='store_true',help='also fail when coverage markers remain pending')
    parser.add_argument('--strict-legacy-events',action='store_true',help='promote legacy event-vocabulary advisories to syntax issues')
    parser.add_argument('--require-source-locators',action='store_true',help='also require exact source locators inside recorded sections; otherwise inventory them only')
    run(parser.parse_args())

if __name__=='__main__':main()
