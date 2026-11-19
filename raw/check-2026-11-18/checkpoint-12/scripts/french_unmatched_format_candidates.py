"""Supplementary lexical links for already-unmatched French difference hunks.

Read-only sources/ledger. Declared projections remove only balanced instances of
listed formatting wrappers and collapse ASCII whitespace. Alphabet commands are
retained. These projections are navigation aids, never semantic equivalences.
"""
from pathlib import Path
from collections import Counter,defaultdict
from functools import lru_cache
from datetime import datetime,timezone
import argparse,csv,difflib,hashlib,io,json,re
from french_layer_differences import ledger_rows,HEADER

SPACE=re.compile(r'[ \t\r\n\f\v]+')
CONTROL=re.compile(r'\\([A-Za-z@]+|.)',re.S)
PROFILES=[('P0_whitespace',()),('P1_upright',('symup',)),('P2_upright_uline',('symup','uline')),('P3_upright_underlines',('symup','uline','underline','uwave'))]
ALPHABETS={'mathcal','mathfrak','mathscr','mathbb','mathbf','mathrm','mathit','mathsf','mathtt','boldsymbol','operatorname','symbf','symcal','symfrak','symbb','symit','symrm','symnormal'}

def utc():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def tsv(p,fields,rows):
 with p.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n',extrasaction='ignore');w.writeheader()
  for r in rows:w.writerow({k:json.dumps(v,ensure_ascii=False,separators=(',',':')) if isinstance(v,(list,dict)) else v for k,v in r.items()})
def balanced(text,pos):
 if pos>=len(text) or text[pos]!='{':return None
 depth=1;i=pos+1
 while i<len(text):
  if text[i]=='\\':
   m=CONTROL.match(text,i);i=m.end() if m else i+1;continue
  if text[i]=='%':
   e=text.find('\n',i);i=len(text) if e<0 else e+1;continue
  if text[i]=='{':depth+=1
  elif text[i]=='}':
   depth-=1
   if depth==0:return i+1
  i+=1
 return None

def alphabet_controls(text):return [m[1] for m in CONTROL.finditer(text) if m[1] in ALPHABETS]
@lru_cache(maxsize=None)
def project(text,profile):
 allowed=dict(PROFILES)[profile];removed=[];unparsed=[]
 def scan(lo,hi):
  chunks=[];i=lo
  while i<hi:
   if text[i]=='%':
    e=text.find('\n',i,hi);e=hi if e<0 else e+1;chunks.append(text[i:e]);i=e;continue
   if text[i]=='\\':
    m=CONTROL.match(text,i)
    if m:
     if m[1] in allowed:
      at=m.end()
      while at<hi and text[at] in ' \t\r\n\f\v':at+=1
      end=balanced(text,at)
      if end and end<=hi:
       removed.append({'macro':m[1],'character_start':i,'character_end':end,'argument_start':at+1,'argument_end':end-1,'argument_sha256':sha(text[at+1:end-1].encode()),'potential_notational_distinction':m[1] in {'uline','underline','uwave'}})
       chunks.append(scan(at+1,end-1));i=end;continue
      unparsed.append({'macro':m[1],'character_start':i,'reason':'not an exact balanced one-braced-argument wrapper'})
     chunks.append(m[0]);i=m.end();continue
   chunks.append(text[i]);i+=1
  return ''.join(chunks)
 value=SPACE.sub(' ',scan(0,len(text))).strip()
 before=alphabet_controls(text);after=alphabet_controls(value)
 if before!=after:raise AssertionError('A retained alphabet command changed during projection.')
 return value,{'removed_wrappers':removed,'unparsed_allowed_commands':unparsed,'alphabet_controls':before,'alphabet_controls_preserved':True,'projection_sha256':sha(value.encode()),'sensitive_wrapper_removed':any(x['potential_notational_distinction'] for x in removed)}
@lru_cache(maxsize=None)
def deltas(old,new):
 ops=difflib.SequenceMatcher(None,old,new,autojunk=False).get_opcodes();out=[]
 for k,(tag,i,j,u,v) in enumerate(ops):
  if tag=='equal':continue
  before=old[ops[k-1][1]:i] if k and ops[k-1][0]=='equal' else ''
  after=old[j:ops[k+1][2]] if k+1<len(ops) and ops[k+1][0]=='equal' else ''
  out.append((tag,i,j,u,v,before,after))
 return out

