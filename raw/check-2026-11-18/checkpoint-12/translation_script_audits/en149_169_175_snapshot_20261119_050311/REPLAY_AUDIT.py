"""Replay seven approved scripts in an isolated disposable tree; metadata only.

No live source, ledger, record, rights or progress file is opened for mutation.
The simulation is not a reading, approval, build or claim of semantic validity.
"""
import csv
from collections import Counter
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime, timezone
import difflib
import hashlib
import importlib
import io
import json
from pathlib import Path
import re
import runpy
import shutil
import sys
import traceback

sys.dont_write_bytecode = True
BASE = Path('tmp/en149_mechanical_audit_169_175')
FROZEN = BASE / 'frozen'
REPLAY = BASE / 'replay'
OUT = BASE / 'report'
ORIGINAL = Path('tmp/math_expression_inventory_02/sources/en/en/149.tex')
BASELINE_LEDGER = Path('tmp/frozen_build_inputs/read_through_errata_307/CORRECTIONS.tsv')
EN = 'sources/en/en/149.tex'
FR = 'sources/fr/fr/149.tex'
PAGES = range(169, 176)


def sha(value):
    return hashlib.sha256(value).hexdigest()


def rowhash(row):
    return sha(json.dumps(row, ensure_ascii=False, separators=(',', ':')).encode())


def rows(path):
    with path.open(newline='') as f:
        return list(csv.reader(f, delimiter='\t'))


def write_tsv(path, records, fields):
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n', extrasaction='ignore')
        writer.writeheader()
        for row in records:
            writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v
                             for k, v in row.items()})


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


assert not REPLAY.exists() and not OUT.exists()
REPLAY.mkdir(parents=True)
OUT.mkdir()
shutil.copytree(FROZEN / 'scripts', REPLAY / 'scripts')
for name, data in [(EN, ORIGINAL.read_bytes()), (FR, (FROZEN / FR).read_bytes())]:
    path = REPLAY / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
for name in ['CORRECTIONS.tsv', 'CHECK_EVENTS.tsv']:
    with (REPLAY / name).open('w', newline='') as f:
        csv.writer(f, delimiter='\t').writerow(rows(FROZEN / name)[0])
for name in ['CHECK_RECORD.md', 'progress.log']:
    (REPLAY / name).write_text('')

initial_hashes = {p.relative_to(REPLAY).as_posix(): sha(p.read_bytes())
                  for p in REPLAY.rglob('*') if p.is_file()}
sys.path.insert(0, str((REPLAY / 'scripts').resolve()))
audit = importlib.import_module('audit_utils')
assert audit.ROOT == REPLAY.resolve()
# Suppress simulation timestamps; no correction row in this scope uses them.
audit.utc = lambda: 'SIMULATED_METADATA_ONLY'
edits = importlib.import_module('translation_edits')
assert edits.ROOT == REPLAY.resolve()
lexer = importlib.import_module('translation_math_lexer')
original_replace = audit.replace
original_align = edits.align_math
operations, alignments, execution = [], [], []
active_page = None


def audited_replace(*args, **kwargs):
    before_rows = len(rows(REPLAY / 'CORRECTIONS.tsv')) - 1
    before = (REPLAY / EN).read_bytes()
    record = {'script_page': active_page, 'operation': len(operations) + 1,
              'kind': 'explicit_replace', 'file': args[0], 'printed_page': args[4],
              'old_sha256': sha(args[1].encode()), 'new_sha256': sha(args[2].encode()),
              'old_bytes': len(args[1].encode()), 'new_bytes': len(args[2].encode()),
              'requested_occurrences': kwargs.get('count', 1),
              'source_before_sha256': sha(before)}
    try:
        result = original_replace(*args, **kwargs)
        record['completed'] = True
        return result
    except Exception as error:
        record['completed'] = False
        record['exception_type'] = type(error).__name__
        raise
    finally:
        record['source_after_sha256'] = sha((REPLAY / EN).read_bytes())
        record['appended_rows'] = len(rows(REPLAY / 'CORRECTIONS.tsv')) - 1 - before_rows
        operations.append(record)


def audited_align(rel, layer, unit, page, pairs, expected, printed=False, localized=None):
    pairs = list(pairs)
    current, _, _ = audit.page_text(rel, page)
    french, _, _ = audit.page_text(FR, page)
    tb, ts = edits.math_ranges(current)
    fb, fs = edits.math_ranges(french)
    before_rows = len(rows(REPLAY / 'CORRECTIONS.tsv')) - 1
    record = {'script_page': active_page, 'page': page,
              'target_outer_spans_before': len(ts), 'french_outer_spans': len(fs),
              'expected_target': expected[0], 'expected_french': expected[1],
              'pair_count': len(pairs),
              'duplicate_target_indices': len(pairs) - len({a for a, b in pairs}),
              'duplicate_french_indices': len(pairs) - len({b for a, b in pairs}),
              'all_indices_in_range': all(0 <= a < len(ts) and 0 <= b < len(fs) for a, b in pairs),
              'pairs_sha256': rowhash(pairs),
              'target_page_before_sha256': sha(tb), 'french_page_sha256': sha(fb),
              'localized_target_indices': sorted((localized or {}).keys())}
    try:
        value = original_align(rel, layer, unit, page, pairs, expected, printed, localized)
        record['completed'] = True
        record['returned_row_count'] = value
        return value
    except Exception as error:
        record['completed'] = False
        record['exception_type'] = type(error).__name__
        raise
    finally:
        record['appended_rows'] = len(rows(REPLAY / 'CORRECTIONS.tsv')) - 1 - before_rows
        alignments.append(record)


