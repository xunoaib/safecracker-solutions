#!/usr/bin/env python3

ROWS = COLS = 5


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


def main():
    print('cost to solve:', dist_to_solve(INIT))


# [23, 4, 14, 10, 17]
# [8, 13, 24, 3, 9]
# [0, 21, 2, 18, 11]
# [19, 12, 22, 1, 7]
# [6, 16, 5, 15, 20]

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

if __name__ == '__main__':
    main()
