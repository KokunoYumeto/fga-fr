"""Inventory literal source-page markers and extract source segments for root.

This is lexical infrastructure only. It does not expand TeX, read scans, decide
whether markers are correct, align sentences, or certify mathematical content.
Source files are read as immutable bytes. Reports contain structural fields only;
the extract subcommand writes requested exact source slices for human reading.
"""

import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import re


UNITS = ['149', 'e149', '182', 'e182', '190', 'e190', '195', 'e195',
         '212', 'e212', '221', 'e221', '232', 'e232', '236', 'e236', 'com']
CONFIG = {
    'fr': ('fr/main.tex', 'fr'),
    'fr_printed': ('fr/main.tex', 'fr'),
    'en': ('en/main.tex', 'en'),
    'es': ('es/FGA_ES_CURRENT.tex', 'es'),
    'es_149_printed': ('es/FGA_ES_149_PRINTED.tex', 'es'),
    'pt-BR': ('pt_BR/FGA_PTBR_CURRENT.tex', 'pt_BR/current'),
    'pt-BR_printed': ('pt_BR/FGA_PTBR_PRINTED.tex', 'pt_BR/diplomatic'),
    'vi': ('FGA_vi_current.tex', 'sources/current'),
    'vi_diplomatic': ('FGA_vi_diplomatic.tex', 'sources/diplomatic'),
    'ko': ('main.tex', ''),
    'zh-Hans': ('source/zh/main.tex', 'source/zh'),
}
CONTROL = re.compile(rb'\\([A-Za-z@]+|[^A-Za-z@])')
LITERAL_PAGE = re.compile(r'(?:[0-9]+|[IVXLCDMivxlcdm]+)\Z')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def utc():
    return datetime.now(timezone.utc).isoformat()


def mask_comments(data):
    """Keep byte positions and newline bytes while masking unescaped comments."""
    result = bytearray(data)
    position = 0
    while position < len(data):
        if data[position] == 37:
            before, slashes = position - 1, 0
            while before >= 0 and data[before] == 92:
                before -= 1
                slashes += 1
            if slashes % 2 == 0:
                end = position
                while end < len(data) and data[end] not in (10, 13):
                    end += 1
                result[position:end] = b' ' * (end - position)
                position = end
                continue
        position += 1
    return bytes(result)


def skip_space(data, position):
    while position < len(data) and data[position:position + 1].isspace():
        position += 1
    return position


def group(data, position, opening=123, closing=125):
    position = skip_space(data, position)
    if position >= len(data) or data[position] != opening:
        return None
    start, depth, cursor = position, 1, position + 1
    while cursor < len(data):
        if data[cursor] == 92:
            token = CONTROL.match(data, cursor)
            cursor = token.end() if token else cursor + 1
            continue
        if data[cursor] == opening:
            depth += 1
        elif data[cursor] == closing:
            depth -= 1
            if depth == 0:
                return start, cursor + 1, data[start + 1:cursor]
        cursor += 1
    return None


def line_number(data, offset):
    return data.count(b'\n', 0, offset) + 1


def line_end(data, end):
    return line_number(data, end) - int(end > 0 and data[end - 1:end] == b'\n')


def calls(data, names):
    masked = mask_comments(data)
    result = []
    for token in CONTROL.finditer(masked):
        name = token[1].decode('ascii', errors='replace')
        if name not in names:
            continue
        argument = group(masked, token.end())
        if argument is None:
            continue
        value = argument[2].decode('utf-8').strip()
        result.append(dict(macro='\\' + name, argument=value,
                           byte_start=token.start(), byte_end=argument[1],
                           line=line_number(data, token.start())))
    return result


def markers(data):
    result = []
    occurrences = Counter()
    for item in calls(data, {'src'}):
        if not LITERAL_PAGE.fullmatch(item['argument']):
            continue
        key = str(int(item['argument'])) if item['argument'].isdigit() else item['argument'].upper()
        occurrences[key] += 1
        result.append(dict(item, page=key, ordinal=len(result) + 1,
                           occurrence=occurrences[key]))
    return result


