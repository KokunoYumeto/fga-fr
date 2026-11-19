"""Literal, context-aware TeX math ranges; pure bytes in, metadata out.

API: scan_math(data: bytes) -> dict containing spans, issues, text_groups,
references, and counts. Offsets are zero-based; all ends are exclusive.
Each balanced span includes its delimiter/environment bytes; inner offsets
exclude those bytes. All supported nested math environments are included,
as are dollar spans within literal text-command bodies. Parent indices refer
to the returned spans list. Consumers can select outermost spans if desired.

Supported current syntax: single-dollar math, \\[...\\], equation, align,
align*, aligned, array, gathered, split; literal text-box contexts below.
\\(...\\) is also supported. Double dollars, nonliteral environments,
unclassified environments, verbatim, and unbalanced structures are issues.
No macro expansion, catcode changes, conditional evaluation, or content
interpretation is attempted. No source bytes are returned or modified.
"""
from collections import Counter
import re

CONTROL = re.compile(rb'\\([A-Za-z@]+|[^A-Za-z@])')
TOKEN = re.compile(rb'\\([A-Za-z@]+|[^A-Za-z@])|(\$+)|([{}])')
DISPLAY_ENVIRONMENTS = frozenset({'equation', 'align', 'align*'})
INNER_ENVIRONMENTS = frozenset({'aligned', 'array', 'gathered', 'split'})
NONMATH_ENVIRONMENTS = frozenset({'center', 'description', 'enumerate',
                                'flushright', 'proof', 'quote'})
# The integer selects the mandatory braced argument supplying text contents.
TEXT_ARGUMENT = {
    'text': 1, 'textbf': 1, 'textit': 1, 'textnormal': 1, 'textsc': 1,
    'texttt': 1, 'textup': 1, 'textsuperscript': 1, 'hbox': 1, 'mbox': 1,
    'resizebox': 3,
}
REFERENCE_COMMANDS = frozenset({'tag', 'ref', 'eqref', 'pageref', 'autoref',
                               'cref', 'Cref', 'vref', 'Vref', 'label',
                               'cite', 'citet', 'citep', 'nocite', 'bibitem'})


def mask_comments(data):
    """Consume control sequences first, then mask unescaped percent comments."""
    masked = bytearray(data)
    ranges = []
    cursor = 0
    while cursor < len(data):
        if data[cursor] == 92:
            token = CONTROL.match(data, cursor)
            cursor = token.end() if token else cursor + 1
        elif data[cursor] == 37:
            end = cursor
            while end < len(data) and data[end] not in (10, 13):
                end += 1
            ranges.append((cursor, end))
            masked[cursor:end] = b' ' * (end - cursor)
            cursor = end
        else:
            cursor += 1
    return bytes(masked), ranges


