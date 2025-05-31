#!/usr/bin/env python3

import cv2

ROWS = COLS = 5


def parse_subimages(im):
    '''Parses an images into subimages as a 5x5 list'''

    h, w, _ = im.shape
    rowsize = h / ROWS
    colsize = w / COLS
    subimages = []

    for r in range(ROWS):
        row = []
        for c in range(COLS):
            ystart = int(r * rowsize)
            yend = int(ystart + rowsize)
            xstart = int(c * colsize)
            xend = int(xstart + colsize)
            subim = im[ystart:yend, xstart:xend]
            print((xstart, ystart), (xend, yend))
            if 0 in subim.shape:
                print('Empty image')
            row.append(subim)
        subimages.append(row)

    return subimages


def main():

    im = cv2.imread('2025-05-30_22-15_safecracker_tiles_cropped.png')
    subimages = parse_subimages(im)

    # for r, row in enumerate(subimages):
    #     for c, subim in enumerate(row):
    #         cv2.imwrite(f'tile_{r}_{c}.png', subim)


if __name__ == '__main__':
    main()
