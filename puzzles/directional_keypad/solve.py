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


# Create a dependency graph of jumps
graph = {}
offsets = raw_to_offsets(RAW)
for r, row in enumerate(offsets):
    for c, (roff, coff) in enumerate(row):
        graph[r, c] = r + roff, c + coff

# Find the only position not pointed to by any other position
pos = next(iter(set(graph) - set(graph.values())))

print('Row Col')
i = 0
while pos:
    print(f'{i:>2} {pos}')
    npos = graph[pos]
    if npos == pos:
        break
    pos = npos
    i += 1