def distinguishing(a,b,x,y):return bool(a and b and a!=b and a in x and b in y and (a not in y or b not in x))
def find_pair(row_old,row_new,left,right,same_page):
 found=[]
 for orientation,x,y in [('printed_to_corrected',right,left),('corrected_to_printed',left,right)]:
  if distinguishing(row_old,row_new,x,y):
   found.append({'orientation':orientation,'method':'full_ledger_payload_pair','ledger_old_fragment':row_old,'ledger_new_fragment':row_new,'fragment_old_start':0,'fragment_old_end':len(row_old),'fragment_new_start':0,'fragment_new_end':len(row_new),'context_before':0,'context_after':0,'old_occurrences':x.count(row_old),'new_occurrences':y.count(row_new),'whole_hunk_pair':row_old==x and row_new==y,'short_fragment':min(len(row_old),len(row_new))<8})
   continue
  if not same_page:continue
  for tag,i,j,u,v,before,after in deltas(row_old,row_new):
   for size in [48,32,24,16,12,8,4,2,0]:
    pre=before[-size:] if size else '';post=after[:size] if size else ''
    a=pre+row_old[i:j]+post;b=pre+row_new[u:v]+post
    if min(len(a),len(b))<8:continue
    if distinguishing(a,b,x,y):
     found.append({'orientation':orientation,'method':'localized_ledger_edit_pair','edit_opcode':tag,'ledger_old_fragment':a,'ledger_new_fragment':b,'fragment_old_start':i-len(pre),'fragment_old_end':j+len(post),'fragment_new_start':u-len(pre),'fragment_new_end':v+len(post),'context_before':len(pre),'context_after':len(post),'old_occurrences':x.count(a),'new_occurrences':y.count(b),'whole_hunk_pair':a==x and b==y,'short_fragment':False})
     break
 return found

