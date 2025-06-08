import json
import math
from collections import defaultdict
from itertools import batched

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

    # create a graph of possible moves, respecting the "jump" requirement
    jump_graph = defaultdict(dict)
    for src, dir_tars in dirs.items():
        for dir, tar in dir_tars.items():
            jump_tar = dirs[tar].get(dir)
            if jump_tar is not None:
                jump_graph[src][dir] = jump_tar

    solution = solve(jump_graph, start=0, goal=28)
    for i, v in enumerate(solution):
        print(v, end=' ')
        if not (i + 1) % 4:
            print()
    print()


def solve(graph, start, goal):
    q = [(start, tuple())]
    visited = {start}
    while q:
        node, path = q.pop(0)
        if node == goal:
            return path
        for dir, tar in graph[node].items():
            if tar not in visited:
                visited.add(tar)
                q.append((tar, path + (dir, )))


if __name__ == '__main__':
    main()
