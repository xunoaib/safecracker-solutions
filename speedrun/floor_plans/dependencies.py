#!/usr/bin/env python3
import re
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

DEPS_TEXT = '''
rotating safe => three museum puzzles
resistor + 8_pin_circuit + 4_pin_circuit + transistor => workshop
three museum puzzles => library
magnetic_card => service corridor
steering_wheel => laundry room
carved_stone_block => polybius
lever => loft_queens
t-shaped key => piston
'''

DOORS_TEXT = '''
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
    'study_keypad': ['access_service_hall'],
    'tile_elimination': [],
    'upstairs_wheels': ['access_loft'],
    'workshop_dials': ['access_boudoir'],
    'workshop_keypad': ['red_magnetic_card'],
    'driving': ['6821_paper']
}

DEPENDENCIES = {
    'access_library':
    ('museum_square_numbers', 'tile_elimination', 'currency_sudoku'),
}

dependency_graph = defaultdict(set)


def parse_arrow_block(text):
    for line in text.strip().splitlines():
        if '=>' not in line:
            continue
        lhs, rhs = map(str.strip, line.split('=>'))
        inputs = [x.strip() for x in re.split(r'\+|,', lhs)]
        outputs = [x.strip() for x in re.split(r'\+|,', rhs)]
        for out in outputs:
            for inp in inputs:
                dependency_graph[out].add(inp)


parse_arrow_block(DEPS_TEXT)
parse_arrow_block(DOORS_TEXT)

for reward_source, items in REWARDS.items():
    for item in items:
        dependency_graph[item].add(reward_source)

for goal, reqs in DEPENDENCIES.items():
    for req in reqs:
        dependency_graph[goal].add(req)

# print(dependency_graph)
for goal, reqs in dependency_graph.items():
    print(reqs, goal)