def scan_math(data):
    """Return only lexical ranges, command spellings, counts, and issue locators.

    Balanced spans can still have ambiguous=True when a literal mode conflict
    was observed. Missing delimiters are never invented. Any nonempty issues
    list should be exposed by the caller before relying on complete coverage.
    """
    if not isinstance(data, bytes):
        raise TypeError('scan_math requires bytes')
    masked, comments = mask_comments(data)
    tokens = list(TOKEN.finditer(masked))
    issues, pairs, brace_stack = [], {}, []

    def issue(code, start, end, **extra):
        row = dict(code=code, start=start, end=end)
        row.update(extra)
        issues.append(row)

    # Build literal brace-pair offsets without treating escaped braces as groups.
    for token in tokens:
        if token.group(3) == b'{':
            brace_stack.append(token.start())
        elif token.group(3) == b'}':
            if brace_stack:
                pairs[brace_stack.pop()] = token.end()
            else:
                issue('unmatched_closing_brace', token.start(), token.end())
    for start in brace_stack:
        issue('unclosed_brace', start, start + 1)

    def skip_space(cursor):
        while cursor < len(masked) and masked[cursor:cursor + 1].isspace():
            cursor += 1
        return cursor

    def argument(cursor):
        start = skip_space(cursor)
        if start not in pairs:
            return None
        return start, pairs[start]

    def after_star(cursor):
        cursor = skip_space(cursor)
        starred = masked[cursor:cursor + 1] == b'*'
        return cursor + int(starred), starred

    text_groups, text_at, references = [], {}, []
    command_counts, environment_counts, delimiter_counts = Counter(), Counter(), Counter()
    for token in tokens:
        if token.group(2):
            delimiter_counts['dollar_run_' + str(len(token.group(2)))] += 1
            continue
        if not token.group(1):
            continue
        command = token.group(1).decode('ascii', errors='replace')
        command_counts[command] += 1
        if command in {'[', ']', '(', ')'}:
            delimiter_counts['\\' + command] += 1
        if command in {'verb', 'Verb', 'catcode', 'mathcode', 'everymath', 'everydisplay'}:
            issue('unsupported_literal_control', token.start(), token.end(), command=command)
        if command in TEXT_ARGUMENT:
            cursor, starred = after_star(token.end())
            args = []
            for _ in range(TEXT_ARGUMENT[command]):
                item = argument(cursor)
                if item is None:
                    break
                args.append(item)
                cursor = item[1]
            if len(args) != TEXT_ARGUMENT[command]:
                issue('text_command_without_expected_literal_arguments', token.start(), token.end(),
                      command=command, expected_arguments=TEXT_ARGUMENT[command],
                      observed_arguments=len(args))
            else:
                start, end = args[-1]
                row = dict(text_group_index=len(text_groups), command=command,
                           command_start=token.start(), command_end=token.end(), starred=starred,
                           group_start=start, group_end=end, inner_start=start + 1, inner_end=end - 1,
                           dollar_bytes=masked[start + 1:end - 1].count(b'$'),
                           entered_from_math=False, parent_open_index=None)
                text_groups.append(row)
                if start in text_at:
                    issue('overlapping_text_group_registration', start, end)
                text_at[start] = row
        if command in REFERENCE_COMMANDS:
            cursor, starred = after_star(token.end())
            item = argument(cursor)
            if item is None:
                issue('reference_without_literal_argument', token.start(), token.end(), command=command)
            else:
                references.append(dict(command=command, starred=starred,
                                       start=token.start(), end=item[1],
                                       inner_start=item[0] + 1, inner_end=item[1] - 1))

    # A literal text body establishes its own mode context while retaining its
    # enclosing math parent. Its closing brace restores the previous context.
    contexts = [dict(frames=[], text_group=None)]
    groups, environments, all_frames = [], [], []

    def nearest_frame():
        for context in reversed(contexts):
            if context['frames']:
                return context['frames'][-1]
        return None

    def open_frame(kind, delimiter, environment, start, inner_start, ambiguous=False):
        parent = nearest_frame()
        frame = dict(open_index=len(all_frames), kind=kind, delimiter=delimiter,
                     environment=environment, start=start, inner_start=inner_start,
                     inner_end=None, end=None,
                     parent_open_index=parent['open_index'] if parent else None,
                     depth=parent['depth'] + 1 if parent else 0,
                     text_group_index=contexts[-1]['text_group'],
                     opening_brace_depth=len(groups), ambiguous=ambiguous)
        all_frames.append(frame)
        contexts[-1]['frames'].append(frame)
        return frame

    def close_frame(frame, inner_end, end):
        if len(groups) != frame['opening_brace_depth']:
            issue('math_delimiters_cross_brace_depth', frame['start'], end,
                  opening_brace_depth=frame['opening_brace_depth'], closing_brace_depth=len(groups))
            frame['ambiguous'] = True
        frame['inner_end'], frame['end'] = inner_end, end
        contexts[-1]['frames'].pop()

    skip_until = -1
    for token in tokens:
        start, end = token.start(), token.end()
        if start < skip_until:
            continue
        if token.group(3) == b'{':
            text_group = text_at.get(start)
            groups.append((start, text_group))
            if text_group is not None:
                parent = nearest_frame()
                text_group['entered_from_math'] = bool(contexts[-1]['frames'])
                text_group['parent_open_index'] = parent['open_index'] if parent else None
                contexts.append(dict(frames=[], text_group=text_group['text_group_index']))
            continue
        if token.group(3) == b'}':
            if not groups:
                continue  # Already recorded by literal brace pairing.
            group_start, text_group = groups.pop()
            if text_group is not None:
                for frame in contexts[-1]['frames']:
                    issue('unclosed_math_before_text_group_end', frame['start'], end,
                          text_group_index=text_group['text_group_index'])
                contexts.pop()
            continue
        if token.group(2):
            if len(token.group(2)) != 1:
                issue('unsupported_multiple_dollar_run', start, end,
                      dollar_count=len(token.group(2)))
                continue
            active = contexts[-1]['frames']
            if not active:
                open_frame('inline', '$', '', start, end)
            elif active[-1]['delimiter'] == '$':
                close_frame(active[-1], start, end)
            else:
                issue('dollar_in_math_without_text_context', start, end,
                      enclosing_open_index=active[-1]['open_index'])
                active[-1]['ambiguous'] = True
            continue
        if not token.group(1):
            continue
        command = token.group(1).decode('ascii', errors='replace')
        if command in {'[', '('}:
            ambiguous = bool(contexts[-1]['frames'])
            if ambiguous:
                issue('math_opener_inside_math_without_text_context', start, end,
                      command=command, enclosing_open_index=contexts[-1]['frames'][-1]['open_index'])
            open_frame('display' if command == '[' else 'inline', '\\' + command, '', start, end, ambiguous)
        elif command in {']', ')'}:
            wanted = '\\[' if command == ']' else '\\('
            active = contexts[-1]['frames']
            if active and active[-1]['delimiter'] == wanted:
                close_frame(active[-1], start, end)
            else:
                issue('unmatched_math_closer', start, end, command=command)
        elif command in {'begin', 'end'}:
            item = argument(end)
            if item is None:
                issue('environment_without_literal_argument', start, end, command=command)
                continue
            group_start, group_end = item
            value = masked[group_start + 1:group_end - 1]
            skip_until = group_end
            if not re.fullmatch(rb'[A-Za-z*]+', value):
                issue('nonliteral_environment_name', start, group_end, command=command)
                continue
            name = value.decode('ascii')
            environment_counts[(command, name)] += 1
            if name not in DISPLAY_ENVIRONMENTS | INNER_ENVIRONMENTS | NONMATH_ENVIRONMENTS:
                issue('unclassified_environment', start, group_end, command=command, environment=name)
            if command == 'begin':
                frame = None
                if name in DISPLAY_ENVIRONMENTS | INNER_ENVIRONMENTS:
                    active = bool(contexts[-1]['frames'])
                    ambiguous = (name in DISPLAY_ENVIRONMENTS and active) or (name in INNER_ENVIRONMENTS and not active)
                    if ambiguous:
                        issue('math_environment_mode_conflict', start, group_end,
                              environment=name, enclosing_math=active)
                    frame = open_frame('environment', 'environment', name, start, group_end, ambiguous)
                environments.append(dict(name=name, start=start, end=group_end, frame=frame,
                                         context_index=len(contexts) - 1))
            elif not environments or environments[-1]['name'] != name:
                issue('unmatched_or_crossed_environment_end', start, group_end, environment=name)
            else:
                opened = environments.pop()
                frame = opened['frame']
                if frame is not None:
                    if (opened['context_index'] == len(contexts) - 1
                            and contexts[-1]['frames'] and contexts[-1]['frames'][-1] is frame):
                        close_frame(frame, start, group_end)
                    else:
                        issue('math_context_mismatch_at_environment_end', start, group_end,
                              environment=name, opening_start=opened['start'])

    for context in contexts:
        for frame in context['frames']:
            issue('unclosed_math_at_end_of_file', frame['start'], frame['inner_start'],
                  open_index=frame['open_index'], delimiter=frame['delimiter'], environment=frame['environment'])
    for opened in environments:
        issue('unclosed_environment_at_end_of_file', opened['start'], opened['end'], environment=opened['name'])
    spans = [frame for frame in all_frames if frame['end'] is not None]
    mapping = {frame['open_index']: i for i, frame in enumerate(spans)}
    for i, frame in enumerate(spans):
        frame['span_index'] = i
        frame['parent_span_index'] = mapping.get(frame['parent_open_index'])
        frame.pop('opening_brace_depth')
    for row in text_groups:
        row['parent_span_index'] = mapping.get(row['parent_open_index'])
        in_context = [s for s in spans if s['text_group_index'] == row['text_group_index']]
        row['math_spans_in_context'] = len(in_context)
        row['direct_nested_math_spans'] = sum(s['parent_open_index'] == row['parent_open_index']
                                              for s in in_context)
    return dict(spans=spans, issues=sorted(issues, key=lambda row: (row['start'], row['end'], row['code'])),
                text_groups=text_groups, references=references,
                command_counts=dict(command_counts), delimiter_counts=dict(delimiter_counts),
                environment_counts=[dict(command=command, environment=name, count=count)
                                    for (command, name), count in sorted(environment_counts.items())],
                comment_ranges=comments, raw_dollar_bytes=data.count(b'$'),
                comment_dollar_bytes=sum(data[a:b].count(b'$') for a, b in comments),
                escaped_dollar_controls=command_counts.get('$', 0))
