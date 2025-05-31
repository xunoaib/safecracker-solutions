import cv2
import numpy as np
import pygame

from rotating_symbol_tiles import parse_subimages


def numpy_to_surface(img_np):
    """Convert a NumPy image array to a Pygame surface."""
    return pygame.surfarray.make_surface(np.transpose(img_np, (1, 0, 2)))


def display_image_grid(image_grid):
    pygame.init()

    rows = len(image_grid)
    cols = len(image_grid[0])
    img_h, img_w, _ = image_grid[0][0].shape

    # Set up the display window
    window_width = cols * img_w
    window_height = rows * img_h
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("NumPy Image Grid")

    # Pre-convert all numpy arrays to surfaces
    surfaces = [[numpy_to_surface(img) for img in row] for row in image_grid]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the image grid
        for y in range(rows):
            for x in range(cols):
                screen.blit(surfaces[y][x], (x * img_w, y * img_h))

        pygame.display.flip()

    pygame.quit()


# Example usage (creates fake RGB images):
if __name__ == "__main__":
    im = cv2.imread('2025-05-30_22-15_safecracker_tiles_cropped.png')
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    subimages = parse_subimages(im)

    display_image_grid(subimages)
