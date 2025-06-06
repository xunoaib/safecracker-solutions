#!/usr/bin/env python3
import sys
from heapq import heappop, heappush
from itertools import count, pairwise
from typing import Callable

ROWS = COLS = 5
ALL_COORDS = tuple((r, c) for r in range(ROWS) for c in range(COLS))

MOVES = tuple(range(16))

GOAL = (
    (0, 1, 2, -1, -1),
    (5, 6, 7, 8, -1),
    (10, 11, 12, 13, 14),
    (-1, 16, 17, 18, 19),
    (-1, -1, 22, 23, 24),
)

INIT = (
    (10, 18, 12, 8, 1),
    (22, -1, 19, 5, -1),
    (-1, 14, 16, 6, 2),
    (23, -1, -1, 13, -1),
    (24, 11, 17, 0, 7),
)

GOAL_POSITIONS = {GOAL[r][c]: (r, c) for r, c in ALL_COORDS}

ROTATION_SEQUENCE = [
    (0, 0),
    (0, 1),
    (1, 1),
    (1, 0),
    (0, 0),
]


def dist(src, tar):
    return abs(tar[0] - src[0]) + abs(tar[1] - src[1])


def tile_pos(grid: tuple[tuple, ...], num: int):
    '''Finds the (r,c) position of a given tile in the grid'''
    for r, c in ALL_COORDS:
        if grid[r][c] == num:
            return r, c


def dist_to_solve(grid):
    '''Sum of distances of tiles from their correct positions (NOT
    admissible)'''
    cost = 0
    for pos, num in grid.items():
        goal_pos = tile_pos(GOAL, num)
        if goal_pos is not None:
            cost += dist(pos, goal_pos)
    return cost


def dist_to_solve_numbers(grid, numbers):
    cost = 0
    num_to_pos = {v: k for k, v in grid.items()}
    for num in numbers:
        goal_pos = tile_pos(GOAL, num)
        if goal_pos is not None:
            cost += dist(pos, goal_pos)
    return cost


def rotate(grid: tuple[tuple, ...], move: int):
    '''Applies the given move to a copy of the grid'''
    r, c = divmod(move, COLS - 1)  # upper left tile
    ngrid = list(map(list, grid))
    for (src_r, src_c), (tar_r, tar_c) in pairwise(ROTATION_SEQUENCE):
        ngrid[r + tar_r][c + tar_c] = grid[r + src_r][c + src_c]
    return tuple(map(tuple, ngrid))


def solve_custom(
    grid: tuple[tuple, ...], solved: Callable, heuristic: Callable
):
    visited = {grid}

    counter = count()
    q = [(heuristic(grid), 0, next(counter), grid, tuple())]

    max_len = 0

    while q:
        h, g, i, grid, path = heappop(q)

        if len(path) > max_len:
            max_len = len(path)

        if solved(grid):
            return grid, path

        for move in MOVES:
            new_grid = rotate(grid, move)
            if new_grid not in visited:
                visited.add(new_grid)
                heappush(
                    q, (
                        heuristic(new_grid) + g + 1,
                        g + 1,
                        next(counter),
                        new_grid,
                        path + (move, ),
                    )
                )
    print('No solution')
    exit()


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


def make_color_map(grid: dict):
    '''Generates a color map (value -> ANSI color code)'''
    # vals = sorted(v for v in grid.values() if v != -1)
    vals = tuple(v for row in grid for v in row)
    min_val, max_val = min(vals), max(vals)
    range_val = max_val - min_val if max_val != min_val else 1

    color_map = {}
    for val in vals:
        norm = (val - min_val) / range_val  # normalize between 0 and 1
        r = int(255 * norm)
        g = int(255 * (1 - norm))
        b = 128
        color_map[val] = f"\033[38;2;{r};{g};{b}m{val:>2}\033[0m"
    return color_map


def print_grid(grid: dict):
    color_map = make_color_map(grid)
    rows = [
        [
            color_map[grid[r][c]] if grid[r][c] != -1 else '•'
            for c in range(COLS)
        ] for r in range(ROWS)
    ]
    for row in rows:
        print(*(f' {v:>2}' for v in row))


