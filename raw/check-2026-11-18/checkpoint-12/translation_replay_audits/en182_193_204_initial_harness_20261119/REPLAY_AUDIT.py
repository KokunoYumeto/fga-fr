"""Frozen EN182 pages 193–204 replay; byte equality and structural metadata only.

The copied edit scripts and helpers remain byte-identical to their capture.
Only disposable replay files are mutated. Output contains no source or ledger
payload. This verifies execution/reconstruction, not substantive correctness.
"""
import ast
from collections import Counter, defaultdict
from contextlib import redirect_stdout, redirect_stderr
import csv
from datetime import datetime, timezone
import difflib
import hashlib
import importlib
import inspect
import io
import json
import os
from pathlib import Path
import re
import runpy
import shutil
import sys
import traceback

sys.dont_write_bytecode = True
WORK = Path(__file__).resolve().parents[2]
BASE = WORK / 'tmp/en182_replay_193_204_20261119'
FROZEN = BASE / 'frozen'
REPLAY = BASE / 'isolated'
OUT = WORK / 'FGA_CHECK/translation_replay_audits/en182_193_204_20261119'
ORIGINAL = BASE / 'baseline_original/182.tex'
ORIGINAL_CHECK = BASE / 'baseline_original/182_copy.tex'
BASELINE = BASE / 'baseline_original/CORRECTIONS_prefix.tsv'
EN = 'sources/en/en/182.tex'
FR = 'sources/fr/fr/182.tex'
PAGES = list(range(193, 205))
SCRIPT_NAMES = [f'apply_en_182_{p}.py' for p in PAGES]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def rowhash(row):
    return sha(json.dumps(row, ensure_ascii=False, separators=(',', ':')).encode())


def read_rows(path):
    with path.open(newline='', encoding='utf-8') as stream:
        return list(csv.reader(stream, delimiter='\t', strict=True))


def dump(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def tsv(name, data, fields):
    with (OUT / name).open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fields, delimiter='\t', lineterminator='\n', extrasaction='ignore')
        writer.writeheader()
        for row in data:
            writer.writerow({k: json.dumps(v, ensure_ascii=False, separators=(',', ':'))
                             if isinstance(v, (list, dict)) else v for k, v in row.items()})


def local_path(path):
    try:
        return Path(path).resolve().relative_to(WORK).as_posix()
    except (ValueError, TypeError):
        return Path(path).name


assert not REPLAY.exists() and not OUT.exists(), 'Isolated replay/output already exists'
REPLAY.mkdir(parents=True)
OUT.mkdir(parents=True)
manifest_bytes = (FROZEN / 'SNAPSHOT.json').read_bytes()
manifest = json.loads(manifest_bytes)
input_checks = []
for item in manifest['files']:
    name = item['path']
    assert not Path(name).is_absolute() and '..' not in Path(name).parts
    data = (FROZEN / name).read_bytes()
    record = {'file': name, 'bytes': len(data), 'sha256': sha(data),
              'manifest_bytes_match': len(data) == item['bytes'],
              'manifest_sha256_match': sha(data) == item['sha256']}
    input_checks.append(record)
    assert record['manifest_bytes_match'] and record['manifest_sha256_match'], name
    target = REPLAY / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
assert len(input_checks) == len(manifest['files'])
original = ORIGINAL.read_bytes()
original_check = ORIGINAL_CHECK.read_bytes()
assert original == original_check
baseline_bytes = BASELINE.read_bytes()
actual_ledger_bytes = (FROZEN / 'CORRECTIONS.tsv').read_bytes()
baseline_rows = read_rows(BASELINE)
actual_ledger = read_rows(FROZEN / 'CORRECTIONS.tsv')
actual_events = read_rows(FROZEN / 'CHECK_EVENTS.tsv')
baseline_count = len(baseline_rows) - 1
ledger_header = actual_ledger[0]
fields = {k: n for n, k in enumerate(ledger_header)}
(REPLAY / EN).write_bytes(original)
for name in ['CORRECTIONS.tsv', 'CHECK_EVENTS.tsv']:
    with (REPLAY / name).open('w', newline='', encoding='utf-8') as stream:
        csv.writer(stream, delimiter='\t').writerow(read_rows(FROZEN / name)[0])
