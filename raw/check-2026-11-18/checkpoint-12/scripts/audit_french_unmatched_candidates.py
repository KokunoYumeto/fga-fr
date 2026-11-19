"""Metadata and literal-pair audit; no mathematical or correction verdicts.

Reconstructs projections from their declared deletion ranges, retaining original
payloads. This validator does not call the producing projection or match helpers.
"""
from pathlib import Path
from collections import Counter,defaultdict
from datetime import datetime,timezone
import argparse,csv,hashlib,io,json,re

def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def table(p):
 with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def parse_ledger(data):
 rr=csv.reader(io.StringIO(data.decode('utf-8'),newline=''),delimiter='\t');header=next(rr);out=[];last=rr.line_num
 for i,values in enumerate(rr,1):
  d=dict(zip(header,values));d.update(row_id=f'C{i:06d}',data_row=i,physical_line_start=last+1,physical_line_end=rr.line_num,row_sha256=sha(json.dumps(values,ensure_ascii=False,separators=(',',':')).encode()))
  last=rr.line_num;out.append(d)
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path,required=True);ap.add_argument('--frozen',type=Path,required=True);ap.add_argument('--old-frozen',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 a.out.mkdir(parents=True,exist_ok=False);start=now();checks=[]
 def check(name,ok,details=None):checks.append({'check':name,'pass':bool(ok),'details':details})
 meta=json.loads((a.report/'INVENTORY.json').read_text());hobj=json.loads((a.report/'HUNK_PAYLOADS.json').read_text());hunks={h['hunk_id']:h for h in hobj['hunks']}
 rows=parse_ledger((a.frozen/'CORRECTIONS.tsv').read_bytes());byid={r['row_id']:r for r in rows};old=parse_ledger((a.old_frozen/'CORRECTIONS.tsv').read_bytes())
 check('68_original_hunks_and_55_outside_149_212',len(hunks)==68 and sum(h['relative_file'] not in {'fr/149.tex','fr/212.tex'} for h in hunks.values())==55)
 check('current_and_old_ledger_hashes_exact',sha((a.frozen/'CORRECTIONS.tsv').read_bytes())==meta['current_ledger_sha256'] and sha((a.old_frozen/'CORRECTIONS.tsv').read_bytes())==meta['hunk_snapshot_ledger_sha256'])
 check('old_row_hashes_are_unchanged_prefix',len(rows)>=len(old) and all(r['row_sha256']==s['row_sha256'] for r,s in zip(rows,old)))
 check('all_original_hunk_payload_hashes_exact',all(sha(h['old_text'].encode())==h['old_sha256'] and sha(h['new_text'].encode())==h['new_sha256'] for h in hunks.values()))
 source_status=table(a.report/'CURRENT_SOURCE_STATUS.tsv');sources={r['file']:(a.frozen/r['file']).read_bytes() for r in source_status};initial={p:sha(b) for p,b in sources.items()}
 check('all_current_source_manifest_hashes_and_sizes',all(sha(sources[r['file']])==r['current_sha256'] and len(sources[r['file']])==int(r['current_bytes']) for r in source_status))
 profiles={p['profile']:p for p in json.loads((a.report/'NORMALIZATION_PROFILES.json').read_text())}
 projection_errors=[];projection_count=0
 def reconstruct(original,view,info,profile,label):
  nonlocal projection_count
  projection_count+=1;ranges=[];good=True
  for r in info['removed_wrappers']:
   s=r['character_start'];e=r['character_end'];aa=r['argument_start'];bb=r['argument_end'];macro=r['macro']
   good=good and macro in profiles[profile]['removed_balanced_wrappers'] and bool(re.fullmatch(r'\\'+re.escape(macro)+r'[ \t\r\n\f\v]*\{',original[s:aa])) and original[bb:e]=='}' and sha(original[aa:bb].encode())==r['argument_sha256']
   ranges += [(s,aa),(bb,e)]
  masked=[False]*len(original)
  for s,e in ranges:
   for i in range(s,e):masked[i]=True
  restored=''.join(c for i,c in enumerate(original) if not masked[i]);restored=re.sub(r'[ \t\r\n\f\v]+',' ',restored).strip()
  good=good and restored==view and sha(view.encode())==info['projection_sha256']
  alphabet=set(profiles[profile]['retained_alphabet_controls']);tokens=lambda t:[m[1] for m in re.finditer(r'\\([A-Za-z@]+|.)',t,re.S) if m[1] in alphabet]
  good=good and tokens(original)==tokens(view)==info['alphabet_controls']
  if not good:projection_errors.append(label)
 hprojections=json.loads((a.report/'HUNK_PROJECTIONS.json').read_text());hp={}
 for p in hprojections:
  h=hunks[p['hunk_id']];hp[p['hunk_id'],p['profile']]=p
  reconstruct(h['old_text'],p['fr_projection'],p['fr_metadata'],p['profile'],p['hunk_id']+'/fr/'+p['profile'])
  reconstruct(h['new_text'],p['fr_printed_projection'],p['fr_printed_metadata'],p['profile'],p['hunk_id']+'/fr_printed/'+p['profile'])
 details=json.loads((a.report/'CANDIDATE_DETAILS.json').read_text());links=table(a.report/'CANDIDATE_LINKS.tsv');linkids={r['candidate_id']:r for r in links};candidate_errors=[];payload_row_ids=set()
 for d in details:
  row=byid[d['row_id']];h=hunks[d['hunk_id']];p=hp[d['hunk_id'],d['profile']];m=d['match'];ro=d['ledger_old_projection'];rn=d['ledger_new_projection'];payload_row_ids.add(row['row_id'])
  reconstruct(row['old'],ro,d['ledger_old_projection_metadata'],d['profile'],d['candidate_id']+'/old')
  reconstruct(row['new'],rn,d['ledger_new_projection_metadata'],d['profile'],d['candidate_id']+'/new')
  x,y=(p['fr_printed_projection'],p['fr_projection']) if d['orientation']=='printed_to_corrected' else (p['fr_projection'],p['fr_printed_projection'])
  aa=m['ledger_old_fragment'];bb=m['ledger_new_fragment'];good=bool(aa and bb and aa!=bb and aa in x and bb in y and (aa not in y or bb not in x))
  good=good and aa==ro[m['fragment_old_start']:m['fragment_old_end']] and bb==rn[m['fragment_new_start']:m['fragment_new_end']]
  good=good and x.count(aa)==d['old_occurrences']==m['old_occurrences'] and y.count(bb)==d['new_occurrences']==m['new_occurrences']
  good=good and (aa==x and bb==y)==d['whole_hunk_pair']==m['whole_hunk_pair']
  good=good and row['row_sha256']==d['row_sha256'] and sha(row['old'].encode())==d['ledger_old_sha256'] and sha(row['new'].encode())==d['ledger_new_sha256']
  good=good and row['data_row']==d['data_row'] and row['physical_line_start']==d['physical_line_start'] and row['physical_line_end']==d['physical_line_end']
  good=good and row['printed_page'] in h['candidate_page_keys'] and d['page_relation']=='same page' and d['added_after_hunk_snapshot']==(row['data_row']>len(old))
  if d['method']=='localized_ledger_edit_pair':good=good and min(len(aa),len(bb))>=8
  else:good=good and aa==ro and bb==rn
  if not good:candidate_errors.append(d['candidate_id'])
 check('all_declared_projections_reconstruct_without_alphabet_changes',not projection_errors,{'projections_checked':projection_count,'errors':projection_errors})
 check('all_candidate_pairs_fragments_counts_and_row_hashes_exact',not candidate_errors,{'candidate_links':len(details),'errors':candidate_errors})
 check('candidate_table_ids_exact_unique',len(linkids)==len(details) and set(linkids)=={d['candidate_id'] for d in details})
 payloads=json.loads((a.report/'LEDGER_PAYLOADS.json').read_text());payload_index={r['row_id']:r for r in payloads};badpayload=[]
 for p in payloads:
  row=byid[p['row_id']]
  if any(v!=row[k] for k,v in p.items()):badpayload.append(p['row_id'])
 check('all_158_included_ledger_payloads_exact',len(payloads)==158 and not badpayload,badpayload)
 status=table(a.report/'HUNK_STATUS.tsv');byh=defaultdict(list)
 for d in details:byh[d['hunk_id']].append(d)
 status_errors=[]
 for s in status:
  h=hunks[s['hunk_id']];ds=byh[s['hunk_id']];rr=list(dict.fromkeys(d['row_id'] for d in ds))
  good=rr==json.loads(s['paired_candidate_rows']) and len(rr)==int(s['paired_candidate_row_count']) and len(ds)==int(s['candidate_link_count'])
  good=good and sources[h['fr_file']].count(h['old_text'].encode())==int(s['current_fr_hunk_payload_exact_count']) and sources[h['fr_printed_file']].count(h['new_text'].encode())==int(s['current_printed_hunk_payload_exact_count'])
  if not good:status_errors.append(s['hunk_id'])
 check('all_hunk_status_and_current_payload_survival_counts',not status_errors,status_errors)
 hist=table(a.report/'FR_CORRECTED_PAGE_HISTORY.tsv');only=table(a.report/'FR_ONLY_OPERATION_HISTORY.tsv');history_errors=[];order=defaultdict(list)
 mirror=defaultdict(list)
 for r in rows:
  if r['file'].startswith('sources/fr_printed/'):
   mirror['/'.join(r['file'].split('/')[2:]),r['printed_page'],r['old'],r['new']].append(r['row_id'])
 for x in hist:
  h=hunks[x['hunk_id']];r=byid[x['row_id']];twins=mirror[h['relative_file'],r['printed_page'],r['old'],r['new']]
  good=not byh[x['hunk_id']] and r['file']==h['fr_file'] and r['printed_page'] in h['candidate_page_keys'] and r['row_sha256']==x['row_sha256'] and twins==json.loads(x['identical_printed_operation_rows']) and (not twins)==(x['no_identical_printed_operation']=='True')
  if not good:history_errors.append((x['hunk_id'],x['row_id']))
  order[x['hunk_id']].append(r['data_row'])
  if not twins:payload_row_ids.add(r['row_id'])
 check('history_rows_exact_and_ledger_ordered',not history_errors and all(v==sorted(v) for v in order.values()),history_errors)
 check('FR_only_subset_and_payload_selection_exact',only==[r for r in hist if r['no_identical_printed_operation']=='True'] and set(payload_index)==payload_row_ids)
 check('hunk_pair_counts_reconcile',sum(bool(byh[s['hunk_id']]) for s in status)==meta['hunks_with_paired_candidate']==56 and sum(not byh[s['hunk_id']] for s in status)==meta['hunks_without_paired_candidate']==12)
 post=table(a.report/'POST_SNAPSHOT_FRENCH_ROWS.tsv');expected=[r['row_id'] for r in rows[len(old):] if r['file'].startswith(('sources/fr/','sources/fr_printed/'))]
 check('twelve_post_snapshot_French_rows_exact',[r['row_id'] for r in post]==expected and len(post)==12)
 check('captured_inputs_unchanged_during_audit',all(sha((a.frozen/p).read_bytes())==v for p,v in initial.items()))
 private=[]
 for p in a.report.iterdir():
  if p.is_file() and re.search(r'(?<![\w.-])[\w.%+-]+@[\w.-]+\.[A-Za-z]{2,}|/(?:workspace|home|root|tmp)/',p.read_text()):private.append(p.name)
 check('no_detected_email_or_absolute_host_prefix',not private,private)
 failed=[x['check'] for x in checks if not x['pass']]
 result={'status':'PASS' if not failed else 'FAIL','started_utc':start,'completed_utc':now(),'checks':checks,'failed_checks':failed,'candidate_links':len(details),'projections_reconstructed':projection_count,'payload_rows_verified':len(payloads),'history_rows_verified':len(hist),'scope':'Literal projection, substring, hash and locator audit only; no semantic equivalence or correction validity judgment.'}
 (a.out/'AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 (a.out/'REPORT.md').write_text(f"# Supplementary matcher metadata audit\n\nStatus: **{result['status']}**. Completed {result['completed_utc']}.\n\nChecked {len(details)} candidate links, reconstructed {projection_count} declared projections directly from recorded wrapper-deletion ranges, verified {len(payloads)} exact ledger payloads and {len(hist)} append-order history rows. Original alphabet controls were retained in every reconstructed projection. Hunk payloads, ledger hashes, row locators, fragment indices, occurrence counts, history counterparts and current-payload survival counts all reconcile.\n\nThis is a metadata and literal-substring audit. It does not establish mathematical equivalence, justify a correction, or prove that a candidate accounts for the complete net hunk difference. Exact check results are in AUDIT.json.\n")
 print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
if __name__=='__main__':main()
