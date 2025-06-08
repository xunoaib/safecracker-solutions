#!/usr/bin/env python3
import json
from collections import defaultdict

FLOORS = ['basement', 'ground', 'second', 'loft']


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

    to_merge = [
        ('b5', 'g4'),
        ('g5', 's35'),
        ('g10', 's15'),
        ('s20', 'l3'),
    ]

    for a, b in to_merge:
        merge_nodes(graph, a, b)

    print(graph)


if __name__ == '__main__':
    main()
