import json
from collections import defaultdict

from z3 import And, If, Int, Or, Solver

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


def main():
    with open('nodes.json') as f:
        nodes = json.load(f)

    tiles = defaultdict(set)
    for (c, r), dir_idx in nodes:
        tiles[r, c].add(DIR_INDEXES.index(dir_idx))

    rotations = {p: Int(f'o{i}') for i, p in enumerate(sorted(tiles))}

    s = Solver()
    s.add([And(0 <= z, z < 8) for z in rotations.values()])

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

    print(connections)

    # require that each pipe has a corresponding connection in the opposite tile.
    # for now, enforce only one constraint for a tile (UP)

    p = (4, 0)
    p_dirs = pd1, pd2 = connections[p]

    q = (p[0] - 1, p[1])
    q_dirs = qd1, qd2 = connections[q]

    tiles_in_dirs = [tile_in_direction(p, d) for d in range(8)]

    d = N
    d_op = (d + 4) % 8
    s.add(If(pd1 == d, Or(qd1 == d_op, qd2 == d_op), True))
    s.add(If(pd2 == d, Or(qd1 == d_op, qd2 == d_op), True))

    # s.add(If(pd1 == N, Or(qd1 == S, qd2 == S), True))
    # s.add(If(pd2 == N, Or(qd1 == S, qd2 == S), True))

    print(connections[p], tiles[p])
    print(connections[q], tiles[q])


if __name__ == '__main__':
    main()
