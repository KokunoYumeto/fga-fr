"""Explicitly approved page-local translation edits, with one row per range.

The caller supplies every math-span pairing after reading the prose and scan.
Equal counts or lexical similarity are never treated as reader approval.
"""
import csv, hashlib, re
from audit_utils import ROOT, FIELDS, read, write, page_text, utc
from translation_math_lexer import scan_math, NONMATH_ENVIRONMENTS

NAMES={'en':'English','es':'Spanish','es_149_printed':'Spanish as printed',
 'pt-BR':'Brazilian Portuguese','pt-BR_printed':'Brazilian Portuguese as printed',
 'vi':'Vietnamese','vi_diplomatic':'Vietnamese as printed','ko':'Korean','zh-Hans':'Simplified Chinese'}

def math_ranges(text, page_fragment=False):
    data=text.encode('utf-8'); result=scan_math(data)
    issues=result['issues']
    if page_fragment:
        # The complete file is checked by the callers before this exception.
        # A printed-page boundary may bisect a nonmath list environment.
        issues=[i for i in issues if not (
            i['code'] in {'unclosed_environment_at_end_of_file',
                          'unmatched_or_crossed_environment_end'}
            and i.get('environment') in NONMATH_ENVIRONMENTS)]
    if issues:
        raise ValueError(issues)
    return data,[s for s in result['spans'] if s['parent_span_index'] is None]

def page_math_ranges(rel,page):
    """Select complete page-contained spans from a strict whole-file parse.

    A printed break can bisect a prose group or list. It must not bisect a
    formula: such a range is rejected instead of being guessed or truncated.
    """
    whole=read(rel);data,spans=math_ranges(whole)
    marker=re.search(r'\\src\{'+str(page)+r'\}',whole)
    if not marker:raise ValueError(page)
    start=marker.start();nxt=re.search(r'\\src\{\d+\}',whole[marker.end():])
    end=marker.end()+nxt.start() if nxt else len(whole)
    byte_start=len(whole[:start].encode());byte_end=len(whole[:end].encode())
    selected=[]
    for span in spans:
        if span['end']<=byte_start or span['start']>=byte_end:continue
        if span['start']<byte_start or span['end']>byte_end:
            raise ValueError('A mathematical expression crosses the printed-page boundary')
        row=dict(span)
        for key in ('start','end','inner_start','inner_end'):
            row[key]-=byte_start
        selected.append(row)
    text=whole[start:end]
    return text,whole[:start].count('\n')+1,whole[:end].count('\n'),data[byte_start:byte_end],selected

def show_math(rel,unit,page,printed=False):
    source=f'sources/{"fr_printed" if printed else "fr"}/fr/{unit}.tex'
    for label,path in [('FR',source),('TRANSLATION',rel)]:
        text,lo,hi,data,spans=page_math_ranges(path,page)
        print(label,path,'lines',lo,hi,'outer math count',len(spans))
        for i,s in enumerate(spans):
            print(i,repr(data[s['start']:s['end']].decode()))

def align_math(rel,layer,unit,page,pairs,expected,printed=False,localized=None):
    source=f'sources/{"fr_printed" if printed else "fr"}/fr/{unit}.tex'
    fr,frlo,frhi,fb,fs=page_math_ranges(source,page)
    target,lo,hi,tb,ts=page_math_ranges(rel,page)
    if (len(ts),len(fs)) != expected:
        raise ValueError(f'Changed span counts: {(len(ts),len(fs))} != {expected}')
    if len({a for a,b in pairs}) != len(pairs):
        raise ValueError('Repeated destination math index')
    localized=localized or {}; mutations=[]; rows=[]
    for ti,fi in pairs:
        t,f=ts[ti],fs[fi];old=tb[t['start']:t['end']].decode();new=fb[f['start']:f['end']].decode()
        for a,b in localized.get(ti,[]):
            if a not in new:raise ValueError('Missing explicitly localized formula text')
            new=new.replace(a,b)
        if old==new:continue
        source_line=lo+tb[:t['start']].count(b'\n')
        fr_line=frlo+fb[:f['start']].count(b'\n')
        evidence=(f'Corrected French {source}, source line {fr_line}, outer math span {fi}; '
          f'printed {unit}-{page}, 400-dpi image and enlarged crops personally inspected in the sequential translation reading. '
          'Explicit paragraphwise pairing approved by the reader. DECISIONS_20261119 row all/formulas requires the French formula TeX, including its alphabets, indices, punctuation and display status; prose inside formulas is translated where explicitly listed. '
          f'French page SHA-256 {hashlib.sha256(fb).hexdigest()}.')
        if printed:evidence=evidence.replace('Corrected French','Literal French')
        rows.append([rel,NAMES[layer],f'{unit}-{page}',f'formula span {ti}; source line {source_line}','formula alignment',old,new,evidence,'terminology','low'])
        mutations.append((t['start'],t['end'],new.encode()))
    for a,b,new in sorted(mutations,reverse=True):tb=tb[:a]+new+tb[b:]
    whole=read(rel)
    if whole.count(target)!=1:raise ValueError('Page segment is not unique')
    write(rel,whole.replace(target,tb.decode(),1))
    with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as out:csv.writer(out,delimiter='\t').writerows(rows)
    return len(rows)

def start_unit(layer,unit,rel):
    heading=f'## {NAMES[layer]} {unit}'
    record=read('CHECK_RECORD.md')
    if '\n'+heading+'\n' in record:raise ValueError('Unit record already started')
    with (ROOT/'CHECK_RECORD.md').open('a') as out:
        out.write(f'\n{heading}\n\nReader: GPT-6 Astra, ChatGPT Pro mode, this run. Started {utc()}. '
          f'Translation source: `{rel}`. The source is compared paragraph by paragraph with the appropriate French layer, '
          'with the original scan open for formulas, numbers and references. Page entries below record partial progress; '
          'the unit is complete only when its explicit completion line is written.\n')

def record_translation_page(layer,unit,page,rel,body,entry_lines=None,printed=False):
    target,lo,hi=page_text(rel,page);frpath=f'sources/{"fr_printed" if printed else "fr"}/fr/{unit}.tex';fr,fl,fh=page_text(frpath,page)
    stamp=utc()
    with (ROOT/'CHECK_RECORD.md').open('a') as out:
        out.write(f'\n**Printed page {page}.** Recorded {stamp}. Compared `{rel}`, current lines {lo}–{hi}, '
            f'with `{frpath}`, lines {fl}–{fh}, and the 400-dpi printed image and enlarged crops. ')
        if entry_lines:out.write(f'Translation entry lines {entry_lines[0]}–{entry_lines[1]}. ')
        out.write(body+'\n')
    with (ROOT/'progress.log').open('a') as out:out.write(f'translation page {layer} {unit}-{page} read {stamp}\n')

def finish_unit(layer,unit,body):
    stamp=utc()
    with (ROOT/'CHECK_RECORD.md').open('a') as out:out.write(f'\nUnit completion: {stamp}. {body}\n')
    with (ROOT/'progress.log').open('a') as out:out.write(f'{layer} {unit} done {stamp}\n')
