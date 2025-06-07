import cv2
import numpy as np

img = cv2.imread('cropped.jpg')
assert img is not None, 'Failed to load cropped.jpg'

original_IDS = [
    [10, 18, 12, 8, 1],
    [22, -1, 19, 5, -1],
    [-1, 14, 16, 6, 2],
    [23, -1, -1, 13, -1],
    [24, 11, 17, 0, 7],
]

IDS = [row.copy() for row in original_IDS]

ROWS, COLS = 5, 5
tile_h, tile_w = img.shape[0] // ROWS, img.shape[1] // COLS


def slice_tiles():
    return [
        [
            img[r * tile_h:(r + 1) * tile_h,
                c * tile_w:(c + 1) * tile_w].copy() for c in range(COLS)
        ] for r in range(ROWS)
    ]


tiles = slice_tiles()  # current tile state
original_tiles = slice_tiles()  # saved initial state

WINDOW_NAME = 'Tile Grid'
knob_radius = 13

knobs = [(r, c) for r in range(ROWS - 1) for c in range(COLS - 1)]


def render():
    '''Reconstruct and display the full grid image with knobs and gradient-colored text'''
    grid_img = np.zeros_like(img)
    for r in range(ROWS):
        for c in range(COLS):
            tile = tiles[r][c].copy()
            id_val = IDS[r][c]

            # Normalize ID to 0.0–1.0
            norm = id_val / 24.0

            # Use HSV to RGB mapping for gradient (blue to red)
            hsv = np.uint8([[[int(240 * (1 - norm)), 255, 255]]])  # Hue: 240→0
            rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[0][0]
            color = tuple(int(x) for x in rgb)

            text = str('x' if id_val == -1 else id_val)
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        2)[0]
            text_x = (tile_w - text_size[0]) // 2
            text_y = (tile_h + text_size[1]) // 2
            cv2.putText(
                tile, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1,
                color, 2, cv2.LINE_AA
            )

            grid_img[r * tile_h:(r + 1) * tile_h,
                     c * tile_w:(c + 1) * tile_w] = tile

    for i, (r, c) in enumerate(knobs):
        cx = (c + 1) * tile_w
        cy = (r + 1) * tile_h
        cv2.circle(grid_img, (cx, cy), knob_radius, (128, 128, 128), -1)
        cv2.putText(
            grid_img, str(i), (cx - knob_radius // 2, cy + knob_radius // 2),
            cv2.FONT_HERSHEY_SIMPLEX, .8, (255, 0, 0), 2, cv2.LINE_AA
        )

    return grid_img


def rotate_clockwise(r, c):
    '''Rotate 4 tiles and their labels clockwise around the knob at (r, c)'''
    # Rotate image tiles
    A = tiles[r][c]
    B = tiles[r][c + 1]
    C = tiles[r + 1][c + 1]
    D = tiles[r + 1][c]
    tiles[r][c] = D
    tiles[r][c + 1] = A
    tiles[r + 1][c + 1] = B
    tiles[r + 1][c] = C

    # Rotate associated text IDs
    A = IDS[r][c]
    B = IDS[r][c + 1]
    C = IDS[r + 1][c + 1]
    D = IDS[r + 1][c]
    IDS[r][c] = D
    IDS[r][c + 1] = A
    IDS[r + 1][c + 1] = B
    IDS[r + 1][c] = C


def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        for r, c in knobs:
            cx = (c + 1) * tile_w
            cy = (r + 1) * tile_h
            if (x - cx)**2 + (y - cy)**2 <= knob_radius**2:
                rotate_clockwise(r, c)
                cv2.imshow(WINDOW_NAME, render())
                break


cv2.imshow(WINDOW_NAME, render())
cv2.setMouseCallback(WINDOW_NAME, click_event)

while True:
    key = cv2.waitKey(0)
    if key == ord('q'):
        break
    elif key == ord('r'):
        tiles = slice_tiles()  # reset to original
        IDS = [row.copy() for row in original_IDS]
        cv2.imshow(WINDOW_NAME, render())

cv2.destroyAllWindows()
