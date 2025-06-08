EXPECTED_COUNTS = {
    'red': 15,
    'yellow': 1,
    'green': 1,
    'brown': 1,
    'blue': 1,
    'pink': 1,
    'black': 1,
}

BALL_VALUES = {
    'red': 1,
    'yellow': 2,
    'green': 3,
    'brown': 4,
    'blue': 5,
    'pink': 6,
    'black': 7,
}

REAL_COUNTS = {
    'red': 11 + 2,  # on table + in pocket
    'yellow': 0 + 1,
    'green': 0,
    'brown': 1,
    'blue': 1,
    'pink': 1,
    'black': 0,
}

MISSING_COUNTS = {
    c: EXPECTED_COUNTS[c] - REAL_COUNTS[c]
    for c in EXPECTED_COUNTS
}

values = [
    v for color, count in MISSING_COUNTS.items()
    for v in (BALL_VALUES[color], ) * count
]

print(*values, sep='')
