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
    'photo',
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
    'chip_card',  # gold
    'lever',
    '6821_paper',
    'steering_wheel',
    'small_iron_key',
    'screen_key_card_reader',
]

DEPS = '''
rotating safe => three museum puzzles
components => workshop
three museum puzzles => library
magnetic_card => service corridor
steering_wheel => laundry room
carved_stone_block => polybius
lever => loft_queens
t-shaped key => piston
'''

DOORS = '''
museum => small corridor
dining room + brass_key => main landing
main landing => hall
west corridor => kitchen
colored_wires + pipe key => yellow room
piston + basement_water => double key
double key => violet room
small gold key + violet room => small iron key + screen_key_card_reader
small iron key => mastermind_phone
chip_card => boudoir
triple keys x4 => door_digits
'''

REWARDS = {
    'double_doors': ['access_fountain'],
    'basement_wires': ['gps_keycard', 'brass_key'],
    'basement_knobs': ['access_rest_of_basement'],
    'basement_water': ['piston'],
    'boudoir_slides': ['triple_key_3'],
    'caesar_wheel': ['8_pin_circuit', 'photo'],
    'mastermind_phone': ['chip_card', 'letter_from_margaret'],
    'colored_wires': ['access_yellow_room'],
    'call_sarah': ['steering_wheel'],
    'off_button': ['magnetic_card', 'snooker_rules'],
    'concentric_circles': ['resistor', '4298_paper'],
    'currency_sudoku': [],
    'directional_keypad': ['access_workshop'],
    'fountain': ['double_key'],
    'kitchen_dumbwaiter': ['special_pipe_key'],
    'laser': ['small_gold_key', 't_shaped_key'],
    'library_keypad': ['triple_key_4'],
    'loft_loop_pipes': ['carved_stone_block'],
    'loft_queens': ['triple_key_1'],
    'magnet_ball': ['4_pin_circuit'],
    'museum_square_numbers': [],
    'picture_swapping': ['laser_letter'],
    'polybius': ['triple_key_2'],
    'rotating_symbol_tiles': ['l_eq_e_paper', 'access_triple_museum'],
    'snooker': ['fountain_plug', 'lever'],
    'study_keypad': [],
    'tile_elimination': [],
    'upstairs_wheels': [],
    'workshop_dials': [],
    'workshop_keypad': [],
    'driving': ['6821_paper']
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
