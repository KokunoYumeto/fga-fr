"""Literal terminology candidate inventory; never modifies edition sources.

The supplied decision record remains authoritative as data. This script does
not decide mathematical senses, translation accuracy, register, formula equality,
or whether a candidate should change. It emits exact byte/line locators for an
explicit finite list of literal strings. Searches retain case and whitespace.
"""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter, defaultdict
import argparse, bisect, csv, hashlib, json, re, unicodedata
from source_segments import CONFIG, UNITS, expected_units, source_path, markers

LANG_LAYERS = {'en':['en'], 'es':['es','es_149_printed'],
               'pt-BR':['pt-BR','pt-BR_printed'],
               'vi':['vi','vi_diplomatic'], 'ko':['ko'], 'zh-Hans':['zh-Hans']}
# A literal can be a word, stem or phrase. These are navigation candidates,
# including prescribed and alternative forms; none is an automatic replacement.
COMMON = {
 'limits': {
  'en':'inductive limit|direct limit|colimit|projective limit|inverse limit|inductive system|direct system|projective system|inverse system',
  'es':'límite inductivo|límite directo|colímite|límite proyectivo|límite inverso|límites inductivos|límites directos|límites proyectivos|límites inversos|sistema inductivo|sistema directo|sistema proyectivo|sistema inverso',
  'pt-BR':'limite indutivo|limite direto|colimite|limite projetivo|limite inverso|limites indutivos|limites diretos|limites projetivos|limites inversos|sistema indutivo|sistema direto|sistema projetivo|sistema inverso',
  'vi':'giới hạn quy nạp|giới hạn xạ ảnh|giới hạn trực tiếp|giới hạn ngược|đối giới hạn|hệ quy nạp|hệ xạ ảnh',
  'ko':'귀납극한|사영극한|여극한|쌍대극한|역극한|직접극한|귀납계|사영계',
  'zh-Hans':'归纳极限|逆极限|余极限|射影极限|正向极限|归纳系|逆系|正向系|射影系'},
 'stalk': {'en':'stalk|fiber|fibre','es':'tallo|fibra','pt-BR':'talo|fibra','vi':'thớ|mầm','ko':'줄기|섬유|올|파이버','zh-Hans':'茎|纤维'},
 'prescheme': {'en':'prescheme|pre-scheme','es':'preesquema|pre-esquema','pt-BR':'pré-esquema|preesquema|pré esquema','vi':'tiền lược đồ','ko':'준스킴','zh-Hans':'预概形'},
 'register': {'en':'one has|we have|we shall|we will|Let |let |resp.|cf.|it is necessary and sufficient',
  'es':'se tiene|se dice|tenemos|Sea |sea |vosotros|resp.|cf.|es necesario y suficiente',
  'pt-BR':'tem-se|diz-se|temos|nós|Seja |seja |resp.|cf.|é necessário e suficiente',
  'vi':' ta |Ta |chúng ta|chúng tôi|Giả sử|cần và đủ|resp.|cf.',
  'ko':'이다.|한다.|입니다|합니다|resp.|cf.',
  'zh-Hans':'我们|resp.|cf.'}}
