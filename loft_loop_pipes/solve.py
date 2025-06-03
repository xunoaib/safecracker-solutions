import json
from collections import defaultdict

from z3 import And, If, Int, Or, Solver, sat

DIR_INDEXES = 'N NE E SE S SW W NW'.split()
N, NE, E, SE, S, SW, W, NW = range(len(DIR_INDEXES))


def rotate(dir_indexes: set[int], offset: int):
    assert offset in (-2, 2)
    return {(d + offset) % len(DIR_INDEXES) for d in dir_indexes}


def main():
    with open('nodes.json') as f:
        nodes = json.load(f)

    tiles = defaultdict(set)
    for (x, y), dir_idx in nodes:
        tiles[x, y].add(DIR_INDEXES.index(dir_idx))

    # print(tiles)
    # s = tiles[0, 0]
    # print(s)
    # for _ in range(4):
    #     s = rotate(s, -2)
    #     print(s)

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

    p = (0, 4)
    p_dirs = pd1, pd2 = connections[p]

    q = (p[0], p[1] - 1)
    q_dirs = qd1, qd2 = connections[q]

    s.add(If(pd1 == N, Or(qd1 == S, qd2 == S), True))

    print(connections[p], tiles[p])
    print(connections[q], tiles[q])


if __name__ == '__main__':
    main()
