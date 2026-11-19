"""Lexical statement/event navigation. No source edits or substantive verdicts.

Inventories explicit TeX heading arguments and visible list-label syntax. Links
are only identifier/locator candidates; neither a match nor its absence decides
whether a statement was read, proved, corrected, or covered by another event.
"""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter, defaultdict
import argparse, bisect, csv, hashlib, io, json, re, unicodedata
from source_segments import CONTROL, group, mask_comments, markers, source_path, expected_units
from ledger_structure import sections

UNITS=['149','182','190','195','212','221','232','236','com','e149','e182','e190','e195','e212','e221','e232','e236']
NUMBER=r'\d+(?:\s*[.,]\s*\d+)*(?:\s+(?:bis|ter|quater))?'
NAMES={'proposition':['proposition','prop'], 'theorem':['theoreme','theorem','thm'],
       'lemma':['lemme','lemma','lem'], 'corollary':['corollaire','corollary','cor'],
       'remark':['remarque','remarques','remark','remarks','rem'],
       'definition':['definition','def'], 'example':['exemple','exemples','example','examples'],
       'scholium':['scholie','scholium'], 'conjecture':['conjecture'], 'criterion':['critere','criterion']}
ALL_NAMES='|'.join(sorted({x for a in NAMES.values() for x in a},key=len,reverse=True))
NAME_RE=re.compile(r'(?<![a-z])('+ALL_NAMES+r')(?![a-z])')
PAGE_HEAD=re.compile(r'^(e?(?:149|182|190|195|212|221|232|236)|com)-(\d+)$')

def utc():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def normalize(s):
    s=''.join(c for c in unicodedata.normalize('NFD',s.casefold()) if not unicodedata.combining(c))
    return re.sub(r'\s+',' ',s).strip()
def plain(s):
    # A transparent lexical projection, not TeX expansion.
    s=re.sub(r'\\[A-Za-z@]+\*?','',s)
    s=re.sub(r'[{}$]','',s)
    return normalize(s)
def number(s):
    m=re.search(NUMBER,plain(s))
    return re.sub(r'\s*[.,]\s*','.',m[0]).strip() if m else ''
def kind(s):
    m=NAME_RE.search(plain(s))
    return next((k for k,v in NAMES.items() if m and m[1] in v),'other')
def n_pattern(n):
    return re.escape(n).replace(r'\.',r'[.,]\s*').replace(r'\ ',r'\s*')
def token_pattern(n):
    return r'(?<![\w.])'+n_pattern(n)+r'(?![\w.]|\s*\d)'
def write_tsv(p,cols,rows):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=cols,delimiter='\t',lineterminator='\n',extrasaction='ignore');w.writeheader();w.writerows(rows)
def page_at(marks,off):
    prior=[x for x in marks if x['byte_start']<=off]
    return prior[-1]['page'] if prior else ''
def span_meta(data,start,end):
    line=data.count(b'\n',0,start)+1;ls=data.rfind(b'\n',0,start)+1
    return {'byte_start':start,'byte_end':end,'source_line':line,'source_end_line':data.count(b'\n',0,end)+1,
            'column_byte':start-ls+1,'column_character':len(data[ls:start].decode('utf-8'))+1}
def parse_macro(data,token,nargs,optional=False):
    at=token.end();opt=''
    if optional:
        q=group(data,at,91,93)
        if q:opt=q[2].decode('utf-8');at=q[1]
    values=[]
    for _ in range(nargs):
        q=group(data,at)
        if not q:return None
        values.append(q[2].decode('utf-8'));at=q[1]
    return at,opt,values