SPEC = {
 1:{l:'prof|rg|long|deg.tr|Ker' for l in LANG_LAYERS},
 2:COMMON['limits'],3:COMMON['stalk'],4:COMMON['prescheme'],5:COMMON['register'],
 6:{'en':'fibre|fiber|neighbourhood|neighborhood|centre|center|behaviour|behavior|isation|ization|localise|localize|normalise|normalize|characterise|characterize|generalise|generalize|realise|realize|factorise|factorize|organise|organize'},
 7:{'en':'inductive limit|direct limit|colimit|inductive system|direct system'},
 8:{'en':'projective limit|inverse limit|projective system|inverse system'},
 9:{'en':'final object|terminal object'},
 10:{'en':'Noetherian|noetherian|Artinian|artinian|Abelian|abelian|Cartesian|cartesian|Henselian|henselian'},
 11:{'en':COMMON['stalk']['en']},12:{'en':'Scholium|scholium|scholie|Scholie|theorem-scholium'},
 13:{'en':'filtered|filtering|cofiltered|cofiltering|left filtered|pseudo-filtered'},
 14:{'en':'inverse image|pullback|pull-back|reciprocal image'},
 15:{'en':'basic localizer|aspheric|modelizer|homotopism|contrafunctor|squarable|group with loops|outer group|actual action|probably|sans doute|category of models|Quillen couple'},
 16:{'en':'prescheme|pre-scheme|radicial|immersion|embedding|étale|etale|resp.|quasi-compact|quasicompact|if and only if|iff'},
 17:{'es':'funtor|functor'},18:{'es':'entorno|vecindad'},
 19:{'es':'cuasicompact|cuasi-compact|cuasicoherente|cuasi-coherente|cuasifinit|cuasi-finit|cuasi '},
 20:{'es':'imagen inversa|imagen recíproca|imágenes inversas|imágenes recíprocas'},21:{'es':COMMON['limits']['es']},
 22:{'es':'tallo|fibra'},23:{'es':'cuerpo|campo'},
 24:{'es':'se tiene|se dice|tenemos|vosotros|si y solo si|si y sólo si|Sea |sea '},
 25:{'es':'esquema|preesquema|pre-esquema|haz|prehaz|gavilla|liso|lisa|suave|recubrimiento|sucesión exacta|sucesiones exactas|inmersión|plano|plana|planitud|espacio anillado|étale|etale'},
 26:{'pt-BR':'liso|lisa|suave|formalmente liso|formalmente lisa'},
 27:{'pt-BR':'planicidade|planitude|planura'},28:{'pt-BR':'cobertura|recobrimento'},
 29:{'pt-BR':'sequência exata|sequências exatas|sucessão exata|sucessões exatas'},
 30:{'pt-BR':COMMON['prescheme']['pt-BR']},
 31:{'pt-BR':'imagem inversa|imagem recíproca|imagens inversas|imagens recíprocas'},
 32:{'pt-BR':'quase-|quasi-|quase |quasi '},
 33:{'pt-BR':'-se|nós|temos|exacto|exacta|secção|secções|facto|projectivo|projectiva|ação|projetivo|projetiva'},
 34:{'pt-BR':'esquema|feixe|pré-feixe|pre-feixe|talo|fibra|limite indutivo|limite projetivo|limite direto|limite inverso|funtor|functor|espaço anelado|imersão|corpo|vizinhança|étale|etale'},
 35:{'vi':'iđêan|ideal|i-đê-an|iđêal'},36:{'vi':COMMON['limits']['vi']},
 37:{'vi':COMMON['register']['vi']},38:{'vi':'iđêan|môđun|ideal|module|mô-đun|mô đun'},
 39:{'vi':'lược đồ|tiền lược đồ|bó|tiền bó|hàm tử|cấu xạ|đồng cấu|môđun|phẳng|trơn|thớ|lân cận|không gian vành|trường|dãy khớp|sơ đồ|étale|etale'},
 48:{'zh-Hans':'赋环空间|环层空间|带环空间|环积空间|局部环层空间'},
 49:{'zh-Hans':'光滑|平滑|形式光滑|光滑态射'},
 50:{'zh-Hans':'固有|紧合|逆紧|固有态射|紧合态射'},
 51:{'zh-Hans':'归纳极限|逆极限|余极限|射影极限|正向极限'},
 52:{'zh-Hans':'叠|栈'},53:{'zh-Hans':'我们|，|。|；|：|（|）|、|,|.|;|:|(|)'},
 54:{'zh-Hans':'概形|概型|预概形|态射|预层|凝聚|拟凝聚|拟紧|平坦|平展|函子|纤维|茎|终对象|邻域|当且仅当'},
 55:{'ko':'섬유|섬유곱|의 올|올곱|파이버|올'},
 56:{'ko':'모듈라이|가군|모듈'},57:{'ko':COMMON['limits']['ko']},
 58:{'ko':'아이디얼|이데알|준콤팩트|준컴팩트|끝 대상|종대상|덮개|피복|피복 공간|피복공간'},
 59:{'ko':'준스킴|준층|준연접|준콤팩트'},
 60:{'ko':'이다.|한다.|입니다|합니다'},
 61:{'ko':'스킴|사상|함자|평탄|고유|근방|환 달린 공간|줄기|매끄러운|에탈'}
}


