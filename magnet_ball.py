#!/usr/bin/env python3

import cv2
import numpy as np

rows, cols = 20, 25


class Tile:
    WALL = 'x'
    EMPTY = '.'
    START = 's'
    END = 'e'


def image_to_bitmap(im):

    out = im.copy()
    bitmap = []

    h, w = im.shape
    rowsize = h // rows + .75
    colsize = w // cols + .75

    for r in range(rows):
        row = []
        cv2.line(out, (0, int(r * rowsize)), (w, int(r * rowsize)), 127)
        for c in range(cols):
            x = int(c * colsize)
            y = int(r * rowsize)
            im_sub = im[y:int(y + rowsize), x:int(x + colsize)]
            sh, sw = im_sub.shape
            pixels = sh * sw
            avg_val = np.sum(im_sub) / pixels
            row.append('x' if avg_val < 140 else '.')
            cv2.line(out, (int(c * colsize), 0), (int(c * colsize), h), 127)
        bitmap.append(row)

    cv2.imshow('out', out)
    cv2.waitKey()

    return bitmap


def image_to_grid():
    '''Parses walls from a black and white preprocessed image (excludes goal tiles)'''
    im = cv2.imread('magnet_ball_bw.png')
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    bitmap = image_to_bitmap(im)
    for row in bitmap:
        print(''.join(row))


def load_grid(fname):
    return {
        (r, c): ch
        for r, line in enumerate(open(fname))
        for c, ch in enumerate(line) if ch in 'x.se'
    }


def find_accessible_from(r, c):
    pass


def solve(grid):
    start = next(p for p, ch in grid.items() if ch == Tile.START)
    grid[start] = Tile.EMPTY
    goals = [p for p, ch in grid.items() if ch == Tile.END]
    visited = set()

    q = [(start, tuple())]
    while q:
        p, path = q.pop(0)
        if p in goals:
            return path

        for n in neighbors(grid, p):
            if n not in visited:
                visited.add(n)
                q.append((n, path + (n, )))


def neighbors(grid, pos):
    for dir in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if end_pos := walk_in_dir(grid, pos, dir):
            yield end_pos


def walk_in_dir(grid: dict[tuple[int, int], str], pos, dir: tuple[int, int]):
    '''Attempts to move as far as possible in one direction.
    Returns the final resting position, or None if ball goes out of bounds or
    doesn't move at all'''

    start = pos
    while True:
        npos = (pos[0] + dir[0], pos[1] + dir[1])

        if npos not in grid:
            return None

        ch = grid[npos]

        if ch == Tile.WALL:
            break

        pos = npos

        if ch == Tile.END:
            break

    if pos == start:
        return None

    return pos


def main():
    # image_to_grid()
    grid = load_grid('grid.txt')
    if path := solve(grid):
        print(path)
    else:
        print('No solution')


if __name__ == '__main__':
    main()