for name in ['CHECK_RECORD.md', 'progress.log']:
    (REPLAY / name).write_bytes(b'')
initial_hashes = {p.relative_to(REPLAY).as_posix(): sha(p.read_bytes())
                  for p in REPLAY.rglob('*') if p.is_file()}

# Enforce that scripts can only read/write inside the disposable tree.
execution_active = False
blocked_io = []


def io_guard(event, args):
    if not execution_active:
        return
    if event == 'open' and args and isinstance(args[0], (str, bytes, os.PathLike)):
        path = Path(os.fsdecode(args[0])).resolve()
        mode = args[1] or ''
        flags = args[2] or 0
        write = any(c in mode for c in 'wax+') or bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        if (write or path.is_relative_to(WORK)) and not path.is_relative_to(REPLAY):
            blocked_io.append({'event': event, 'file': path.name, 'write': write})
            raise PermissionError('Replay attempted I/O outside disposable tree')
    if event in {'subprocess.Popen', 'os.system', 'socket.connect', 'os.remove', 'os.rename', 'os.rmdir'}:
        blocked_io.append({'event': event})
        raise PermissionError('Replay attempted unsupported external operation')


sys.addaudithook(io_guard)
sys.path.insert(0, str(REPLAY / 'scripts'))
audit = importlib.import_module('audit_utils')
assert audit.ROOT == REPLAY.resolve()
audit.utc = lambda: 'SIMULATED_METADATA_ONLY'
edits = importlib.import_module('translation_edits')
counts_module = importlib.import_module('update_record_counts')
lexer = importlib.import_module('translation_math_lexer')
assert edits.ROOT == REPLAY.resolve() and counts_module.ROOT == REPLAY.resolve()

operations, alignments, pair_checks, calls, executions = [], [], [], [], []
active_script = None
executed_lines = defaultdict(set)
script_paths = {(REPLAY / 'scripts' / name).resolve(): name for name in SCRIPT_NAMES}


def trace_lines(frame, event, arg):
    path = Path(frame.f_code.co_filename).resolve()
    if path not in script_paths:
        return None
    if event == 'line':
        executed_lines[script_paths[path]].add(frame.f_lineno)
    return trace_lines


def caller_sites():
    result = []
    frame = inspect.currentframe().f_back
    while frame:
        path = Path(frame.f_code.co_filename).resolve()
        if path in script_paths:
            result.append({'script': script_paths[path], 'line': frame.f_lineno,
                           'function': frame.f_code.co_name})
        frame = frame.f_back
    return result


def mark_call(function):
    call = {'sequence': len(calls) + 1, 'script': active_script, 'function': function,
            'sites': caller_sites()}
    calls.append(call)
    return call


def row_count():
    return len(read_rows(REPLAY / 'CORRECTIONS.tsv')) - 1


original_replace = audit.replace


def audited_replace(*args, **kwargs):
    binding = inspect.signature(original_replace).bind(*args, **kwargs)
    binding.apply_defaults()
    b = binding.arguments
    call = mark_call('replace')
    before_rows = row_count()
    before = (REPLAY / b['rel']).read_bytes()
    text = audit.read(b['rel'])
    lo, hi = 0, len(text)
    pm = re.fullmatch(r'(?:e?\d+)-(\d+)', b['page'])
    # Match the frozen helper's literal page-range convention exactly.
    if pm and not b['full']:
        m = re.search(r'\\src\{' + pm.group(1) + r'\}', text)
        if m:
            lo = m.start()
            nxt = re.search(r'\\src\{\d+\}', text[m.end():])
            if nxt:
                hi = m.end() + nxt.start()
    segment = text[lo:hi]
    observed = segment.count(b['old'])
    predicted_text = text[:lo] + segment.replace(b['old'], b['new']) + text[hi:]
    predicted = predicted_text.replace('\n', '\r\n').encode() if b'\r\n' in before else predicted_text.encode()
    record = {'sequence': len(operations) + 1, 'call_sequence': call['sequence'],
              'script': active_script, 'file': b['rel'], 'printed_page': b['page'],
              'old_sha256': sha(b['old'].encode()), 'new_sha256': sha(b['new'].encode()),
              'old_bytes': len(b['old'].encode()), 'new_bytes': len(b['new'].encode()),
              'requested_occurrences': b['count'], 'observed_occurrences_before': observed,
              'source_before_sha256': sha(before), 'full_file_scope': b['full'],
              'completed': False}
    try:
        value = original_replace(*args, **kwargs)
        record['completed'] = True
        return value
    except Exception as error:
        record['exception_type'] = type(error).__name__
        raise
    finally:
        after = (REPLAY / b['rel']).read_bytes()
        record.update(source_after_sha256=sha(after), appended_rows=row_count() - before_rows,
                      source_changed=before != after, independently_predicted_bytes_match=after == predicted)
        operations.append(record)


