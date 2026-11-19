"""Nonmutating, page-keyed lexical math and reference candidate navigator.

The input is read twice before analysis; output retains hashes and exact source
slices. Token normalization is used only for ordered search candidates. Nothing
here expands TeX, judges meaning, or authorizes source changes.
"""
import argparse
from bisect import bisect_right
from collections import Counter
import csv
from datetime import datetime, timezone
import difflib
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
if not all((HERE / name).exists() for name in
           ['source_segments.py', 'translation_math_lexer.py']):
    sys.path.insert(0, str(Path('FGA_CHECK/scripts').resolve()))
import source_segments as source
import translation_math_lexer as lexer

PAIRINGS = {'en': 'fr', 'es': 'fr', 'pt-BR': 'fr', 'vi': 'fr',
            'ko': 'fr', 'zh-Hans': 'fr', 'es_149_printed': 'fr_printed',
            'pt-BR_printed': 'fr_printed', 'vi_diplomatic': 'fr_printed'}
ASCII_SPACE = b' \t\r\n\v\f'
EMAIL = re.compile(rb'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
LOCAL_PATH = re.compile(rb'/(?:workspace|home|root|tmp|Users|opt)/[^\s{}<>]*')
DRIVE = re.compile(rb'[A-Za-z]:[\\/][^\s{}<>"\x27]*')
# Exact regex-match hashes checked lexically in the frozen source inventory.
# These are colon-plus-TeX-control sequences, sometimes extending past a closing
# math delimiter. No path text is stored here. Unknown patterns remain blocked.
TEX_LOOKALIKE_CATALOG = {
    'af5ff02056265a639e5f35a8620f6e566403a257f2be838eef0af5d18ae38056': 'math_control_sequence',
    '1a9106f1baeac3eab2a9680e82eee36aac4ede6b26480ebea72d48a57e7fbb9e': 'math_control_sequence',
    '7cec7a1049617d60235b7b42961e389cbeb5f8dcf3320a4cdac41fbca3705b47': 'literal_footnote_control',
    'ce208bd677c7806a30f7c838cdb7765c1dd2bc8fbd025b7b90740b088e4cfb10': 'math_control_sequence',
    'abe9426fa759e6f7d1b83237c9dcd95c525498cdcfe7ee397aca08b88d91f14e': 'math_control_sequence_regex_extends_past_delimiter',
}
# These literal shapes are navigation candidates, never classified references.
SHAPES = re.compile(rb'\((?:[IVXLC]+[,;] *)?[0-9]+(?:\.[0-9]+){1,4}[a-z]?\)'
                    rb'|\[(?:[A-Z][A-Z0-9-]*(?:, *)?)?(?:[IVXLC]+[,;] *)?'
                    rb'[0-9]+(?:\.[0-9]+){0,4}[a-z]?\]')


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def tsv(path, rows, fields):
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter='\t',
                                extrasaction='ignore', lineterminator='\n')
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value, ensure_ascii=False)
                             if isinstance(value, (dict, list)) else value
                             for key, value in row.items()})


def jsonl(path, rows, compressed=False):
    if compressed:
        # Fixed gzip timestamp makes the report reproducible for fixed rows.
        with path.open('wb') as raw, gzip.GzipFile(fileobj=raw, mode='wb', mtime=0) as packed:
            for row in rows:
                packed.write((json.dumps(row, ensure_ascii=False,
                                         separators=(',', ':')) + '\n').encode())
    else:
        with path.open('w') as stream:
            for row in rows:
                stream.write(json.dumps(row, ensure_ascii=False,
                                        separators=(',', ':')) + '\n')


def normalized_digest(data):
    """Omit comments/ASCII whitespace; preserve control-sequence boundaries.

    This is a lexical signature, not a claim of TeX or mathematical equivalence.
    Control words remain single tokens; all other non-space bytes are tokens.
    UTF-8 bytes and every brace, macro, symbol and punctuation byte are retained.
    """
    masked, _ = lexer.mask_comments(data)
    digest = hashlib.sha256()
    cursor = 0
    while cursor < len(masked):
        if masked[cursor] in ASCII_SPACE:
            cursor += 1
            continue
        match = lexer.CONTROL.match(masked, cursor) if masked[cursor] == 92 else None
        token = match.group() if match else masked[cursor:cursor + 1]
        digest.update(len(token).to_bytes(4, 'big'))
        digest.update(token)
        cursor += len(token)
    return digest.hexdigest()


def relative(value):
    path = Path(value)
    if path.is_absolute():
        try:
            return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
        except ValueError:
            raise ValueError('Input/output paths must be relative to this workspace')
    return path.as_posix()