def interesting_macro(name):
    return 'src' in name.lower() or 'source' in name.lower() or name in {'sid', 'FgaUnitKey', 'fgaunitid'}


def control_name(data, position):
    position = skip_space(data, position)
    wrapped = group(data, position)
    if wrapped:
        token = CONTROL.fullmatch(wrapped[2].strip())
        return (token[1].decode(), wrapped[1]) if token else (None, wrapped[1])
    token = CONTROL.match(data, position)
    return (token[1].decode(), token.end()) if token else (None, position)


def definitions(data):
    masked = mask_comments(data)
    result = []
    kinds = {'newcommand', 'renewcommand', 'providecommand', 'DeclareRobustCommand',
             'def', 'gdef', 'edef', 'xdef', 'let'}
    for token in CONTROL.finditer(masked):
        kind = token[1].decode('ascii', errors='replace')
        if kind not in kinds:
            continue
        cursor = skip_space(masked, token.end())
        if masked[cursor:cursor + 1] == b'*':
            cursor += 1
        name, cursor = control_name(masked, cursor)
        if not name or not interesting_macro(name):
            continue
        alias, arity, literal, body_hash, body_commands = '', 0, '', '', ''
        definition_end = cursor
        if kind == 'let':
            cursor = skip_space(masked, cursor)
            if masked[cursor:cursor + 1] == b'=':
                cursor += 1
            target, cursor = control_name(masked, cursor)
            alias = '\\' + target if target else ''
            definition_end = cursor
        else:
            if kind in {'def', 'gdef', 'edef', 'xdef'}:
                body_start = masked.find(b'{', cursor)
                if body_start < 0:
                    continue
                params = re.findall(rb'#([1-9])', masked[cursor:body_start])
                arity = max((int(n) for n in params), default=0)
                cursor = body_start
            else:
                argument_count = group(masked, cursor, 91, 93)
                if argument_count:
                    arity = int(argument_count[2]) if argument_count[2].isdigit() else -1
                    cursor = argument_count[1]
                    default = group(masked, cursor, 91, 93)
                    if default:
                        cursor = default[1]
            body = group(masked, cursor)
            if not body:
                continue
            body_hash = sha(data[body[0]:body[1]])
            definition_end = body[1]
            body_commands = ','.join(sorted({'\\' + m[1].decode('ascii', errors='replace')
                                             for m in CONTROL.finditer(body[2])}))
            value = body[2].decode('utf-8').strip()
            if re.fullmatch(r'[A-Za-z0-9_.:-]+', value):
                literal = value
        result.append(dict(macro='\\' + name, declaration='\\' + kind,
                           argument_count=arity, alias_target=alias,
                           literal_identifier_value=literal, line=line_number(data, token.start()),
                           definition_body_sha256=body_hash, body_command_spellings=body_commands,
                           definition_byte_start=token.start(),definition_byte_end=definition_end))
    for item in result:
        item['nested_definition'] = any(other['definition_byte_start'] < item['definition_byte_start'] < other['definition_byte_end'] for other in result)
    return result


def source_path(layer, unit):
    filename = '149_diplomatic.tex' if layer == 'es_149_printed' and unit == '149' else unit + '.tex'
    return (Path(CONFIG[layer][1]) / filename).as_posix()


def expected_units(layer):
    return ['149'] if layer == 'es_149_printed' else UNITS


def layer_bytes(work, layer):
    root = work / 'sources' / layer
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}


def tree_hash(files):
    digest = hashlib.sha256()
    for name, data in sorted(files.items()):
        digest.update(name.encode())
        digest.update(b'\0')
        digest.update(hashlib.sha256(data).digest())
    return digest.hexdigest()