original_align = edits.align_math


def audited_align(rel, layer, unit, page, pairs, expected, printed=False, localized=None):
    mark_call('align_math')
    pairs = list(pairs)
    target, _, _, tb, ts = edits.page_math_ranges(rel, page)
    reference = f'sources/{"fr_printed" if printed else "fr"}/fr/{unit}.tex'
    french, _, _, fb, fs = edits.page_math_ranges(reference, page)
    before_rows = row_count()
    local = localized or {}
    records = []
    mutations = []
    for number, (ti, fi) in enumerate(pairs, 1):
        valid = 0 <= ti < len(ts) and 0 <= fi < len(fs)
        item = {'script': active_script, 'page': page, 'pair_ordinal': number,
                'target_index': ti, 'french_index': fi, 'indices_in_range': valid}
        if valid:
            t, f = ts[ti], fs[fi]
            old = tb[t['start']:t['end']]
            new = fb[f['start']:f['end']].decode()
            localization_count = 0
            for a, b in local.get(ti, []):
                assert a in new
                new = new.replace(a, b)
                localization_count += 1
            new = new.encode()
            item.update(old_sha256=sha(old), new_sha256=sha(new), byte_identical=old == new,
                        localized_replacement_count=localization_count)
            if old != new:
                mutations.append((t['start'], t['end'], new))
        records.append(item)
    predicted = tb
    for a, b, data in sorted(mutations, reverse=True):
        predicted = predicted[:a] + data + predicted[b:]
    record = {'script': active_script, 'page': page, 'pair_count': len(pairs),
              'target_outer_spans_before': len(ts), 'french_outer_spans': len(fs),
              'expected_target': expected[0], 'expected_french': expected[1],
              'duplicate_target_indices': len(pairs) - len({a for a, b in pairs}),
              'duplicate_french_indices': len(pairs) - len({b for a, b in pairs}),
              'all_indices_in_range': all(x['indices_in_range'] for x in records),
              'pairs_sha256': rowhash(pairs), 'nonidentical_pairs': len(mutations),
              'identical_pairs': sum(x.get('byte_identical', False) for x in records),
              'target_page_before_sha256': sha(tb), 'french_page_sha256': sha(fb),
              'completed': False}
    try:
        result = original_align(rel, layer, unit, page, pairs, expected, printed, localized)
        record.update(completed=True, returned_row_count=result)
        return result
    except Exception as error:
        record['exception_type'] = type(error).__name__
        raise
    finally:
        after = audit.page_text(rel, page)[0].encode()
        record.update(appended_rows=row_count() - before_rows,
                      independently_predicted_page_bytes_match=after == predicted)
        alignments.append(record)
        pair_checks.extend(records)


audit.replace = audited_replace
edits.align_math = audited_align


def plain_wrapper(function, original_function):
    def wrapped(*args, **kwargs):
        mark_call(function)
        return original_function(*args, **kwargs)
    return wrapped


for module, names in [(audit, ['event']),
                      (edits, ['start_unit', 'record_translation_page', 'finish_unit']),
                      (counts_module, ['update'])]:
    for name in names:
        setattr(module, name, plain_wrapper(name, getattr(module, name)))

