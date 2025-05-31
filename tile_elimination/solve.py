# Rules: must eliminate all tiles by jumping between them (no farther than 2
# tiles away), in any direction (orthogonal and diagonal)

from itertools import pairwise

input_grid = '''
..xx.x.
.s..xx.
.xx....
.x..xx.
.x.x...
.x.x.x.
xxx.xxx
x.xx.x.
'''.strip()


def neighbors(tiles, r, c):
    for d in (1, 2):
        for roff, coff in [
            (-d, 0),
            (d, 0),
            (0, d),
            (0, -d),
            (d, d),
            (d, -d),
            (-d, d),
            (-d, -d),
        ]:
            n = (r + roff, c + coff)
            if n in tiles:
                yield n


def solve(tiles, start):
    q = [(start, tiles, (start, ))]
    while q:
        p, tiles, path = q.pop()
        if not tiles:
            return path
        for n in neighbors(tiles, *p):
            q.append((n, tiles - {n}, path + (n, )))


def format_solution(solution):
    actions = []
    for p, n in pairwise(solution):
        roff, coff = (n[0] - p[0], n[1] - p[1])

        s = '2' if 2 in (abs(coff), abs(roff)) else '1'

        if roff > 0:
            s += 'D'
        elif roff < 0:
            s += 'U'

        if coff > 0:
            s += 'R'
        elif coff < 0:
            s += 'L'

        actions.append(s)

    return ' '.join(actions)


def main():

    tiles = frozenset(
        (r, c) for r, line in enumerate(input_grid.splitlines())
        for c, ch in enumerate(line) if ch == 'x'
    )

    start = next(
        (r, c) for r, line in enumerate(input_grid.splitlines())
        for c, ch in enumerate(line) if ch == 's'
    )

    solution = solve(tiles, start)
    print(format_solution(solution))


if __name__ == '__main__':
    main()