def capture(work, paths):
    started = utc()
    first = {path: (work / path).read_bytes() for path in sorted(paths)}
    second = {path: (work / path).read_bytes() for path in sorted(paths)}
    if first != second:
        raise ValueError('Selected source files changed during capture; retry with a frozen input')
    return first, {'started_utc': started, 'completed_utc': utc(),
                   'two_consecutive_reads_identical': True,
                   'source_work': relative(work),
                   'files': {p: {'bytes': len(b), 'sha256': sha(b)}
                             for p, b in first.items()}}


def locator(data, marks, start, end):
    starts = [m['byte_start'] for m in marks]
    index = bisect_right(starts, start) - 1
    anchor = marks[max(0, index)] if marks else None
    covered = [m['page'] for m in marks
               if start < m['byte_start'] < end]
    if anchor:
        covered.insert(0, anchor['page'])
    return {'byte_start': start, 'byte_end_exclusive': end,
            'line_start': source.line_number(data, start),
            'line_end': source.line_end(data, end),
            'page': anchor['page'] if anchor else '',
            'page_occurrence': anchor['occurrence'] if anchor else None,
            'unmarked_prefix': index < 0,
            'cross_marker': len(set(covered)) > 1,
            'covered_pages': list(dict.fromkeys(covered))}


def privacy(data, parsed):
    findings = []
    for kind, pattern in [('email', EMAIL), ('local_absolute_path', LOCAL_PATH)]:
        for match in pattern.finditer(data):
            findings.append({'kind': kind, 'start': match.start(), 'end': match.end(),
                             'sha256': sha(match.group())})
    for match in DRIVE.finditer(data):
        catalog = TEX_LOOKALIKE_CATALOG.get(sha(match.group()))
        starts_in_math = any(s['start'] <= match.start() < s['end']
                             for s in parsed['spans'])
        is_footnote_call = (catalog == 'literal_footnote_control' and
                            data[match.start() + 2:match.end()] == b'\\footnote' and
                            data[match.end():match.end() + 1] == b'{')
        if catalog and (starts_in_math or is_footnote_call):
            findings.append({'kind': 'tex_control_lookalike_preserved',
                             'start': match.start(), 'end': match.end(),
                             'sha256': sha(match.group()), 'basis': catalog})
            continue
        # A colon plus one TeX control word in literal math is a known lexical
        # lookalike; literal math punctuation may follow. An additional path
        # separator or filename suffix remains a blocking finding.
        candidate = match.group()[2:]
        control = lexer.CONTROL.match(candidate)
        if control and not re.fullmatch(rb'[0-9_^*+\-=,:;!?()$]*', candidate[control.end():]):
            control = None
        inside = [s for s in parsed['spans']
                  if s['start'] <= match.start() and match.end() <= s['end']]
        if control and inside:
            containing = min(inside, key=lambda s: s['end'] - s['start'])
            text_inside = any(g['inner_start'] <= match.start() < g['inner_end']
                              and g['inner_start'] > containing['start']
                              for g in parsed['text_groups'])
            if not text_inside:
                findings.append({'kind': 'tex_control_lookalike_preserved',
                                 'start': match.start(), 'end': match.end(),
                                 'sha256': sha(match.group())})
                continue
        findings.append({'kind': 'drive_path_candidate', 'start': match.start(),
                         'end': match.end(), 'sha256': sha(match.group())})
    return findings