stdout = io.StringIO()
for name in SCRIPT_NAMES:
    active_script = name
    script = REPLAY / 'scripts' / name
    before_rows = row_count()
    record = {'script': name, 'script_sha256': sha(script.read_bytes()),
              'execution_count': 1, 'source_before_sha256': sha((REPLAY / EN).read_bytes()),
              'completed': False}
    try:
        execution_active = True
        sys.settrace(trace_lines)
        with redirect_stdout(stdout), redirect_stderr(stdout):
            runpy.run_path(str(script), run_name='__main__')
        record['completed'] = True
    except Exception as error:
        execution_active = False
        sys.settrace(None)
        record.update(exception_type=type(error).__name__, message_sha256=sha(str(error).encode()),
                      trace_locations=[{'file': Path(f.filename).name, 'line': f.lineno, 'function': f.name}
                                       for f in traceback.extract_tb(error.__traceback__)])
    finally:
        execution_active = False
        sys.settrace(None)
    record.update(appended_rows=row_count() - before_rows,
                  source_after_sha256=sha((REPLAY / EN).read_bytes()))
    executions.append(record)
    dump('SCRIPT_EXECUTION.json', executions)
    if not record['completed']:
        break


def segments(data):
    matches = list(re.finditer(rb'\\src\{([0-9]+)\}', data))
    sequence = [int(m[1]) for m in matches]
    result = {int(m[1]): (m.start(), matches[i + 1].start() if i + 1 < len(matches) else len(data))
              for i, m in enumerate(matches)}
    return sequence, result


actual = (FROZEN / EN).read_bytes()
simulated = (REPLAY / EN).read_bytes()
initial_sequence, initial_ranges = segments(original)
actual_sequence, actual_ranges = segments(actual)
replay_sequence, replay_ranges = segments(simulated)
page_checks = []
for page in PAGES:
    record = {'page': page, 'all_markers_present': all(page in x for x in [initial_ranges, actual_ranges, replay_ranges])}
    if record['all_markers_present']:
        ia, ib = initial_ranges[page]
        aa, ab = actual_ranges[page]
        ra, rb = replay_ranges[page]
        record.update(initial_sha256=sha(original[ia:ib]), frozen_current_sha256=sha(actual[aa:ab]),
                      replayed_sha256=sha(simulated[ra:rb]), current_equals_replay=actual[aa:ab] == simulated[ra:rb],
                      source_line_start=actual.count(b'\n', 0, aa) + 1,
                      source_line_end=actual.count(b'\n', 0, ab))
    page_checks.append(record)

generated = read_rows(REPLAY / 'CORRECTIONS.tsv')[1:]
selected = [(i, row) for i, row in enumerate(actual_ledger[1:], 1)
            if i > baseline_count and row[fields['file']] == EN and row[fields['layer']] == 'English'
            and row[fields['printed_page']] in {f'182-{p}' for p in PAGES}]
all_en182_suffix = [(i, row) for i, row in enumerate(actual_ledger[1:], 1)
                   if i > baseline_count and row[fields['file']] == EN and row[fields['layer']] == 'English']
gen_hashes = [rowhash(r) for r in generated]
actual_hashes = [rowhash(r) for _, r in selected]
row_checks = []
for i, row in enumerate(generated):
    matches = [f'C{number:06d}' for number, value in selected if value == row]
    row_checks.append({'replay_row': f'R{i+1:06d}', 'row_sha256': gen_hashes[i],
                       'printed_page': row[fields['printed_page']], 'kind': row[fields['kind']],
                       'exact_frozen_row_ids': matches, 'exact_match_count': len(matches),
                       'same_ordinal_exact': i < len(selected) and row == selected[i][1]})
row_deltas = [{'opcode': op, 'replay_start': a + 1, 'replay_end': b,
               'frozen_row_ids': [f'C{selected[j][0]:06d}' for j in range(c, d)]}
              for op, a, b, c, d in difflib.SequenceMatcher(None, gen_hashes, actual_hashes, autojunk=False).get_opcodes()
              if op != 'equal']
generated_body = (REPLAY / 'CORRECTIONS.tsv').read_bytes().split(b'\n', 1)[1]
# Preserve actual physical serialization while excluding unrelated interleaved rows.
ledger_line_offsets = [0] + [m.end() for m in re.finditer(b'\n', actual_ledger_bytes)]
physical_reader = csv.reader(io.StringIO(actual_ledger_bytes.decode('utf-8'), newline=''), delimiter='\t')
next(physical_reader)
previous_line = physical_reader.line_num
serialized_rows = {}
for number, values in enumerate(physical_reader, 1):
    serialized_rows[number] = actual_ledger_bytes[ledger_line_offsets[previous_line]:ledger_line_offsets[physical_reader.line_num]]
    previous_line = physical_reader.line_num
