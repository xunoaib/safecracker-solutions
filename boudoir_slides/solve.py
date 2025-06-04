import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Literal

START = '''
.C.iii
AC.EF.
AjjEFG
BkkkFG
B.D..H
..DllH
'''.strip()

ROWS, COLS = 6, 6
KEY_TILE_ID = 'j'


@dataclass(frozen=True)
class Tile:
    id: str
    pos: tuple[int, int]
    orientation: Literal['v'] | Literal['h']
    length: int

    @property
    def offset(self):
        return (1, 0) if self.orientation == 'v' else (0, 1)

    def move(self, amount: int):
        '''Positive amount means down or right. Negative means up or left'''
        newpos = (
            self.pos[0] + self.offset[0] * amount,
            self.pos[1] + self.offset[1] * amount,
        )
        return Tile(self.id, newpos, self.orientation, self.length)

    @property
    def spots(self):
        '''Returns all positions covered by this tile'''

        return {
            (
                self.pos[0] + self.offset[0] * i,
                self.pos[1] + self.offset[1] * i
            )
            for i in range(self.length)
        }

    def neighbors(self, other_tiles):
        '''Returns moved versions of this tile (in both possible directions).
        Only returns moves which keep the tile within the grid boundaries.
        '''

        offsets = [
            (
                (self.offset[0], self.offset[1]),
                'down' if self.orientation == 'v' else 'right'
            ),
            (
                (-self.offset[0], -self.offset[1]),
                'up' if self.orientation == 'v' else 'left'
            ),
        ]

        other_spots = {s for t in other_tiles for s in t.spots}

        # try moving in both directions
        for (roff, coff), move in offsets:
            # try moving each piece every possible distance
            pos = self.pos
            dist = 1
            while True:
                newpos = (pos[0] + roff, pos[1] + coff)
                newtile = Tile(self.id, newpos, self.orientation, self.length)

                # check for out of bounds
                if not all(
                    0 <= r < ROWS and 0 <= c < COLS for r, c in newtile.spots
                ):
                    break

                # check for overlap with other tiles
                if newtile.spots & other_spots:
                    break

                yield newtile, f'{self.id} {move} x {dist}'
                pos = newpos
                dist += 1


def display(all_tiles: list[Tile] | frozenset[Tile], highlight=None):
    grid = {p: t.id for t in all_tiles for p in t.spots}
    for r in range(ROWS):
        for c in range(COLS):
            out = grid.get((r, c), '.')
            if out == highlight:
                out = f'\033[91;1m{out}\033[0m'
            print(out, end='')
        print()
    print()


def string_to_grid(start):
    grid_lst = [tuple(row) for row in start.splitlines()]
    return {
        (r, c): ch
        for r, row in enumerate(grid_lst)
        for c, ch in enumerate(row) if ch != '.'
    }


def get_orientation(spots):
    rows, _ = zip(*spots)
    return 'h' if len(set(rows)) == 1 else 'v'


def parse_tiles(grid):
    id_positions = defaultdict(list)
    for p, id in grid.items():
        id_positions[id].append(p)

    return [
        Tile(id, min(spots), get_orientation(spots), len(spots))
        for id, spots in sorted(id_positions.items())
    ]


def neighbors(all_tiles: list[Tile] | frozenset[Tile]):
    '''Returns all valid neighboring states for this tile'''

    for tile in all_tiles:
        other_tiles = [t for t in all_tiles if t != tile]
        for n, move in tile.neighbors(other_tiles):
            yield frozenset(other_tiles + [n]), move


def solved(tiles):
    key_tile = next(t for t in tiles if t.id == KEY_TILE_ID)
    return max(c for r, c in key_tile.spots) == COLS - 1


def solve(tiles):
    start = frozenset(tiles)
    q = [(start, tuple())]
    visited = {start}
    while q:
        tiles, moves = q.pop(0)
        if solved(tiles):
            return moves
        for ntiles, move in neighbors(tiles):
            if ntiles not in visited:
                visited.add(ntiles)
                q.append((ntiles, moves + (move, )))


def move(tiles, move: str):
    # move should be in the form '<tile_id> <left|right|up|down> x <amount>'
    tid, dir, _, amt = move.split()
    tile = next(t for t in tiles if t.id == tid)
    other_tiles = [t for t in tiles if t != tile]
    tile = tile.move(-int(amt) if dir in ('left', 'up') else int(amt))
    return frozenset(other_tiles) | {tile}


def main():
    grid = string_to_grid(START)
    tiles = parse_tiles(grid)

    stepwise = '-s' in sys.argv
    visualize = stepwise or '-v' in sys.argv

    if moves := solve(tiles):
        for i, m in enumerate(moves):
            if not i % 4:
                print()
            print(f'{i}. {m}')
            tiles = move(tiles, m)
            tid, dir, _, amt = m.split()

            if visualize:
                print()
                display(tiles, highlight=tid)

            if stepwise:
                input()
    else:
        print('No solution')


if __name__ == '__main__':
    main()
