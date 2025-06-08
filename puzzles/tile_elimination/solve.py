# Rules: must eliminate all tiles by jumping between them (no farther than 2
# tiles away), in any direction (orthogonal and diagonal)

from heapq import heappop, heappush
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
        ]:
            n = (r + roff, c + coff)
            if n in tiles:
                yield n


def solve(tiles, start):
    q = [(0, start, tiles, (start, ))]
    while q:
        g, p, tiles, path = heappop(q)
        if not tiles:
            return path
        for n in neighbors(tiles, *p):
            d = abs(p[0] - n[0]) + abs(p[1] - n[1])
            heappush(q, (g + d, n, tiles - {n}, path + (n, )))


def format_actions(solution):
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

    return actions


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
    actions = format_actions(solution)
    for i, action in enumerate(actions):
        print(action.replace('1', ' '), end='  ')
        if not (i + 1) % 4:
            print()
    print()


if __name__ == '__main__':
    main()