def extract_file(data,layer,unit,rel):
    masked=mask_comments(data);marks=markers(data);out=[];aux=[];issues=[];covered=[]
    def emit(start,end,category,title,num='',typ='other',number_origin='',parent=''):
        label=number(num) if re.search(r'\d',num) else plain(num)
        if category in {'explicit_item_label','implicit_item_label','manual_list_label'}:
            label=label.strip('(). ')
        out.append(dict(layer=layer,unit=unit,file=rel,preceding_literal_page=page_at(marks,start),category=category,
                        statement_type=typ,identifier_raw=num,identifier_normalized=label,
                        identifier_origin=number_origin,heading_exact=data[start:end].decode('utf-8'),heading_projection=plain(title),
                        parent_candidate=parent,**span_meta(data,start,end)))
    for t in CONTROL.finditer(masked):
        cmd=t[1].decode('ascii',errors='replace')
        if cmd=='result':
            parsed=parse_macro(masked,t,2,True)
            if not parsed:issues.append(dict(file=rel,line=masked.count(b'\n',0,t.start())+1,issue='unparsed result macro'));continue
            end,opt,args=parsed;title,label=args;typ=kind(title);num=number(label);origin='second result argument'
            if not num:
                num=number(title);origin='number in first result argument' if num else 'no explicit numeric identifier'
            cat='named_numbered_statement' if typ!='other' and num else 'named_unnumbered_heading' if typ!='other' else 'other_result_heading'
            emit(t.start(),end,cat,title,label if number(label) else num,typ,origin);covered.append((t.start(),end))
        elif cmd=='fsection':
            parsed=parse_macro(masked,t,2)
            if parsed:
                end,opt,args=parsed
                emit(t.start(),end,'section_heading',args[1],number(args[0]),'other','fsection first argument');covered.append((t.start(),end))
        elif cmd in {'section','subsection','subsubsection','paragraph','subparagraph'}:
            at=t.end()
            if masked[at:at+1]==b'*':at+=1
            q=group(masked,at,91,93)
            if q:at=q[1]
            q=group(masked,at)
            if not q:continue
            title=q[2].decode();p=plain(title);num=number(title) if re.match(r'^\d',p) else ''
            typ=kind(title);cat='remark_group_heading' if re.match(r'^remarques?\b',p) else 'section_heading'
            emit(t.start(),q[1],cat,title,num,typ,'section title' if num else 'no explicit numeric identifier');covered.append((t.start(),q[1]))
        elif cmd in {'tag','label','sid'}:
            parsed=parse_macro(masked,t,1)
            if parsed:
                end,opt,args=parsed
                aux.append(dict(layer=layer,unit=unit,file=rel,preceding_literal_page=page_at(marks,t.start()),macro=cmd,literal_identifier=args[0],**span_meta(data,t.start(),end)))
    # Manual named headings, erratum locators, and explicit list labels.
    offset=0;previous_blank=True
    for raw in masked.splitlines(keepends=True):
        stripped=raw.lstrip();start=offset+len(raw)-len(stripped);end=offset+len(raw.rstrip(b'\r\n'))
        s=stripped.decode('utf-8').rstrip('\r\n');p=plain(s)
        inside=any(a<=start<b for a,b in covered)
        if not inside and s:
            named=re.match(r'^(?:[a-z]\.\s*)?('+ALL_NAMES+r')\s+('+NUMBER+r')\b',p)
            if named:
                explicit=bool(re.match(r'^(?:\\par\s*)*\\(?:noindent|uline|textnormal|textbf|textit|emph|normalfont)\b',s))
                category='named_numbered_statement' if explicit else 'line_start_named_reference_candidate'
                emit(start,end,category,s,named[2],kind(named[1]),'formatted manual heading' if explicit else 'unformatted line-start keyword; heading not asserted');covered.append((start,end))
            elif 'BIBLIOGRAPHIE' in s and not s.startswith(r'\addcontentsline'):
                emit(start,end,'bibliography_heading',s);covered.append((start,end))
            elif re.match(r'^\d+\.\d+\.\s*[-–]',p):
                num=re.match(r'^(\d+\.\d+)',p)[1]
                emit(start,end,'numbered_paragraph_candidate',s,num,'numbered_paragraph','standalone decimal label and dash');covered.append((start,end))
            elif unit.startswith('e') and re.match(r'^(?:page\s+\d|ligne\s+\d|remarque sur la page\s+\d)',p):
                # Include a multiline heading up to its first short-dash
                # separator within this paragraph. No body interpretation.
                tail=masked[start:];blank=re.search(rb'\r?\n[ \t]*\r?\n',tail)
                limit=blank.start() if blank else min(len(tail),1200)
                rawseg=data[start:start+limit];sep=re.search(rb'\s+(?:---|--)??-\s+',rawseg)
                h_end=start+sep.start() if sep else end
                target=re.match(r'^(page|ligne|remarque sur la page)\s+(\d+)',p)
                emit(start,h_end,'erratum_locator',data[start:h_end].decode(),target[1]+' '+target[2],'erratum_locator','literal target locator');covered.append((start,h_end))
        # Explicit item labels are kept separately; proof conditions and
        # bibliography entries are not asserted to be independent statements.
        if not inside:
            item=re.match(r'^\\item\b',s)
            if item:
                q=group(stripped,item.end(),91,93)
                if q:
                    label=q[2].decode();h_end=start+q[1];cat='explicit_item_label'
                else:
                    label='';h_end=start+item.end();cat='implicit_item_label'
                emit(start,h_end,cat,label,label,'list_item','explicit item argument' if label else 'implicit counter not expanded')
            elif not any(a<=start<b for a,b in covered):
                # Projection begins after transparent noindent/font commands.
                label=re.match(r'^(\([ivxlcdm]+\)|[ivxlcdm]+[.)]|\(?\d+(?:[.,]\d+)*\)?[.)]|\d+(?:o|e|°)\b|[a-z][.)])(?:\s|$)',p)
                raw_prefix=re.sub(r'^\\noindent\s*','',s)
                structural_start=s.startswith(r'\noindent') or previous_blank or bool(re.match(r'^(?:\d|\([ivxlcdm]+\))',p))
                if label and structural_start and not raw_prefix.startswith('$'):
                    emit(start,end,'manual_list_label',s,label[1],'list_item','line-start literal label')
        previous_blank=not s;offset+=len(raw)
    out.sort(key=lambda r:(r['byte_start'],r['byte_end'],r['category']))
    prev=None
    for row in out:
        if row['category'] in {'explicit_item_label','implicit_item_label','manual_list_label'}:
            if prev:
                row['parent_candidate']=str(prev['byte_start'])
                row['parent_heading_projection']=prev['heading_projection']
                if re.fullmatch(r'\[\d+\]',plain(row['identifier_raw'])):row['category']='bracketed_numeric_item'
                elif prev['category']=='bibliography_heading':row['category']='bibliography_item_candidate'
                elif prev['statement_type']=='remark':row['category']='remark_member_candidate';row['statement_type']='remark'
                elif unit.startswith('e') and re.fullmatch(r'\([ivxlcdm]+\)',plain(row['identifier_raw'])):row['category']='erratum_roman_claim_candidate'
            else:row['parent_heading_projection']=''
        elif row['category']=='line_start_named_reference_candidate':
            row['parent_heading_projection']=''
        else:
            row['parent_heading_projection']='';prev=row
    return out,aux,issues

