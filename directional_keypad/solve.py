RAW = '''
>> vv < v
^ vv < <<<
>>> > v g
^ >> << ^^^
'''.strip()

OFFSETS = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^': (-1, 0),
    'g': (0, 0),
}


def raw_to_offsets(raw: str):
    rows = [line.split() for line in raw.splitlines()]
    result = []
    for row in rows:
        p = []
        for s in row:
            roff, coff = OFFSETS[s[0]]
            p.append((roff * len(s), coff * len(s)))
        result.append(p)
    return result


for row in raw_to_offsets(RAW):
    print(row)
