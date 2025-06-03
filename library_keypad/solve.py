# Glitchy library keypad safe.
# The number of retracting bars indicates how many digits are in the correct
# position.

from itertools import product

from z3 import And, If, Int, Not, Or, Solver, Sum, sat

TEMPLATE = '''
  00  
 6  1 
 6  1 
  55  
 4  2 
 4  2 
  33  
'''.strip('\n')

TOP, TOP_RIGHT, BOT_RIGHT, BOT, BOT_LEFT, MID, TOP_LEFT = range(7)


def feedback(guess):
    '''Returns the number of correct digits in the correct positions given a guess.'''

    if isinstance(guess, int):
        guess = tuple(map(int, str(guess)))
    return sum(g == d for g, d in zip(guess, (8, 7, 9, 6)))


def str_to_segment(s):
    return {
        't': TOP,
        'tr': TOP_RIGHT,
        'br': BOT_RIGHT,
        'b': BOT,
        'bl': BOT_LEFT,
        'm': MID,
        'tl': TOP_LEFT,
    }[s]


def decode_segments(segment_strs):
    segments = []
    for g in segment_strs:
        segment = 0
        for s in g.split():
            segment |= 1 << int(str_to_segment(s))
        segments.append(segment)
    return segments


def display_segment(segment):
    out = TEMPLATE
    for i, v in enumerate(f'{segment:07b}'[::-1]):
        out = out.replace(str(i), 'X' if v == '1' else '.')
    return out


def display(segment_or_segments):
    if isinstance(segment_or_segments, int):
        return display_segment(segment_or_segments)

    outs = [display_segment(s).split('\n') for s in segment_or_segments]
    print(*(''.join(g) for g in zip(*outs)), sep='\n')
    print()


def merge(segments):
    out = []
    for g in zip(*segments):
        r = 0
        for v in g:
            r |= v
        out.append(r)
    return out


def subtract(orig_segments, segments_to_sub):
    segments = []
    for o, s in zip(orig_segments, segments_to_sub):
        segments.append(o & (0b1111111 - s))
    return segments


def invert(segments):
    return [0b1111111 - s for s in segments]


KNOWN_DIGITS = {
    k: decode_segments([v])[0]
    for k, v in {
        0: 't b tr tl br bl',
        1: 'tr br',
        2: 't m b tr bl',
        3: 't m b tr br',
        4: 'tl m tr br',
        5: 't m b tl br',
        6: 't m b tl bl br',
        7: 't tr br',
        8: 't m b tl tr bl br',
        9: 't m tl tr br b'
    }.items()
}

NUM_DIGITS = 4


def add_guess_knowledge(solver: Solver, zdigits, guess, ncorrect):
    correct_positions = [If(zdigits[i] == guess[i], 1, 0) for i in range(4)]
    solver.add(Sum(correct_positions) == ncorrect)


def interactive_z3(candidates):
    solver = Solver()
    zdigits = [Int(f'z{i}') for i in range(len(candidates))]
    for z, possible_digits in zip(zdigits, candidates):
        solver.add(Or(*(z == d for d in possible_digits)))

    while True:
        slns = find_all_solutions(solver, zdigits)
        if len(slns) == 1:
            print('Found solution:', slns[0])
            break
        elif len(slns) == 0:
            print('No solution')
            break

        print('Current candidates:\n')
        print(*map(format, slns))
        guess = input('Guess? [xxxx] > ')
        ncorrect = int(input('Number correct? > '))

        add_guess_knowledge(solver, zdigits, guess, ncorrect)


def format(digits):
    return int(''.join(str(d) for d in digits))


def find_all_solutions(solver: Solver, zdigits):
    solver.push()

    solutions = []
    while solver.check() == sat:
        model = solver.model()
        solution = [model[z].as_long() for z in zdigits]
        solutions.append(solution)

        block = []
        for d in model.decls():
            var = d()
            val = model[d]
            block.append(var != val)
        solver.add(Or(block))

    solver.pop()
    return sorted(solutions)


def main():
    segments = [0 for _ in range(NUM_DIGITS)]

    partial = decode_segments(['tr m b', 't br', 'tl tr br', 'tl bl m'])
    display(partial)

    candidates = []
    for v in partial:
        row = []
        for d, u in KNOWN_DIGITS.items():
            if (v | u) ^ u == 0:  # finds all possible digits
                row.append(d)
        candidates.append(row)

    print('Candidates:', candidates, end='\n\n')

    interactive_z3(candidates)

    pool = set(product(*candidates))


if __name__ == '__main__':
    main()
