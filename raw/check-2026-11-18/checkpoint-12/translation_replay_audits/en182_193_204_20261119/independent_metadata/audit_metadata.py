"""Independent frozen-capture and exact ledger-record serialization checks.

No edit scripts are executed. Source files are hashed only. No payload is
printed or included in output, and only this tmp audit directory is written.
"""
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re

WORK = Path(__file__).resolve().parents[3]
BASE = WORK / 'tmp/en182_replay_193_204_20261119'
OUT = BASE / 'independent_metadata'
FROZEN = BASE / 'frozen'
REPLAY = BASE / 'isolated_verified'
BASELINE = BASE / 'baseline_original'
REPORT = WORK / 'FGA_CHECK/translation_replay_audits/en182_193_204_20261119'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def rowhash(row):
    return sha(json.dumps(row, ensure_ascii=False, separators=(',', ':')).encode())


def parse_records(data):
    assert data.decode().encode() == data
    assert data.count(b'\r') == data.count(b'\r\n')
    offsets = [0] + [m.end() for m in re.finditer(b'\n', data)]
    if offsets[-1] != len(data):
        offsets.append(len(data))
    reader = csv.reader(io.StringIO(data.decode(), newline=''), delimiter='\t', strict=True)
    previous, records = 0, []
    for number, values in enumerate(reader):
        start, end = offsets[previous], offsets[reader.line_num]
        records.append({'data_row': number, 'values': values, 'byte_start': start,
                        'byte_end_exclusive': end, 'physical_start': previous + 1,
                        'physical_end': reader.line_num, 'raw': data[start:end],
                        'fields_sha256': rowhash(values), 'raw_sha256': sha(data[start:end])})
        previous = reader.line_num
    assert b''.join(r['raw'] for r in records) == data
    return records


def read_tsv(path):
    with path.open(newline='') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))