selected_serialized_bytes = b''.join(serialized_rows[number] for number, row in selected)
serialized_selected_exact = generated_body == selected_serialized_bytes
interleaved_rows = [{'row_id': f'C{number:06d}', 'file': row[fields['file']],
                     'printed_page': row[fields['printed_page']], 'row_sha256': rowhash(row)}
                    for number, row in enumerate(actual_ledger[1:], 1)
                    if selected[0][0] <= number <= selected[-1][0] and number not in {i for i, r in selected}]


mutation_names = {'replace', 'ch', 'change', 'align_math', 'event', 'start_unit',
                  'record_translation_page', 'finish_unit', 'update'}
static_checks = []
for name in SCRIPT_NAMES:
    tree = ast.parse((FROZEN / 'scripts' / name).read_bytes())
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in mutation_names:
            matches = [c['sequence'] for c in calls if any(s['script'] == name and node.lineno <= s['line'] <= node.end_lineno for s in c['sites'])]
            static_checks.append({'script': name, 'function': node.func.id, 'line': node.lineno,
                                  'end_line': node.end_lineno, 'execution_observed': bool(matches),
                                  'instrumented_call_sequences': matches,
                                  'line_event_observed': any(n in executed_lines[name] for n in range(node.lineno, node.end_lineno + 1))})

event_fields = {k: i for i, k in enumerate(actual_events[0])}
event_projection_columns = [i for i, name in enumerate(actual_events[0]) if name != 'date_utc']
project_event = lambda row: [row[i] for i in event_projection_columns]
generated_events = read_rows(REPLAY / 'CHECK_EVENTS.tsv')[1:]
generated_ids = [r[event_fields['id']] for r in generated_events]
id_prefix = os.path.commonprefix(generated_ids)
actual_selected_events = [(i, row) for i, row in enumerate(actual_events[1:], 1)
                          if row[event_fields['id']].startswith(id_prefix)] if id_prefix else []
event_checks = []
for i, row in enumerate(generated_events):
    wanted = project_event(row)
    matches = [(n, r) for n, r in actual_selected_events if project_event(r) == wanted]
    event_checks.append({'replay_event': f'RE{i+1:04d}', 'id_sha256': sha(row[event_fields['id']].encode()),
                         'projection_sha256': rowhash(wanted), 'frozen_event_rows': [f'E{n:06d}' for n, _ in matches],
                         'exact_match_count': len(matches),
                         'same_ordinal_exact': i < len(actual_selected_events) and wanted == project_event(actual_selected_events[i][1])})

STAMP = r'(\d{4}-\d{2}-\d{2}(?:T| )\d{2}:\d{2}:\d{2}(?:Z| UTC))'
record_text = (FROZEN / 'CHECK_RECORD.md').read_bytes().decode()
record_lines = record_text.splitlines()
heading_indices = [i for i, line in enumerate(record_lines) if line == '## English 182']
record_pages, completion_lines = [], []
section_end = None
if len(heading_indices) == 1:
    start = heading_indices[0]
    section_end = next((i for i in range(start + 1, len(record_lines)) if record_lines[i].startswith('## ')), len(record_lines))
    for i in range(start + 1, section_end):
        line = record_lines[i]
        m = re.match(r'\*\*Printed page (\d+)\.\*\* Recorded ' + STAMP + r'\.', line)
        if m:
            record_pages.append({'page': int(m[1]), 'line': i + 1, 'timestamp': m[2]})
        c = re.match(r'Unit completion: ' + STAMP + r'\.', line)
        if c:
            completion_lines.append({'line': i + 1, 'timestamp': c[1]})
progress_pages, progress_done = [], []
for i, line in enumerate((FROZEN / 'progress.log').read_text().splitlines(), 1):
    m = re.fullmatch(r'translation page en 182-(\d+) read ' + STAMP, line)
    if m:
        progress_pages.append({'page': int(m[1]), 'line': i, 'timestamp': m[2]})
    c = re.fullmatch(r'en 182 done ' + STAMP, line)
    if c:
        progress_done.append({'line': i, 'timestamp': c[1]})