def analyze(layer, unit, data):
    path = 'sources/' + layer + '/' + source.source_path(layer, unit)
    parsed = lexer.scan_math(data)
    marks = source.markers(data)
    records = []
    for n, span in enumerate(parsed['spans']):
        raw = data[span['start']:span['end']]
        inner = data[span['inner_start']:span['inner_end']]
        row = {'id': f'{layer}:{unit}:M{n + 1:05d}', 'layer': layer, 'unit': unit,
               'file': path, 'span_ordinal': n + 1,
               'kind': span['kind'], 'delimiter': span['delimiter'],
               'environment': span['environment'], 'depth': span['depth'],
               'parent_id': (f'{layer}:{unit}:M{span["parent_span_index"] + 1:05d}'
                             if span['parent_span_index'] is not None else ''),
               'inner_start': span['inner_start'], 'inner_end_exclusive': span['inner_end'],
               'raw_sha256': sha(raw), 'inner_sha256': sha(inner),
               'inner_token_sha256': normalized_digest(inner),
               'full_token_sha256': normalized_digest(raw),
               'ambiguous': span['ambiguous'], 'raw_text': raw.decode('utf-8')}
        row.update(locator(data, marks, span['start'], span['end']))
        records.append(row)
    references = []
    for n, item in enumerate(parsed['references']):
        raw = data[item['start']:item['end']]
        row = {'id': f'{layer}:{unit}:R{n + 1:05d}', 'layer': layer, 'unit': unit,
               'file': path, 'command': item['command'], 'starred': item['starred'],
               'raw_sha256': sha(raw), 'token_sha256': normalized_digest(raw),
               'raw_text': raw.decode('utf-8')}
        row.update(locator(data, marks, item['start'], item['end']))
        references.append(row)
    masked, _ = lexer.mask_comments(data)
    shapes = []
    for match in SHAPES.finditer(masked):
        if any(r['start'] <= match.start() and match.end() <= r['end']
               for r in parsed['references']):
            continue
        row = {'id': f'{layer}:{unit}:S{len(shapes) + 1:05d}', 'layer': layer,
               'unit': unit, 'file': path, 'raw_sha256': sha(match.group()),
               'token_sha256': normalized_digest(match.group()),
               'raw_text': data[match.start():match.end()].decode('utf-8'),
               'classification': 'literal_reference_shaped_candidate_only'}
        row.update(locator(data, marks, match.start(), match.end()))
        shapes.append(row)
    return {'layer': layer, 'unit': unit, 'file': path, 'data': data,
            'sha256': sha(data), 'markers': marks, 'math': records,
            'references': references, 'reference_shapes': shapes,
            'issues': parsed['issues'], 'privacy': privacy(data, parsed),
            'text_groups': parsed['text_groups']}


def page_segment(item, page, include_prefix=True):
    marks = item['markers']
    selected = [m for m in marks if m['page'] == page]
    if not selected:
        return {'status': 'missing_marker', 'page': page}
    if len(selected) > 1:
        return {'status': 'duplicate_marker', 'page': page,
                'occurrences': len(selected)}
    marker = selected[0]
    index = marks.index(marker)
    start = 0 if include_prefix and index == 0 else marker['byte_start']
    end = marks[index + 1]['byte_start'] if index + 1 < len(marks) else len(item['data'])
    raw = item['data'][start:end]
    return {'status': 'literal_marker_segment', 'page': page,
            'next_page': marks[index + 1]['page'] if index + 1 < len(marks) else '',
            'prefix_included': start < marker['byte_start'],
            'marker_byte_start': marker['byte_start'],
            'byte_start': start, 'byte_end_exclusive': end,
            'line_start': source.line_number(item['data'], start),
            'line_end': source.line_end(item['data'], end),
            'bytes': len(raw), 'sha256': sha(raw), 'file': item['file']}


def page_records(item, page, stream):
    return [row for row in item[stream] if row['page'] == page]


def alignment(left, right, key, prefix):
    result = []
    matcher = difflib.SequenceMatcher(None, [r[key] for r in left],
                                     [r[key] for r in right], autojunk=False)
    for operation, a, b, c, d in matcher.get_opcodes():
        pieces = [(a + n, a + n + 1, c + n, c + n + 1)
                  for n in range(b - a)] if operation == 'equal' else [(a, b, c, d)]
        for aa, bb, cc, dd in pieces:
            l, r = left[aa:bb], right[cc:dd]
            identical = (len(l) == len(r) == 1 and
                         l[0]['raw_sha256'] == r[0]['raw_sha256'])
            result.append({'id': f'{prefix}:A{len(result) + 1:04d}',
                           'operation': operation,
                           'status': ('raw_identical' if identical else
                                      'token_candidate_raw_different' if operation == 'equal'
                                      else 'unpaired_ordered_block'),
                           'left_ids': [x['id'] for x in l],
                           'right_ids': [x['id'] for x in r],
                           'left_count': len(l), 'right_count': len(r),
                           'left_ordinals': [aa + 1, bb] if l else [],
                           'right_ordinals': [cc + 1, dd] if r else [],
                           'human_review_required': True})
    return result


