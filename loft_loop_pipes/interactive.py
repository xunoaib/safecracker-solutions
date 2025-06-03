# Generated with ChatGPT

import math
import sys

import pygame

# --- Settings ---
IMAGE_PATH = 'cropped.jpg'  # Replace with your image path
GRID_ROWS, GRID_COLS = 5, 5
NODE_RADIUS = 10
# BOX_OUTLINE_COLOR = (0, 0, 0)
NODE_COLOR = (0, 0, 0)
SELECTED_COLOR = (255, 0, 0)

DIRECTIONS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

# Axis-aligned direction offsets for edge placement (normalized to box size)
DIR_OFFSETS = {
    'N': (0.5, 0.1),
    'NE': (0.9, 0.1),
    'E': (0.9, 0.5),
    'SE': (0.9, 0.9),
    'S': (0.5, 0.9),
    'SW': (0.1, 0.9),
    'W': (0.1, 0.5),
    'NW': (0.1, 0.1),
}

# --- Main Program ---
pygame.init()
image = pygame.image.load(IMAGE_PATH)
img_w, img_h = image.get_size()
screen = pygame.display.set_mode((img_w, img_h))
pygame.display.set_caption("Image Grid Overlay")
clock = pygame.time.Clock()

box_w = img_w // GRID_COLS
box_h = img_h // GRID_ROWS

selected_nodes = set()

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(image, (0, 0))

    nodes = []  # Clear nodes every frame

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            box_x = col * box_w
            box_y = row * box_h
            # pygame.draw.rect(
            #     screen, BOX_OUTLINE_COLOR, (box_x, box_y, box_w, box_h), 1
            # )

            for direction in DIRECTIONS:
                fx, fy = DIR_OFFSETS[direction]
                node_x = int(box_x + fx * box_w)
                node_y = int(box_y + fy * box_h)

                rect = pygame.Rect(
                    node_x - NODE_RADIUS, node_y - NODE_RADIUS,
                    NODE_RADIUS * 2, NODE_RADIUS * 2
                )

                color = SELECTED_COLOR if (
                    (col, row), direction
                ) in selected_nodes else NODE_COLOR
                pygame.draw.circle(
                    screen, color, (node_x, node_y), NODE_RADIUS, 2
                )

                nodes.append(((col, row), direction, rect))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for (grid_pos, direction, node_rect) in nodes:
                if node_rect.collidepoint(mx, my):
                    key = (grid_pos, direction)
                    if key in selected_nodes:
                        selected_nodes.remove(key)
                    else:
                        selected_nodes.add(key)
                    print(f"Clicked box {grid_pos}, direction {direction}")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
