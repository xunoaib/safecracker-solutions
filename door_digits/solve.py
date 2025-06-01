from enum import Enum

# Safe contains 4 bars.
# Pressing 6666, 7777, 8888, or 9999 causes one bar to temporarily retract.

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


NUM_DIGITS = 4

segments = [0 for _ in range(NUM_DIGITS)]

panel = decode_segments(['tr m b', 't br', 'tl tr br', 'tl m bl'])
violet = decode_segments(['br', 'b', 't m', 'b tr'])
yellow = decode_segments(['t m', 't', 'bl', 't m'])
corridor = decode_segments(['tr', 'm', 'tr', 'bl br'])

# display(violet)
# display(panel)
# display(yellow)
# display(corridor)

bathrooms = [violet, yellow, corridor]
all = [panel, violet, yellow, corridor]

v = merge(all)
display(v)

# display(invert(v))
# display(merge([invert(v), panel]))

# display(merge(bathrooms))
exit(0)

for p in bathrooms:
    v = merge([panel, p])
    display(v)
