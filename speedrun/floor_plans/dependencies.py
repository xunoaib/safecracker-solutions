#!/usr/bin/env python3
import json
from collections import defaultdict

FLOORS = ['basement', 'ground', 'second', 'loft']

ITEMS = [
    't_shaped_key',
    'piston'
    'resistor',
    '4298_paper',
    'double_key',
    'l_eq_e_paper',
    'fountain_plug',
    '8_pin_circuit',
    'photo_of_sarah',
    '4_pin_circuit',
    'laser_letter',
    'transistor',
    'small_gold_key',
    'magnetic_card',
    'triple_key_1',
    'triple_key_2',
    'triple_key_3',
    'triple_key_4',
    'gps_keycard',
    'brass_key',
    'special_pipe_key',
    'carved_stone_block',
    'snooker_rules',
    'chip_card',
    'lever',
    '6821_paper',
    'wheel',
    'small_iron_key',
    'screen_key_card_reader',
]

REWARDS = {
    'basement_wires': [],
    'basement_knobs': [],
    'basement_water': [],
    'boudoir_slides': [],
    'caesar_wheel': [],
    'mastermind_phone': [],
    'colored_wires': [],
    'concentric_circles': [],
    'currency_sudoku': [],
    'directional_keypad': [],
    'fountain': [],
    'kitchen_dumbwaiter': [],
    'laser': [],
    'library_keypad': [],
    'loft_loop_pipes': [],
    'loft_queens': [],
    'magnet_ball': [],
    'museum_square_numbers': [],
    'picture_swapping': [],
    'polybius': [],
    'rotating_symbol_tiles': [],
    'snooker': [],
    'study_keypad': [],
    'tile_elimination': [],
    'upstairs_wheels': [],
    'workshop_dials': [],
    'workshop_keypad': [],
}


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