def dump(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def tsv(name, rows):
    with (OUT / name).open('w', newline='') as stream:
        writer = csv.DictWriter(stream, list(rows[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


machine_names = ['SUMMARY.json', 'LEDGER_ROW_CHECKS.tsv', 'CAPTURE_HASH_CHECKS.tsv',
                 'FROZEN_SNAPSHOT.json', 'BASELINE_PROVENANCE.json', 'SCRIPT_EXECUTION.json']
machine_bytes = {name: (REPORT / name).read_bytes() for name in machine_names}
reported = json.loads(machine_bytes['SUMMARY.json'])
assert reported['status'] == 'PASS', 'Final authoritative report is not ready'
snapshot_bytes = (FROZEN / 'SNAPSHOT.json').read_bytes()
snapshot = json.loads(snapshot_bytes)
manifest = {x['path']: x for x in snapshot['files']}
assert machine_bytes['FROZEN_SNAPSHOT.json'] == snapshot_bytes
assert sha(snapshot_bytes) == reported['capture_manifest_sha256']
reported_capture = read_tsv(REPORT / 'CAPTURE_HASH_CHECKS.tsv')
assert len(reported_capture) == len(manifest) == 316
reported_capture_map = {r['file']: r for r in reported_capture}
assert set(reported_capture_map) == set(manifest)
capture_checks = []
for name, item in manifest.items():
    data = (FROZEN / name).read_bytes()
    row = reported_capture_map[name]
    capture_checks.append({'file': name, 'bytes': len(data), 'sha256': sha(data),
                           'manifest_exact': len(data) == item['bytes'] and sha(data) == item['sha256'],
                           'published_capture_exact': len(data) == int(row['bytes']) and sha(data) == row['sha256']})
actual_set = {p.relative_to(FROZEN).as_posix() for p in FROZEN.rglob('*') if p.is_file()}
assert actual_set == set(manifest) | {'SNAPSHOT.json'}
assert all(r['manifest_exact'] and r['published_capture_exact'] for r in capture_checks)

baseline_metadata_bytes = (BASELINE / 'BASELINE.json').read_bytes()
baseline_metadata = json.loads(baseline_metadata_bytes)
assert machine_bytes['BASELINE_PROVENANCE.json'] == baseline_metadata_bytes
baseline_source_bytes = [(BASELINE / name).read_bytes() for name in ['182.tex', '182_copy.tex']]
assert baseline_source_bytes[0] == baseline_source_bytes[1]
assert all(len(baseline_source_bytes[0]) == r['bytes'] and sha(baseline_source_bytes[0]) == r['sha256']
           for r in baseline_metadata['original_inputs'])
assert sha(baseline_source_bytes[0]) == reported['original_baseline_sha256']
prefix_bytes = (BASELINE / 'CORRECTIONS_prefix.tsv').read_bytes()
frozen_bytes = (FROZEN / 'CORRECTIONS.tsv').read_bytes()
replay_bytes = (REPLAY / 'CORRECTIONS.tsv').read_bytes()
prefix, actual, replay = map(parse_records, [prefix_bytes, frozen_bytes, replay_bytes])
assert sha(prefix_bytes) == baseline_metadata['baseline_ledger_sha256'] == reported['baseline_ledger_sha256']
assert len(prefix_bytes) == baseline_metadata['baseline_ledger_bytes']
assert len(prefix) - 1 == baseline_metadata['baseline_ledger_rows'] == reported['baseline_ledger_rows'] == 21869
assert frozen_bytes.startswith(prefix_bytes)
assert [r['values'] for r in actual[:len(prefix)]] == [r['values'] for r in prefix]
assert actual[0]['raw'] == replay[0]['raw'] == prefix[0]['raw']
assert sha(frozen_bytes) == manifest['CORRECTIONS.tsv']['sha256'] == reported['frozen_ledger_sha256']
fields = {name: i for i, name in enumerate(actual[0]['values'])}
pages = {f'182-{page}' for page in range(193, 205)}
selected = [r for r in actual[1:] if r['values'][fields['file']] == 'sources/en/en/182.tex'
            and r['values'][fields['layer']] == 'English' and r['values'][fields['printed_page']] in pages]
expected_ids = [n for n in range(21870, 22553) if n != 22110]
assert [r['data_row'] for r in selected] == expected_ids
assert len(selected) == len(replay) - 1 == reported['generated_correction_rows'] == reported['selected_frozen_rows'] == 682
published_rows = read_tsv(REPORT / 'LEDGER_ROW_CHECKS.tsv')
assert len(published_rows) == 682
row_checks = []
for n, (frozen, generated, published) in enumerate(zip(selected, replay[1:], published_rows), 1):
    field_equal = frozen['values'] == generated['values']
    raw_equal = frozen['raw'] == generated['raw']
    identity = f'C{frozen["data_row"]:06d}'
    published_exact = (published['replay_row'] == f'R{n:06d}' and published['row_sha256'] == frozen['fields_sha256']
                       and published['printed_page'] == frozen['values'][fields['printed_page']]
                       and published['kind'] == frozen['values'][fields['kind']]
                       and json.loads(published['exact_frozen_row_ids']) == [identity]
                       and published['exact_match_count'] == '1' and published['same_ordinal_exact'] == 'True')
    row_checks.append({'replay_row': f'R{n:06d}', 'frozen_row_id': identity,
                       'printed_page': frozen['values'][fields['printed_page']],
                       'frozen_physical_start': frozen['physical_start'], 'frozen_physical_end': frozen['physical_end'],
                       'frozen_byte_start': frozen['byte_start'], 'frozen_byte_end_exclusive': frozen['byte_end_exclusive'],
                       'replay_physical_start': generated['physical_start'], 'replay_physical_end': generated['physical_end'],
                       'replay_byte_start': generated['byte_start'], 'replay_byte_end_exclusive': generated['byte_end_exclusive'],
                       'fields_sha256': frozen['fields_sha256'], 'frozen_raw_record_sha256': frozen['raw_sha256'],
                       'replay_raw_record_sha256': generated['raw_sha256'],
                       'fields_exact': field_equal, 'physical_serialization_exact': raw_equal,
                       'published_identity_exact': published_exact})
assert all(r['fields_exact'] and r['physical_serialization_exact'] and r['published_identity_exact'] for r in row_checks)
joined = b''.join(r['raw'] for r in selected)
generated_body = replay_bytes[replay[0]['byte_end_exclusive']:]
assert joined == generated_body
assert len({r['raw_sha256'] for r in selected}) == len(selected)
assert len({r['fields_sha256'] for r in selected}) == len(selected)
excluded = actual[22110]
assert excluded['values'][fields['file']] != 'sources/en/en/182.tex'
assert len(baseline_metadata['excluded_interleaved_rows']) == 1
excluded_meta = baseline_metadata['excluded_interleaved_rows'][0]
assert excluded_meta['row_id'] == 'C022110' and excluded_meta['row_sha256'] == excluded['fields_sha256']

page_checks = []
execution = json.loads(machine_bytes['SCRIPT_EXECUTION.json'])
for page in range(193, 205):
    pp = f'182-{page}'
    a = [r for r in selected if r['values'][fields['printed_page']] == pp]
    b = [r for r in replay[1:] if r['values'][fields['printed_page']] == pp]
    script = [r for r in execution if r['script'] == f'apply_en_182_{page}.py']
    assert len(script) == 1 and script[0]['completed']
    assert script[0]['appended_rows'] == len(a) == len(b)
    page_checks.append({'page': page, 'rows': len(a), 'first_frozen_row_id': f'C{a[0]["data_row"]:06d}',
                        'last_frozen_row_id': f'C{a[-1]["data_row"]:06d}',
                        'frozen_serialized_sha256': sha(b''.join(r['raw'] for r in a)),
                        'replayed_serialized_sha256': sha(b''.join(r['raw'] for r in b)),
                        'physical_serialization_exact': b''.join(r['raw'] for r in a) == b''.join(r['raw'] for r in b),
                        'execution_appended_rows_exact': True})
page199 = next(r for r in page_checks if r['page'] == 199)
assert page199['rows'] == 62 and page199['first_frozen_row_id'] == 'C022169' and page199['last_frozen_row_id'] == 'C022230'
page199_records = [r for r in selected if r['values'][fields['printed_page']] == '182-199']
assert [r['data_row'] for r in page199_records] == list(range(22169, 22231))

# Hash-only source binding; no lexical, text, or mathematical inspection.
en_frozen = (FROZEN / 'sources/en/en/182.tex').read_bytes()
en_replay = (REPLAY / 'sources/en/en/182.tex').read_bytes()
assert sha(en_frozen) == sha(en_replay) == reported['whole_en182_frozen_sha256'] == reported['whole_en182_replayed_sha256']
assert en_frozen == en_replay
assert all((REPORT / name).read_bytes() == data for name, data in machine_bytes.items())
assert (FROZEN / 'SNAPSHOT.json').read_bytes() == snapshot_bytes
assert all(sha((FROZEN / row['file']).read_bytes()) == row['sha256'] for row in capture_checks)
assert (BASELINE / 'BASELINE.json').read_bytes() == baseline_metadata_bytes
assert (REPLAY / 'CORRECTIONS.tsv').read_bytes() == replay_bytes
tsv('CAPTURE_HASH_CHECKS.tsv', capture_checks)
tsv('LEDGER_IDENTITY_AND_SERIALIZATION.tsv', row_checks)
tsv('PAGE_ROW_RANGES.tsv', page_checks)
summary = {'status': 'PASS', 'completed_utc': datetime.now(timezone.utc).isoformat(),
           'capture_started_utc': snapshot['snapshot_started_utc'], 'capture_completed_utc': snapshot['snapshot_completed_utc'],
           'snapshot_sha256': sha(snapshot_bytes), 'capture_files': len(capture_checks),
           'capture_bytes': sum(r['bytes'] for r in capture_checks), 'capture_file_set_exact': True,
           'all_capture_hashes_sizes_and_published_metadata_exact': True,
           'baseline_original_copies_identical': True, 'baseline_original_sha256': sha(baseline_source_bytes[0]),
           'baseline_ledger_rows': len(prefix) - 1, 'baseline_ledger_sha256': sha(prefix_bytes),
           'baseline_exact_byte_and_row_prefix': True,
           'frozen_ledger_rows': len(actual) - 1, 'frozen_ledger_sha256': sha(frozen_bytes),
           'scoped_rows': len(selected), 'first_scoped_row_id': 'C021870', 'last_scoped_row_id': 'C022552',
           'excluded_interleaved_row_id': 'C022110', 'excluded_interleaved_fields_sha256': excluded['fields_sha256'],
           'all_682_row_identities_fields_order_and_serialized_bytes_exact': True,
           'all_682_published_row_checks_exact': True, 'scoped_exact_duplicate_extra_rows': 0,
           'scoped_serialized_bytes': len(joined), 'scoped_serialized_sha256': sha(joined),
           'replay_ledger_sha256': sha(replay_bytes), 'header_bytes_exact': True,
           'page199': {**page199, 'frozen_physical_start': page199_records[0]['physical_start'],
                       'frozen_physical_end': page199_records[-1]['physical_end'],
                       'frozen_byte_start': page199_records[0]['byte_start'],
                       'frozen_byte_end_exclusive': page199_records[-1]['byte_end_exclusive']},
           'source_binding_hash_only_equal': True, 'frozen_and_replayed_EN182_sha256': sha(en_frozen),
           'authoritative_report_relative_path': REPORT.relative_to(WORK).as_posix(),
           'authoritative_replay_relative_path': REPLAY.relative_to(WORK).as_posix(),
           'authoritative_machine_file_hashes': {name: sha(data) for name, data in machine_bytes.items()},
           'all_audited_inputs_and_machine_outputs_unchanged': True,
           'audit_scope': 'Capture hashes, baseline hashes, scoped ledger row identities/order/physical serialization and page199 range; no substantive or source-structure adjudication.',
           'scripts_reexecuted': False, 'source_payloads_interpreted': False, 'live_reads': False,
           'source_ledger_record_events_progress_mutations': 0, 'FGA_CHECK_writes': 0, 'blockers': []}
dump('SUMMARY.json', summary)
print(json.dumps(summary, indent=2))
