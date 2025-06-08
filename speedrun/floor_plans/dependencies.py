import re
from collections import defaultdict


def wrap_label(label, width=16):
    return '\n'.join(label[i:i + width] for i in range(0, len(label), width))


# === Lookup Dictionaries ===


def enum_lookup(enum_type):
    return {e.name.lower(): e for e in enum_type}


def sanitize(s):
    return s.strip().lower().replace('-', '_').replace(' ', '_')


# === Dependency Graph ===
dependency_graph = defaultdict(set)

# === Input Text ===
DEPS_TEXT = '''
rotating safe => three museum puzzles
resistor + 8_pin_circuit + 4_pin_circuit + transistor => workshop
three museum puzzles => library
magnetic_card => service corridor
steering_wheel => laundry room
carved_stone_block => polybius
lever => loft_queens
t_shaped_key => piston
'''

REWARDS = {
    'double_doors': ['access_fountain'],
    'basement_wires': ['gps_keycard', 'brass_key'],
    'basement_knobs': ['access_rest_of_basement'],
    'basement_water': ['piston'],
    'boudoir_slides': ['triple_key_3'],
    'caesar_wheel': ['8_pin_circuit', 'photo'],
    'mastermind_phone': ['gold_keycard', 'letter_from_margaret'],
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
    'driving': ['6821_paper'],
}

# Goal => Requirements
GOAL_REQUIREMENTS = {
    'access_library':
    ('museum_square_numbers', 'tile_elimination', 'currency_sudoku'),
    'access_boudoir': ('workshop_dials', ),
    'study_keypad':
    ('resistor', 'transistor', '8_pin_circuit', '4_pin_circuit'),
}

# === Parsing Logic ===


def parse_colon_block(text):
    '''goal: <comma-delimited list of requirements>'''
    for line in text.strip().splitlines():
        if ':' not in line:
            continue
        lhs, rhs = map(str.strip, line.split(':', 1))
        goal = sanitize(lhs)
        reqs = [sanitize(x) for x in rhs.split(',') if x.strip()]
        for req in reqs:
            dependency_graph[goal].add(req)


def parse_arrow_block(text):
    '''puzzle: list of unlocks'''
    for line in text.strip().splitlines():
        if '=>' not in line:
            continue
        lhs, rhs = map(str.strip, line.split('=>'))
        inputs = [sanitize(x) for x in re.split(r'\+|,', lhs)]
        outputs = [sanitize(x) for x in re.split(r'\+|,', rhs)]
        for out in outputs:
            for inp in inputs:
                dependency_graph[out].add(inp)


parse_arrow_block(DEPS_TEXT)

for reward_source, items in REWARDS.items():
    for item in items:
        dependency_graph[sanitize(item)].add(sanitize(reward_source))

for goal, reqs in GOAL_REQUIREMENTS.items():
    for req in reqs:
        dependency_graph[sanitize(goal)].add(sanitize(req))

# === Output ===
for goal, reqs in dependency_graph.items():
    # print(f"{goal} depends on {sorted(reqs)}")
    for req in reqs:
        print(f'{req}: {goal}')
        pass
