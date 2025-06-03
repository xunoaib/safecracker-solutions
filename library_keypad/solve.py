# Glitchy library keypad safe.
# The number of retracting bars indicates the number of correctly placed digits.
import sys
from collections import defaultdict
from itertools import product

from z3 import If, Int, Or, Solver, Sum, sat

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


def add_guess_knowledge(solver: Solver, zdigits: list, guess, ncorrect):
    '''Adds the result of a guess to the knowledge base'''

    correct_positions = [If(zdigits[i] == guess[i], 1, 0) for i in range(4)]
    solver.add(Sum(correct_positions) == ncorrect)


def init_solver(candidates):
    solver = Solver()
    zdigits = [Int(f'z{i}') for i in range(len(candidates))]
    for z, possible_digits in zip(zdigits, candidates):
        solver.add(Or(*(z == d for d in possible_digits)))
        solver.add(z >= 1)
        solver.add(z <= 9)
    return solver, zdigits


def interactive_z3(candidates):
    '''Allows the user to manually enter their own guesses and feedback, using
    z3 to narrow down possible codes'''

    solver, zdigits = init_solver(candidates)
    while True:
        slns = find_all_solutions(solver, zdigits)
        if len(slns) == 1:
            print('Found solution: ', *slns[0], sep='')
            break
        elif len(slns) == 0:
            print('No solution')
            break

        print('Current candidates:\n')
        print(*map(format, slns))
        guess = input('Guess? [xxxx] > ')
        ncorrect = int(input('Number correct? > '))

        add_guess_knowledge(solver, zdigits, guess, ncorrect)


def automatic_z3(candidates):
    '''Automatically suggests guesses, accepting feedback and using z3 to
    narrow down possible codes'''

    solver, zdigits = init_solver(candidates)
    while True:
        slns = find_all_solutions(solver, zdigits)

        if len(slns) == 1:
            print('\n\033[92;1mSolution: ', *slns[0], '\033[0m', sep='')
            break

        elif len(slns) == 0:
            print('\033[91;1mNo solution\033[0m')
            break

        guess = best_guess(slns)

        print('Candidates:\n')
        print('\033[38;5;248m' + ' '.join(map(format, slns)) + '\033[m')
        print('\n\033[93;1mGuess: ', *guess, '\033[0m', sep='')

        # We could read input from the user here, but for ease of use, we'll
        # just simulate what the actual response would be.

        # ncorrect = int(input('Number correct? > '))
        ncorrect = feedback(guess)
        print('\033[96mFeedback:', ncorrect, 'correct\033[0m')

        add_guess_knowledge(solver, zdigits, guess, ncorrect)


def format(digits):
    return ''.join(str(d) for d in digits)


def score_guess(guess, solution_candidates):
    '''Returns a score indicating how well the guess splits the solution candidates'''

    buckets = defaultdict(list)
    for code in solution_candidates:
        feedback = sum(g == c for g, c in zip(guess, code))
        buckets[feedback].append(code)

    # a good guess minimizes the size of the largest bucket (worst-case).
    # however, im not 100% sure feedback frequency is the best metric to use.
    return max(len(b) for b in buckets.values())


def best_guess(solution_candidates):
    min_score = float('inf')
    best = None
    for guess in product(range(1, 10), repeat=4):
        score = score_guess(guess, solution_candidates)
        if score < min_score:
            min_score = score
            best = guess
    return best


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
    partial = decode_segments(['tr m b', 't br', 'tl tr br', 'tl bl m'])
    # display(partial)

    candidates = []
    for v in partial:
        row = []
        for d, u in KNOWN_DIGITS.items():
            if (v | u) ^ u == 0:  # finds all possible digits
                row.append(d)
        candidates.append(row)

    if '-i' in sys.argv:
        print('Candidates:', candidates, end='\n\n')
        interactive_z3(candidates)

    elif '-a' in sys.argv:
        print('Automatic solving:')
        automatic_z3(candidates)

    else:
        print(
            'No option selected. Pass -i for interactive or -a for automatic'
        )


if __name__ == '__main__':
    main()
