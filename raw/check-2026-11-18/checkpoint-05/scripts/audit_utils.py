"""Small auditable mutations. Run from the deliverable directory.
Only explicitly supplied replacements are applied; no OCR decides a reading.
"""
from pathlib import Path
from datetime import datetime, timezone
import csv, re
ROOT=Path(__file__).resolve().parents[1]
FIELDS=['file','layer','printed_page','line','statement','old','new','evidence','kind','confidence']
def utc(): return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
def read(rel): return (ROOT/rel).read_bytes().decode('utf-8').replace('\r\n','\n')
def write(rel,text):
    p=ROOT/rel; old=p.read_bytes() if p.exists() else b''
    p.write_bytes(text.replace('\n','\r\n').encode() if b'\r\n' in old else text.encode())
def replace(rel,old,new,layer,page,line,statement,evidence,kind='reading',confidence='low',count=1,full=False):
    text=read(rel)
    start,end=0,len(text)
    pm=re.fullmatch(r'[a-z0-9]+-(\d+)',page)
    if pm and not full:
        marker=re.search(r'\\src\{'+pm.group(1)+r'\}',text)
        if marker:
            start=marker.start()
            nxt=re.search(r'\\src\{\d+\}',text[marker.end():])
            if nxt: end=marker.end()+nxt.start()
    segment=text[start:end]; n=segment.count(old)
    if n==0:
        with (ROOT/'CORRECTIONS.tsv').open(newline='') as f:
            already=any(r['file']==rel and r['old']==old and r['new']==new for r in csv.DictReader(f,delimiter='\t'))
        if already and new in segment: return
    if n!=count: raise ValueError(f'{rel}: expected {count} preimages, found {n}: {old[:80]}')
    write(rel,text[:start]+segment.replace(old,new)+text[end:])
    with (ROOT/'CORRECTIONS.tsv').open('a',newline='') as f:
        csv.writer(f,delimiter='\t').writerow([rel,layer,page,line,statement,old,new,evidence,kind,confidence])
def footnotes(text):
    for m in re.finditer(r'\\footnote\{',text):
        i=m.end(); depth=1
        while depth and i<len(text):
            if text[i]=='{' and (i==0 or text[i-1]!='\\'): depth+=1
            if text[i]=='}' and (i==0 or text[i-1]!='\\'): depth-=1
            i+=1
        if depth: raise ValueError('unclosed footnote')
        yield m.start(),i,text[m.end():i-1]
def page_text(rel,page):
    text=read(rel); match=re.search(r'\\src\{'+str(page)+r'\}',text)
    if not match: raise ValueError(page)
    start=match.start(); nxt=re.search(r'\\src\{\d+\}',text[match.end():])
    end=match.end()+nxt.start() if nxt else len(text)
    return text[start:end],text[:start].count('\n')+1,text[:end].count('\n')
def event(sid,how,result,where):
    with (ROOT/'CHECK_EVENTS.tsv').open('a',newline='') as f:
        csv.writer(f,delimiter='\t').writerow([sid,utc(),'GPT-6 Astra, ChatGPT Pro mode, this run',how,result,where])
def record_page(expose,page,body,done=True):
    stamp=utc()
    with (ROOT/'CHECK_RECORD.md').open('a') as f:
        f.write(f'\n### {expose}-{page}\n\nReader: GPT-6 Astra, ChatGPT Pro mode, this run. Recorded {stamp}.\n\n{body}\n')
    if done:
        with (ROOT/'progress.log').open('a') as f: f.write(f'page {expose}-{page} done {stamp}\n')
def underline_prose(text):
    """Format an explicitly selected, visually verified emphasis span."""
    parts=re.split(r'(\$[^$]+\$|\([0-9]+\.[0-9]+\))',text)
    for i,s in enumerate(parts):
        if i%2: continue
        m=re.fullmatch(r'([\s,.;:()]*)(.*?)([\s,.;:()]*?)',s,re.S)
        if m and m.group(2): parts[i]=m.group(1)+r'\uline{'+m.group(2)+'}'+m.group(3)
    return ''.join(parts)
def upright_page(rel,layer,page):
    """Apply only after visually deciding this page's letterforms are upright.

    Identical display preimages are replaced together with a page-local count
    guard. Their aggregate correction row still needs later per-place review.
    """
    text,_,_=page_text(rel,int(page.split('-')[-1]))
    inline=list(dict.fromkeys(re.findall(r'(?<!\\)\$([^$]+)\$',text)))
    for expr in inline:
        if expr.startswith(r'\symup{'): continue
        if '&' in expr:
            if r'\symup{' not in expr: raise ValueError('Manual array typography required')
            continue
        replace(rel,'$'+expr+'$',r'$\symup{'+expr+'}$',layer,page,'inline mathematical letters','','400-dpi image and enlarged page crops: typed mathematical letters are upright. Explicit nested script, Gothic, roman and underline commands remain unchanged.',count=text.count('$'+expr+'$'))
    text,_,_=page_text(rel,int(page.split('-')[-1]))
    seen=set()
    for m in list(re.finditer(r'(\\begin\{equation\}(?:\\tag\{[^}]+\})?\s*)(.*?)(\s*\\end\{equation\})',text,re.S)):
        old=m.group(0)
        if old in seen: continue
        seen.add(old)
        body=m.group(2)
        if r'\symup{' in body: continue
        formatted=r'\symup{'+body+'}'
        if '&' in body:
            a=re.search(r'(\\begin\{aligned\})(.*?)(\\end\{aligned\})',body,re.S)
            if not a: raise ValueError('Manual alignment typography required')
            pieces=re.split(r'(\\\\|&)',a.group(2))
            pieces=[x if x in ('&',r'\\') or not x.strip() else r'\symup{'+x.strip()+'}' for x in pieces]
            formatted=body[:a.start(2)]+''.join(pieces)+body[a.end(2):]
        replace(rel,old,m.group(1)+formatted+m.group(3),layer,page,'numbered display','','400-dpi scan formula and enlarged crop: upright typed variables; explicit mathematical alphabets retained.',count=text.count(old))
    text,_,_=page_text(rel,int(page.split('-')[-1]))
    seen=set()
    for m in list(re.finditer(r'(\\\[\s*)(.*?)(\s*\\\])',text,re.S)):
        old=m.group(0)
        if old in seen: continue
        seen.add(old)
        body=m.group(2)
        if r'\symup{' in body: continue
        formatted=r'\symup{'+body+'}'
        if '&' in body:
            a=re.search(r'(\\begin\{aligned\})(.*?)(\\end\{aligned\})',body,re.S)
            if not a: raise ValueError('Manual alignment typography required')
            pieces=re.split(r'(\\\\|&)',a.group(2))
            pieces=[x if x in ('&',r'\\') or not x.strip() else r'\symup{'+x.strip()+'}' for x in pieces]
            formatted=body[:a.start(2)]+''.join(pieces)+body[a.end(2):]
        replace(rel,old,m.group(1)+formatted+m.group(3),layer,page,'unnumbered display','','400-dpi scan formula and enlarged crop: upright typed variables; explicit mathematical alphabets retained.',count=text.count(old))
