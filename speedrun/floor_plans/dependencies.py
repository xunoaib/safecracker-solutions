#!/usr/bin/env python3
import json
from collections import defaultdict

FLOORS = ['basement', 'ground', 'loft', 'second']

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


def load_graph(fname):
    with open(fname) as f:
        data = json.load(f)

    graph = defaultdict(set)
    for a, b in data['links']:
        graph[a].add(b)
        graph[b].add(a)

    return dict(graph)


def shift_node_ids(graph: dict[int, set[int]], amount: int):
    '''Shifts all nodes IDS up by a given amount'''

    new_graph = {}
    for src, tars in graph.items():
        new_graph[src] = {tar + amount for tar in tars}
    return new_graph


def load_graphs():
    graphs = {}
    node_count = 0
    for floor in FLOORS:
        graph = load_graph(f'floor_{floor}_nodes.json')
        graph = shift_node_ids(graph, node_count)
        graphs[floor] = graph
        node_count += len(graph)

    return graphs


def main():
    graphs = load_graphs()
    print(graphs)


if __name__ == '__main__':
    main()
