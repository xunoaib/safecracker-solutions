# Mastermind Phone Puzzle
# Must guess a 4 digit code in 5 guesses.
# Feedback is given for each digit in the guess, indicating whether it is:
# - present in the solution and in the correct position
# - present in the solution but in the incorrect position
# - not present in the solution

import sys
from collections import defaultdict
from itertools import product

WRONG, PARTIAL, CORRECT = range(3)


class Guesser:
    '''Accepts guesses and responses and generates possible candidates'''

    def __init__(self):
        self.responses = []

    def add(self, guess: tuple[int, ...], response: tuple[int, ...]):
        self.responses.append((guess, response))

    def candidates(self):
        for candidate in product(range(1, 10), repeat=4):
            if all(
                feedback(guess, candidate) == response
                for guess, response in self.responses
            ):
                yield candidate


def feedback(guess, solution):
    '''Returns feedback for a guess given the solution'''

    result = tuple()
    for s, g in zip(solution, guess):
        if g == s:
            result += (CORRECT, )
        elif g in solution:
            result += (PARTIAL, )
        else:
            result += (WRONG, )
    return result


def interactive(candidates):
    '''Allows the user to manually enter their own guesses and feedback to
    narrow down possible codes'''

    guesser = Guesser()
    while True:
        candidates = list(guesser.candidates())

        print('Found', len(candidates), 'candidates')
        if len(candidates) == 1:
            print('Found solution: ', *candidates[0], sep='')
            break
        elif len(candidates) == 0:
            print('No solution')
            break
        elif len(candidates) < 100:
            print('Current candidates:\n')
            print(*map(format, candidates))

        print()
        guess_str = input('\033[93mGuess? [xxxx] > \033[0m')
        guess = tuple(map(int, guess_str))
        response_str = input(
            '\033[93mResponse? [wcp] (w)rong/(c)orrect/(p)artial > \033[0m'
        ).lower()
        response = tuple(
            {
                'w': WRONG,
                'c': CORRECT,
                'p': PARTIAL
            }[v] for v in response_str
        )
        guesser.add(guess, response)
        print()


# def automatic_z3(candidates):
#     '''Automatically suggests guesses, accepting feedback and using z3 to
#     narrow down possible codes'''
#
#     solver, zdigits = init_solver(candidates)
#     print(zdigits)
#     while True:
#         if len(slns) == 1:
#             print('\n\033[92;1mSolution: ', *slns[0], '\033[0m', sep='')
#             break
#
#         elif len(slns) == 0:
#             print('\033[91;1mNo solution\033[0m')
#             break
#
#         guess = best_guess(slns)
#
#         print('Candidates:\n')
#         print('\033[38;5;248m' + ' '.join(map(format, slns)) + '\033[m')
#         print('\n\033[93;1mGuess: ', *guess, '\033[0m', sep='')
#
#         # We could read input from the user here, but for ease of use, we'll
#         # just simulate what the actual response would be.
#
#         # ncorrect = int(input('Number correct? > '))
#         ncorrect = feedback(guess)
#         print('\033[96mFeedback:', ncorrect, 'correct\033[0m')
#
#         add_guess_knowledge(solver, zdigits, guess, ncorrect)


def format(digits):
    return ''.join(str(d) for d in digits)


def score_guess(guess, solution_candidates):
    '''Returns a score indicating how well the guess splits the solution candidates'''

    buckets = defaultdict(list)
    for code in solution_candidates:
        response = sum(g == c for g, c in zip(guess, code))
        buckets[response].append(code)

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


def main():

    candidates = [list(range(1, 10)) for _ in range(10)]

    # g = Guesser()
    # g.add((1, 2, 3, 4), (WRONG, WRONG, PARTIAL, CORRECT))
    # print(list(g.candidates()))
    # exit(0)

    if '-i' in sys.argv:
        interactive(candidates)
    # else:
    #     print('Automatic solving:')
    #     automatic_z3(candidates)


if __name__ == '__main__':
    main()
