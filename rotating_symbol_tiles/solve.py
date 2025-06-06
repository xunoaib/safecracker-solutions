#!/usr/bin/env python3
import sys
from collections import Counter
from functools import cache
from heapq import heappop, heappush
from itertools import count, pairwise
from time import time
from typing import Callable

Grid = tuple[tuple[int, ...], ...]

ROWS = COLS = 5
ALL_COORDS = tuple((r, c) for r in range(ROWS) for c in range(COLS))

MAX_MOVES = 62
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


def tile_pos(grid: Grid, num: int):
    '''Finds the (r,c) position of a given tile in the grid'''
    for r, c in ALL_COORDS:
        if grid[r][c] == num:
            return r, c


def rotate(grid: Grid, move: int):
    '''Applies the given move to a copy of the grid'''
    r, c = divmod(move, COLS - 1)  # upper left tile
    ngrid = list(map(list, grid))
    for (src_r, src_c), (tar_r, tar_c) in pairwise(ROTATION_SEQUENCE):
        ngrid[r + tar_r][c + tar_c] = grid[r + src_r][c + src_c]
    return tuple(map(tuple, ngrid))


Path = tuple[int, ...]
HeapItem = tuple[int | float, int, int, Grid]
Solution = tuple[Grid, Path]


@cache
def find_all_solutions_up_to(grid: Grid, n: int, extra_moves_allowed) -> list:

    def solved(grid, n=n):
        return solved_up_to(grid, n)

    def heuristic(grid, n=n):
        return heuristic_up_to(grid, n)

    solutions = _solve_up_to(
        grid, solved, heuristic, find_all_solutions=True, extra_moves_allowed=extra_moves_allowed)
    assert isinstance(solutions, list)
    return solutions


# def find_solution_up_to(grid: Grid, n: int) -> tuple[Grid, Path]:
#
#     def solved(grid, n=n):
#         return solved_up_to(grid, n)
#
#     def heuristic(grid, n=n):
#         return heuristic_up_to(grid, n)
#
#     solutions = _solve_up_to(grid, solved, heuristic, find_all_solutions=False)
#     return solutions[0]


def _solve_up_to(
    grid: Grid,
    solved: Callable[[Grid], bool],
    heuristic: Callable[[Grid], int | float],
    find_all_solutions: bool = False,
    max_moves=MAX_MOVES,
    extra_moves_allowed: int = 0,  # allow this many moves above the optimal solution
):
    solutions: list[tuple[Grid, Path]] = []
    counter = count()
    max_len = 0
    start_time = time()

    visited: dict[Grid, Path] = {grid: tuple()}
    q: list[HeapItem] = [(heuristic(grid), 0, next(counter), grid)]

    while q:
        h, g, i, grid = heappop(q)

        path = visited[grid]
        if len(path) > max_len:
            max_len = len(path)
            elapsed = time() - start_time
            # print(f'{elapsed:>4.1f}s  New max length', max_len)

        if solutions and g + heuristic(grid) > len(solutions[0][1]) + extra_moves_allowed:
            continue

        if solved(grid):
            # print('Found solution', len(path), path)
            if not find_all_solutions:
                return grid, path
            solutions.append((grid, path))
        elif max_moves is not None and len(path) > max_moves:
            continue

        for move in MOVES:
            new_grid = rotate(grid, move)
            if new_grid not in visited:
                visited[new_grid] = path + (move, )
                heappush(
                    q, (
                        heuristic(new_grid) + g + 1,
                        g + 1,
                        next(counter),
                        new_grid,
                    )
                )

    if find_all_solutions:
        return solutions

    print('No solution')
    exit()


def make_color_map(grid: Grid):
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


def print_grid(grid: Grid):
    color_map = make_color_map(grid)
    for row in grid:
        for v in row:
            s = color_map[v] if v != -1 else '•'
            print(f' {s:>2}', end='')
        print()


def simulate_solution():
    print('Simulating solution')
    solution = (
        14, 13, 12, 12, 8, 4, 0, 3, 3, 2, 1, 1, 7, 6, 6, 2, 3, 3, 11, 7, 3, 6,
        6, 5, 4, 4, 6, 6, 5, 5, 15, 14, 14, 10, 6, 15, 15, 11, 7, 10, 7, 3, 10,
        9, 8, 8, 12, 9, 12, 9, 10, 11, 14, 10, 15, 10, 15, 15, 12, 13, 14, 14
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


def solve_all_at_once():

    def heuristic(grid: Grid):
        return heuristic_up_to(grid, ROWS * COLS - 1)

    def solved(grid: Grid):
        return solved_up_to(grid, ROWS * COLS - 1)

    if solution := solve_up_to(INIT, solved, heuristic):
        print(f'Found solution of length {len(solution)}')
        print(solution)
    else:
        print('No solution')

    return solution


def solved_up_to(grid: Grid, n):
    '''Returns whether tiles from 0 through n are solved'''
    for j in range(n + 1):
        r, c = divmod(j, COLS)
        if grid[r][c] != GOAL[r][c]:
            return False
    return True


def heuristic_up_to(grid: Grid, n):
    '''Heuristic cost function only considering tiles from 0 through n'''
    cost = 0
    # TODO: iterate over each cell instead of searching for each number
    for j in range(n + 1):
        src = tile_pos(grid, j)
        tar = divmod(j, COLS)
        if src is not None and tar is not None:
            cost += sum(abs(a - b) for a, b in zip(src, tar))
    return .7 * cost


@cache
def recursive_solve(grid: Grid, n=0):
    if n > ROWS * COLS - 1:
        assert solved_up_to(grid, ROWS * COLS - 1)
        print('solved!')
        return tuple()

    extra_moves_allowed = 0

    solutions = find_all_solutions_up_to(
        grid, n, extra_moves_allowed=extra_moves_allowed)
    if not solutions:
        print(f'Level {n} => no solutions!')
        return False

    len_freq = Counter([len(path) for grid, path in solutions]).keys()
    print(f'Level {n} => {len(solutions)} solutions between lengths {
          min(len_freq)} and {max(len_freq)}')

    if n == ROWS*COLS-1 or n < 10:
        next_n = n+1
    else:
        next_n = ROWS*COLS-1

    for ngrid, path in solutions:
        result = recursive_solve(ngrid, next_n)
        if result is not False:
            return path + result


def solve_incremental_multi():
    if result := recursive_solve(INIT):
        print('Path:', result)
        print(len(result), 'moves')
    else:
        print('No solution')


def solve_incremental():
    print('Solving new')

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
        grid, moves = solve_up_to(grid, solved, heuristic)
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
        solve_all_at_once()
    elif '-s' in sys.argv:
        simulate_solution()
    elif '-m' in sys.argv:
        solve_incremental()
    else:
        solve_incremental_multi()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('interrupted')
