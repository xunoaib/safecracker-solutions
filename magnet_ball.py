#!/usr/bin/env python3

import cv2
import numpy as np

rows, cols = 20, 25


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


def main():
    # image_to_grid()

    grid = load_grid('grid.txt')
    print(grid)


if __name__ == '__main__':
    main()