def literal_include_graph(work, layer, files):
    root = (work / 'sources' / layer).resolve()
    entry = CONFIG[layer][0]
    cwd = (root / entry).parent
    pending, visited, rows = [entry], set(), []
    while pending:
        current = pending.pop(0)
        if current in visited or current not in files:
            continue
        visited.add(current)
        for item in calls(files[current], {'input', 'include'}):
            value = item['argument']
            resolved, status = '', 'nonliteral or unresolved'
            if re.fullmatch(r'[A-Za-z0-9_./-]+', value):
                filename = value if Path(value).suffix else value + '.tex'
                candidates = [(cwd / filename).resolve(), (root / current).parent.joinpath(filename).resolve()]
                for candidate in candidates:
                    if candidate.is_relative_to(root):
                        relative = candidate.relative_to(root).as_posix()
                        if relative in files:
                            resolved, status = relative, 'literal project path resolved'
                            pending.append(relative)
                            break
            rows.append(dict(layer=layer,including_source='sources/' + layer + '/' + current,
                             line=item['line'],macro=item['macro'],literal_argument=value,
                             resolved_source=('sources/' + layer + '/' + resolved) if resolved else '',
                             status=status,scope='literal include graph; no TeX expansion'))
    return visited, rows


def safe_new_output(work, output):
    output = output.resolve()
    protected = [(work / 'sources').resolve(), (Path(__file__).resolve().parents[1] / 'sources').resolve()]
    if any(output == sources or output.is_relative_to(sources) for sources in protected):
        raise ValueError('Output must not be inside a source tree')
    if output.exists():
        raise FileExistsError('Choose a new output directory; existing files will not be overwritten')
    output.mkdir(parents=True)
    return output


