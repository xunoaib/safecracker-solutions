import sys

import cv2
import numpy as np
import pygame

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
            if 0 in subim.shape:
                print('Empty image')
            row.append(subim)
        subimages.append(row)

    return subimages


def numpy_to_surface(img_np):
    """Convert a NumPy image array to a Pygame surface."""
    return pygame.surfarray.make_surface(np.transpose(img_np, (1, 0, 2)))


def display_image_grid(image_grid_with_ids):
    pygame.init()

    rows = len(image_grid_with_ids)
    cols = len(image_grid_with_ids[0])
    img_h, img_w, _ = image_grid_with_ids[0][0][0].shape

    window_width = cols * img_w
    window_height = rows * img_h
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("NumPy Image Grid")

    # Pre-convert all numpy arrays to surfaces
    surfaces = [
        [numpy_to_surface(img_id[0]) for img_id in row]
        for row in image_grid_with_ids
    ]

    font = pygame.font.SysFont(None, 24)
    selected = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                col = mx // img_w
                row = my // img_h

                if row < rows and col < cols:
                    if selected is None:
                        selected = (row, col)
                    elif selected == (row, col):
                        selected = None
                    else:
                        # Swap
                        r1, c1 = selected
                        image_grid_with_ids[row][col], image_grid_with_ids[r1][
                            c1] = image_grid_with_ids[r1][
                                c1], image_grid_with_ids[row][col]
                        surfaces[row][col], surfaces[r1][c1] = surfaces[r1][
                            c1], surfaces[row][col]
                        selected = None

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                # Print current configuration of image IDs
                current_ids = [
                    [img_id[1] for img_id in row]
                    for row in image_grid_with_ids
                ]
                print("Current grid configuration:")
                for row in current_ids:
                    print(row)
                sys.stdout.flush()  # Ensure output appears immediately

        screen.fill((0, 0, 0))
        for y in range(rows):
            for x in range(cols):
                px = x * img_w
                py = y * img_h
                screen.blit(surfaces[y][x], (px, py))

                if selected == (y, x):
                    pygame.draw.rect(
                        screen, (255, 255, 0), (px, py, img_w, img_h), 3
                    )

                image_id = image_grid_with_ids[y][x][1]
                text_surface = font.render(
                    str(image_id), True, (255, 255, 255)
                )
                screen.blit(text_surface, (px + 5, py + 5))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    im = cv2.imread('2025-05-30_22-15_safecracker_tiles_cropped.png')
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    subimages = parse_subimages(im)

    # Tag each image with its original ID
    numbered_subimages = []
    count = 0
    for row in subimages:
        numbered_row = []
        for img in row:
            numbered_row.append((img, count))
            count += 1
        numbered_subimages.append(numbered_row)

    display_image_grid(numbered_subimages)
