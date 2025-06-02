from itertools import product

# 7-segment displays on doors

TEMPLATE = '''
  00  
 6  1 
 6  1 
  55  
 4  2 
 4  2 
  33  
'''.strip('\n')

TOP = 0
TOP_RIGHT = 1
BOT_RIGHT = 2
BOT = 3
BOT_LEFT = 4
MID = 5
TOP_LEFT = 6


def str_to_segment(s):
    return {
        't': TOP,
        'tr': TOP_RIGHT,
        'br': BOT_RIGHT,
        'b': BOT,
        'bl': BOT_LEFT,
        'm': MID,
        'tl': TOP_LEFT,
    }[s]


def decode_segments(segment_strs):
    segments = []
    for g in segment_strs:
        segment = 0
        for s in g.split():
            segment |= 1 << int(str_to_segment(s))
        segments.append(segment)
    return segments


def display_segment(segment):
    out = TEMPLATE
    for i, v in enumerate(f'{segment:07b}'[::-1]):
        out = out.replace(str(i), 'X' if v == '1' else '.')
    return out


def display(segment_or_segments):
    if isinstance(segment_or_segments, int):
        return display_segment(segment_or_segments)

    outs = [display_segment(s).split('\n') for s in segment_or_segments]
    print(*(''.join(g) for g in zip(*outs)), sep='\n')
    print()


def merge(segments):
    out = []
    for g in zip(*segments):
        r = 0
        for v in g:
            r |= v
        out.append(r)
    return out


def subtract(orig_segments, segments_to_sub):
    segments = []
    for o, s in zip(orig_segments, segments_to_sub):
        segments.append(o & (0b1111111 - s))
    return segments


def invert(segments):
    return [0b1111111 - s for s in segments]


KNOWN_DIGITS = {
    k: decode_segments([v])[0]
    for k, v in {
        0: 't b tr tl br bl',
        1: 'tr br',
        2: 't m b tr bl',
        3: 't m b tr br',
        4: 'tl m tr br',
        5: 't m b tl br',
        6: 't m b tl bl br',
        7: 't tr br',
        8: 't m b tl tr bl br',
        9: 't m tl tr br b'
    }.items()
}

NUM_DIGITS = 4

segments = [0 for _ in range(NUM_DIGITS)]

violet = decode_segments(['br', 'b', 't m', 'b tr'])
yellow = decode_segments(['t m', 't', 'bl', 't m'])
corridor = decode_segments(['tr', 'm', 'tr', 'bl br'])
merged = merge([violet, yellow, corridor])
display(merged)

candidates = []
for v in merged:
    row = []
    for d, u in KNOWN_DIGITS.items():
        if (v | u) ^ u == 0:
            row.append(d)
    candidates.append(row)

print('Candidates:', candidates)

print('\nPossible codes:')
print()

# Without more info, we assume a digit may be used no more than once
for p in product(*candidates):
    if len(set(p)) == len(p):
        print('  ' + ''.join(map(str, p)))