record_progress = []
for page in PAGES:
    r = [x for x in record_pages if x['page'] == page]
    p = [x for x in progress_pages if x['page'] == page]
    record_progress.append({'page': page, 'record_count': len(r), 'progress_count': len(p),
                            'record_lines': [x['line'] for x in r], 'progress_lines': [x['line'] for x in p],
                            'timestamps_equal': len(r) == len(p) == 1 and r[0]['timestamp'] == p[0]['timestamp'],
                            'timestamp': r[0]['timestamp'] if len(r) == 1 else None})

after_hashes = {p.relative_to(REPLAY).as_posix(): sha(p.read_bytes())
                for p in REPLAY.rglob('*') if p.is_file()}
allowed = {EN, 'CORRECTIONS.tsv', 'CHECK_EVENTS.tsv', 'CHECK_RECORD.md', 'progress.log'}
unexpected_writes = [p for p in sorted(set(initial_hashes) | set(after_hashes))
                     if initial_hashes.get(p) != after_hashes.get(p) and p not in allowed]
for item in input_checks:
    item['unchanged_after_replay'] = sha((FROZEN / item['file']).read_bytes()) == item['sha256']
all_duplicates = defaultdict(list)
for i, row in enumerate(actual_ledger[1:], 1):
    all_duplicates[rowhash(row)].append(i)
duplicate_groups = [{'row_sha256': h, 'row_ids': [f'C{i:06d}' for i in ids],
                     'entirely_in_baseline_prefix': all(i <= baseline_count for i in ids)}
                    for h, ids in all_duplicates.items() if len(ids) > 1]
operation_duplicates = Counter((r['file'], r['printed_page'], r['old_sha256'], r['new_sha256']) for r in operations)
parsed = lexer.scan_math(actual)
source_deltas = [{'opcode': op, 'replayed_byte_start': a, 'replayed_byte_end_exclusive': b,
                  'frozen_byte_start': c, 'frozen_byte_end_exclusive': d,
                  'replayed_span_sha256': sha(simulated[a:b]), 'frozen_span_sha256': sha(actual[c:d])}
                 for op, a, b, c, d in difflib.SequenceMatcher(None, simulated, actual, autojunk=False).get_opcodes()
                 if op != 'equal'] if actual != simulated else []
