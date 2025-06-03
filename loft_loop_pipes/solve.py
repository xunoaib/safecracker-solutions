import json
from collections import defaultdict

DIR_INDEXES = 'N NE E SE S SW W NW'.split()


def rotate(dir_indexes: set[int], offset: int):
    assert offset in (-2, 2)
    return {(d + offset) % len(DIR_INDEXES) for d in dir_indexes}


def main():
    with open('nodes.json') as f:
        nodes = json.load(f)

    tiles = defaultdict(set)
    for (x, y), d in nodes:
        tiles[x, y].add(DIR_INDEXES.index(d))

    print(tiles)

    s = tiles[0, 0]
    print(s)
    for _ in range(4):
        s = rotate(s, -2)
        print(s)


if __name__ == '__main__':
    main()
