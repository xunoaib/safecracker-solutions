# Dial numbering:
#   0 1 2
#   3 4 5

DIAL_LETTERS = [
    'GDLF',
    'OTNI',
    'KCMR',
    'UAPC',
    'ZWTN',
    'SABE',
]


def solve_recursive(letters: list[str] | str, dial=0):
    if len(letters) == 0:
        return ''

    if dial >= len(DIAL_LETTERS):
        return None

    for ch in set(DIAL_LETTERS[dial]) & set(letters):
        new_letters = list(letters)
        new_letters.remove(ch)
        result = solve_recursive(new_letters, dial + 1)
        if isinstance(result, str):
            return ch + result


letters = 'WALTER'
assignments = solve_recursive(letters)
print('Dials:', assignments)

for dial, ch in enumerate(assignments):
    times = DIAL_LETTERS[dial].index(ch)
    print(f'Turn dial {dial} x {times} times')