completion_equal = len(completion_lines) == len(progress_done) == 1 and completion_lines[0]['timestamp'] == progress_done[0]['timestamp']
summary = {
    'completed_utc': datetime.now(timezone.utc).isoformat(),
    'capture_started_utc': manifest['snapshot_started_utc'],
    'capture_completed_utc': manifest['snapshot_completed_utc'],
    'capture_manifest_sha256': sha(manifest_bytes), 'capture_files': len(input_checks),
    'original_baseline_sha256': sha(original), 'original_selected_copy_equals_pinned_snapshot': original == original_check,
    'baseline_ledger_sha256': sha(baseline_bytes), 'baseline_ledger_rows': baseline_count,
    'frozen_ledger_sha256': sha(actual_ledger_bytes), 'frozen_ledger_rows': len(actual_ledger) - 1,
    'baseline_ledger_exact_byte_prefix': actual_ledger_bytes.startswith(baseline_bytes),
    'baseline_ledger_exact_row_prefix': actual_ledger[1:1+baseline_count] == baseline_rows[1:],
    'planned_scripts': len(SCRIPT_NAMES), 'executed_scripts': len(executions),
    'all_scripts_completed': len(executions) == len(SCRIPT_NAMES) and all(r['completed'] for r in executions),
    'whole_en182_frozen_sha256': sha(actual), 'whole_en182_replayed_sha256': sha(simulated),
    'whole_en182_bytes_equal': actual == simulated, 'whole_en182_bytes': len(actual),
    'page_count': len(page_checks), 'all_page_bytes_equal': all(r.get('current_equals_replay') for r in page_checks),
    'page_marker_sequences_equal': initial_sequence == actual_sequence == replay_sequence,
    'page_marker_sequence_has_no_duplicates': len(actual_sequence) == len(set(actual_sequence)),
    'unit_prefix_unchanged': original[:initial_ranges[193][0]] == simulated[:replay_ranges[193][0]],
    'generated_correction_rows': len(generated), 'selected_frozen_rows': len(selected),
    'all_en182_suffix_rows_selected': selected == all_en182_suffix,
    'generated_rows_equal_frozen_in_order': gen_hashes == actual_hashes,
    'selected_row_first': f'C{selected[0][0]:06d}' if selected else None,
    'selected_row_last': f'C{selected[-1][0]:06d}' if selected else None,
    'generated_serialized_ledger_body_equals_selected_frozen_rows': serialized_selected_exact,
    'interleaved_out_of_scope_rows': interleaved_rows,
    'bytes_after_page204_unchanged_from_original': original[initial_ranges[204][1]:] == simulated[replay_ranges[204][1]:],
    'frozen_EN182_rows_after_page204': sum(row[fields['file']] == EN and row[fields['printed_page']] not in {f'182-{p}' for p in PAGES} for row in actual_ledger[1:]),
    'selected_frozen_duplicate_extra_rows': sum(v - 1 for v in Counter(actual_hashes).values()),
    'whole_ledger_duplicate_groups': len(duplicate_groups),
    'whole_ledger_duplicate_extra_rows': sum(len(r['row_ids']) - 1 for r in duplicate_groups),
    'all_whole_ledger_duplicates_preexist_in_baseline': all(r['entirely_in_baseline_prefix'] for r in duplicate_groups),
    'explicit_replace_calls': len(operations), 'explicit_replace_generated_rows': sum(r['appended_rows'] for r in operations),
    'explicit_replace_all_completed': all(r['completed'] for r in operations),
    'explicit_replace_all_counts_match': all(r['observed_occurrences_before'] == r['requested_occurrences'] for r in operations),
    'explicit_replace_all_predicted_bytes_match': all(r['independently_predicted_bytes_match'] for r in operations),
    'explicit_replace_noop_calls': sum(not r['source_changed'] for r in operations),
    'duplicate_explicit_operation_fingerprints': sum(v-1 for v in operation_duplicates.values()),
    'math_alignment_calls': len(alignments), 'math_pair_count': len(pair_checks),
    'math_nonidentical_pairs': sum(r['nonidentical_pairs'] for r in alignments),
    'math_identical_pairs': sum(r['identical_pairs'] for r in alignments),
    'math_generated_rows': sum(r['appended_rows'] for r in alignments),
    'math_all_counts_match': all(r['target_outer_spans_before'] == r['expected_target'] and r['french_outer_spans'] == r['expected_french'] for r in alignments),
    'math_all_indices_unique_in_range': all(r['all_indices_in_range'] and not r['duplicate_target_indices'] and not r['duplicate_french_indices'] for r in alignments),
    'math_all_predicted_page_bytes_match': all(r['independently_predicted_page_bytes_match'] for r in alignments),
    'math_rows_equal_nonidentical_pairs': all(r['appended_rows'] == r['nonidentical_pairs'] for r in alignments),
    'static_mutation_call_sites': len(static_checks),
    'all_static_mutation_call_sites_observed': all(r['execution_observed'] for r in static_checks),
    'generated_events': len(generated_events), 'selected_frozen_events': len(actual_selected_events),
    'events_exact_except_runtime_timestamps_in_order': [project_event(r) for r in generated_events] == [project_event(r) for _, r in actual_selected_events],
    'generated_event_ids_unique': len(generated_ids) == len(set(generated_ids)),
    'every_generated_event_exactly_one_frozen_match': all(r['exact_match_count'] == 1 for r in event_checks),
    'record_unit_headings': len(heading_indices), 'record_page_entries': len(record_pages),
    'progress_page_entries': len(progress_pages),
    'record_and_progress_exact_page_order': [r['page'] for r in record_pages] == [r['page'] for r in progress_pages] == PAGES,
    'record_progress_timestamps_match': all(r['timestamps_equal'] for r in record_progress),
    'record_completion_lines': completion_lines, 'progress_completion_lines': progress_done,
    'partial_unit_has_no_completion_marker': len(completion_lines) == len(progress_done) == 0,
    'final_source_lexical_issue_count': len(parsed['issues']),
    'all_captured_inputs_unchanged': all(r['unchanged_after_replay'] for r in input_checks),
    'captured_scripts_and_helpers_unchanged_in_replay': all(initial_hashes[p] == after_hashes[p] for p in initial_hashes if p.startswith('scripts/')),
    'unexpected_replay_writes': unexpected_writes, 'blocked_io': blocked_io,
    'discarded_runtime_stdout_bytes': len(stdout.getvalue().encode()),
    'discarded_runtime_stdout_sha256': sha(stdout.getvalue().encode()),
    'source_delta_blocks': len(source_deltas), 'ledger_delta_blocks': len(row_deltas),
    'runtime_timestamp_policy': 'Simulated timestamps only in isolated outputs; correction rows compared exactly; event timestamp excluded from exact projection.',
    'semantic_or_scan_adjudication': False, 'build_performed': False,
    'live_source_or_ledger_reads': False, 'protected_writes': 0,
}
required = ['baseline_ledger_exact_byte_prefix', 'baseline_ledger_exact_row_prefix', 'all_scripts_completed',
            'whole_en182_bytes_equal', 'all_page_bytes_equal', 'page_marker_sequences_equal',
            'page_marker_sequence_has_no_duplicates', 'generated_rows_equal_frozen_in_order',
            'generated_serialized_ledger_body_equals_selected_frozen_rows', 'all_en182_suffix_rows_selected',
            'explicit_replace_all_completed', 'explicit_replace_all_counts_match', 'explicit_replace_all_predicted_bytes_match',
            'math_all_counts_match', 'math_all_indices_unique_in_range', 'math_all_predicted_page_bytes_match',
            'math_rows_equal_nonidentical_pairs', 'all_static_mutation_call_sites_observed',
            'events_exact_except_runtime_timestamps_in_order', 'generated_event_ids_unique',
            'every_generated_event_exactly_one_frozen_match', 'record_and_progress_exact_page_order',
            'record_progress_timestamps_match', 'partial_unit_has_no_completion_marker', 'bytes_after_page204_unchanged_from_original',
            'all_captured_inputs_unchanged', 'captured_scripts_and_helpers_unchanged_in_replay']
