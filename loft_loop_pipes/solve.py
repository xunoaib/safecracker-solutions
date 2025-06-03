import json
from collections import defaultdict

from z3 import And, If, Int, Or, Solver, sat

NUM_ROWS = NUM_COLS = 5

DIR_INDEXES = 'N NE E SE S SW W NW'.split()
N, NE, E, SE, S, SW, W, NW = range(len(DIR_INDEXES))

DIR_OFFSETS = {
    N: (-1, 0),
    NE: (-1, 1),
    E: (0, 1),
    SE: (1, 1),
    S: (1, 0),
    SW: (1, -1),
    W: (0, -1),
    NW: (-1, -1),
}


def rotate(dir_indexes: set[int], offset: int):
    assert offset in (-2, 2)
    return {(d + offset) % len(DIR_INDEXES) for d in dir_indexes}


def tile_in_direction(pos: tuple[int, int], direction: int):
    roff, coff = DIR_OFFSETS[direction]
    return pos[0] + roff, pos[1] + coff


def inbounds(pos: tuple[int, int]):
    return 0 <= pos[0] < NUM_ROWS and 0 <= pos[1] < NUM_COLS


def main():
    with open('nodes.json') as f:
        nodes = json.load(f)

    tiles = defaultdict(set)
    for (c, r), dir_idx in nodes:
        tiles[r, c].add(DIR_INDEXES.index(dir_idx))

    rotations = {p: Int(f'o{i}') for i, p in enumerate(sorted(tiles))}

    s = Solver()
    s.add([And(0 <= z, z < 4) for z in rotations.values()])

    # create variables for the directions of each tile's final connections
    connections = {}
    for tid, (p, dirs) in enumerate(tiles.items()):
        vals = []
        for did, dir_idx in enumerate(dirs):
            nodedir = Int(f'n{tid}_{did}')
            vals.append(nodedir)
            # apply offest to final direction
            s.add(nodedir == (2 * rotations[p] + dir_idx) % 8)
        connections[p] = tuple(vals)

    # require that each pipe has a corresponding connection in the opposite tile.
    # for now, enforce only one constraint for a tile (UP)

    for p in sorted(tiles):
        p_dirs = connections[p]
        tiles_in_dirs = [tile_in_direction(p, d) for d in range(8)]

        # apply conditional constraint to each direction
        for d in range(8):
            d_op = (d + 4) % 8
            q = tiles_in_dirs[d]
            q_dirs = connections.get(q)
            for pd in p_dirs:
                if q_dirs is None:  # q is out of bounds
                    s.add(pd != d)  # p must stay in bounds
                else:  # require q to connect back to p
                    s.add(
                        If(
                            pd == d, Or(q_dirs[0] == d_op, q_dirs[1] == d_op),
                            True
                        )
                    )

    assert s.check() == sat
    m = s.model()

    print()
    for r in range(5):
        for c in range(5):
            v = rotations[r, c]
            print(m[v].as_long(), end=' ')
        print()


if __name__ == '__main__':
    main()
