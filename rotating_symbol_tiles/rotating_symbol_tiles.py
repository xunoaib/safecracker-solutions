#!/usr/bin/env python3
from heapq import heappop, heappush
from itertools import pairwise

from numpy import random

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


def serialize(grid: dict):
    return tuple(sorted(grid.items()))


def rotate(grid: dict, move: int):
    '''Applies the given move to a copy of the grid'''
    r, c = divmod(move, COLS - 1)  # upper left tile

    seq = [
        (r, c),
        (r, c + 1),
        (r + 1, c),
        (r + 1, c + 1),
        (r, c),
    ]

    ngrid = grid.copy()
    for a, b in pairwise(seq):
        ngrid[b] = grid[a]

    return ngrid


def solve(grid):
    visited = {serialize(grid)}

    i = 0
    q = [(dist_to_solve(grid), 0, i, grid, tuple())]

    while q:
        h, g, _, grid, path = heappop(q)

        if dist_to_solve(grid) == 0:
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


def main():
    if solution := solve(INIT):
        print(f'Found solution of length {len(solution)}')
        print(solution)
    else:
        print('No solution')


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