summary['failed_checks'] = [key for key in required if not summary[key]]
summary['status'] = 'PASS' if not summary['failed_checks'] and not unexpected_writes and not blocked_io and not summary['selected_frozen_duplicate_extra_rows'] else 'BLOCKER'
dump('SUMMARY.json', summary)
dump('EXPLICIT_OPERATIONS.json', operations)
dump('MATH_ALIGNMENT_COUNTS.json', alignments)
dump('INSTRUMENTED_CALLS.json', calls)
dump('EXACT_DUPLICATE_GROUPS.json', duplicate_groups)
dump('SOURCE_BYTE_DELTAS.json', source_deltas)
dump('LEDGER_DELTAS.json', row_deltas)
dump('LEXICAL_ISSUES.json', parsed['issues'])
tsv('CAPTURE_HASH_CHECKS.tsv', input_checks, list(input_checks[0]))
tsv('PAGE_BYTE_CHECKS.tsv', page_checks, list(page_checks[0]))
tsv('MATH_PAIR_CHECKS.tsv', pair_checks, list(pair_checks[0]) if pair_checks else ['script'])
tsv('LEDGER_ROW_CHECKS.tsv', row_checks, list(row_checks[0]) if row_checks else ['replay_row'])
tsv('STATIC_OPERATION_COVERAGE.tsv', static_checks, list(static_checks[0]))
tsv('EVENT_CORRESPONDENCE.tsv', event_checks, list(event_checks[0]) if event_checks else ['replay_event'])
tsv('RECORD_PROGRESS_CORRESPONDENCE.tsv', record_progress, list(record_progress[0]))
dump('BASELINE_PROVENANCE.json', json.loads((BASE / 'baseline_original/BASELINE.json').read_text()))
dump('FROZEN_SNAPSHOT.json', manifest)
(OUT / 'REPLAY_AUDIT.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(summary, indent=2))