def event_rows(blob):
    reader=csv.DictReader(io.StringIO(blob.decode('utf-8'),newline=''),delimiter='\t');out=[];last=1
    for i,r in enumerate(reader,1):
        out.append(dict(event_row=f'E{i:06d}',data_row=i,physical_start=last+1,physical_end=reader.line_num,**r));last=reader.line_num
    return out

def event_units(row):
    units=[];m=re.match(r'^(e?(?:149|182|190|195|212|221|232|236)|com)(?=-|$)',row['id'])
    if m:units.append(m[1])
    loc=normalize(row['where'])
    for m in re.finditer(r'errat(?:um|a)\s+(149|182|190|195|212|221|232|236)\b',loc):units.append('e'+m[1])
    for m in re.finditer(r'expose\s+(149|182|190|195|212|221|232|236)\b',loc):units.append(m[1])
    if not units:
        m=re.match(r'(e?(?:149|182|190|195|212|221|232|236)|com)(?:\b|[,-])',loc)
        if m:units.append(m[1])
    return list(dict.fromkeys(units))
def event_pages(row):
    loc=normalize(row['where']);nums=[]
    for m in re.finditer(r'(?<![a-z])(?:pp?\.|printed page|page)\s*(\d+)(?:\s*[-–]\s*(\d+))?',loc):
        a=int(m[1]);b=int(m[2]) if m[2] else a
        nums.extend(str(x) for x in range(a,b+1) if b-a<40)
    return list(dict.fromkeys(nums))
