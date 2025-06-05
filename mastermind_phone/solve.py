# Mastermind Phone Puzzle
# Must guess a 4 digit code in 5 guesses.
# Feedback is given for each digit in the guess, indicating whether it is:
# - present in the solution and in the correct position
# - present in the solution but in the incorrect position
# - not present in the solution

import sys
from collections import defaultdict
from functools import cache
from itertools import product
from typing import Callable

WRONG, PARTIAL, CORRECT = range(3)

ALL_POSSIBLE_CODES = list(product(range(1, 10), repeat=4))


class Guesser:
    '''Accepts guesses and responses and generates possible candidates'''

    def __init__(self, first_response=(1, 2, 3, 4)):
        self.responses = []
        self.filters = []
        self.first_response = first_response

    def add(self, guess: tuple[int, ...], response: tuple[int, ...] | str):
        if isinstance(response, str):
            response = string_to_response(response)
        self.responses.append((guess, response))

    def add_filter(self, func: Callable):
        self.filters.append(func)

    def candidates(self):
        candidates = []
        for candidate in find_candidates(tuple(self.responses)):
            if all(validator(candidate) for validator in self.filters):
                candidates.append(candidate)
        return candidates

    def best_guess(self):
        if not self.responses and self.first_response:
            return self.first_response
        return _best_guess(self.candidates())

    def clear_responses(self):
        self.responses.clear()


class DataSource:

    def get(self, guesser: Guesser) -> tuple[tuple, tuple]:
        raise NotImplementedError(
            "Base class doesn't provide an implementation for get()"
        )


class ManualDataSource(DataSource):
    '''Allows user to enter guesses/responses'''

    def get(self, guesser: Guesser):
        guess_str = input('\033[93mGuess? [xxxx] > \033[0m')
        response_str = input(
            '\033[93mResponse? [wcp] (w)rong/(c)orrect/(p)artial > \033[0m'
        ).lower()

        guess = tuple(map(int, guess_str))
        response = string_to_response(response_str)
        return guess, response


class AutomaticDataSource(DataSource):
    '''Provides a guess and accepts feedback from the user'''

    def get(self, guesser: Guesser):
        guess = guesser.best_guess()
        assert guess is not None

        print('Guess: ', *guess, sep='')
        response_str = input(
            '\033[93mResponse? [wcp] (w)rong/(c)orrect/(p)artial > \033[0m'
        ).lower()
        response = string_to_response(response_str)
        return guess, response


def string_to_response(response_str: str):
    return tuple(map('wpc'.index, response_str))


@cache
def find_candidates(responses: tuple):
    candidates = []
    for candidate in ALL_POSSIBLE_CODES:
        if all(
            feedback(guess, candidate) == response
            for guess, response in responses
        ):
            candidates.append(candidate)
    return candidates.copy()


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


def solve_loop(guesser: Guesser, data_source: DataSource):
    '''DataSource generates guesses/responses'''

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

        guess, response = data_source.get(guesser)
        guesser.add(guess, response)
        print()


def format(digits):
    return ''.join(str(d) for d in digits)


def score_guess(guess, candidates):
    '''Returns a score indicating how well the guess splits the solution candidates'''

    buckets = defaultdict(list)
    for solution in candidates:
        response = feedback(guess, solution)
        buckets[response].append(solution)

    # a good guess minimizes the size of the largest bucket (worst-case).
    # however, im not 100% sure feedback frequency is the best metric to use.
    return max(len(b) for b in buckets.values())


def _best_guess(candidates):
    best = (float('inf'), None)
    for guess in ALL_POSSIBLE_CODES:
        score = score_guess(guess, candidates)
        best = min(best, (score, guess))
    return best[1]


def create_guesser():
    '''Creates and a configures a most informed guesser'''

    g = Guesser()

    # add prior knowledge that the last digit is always 9
    g.add_filter(lambda c: c[-1] == 9)

    # assume that digits are distinct
    g.add_filter(lambda c: len(set(c)) == len(c))

    return g


def main():

    # hardcode_first = None
    hardcode_first = (1, 2, 3, 4)

    if '-i' in sys.argv:
        data_source = ManualDataSource()
    else:
        data_source = AutomaticDataSource()

    guesser = create_guesser()

    solve_loop(guesser, data_source)


if __name__ == '__main__':
    main()