audit.replace = audited_replace
edits.align_math = audited_align
stdout = io.StringIO()
for page in PAGES:
    active_page = page
    script = REPLAY / 'scripts' / f'apply_en_149_{page}.py'
    before = len(rows(REPLAY / 'CORRECTIONS.tsv')) - 1
    record = {'page': page, 'script': 'scripts/' + script.name,
              'script_sha256': sha(script.read_bytes()), 'completed': False}
    try:
        with redirect_stdout(stdout), redirect_stderr(stdout):
            runpy.run_path(str(script), run_name='__main__')
        record['completed'] = True
    except Exception as error:
        record['exception_type'] = type(error).__name__
        record['message_sha256'] = sha(str(error).encode())
        record['trace_locations'] = [dict(file=Path(frame.filename).name, line=frame.lineno,
                                          function=frame.name)
                                     for frame in traceback.extract_tb(error.__traceback__)]
    record['appended_rows'] = len(rows(REPLAY / 'CORRECTIONS.tsv')) - 1 - before
    execution.append(record)
    if not record['completed']:
        break
(BASE / 'replay_stdout.txt').write_text(stdout.getvalue())

# Byte-based page slicing independent of the editing helper's text normalization.
def segments(data):
    matches = list(re.finditer(rb'\\src\{([0-9]+)\}', data))
    return {int(m[1]): (m.start(), matches[n + 1].start() if n + 1 < len(matches) else len(data))
            for n, m in enumerate(matches)}


initial = ORIGINAL.read_bytes()
actual = (FROZEN / EN).read_bytes()
simulated = (REPLAY / EN).read_bytes()
initial_ranges, actual_ranges, replay_ranges = map(segments, [initial, actual, simulated])
page_checks = []
for page in PAGES:
    record = {'page': page, 'all_markers_present': all(page in x for x in [initial_ranges, actual_ranges, replay_ranges])}
    if record['all_markers_present']:
        ia, ib = initial_ranges[page]
        aa, ab = actual_ranges[page]
        ra, rb = replay_ranges[page]
        target = actual[aa:ab]
        replay = simulated[ra:rb]
        parsed = lexer.scan_math(target)
        record.update({'initial_sha256': sha(initial[ia:ib]), 'frozen_current_sha256': sha(target),
                       'replayed_sha256': sha(replay), 'current_equals_replay': target == replay,
                       'source_line_start': actual.count(b'\n', 0, aa) + 1,
                       'source_line_end': actual.count(b'\n', 0, ab),
                       'math_spans': len(parsed['spans']),
                       'outer_math_spans': sum(s['parent_span_index'] is None for s in parsed['spans']),
                       'lexical_issue_count': len(parsed['issues'])})
    page_checks.append(record)

expected_rows = rows(REPLAY / 'CORRECTIONS.tsv')[1:]
baseline_rows = rows(BASELINE_LEDGER)[1:]
current_rows = rows(FROZEN / 'CORRECTIONS.tsv')[1:]
header = rows(FROZEN / 'CORRECTIONS.tsv')[0]
index = {name: n for n, name in enumerate(header)}
selected_rows = [(i + 1, row) for i, row in enumerate(current_rows)
                 if i >= len(baseline_rows) and row[index['file']] == EN
                 and row[index['layer']] == 'English'
                 and row[index['printed_page']] in {f'149-{p}' for p in PAGES}]
expected_hashes = [rowhash(row) for row in expected_rows]
actual_hashes = [rowhash(row) for _, row in selected_rows]
row_checks = []
for n, row in enumerate(expected_rows):
    matches = [f'C{num:06d}' for num, candidate in selected_rows if candidate == row]
    row_checks.append({'replay_row': f'R{n + 1:06d}', 'row_sha256': rowhash(row),
                       'printed_page': row[index['printed_page']], 'kind': row[index['kind']],
                       'exact_live_candidates': matches, 'exact_match_count': len(matches)})
row_deltas = [{'operation': op, 'expected_row_start': a + 1, 'expected_row_end': b,
               'actual_row_ids': [f'C{selected_rows[i][0]:06d}' for i in range(c, d)],
               'expected_count': b - a, 'actual_count': d - c}
              for op, a, b, c, d in difflib.SequenceMatcher(None, expected_hashes, actual_hashes,
                                                           autojunk=False).get_opcodes() if op != 'equal']