def md_payload(row):
 fields=['file','layer','printed_page','line','statement','kind','confidence']
 s=[f"## {row['row_id']}\n",f"Ledger data row {row['data_row']}; physical lines {row['physical_line_start']}–{row['physical_line_end']}.\n",f"Row SHA-256: `{row['row_sha256']}`. Old SHA-256: `{sha(row['old'].encode())}`. New SHA-256: `{sha(row['new'].encode())}`.\n"]
 s += [f"**{key}:** {row[key]}\n" for key in fields]
 for key in ['old','new','evidence']:
  s += [f'### {key}\n','````tex\n'+row[key]+'\n````\n']
 return '\n'.join(s)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,default=Path('FGA_CHECK'));ap.add_argument('--hunks',type=Path,required=True);ap.add_argument('--snapshot',type=Path,required=True);ap.add_argument('--old-frozen',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--frozen',type=Path,required=True);a=ap.parse_args()
 if a.out.exists() or a.frozen.exists():raise FileExistsError('Use new output and frozen-input directories.')
 if any(p.resolve().is_relative_to((a.work/'sources').resolve()) for p in [a.out,a.frozen]):raise ValueError('Outputs must not enter source trees.')
 started=utc();hunk_bytes=a.hunks.read_bytes();hobj=json.loads(hunk_bytes);hunks=hobj['hunks'];assert len(hunks)==68
 old_ledger_bytes=(a.old_frozen/'CORRECTIONS.tsv').read_bytes();old_rows=ledger_rows(old_ledger_bytes);old_summary=json.loads((a.snapshot/'SUMMARY.json').read_text());old_manifest=json.loads((a.snapshot/'FROZEN_SNAPSHOT.json').read_text())
 paths=['CORRECTIONS.tsv']+[p.relative_to(a.work).as_posix() for layer in ['fr','fr_printed'] for p in sorted((a.work/'sources'/layer).rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
 for attempt in range(1,6):
  captured={p:(a.work/p).read_bytes() for p in paths}
  if captured=={p:(a.work/p).read_bytes() for p in paths}:break
 else:raise RuntimeError('No stable capture after five immediate attempts.')
 capture_end=utc();a.out.mkdir(parents=True);a.frozen.mkdir(parents=True)
 for p,b in captured.items():
  dest=a.frozen/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
 rows=ledger_rows(captured['CORRECTIONS.tsv']);byid={r['row_id']:r for r in rows};prefix_ok=len(rows)>=len(old_rows) and all(x['row_sha256']==y['row_sha256'] for x,y in zip(rows,old_rows))
 original_hashes={x['path']:x for x in old_manifest['files']};source_status=[]
 for p,b in captured.items():
  old=original_hashes.get(p)
  source_status.append({'file':p,'current_bytes':len(b),'current_sha256':sha(b),'hunk_snapshot_sha256':old['sha256'] if old else '', 'unchanged_since_hunk_snapshot':bool(old and sha(b)==old['sha256'])})
 french=[r for r in rows if r['file'].startswith(('sources/fr/fr/','sources/fr_printed/fr/'))]
 byfile=defaultdict(list);bypage=defaultdict(list);mirrors=defaultdict(list)
 for r in french:
  suffix=r['file'].split('/fr/',1)[-1] if r['file'].startswith('sources/fr/') else r['file'].split('/fr_printed/',1)[-1]
  # Use the actual relative filename, retaining the inner fr/ component.
  suffix='/'.join(r['file'].split('/')[2:]);byfile[suffix].append(r)
  bypage[suffix,r['printed_page']].append(r)
  if r['file'].startswith('sources/fr_printed/'):
   mirrors[suffix,r['printed_page'],r['old'],r['new']].append(r['row_id'])
 candidates=[];details=[];statuses=[];payload_ids=set();history=[];projected=[]
 for h in hunks:
  left=h['old_text'];right=h['new_text'];pages=set(h['candidate_page_keys']);hfound=[];collapsed=[]
  assert sha(left.encode())==h['old_sha256'] and sha(right.encode())==h['new_sha256']
  for profile,allowed in PROFILES:
   l,lmeta=project(left,profile);r,rmeta=project(right,profile)
   projected.append({'hunk_id':h['hunk_id'],'profile':profile,'fr_projection':l,'fr_printed_projection':r,'fr_metadata':lmeta,'fr_printed_metadata':rmeta})
   if l==r:collapsed.append(profile);continue
   for row in byfile[h['relative_file']]:
    compatible=row['printed_page'] in pages
    if not compatible and min(len(row['old']),len(row['new']))<12:continue
    ro,rom=project(row['old'],profile);rn,rnm=project(row['new'],profile)
    if not ro or not rn or ro==rn:continue
    matches=find_pair(ro,rn,l,r,compatible)
    for match in matches:
     cid=f'FM{len(candidates)+1:06d}'
     record={'candidate_id':cid,'hunk_id':h['hunk_id'],'row_id':row['row_id'],'data_row':row['data_row'],'physical_line_start':row['physical_line_start'],'physical_line_end':row['physical_line_end'],'ledger_file':row['file'],'ledger_layer':row['layer'],'ledger_page':row['printed_page'],'ledger_kind':row['kind'],'page_relation':'same page' if compatible else 'different page','profile':profile,'method':match['method'],'orientation':match['orientation'],'whole_hunk_pair':match['whole_hunk_pair'],'old_occurrences':match['old_occurrences'],'new_occurrences':match['new_occurrences'],'short_fragment':match['short_fragment'],'sensitive_wrappers_removed':any(x['sensitive_wrapper_removed'] for x in [lmeta,rmeta,rom,rnm]),'alphabet_controls_preserved':True,'row_sha256':row['row_sha256'],'ledger_old_sha256':sha(row['old'].encode()),'ledger_new_sha256':sha(row['new'].encode()),'fr_hunk_sha256':h['old_sha256'],'fr_printed_hunk_sha256':h['new_sha256'],'added_after_hunk_snapshot':row['data_row']>len(old_rows),'payload_link':'LEDGER_PAYLOADS.md#'+row['row_id'].lower()}
     candidates.append(record);hfound.append(record);payload_ids.add(row['row_id'])
     details.append({**record,'match':match,'ledger_old_projection':ro,'ledger_new_projection':rn,'ledger_old_projection_metadata':rom,'ledger_new_projection_metadata':rnm})
  # If there is no paired link, provide all corrected-French page operations
  # in append order, marking absence of an identical printed-layer operation.
  hh=[]
  if not hfound:
   for row in french:
    if row['file']!=h['fr_file'] or row['printed_page'] not in pages:continue
    twin=mirrors[h['relative_file'],row['printed_page'],row['old'],row['new']]
    hr={'hunk_id':h['hunk_id'],'row_id':row['row_id'],'data_row':row['data_row'],'physical_line_start':row['physical_line_start'],'physical_line_end':row['physical_line_end'],'ledger_page':row['printed_page'],'kind':row['kind'],'statement':row['statement'],'identical_printed_operation_rows':twin,'no_identical_printed_operation':not twin,'added_after_hunk_snapshot':row['data_row']>len(old_rows),'row_sha256':row['row_sha256'],'payload_link':'LEDGER_PAYLOADS.md#'+row['row_id'].lower()}
    history.append(hr);hh.append(hr)
    if not twin:payload_ids.add(row['row_id'])
  frb=captured[h['fr_file']];prb=captured[h['fr_printed_file']]
  unique_rows=list(dict.fromkeys(x['row_id'] for x in hfound))
  statuses.append({'hunk_id':h['hunk_id'],'relative_file':h['relative_file'],'page_keys':h['candidate_page_keys'],'snapshot_status':h.get('post_snapshot_status',''),'current_fr_file_sha256':sha(frb),'current_printed_file_sha256':sha(prb),'current_fr_hunk_payload_exact_count':frb.count(left.encode()) if left else 0,'current_printed_hunk_payload_exact_count':prb.count(right.encode()) if right else 0,'paired_candidate_rows':unique_rows,'paired_candidate_row_count':len(unique_rows),'candidate_link_count':len(hfound),'profiles_with_pair':list(dict.fromkeys(x['profile'] for x in hfound)),'profiles_collapsing_hunk_difference':collapsed,'history_rows':len(hh),'history_without_identical_printed_operation':sum(x['no_identical_printed_operation'] for x in hh),'status':'paired lexical candidates; root review required' if hfound else 'no paired candidate; inspect append-order French history','review_link':'REVIEW.md#'+h['hunk_id'].lower()})
 payloads=[{k:r[k] for k in ['row_id','data_row','physical_line_start','physical_line_end','row_sha256',*HEADER]} for r in rows if r['row_id'] in payload_ids]
 profile_doc=[{'profile':name,'removed_balanced_wrappers':list(wrappers),'whitespace':'ASCII whitespace collapsed to one space and outer ASCII whitespace trimmed','retained_alphabet_controls':sorted(ALPHABETS),'meaning_warning':'These are lexical search projections only. Underlines and upright fonts can distinguish mathematical notation; removals are reported per field, never adjudicated as semantically harmless.'} for name,wrappers in PROFILES]
 metadata={'started_utc':started,'captured_current_inputs_utc':capture_end,'completed_utc':utc(),'capture_attempt':attempt,'hunk_snapshot_utc':hobj['snapshot'],'hunk_orientation':hobj['orientation'],'hunk_input_sha256':sha(hunk_bytes),'hunk_snapshot_ledger_sha256':sha(old_ledger_bytes),'current_ledger_sha256':sha(captured['CORRECTIONS.tsv']),'hunk_snapshot_ledger_rows':len(old_rows),'current_ledger_rows':len(rows),'old_ledger_row_hash_prefix_unchanged':prefix_ok,'unmatched_hunks':len(hunks),'hunks_outside_149_212':sum(h['relative_file'] not in {'fr/149.tex','fr/212.tex'} for h in hunks),'hunks_with_paired_candidate':sum(bool(s['paired_candidate_row_count']) for s in statuses),'hunks_without_paired_candidate':sum(not s['paired_candidate_row_count'] for s in statuses),'candidate_links':len(candidates),'distinct_candidate_ledger_rows':len({x['row_id'] for x in candidates}),'ledger_payload_rows':len(payloads),'history_rows_for_no_pair':len(history),'history_without_identical_printed_operation':sum(x['no_identical_printed_operation'] for x in history),'current_changed_French_files':[s['file'] for s in source_status if s['file'].startswith('sources/') and not s['unchanged_since_hunk_snapshot']],'hunks_with_old_fr_payload_not_present_now':[s['hunk_id'] for s in statuses if not s['current_fr_hunk_payload_exact_count']],'scope':'Mechanical candidate linkage only. No source, ledger, mathematical, translation or correction-validity adjudication.'}
 tsv(a.out/'HUNK_STATUS.tsv',list(statuses[0]),statuses)
 if candidates:tsv(a.out/'CANDIDATE_LINKS.tsv',list(candidates[0]),candidates)
 if history:tsv(a.out/'FR_CORRECTED_PAGE_HISTORY.tsv',list(history[0]),history);tsv(a.out/'FR_ONLY_OPERATION_HISTORY.tsv',list(history[0]),[r for r in history if r['no_identical_printed_operation']])
 tsv(a.out/'CURRENT_SOURCE_STATUS.tsv',list(source_status[0]),source_status)
 for name,value in [('INVENTORY.json',metadata),('NORMALIZATION_PROFILES.json',profile_doc),('HUNK_PAYLOADS.json',hobj),('HUNK_PROJECTIONS.json',projected),('CANDIDATE_DETAILS.json',details),('LEDGER_PAYLOADS.json',payloads)]:
  (a.out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (a.out/'LEDGER_PAYLOADS.md').write_text('# Exact ledger payloads linked from unmatched hunks\n\nThese are literal current-ledger fields, not verdicts. Row IDs are bound to the current ledger hash in INVENTORY.json.\n\n'+'\n'.join(md_payload(r) for r in payloads),encoding='utf-8')
 review=['# Unmatched French-layer hunk candidate review\n','The hunk orientation is corrected French → printed French. A ledger row normally records its own old → new operation, so each candidate explicitly states its direction. No match here confirms a correction, and a local edit fragment does not account for an entire hunk.\n']
 for h,status in zip(hunks,statuses):
  review += [f"## {h['hunk_id']}\n",f"File `{h['relative_file']}`; pages {', '.join(h['candidate_page_keys'])}. Snapshot source lines: corrected {h['fr_range']['line_start']}–{h['fr_range']['line_end']}; printed {h['fr_printed_range']['line_start']}–{h['fr_printed_range']['line_end']}.\n",f"Current exact payload occurrences: corrected {status['current_fr_hunk_payload_exact_count']}, printed {status['current_printed_hunk_payload_exact_count']}. A changed-file locator can have moved even when its payload survives.\n",f"Corrected payload SHA-256 `{h['old_sha256']}`; printed payload SHA-256 `{h['new_sha256']}`.\n",'### Snapshot corrected French\n','````tex\n'+h['old_text']+'\n````\n','### Snapshot printed French\n','````tex\n'+h['new_text']+'\n````\n','### Candidate ledger rows\n']
  hc=[x for x in candidates if x['hunk_id']==h['hunk_id']]
  unique={}
  for c in hc:unique.setdefault(c['row_id'],[]).append(c)
  if unique:
   for rid,cs in unique.items():
    r=byid[rid]
    review.append(f"- [{rid}](LEDGER_PAYLOADS.md#{rid.lower()}): {r['layer']}, {r['kind']}, ledger page {r['printed_page']}; profiles {', '.join(dict.fromkeys(c['profile'] for c in cs))}; methods {', '.join(dict.fromkeys(c['method'] for c in cs))}; directions {', '.join(dict.fromkeys(c['orientation'] for c in cs))}.\n")
  else:
   review.append('No paired candidate under the declared projections. The following corrected-French operations have no byte-identical old/new counterpart recorded in the printed layer on this page. They are listed in ledger append order, including later repairs and reversals; this is not a reconstructed net change.\n')
   for hr in history:
    if hr['hunk_id']==h['hunk_id'] and hr['no_identical_printed_operation']:
     review.append(f"- [{hr['row_id']}](LEDGER_PAYLOADS.md#{hr['row_id'].lower()}): {hr['kind']}; {hr['statement']}; appended after hunk snapshot: {hr['added_after_hunk_snapshot']}.\n")
  if status['profiles_collapsing_hunk_difference']:review.append('**Projection warning:** '+', '.join(status['profiles_collapsing_hunk_difference'])+' collapses this difference. This is not evidence that the original notations mean the same thing.\n')
 (a.out/'REVIEW.md').write_text('\n'.join(review),encoding='utf-8')
 readme=f'''# Supplementary candidate links for unmatched French hunks\n\nOriginal hunk snapshot: {hobj['snapshot']}. Current source/ledger capture: {capture_end}.\n\nThis report considers exactly the original 68 unmatched hunks, including 55 outside exposés 149 and 212. It uses the current correction ledger, preserving exact row payloads and hashes, and checks current source-file hashes and occurrence of the old hunk payloads. **No source or ledger was edited; no correction was adjudicated.**\n\n## Results\n\n- {metadata['hunks_with_paired_candidate']} hunks have at least one paired lexical candidate under the declared projections.\n- {metadata['hunks_without_paired_candidate']} have no pair; their same-page corrected-French operations are listed in ledger append order.\n- {len(candidates)} candidate links refer to {metadata['distinct_candidate_ledger_rows']} distinct ledger rows. Multiple profiles, directions and local edits can link the same row.\n- {len(payloads)} exact ledger payloads are included, only for these unmatched hunks and their fallback histories.\n\n## Normalization is a search aid\n\nP0 collapses ASCII whitespace. P1 additionally removes exact balanced `\\symup{{...}}` wrappers. P2 also removes `\\uline{{...}}`. P3 additionally looks through `\\underline{{...}}` and `\\uwave{{...}}`. No other wrapper, macro, alphabet, index, sign, word, punctuation or footnote is removed or substituted. Alphabet controls such as `\\mathcal`, `\\mathfrak`, `\\mathbf`, `\\mathrm` and `\\operatorname` remain literal and are checked unchanged by projection.\n\nUnderlines and upright letters can distinguish mathematical notation. Every removal is retained as field-level metadata with positions and argument hashes, and sensitive-decoration removals are flagged. A projection that collapses a hunk difference is reported explicitly, never treated as proof of equivalence.\n\nA full-payload pair means both projected ledger fields occur on opposite hunk sides with at least one distinguishing occurrence. A localized edit pair uses an actual differing block of the projected ledger operation, with up to 48 characters of matching adjacent context; both fragments must be at least eight characters. Such a fragment is only a candidate for part of the hunk, not evidence that its entire net difference is accounted for. Page mismatches and repeated occurrences remain visible.\n\n## History and direction\n\nThe hunk direction is corrected French to printed French. Ledger operation directions are reported separately as printed-to-corrected or corrected-to-printed. A reverse match can represent restoration or withdrawal and must not be mistaken for a surviving correction.\n\nFor hunks without a pair, `FR_CORRECTED_PAGE_HISTORY.tsv` retains all corrected-French rows for the exact file/page in ledger order. `FR_ONLY_OPERATION_HISTORY.tsv` selects rows with no byte-identical old/new counterpart in the printed layer on that page. This is a mechanical distinction, not a judgment about which operation changes meaning. The exact payload collection includes this latter set.\n\n## Snapshot limits\n\nThe original ledger had {len(old_rows)} rows; the captured current ledger has {len(rows)}. Original row hashes remain an unchanged prefix: {prefix_ok}. Current ledger SHA-256: `{metadata['current_ledger_sha256']}`. Original hunk-snapshot ledger SHA-256: `{metadata['hunk_snapshot_ledger_sha256']}`.\n\nRoot reported twelve editorial-footnote removals in corrected French 149 and 212 after the hunk snapshot. The report does not delete footnotes from hunk text or pretend the old hunks are current. `CURRENT_SOURCE_STATUS.tsv` and `HUNK_STATUS.tsv` show actual current hashes and exact-payload survival. The original hunk payload no longer occurs in current corrected French for {len(metadata['hunks_with_old_fr_payload_not_present_now'])} of the 68 hunks. All links still refer explicitly to the original 68 hunks. Regenerate the main layer diff for a final current net-difference accounting.\n\n## Review files\n\n- `REVIEW.md`: paired source payloads and links to candidate or fallback ledger rows.\n- `LEDGER_PAYLOADS.md` and `.json`: exact current-ledger old/new/evidence fields, row IDs, physical lines and hashes.\n- `CANDIDATE_LINKS.tsv`, `CANDIDATE_DETAILS.json`: candidate direction, profile, actual paired fragments and normalization metadata.\n- `HUNK_STATUS.tsv`, `HUNK_PAYLOADS.json`, `HUNK_PROJECTIONS.json`: original hunk identity and projected navigation views.\n- `FR_CORRECTED_PAGE_HISTORY.tsv`, `FR_ONLY_OPERATION_HISTORY.tsv`: append-order fallback history.\n- `CURRENT_SOURCE_STATUS.tsv`, `NORMALIZATION_PROFILES.json`, `INVENTORY.json`: input binding, declared rules and timing.\n'''
 (a.out/'README.md').write_text(readme,encoding='utf-8')
 print(json.dumps(metadata,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