def utc():return datetime.now(timezone.utc).isoformat()
def digest(data):return hashlib.sha256(data).hexdigest()
def write_tsv(path,fields,rows):
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
def md(value):return str(value).replace('|','\\|').replace('\n',' ')
def literal_forms(term,lang):
    # Explicit case variants are searchable literals in their own right.
    yield term,'exact'
    if lang in {'en','es','pt-BR','vi'} and term and term[0].isalpha():
        for form,label in [(term[0].upper()+term[1:],'initial capital'),(term.upper(),'uppercase')]:
            if form!=term:yield form,label

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,default=Path('FGA_CHECK'))
    ap.add_argument('--decisions',type=Path,required=True);ap.add_argument('--standards',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();start=utc()
    decisions_bytes=a.decisions.read_bytes();standards_bytes=a.standards.read_bytes()
    rows=list(csv.DictReader(decisions_bytes.decode('utf-8').splitlines(),delimiter='\t'))
    assert len(rows)==67 and Counter(r['confidence'] for r in rows)=={'high':38,'medium':27,'low':2}
    a.out.mkdir(parents=True,exist_ok=True)
    frozen={};files=[]
    for lang,layers in LANG_LAYERS.items():
        for layer in layers:
            unit_map={source_path(layer,u):u for u in expected_units(layer)}
            for p in sorted((a.work/'sources'/layer).rglob('*.tex')):
                rel=p.relative_to(a.work).as_posix();data=p.read_bytes();text=data.decode('utf-8')
                sub=p.relative_to(a.work/'sources'/layer).as_posix();unit=unit_map.get(sub,'')
                markerlist=markers(data);newline=[i for i,b in enumerate(data) if b==10]
                frozen[rel]={'data':data,'text':text,'markers':markerlist,'newline':newline,'unit':unit,'language':lang,'layer':layer}
                files.append(dict(file=rel,language=lang,layer=layer,unit=unit,scope='unit' if unit else 'ancillary',bytes=len(data),sha256=digest(data),literal_markers=len(markerlist),unicode_nfc=(text==unicodedata.normalize('NFC',text))))
    # Every source is compared with its captured bytes before and after scanning.
    assert all((a.work/r).read_bytes()==v['data'] for r,v in frozen.items())
    capture_end=utc();literals=[];occ=[];counts=Counter();distinct_places=defaultdict(set)
    by_rule=defaultdict(list)
    for ordinal,row in enumerate(rows,1):
        rid=f'T{ordinal:03d}';spec=SPEC.get(ordinal,{})
        assert row['language'] in {'all',*LANG_LAYERS} or not spec
        for lang,termstring in spec.items():
            seen=set()
            for term in termstring.split('|'):
                for literal,variant in literal_forms(term,lang):
                    if literal in seen:continue
                    seen.add(literal);lid=f'{rid}-{lang}-{len(seen):03d}'
                    literals.append(dict(decision_id=rid,literal_id=lid,language=lang,literal=literal,listed_candidate=term,case_variant=variant,matcher='case-sensitive literal substring; overlaps retained',decision_confidence=row['confidence']))
                    b=literal.encode('utf-8')
                    for rel,v in frozen.items():
                        if v['language']!=lang:continue
                        data=v['data'];pos=0
                        while True:
                            pos=data.find(b,pos)
                            if pos<0:break
                            line=bisect.bisect_left(v['newline'],pos)+1
                            line_start=v['newline'][line-2]+1 if line>1 else 0
                            line_end=v['newline'][line-1] if line<=len(v['newline']) else len(data)
                            prior=[m for m in v['markers'] if m['byte_start']<=pos]
                            page=prior[-1]['page'] if prior else ''
                            snippet=data[line_start:line_end].decode('utf-8').rstrip('\r')
                            entry=dict(decision_id=rid,literal_id=lid,language=lang,layer=v['layer'],file=rel,unit=v['unit'],preceding_literal_page=page,source_line=line,column_character=len(data[line_start:pos].decode('utf-8'))+1,column_byte=pos-line_start+1,byte_start=pos,byte_end=pos+len(b),matched_literal=literal,scope='unit' if v['unit'] else 'ancillary',source_line_text=snippet)
                            occ.append(entry);by_rule[ordinal].append(entry);counts[rid]+=1;distinct_places[rid].add((rel,pos,pos+len(b)));pos+=1
    unchanged=all((a.work/r).read_bytes()==v['data'] for r,v in frozen.items())
    assert unchanged,'Translation source changed during inventory; rerun against a stable snapshot.'
    occ.sort(key=lambda r:(r['decision_id'],r['file'],r['byte_start'],r['byte_end'],r['literal_id']))
    fieldnames=list(rows[0]);inventory=[]
    for ordinal,row in enumerate(rows,1):
        rid=f'T{ordinal:03d}';lang=row['language'];applicable=lang=='all' or lang in LANG_LAYERS
        scope_langs=list(LANG_LAYERS) if lang=='all' else [lang] if applicable else []
        policy='excluded: low-confidence decision is not to be applied' if row['confidence']=='low' else 'pending root reading; not applied by inventory' if applicable else 'outside the six FGA translations'
        inventory.append(dict(decision_id=rid,input_record=ordinal,input_line=ordinal+1,applicable=applicable,applicable_languages=','.join(scope_langs),application_status=policy,literal_candidates=sum(x['decision_id']==rid for x in literals),literal_occurrences=counts[rid],distinct_literal_spans=len(distinct_places[rid]),**row))
    write_tsv(a.out/'DECISION_INVENTORY.tsv',list(inventory[0]),inventory)
    write_tsv(a.out/'SEARCH_LITERALS.tsv',list(literals[0]),literals)
    write_tsv(a.out/'LITERAL_OCCURRENCES.tsv',list(occ[0]),occ)
    write_tsv(a.out/'SOURCE_HASHES.tsv',list(files[0]),files)
    low=[r for r in inventory if r['confidence']=='low'];low_ids={r['decision_id'] for r in low}
    low_occ=[r for r in occ if r['decision_id'] in low_ids]
    write_tsv(a.out/'LOW_CONFIDENCE_OCCURRENCES.tsv',list(occ[0]),low_occ)
    applicable=[r for r in inventory if r['applicable']]
    info={'started_utc':start,'capture_completed_utc':capture_end,'completed_utc':utc(),'input_decisions_sha256':digest(decisions_bytes),'input_standards_sha256':digest(standards_bytes),'decision_rows':len(rows),'input_confidence_counts':dict(Counter(r['confidence'] for r in rows)),'applicable_decisions':len(applicable),'applicable_confidence_counts':dict(Counter(r['confidence'] for r in applicable)),'out_of_scope_decisions':[r['decision_id'] for r in inventory if not r['applicable']],'translation_files':len(files),'unit_files':sum(r['scope']=='unit' for r in files),'ancillary_files':sum(r['scope']=='ancillary' for r in files),'literal_candidates':len(literals),'literal_occurrences':len(occ),'sources_unchanged':unchanged,'low_confidence_occurrences':dict(Counter(r['decision_id'] for r in low_occ)),'nfc_diagnostics':[r['file'] for r in files if r['language']=='vi' and not r['unicode_nfc']],'non_adjudication':'No edition text changed. Literal substrings are navigation aids, not decisions; duplicates and irrelevant senses are retained.'}
    (a.out/'INVENTORY.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
    chunks=['# Low-confidence terminology decisions\n',f'Literal inventory captured {capture_end}. The two supplied decisions below are reproduced field for field. **Neither decision is applied.** The entries are lexical candidate locations, not decisions about mathematical meaning.\n',
            'All supplied `.tex` files in the two relevant language trees were searched with the explicit literals listed below. Every occurrence of those literal strings is included, including overlapping strings, compounds and nonmathematical uses. In particular, an isolated search for Korean `올` can match verbs; these are deliberately retained as false-positive candidates for the root reader. No translation text was changed.\n',
            'Locators use source lines and byte offsets in the captured files. The printed-page field is the nearest preceding literal source marker, not a reading of the scan; missing or misplaced markers can affect it. Hashes are in the companion `SOURCE_HASHES.tsv`. Subsequent source edits require regeneration.\n']
    for entry in low:
        rid=entry['decision_id'];original=rows[entry['input_record']-1];selected=[r for r in low_occ if r['decision_id']==rid]
        chunks += [f"## {rid}: {original['language']} — {original['concept']}\n",f"Input record {entry['input_record']}, TSV line {entry['input_line']}.\n"]
        for field in fieldnames:chunks.append(f'**{field}:** {original[field]}\n')
        literal_set=[x['literal'] for x in literals if x['decision_id']==rid]
        chunks.append('### Exhaustive literal candidate search\n')
        chunks.append('Search strings: '+', '.join('`'+x+'`' for x in literal_set)+'.\n')
        termcounts=Counter(r['matched_literal'] for r in selected)
        chunks += ['| Literal | Raw occurrences |\n| --- | ---: |\n'+'\n'.join(f'| {md(t)} | {termcounts[t]} |' for t in literal_set)+'\n',
                   f'Raw literal matches: {len(selected)}. Different exact byte spans: {len(set((r["file"],r["byte_start"],r["byte_end"]) for r in selected))}. Overlapping shorter and longer terms remain separate.\n',
                   '| File | Unit / preceding page marker | Source line | Column | Byte span | Matched literal | Context |\n| --- | --- | ---: | ---: | --- | --- | --- |\n']
        table_rows=[]
        for r in selected:
            loc=(r['unit']+'-'+r['preceding_literal_page']) if r['unit'] and r['preceding_literal_page'] else 'ancillary / no preceding marker'
            table_rows.append(f"| {r['file']} | {loc} | {r['source_line']} | {r['column_character']} | {r['byte_start']}–{r['byte_end']} | {md(r['matched_literal'])} | {md(r['source_line_text'])} |")
        chunks[-1]=chunks[-1]+'\n'.join(table_rows)+'\n'
    (a.work/'TERMINOLOGY_LOW_CONFIDENCE.md').write_text('\n'.join(chunks),encoding='utf-8')
    report=['# Mechanical terminology inventory\n',f"Captured {capture_end}; completed {info['completed_utc']}.\n",'No translation or French source was edited. This inventory does not count as a paragraph reading, terminology application, mathematical check, or correction-row verdict.\n',
    '## Decision scope\n',
    '| Scope | Decisions | High | Medium | Low |\n| --- | ---: | ---: | ---: | ---: |\n| Entire supplied record | 67 | 38 | 27 | 2 |\n| Six FGA translations, including all-language rules | 53 | 31 | 20 | 2 |\n| Other language/work scopes | 14 | 7 | 7 | 0 |\n',
    'Thus **51 high/medium decisions and 2 excluded low-confidence decisions** fall within the six translation scopes. The earlier count of 65 high/medium decisions describes the whole input table; it is not the count applicable to these translations. No application is inferred from these counts.\n',
    'The five records T001–T005 explicitly have `language=all`, so their literal scope includes English, Spanish, Brazilian Portuguese, Vietnamese, Korean and Simplified Chinese. Their original decisions are retained without rewriting in `DECISION_INVENTORY.tsv`.\n',
    'The 14 out-of-scope records are T040–T047 (Japanese), T062–T064 (French for translation of other works) and T065–T067 (German). They are retained in the inventory with empty candidate searches rather than silently discarded.\n',
    '## Search coverage and limits\n',
    f"Searched {len(files)} current translation `.tex` files: {info['unit_files']} exposé/Commentaires/erratum files and {info['ancillary_files']} ancillary files. Applied {len(literals)} explicitly enumerated, case-sensitive literal strings and recorded {len(occ)} matches. All captured source bytes were rechecked unchanged after searching.\n",
    'The input counts concern other works and are copied only as provenance, never treated as FGA counts. Each FGA count in this inventory comes from this snapshot. Literal searches preserve whitespace and do not expand TeX. Phrases split by line breaks or commands can be missed. Stems can match larger words; overlapping shorter and longer literals are retained. These are candidate counts, not correction counts.\n',
    'Rules about all formulas, register, meaning, punctuation outside mathematics, Unicode normalization and formula/character spacing cannot be verified by a finite literal vocabulary. The root reader must examine every paragraph and formula. T001 lists operator-name candidates only; it is not a substitute for the separate mathematical-expression navigator or the scan. T053 includes punctuation candidates both inside and outside formulas without deciding their function.\n',
    'The two low decisions are reproduced exactly in `TERMINOLOGY_LOW_CONFIDENCE.md`, with the complete lexical candidate tables. No low-confidence choice was applied. Korean `올` produces intentionally broad matches; Chinese absent candidate spellings remain visible with zero counts.\n',
    '## Files\n',
    '- `DECISION_INVENTORY.tsv`: all 67 original record rows, applicability and candidate counts.\n- `SEARCH_LITERALS.tsv`: every search string and its explicit case variant.\n- `LITERAL_OCCURRENCES.tsv`: every match, original line text, byte span, line/column and preceding literal page marker.\n- `LOW_CONFIDENCE_OCCURRENCES.tsv`: exact subset for T051 and T055.\n- `SOURCE_HASHES.tsv`: file scope, sizes, SHA-256 and NFC diagnostics.\n- `INVENTORY.json`: timing, input hashes and totals.\n',
    'Reproduce from the deliverable parent directory with `python3 -B FGA_CHECK/scripts/terminology_inventory.py --work FGA_CHECK --decisions <supplied-decisions.tsv> --standards <supplied-standards.md> --out FGA_CHECK/terminology_inventory/<new-snapshot-name>`. Input files are not copied into the deliverable.\n']
    (a.out/'README.md').write_text('\n'.join(report),encoding='utf-8')
    # Exact source locators in the snapshot are distinct from evolving root text.
    print(json.dumps(info,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