def pair_page(left, right, page):
    ls, rs = page_segment(left, page), page_segment(right, page)
    status = 'aligned_marker_boundaries'
    if ls['status'] != 'literal_marker_segment':
        status = 'french_' + ls['status']
    elif rs['status'] != 'literal_marker_segment':
        status = 'translation_' + rs['status']
    elif ls['next_page'] != rs['next_page']:
        status = 'next_marker_boundary_mismatch_unaligned'
    if left['issues'] or right['issues']:
        status += '_lexical_issues_present'
    streams = {}
    counts = {}
    for stream, key in [('math', 'inner_token_sha256'), ('references', 'token_sha256'),
                        ('reference_shapes', 'token_sha256')]:
        l = page_records(left, page, stream)
        r = page_records(right, page, stream)
        if stream == 'math':
            counts['french_math_all'] = len(l)
            counts['translation_math_all'] = len(r)
            l = [x for x in l if not x['parent_id']]
            r = [x for x in r if not x['parent_id']]
        counts['french_' + stream] = len(l)
        counts['translation_' + stream] = len(r)
        streams[stream] = (alignment(l, r, key, f'{right["layer"]}:{left["unit"]}:{page}:{stream}')
                           if status == 'aligned_marker_boundaries' else [])
    return {'translation': right['layer'], 'french_layer': left['layer'],
            'unit': left['unit'], 'page': page, 'page_key': left['unit'] + '-' + page,
            'status': status, 'french_file': left['file'],
            'translation_file': right['file'], 'french_sha256': left['sha256'],
            'translation_sha256': right['sha256'], 'french_segment': ls,
            'translation_segment': rs, **counts, 'candidate_alignments': streams}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--layers', default='en', help='Translation layer list, or all')
    parser.add_argument('--units', default='149', help='Unit list, or all')
    parser.add_argument('--page', help='One literal printed-page key; omit for all unit pages')
    parser.add_argument('--source-segments', action='store_true',
                        help='Write exact paired page source fragments; intended for selected units')
    parser.add_argument('--compact', action='store_true',
                        help='Gzip large record/alignment JSONL streams')
    parser.add_argument('--note', default='', help='Snapshot staleness or requested scope note')
    args = parser.parse_args()
    if args.page and not source.LITERAL_PAGE.fullmatch(args.page):
        parser.error('Page must be one literal decimal or Roman page key')
    if args.page:
        args.page = str(int(args.page)) if args.page.isdigit() else args.page.upper()
    try:
        args.out.resolve().relative_to((args.work / 'sources').resolve())
    except ValueError:
        pass
    else:
        parser.error('Output must be outside the input sources tree')
    if EMAIL.search(args.note.encode()) or LOCAL_PATH.search(args.note.encode()):
        parser.error('Scope notes must omit email addresses and local absolute paths')
    if args.out.exists():
        parser.error('Output directory already exists; choose a fresh destination')
    layers = list(PAIRINGS) if args.layers == 'all' else args.layers.split(',')
    units = source.UNITS if args.units == 'all' else args.units.split(',')
    if not layers or any(x not in PAIRINGS for x in layers):
        parser.error('Unknown translation layer')
    if not units or any(x not in source.UNITS for x in units):
        parser.error('Unknown source unit')
    jobs = [(layer, unit) for layer in layers for unit in units
            if unit in source.expected_units(layer)]
    selected = sorted(set((layer, unit) for layer, unit in jobs) |
                      set((PAIRINGS[layer], unit) for layer, unit in jobs))
    paths = ['sources/' + layer + '/' + source.source_path(layer, unit)
             for layer, unit in selected]
    captured, manifest = capture(args.work, paths)
    manifest['note'] = args.note
    manifest['pairings'] = {l: PAIRINGS[l] for l in layers}
    manifest['script_sha256'] = sha(Path(__file__).read_bytes())
    manifest['lexer_sha256'] = sha(Path(lexer.__file__).read_bytes())
    manifest['marker_helper_sha256'] = sha(Path(source.__file__).read_bytes())
    analyzed = {(layer, unit): analyze(layer, unit, captured['sources/' + layer + '/' +
                                                          source.source_path(layer, unit)])
                for layer, unit in selected}
    privacy_rows = [dict(file=item['file'], **finding) for item in analyzed.values()
                    for finding in item['privacy']]
    blockers = [x for x in privacy_rows if x['kind'] != 'tex_control_lookalike_preserved']
    if blockers:
        print(json.dumps({'status': 'privacy_preflight_blocked_no_output',
                          'findings': blockers}))
        return 2
    args.out.mkdir(parents=True)
    dump(args.out / 'CAPTURE.json', manifest)
    dump(args.out / 'PRIVACY.json', privacy_rows)
    pages = []
    for layer, unit in jobs:
        left, right = analyzed[PAIRINGS[layer], unit], analyzed[layer, unit]
        keys = ([args.page] if args.page else list(dict.fromkeys(
                [m['page'] for m in left['markers']] + [m['page'] for m in right['markers']])))
        for page in keys:
            pair = pair_page(left, right, page)
            pages.append(pair)
            if args.source_segments:
                folder = args.out / 'pages' / layer / unit / page
                folder.mkdir(parents=True)
                for role, item in [('french', left), ('translation', right)]:
                    loc = pair[role + '_segment']
                    if loc['status'] == 'literal_marker_segment':
                        fragment = item['data'][loc['byte_start']:loc['byte_end_exclusive']]
                        assert sha(fragment) == loc['sha256']
                        (folder / (role + '.tex')).write_bytes(fragment)
                dump(folder / 'PAIR.json', pair)
                for stream in ['math', 'references', 'reference_shapes']:
                    payload = {role: page_records(item, page, stream)
                               for role, item in [('french', left), ('translation', right)]}
                    dump(folder / (stream.upper() + '.json'), payload)
    filtered = lambda item, stream: [r for r in item[stream]
                                    if not args.page or r['page'] == args.page]
    math = [r for item in analyzed.values() for r in filtered(item, 'math')]
    refs = [r for item in analyzed.values() for r in filtered(item, 'references')]
    shapes = [r for item in analyzed.values() for r in filtered(item, 'reference_shapes')]
    suffix = '.jsonl.gz' if args.compact else '.jsonl'
    for name, rows in [('MATH_REGIONS', math), ('REFERENCES', refs),
                       ('REFERENCE_SHAPED_CANDIDATES', shapes), ('PAGE_PAIRS', pages)]:
        jsonl(args.out / (name + suffix), rows, args.compact)
    flat = [{k: v for k, v in page.items() if k not in
             ['candidate_alignments', 'french_segment', 'translation_segment']}
            for page in pages]
    fields = ['translation', 'french_layer', 'unit', 'page', 'page_key', 'status',
              'french_file', 'translation_file', 'french_sha256', 'translation_sha256',
              'french_math_all', 'translation_math_all', 'french_math', 'translation_math',
              'french_references', 'translation_references',
              'french_reference_shapes', 'translation_reference_shapes']
    tsv(args.out / 'PAGE_COUNTS.tsv', flat, fields)
    blocks = [dict(translation=p['translation'], french_layer=p['french_layer'],
                   unit=p['unit'], page=p['page'], stream=stream, **row)
              for p in pages for stream, rows in p['candidate_alignments'].items() for row in rows]
    jsonl(args.out / ('CANDIDATE_ALIGNMENT' + suffix), blocks, args.compact)
    issue_rows = [dict(layer=item['layer'], unit=item['unit'], file=item['file'], **issue)
                  for item in analyzed.values() for issue in item['issues']]
    dump(args.out / 'LEXICAL_ISSUES.json', issue_rows)
    unmarked = [r['id'] for r in math if not r['page'] or r['cross_marker'] or r['ambiguous']]
    checks = {'all_math_slices_match_hashes': all(sha(r['raw_text'].encode()) == r['raw_sha256']
                                               for r in math),
              'all_reference_slices_match_hashes': all(sha(r['raw_text'].encode()) == r['raw_sha256']
                                                    for r in refs + shapes),
              'unique_math_ids': len({r['id'] for r in math}) == len(math),
              'problematic_math_ids': unmarked,
              'token_boundary_fixture': normalized_digest(b'\\to P') != normalized_digest(b'\\toP'),
              'whitespace_fixture': normalized_digest(b'a + b') == normalized_digest(b'a+b'),
              'comment_fixture': normalized_digest(b'a%test\n+b') == normalized_digest(b'a+b')}
    dump(args.out / 'EXACTNESS_CHECKS.json', checks)
    summary = {'completed_utc': utc(), 'selected_files': len(captured),
               'translation_unit_pairs': len(jobs), 'page_pairs': len(pages),
               'math_regions': len(math), 'outermost_math_regions': sum(not r['parent_id'] for r in math),
               'nested_math_regions': sum(bool(r['parent_id']) for r in math),
               'explicit_reference_commands': len(refs), 'reference_shaped_candidates': len(shapes),
               'lexical_issues': len(issue_rows), 'page_status_counts': dict(Counter(p['status'] for p in pages)),
               'alignment_status_counts': {s: dict(Counter(r['status'] for r in blocks if r['stream'] == s))
                                           for s in ['math', 'references', 'reference_shapes']},
               'privacy_blockers': 0, 'tex_control_lookalikes_preserved': len(privacy_rows),
               'input_capture': manifest, 'exactness_checks': checks,
               'semantic_adjudication_performed': False, 'live_sources_modified': False}
    dump(args.out / 'SUMMARY.json', summary)
    print(json.dumps({k: v for k, v in summary.items() if k not in ['input_capture', 'exactness_checks']}))
    return 2 if issue_rows or unmarked or not all(v for k, v in checks.items()
                                                if isinstance(v, bool)) else 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, FileNotFoundError) as error:
        print(type(error).__name__ + ': ' + str(error), file=sys.stderr)
        raise SystemExit(2)
