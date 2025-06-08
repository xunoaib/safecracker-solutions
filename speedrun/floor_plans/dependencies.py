import re
from collections import defaultdict
from enum import Enum, auto

import matplotlib.pyplot as plt
import networkx as nx
# You need pygraphviz installed: pip install pygraphviz
from networkx.drawing.nx_agraph import graphviz_layout


def wrap_label(label, width=16):
    return '\n'.join(label[i:i + width] for i in range(0, len(label), width))


def visualize_dependency_graph_left_to_right(dependency_graph):
    G = nx.DiGraph()

    # Add edges
    for target, sources in dependency_graph.items():
        for source in sources:
            G.add_edge(wrap_label(source), wrap_label(target))

    # Use Graphviz layout (dot) with Left-to-Right direction
    pos = graphviz_layout(
        G, prog='dot', args='-Grankdir=LR -Gnodesep=0.6 -Granksep=1.0'
    )

    plt.figure(figsize=(20, 12))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2000,
        node_color='lightyellow',
        font_size=9,
        font_weight='bold',
        edgecolors='black',
        arrows=True,
        arrowsize=12,
        arrowstyle='-|>'
    )

    plt.title("Left-to-Right Dependency Graph", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


# === Enums ===


class Item(Enum):
    T_SHAPED_KEY = auto()
    PISTON = auto()
    RESISTOR = auto()
    PAPER_4298 = auto()
    DOUBLE_KEY = auto()
    L_EQ_E_PAPER = auto()
    FOUNTAIN_PLUG = auto()
    PIN_8_CIRCUIT = auto()
    PHOTO = auto()
    PIN_4_CIRCUIT = auto()
    LASER_LETTER = auto()
    TRANSISTOR = auto()
    SMALL_GOLD_KEY = auto()
    MAGNETIC_CARD = auto()
    TRIPLE_KEY_1 = auto()
    TRIPLE_KEY_2 = auto()
    TRIPLE_KEY_3 = auto()
    TRIPLE_KEY_4 = auto()
    GPS_KEYCARD = auto()
    BRASS_KEY = auto()
    SPECIAL_PIPE_KEY = auto()
    CARVED_STONE_BLOCK = auto()
    SNOOKER_RULES = auto()
    CHIP_CARD = auto()
    LEVER = auto()
    PAPER_6821 = auto()
    STEERING_WHEEL = auto()
    SMALL_IRON_KEY = auto()
    SCREEN_KEY_CARD_READER = auto()


class RewardSource(Enum):
    DOUBLE_DOORS = auto()
    BASEMENT_WIRES = auto()
    BASEMENT_KNOBS = auto()
    BASEMENT_WATER = auto()
    BOUDOIR_SLIDES = auto()
    CAESAR_WHEEL = auto()
    MASTERMIND_PHONE = auto()
    COLORED_WIRES = auto()
    CALL_SARAH = auto()
    OFF_BUTTON = auto()
    CONCENTRIC_CIRCLES = auto()
    CURRENCY_SUDOKU = auto()
    DIRECTIONAL_KEYPAD = auto()
    FOUNTAIN = auto()
    KITCHEN_DUMBWAITER = auto()
    LASER = auto()
    LIBRARY_KEYPAD = auto()
    LOFT_LOOP_PIPES = auto()
    LOFT_QUEENS = auto()
    MAGNET_BALL = auto()
    MUSEUM_SQUARE_NUMBERS = auto()
    PICTURE_SWAPPING = auto()
    POLYBIUS = auto()
    ROTATING_SYMBOL_TILES = auto()
    SNOOKER = auto()
    STUDY_KEYPAD = auto()
    TILE_ELIMINATION = auto()
    UPSTAIRS_WHEELS = auto()
    WORKSHOP_DIALS = auto()
    WORKSHOP_KEYPAD = auto()
    DRIVING = auto()


# === Lookup Dictionaries ===


def enum_lookup(enum_type):
    return {e.name.lower(): e for e in enum_type}


ITEM_LOOKUP = enum_lookup(Item)
REWARD_LOOKUP = enum_lookup(RewardSource)


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
    'driving': ['6821_paper'],
}

# Goal => Requirements
GOAL_REQUIREMENTS = {
    'access_library':
    ('museum_square_numbers', 'tile_elimination', 'currency_sudoku')
}

# === Parsing Logic ===


def parse_arrow_block(text):
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
    print(f"{goal} depends on {sorted(reqs)}")

visualize_dependency_graph_left_to_right(dependency_graph)
