#!/usr/bin/env python3
from functools import cache
from heapq import heappop, heappush
from itertools import count, pairwise
from typing import Callable

from tabulate import tabulate

ROWS = COLS = 5

MOVES = tuple(range(16))


def dist(src, tar):
    return abs(tar[0] - src[0]) + abs(tar[1] - src[1])


def list_to_dict(grid):
    return {
        (r, c): v
        for r, line in enumerate(grid)
        for c, v in enumerate(line)
    }


def find_num_pos(grid, num):
    return next(
        (
            (r, c) for r in range(ROWS)
            for c in range(COLS) if grid[r, c] == num
        ), None
    )


def dist_to_solve(grid):
    '''Sum of distances of tiles from their correct positions (NOT admissible)'''
    cost = 0
    for pos, num in grid.items():
        goal_pos = find_num_pos(GOAL, num)
        if goal_pos is not None:
            cost += dist(pos, goal_pos)
    return cost


def dist_to_solve_numbers(grid, numbers):
    cost = 0
    num_to_pos = {v: k for k, v in grid.items()}

    for num in numbers:
        goal_pos = find_num_pos(GOAL, num)
        if goal_pos is not None:
            cost += dist(pos, goal_pos)
    return cost


def serialize(grid: dict):
    return tuple(sorted(grid.items()))


def rotate(grid: dict, move: int):
    '''Applies the given move to a copy of the grid'''
    r, c = divmod(move, COLS - 1)  # upper left tile

    seq = [
        (r, c),
        (r, c + 1),
        (r + 1, c + 1),
        (r + 1, c),
        (r, c),
    ]

    ngrid = grid.copy()
    for a, b in pairwise(seq):
        ngrid[b] = grid[a]

    return ngrid


def solve_custom(grid, solved: Callable, heuristic: Callable):
    visited = {serialize(grid)}

    counter = count()
    q = [(heuristic(grid), 0, next(counter), grid, tuple())]

    max_len = 0

    while q:
        h, g, i, grid, path = heappop(q)

        if len(path) > max_len:
            max_len = len(path)
            print(f'Expanding search to {max_len} moves')

        # if len(path) > 150:
        #     continue

        if solved(grid):
            return grid, path

        for move in MOVES:
            new_grid = rotate(grid, move)
            new_serial = serialize(new_grid)
            if new_serial not in visited:
                visited.add(new_serial)
                heappush(
                    q, (
                        heuristic(new_grid) + g + 1,
                        g + 1,
                        next(counter),
                        new_grid,
                        path + (move, ),
                    )
                )


def solve(grid):
    visited = {serialize(grid)}

    i = 0
    q = [(dist_to_solve(grid), 0, i, grid, tuple())]

    max_len = 0

    while q:
        _, g, _, grid, path = heappop(q)

        if len(path) > max_len:
            max_len = len(path)
            print(f'Expanding search to {max_len} moves')

        if len(path) > 150:
            continue

        if dist_to_solve(grid) == 0:
            __import__('pprint').pprint(grid)
            return path

        for move in MOVES:
            new_grid = rotate(grid, move)
            new_serial = serialize(new_grid)
            if new_serial not in visited:
                visited.add(new_serial)
                heappush(
                    q, (
                        dist_to_solve(new_grid), g + 1, i + 1, new_grid, path +
                        (move, )
                    )
                )
                i += 1


def print_grid(grid: dict):
    # for r in range(ROWS):
    #     print(','.join(str(grid[r, c]) for c in range(COLS)))

    rows = [[grid[r, c] for c in range(COLS)] for r in range(ROWS)]
    print(tabulate(rows, tablefmt='plain'))


def main():

    # solution = (
    #     9, 1, 2, 4, 1, 0, 7, 2, 9, 14, 15, 4, 0, 1, 6, 6, 2, 6, 6, 11, 15, 11,
    #     6, 6, 9, 13, 9, 13, 9, 5, 0, 0, 6, 13, 13, 14, 12, 12, 13, 13, 13, 15,
    #     11, 11, 14, 13, 12, 15, 15, 15, 12, 13, 14, 14, 14, 15, 10, 2, 1, 6, 2,
    #     2, 2, 3, 3, 3, 1, 2, 3, 7, 7, 7, 11, 15, 11, 11, 7, 15, 15, 4, 4, 4, 8,
    #     4, 0, 12, 12, 13, 14, 14, 12, 13, 14, 14, 12, 12, 12, 13, 13, 13, 12,
    #     3, 3, 3, 2, 3, 2, 3, 3, 3, 2, 2, 2, 3, 3, 0, 1, 3, 2, 0, 0, 0, 12, 12,
    #     12, 13, 14, 15, 14, 13, 12, 15, 15, 15, 14, 15, 15, 14, 14, 14, 15, 14,
    #     12, 13, 14, 14, 14, 12, 12, 13, 12, 12, 14, 14, 12, 13, 14, 14, 13, 13,
    #     13, 14, 13, 12, 13, 12, 12, 12, 13, 13, 13, 12, 12, 12, 13, 12, 12
    # )
    # grid = INIT
    # print_grid(grid)
    # for m in solution:
    #     grid = rotate(grid, m)
    #     print()
    #     print('move', m, divmod(m, COLS + 1))
    #     print()
    #     print_grid(grid)
    #     input()
    # return

    # if solution := solve(INIT):
    #     print(f'Found solution of length {len(solution)}')
    #     print(solution)
    # else:
    #     print('No solution')

    grid = INIT

    def solved_up_to(grid, n):
        '''Returns whether tiles from 0 through n are solved'''
        for j in range(n + 1):
            src = find_num_pos(grid, j)
            tar = find_num_pos(GOAL, j)
            if None not in (src, tar) and src != tar:
                return False
        return True

    def heuristic_up_to(grid, n):
        '''Heuristic cost function only considering tiles from 0 through n'''
        cost = 0
        for j in range(n + 1):
            src = find_num_pos(grid, j)
            tar = find_num_pos(GOAL, j)
            if None not in (src, tar):
                cost += sum(abs(a - b) for a, b in zip(src, tar))
        return cost

    for idx in range(ROWS * COLS):
        n = GOAL[divmod(idx, COLS)]

        def solved(grid, n=n):
            return solved_up_to(grid, n)

        def heuristic(grid, n=n):
            return heuristic_up_to(grid, n)

        print('Solving for tile', n)
        grid, path = solve_custom(grid, solved, heuristic)
        print(path)
        print_grid(grid)
        break


INIT = list_to_dict([[r * COLS + c for c in range(COLS)] for r in range(ROWS)])
GOAL = list_to_dict(
    [
        [23, 4, 14, -1, -1],
        [8, 13, 24, 3, -1],
        [0, 21, 2, 18, 11],
        [-1, 12, 22, 1, 7],
        [-1, -1, 5, 15, 20],
    ]
)

# [23, 4, 14, 10, 17]
# [8, 13, 24, 3, 9]
# [0, 21, 2, 18, 11]
# [19, 12, 22, 1, 7]
# [6, 16, 5, 15, 20]

if __name__ == '__main__':
    main()
