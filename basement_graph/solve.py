import json
import math
from collections import defaultdict

DIRNAMES = ['R', 'DR', 'D', 'DL', 'L', 'UL', 'U', 'UR']


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def offset_to_dir_index(offset: tuple[int, int]):
    '''Returns a number between 0 and 7 indicating the direction of the vector'''
    xoff, yoff = offset
    angle_deg = math.degrees(math.atan2(yoff, xoff))
    wedge_deg = 360 / 8
    return int(((angle_deg + wedge_deg / 2) // wedge_deg)) % 8


def main():
    with open('nodes.json') as f:
        nodes = {}
        for item in json.load(f):
            nodes[item['id']] = (item['x'], item['y'])

    with open('links.json') as f:
        links = set(tuple(sorted(link)) for link in json.load(f))

    connected = defaultdict(set)
    for a, b in links:
        connected[a].add(b)
        connected[b].add(a)

    # create a graph of connections based on relative direction
    dirs = defaultdict(dict)
    for src, tars in connected.items():
        for tar in tars:
            dir_idx = offset_to_dir_index(sub(nodes[tar], nodes[src]))
            direction = DIRNAMES[dir_idx]
            dirs[src][direction] = tar

    __import__('pprint').pprint(dirs)


if __name__ == '__main__':
    main()
