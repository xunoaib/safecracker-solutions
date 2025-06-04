# Glitchy library keypad safe.
# The number of retracting bars indicates the number of correctly placed digits

import sys
from collections import defaultdict
from itertools import product

from z3 import If, Int, Or, Solver, Sum, sat

NUM_DIGITS = 4


def feedback(guess):
    '''Returns the number of correct digits in the correct positions given a guess.'''

    if isinstance(guess, int):
        guess = tuple(map(int, str(guess)))
    return sum(g == d for g, d in zip(guess, (8, 7, 9, 6)))


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
    print(zdigits)
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

    candidates = [list(range(1, 10)) for _ in range(10)]

    if '-i' in sys.argv:
        print('Candidates:', candidates, end='\n\n')
        interactive_z3(candidates)
    else:
        print('Automatic solving:')
        automatic_z3(candidates)


if __name__ == '__main__':
    main()
