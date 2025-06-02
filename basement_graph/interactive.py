import json
import os

import pygame

ss_image = pygame.image.load('ss.png')
with open('nodes.json') as f:
    nodes = json.load(f)

# load/initialize existing links
LINKS_FILE = 'links.json'
if os.path.exists(LINKS_FILE):
    with open(LINKS_FILE) as f:
        links = set(tuple(sorted(link)) for link in json.load(f))
else:
    links = set()

pygame.init()
screen = pygame.display.set_mode(ss_image.get_size())
pygame.display.set_caption('Interactive Basement Linker')
clock = pygame.time.Clock()

selected_node = None
running = True
NODE_RADIUS = 18


def draw():
    screen.blit(ss_image, (0, 0))

    # draw links
    for id1, id2 in links:
        n1 = next(n for n in nodes if n['id'] == id1)
        n2 = next(n for n in nodes if n['id'] == id2)
        pygame.draw.line(
            screen, (0, 255, 0), (n1['x'], n1['y']), (n2['x'], n2['y']), 4
        )

    # draw nodes
    for node in nodes:
        color = (255, 255, 0) if selected_node == node['id'] else (0, 255, 0)
        pygame.draw.circle(
            screen, color, (node['x'], node['y']), NODE_RADIUS, 2
        )


def get_clicked_node(pos):
    for node in nodes:
        dx = pos[0] - node['x']
        dy = pos[1] - node['y']
        if dx * dx + dy * dy <= NODE_RADIUS * NODE_RADIUS:
            return node['id']
    return None


def save_links():
    with open(LINKS_FILE, 'w') as f:
        json.dump(sorted([list(link) for link in links]), f, indent=2)
    print('Saved links')


while running:
    draw()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                save_links()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = get_clicked_node(pygame.mouse.get_pos())
            if clicked is not None:
                if selected_node is None:
                    selected_node = clicked
                elif selected_node == clicked:
                    selected_node = None  # deselect
                else:
                    link = tuple(sorted((selected_node, clicked)))
                    if link in links:
                        links.remove(link)
                    else:
                        links.add(link)
                    selected_node = None

    clock.tick(60)

pygame.quit()
