from collections import defaultdict
from dataclasses import dataclass
from typing import Literal

start = '''
.1.222
31.45.
3kk456
788856
7.9..0
..9aa0
'''.strip()

ROWS, COLS = 6, 6


@dataclass
class Tile:
    id: str
    pos: tuple[int, int]
    orientation: Literal['v'] | Literal['h']
    length: int


def string_to_grid(start):
    grid_lst = [tuple(row) for row in start.splitlines()]
    return {
        (r, c): ch
        for r, row in enumerate(grid_lst)
        for c, ch in enumerate(row) if ch != '.'
    }


def get_orientation(spots):
    rows, cols = zip(*spots)
    return 'h' if len(set(rows)) == 1 else 'v'


def parse_tiles(grid):
    id_positions = defaultdict(list)
    for p, id in grid.items():
        id_positions[id].append(p)

    return [
        Tile(id, min(spots), get_orientation(spots), len(spots))
        for id, spots in sorted(id_positions.items())
    ]


def main():
    grid = string_to_grid(start)
    tiles = parse_tiles(grid)
    for t in tiles:
        print(t)


if __name__ == '__main__':
    main()