parsed_current = lexer.scan_math(actual)
mask_initial, _ = lexer.mask_comments(initial)
mask_fr, _ = lexer.mask_comments((FROZEN / FR).read_bytes())
known_controls = {m[1] for data in [mask_initial, mask_fr] for m in lexer.CONTROL.finditer(data)}
novel = []
for page in PAGES:
    if page not in actual_ranges:
        continue
    a, b = actual_ranges[page]
    masked, _ = lexer.mask_comments(actual[a:b])
    for match in lexer.CONTROL.finditer(masked):
        if match[1] not in known_controls:
            novel.append({'page': page, 'control': match[1].decode('ascii', errors='replace'),
                          'source_line': actual.count(b'\n', 0, a + match.start()) + 1,
                          'byte_start': a + match.start()})

allowed_writes = {EN, 'CORRECTIONS.tsv', 'CHECK_RECORD.md', 'CHECK_EVENTS.tsv', 'progress.log'}
after_hashes = {p.relative_to(REPLAY).as_posix(): sha(p.read_bytes()) for p in REPLAY.rglob('*') if p.is_file()}
unexpected = [p for p in set(initial_hashes) | set(after_hashes)
              if initial_hashes.get(p) != after_hashes.get(p) and p not in allowed_writes]
prefix_preserved = initial[:initial_ranges[169][0]] == simulated[:replay_ranges[169][0]]
suffix_preserved = initial[initial_ranges[175][1]:] == simulated[replay_ranges[175][1]:]
input_checks = []
for filename in ['CAPTURE.json', 'EXTRA_CAPTURE.json']:
    manifest = json.loads((FROZEN / filename).read_text())
    for name, info in manifest['files'].items():
        input_checks.append({'file': name, 'sha256': info['sha256'],
                             'unchanged': sha((FROZEN / name).read_bytes()) == info['sha256']})
summary = {'completed_utc': datetime.now(timezone.utc).isoformat(),
           'frozen_capture': json.loads((FROZEN / 'CAPTURE.json').read_text()),
           'script_count': len(execution), 'all_scripts_replayed_without_exception': all(x['completed'] for x in execution) and len(execution) == 7,
           'all_selected_pages_equal_replay': all(x.get('current_equals_replay') for x in page_checks),
           'replay_generated_ledger_rows': len(expected_rows), 'selected_actual_appended_rows': len(selected_rows),
           'all_generated_rows_equal_actual_in_order': expected_hashes == actual_hashes,
           'selected_actual_exact_duplicate_rows': sum(v - 1 for v in Counter(actual_hashes).values()),
           'all_math_pair_indices_unique_and_in_range': all(x['all_indices_in_range'] and not x['duplicate_target_indices'] for x in alignments),
           'all_math_expected_counts_match': all(x['target_outer_spans_before'] == x['expected_target'] and x['french_outer_spans'] == x['expected_french'] for x in alignments),
           'initial_to_replay_page_marker_sequence_equal': list(initial_ranges) == list(replay_ranges),
           'current_to_replay_page_marker_sequence_equal': list(actual_ranges) == list(replay_ranges),
           'replay_unit_prefix_unchanged': prefix_preserved, 'replay_after_page175_unchanged': suffix_preserved,
           'frozen_french_source_unchanged_in_replay': (REPLAY / FR).read_bytes() == (FROZEN / FR).read_bytes(),
           'full_current_en_source_equals_replay': actual == simulated,
           'baseline_ledger_exact_byte_prefix_preserved': (FROZEN / 'CORRECTIONS.tsv').read_bytes().startswith(BASELINE_LEDGER.read_bytes()),
           'baseline_ledger_rows': len(baseline_rows), 'whole_current_en_lexical_issues': len(parsed_current['issues']),
           'new_controls_absent_from_initial_en_and_current_fr': len(novel),
           'unexpected_simulation_writes': unexpected, 'all_frozen_inputs_unchanged': all(x['unchanged'] for x in input_checks),
           'live_mutations': 0, 'content_math_or_scan_adjudication': False,
           'build_performed': False, 'row_delta_blocks': row_deltas}
dump(OUT / 'SUMMARY.json', summary)
dump(OUT / 'SCRIPT_EXECUTION.json', execution)
dump(OUT / 'EXPLICIT_OPERATIONS.json', operations)
dump(OUT / 'MATH_PAIR_COUNTS.json', alignments)
dump(OUT / 'LEDGER_DELTAS.json', row_deltas)
dump(OUT / 'LEXICAL_ISSUES.json', parsed_current['issues'])
write_tsv(OUT / 'PAGE_BYTE_CHECKS.tsv', page_checks, list(page_checks[0]))
write_tsv(OUT / 'LEDGER_ROW_CHECKS.tsv', row_checks, list(row_checks[0]) if row_checks else ['replay_row'])
write_tsv(OUT / 'NEW_CONTROL_CANDIDATES.tsv', novel, ['page', 'control', 'source_line', 'byte_start'])
write_tsv(OUT / 'FROZEN_INPUT_CHECKS.tsv', input_checks, ['file', 'sha256', 'unchanged'])
print(json.dumps({k: v for k, v in summary.items() if k != 'frozen_capture'}, indent=2))