def matching_features(heading,event):
    num=heading['identifier_normalized'];typ=heading['statement_type'];features=[]
    fields={k:normalize(event[k]) for k in ('id','where','result')}
    if heading['category']=='erratum_locator':
        raw=heading['identifier_raw'];loc=normalize(raw)
        for field in ('where','result'):
            if re.search(r'(?<![a-z0-9])'+re.escape(loc)+r'(?!\d)',fields[field]):features.append(field+':literal-erratum-target')
        return features
    if num:
        if re.search(token_pattern(num),fields['id']):features.append('id:identifier-token')
        aliases=NAMES.get(typ,[])+({'theorem':['th'],'example':['ex'],'scholium':['schol']}.get(typ,[]))
        if aliases and any(re.search(r'(?<![a-z])'+re.escape(alias)+r'-?'+n_pattern(num)+r'(?![\w.]|\s*\d)',fields['id']) for alias in aliases):
            features.append('id:typed-identifier-token')
        for field in ('where','result'):
            if re.search(token_pattern(num),fields[field]):
                aliases=NAMES.get(typ,[])
                for name in aliases:
                    if re.search(r'(?<![a-z])'+re.escape(name)+r'\s*[:.]?\s*\(?'+n_pattern(num)+r'(?![\w.]|\s*\d)',fields[field]):
                        features.append(field+':named-identifier');break
                if heading['category']=='erratum_roman_claim_candidate' and re.search(r'\('+re.escape(num.strip('().'))+r'\)',fields[field]):features.append(field+':roman-claim-label')
    elif typ in NAMES:
        if any(re.search(r'(?<![a-z])'+x+r'(?![a-z])',fields['where']) for x in NAMES[typ]):features.append('where:unnumbered-name-only')
    return features

def record_matches(heading,sec):
    num=heading['identifier_normalized'];typ=heading['statement_type'];hits=[]
    if not num:return hits
    for n,raw in enumerate(sec['body'].decode('utf-8').splitlines(),sec['line']+1):
        s=normalize(raw);features=[]
        if heading['category']=='erratum_locator':
            if normalize(heading['identifier_raw']) in s:features.append('literal-erratum-target')
        else:
            if re.search(token_pattern(num),s):
                for name in NAMES.get(typ,[]):
                    if re.search(r'(?<![a-z])'+name+r'\s*[:.]?\s*\(?'+n_pattern(num)+r'(?![\w.]|\s*\d)',s):features.append('named-identifier');break
                exact_id=heading['unit']+'-'+num
                if exact_id in s:features.append('unit-identifier-token')
                if heading['category']=='erratum_roman_claim_candidate' and '('+num.strip('().')+')' in s:features.append('roman-claim-label')
        if features:hits.append(dict(record_line=n,features=';'.join(features),line_exact=raw))
    return hits

