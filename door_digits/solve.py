from enum import Enum

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
        segment = [0] * 7
        for s in g.split():
            segment[int(str_to_segment(s))] = 1
        segments.append(segment)
    return segments


def display_segment(segment: list[int]):
    out = TEMPLATE
    for i, v in enumerate(segment):
        out = out.replace(str(i), 'X' if v else '.')
    return out


def display(segment_or_segments):
    if isinstance(segment_or_segments[0], int):
        return display_segment(segment_or_segments)

    outs = [display_segment(s).split('\n') for s in segment_or_segments]
    print()
    print(*(''.join(g) for g in zip(*outs)), sep='\n')
    print()


NUM_DIGITS = 4

segments = [[0] * 7 for _ in range(NUM_DIGITS)]

panel = decode_segments(['tr m b', 't br', 'tl tr br', 'tl m bl'])
x = violet = decode_segments(['br', 'b', 't m', 'b tr'])
x = yellow = decode_segments(['t m', 't', 'bl', 't m'])
x = corridor = decode_segments(['tr', 'm', 'tr', 'bl br'])

display(x)
