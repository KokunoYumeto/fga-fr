"""Exact-byte footnote inventory; no wording or validity classification.

Reads only a frozen input bundle. Bodies are stored once by SHA-256; counterpart
links require actual byte equality, with no whitespace or TeX normalization.
"""
import argparse
from bisect import bisect_right
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path('FGA_CHECK/scripts').resolve()))
import source_segments as source

PRIVATE = [
    ('email_pattern', re.compile(rb'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')),
    ('local_absolute_path_pattern', re.compile(rb'/(?:workspace|home|root|tmp|Users|opt)/[^\s{}<>]*')),
    ('drive_path_or_tex_control_lookalike', re.compile(rb'[A-Za-z]:[\\/][^\s{}<>]*')),
]
# Exact body and regex-match hashes pin a lexically verified false path match:
# a colon followed by one overline control word inside balanced inline math,
# outside text-command groups, with zero parser issues. No prose was interpreted.
VERIFIED_TEX_LOOKALIKE = (
    'b4daa570aa36244be6f33ce5487b0b5ac069293c5d834457738baa30382d7fd6',
    '41fc020699c008c7ebe312f396e89d34789b770c8bbe48f6f8ec2ee2600dbc12',
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def tsv(path, rows, fields):
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter='\t', lineterminator='\n', extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v
                             for k, v in row.items()})


