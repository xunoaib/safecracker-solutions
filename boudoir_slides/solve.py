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


@dataclass(frozen=True)
class Tile:
    id: str
    pos: tuple[int, int]
    orientation: Literal['v'] | Literal['h']
    length: int

    # def __repr__(self):
    #     return f'Tile(id={self.id} @ {self.pos})'

    @property
    def offset(self):
        return (1, 0) if self.orientation == 'v' else (0, 1)

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

    @property
    def positions_past_end(self):
        '''Returns the adjacent positions immediately beyond either "end" of this piece'''

        return [
            (
                self.pos[0] - self.offset[0],
                self.pos[1] - self.offset[1],
            ),
            (
                self.pos[0] + self.offset[0] * self.length,
                self.pos[1] + self.offset[1] * self.length
            )
        ]

    def neighbors(self):
        '''Returns moved versions of this tile (in both possible directions).
        Only returns moves which keep the tile within the grid boundaries.
        '''

        offsets = [
            (self.offset[0], self.offset[1]),
            (-self.offset[0], -self.offset[1])
        ]

        for roff, coff in offsets:
            newpos = (self.pos[0] + roff, self.pos[1] + coff)
            newtile = Tile(self.id, newpos, self.orientation, self.length)
            if all(0 <= r < ROWS and 0 <= c < COLS for r, c in newtile.spots):
                yield newtile


def display(all_tiles: list[Tile] | frozenset[Tile]):
    grid = {p: t.id for t in all_tiles for p in t.spots}
    for r in range(ROWS):
        for c in range(COLS):
            print(grid.get((r, c), '.'), end='')
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


def neighbors(all_tiles: list[Tile]):
    '''Returns all valid neighboring states for this tile'''

    for tile in all_tiles:
        other_tiles = [t for t in all_tiles if t != tile]
        for n in tile.neighbors():

            # check for overlap
            other_spots = {s for t in other_tiles for s in t.spots}
            if not n.spots & other_spots:
                yield frozenset(other_tiles + [n])


def main():
    grid = string_to_grid(start)
    all_tiles = parse_tiles(grid)
    for t in all_tiles:
        print(t)

    print()
    for n in neighbors(all_tiles):
        display(n)

    print(len(list(neighbors(all_tiles))))


if __name__ == '__main__':
    main()
