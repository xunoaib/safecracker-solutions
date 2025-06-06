#!/usr/bin/env python3
import json
from collections import defaultdict

FLOORS = ['basement', 'ground', 'second', 'loft']

ITEMS = [
    't-shaped key',
    'piston'
    'resistor',
    '4298 paper',
    'double key',
    'L=E paper',
    'fountain plug',
    '8 pin circuit',
    'photo of sarah',
    '4 pin circuit',
    'laser letter',
    'transistor',
    'small gold key',
    'magnetic card',
    'triple key 1',
    'triple key 2',
    'triple key 3',
    'triple key 4',
    'gps keycard',
    'brass key',
    'special pipe key',
    'carved stone block',
    'snooker rules',
    'chip card',
    'lever',
    '6821 paper',
    'wheel',
    'small iron key',
    'screen & key card reader',
]


def load_floor_graph(fname, prefix):
    with open(fname) as f:
        data = json.load(f)

    graph = defaultdict(set)
    for a, b in data['links']:
        a = f'{prefix}{a}'
        b = f'{prefix}{b}'
        graph[a].add(b)
        graph[b].add(a)

    return dict(graph)


def load_complete_graph():
    graphs = {}
    for floor in FLOORS:
        graphs |= load_floor_graph(f'floor_{floor}_nodes.json', floor[0])
    return graphs


def merge_nodes(graph, n, m):
    '''Collapses identical nodes n and m which are expected to link floors.
    The new node id will be named: <n>_<m>
    '''

    new_id = f'{n}_{m}'
    graph[new_id] = set()

    for node in (n, m):
        for other in graph[node]:
            graph[other].remove(node)
            graph[other].add(new_id)
            graph[new_id].add(other)

    del graph[n]
    del graph[m]


def main():
    graph = load_complete_graph()
    merge_nodes(graph, 's15', 'g10')
    print(graph)


if __name__ == '__main__':
    main()