def simulate_solution():
    print('Simulating solution')
    solution = (
        9, 1, 2, 4, 1, 0, 7, 2, 9, 14, 15, 4, 0, 1, 6, 6, 2, 6, 6, 11, 15, 11,
        6, 6, 9, 13, 9, 13, 9, 5, 0, 0, 6, 13, 13, 14, 12, 12, 13, 13, 13, 15,
        11, 11, 14, 13, 12, 15, 15, 15, 12, 13, 14, 14, 14, 15, 10, 2, 1, 6, 2,
        2, 2, 3, 3, 3, 1, 2, 3, 7, 7, 7, 11, 15, 11, 11, 7, 15, 15, 4, 4, 4, 8,
        4, 0, 12, 12, 13, 14, 14, 12, 13, 14, 14, 12, 12, 12, 13, 13, 13, 12,
        3, 3, 3, 2, 3, 2, 3, 3, 3, 2, 2, 2, 3, 3, 0, 1, 3, 2, 0, 0, 0, 12, 12,
        12, 13, 14, 15, 14, 13, 12, 15, 15, 15, 14, 15, 15, 14, 14, 14, 15, 14,
        12, 13, 14, 14, 14, 12, 12, 13, 12, 12, 14, 14, 12, 13, 14, 14, 13, 13,
        13, 14, 13, 12, 13, 12, 12, 12, 13, 13, 13, 12, 12, 12, 13, 12, 12
    )
    grid = INIT
    print_grid(grid)
    for m in solution:
        grid = rotate(grid, m)
        print()
        print('move', m, divmod(m, COLS + 1))
        print()
        print_grid(grid)
        # input()


def solve_traditional():
    print('Solving traditionally')
    if solution := solve(INIT):
        print(f'Found solution of length {len(solution)}')
        print(solution)
    else:
        print('No solution')
    return


def solve_new():
    print('Solving new')

    def solved_up_to(grid, n):
        '''Returns whether tiles from 0 through n are solved'''
        for j in range(n + 1):
            r, c = divmod(j, COLS)
            if grid[r][c] != GOAL[r][c]:
                return False
        return True

    def heuristic_up_to(grid, n):
        '''Heuristic cost function only considering tiles from 0 through n'''
        cost = 0
        for j in range(n + 1):
            src = tile_pos(grid, j)
            tar = divmod(j, COLS)
            if None not in (src, tar):
                cost += sum(abs(a - b) for a, b in zip(src, tar))
        return .7 * cost

    all_moves = []

    # Incrementally solve a subset of tiles to improve runtime
    ns = list(range(11)) + [ROWS * COLS - 1]
    # ns = list(range(ROWS * COLS))
    # ns = [3, 4, 5, 6, 7, 8, 9, 10, 11, 24]
    # ns = [0, 1, 2, 4, 5, 6, 7, 9, 10, 11, ROWS * COLS - 1]

    grid = INIT
    for n in ns:

        def solved(grid, n=n):
            return solved_up_to(grid, n)

        def heuristic(grid, n=n):
            return heuristic_up_to(grid, n)

        print(f'\n>>> Solving tiles through {n}', '\n')
        grid, moves = solve_custom(grid, solved, heuristic)
        print_grid(grid)
        all_moves.append(moves)
        print()
        print('Steps:', moves, f'({sum(map(len, all_moves))} total)')

        if solved(grid, ROWS * COLS - 1):
            break

        # input()

    print()
    for i, m in enumerate(all_moves):
        print(f'Tile {i:>2} -', *m)

    solution = tuple(m for moves in all_moves for m in moves)
    print(f'\nTotal solution ({len(solution)} total)\n')
    print(solution)

    print()
    print_grid(grid)


def main():

    if '-t' in sys.argv:
        solve_traditional()
    elif '-s' in sys.argv:
        simulate_solution()
    else:
        solve_new()


if __name__ == '__main__':
    main()