def write_tsv(path, columns, rows):
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, delimiter='\t', extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def inventory(work, output):
    started = utc()
    snapshots = {layer: layer_bytes(work, layer) for layer in CONFIG}
    unit_rows, marker_rows, macro_rows, input_rows, identifiers, issues, layer_rows = [], [], [], [], [], [], []
    index = {}
    for layer, files in snapshots.items():
        reachable, graph = literal_include_graph(work, layer, files)
        input_rows.extend(graph)
        total = 0
        for relative, data in files.items():
            if relative.endswith('.tex'):
                for item in definitions(data):
                    macro_rows.append(dict(layer=layer,source='sources/' + layer + '/' + relative,**item))
        for unit in expected_units(layer):
            relative = source_path(layer, unit)
            present = relative in files
            data = files.get(relative, b'')
            marked = markers(data)
            index[layer, unit] = marked
            counts = Counter(m['page'] for m in marked)
            total += len(marked)
            prefix = marked[0]['byte_start'] if marked else len(data)
            unit_rows.append(dict(layer=layer,unit=unit,source='sources/' + layer + '/' + relative,
                                  present=present,literal_include_reachable=relative in reachable,
                                  source_file_sha256=sha(data) if present else '',source_bytes=len(data),
                                  marker_count=len(marked),macro_spellings=','.join(sorted({m['macro'] for m in marked})),
                                  page_marker_sequence=','.join(m['page'] for m in marked),
                                  repeated_markers=','.join(k for k,v in counts.items() if v > 1),
                                  unmarked_prefix_bytes=prefix,scope='lexical structure only'))
            if not present:
                issues.append(dict(layer=layer,unit=unit,page='',issue='missing expected unit source',source='sources/' + layer + '/' + relative,detail='Declared layer scope; no content inference'))
            elif relative not in reachable:
                issues.append(dict(layer=layer,unit=unit,page='',issue='unit not reached by literal include graph',source='sources/' + layer + '/' + relative,detail='No TeX macro expansion was attempted'))
            for ordinal, item in enumerate(marked):
                end = marked[ordinal + 1]['byte_start'] if ordinal + 1 < len(marked) else len(data)
                marker_rows.append(dict(layer=layer,unit=unit,source='sources/' + layer + '/' + relative,
                                       source_file_sha256=sha(data),**item,segment_byte_end=end,
                                       segment_last_line=line_end(data,end)))
            for item in calls(data, {'sid'}):
                identifiers.append(dict(layer=layer,unit=unit,source='sources/' + layer + '/' + relative,**item))
            for page, count in counts.items():
                if count > 1:
                    issues.append(dict(layer=layer,unit=unit,page=page,issue='duplicate page marker within unit',source='sources/' + layer + '/' + relative,detail=str(count) + ' literal occurrences; extraction requires occurrence selection'))
            numbers = [int(m['page']) for m in marked if m['page'].isdigit()]
            if any(b < a for a,b in zip(numbers,numbers[1:])):
                issues.append(dict(layer=layer,unit=unit,page='',issue='descending numeric marker order',source='sources/' + layer + '/' + relative,detail='Lexical sequence only'))
        layer_rows.append(dict(layer=layer,entry_point='sources/' + layer + '/' + CONFIG[layer][0],
                               declared_units=','.join(expected_units(layer)),source_tree_sha256=tree_hash(files),
                               source_files=len(files),unit_files=len(expected_units(layer)),marker_count=total,
                               page_macro='\\src',page_macro_required_arguments=1,
                               scope='149 only' if layer == 'es_149_printed' else 'eight exposes, eight errata, commentary'))
    matrix = []
    for unit in UNITS:
        reference = [m['page'] for m in index.get(('fr', unit), [])]
        union = list(dict.fromkeys(reference + [m['page'] for layer in CONFIG for m in index.get((layer,unit),[])]))
        for page in union:
            row = dict(unit=unit,page=page,reference_layer='fr')
            for layer in CONFIG:
                if unit not in expected_units(layer):
                    row[layer] = 'outside declared scope'
                    continue
                count = sum(m['page'] == page for m in index[layer,unit])
                row[layer] = count
                if page in reference and count == 0:
                    issues.append(dict(layer=layer,unit=unit,page=page,issue='marker missing versus French reference',source='sources/' + layer + '/' + source_path(layer,unit),detail='Missing anchor only; text presence or correctness not decided'))
                elif page not in reference and count:
                    issues.append(dict(layer=layer,unit=unit,page=page,issue='marker absent from French reference set',source='sources/' + layer + '/' + source_path(layer,unit),detail='Cross-layer structural difference only'))
            matrix.append(row)
    output = safe_new_output(work, output)
    tables = [
        ('LAYER_SUMMARY.tsv',list(layer_rows[0]),layer_rows),
        ('UNIT_STRUCTURE.tsv',list(unit_rows[0]),unit_rows),
        ('MARKER_OCCURRENCES.tsv',list(marker_rows[0]),marker_rows),
        ('MACRO_DEFINITIONS.tsv',list(macro_rows[0]),macro_rows),
        ('INPUT_GRAPH.tsv',list(input_rows[0]),input_rows),
        ('UNIT_IDENTIFIERS.tsv',list(identifiers[0]),identifiers),
        ('CROSS_LAYER_MATRIX.tsv',['unit','page','reference_layer',*CONFIG],matrix),
        ('STRUCTURAL_ISSUES.tsv',['layer','unit','page','issue','source','detail'],issues),
    ]
    for name, columns, rows in tables:
        write_tsv(output/name, columns, rows)
    metadata = dict(started_utc=started,completed_utc=utc(),layers=len(CONFIG),unit_files=len(unit_rows),
                    marker_occurrences=len(marker_rows),issues=len(issues),reference_layer='fr',
                    source_reads='one captured byte set per layer; no source writes',
                    comment_handling='unescaped percent comments masked without changing byte offsets',
                    limitations='literal src/sid calls and literal include paths; no TeX expansion or verbatim-environment simulation; no scans/content review',
                    offset_convention='zero-based bytes, exclusive end; one-based source lines',
                    script_sha256=sha(Path(__file__).read_bytes()))
    snapshot = work / 'SNAPSHOT.json'
    if snapshot.exists():
        metadata['frozen_snapshot'] = json.loads(snapshot.read_text())
    (output/'INVENTORY_METADATA.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(f'Inventoried {len(CONFIG)} layers, {len(unit_rows)} unit files, {len(marker_rows)} page markers; {len(issues)} structural issues.')


def select_segment(data, page=None, occurrence=None, include_prefix=False, neighbors=False):
    marked = markers(data)
    if page is None:
        return dict(status='whole unit',start=0,end=len(data),matched_page='',next_page='')
    key = str(int(page)) if page.isdigit() else page.upper()
    found = [m for m in marked if m['page'] == key]
    if len(found) > 1 and occurrence is None:
        return dict(status='ambiguous duplicate marker',start=None,end=None,matched_page='',next_page='',matches=len(found))
    if found:
        selected = occurrence or 1
        if not 1 <= selected <= len(found):
            return dict(status='requested occurrence absent',start=None,end=None,matched_page='',next_page='',matches=len(found))
        item = found[selected - 1]
        position = marked.index(item)
        following = marked[position + 1] if position + 1 < len(marked) else None
        start = 0 if include_prefix and position == 0 else item['byte_start']
        return dict(status='exact marker segment',start=start,end=following['byte_start'] if following else len(data),matched_page=item['page'],next_page=following['page'] if following else '')
    if neighbors and key.isdigit() and all(m['page'].isdigit() for m in marked):
        numbers = [int(m['page']) for m in marked]
        if numbers and all(b > a for a,b in zip(numbers,numbers[1:])):
            previous = [m for m in marked if int(m['page']) < int(key)]
            following = [m for m in marked if int(m['page']) > int(key)]
            before = previous[-1] if previous else None
            after = following[0] if following else None
            return dict(status='neighbor context; requested marker absent',start=before['byte_start'] if before else 0,end=after['byte_start'] if after else len(data),matched_page=before['page'] if before else '',next_page=after['page'] if after else '')
    return dict(status='requested marker absent',start=None,end=None,matched_page='',next_page='',matches=0)


def extract(work, output, layers, unit, page, occurrence, include_prefix, neighbors, strict):
    captured = {layer: layer_bytes(work, layer) for layer in layers}
    output = safe_new_output(work, output)
    records, panels = [], []
    for layer in layers:
        relative = source_path(layer,unit)
        files = captured[layer]
        data = files.get(relative,b'')
        if unit not in expected_units(layer):
            chosen = dict(status='unit outside declared layer scope',start=None,end=None,matched_page='',next_page='')
        elif relative not in files:
            chosen = dict(status='unit source missing',start=None,end=None,matched_page='',next_page='')
        else:
            chosen = select_segment(data,page,occurrence,include_prefix,neighbors)
        start,end = chosen['start'],chosen['end']
        segment = data[start:end] if start is not None else b''
        filename = layer + '.tex' if start is not None else ''
        if filename:
            (output/filename).write_bytes(segment)
        record = dict(layer=layer,unit=unit,requested_page=page or '',requested_occurrence=occurrence or '',
                      status=chosen['status'],source='sources/'+layer+'/'+relative,
                      source_tree_sha256=tree_hash(files),source_file_sha256=sha(data) if relative in files else '',
                      byte_start=start if start is not None else '',byte_end_exclusive=end if end is not None else '',
                      first_line=line_number(data,start) if start is not None else '',
                      last_line=line_end(data,end) if end is not None else '',
                      matched_page=chosen['matched_page'],next_marker_page=chosen['next_page'],
                      segment_file=filename,segment_bytes=len(segment),segment_sha256=sha(segment) if filename else '',
                      content_review='not performed by extractor')
        records.append(record)
        heading = '<h2>'+html.escape(layer)+'</h2><p>'+html.escape(record['status'])+'</p>'
        locator = '<p class="locator">'+html.escape(record['source'])+'</p>'
        interval = '<p class="locator">Lines '+str(record['first_line'])+'–'+str(record['last_line'])+'; bytes '+str(record['byte_start'])+'–'+str(record['byte_end_exclusive'])+'</p>'
        body = html.escape(segment.decode('utf-8')) if filename else 'No source slice was selected. See SEGMENTS.tsv for the structural status.'
        panels.append('<section><header>'+heading+locator+interval+'</header><pre>'+body+'</pre></section>')
    write_tsv(output/'SEGMENTS.tsv',list(records[0]),records)
    title = 'Source segments: '+unit+(' / '+page if page else ' / whole unit')
    page_html = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'"><title>'+html.escape(title)+'</title><style>body{margin:0;color:#16202a;background:#f4f5f6;font:15px system-ui}h1{font-size:20px;margin:16px}body>p{margin:0 16px 16px}.panels{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(420px,48vw);gap:12px;overflow-x:auto;padding:0 16px 16px}section{background:white;border:1px solid #b7c0c8;border-radius:6px;min-width:0}header{padding:10px 14px;border-bottom:1px solid #d5dbe0}h2{font-size:18px;margin:0}header p{margin:5px 0}.locator{font:12px ui-monospace,monospace;overflow-wrap:anywhere}pre{margin:0;padding:14px;height:70vh;overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere;tab-size:2;font:13px/1.5 ui-monospace,monospace}</style><body><h1>'+html.escape(title)+'</h1><p>Exact source slices selected by literal markers. Columns are not sentence-aligned. No content review is implied.</p><main class="panels">'+''.join(panels)+'</main></body></html>'
    (output/'index.html').write_text(page_html,encoding='utf-8')
    print('Extracted structural selections for '+','.join(layers)+'; source text was not printed to the console.')
    print('Statuses: '+ '; '.join(r['layer']+'='+r['status'] for r in records))
    if strict and any(r['status'] not in {'whole unit','exact marker segment'} for r in records):
        raise SystemExit(2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work',type=Path,required=True,help='root containing sources/')
    sub = parser.add_subparsers(dest='command',required=True)
    inv = sub.add_parser('inventory',help='write structural TSV/JSON reports only')
    inv.add_argument('--out',type=Path,required=True,help='new output directory')
    ext = sub.add_parser('extract',help='write exact source slices and a side-by-side HTML reading aid')
    ext.add_argument('--out',type=Path,required=True,help='new temporary output directory')
    ext.add_argument('--layers',default='fr,en',help='comma-separated layer names or all')
    ext.add_argument('--unit',choices=UNITS,required=True)
    ext.add_argument('--page',help='literal marker page; omit for the whole unit')
    ext.add_argument('--occurrence',type=int,help='explicit one-based selection if a marker is duplicated')
    ext.add_argument('--include-unit-prefix',action='store_true',help='include unmarked prefix only when selecting the first marker')
    ext.add_argument('--neighbor-span',action='store_true',help='for a missing numeric marker, explicitly include surrounding marker context')
    ext.add_argument('--strict',action='store_true',help='write outputs then exit2 for missing, ambiguous, or contextual selections')
    args = parser.parse_args()
    work = args.work.resolve()
    if args.command == 'inventory':
        inventory(work,args.out)
    else:
        layers = list(CONFIG) if args.layers == 'all' else list(dict.fromkeys(args.layers.split(',')))
        if not layers or any(layer not in CONFIG for layer in layers):
            raise ValueError('Unknown layer selection')
        if args.page and not LITERAL_PAGE.fullmatch(args.page):
            raise ValueError('Page must be a literal numeric or Roman marker')
        if args.occurrence is not None and args.occurrence < 1:
            raise ValueError('Occurrence is one-based')
        extract(work,args.out,layers,args.unit,args.page,args.occurrence,args.include_unit_prefix,args.neighbor_span,args.strict)


if __name__ == '__main__':
    main()