def location(data, marks, start, end):
    index = bisect_right([m['byte_start'] for m in marks], start) - 1
    marker = marks[max(index, 0)] if marks else None
    crossed = [m['page'] for m in marks if start < m['byte_start'] < end]
    return {'line_start': source.line_number(data, start), 'line_end': source.line_end(data, end),
            'byte_start': start, 'byte_end_exclusive': end,
            'page': marker['page'] if marker else '',
            'anchor_rule': ('preceding_literal_marker' if index >= 0 else
                            'following_marker_for_prefix' if marker else 'no_literal_marker'),
            'page_occurrence': marker['occurrence'] if marker else '',
            'cross_marker': bool(crossed), 'crossed_pages': crossed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--frozen', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        parser.error('Choose a new output directory')
    if args.out.resolve() == args.frozen.resolve() or args.frozen.resolve() in args.out.resolve().parents:
        parser.error('Output must be outside the frozen input directory')
    manifest = json.loads((args.frozen / 'CAPTURE.json').read_text())
    records, markers, issues, files, bodies = [], [], [], [], {}
    counts = Counter()
    definitions = {'newcommand', 'renewcommand', 'providecommand', 'DeclareRobustCommand',
                   'def', 'gdef', 'edef', 'xdef'}
    for item in manifest['files']:
        data = (args.frozen / item['frozen_path']).read_bytes()
        assert len(data) == item['bytes'] and sha(data) == item['sha256']
        masked = source.mask_comments(data)
        marks = source.markers(data)
        declared = {source.source_path(item['layer'], u): u for u in source.expected_units(item['layer'])}
        unit = declared.get(item['relative_file'], '')
        common = {'version': item['version'], 'layer': item['layer'],
                  'relative_file': item['relative_file'], 'unit': unit,
                  'file_class': 'declared_content_unit' if unit else 'other_tex',
                  'path': (('FGA_CHECK/sources/' if item['version'] == 'current' else 'inputs/original_sources/')
                           + item['layer'] + '/' + item['relative_file']),
                  'file_sha256': item['sha256']}
        starts = len(records)
        for token in source.CONTROL.finditer(masked):
            name = token[1].decode('ascii', errors='replace')
            if 'footnote' in name.lower() or name == 'thanks':
                counts[item['version'], name] += 1
            if name not in {'footnote', 'footnotetext', 'footnotemark', 'thanks'}:
                continue
            cursor = source.skip_space(masked, token.end())
            starred = masked[cursor:cursor + 1] == b'*'
            cursor += int(starred)
            optional = source.group(masked, cursor, 91, 93)
            if optional:
                cursor = optional[1]
            if name == 'footnotemark':
                end = optional[1] if optional else token.end()
                markers.append(dict(common, macro=name, starred=starred,
                                    optional_argument_sha256=sha(data[optional[0] + 1:optional[1] - 1]) if optional else '',
                                    **location(data, marks, token.start(), end)))
                continue
            body = source.group(masked, cursor)
            if body is None:
                issues.append(dict(common, macro=name, line=source.line_number(data, token.start()),
                                   issue='no_balanced_literal_braced_argument'))
                continue
            a, b = body[0] + 1, body[1] - 1
            raw = data[a:b]
            digest = sha(raw)
            assert digest not in bodies or bodies[digest] == raw
            bodies[digest] = raw
            prefix = 'FNC' if item['version'] == 'current' else 'FNO'
            row = dict(common, id=prefix + f'{sum(r["version"] == item["version"] for r in records) + 1:05d}',
                       macro=name, starred=starred, ordinal_in_file=len(records) - starts + 1,
                       body_byte_start=a, body_byte_end_exclusive=b,
                       body_sha256=digest, body_bytes=len(raw),
                       body_line_start=source.line_number(data, a), body_line_end=source.line_end(data, b),
                       invocation_sha256=sha(data[token.start():body[1]]),
                       optional_argument_sha256=sha(data[optional[0] + 1:optional[1] - 1]) if optional else '',
                       contains_literal_parameter_token=bool(re.search(rb'(?<!\\)#[1-9]', masked[a:b])),
                       **location(data, marks, token.start(), body[1]))
            row['page_key'] = unit + '-' + row['page'] if unit and row['page'] else ''
            row['parent_footnote_id'] = next((r['id'] for r in reversed(records[starts:])
                                            if r['body_byte_start'] <= token.start() < r['body_byte_end_exclusive']), '')
            records.append(row)
        files.append(dict(common, bytes=len(data), literal_markers=len(marks),
                          footnote_contents=len(records) - starts))
    by_body = defaultdict(list)
    for row in records:
        by_body[row['version'], row['layer'], row['body_sha256']].append(row)
    for row in records:
        version = 'original' if row['version'] == 'current' else 'current'
        candidates = by_body[version, row['layer'], row['body_sha256']]
        # Hash collision was excluded above using actual body bytes.
        same = [r for r in candidates if r['relative_file'] == row['relative_file']]
        other = [r for r in candidates if r['relative_file'] != row['relative_file']]
        row.update(exact_body_counterparts_same_file=[r['id'] for r in same],
                   exact_body_counterparts_other_file_same_layer=[r['id'] for r in other],
                   exact_body_counterparts_same_file_and_page=[r['id'] for r in same if r['page'] == row['page']],
                   exact_invocation_counterparts_same_file=[r['id'] for r in same if r['invocation_sha256'] == row['invocation_sha256']],
                   counterpart_status=('exact_body_in_other_version_same_file' if same else
                                       'exact_body_in_other_version_other_file_same_layer' if other else
                                       'no_exact_body_in_other_version_same_layer'))
    payloads, withheld, lookalikes = [], [], []
    for digest, raw in sorted(bodies.items()):
        hits = []
        for name, pattern in PRIVATE:
            for match in pattern.finditer(raw):
                if (name == 'drive_path_or_tex_control_lookalike' and
                        (digest, sha(match.group())) == VERIFIED_TEX_LOOKALIKE):
                    lookalikes.append({'body_sha256': digest, 'match_sha256': sha(match.group()),
                                       'byte_start': match.start(), 'byte_end_exclusive': match.end(),
                                       'control': 'overline', 'basis': 'verified_balanced_inline_math_control_sequence'})
                else:
                    hits.append({'kind': name, 'byte_start': match.start(), 'byte_end_exclusive': match.end()})
        if hits:
            value = None
            withheld.append({'body_sha256': digest, 'patterns': hits})
        else:
            value = raw.decode('utf-8')
            assert value.encode('utf-8') == raw
        payloads.append({'body_sha256': digest, 'bytes': len(raw), 'exact_body_utf8': value,
                         'body_withheld_for_sanitization': bool(hits)})
    args.out.mkdir(parents=True)
    dump(args.out / 'CAPTURE.json', manifest)
    dump(args.out / 'CONTENTS.json', payloads)
    dump(args.out / 'EXTRACTION_ISSUES.json', issues)
    dump(args.out / 'SANITIZATION.json', withheld)
    dump(args.out / 'PRIVACY_TEX_LOOKALIKES.json', lookalikes)
    tsv(args.out / 'FOOTNOTES.tsv', records, list(records[0]))
    tsv(args.out / 'MARKER_ONLY_CALLS.tsv', markers, list(markers[0]) if markers else ['version', 'layer', 'path'])
    tsv(args.out / 'FILES.tsv', files, list(files[0]))
    tsv(args.out / 'COMMAND_COUNTS.tsv', [{'version': v, 'macro': n, 'count': c} for (v, n), c in sorted(counts.items())],
        ['version', 'macro', 'count'])
    summary = {'completed_utc': datetime.now(timezone.utc).isoformat(),
               'source_capture_started_utc': manifest['started_utc'],
               'source_capture_completed_utc': manifest['completed_utc'],
               'files_by_version': dict(Counter(r['version'] for r in files)),
               'footnotes_by_version': dict(Counter(r['version'] for r in records)),
               'unique_exact_bodies': len(payloads), 'withheld_body_count': len(withheld),
               'verified_tex_control_lookalikes_preserved': len(lookalikes),
               'marker_only_by_version': dict(Counter(r['version'] for r in markers)),
               'status_counts': {v: dict(Counter(r['counterpart_status'] for r in records if r['version'] == v))
                                 for v in ['current', 'original']},
               'extraction_issues': len(issues), 'cross_marker_footnotes': sum(r['cross_marker'] for r in records),
               'parameter_template_candidates': sum(r['contains_literal_parameter_token'] for r in records),
               'all_frozen_input_hashes_match': True,
               'original_manifest_sha256': sha((args.frozen / 'ORIGINAL_MANIFEST.tsv').read_bytes()),
               'script_sha256': sha(Path(__file__).read_bytes()),
               'source_marker_helper_sha256': sha(Path(source.__file__).read_bytes()),
               'comparison_policy': 'Exact content bytes only; corresponding version and translation layer. Same file/page and exact whole-invocation matches are separate locators. No text normalization or validity classification.',
               'current_sources_may_have_evolved_after_capture': True,
               'live_source_ledger_record_progress_mutations': 0,
               'source_prose_read_or_interpreted': False}
    dump(args.out / 'SUMMARY.json', summary)
    print(json.dumps(summary, indent=2))
    return 2 if issues else 0


if __name__ == '__main__':
    raise SystemExit(main())
