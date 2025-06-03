# Generated with ChatGPT

import math
import sys

import pygame

# --- Settings ---
IMAGE_PATH = 'cropped.jpg'  # Replace with your image path
GRID_ROWS, GRID_COLS = 5, 5
NODE_RADIUS = 5
BOX_OUTLINE_COLOR = (0, 255, 0)
NODE_COLOR = (255, 0, 0)
DIRECTIONS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
DIR_ANGLES = {
    'N': 270,
    'NE': 315,
    'E': 0,
    'SE': 45,
    'S': 90,
    'SW': 135,
    'W': 180,
    'NW': 225
}


def angle_to_offset(angle_deg, distance):
    rad = math.radians(angle_deg)
    return int(distance * math.cos(rad)), int(distance * math.sin(rad))


# --- Main Program ---
pygame.init()
image = pygame.image.load(IMAGE_PATH)
img_w, img_h = image.get_size()
screen = pygame.display.set_mode((img_w, img_h))
pygame.display.set_caption("Image Grid Overlay")
clock = pygame.time.Clock()

# Calculate box sizes
box_w = img_w // GRID_COLS
box_h = img_h // GRID_ROWS

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(image, (0, 0))

    nodes = []  # Clear nodes every frame to rebuild

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            box_x = col * box_w
            box_y = row * box_h
            pygame.draw.rect(
                screen, BOX_OUTLINE_COLOR, (box_x, box_y, box_w, box_h), 1
            )

            center_x = box_x + box_w // 2
            center_y = box_y + box_h // 2
            dist = min(box_w, box_h) // 3

            for direction in DIRECTIONS:
                dx, dy = angle_to_offset(DIR_ANGLES[direction], dist)
                node_x = center_x + dx
                node_y = center_y + dy
                pygame.draw.circle(
                    screen, NODE_COLOR, (node_x, node_y), NODE_RADIUS, 1
                )
                nodes.append(
                    (
                        (col, row), direction,
                        pygame.Rect(
                            node_x - NODE_RADIUS, node_y - NODE_RADIUS,
                            NODE_RADIUS * 2, NODE_RADIUS * 2
                        )
                    )
                )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for (grid_pos, direction, node_rect) in nodes:
                if node_rect.collidepoint(mx, my):
                    print(f"Clicked box {grid_pos}, direction {direction}")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