def run():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,default=Path('FGA_CHECK'));ap.add_argument('--out',type=Path,required=True);ap.add_argument('--frozen',type=Path,required=True);a=ap.parse_args()
    if a.out.exists() or a.frozen.exists():raise FileExistsError('Use new output and frozen-input directories.')
    for p in (a.out,a.frozen):
        if p.resolve().is_relative_to((a.work/'sources').resolve()):raise ValueError('Output must not be in source trees.')
    started=utc();rels=['CHECK_EVENTS.tsv','CHECK_RECORD.md']
    rels += [p.relative_to(a.work).as_posix() for layer in ['fr','fr_printed'] for p in sorted((a.work/'sources'/layer).rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
    captured=None
    for attempt in range(1,6):
        first={r:(a.work/r).read_bytes() for r in rels};second={r:(a.work/r).read_bytes() for r in rels}
        if first==second:captured=first;break
    if captured is None:raise RuntimeError('Could not capture stable inputs after five immediate attempts.')
    capture_end=utc();a.frozen.mkdir(parents=True);a.out.mkdir(parents=True)
    for rel,data in captured.items():
        p=a.frozen/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    manifest=[dict(file=r,bytes=len(b),sha256=sha(b),role='record' if r in {'CHECK_EVENTS.tsv','CHECK_RECORD.md'} else 'French source tree') for r,b in captured.items()]
    headings=[];aux=[];parser_issues=[]
    for layer in ['fr','fr_printed']:
        for unit in UNITS:
            rel='sources/'+layer+'/'+source_path(layer,unit);rows,refs,issues=extract_file(captured[rel],layer,unit,rel)
            headings.extend(rows);aux.extend(refs);parser_issues.extend(issues)
    headings.sort(key=lambda r:(r['layer'],UNITS.index(r['unit']),r['byte_start'],r['byte_end'],r['category']))
    for i,h in enumerate(headings,1):h['heading_id']=f'H{i:05d}'
    byoffset={(h['file'],h['byte_start']):h['heading_id'] for h in headings}
    for h in headings:
        if h['parent_candidate']:h['parent_candidate']=byoffset.get((h['file'],int(h['parent_candidate'])),'')
    events=event_rows(captured['CHECK_EVENTS.tsv']);event_index={e['event_row']:e for e in events};event_info=[]
    for e in events:
        e['_units']=event_units(e);e['_pages']=event_pages(e)
        event_info.append({**{k:v for k,v in e.items() if not k.startswith('_')},'literal_units':','.join(e['_units']),'literal_pages':','.join(e['_pages'])})
    recsecs=sections(captured['CHECK_RECORD.md']);pagesecs=defaultdict(list)
    for sec in recsecs:
        m=PAGE_HEAD.match(sec['heading'])
        if m:pagesecs[m[1],m[2]].append(sec)
    corecats={'named_numbered_statement','named_unnumbered_heading','remark_group_heading','remark_member_candidate','erratum_locator','erratum_roman_claim_candidate','numbered_paragraph_candidate'}
    event_candidates=[];record_candidates=[];coverage=[];used_events=set()
    for h in headings:
        if h['category'] not in corecats:continue
        candidates=[]
        for e in events:
            if h['unit'] not in e['_units']:continue
            same_page=h['preceding_literal_page'] in e['_pages'] if e['_pages'] and h['preceding_literal_page'] else None
            features=matching_features(h,e)
            if features or same_page:
                row=dict(heading_id=h['heading_id'],layer=h['layer'],unit=h['unit'],source_file=h['file'],source_line=h['source_line'],source_page=h['preceding_literal_page'],event_row=e['event_row'],event_id=e['id'],event_physical_start=e['physical_start'],event_physical_end=e['physical_end'],identifier_features=';'.join(features),page_relation='same literal page' if same_page else 'different literal page' if same_page is False else 'page not extracted',event_where=e['where'],match_scope='identifier candidate' if features else 'page-only context')
                event_candidates.append(row);candidates.append(row)
                if features:used_events.add(e['event_row'])
        secs=pagesecs[h['unit'],h['preceding_literal_page']];recordcount=0
        for sec in secs:
            hits=record_matches(h,sec)
            if hits:
                for hit in hits:
                    record_candidates.append(dict(heading_id=h['heading_id'],layer=h['layer'],unit=h['unit'],source_page=h['preceding_literal_page'],record_section_line=sec['line'],record_section_heading=sec['heading'],match_scope='identifier candidate',**hit));recordcount+=1
            else:record_candidates.append(dict(heading_id=h['heading_id'],layer=h['layer'],unit=h['unit'],source_page=h['preceding_literal_page'],record_section_line=sec['line'],record_section_heading=sec['heading'],match_scope='page-section context only',record_line=sec['line'],features='',line_exact=sec['heading']))
        specific=[x for x in candidates if x['identifier_features']];same=[x for x in specific if x['page_relation']=='same literal page'];other=[x for x in specific if x['page_relation']=='different literal page']
        coverage.append(dict(heading_id=h['heading_id'],layer=h['layer'],unit=h['unit'],file=h['file'],source_line=h['source_line'],preceding_literal_page=h['preceding_literal_page'],category=h['category'],statement_type=h['statement_type'],identifier=h['identifier_normalized'],heading_exact=h['heading_exact'],identifier_event_candidates=len(specific),same_page_identifier_candidates=len(same),different_page_identifier_candidates=len(other),page_only_event_candidates=sum(not x['identifier_features'] for x in candidates),event_ids=';'.join(dict.fromkeys(x['event_id'] for x in specific)),page_record_sections=len(secs),record_identifier_lines=recordcount,candidate_status='no identifier candidate' if not specific else 'one identifier candidate' if len(specific)==1 else 'multiple identifier candidates',non_verdict='Lexical navigation only; no proof or reading conclusion.'))
    groups=defaultdict(list)
    for h in headings:
        if h['identifier_normalized'] and h['category'] in corecats:groups[h['layer'],h['unit'],h['identifier_normalized']].append(h)
    collisions=[]
    for (layer,unit,num),members in groups.items():
        if len(members)>1:collisions.append(dict(layer=layer,unit=unit,identifier=num,heading_ids=';'.join(x['heading_id'] for x in members),types=';'.join(x['statement_type'] for x in members),source_lines=';'.join(str(x['source_line']) for x in members),pages=';'.join(x['preceding_literal_page'] for x in members),scope='Repeated lexical number across headings; not asserted to be an error.'))
    orphan_events=[{k:v for k,v in e.items() if not k.startswith('_')} for e in events if e['event_row'] not in used_events]
    missing=[r for r in coverage if not r['identifier_event_candidates']]
    ambiguous=[r for r in coverage if r['identifier_event_candidates']>1 or r['different_page_identifier_candidates']]
    hcols=['heading_id','layer','unit','file','preceding_literal_page','category','statement_type','identifier_raw','identifier_normalized','identifier_origin','heading_exact','heading_projection','parent_candidate','parent_heading_projection','byte_start','byte_end','source_line','source_end_line','column_byte','column_character']
    write_tsv(a.out/'SOURCE_HEADINGS.tsv',hcols,headings)
    write_tsv(a.out/'AUXILIARY_IDENTIFIERS.tsv',['layer','unit','file','preceding_literal_page','macro','literal_identifier','byte_start','byte_end','source_line','source_end_line','column_byte','column_character'],aux)
    write_tsv(a.out/'SOURCE_HASHES.tsv',list(manifest[0]),manifest)
    write_tsv(a.out/'EVENT_LOCATORS.tsv',list(event_info[0]),event_info)
    write_tsv(a.out/'EVENT_CANDIDATES.tsv',list(event_candidates[0]),event_candidates)
    write_tsv(a.out/'RECORD_CANDIDATES.tsv',list(record_candidates[0]),record_candidates)
    for filename,rows in [('CANDIDATE_COVERAGE.tsv',coverage),('NO_IDENTIFIER_CANDIDATE.tsv',missing),('AMBIGUOUS_OR_DIFFERENT_PAGE.tsv',ambiguous)]:write_tsv(a.out/filename,list(coverage[0]),rows)
    write_tsv(a.out/'REPEATED_SOURCE_NUMBERS.tsv',['layer','unit','identifier','heading_ids','types','source_lines','pages','scope'],collisions)
    write_tsv(a.out/'EVENTS_WITHOUT_HEADING_IDENTIFIER_CANDIDATE.tsv',[k for k in events[0] if not k.startswith('_')],orphan_events)
    write_tsv(a.out/'PARSER_ISSUES.tsv',['file','line','issue'],parser_issues)
    after={r:sha((a.work/r).read_bytes()) for r in rels};changed=[r for r in rels if after[r]!=sha(captured[r])]
    metadata=dict(started_utc=started,captured_utc=capture_end,completed_utc=utc(),stable_capture_attempt=attempt,source_tree_files=len(rels)-2,frozen_input_files=len(rels),unit_files=34,source_heading_rows=len(headings),heading_categories=dict(Counter(h['category'] for h in headings)),core_candidate_headings=len(coverage),numbered_named_headings=sum(h['category']=='named_numbered_statement' for h in headings),event_rows=len(events),record_page_sections=sum(map(len,pagesecs.values())),event_candidate_rows=len(event_candidates),record_candidate_rows=len(record_candidates),no_identifier_event_candidate=len(missing),ambiguous_or_different_page=len(ambiguous),events_without_heading_identifier_candidate=len(orphan_events),repeated_number_groups=len(collisions),parser_issues=len(parser_issues),live_inputs_changed_since_capture=changed,source_edits_by_inventory=0,scope='Frozen lexical heading/event/record candidate navigation; not proof, translation, scan or reading coverage.')
    (a.out/'INVENTORY.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    perlayer=[]
    for layer in ['fr','fr_printed']:
        for unit in UNITS:
            hs=[h for h in headings if h['layer']==layer and h['unit']==unit];cs=[r for r in coverage if r['layer']==layer and r['unit']==unit]
            perlayer.append(dict(layer=layer,unit=unit,all_heading_rows=len(hs),named_numbered=sum(h['category']=='named_numbered_statement' for h in hs),core_candidates=len(cs),no_identifier_candidate=sum(not r['identifier_event_candidates'] for r in cs),multiple_identifier_candidates=sum(r['identifier_event_candidates']>1 for r in cs),record_page_context_missing=sum(not r['page_record_sections'] for r in cs)))
    write_tsv(a.out/'UNIT_SUMMARY.tsv',list(perlayer[0]),perlayer)
    report=f'''# Statement and event candidate coverage\n\nCaptured {capture_end}; completed {metadata['completed_utc']}. The source snapshot includes both French layers, all eight exposés, the Commentaires and all eight errata. Records were captured in the same stable two-read interval. No source or main-record file was edited.\n\n## Scope\n\nThis is a lexical navigator, **not a certificate of reading, proof, mathematical validity or correction coverage**. A missing identifier match can reflect another name, an unnumbered assertion, a grouped event, a continuation on another page, or parser limitations. A match can be a cross-reference to a different statement. All links require the root reader's inspection.\n\nThe parser records literal `\\result` arguments, including optional separator arguments, numbered identifiers in a first argument, section headings, manual line-start named headings, erratum page/line locators, explicit list labels and implicit list markers. It retains both numbered and unnumbered named headings. A list member is only associated with the nearest preceding lexical heading; this is not a decision that it is an independent statement or part of that heading's mathematics. Section and other list labels remain in `SOURCE_HEADINGS.tsv` but are outside the main named-heading candidate coverage table.\n\nThe exact heading bytes, file, line, byte range and nearest preceding literal page marker are retained. Plain projections remove TeX control words and braces only for navigation; they do not expand TeX. Equation tags and literal labels/anchors are separate in `AUXILIARY_IDENTIFIERS.tsv` and are not counted as named statements. Implicit list counters are not expanded.\n\n## Snapshot totals\n\n- {len(headings)} source heading/list rows across both layers, including {metadata['numbered_named_headings']} named numbered headings.\n- {len(coverage)} named-heading, remark-member or erratum candidate entries.\n- {len(events)} captured check-event rows; {metadata['record_page_sections']} page sections in the check record.\n- {len(event_candidates)} event candidate links and {len(record_candidates)} record candidate links.\n- {len(missing)} entries have no identifier event candidate; {len(ambiguous)} have multiple candidates or a different-page identifier match. These are navigation flags only.\n- {len(orphan_events)} event rows have no named-heading identifier candidate; events concerning formulas, general claims, typography or cross-work links naturally need not match a named heading.\n- {len(collisions)} repeated source-number groups, counted separately by layer and unit. Reused numbers across theorem types, remark members and erratum locators are not automatically errors.\n- {len(parser_issues)} unresolved result-macro parse issues.\n\n## Candidate rules\n\nAn event is considered only when its ID or locator contains the same literal unit. Identifier candidates come from bounded identifier tokens in the event ID, a named identifier in `where` or `result` using an explicit French/English label-alias list, or an erratum target/roman-label match. The report separately records agreement, disagreement or absence of an extracted printed-page locator. Same-page links without identifier matches are labelled page-only context and do not count as identifier coverage. Repeated source identifiers and multiple events are retained rather than guessed apart.\n\nFor the check record, the exact page-section key supplies context. Within that section, named identifiers, unit-identifier tokens and explicit erratum targets are lexical candidate lines. A page section without such a line is reported only as page-section context. The absence of a named identifier in prose does not imply that the statement was not read.\n\n## Files\n\n- `SOURCE_HEADINGS.tsv`: every extracted heading and list label, with exact identifying text and offsets.\n- `AUXILIARY_IDENTIFIERS.tsv`: equation tags, labels and source anchors.\n- `CANDIDATE_COVERAGE.tsv`: the root reader's central candidate table.\n- `EVENT_CANDIDATES.tsv`, `RECORD_CANDIDATES.tsv`: every candidate link and its literal basis.\n- `NO_IDENTIFIER_CANDIDATE.tsv`, `AMBIGUOUS_OR_DIFFERENT_PAGE.tsv`: subsets for inspection, with no substantive verdict.\n- `REPEATED_SOURCE_NUMBERS.tsv`: source-number collision groups.\n- `EVENTS_WITHOUT_HEADING_IDENTIFIER_CANDIDATE.tsv`: event rows outside the named-heading match set.\n- `EVENT_LOCATORS.tsv`, `UNIT_SUMMARY.tsv`, `SOURCE_HASHES.tsv`, `PARSER_ISSUES.tsv`, `INVENTORY.json`: metadata, locators, integrity and parser diagnostics.\n\n## Reproduction and freshness\n\nRun `python3 -B FGA_CHECK/scripts/statement_event_coverage.py --work FGA_CHECK --out FGA_CHECK/statement_event_coverage/<new-snapshot> --frozen tmp/<new-frozen-inputs>`. Use new output names; the script never overwrites a snapshot. The full immutable input capture is held only in the temporary workspace; the deliverable records its hashes and exact extracted heading text.\n\nLive inputs changed after capture: {len(changed)}. This is expected if the root reading continues; the report remains tied to its captured hashes. Regenerate against final sources and records before using locators as current.\n'''
    (a.out/'README.md').write_text(report,encoding='utf-8')
    print(json.dumps(metadata,ensure_ascii=False,indent=2))
if __name__=='__main__':run()
