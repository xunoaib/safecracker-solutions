import cv2
import numpy as np

img = cv2.imread('cropped.jpg')
assert img is not None, 'Failed to load cropped.jpg'

ROWS, COLS = 5, 5
tile_h, tile_w = img.shape[0] // ROWS, img.shape[1] // COLS

tiles = [
    [
        img[r * tile_h:(r + 1) * tile_h, c * tile_w:(c + 1) * tile_w].copy()
        for c in range(COLS)
    ] for r in range(ROWS)
]

WINDOW_NAME = 'Tile Grid'
knob_radius = 13

knobs = [(r, c) for r in range(ROWS - 1) for c in range(COLS - 1)]


def render():
    '''Reconstruct and display the full grid image with knobs'''
    grid_img = np.zeros_like(img)
    for r in range(ROWS):
        for c in range(COLS):
            grid_img[r * tile_h:(r + 1) * tile_h,
                     c * tile_w:(c + 1) * tile_w] = tiles[r][c]

    for r, c in knobs:
        cx = (c + 1) * tile_w
        cy = (r + 1) * tile_h
        cv2.circle(grid_img, (cx, cy), knob_radius, (128, 128, 128), -1)

    return grid_img


def rotate_clockwise(r, c):
    '''Rotate 4 tiles clockwise around the knob at (r, c)'''
    A = tiles[r][c]
    B = tiles[r][c + 1]
    C = tiles[r + 1][c + 1]
    D = tiles[r + 1][c]
    tiles[r][c] = D
    tiles[r][c + 1] = A
    tiles[r + 1][c + 1] = B
    tiles[r + 1][c] = C


def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Map click to knob
        for r, c in knobs:
            cx = (c + 1) * tile_w
            cy = (r + 1) * tile_h
            if (x - cx)**2 + (y - cy)**2 <= knob_radius**2:
                rotate_clockwise(r, c)
                cv2.imshow(WINDOW_NAME, render())
                break


cv2.imshow(WINDOW_NAME, render())
cv2.setMouseCallback(WINDOW_NAME, click_event)
while cv2.waitKey(0) != ord('q'):
    pass
cv2.destroyAllWindows()
