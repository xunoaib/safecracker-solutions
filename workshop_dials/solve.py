DIAL_LETTERS = [
    'GDLF',
    'OTNI',
    'KCMR',
    'UAPC',
    'ZWTN',
    'SABE',
]


def solve_recursive(letters: set[str], dial=0):
    if dial >= len(DIAL_LETTERS):
        return ''

    for ch in set(DIAL_LETTERS[dial]) & letters:
        result = solve_recursive(letters - {ch}, dial + 1)
        if isinstance(result, str):
            return ch + result


letters = set('WALTER')  # doesnt support duplicate letters
assignments = solve_recursive(letters)
print(assignments)
