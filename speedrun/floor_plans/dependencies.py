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
# objective mapped to requirements
dependency_graph = defaultdict(set)

# === Input Text ===

# X requires Y
REQS_TEXT = '''
upstairs_wheels: steering_wheel
4_pin_circuit: magnet_ball
access_service_hall: study_keypad
access_rest_of_basement: basement_knobs
basement_water: piston
triple_key_3: boudoir_slides
polybius: carved_stone_block
access_yellow_room: colored_wires
colored_wires: special_pipe_key
access_workshop: office_keypad
access_fountain: double_doors
lever: loft_queens
library_keypad: triple_key_4
loft_loop_pipes: carved_stone_block
magnet_ball: 4_pin_circuit
study_keypad: access_service_hall
mastermind_phone: iron_key
museum_square_numbers: access_library
snooker: fountain_plug, lever
rotating_symbol_tiles: l_eq_e_paper, access_triple_museum
study_keypad: access_service_hall
access_loft: upstairs_wheels
access_boudoir: workshop_dials
workshop_dials: gold_keycard
music_box: access_violet_room
door_digits: access_violet_room, triple_key_1, triple_key_2, triple_key_3, triple_key_4

# laser_safe: access_workshop
# workshop_keypad: access_workshop

currency_sudoku: access_triple_museum
tile_elimination: access_triple_museum
museum_square_numbers: access_triple_museum
access_violet_room: double_key

'''

# action => effects
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
    'directional_keypad': ['transistor'],
    'fountain': ['double_key'],
    'kitchen_dumbwaiter': ['special_pipe_key'],
    'laser_safe': ['small_gold_key', 't_shaped_key'],
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
    'music_box': ['iron_key'],
}

# Goal => Requirements
GOAL_REQUIREMENTS = {
    # 'access_library':
    # ('museum_square_numbers', 'tile_elimination', 'currency_sudoku'),
    # 'access_boudoir': ('workshop_dials', ),
    # 'study_keypad':
    # ('resistor', 'transistor', '8_pin_circuit', '4_pin_circuit'),
    # 'access_loft': ('steering_wheel', )
}

# === Parsing Logic ===


def parse_colon_block(text):
    '''goal: <comma-delimited list of requirements>'''
    for line in text.strip().splitlines():
        if line.startswith('#'):
            continue
        if ':' not in line:
            continue
        lhs, rhs = map(str.strip, line.split(':', 1))
        goal = sanitize(lhs)
        reqs = [sanitize(x) for x in rhs.split(', ') if x.strip()]
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


# parse_arrow_block(DEPS_TEXT)
parse_colon_block(REQS_TEXT)

for reward_source, items in REWARDS.items():
    for item in items:
        dependency_graph[sanitize(item)].add(sanitize(reward_source))

for goal, reqs in GOAL_REQUIREMENTS.items():
    for req in reqs:
        dependency_graph[sanitize(goal)].add(sanitize(req))


def main():
    for goal, reqs in dependency_graph.items():
        # for req in reqs:
        #     print(f'{req}: {goal}')
        # print(', '.join(sorted(reqs)), '\033[92m=>\033[0m', goal)
        print(
            goal.ljust(23), '\033[92mrequires\033[0m  ',
            ', '.join(sorted(reqs))
        )


if __name__ == '__main__':
    main()
