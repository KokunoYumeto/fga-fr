"""Independent byte/locator and macro-completeness audit of a candidate inventory.

This audit does not adjudicate a mathematical statement or the meaning of an
identifier match. It reads a frozen input capture and writes audit evidence.
"""
from pathlib import Path
from collections import Counter,defaultdict
from datetime import datetime,timezone
import argparse,csv,hashlib,json,re,unicodedata

def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def table(p):
 with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def mask(data):
 a=bytearray(data)
 for m in re.finditer(rb'%',data):
  i=m.start();n=0
  while i-n-1>=0 and data[i-n-1]==92:n+=1
  if n%2:continue
  e=data.find(b'\n',i);e=len(data) if e<0 else e
  a[i:e]=b' '*(e-i)
 return bytes(a)
def normalized(s):return ''.join(x for x in unicodedata.normalize('NFD',s.casefold()) if not unicodedata.combining(x))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--snapshot',type=Path,required=True);ap.add_argument('--frozen',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 a.out.mkdir(parents=True,exist_ok=False);start=now();checks=[]
 def check(name,condition,details=None):checks.append({'check':name,'pass':bool(condition),'details':details})
 manifest=table(a.snapshot/'SOURCE_HASHES.tsv');data={r['file']:(a.frozen/r['file']).read_bytes() for r in manifest}
 initial={r:sha(b) for r,b in data.items()}
 check('60_captured_inputs',len(data)==60)
 check('all_frozen_sizes_and_hashes_match',all(len(data[r['file']])==int(r['bytes']) and sha(data[r['file']])==r['sha256'] for r in manifest))
 headings=table(a.snapshot/'SOURCE_HEADINGS.tsv');byid={r['heading_id']:r for r in headings}
 check('unique_heading_identifiers',len(byid)==len(headings))
 errors=[]
 for r in headings:
  b=data[r['file']];s=int(r['byte_start']);e=int(r['byte_end']);ls=b.rfind(b'\n',0,s)+1
  good=b[s:e].decode('utf-8')==r['heading_exact'] and b.count(b'\n',0,s)+1==int(r['source_line']) and b.count(b'\n',0,e)+1==int(r['source_end_line']) and s-ls+1==int(r['column_byte']) and len(b[ls:s].decode('utf-8'))+1==int(r['column_character'])
  page_matches=[m for m in re.finditer(rb'\\src\{([0-9]+)\}',mask(b)) if m.start()<=s]
  page=page_matches[-1][1].decode() if page_matches else ''
  good=good and page==r['preceding_literal_page']
  if not good:errors.append(r['heading_id'])
 check('all_heading_bytes_lines_columns_and_pages_exact',not errors,errors)
 offsets={(r['file'],int(r['byte_start'])):r for r in headings}
 macro_errors=[];macro_counts=Counter()
 unit_names={'149','182','190','195','212','221','232','236','com','e149','e182','e190','e195','e212','e221','e232','e236'}
 units={rel for rel in data if rel.startswith('sources/') and Path(rel).suffix=='.tex' and Path(rel).stem in unit_names}
 check('all_34_unit_files_in_macro_and_manual_sweeps',len(units)==34)
 for rel in sorted(units):
  b=mask(data[rel])
  for m in re.finditer(rb'\\(result|fsection|section|subsection|subsubsection|paragraph|subparagraph)(?![A-Za-z@])',b):
   cmd=m[1].decode();macro_counts[cmd]+=1
   row=offsets.get((rel,m.start()))
   if not row or not row['heading_exact'].startswith('\\'+cmd):macro_errors.append((rel,b.count(b'\n',0,m.start())+1,cmd))
 check('every_literal_heading_macro_has_inventory_row',not macro_errors,{'counts':dict(macro_counts),'unmatched':macro_errors})
 check('all_506_result_macros_and_82_fsection_macros_accounted',macro_counts['result']==506 and macro_counts['fsection']==82)
 # An independent line-prefix sweep finds formatted manual named headings.
 names='PROPOSITION|THÉORÈME|THEOREME|LEMME|COROLLAIRE|REMARQUE|REMARQUES|DÉFINITION|DEFINITION|EXEMPLE|EXEMPLES|SCHOLIE|CONJECTURE|CRITÈRE|CRITERE'
 manual=[];manual_bad=[]
 for rel in sorted(units):
  b=mask(data[rel]);off=0
  for line in b.splitlines(keepends=True):
   ss=line.decode('utf-8').strip()
   projection=re.sub(r'\\[A-Za-z@]+\*?','',ss);projection=re.sub(r'[{}$]','',projection)
   explicit=re.match(r'^(?:\\par\s*)*\\(?:noindent|uline|textnormal|textbf|textit|emph|normalfont)\b',ss)
   m=re.match(r'(?i)^(?:[a-z]\.\s*)?('+names+r')\s+(\d+(?:[.,]\s*\d+)*)',projection)
   if explicit and m and not ss.startswith('\\result'):
    pos=off+len(line)-len(line.lstrip());manual.append((rel,pos))
    row=offsets.get((rel,pos))
    if not row or row['category']!='named_numbered_statement':manual_bad.append((rel,b.count(b'\n',0,pos)+1))
   off+=len(line)
 check('formatted_manual_numbered_heading_sweep',not manual_bad,{'literal_manual_headings':len(manual),'unmatched':manual_bad})
 check('unformatted_named_reference_candidates_not_core',all(r['category']=='line_start_named_reference_candidate' for r in headings if r['identifier_origin']=='unformatted line-start keyword; heading not asserted'))
 # Exact input events, record locators, and all published foreign keys.
 source_events=table(a.frozen/'CHECK_EVENTS.tsv');events=table(a.snapshot/'EVENT_LOCATORS.tsv');event_byrow={r['event_row']:r for r in events}
 check('all_event_records_retained_exactly',len(events)==len(source_events) and all(all(e[k]==s[k] for k in s) for e,s in zip(events,source_events)))
 links=table(a.snapshot/'EVENT_CANDIDATES.tsv');link_errors=[]
 for r in links:
  h=byid.get(r['heading_id']);e=event_byrow.get(r['event_row'])
  good=h and e and r['event_id']==e['id'] and r['event_where']==e['where'] and r['event_physical_start']==e['physical_start'] and r['event_physical_end']==e['physical_end'] and r['source_file']==h['file'] and r['source_line']==h['source_line'] and r['source_page']==h['preceding_literal_page'] and r['unit']==h['unit'] and r['layer']==h['layer'] and h['unit'] in e['literal_units'].split(',')
  if not good:link_errors.append((r['heading_id'],r['event_row']))
 check('all_event_link_foreign_keys_and_exact_locators',not link_errors,link_errors)
 records=table(a.snapshot/'RECORD_CANDIDATES.tsv');record_lines=data['CHECK_RECORD.md'].decode().splitlines();record_errors=[]
 for r in records:
  line=int(r['record_line']);section=int(r['record_section_line']);h=byid.get(r['heading_id'])
  actual=record_lines[line-1] if 0<line<=len(record_lines) else None
  if r['match_scope']=='page-section context only':actual=re.sub(r'^#{1,6}\s+','',actual or '')
  okay=h and actual==r['line_exact'] and re.sub(r'^#{1,6}\s+','',record_lines[section-1])==r['record_section_heading'] and h['unit']==r['unit'] and h['layer']==r['layer'] and h['preceding_literal_page']==r['source_page']
  if not okay:record_errors.append((r['heading_id'],line))
 check('all_record_line_and_page_section_locators_exact',not record_errors,record_errors)
 coverage=table(a.snapshot/'CANDIDATE_COVERAGE.tsv');groups=defaultdict(list)
 for r in links:groups[r['heading_id']].append(r)
 coverage_errors=[]
 for r in coverage:
  rr=groups[r['heading_id']];ident=[x for x in rr if x['identifier_features']]
  good=int(r['identifier_event_candidates'])==len(ident) and int(r['same_page_identifier_candidates'])==sum(x['page_relation']=='same literal page' for x in ident) and int(r['different_page_identifier_candidates'])==sum(x['page_relation']=='different literal page' for x in ident) and int(r['page_only_event_candidates'])==sum(not x['identifier_features'] for x in rr)
  if not good:coverage_errors.append(r['heading_id'])
 check('candidate_coverage_counts_reconcile',not coverage_errors,coverage_errors)
 no_ids=table(a.snapshot/'NO_IDENTIFIER_CANDIDATE.tsv');ambiguous=table(a.snapshot/'AMBIGUOUS_OR_DIFFERENT_PAGE.tsv')
 check('no_identifier_subset_exact',no_ids==[r for r in coverage if int(r['identifier_event_candidates'])==0])
 check('ambiguous_or_different_page_subset_exact',ambiguous==[r for r in coverage if int(r['identifier_event_candidates'])>1 or int(r['different_page_identifier_candidates'])>0])
 meta=json.loads((a.snapshot/'INVENTORY.json').read_text())
 check('snapshot_totals_reconcile',len(headings)==meta['source_heading_rows'] and len(coverage)==meta['core_candidate_headings'] and len(events)==meta['event_rows'] and len(links)==meta['event_candidate_rows'] and len(records)==meta['record_candidate_rows'])
 check('zero_unparsed_result_macros',not table(a.snapshot/'PARSER_ISSUES.tsv'))
 check('frozen_inputs_unchanged_through_audit',all(sha((a.frozen/r).read_bytes())==v for r,v in initial.items()))
 privacy=[]
 for p in list(a.snapshot.glob('*'))+[Path('FGA_CHECK/scripts/statement_event_coverage.py')]:
  if not p.is_file():continue
  text=p.read_text()
  if re.search(r'(?<![\w.-])[\w.%+-]+@[\w.-]+\.[A-Za-z]{2,}|/(?:workspace|home|root|tmp)/',text):privacy.append(p.name)
 check('no_detected_email_or_absolute_host_prefix',not privacy,privacy)
 failed=[r['check'] for r in checks if not r['pass']]
 result={'status':'PASS' if not failed else 'FAIL','started_utc':start,'completed_utc':now(),'checks':checks,'failed_checks':failed,'heading_rows':len(headings),'named_numbered_headings':sum(r['category']=='named_numbered_statement' for r in headings),'core_candidate_headings':len(coverage),'event_rows':len(events),'event_links':len(links),'record_links':len(records),'macro_counts':dict(macro_counts),'scope':'Lexical input integrity and locator validation only; no mathematical or reading-coverage conclusion.'}
 (a.out/'AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 report=f'''# Statement/event inventory metadata audit\n\nStatus: **{result['status']}**. Completed {result['completed_utc']}.\n\nThis audit checks frozen bytes, explicit heading-macro enumeration and locator consistency. It does not decide statement meaning, proof validity, scan readings or whether an event substantively covers a heading.\n\n- {len(headings)} exact heading/list spans verified, including {result['named_numbered_headings']} named numbered headings across both French layers.\n- All {macro_counts['result']} literal result macros and {macro_counts['fsection']} fsection macros have inventory entries. Optional result arguments are included by the producing parser.\n- {len(manual)} formatted manual numbered headings independently located by a separate line-prefix sweep.\n- {len(events)} event records preserved exactly, {len(links)} event link locators and {len(records)} record link locators verified.\n- Candidate counts and unmatched/ambiguous subsets reconcile; no unresolved result-macro parse issue.\n- Captured source and record bytes stayed unchanged throughout this audit. No source or main-record edit was made.\n\nFailed checks: {len(failed)}. Exact check details are in `AUDIT.json`. Source hashes and limitations remain in the inventory's README and tables.\n'''
 (a.out/'REPORT.md').write_text(report)
 print(json.dumps({k:v for k,v in result.items() if k!='checks'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
